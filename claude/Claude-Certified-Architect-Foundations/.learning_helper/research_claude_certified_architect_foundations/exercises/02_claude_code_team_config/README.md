# Exercise 2 — Configure Claude Code for a team workflow

**Difficulty:** Medium
**Domains reinforced:** Domain 3 (Claude Code Configuration & Workflows), Domain 2 (Tool Design & MCP Integration)

## Goal

Build a Claude Code configuration for a fictional three-language monorepo (TypeScript API, Python CLI, Markdown docs) that meets the standard the official Exam Guide sets in §8 Exercise 2. **No Python file to edit** — Claude Code's configuration is mostly well-formatted markdown and JSON.

## Task

You're standing in a project root with this layout:

```
your-project/
├── apps/
│   ├── api-ts/        # Express + TypeScript
│   ├── cli-py/        # Python CLI
│   └── docs-md/       # Markdown content
```

A new team member clones the repo tomorrow. Right now they get no conventions from Claude at all. Your job is to fix that **without making every rule load on every keystroke**. You will create:

1. A project-level `CLAUDE.md` (in the project root or `.claude/`) covering universal standards (commit style, test command, code review etiquette).
2. **At least two** rule files under `.claude/rules/` with YAML frontmatter `paths:` using **glob patterns** that conditionally apply conventions to:
   - TypeScript files (`apps/api-ts/**/*.{ts,tsx}`) — function-as-default-export style
   - Python files (`apps/cli-py/**/*.py`) — pytest conventions, type hints required
3. **At least one** project-scoped skill in `.claude/skills/` with a `SKILL.md` that has frontmatter setting **`context: fork`** and **`allowed-tools`** (you decide which tools to whitelist). The skill should run a verbose "explain a folder" analysis without polluting the main conversation.
4. A project-scoped `.mcp.json` with one MCP server entry referencing an environment variable for the API token (use `${GITHUB_TOKEN}` or similar).
5. Bonus: a directory-level `CLAUDE.md` inside `apps/docs-md/` for content-specific voice rules.

You only need to author the files — Claude Code will discover them automatically when you run `claude` in that folder.

Two starter files ship in this folder to show you the frontmatter shape:

- `starter_claude_md.md` — the universal CLAUDE.md skeleton with `TODO` markers
- `starter_testing_rule.md` — a path-scoped rule skeleton with `TODO` markers

Make a working copy of each in your own project root, replace the `TODO` markers with real content, and add the missing files (`.claude/rules/`, `.claude/skills/`, `.mcp.json`, etc.) yourself.

## Hints

1. Exam point worth knowing cold: **path-scoped rules load only when editing matching files**, which is why they save context budget compared with one giant `CLAUDE.md`. Use glob patterns like `apps/api-ts/**/*` rather than relying on directory names.
2. `context: fork` on a skill means the skill runs in an isolated sub-agent — its verbose output does not consume the main conversation's context. Use this for any skill that produces a lot of output (codebase analysis, brainstorming).
3. `allowed-tools` in skill frontmatter should be the **minimum necessary tools**. For a "review this folder" skill you might allow `Read, Glob, Grep` but not `Write` or `Bash`.
4. `.mcp.json` syntax: `"mcpServers": { "name": { "command": "npx", "args": [...], "env": { "TOKEN": "${GITHUB_TOKEN}" } } }`. Environment expansion means you never commit the secret.
5. If you forget the YAML frontmatter on a rule file, Claude Code silently ignores it.

## Success criteria

When you `cd` into your own project root and run `claude`, you should observe:

- The universal standards from `CLAUDE.md` apply to every request.
- Editing a TypeScript file under `apps/api-ts/` triggers the TypeScript rule's conventions.
- Editing a Python file under `apps/cli-py/` triggers the pytest / type-hint rule.
- Editing a Markdown file in `apps/docs-md/` triggers the directory-level `CLAUDE.md` voice rules.
- Invoking `/your-skill-name` runs the skill in a forked context (you can verify by inspecting the response — fork skills return a summary, not the full verbose output).
- Running `cat .mcp.json` shows the env-expanded token reference. `claude` should connect to the MCP server automatically (warning logged but no crash if the binary isn't installed in your sandbox).

If `/memory` shows all your files and `/rules` lists the path-scoped rules, you're set.