# Repository Guidelines

## Project Structure & Module Organization
Source material lives under `plugins/<plugin>/` with the canonical `agents/`, `commands/`, and `skills/` folders (example: `plugins/backend-development/agents/backend-architect.md`). Shared references are in `docs/` (`agents.md`, `plugins.md`, `usage.md`) and regenerated from repository metadata. Use `templates/` for new Markdown assets, keep automation helpers (`add-language-support*.py`, `scripts/generate-docs.py`) at the root, and store generated artifacts in `outputs/` or `reports/` to avoid cluttering plugin folders.

## Build, Test, and Development Commands
Use Python 3.11+ and run commands from the repo root:
```bash
python scripts/generate-docs.py           # Rebuild docs/ from plugins/*
python add-language-support.py --plugin backend-development --language es
python add-language-support-skills.py --plugin cloud-infrastructure
python add-language-support-commands.py --plugin security-scanning
```
Always run `python scripts/generate-docs.py` before every PR so docs stay in sync; the other helpers refresh localized resources whenever you add agents, skills, or commands.

## Coding Style & Naming Conventions
Agent, command, and skill definitions are Markdown with YAML frontmatter; keep keys lowercase-kebab (`name`, `description`, `model`). Stick to 4-space indentation for Python utilities, follow PEP 8, prefer descriptive snake_case, and keep filenames aligned with their agent or command slug so scanners remain deterministic.

## Testing Guidelines
Unit tests are light today, so validate metadata with targeted checks: run `python scripts/generate-docs.py`, preview the updated `docs/*.md`, and manually exercise affected `/plugin` workflows inside Claude Code. When shipping new Python behavior, add a small smoke test or reproducible instructions under `reports/` so reviewers can re-run your scenario.

## Commit & Pull Request Guidelines
Follow Conventional Commits (`feat: add ml orchestration agent`, `fix: correct marketplace stats`), keep subject lines under 72 characters, and link to relevant `docs/` sections in the body. PRs should summarize scope, list affected plugins or scripts, include screenshots or transcript snippets for UX shifts, and state that `python scripts/generate-docs.py` was run. Reference related issues and ping the owners noted in `docs/agents.md`.

## Agent & Plugin Update Checklist
Before publishing a new capability, confirm descriptions, models, and skills show up in `docs/agents.md`, add deployment guidance to the plugin README when outside steps are required, and refresh quick starts (`QUICKSTART.md`, `README.md`) if behavior changes. Keep each PR scoped to one plugin or orchestrator so reviewers can validate prompts and metadata without context switching.
