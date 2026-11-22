---
name: install-second-brain
description: >-
  Install Second Brain Starter (Obsidian LLM Wiki + Hindsight memory) into a
  target repo from a clone of this kit. Prefer official Obsidian and official
  hindsight-cursor. Use when the user asks to set up / install second brain,
  LLM wiki, Obsidian wiki, Karpathy wiki, or Hindsight memory wiring.
---

# Install Second Brain Starter

## When to use

User opens a clone of **second-brain-starter** as the Cursor workspace (or points at it) and asks to install into a **target repository**.

Follow `INSTALL.md` in the kit. **Favour official setups** — do not vendor or hand-copy Hindsight plugin/hooks/MCP from this kit. Do **not** copy this skill into the target; it stays in the kit only.

| Piece | How |
|---|---|
| Wiki scaffold | Copy from this kit (repo containing `INSTALL.md`) |
| Obsidian | Official app; open vault folder |
| Hindsight | Official `pip install hindsight-cursor` + `hindsight-cursor init` |

## Inputs

- **Target repo path** (cwd if already there)
- **PROJECT** name for `obsidian/<PROJECT>/` — ask if missing; default = target directory name; sanitize to filesystem-safe (`[A-Za-z0-9._-]+`)
- **Kit root** — directory containing `INSTALL.md` and `obsidian/{{PROJECT}}/` (the second-brain-starter clone)

## Procedure

### 1. Wiki scaffold (this kit only)

1. Confirm target path, kit root, and PROJECT name.
2. Copy from kit (merge; never delete unrelated files):
   - `AGENTS.md`, `CLAUDE.md` — skip overwrite of existing `AGENTS.md` unless user requests replace
   - `.cursor/rules/llm-wiki.mdc`
   - `.cursor/rules/hindsight-vs-obsidian.mdc` only (boundary rule)
   - `tools/wiki-lint.py`, `wiki-search.py`, `wiki-config.example.json`
   - `obsidian/{{PROJECT}}/` entire tree
3. **Do not** copy `.cursor-plugin/`, `.cursor/hooks.json`, or `.cursor/mcp.json` from the kit (official init owns those).
4. Rename `obsidian/{{PROJECT}}` → `obsidian/<PROJECT>`; substitute `{{PROJECT}}` in file contents.
5. Write `tools/wiki-config.json`: `{"vault": "obsidian/<PROJECT>"}`.
6. Merge wiki-related `.gitignore` entries from the kit (session mdc, wiki-config, Obsidian workspace/cache/plugins).

### 2. Obsidian (official)

1. Install Obsidian if missing (`brew install --cask obsidian` or [obsidian.md](https://obsidian.md)).
2. Ask user to **Open folder as vault** on absolute path `…/obsidian/<PROJECT>/` (not repo root).

### 3. Hindsight (official plugin)

1. In the **target** repo:
   ```bash
   pip install hindsight-cursor
   hindsight-cursor init
   ```
   Prefer local daemon (no `--api-url`) unless user asks for cloud/self-hosted.
2. Merge into `~/.hindsight/cursor.json` (user-global; create if missing) without wiping existing keys — follow `INSTALL.md` §4b:
   - `useLocalDaemon: true`, empty `hindsightApiUrl`, `apiPort: 9077`, agnostic missions
   - Retain LLM: **Qwen** (`llmProvider: "openrouter"`, `llmModel: "qwen/qwen3.7-flash"` or current Qwen flash, `llmApiKeyEnv: "OPENROUTER_API_KEY"`)
3. Apply daemon profile env from `examples/hindsight-profile.env.example` / `INSTALL.md` §4b (consolidation **GLM** + **Jev**, embeddings, `rrf` rerank; Jev off for recall). Restart daemon.
4. Probe `curl -sf http://127.0.0.1:9077/health`. If down: ensure `uv`/`uvx` + API key; allow plugin auto-start or run official embed start commands from `INSTALL.md` §4c.
5. Remind user to **fully quit and reopen Cursor**. Cursor/coding model: **Qwen** in the picker.

### 4. Verify + handoff

1. `python3 tools/wiki-lint.py` → clean
2. Confirm `.cursor-plugin/hindsight-memory/` exists (from official init)
3. Confirm Obsidian vault path + Hindsight health
4. Point user to fill Project identity in `AGENTS.md`
5. Append to `obsidian/<PROJECT>/wiki/log.md`:
   `## [YYYY-MM-DD] install | Second Brain Starter + official Hindsight Cursor plugin`

## Done when

- Vault exists, Obsidian can open it, lint is clean
- Hindsight installed via **official** `hindsight-cursor init` (not a vendored copy)
- Local health check passes at `http://127.0.0.1:9077` (unless user chose cloud)
