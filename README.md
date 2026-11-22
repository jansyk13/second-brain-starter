# Second Brain Starter

Cursor + Obsidian **LLM Wiki** + official **Hindsight** memory — a domain-agnostic starter you clone and install into a project repo.

License: [MIT](LICENSE).

## What you get

- Karpathy-style Obsidian wiki scaffold (`raw/` immutable, `wiki/` agent-owned)
- Thin Cursor rules: wiki ops + Hindsight↔Obsidian boundaries
- `wiki-lint` / `wiki-search` tools (vault path via `tools/wiki-config.json`)
- Install skill (lives in **this kit**, not copied into targets) + [`INSTALL.md`](INSTALL.md)

**Not included (use official installers instead):**

- Obsidian app → [obsidian.md](https://obsidian.md) (Homebrew cask on macOS; download for Windows/Linux)
- Hindsight Cursor plugin / hooks / MCP → [`hindsight-cursor init`](https://hindsight.vectorize.io/sdks/integrations/cursor)

The vault template path is literally `obsidian/{{PROJECT}}/` — `{{PROJECT}}` is a placeholder the install renames (e.g. to `obsidian/Acme/`).

## Quick start

```bash
git clone https://github.com/jansyk13/second-brain-starter.git
```

1. **Open this kit** as a Cursor workspace (so the `install-second-brain` skill is available).
2. Tell the agent the **target repo path** and project name, for example:

> Install Second Brain Starter into `/path/to/my-project`. Project name: `MyProject`. Prefer official Obsidian and `hindsight-cursor` setups.

Or follow [`INSTALL.md`](INSTALL.md) manually (kit root = this repository). The install skill is **not** copied into the target — only the wiki scaffold and rules are.

## Recommended models (OpenRouter)

Default preference for this kit — pin **current** OpenRouter ids (names move fast):

| Role | Prefer | Notes |
|---|---|---|
| **Cursor / coding agent** | **Qwen** | Pick in the Cursor model picker (OpenRouter / Qwen flash or coder SKU) |
| **Hindsight fact extract** | **GLM** (z.ai) | Set in `~/.hindsight/cursor.json` as `llmModel` (`z-ai/glm-*-flash` preferred) |
| **Routing / structured decisions** | **Jev** (TypeSafe) | [Jev](https://openrouter.ai/docs/guides/community/jev) / [Jev Router](https://openrouter.ai/docs/guides/routing/routers/jev-router) (`typesafe/jev-*`, `typesafe/jev-router`) when you want typed routing instead of a fixed chat model |

All three via [OpenRouter](https://openrouter.ai) + `OPENROUTER_API_KEY`. Details and example `cursor.json` in [`INSTALL.md`](INSTALL.md) §4b.

## Requirements

See [`INSTALL.md`](INSTALL.md):

- **Cursor**
- **Obsidian** (official) — open `obsidian/<PROJECT>/` as vault
- **Hindsight** (official `hindsight-cursor`) — local daemon on `http://127.0.0.1:9077` unless using cloud
- **Python 3** for wiki tools + `hindsight-cursor`
- **OpenRouter** with **Qwen + GLM + Jev** as above
