#!/usr/bin/env bash
# FR-IF-07 / T0.2.5 -- a change under msg/ or srv/ requires a version bump.
#
# Consumers pin a tag (FR-IF-04). A message that changes shape under an
# unchanged version number is a contract break that no consumer can detect,
# which is precisely the failure this repository exists to prevent.
#
# Usage: check-version-bump.sh <base-ref>
set -euo pipefail

base="${1:?usage: check-version-bump.sh <base-ref>}"

changed="$(git diff --name-only "$base"...HEAD -- msg/ srv/)"
if [[ -z "$changed" ]]; then
  echo "No interface files changed; version bump not required."
  exit 0
fi

echo "Interface files changed:"
sed 's/^/  /' <<< "$changed"

read_version() { sed -n 's:.*<version>\(.*\)</version>.*:\1:p' "$1" | head -1; }

head_version="$(read_version package.xml)"
base_version="$(git show "$base:package.xml" | sed -n 's:.*<version>\(.*\)</version>.*:\1:p' | head -1)"

echo "package.xml version: $base_version (base) -> $head_version (head)"

if [[ "$head_version" == "$base_version" ]]; then
  cat >&2 <<MSG

FR-IF-07 violation: msg/ or srv/ changed but package.xml <version> is unchanged.

  Field or message addition        -> minor bump
  Rename, removal, or type change  -> MAJOR bump, and CHANGELOG.md must name
                                      every affected consumer (FR-IF-05)

MSG
  exit 1
fi

if ! git diff --quiet "$base"...HEAD -- CHANGELOG.md; then
  echo "CHANGELOG.md updated. OK."
else
  echo "::warning::package.xml was bumped but CHANGELOG.md was not touched (FR-IF-05)."
fi
