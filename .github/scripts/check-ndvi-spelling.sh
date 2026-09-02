#!/usr/bin/env bash
# FR-IF-11 / T0.1.5 -- reject the misspelling of NDVI anywhere in the repo.
#
# The forbidden literal is assembled at runtime rather than written out, so
# that this script does not itself trip the check it enforces. For the same
# reason neither this file nor the allowlist has the misspelling in its name.
#
# NDVI is spelled correctly in code, topics, figures, prose, and variable names.
# This exists because a transposed topic name fails SILENTLY: the subscriber
# receives nothing and it presents as a dead sensor (C-13). The other two guards
# are the topic constants in topics/registry.yaml and the FR-CN-63 startup
# graph-conformance check.
#
# Paths listed in .ndvi-allow are skipped -- see that file for why bagwis-docs
# needs entries and the code repositories do not.
set -uo pipefail

root="$(git rev-parse --show-toplevel)"
cd "$root"

allow=()
if [[ -f .ndvi-allow ]]; then
  while IFS= read -r line; do
    line="${line%%#*}"
    line="$(echo "$line" | xargs)"
    [[ -n "$line" ]] && allow+=(":(exclude)$line")
  done < .ndvi-allow
fi

# git grep so .gitignore and .git/ are handled for us, and -I skips binaries.
# --untracked so a new file is caught before it is ever committed; ignored
# paths (node_modules/, build/) stay excluded either way.
needle="nvdi"

mapfile -t hits < <(
  git grep -I -n -i --untracked -e "$needle" -- \
    ':(exclude).github/scripts/check-ndvi-spelling.sh' \
    ':(exclude).ndvi-allow' \
    "${allow[@]+"${allow[@]}"}" || true
)

if (( ${#hits[@]} > 0 )); then
  echo "FR-IF-11 violation: NDVI is misspelled in ${#hits[@]} place(s)." >&2
  echo "NDVI is spelled correctly everywhere. A transposed topic name fails silently." >&2
  echo >&2
  printf '  %s\n' "${hits[@]}" >&2
  echo >&2
  echo "If an occurrence is a deliberate citation of the defect, add its path to .ndvi-allow." >&2
  exit 1
fi

echo "FR-IF-11 OK: NDVI spelled correctly throughout."
