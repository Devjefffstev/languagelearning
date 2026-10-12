---
paths:
  - "apps/cli-py/**/*.py"
  - "**/test_*.py"
  - "**/*_test.py"
---

# Python testing conventions

<!--
This is a STARTER .claude/rules/testing.md.
The `paths:` field above is YAML frontmatter that Claude Code parses when
loading rules. This rule loads only when the user is editing files that
match one of those glob patterns — saving context budget and avoiding
irrelevant instructions in other contexts.

Replace every TODO below.
-->

## Frameworks

TODO: pytest, unittest, or something else? List plugin versions if they're
pinned (e.g., `pytest>=8`, `pytest-asyncio>=0.23`).

## Required patterns

TODO: each new test file MUST:
- start with `from __future__ import annotations`
- import the module under test as `from <package>.<module> import <thing>`
- define fixtures in `conftest.py`, not inline, unless they're truly local

TODO: each test function MUST:
- have a docstring explaining the scenario, not the implementation
- use `assert ...` with a human-readable message when intent is non-obvious
  - `assert result.status == "shipped", "fixture should produce shipped order"`
- be marked with `@pytest.mark.unit` or `@pytest.mark.integration` so the
  test selection flags work

## What NOT to do

TODO: list anti-patterns. Example:
- Do not use `time.sleep(...)` in tests — use `freezegun.freeze_time(...)`.
- Do not mock at the module level; mock at the boundary where the dependency
  is consumed.
- Do not write tests that depend on real network access. Use `vcrpy` or
  the project's recorded cassettes under `tests/cassettes/`.

## Coverage threshold

TODO: required minimum line coverage for any new code path?
E.g., "new branches must keep overall project coverage >= 90%."