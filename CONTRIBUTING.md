# Contributing

PRs welcome.

- Keep it project-agnostic and English.
- Don’t vendor Hindsight — point at official Obsidian / `hindsight-cursor`.
- Missions in `~/.hindsight/cursor.json` stay global: no company or vault names.
- After edits, seed vault should pass `python3 tools/wiki-lint.py` (local `tools/wiki-config.json` → `obsidian/{{PROJECT}}`).
- Don’t commit `tools/wiki-config.json` or `hindsight-session.mdc`.
