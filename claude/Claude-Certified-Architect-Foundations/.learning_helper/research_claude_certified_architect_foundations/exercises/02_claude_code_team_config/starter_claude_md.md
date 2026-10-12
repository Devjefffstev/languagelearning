# Project Conventions

<!--
This is a STARTER project-level CLAUDE.md for the team workflow exercise.
Replace every TODO below with your project's real conventions.

Key rules (covered by the exam):
  - This file is read at the start of every Claude Code session.
  - User-level (~/.claude/CLAUDE.md) is for personal settings only and is
    NOT shared with teammates via version control.
  - For path-scoped conventions, prefer .claude/rules/<area>.md with
    `paths:` YAML frontmatter instead of bloating this file.
  - Keep this file SHORT. Universal standards only.
-->

## Commit style

TODO: what is your team's commit-message convention? E.g., "Conventional
Commits, with scopes limited to the affected app (`api`, `cli`, `docs`)."
TODO: do you require signed commits, PR references, or any tooling hook?

## Testing

TODO: where do tests live? How do you run them? Example:
- `apps/api-ts`: `pnpm test`
- `apps/cli-py`: `pytest`
- `apps/docs-md`: link checker is `markdown-link-check docs/**/*.md`

## Code review

TODO: review checklist the team uses. Example:
- All new functions declared in a `.ts` file have explicit return types.
- Python files use `from __future__ import annotations` at the top.
- Markdown files preserve sentence-case headings.

## Things Claude should NEVER do without asking

TODO: list the constraints that are non-negotiable. Example:
- Do not run `pnpm install --force` or any command that modifies lockfiles.
- Do not edit `.env*` files.
- Do not push to `main` directly.

## Reference docs

TODO: link to the long-form docs your CLAUDE.md needs to reference. Use
`@import` only when the import short-circuits what Claude would otherwise
have to remember in full.
- @import docs/architecture/overview.md
- @import docs/runbooks/incident-response.md