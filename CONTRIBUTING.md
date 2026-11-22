# Contributing

Issues and PRs welcome.

- Keep the kit **domain-agnostic** and **English-first**.
- Prefer **official** Obsidian and `hindsight-cursor` — do not vendor Hindsight.
- `~/.hindsight/cursor.json` guidance must stay **user-global** (no project/vault names in missions).
- Seed vault must pass `python3 tools/wiki-lint.py` after writing a local `tools/wiki-config.json` pointing at `obsidian/{{PROJECT}}`.
- Do not commit `tools/wiki-config.json` or `hindsight-session.mdc`.
