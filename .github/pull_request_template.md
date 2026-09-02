## What changed

<!-- One or two sentences. What does this PR do, and why now? -->

## Requirements touched

<!-- e.g. FR-IF-03, FR-CN-67. Write "none" if this is pure housekeeping. -->

## Checklist

- [ ] `python3 scripts/generate.py` re-run and the generated files committed
- [ ] `<version>` bumped in `package.xml` **if** anything under `msg/` or `srv/` changed
- [ ] `CHANGELOG.md` updated, naming affected consumers if this is a breaking change (FR-IF-05)
- [ ] CI green
- [ ] No topic name typed as a literal string anywhere (FR-IF-03)

## Consumer impact

<!--
  Breaking change? Name every repo that must move its submodule pointer,
  and open the tracking issues before merging. Delete this section if additive.
-->
