#!/usr/bin/env python3
"""Generate topic constants and TypeScript declarations from one source.

FR-IF-03 requires topic names to be defined once and imported everywhere;
FR-IF-06 requires TypeScript declarations so the dashboard type-checks message
shapes at build time. This script satisfies both from two inputs -- topics/
registry.yaml and the .msg/.srv files -- and emits:

    include/bagwis_interfaces/topics.hpp   C++
    python/topics.py                       Python
    ts/topics.ts                           TypeScript constants
    ts/msg/*.ts, ts/srv/*.ts               TypeScript message shapes
    ts/index.ts                            barrel

Output is COMMITTED to git. bagwis-web is a static Next.js export with no
colcon, so it can only consume files literally present in the submodule tree
(FR-WEB-09). CI regenerates and runs `git diff --exit-code` to prove the
committed output still matches the source.

Standard library only, on purpose: this runs inside CMake during colcon build
on the Pi, where adding pyyaml as a build dependency would be one more thing
that can be missing at the riverbank.

Usage:
    generate.py [--root DIR] [--check]

    --check  regenerate into memory and exit 1 if anything on disk differs,
             without writing. Used by CI and by the CMake build.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BANNER_LINES = [
    "THIS FILE IS GENERATED. DO NOT EDIT.",
    "",
    "Source:    topics/registry.yaml and msg/*.msg",
    "Generator: scripts/generate.py",
    "",
    "Edit the source and re-run scripts/generate.py. CI fails if the committed",
    "output does not match what the generator produces (FR-IF-03, FR-IF-06).",
]


# --------------------------------------------------------------------------
# A deliberately small YAML reader.
#
# registry.yaml is written as a flat subset -- a scalar, then two top-level
# sequences of string-valued mappings, with inline [a, b] lists. That is the
# whole grammar, and handling it here costs less than a build dependency.
# Anything outside the subset raises rather than being silently misread.
# --------------------------------------------------------------------------

def parse_registry(text: str) -> dict:
    root: dict = {}
    current_list: list | None = None
    current_item: dict | None = None

    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip())
        stripped = line.strip()

        if indent == 0:
            if not stripped.endswith(":") and ":" not in stripped:
                raise ValueError(f"{lineno}: expected 'key:' or 'key: value'")
            key, _, value = stripped.partition(":")
            key, value = key.strip(), value.strip()
            if value:
                root[key] = _scalar(value)
                current_list, current_item = None, None
            else:
                current_list = []
                root[key] = current_list
                current_item = None
            continue

        if current_list is None:
            raise ValueError(f"{lineno}: indented line outside any sequence")

        if stripped.startswith("- "):
            current_item = {}
            current_list.append(current_item)
            stripped = stripped[2:].strip()

        if current_item is None:
            raise ValueError(f"{lineno}: mapping entry before any '-' item")

        key, sep, value = stripped.partition(":")
        if not sep:
            raise ValueError(f"{lineno}: expected 'key: value', got {stripped!r}")
        current_item[key.strip()] = _scalar(value.strip())

    return root


def _scalar(value: str):
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [v.strip() for v in inner.split(",")] if inner else []
    if value.isdigit():
        return int(value)
    return value


# --------------------------------------------------------------------------
# .msg / .srv parsing
# --------------------------------------------------------------------------

PRIMITIVE_TS = {
    "bool": "boolean",
    "byte": "number",
    "char": "number",
    "int8": "number",
    "uint8": "number",
    "int16": "number",
    "uint16": "number",
    "int32": "number",
    "uint32": "number",
    "int64": "number",
    "uint64": "number",
    "float32": "number",
    "float64": "number",
    "string": "string",
    "wstring": "string",
}

# Message types from other packages that our fields reference. Declared here as
# TypeScript shims rather than pulled from a generator, because the dashboard
# has no ROS toolchain and these three shapes have been stable for a decade.
EXTERNAL_TS = {
    "std_msgs/Header": "Header",
    "geographic_msgs/GeoPoint": "GeoPoint",
    "builtin_interfaces/Time": "Time",
}


class Field:
    def __init__(self, type_str: str, name: str, comment: str):
        self.raw_type = type_str
        self.name = name
        self.comment = comment
        base = type_str
        self.is_array = False
        if "[" in base:
            base = base[: base.index("[")]
            self.is_array = True
        self.base_type = base


class Constant:
    def __init__(self, type_str: str, name: str, value: str, comment: str):
        self.type = type_str
        self.name = name
        self.value = value
        self.comment = comment


def parse_msg(path: Path) -> tuple[list[Constant], list[Field]]:
    constants: list[Constant] = []
    fields: list[Field] = []
    for raw in path.read_text().splitlines():
        body, _, comment = raw.partition("#")
        body = body.strip()
        comment = comment.strip()
        if not body:
            continue
        parts = body.split(None, 1)
        if len(parts) != 2:
            raise ValueError(f"{path.name}: cannot parse line {raw!r}")
        type_str, rest = parts[0], parts[1].strip()
        if "=" in rest:
            name, _, value = rest.partition("=")
            constants.append(Constant(type_str, name.strip(), value.strip(), comment))
        else:
            fields.append(Field(type_str, rest.split()[0], comment))
    return constants, fields


def parse_srv(path: Path) -> tuple[list[Field], list[Field]]:
    text = path.read_text()
    if "---" not in text:
        raise ValueError(f"{path.name}: service has no '---' separator")
    request_text, _, response_text = text.partition("---")
    return _fields_from_text(request_text), _fields_from_text(response_text)


def _fields_from_text(text: str) -> list[Field]:
    fields = []
    for raw in text.splitlines():
        body, _, comment = raw.partition("#")
        body = body.strip()
        if not body:
            continue
        parts = body.split(None, 1)
        if len(parts) != 2 or "=" in parts[1]:
            continue
        fields.append(Field(parts[0], parts[1].strip().split()[0], comment.strip()))
    return fields


# --------------------------------------------------------------------------
# Emitters
# --------------------------------------------------------------------------

def banner(prefix: str) -> str:
    return "\n".join((prefix + " " + l).rstrip() for l in BANNER_LINES)


def emit_hpp(registry: dict) -> str:
    out = ["// " + l if l else "//" for l in BANNER_LINES]
    out += [
        "",
        "#ifndef BAGWIS_INTERFACES__TOPICS_HPP_",
        "#define BAGWIS_INTERFACES__TOPICS_HPP_",
        "",
        "namespace bagwis",
        "{",
        "namespace topics",
        "{",
        "",
    ]
    for t in registry["topics"]:
        if t.get("note"):
            out.append(f"/// {t['note']}")
        out.append(f"/// Type: {t['type']}")
        out.append(f'inline constexpr char {t["const"]}[] = "{t["name"]}";')
        out.append("")
    out += ["}  // namespace topics", "", "namespace services", "{", ""]
    for s in registry["services"]:
        out.append(f"/// Type: {s['type']}")
        out.append(f'inline constexpr char {s["const"]}[] = "{s["name"]}";')
        out.append("")
    out += [
        "}  // namespace services",
        "}  // namespace bagwis",
        "",
        "#endif  // BAGWIS_INTERFACES__TOPICS_HPP_",
        "",
    ]
    return "\n".join(out)


def emit_py(registry: dict) -> str:
    out = ['"""' + BANNER_LINES[0]]
    out += BANNER_LINES[1:]
    out += ['"""', "", "from __future__ import annotations", ""]

    out.append("# --- Topics ---")
    out.append("")
    for t in registry["topics"]:
        if t.get("note"):
            out.append(f"# {t['note']}")
        out.append(f"#: {t['type']}")
        out.append(f'{t["const"]} = "{t["name"]}"')
        out.append("")

    out.append("# --- Services ---")
    out.append("")
    for s in registry["services"]:
        out.append(f"#: {s['type']}")
        out.append(f'{s["const"]} = "{s["name"]}"')
        out.append("")

    out += [
        "# Machine-readable form, consumed by the startup graph-conformance check",
        "# (FR-CN-63), which compares `ros2 topic list` against these entries and",
        "# fails loudly on a mismatch rather than presenting as a dead sensor.",
        "TOPICS = {",
    ]
    for t in registry["topics"]:
        subs = ", ".join(f'"{s}"' for s in t.get("subscribers", []))
        out += [
            f'    "{t["const"]}": {{',
            f'        "name": "{t["name"]}",',
            f'        "type": "{t["type"]}",',
            f'        "publisher": "{t["publisher"]}",',
            f'        "subscribers": [{subs}],',
            f'        "qos": "{t["qos"]}",',
            "    },",
        ]
    out += ["}", "", "SERVICES = {"]
    for s in registry["services"]:
        out += [
            f'    "{s["const"]}": {{',
            f'        "name": "{s["name"]}",',
            f'        "type": "{s["type"]}",',
            f'        "server": "{s["server"]}",',
            "    },",
        ]
    out += ["}", ""]
    return "\n".join(out)


def emit_ts_topics(registry: dict) -> str:
    out = ["// " + l if l else "//" for l in BANNER_LINES]
    out.append("")
    for t in registry["topics"]:
        if t.get("note"):
            out.append(f"/** {t['note']} */")
        out.append(f"/** Type: `{t['type']}` */")
        out.append(f'export const {t["const"]} = "{t["name"]}" as const;')
        out.append("")
    for s in registry["services"]:
        out.append(f"/** Type: `{s['type']}` */")
        out.append(f'export const {s["const"]} = "{s["name"]}" as const;')
        out.append("")
    out += [
        "/** Every topic name, for exhaustiveness checks and the mock harness. */",
        "export const ALL_TOPICS = [",
    ]
    out += [f"  {t['const']}," for t in registry["topics"]]
    out += ["] as const;", "", "export type TopicName = (typeof ALL_TOPICS)[number];", ""]
    return "\n".join(out)


def ts_type(field: Field, local_names: set[str]) -> str:
    base = field.base_type
    if base in PRIMITIVE_TS:
        ts = PRIMITIVE_TS[base]
    elif base in EXTERNAL_TS:
        ts = EXTERNAL_TS[base]
    elif base in local_names:
        ts = base
    else:
        raise ValueError(f"unmapped type {base!r}")
    return ts + "[]" if field.is_array else ts


def ts_imports(
    fields: list[Field], local_names: set[str], self_name: str, msg_dir: str = "."
) -> list[str]:
    """Import lines for a generated TypeScript file.

    msg_dir is the path from the emitted file back to ts/msg -- "." for files in
    ts/msg itself, "../msg" for the service files in ts/srv.
    """
    external, local = set(), set()
    for f in fields:
        if f.base_type in EXTERNAL_TS:
            external.add(EXTERNAL_TS[f.base_type])
        elif f.base_type in local_names and f.base_type != self_name:
            local.add(f.base_type)
    lines = []
    if external:
        lines.append(
            f'import type {{ {", ".join(sorted(external))} }} '
            f'from "{msg_dir}/_external";'
        )
    for name in sorted(local):
        lines.append(f'import type {{ {name} }} from "{msg_dir}/{name}";')
    return lines


def emit_ts_msg(name: str, constants, fields, local_names) -> str:
    out = ["// " + l if l else "//" for l in BANNER_LINES]
    out.append("")
    imports = ts_imports(fields, local_names, name)
    if imports:
        out += imports + [""]
    for c in constants:
        doc = f"  /** {c.comment} */" if c.comment else None
        if doc:
            out.append(doc.strip())
        out.append(f"export const {name}_{c.name} = {c.value};")
    if constants:
        out.append("")
    out.append(f"export interface {name} {{")
    for f in fields:
        if f.comment:
            out.append(f"  /** {f.comment} */")
        out.append(f"  {f.name}: {ts_type(f, local_names)};")
    out += ["}", ""]
    return "\n".join(out)


def emit_ts_srv(name: str, request, response, local_names) -> str:
    out = ["// " + l if l else "//" for l in BANNER_LINES]
    out.append("")
    imports = ts_imports(request + response, local_names, name, "../msg")
    if imports:
        out += imports + [""]
    for suffix, fields in (("Request", request), ("Response", response)):
        out.append(f"export interface {name}{suffix} {{")
        for f in fields:
            if f.comment:
                out.append(f"  /** {f.comment} */")
            out.append(f"  {f.name}: {ts_type(f, local_names)};")
        out += ["}", ""]
    return "\n".join(out)


def emit_ts_external() -> str:
    out = ["// " + l if l else "//" for l in BANNER_LINES]
    out += [
        "//",
        "// Shapes owned by other ROS packages. Declared here rather than generated,",
        "// because the dashboard has no ROS toolchain to generate them from and these",
        "// three definitions are stable across every ROS 2 distribution.",
        "",
        "/** builtin_interfaces/Time */",
        "export interface Time {",
        "  sec: number;",
        "  nanosec: number;",
        "}",
        "",
        "/** std_msgs/Header -- stamp is the time of physical measurement (FR-IF-08). */",
        "export interface Header {",
        "  stamp: Time;",
        "  frame_id: string;",
        "}",
        "",
        "/** geographic_msgs/GeoPoint -- WGS84. */",
        "export interface GeoPoint {",
        "  latitude: number;",
        "  longitude: number;",
        "  altitude: number;",
        "}",
        "",
    ]
    return "\n".join(out)


def emit_ts_index(msg_names, srv_names) -> str:
    out = ["// " + l if l else "//" for l in BANNER_LINES]
    out += ["", 'export * from "./topics";', 'export * from "./msg/_external";']
    out += [f'export * from "./msg/{n}";' for n in msg_names]
    out += [f'export * from "./srv/{n}";' for n in srv_names]
    out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------

def build(root: Path) -> dict[Path, str]:
    registry = parse_registry((root / "topics" / "registry.yaml").read_text())

    msg_paths = sorted((root / "msg").glob("*.msg"))
    srv_paths = sorted((root / "srv").glob("*.srv"))
    local_names = {p.stem for p in msg_paths}

    outputs: dict[Path, str] = {
        root / "include" / "bagwis_interfaces" / "topics.hpp": emit_hpp(registry),
        root / "python" / "topics.py": emit_py(registry),
        root / "ts" / "topics.ts": emit_ts_topics(registry),
        root / "ts" / "msg" / "_external.ts": emit_ts_external(),
    }

    for p in msg_paths:
        constants, fields = parse_msg(p)
        outputs[root / "ts" / "msg" / f"{p.stem}.ts"] = emit_ts_msg(
            p.stem, constants, fields, local_names
        )

    for p in srv_paths:
        request, response = parse_srv(p)
        outputs[root / "ts" / "srv" / f"{p.stem}.ts"] = emit_ts_srv(
            p.stem, request, response, local_names
        )

    outputs[root / "ts" / "index.ts"] = emit_ts_index(
        [p.stem for p in msg_paths], [p.stem for p in srv_paths]
    )
    return outputs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--check", action="store_true", help="verify without writing")
    args = ap.parse_args()

    outputs = build(args.root)

    if args.check:
        stale = [
            p for p, content in outputs.items()
            if not p.exists() or p.read_text() != content
        ]
        if stale:
            print("Generated output is stale. Run scripts/generate.py:", file=sys.stderr)
            for p in stale:
                print(f"  {p.relative_to(args.root)}", file=sys.stderr)
            return 1
        print(f"{len(outputs)} generated files are up to date.")
        return 0

    for path, content in sorted(outputs.items()):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    print(f"Generated {len(outputs)} files from topics/registry.yaml and msg/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
