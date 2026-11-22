# Second Brain Starter

Clone this, then install it into a project repo. You get an Obsidian LLM Wiki (Karpathy pattern) plus wiring for official Hindsight in Cursor.

MIT — see [LICENSE](LICENSE).

## What’s in the box

- Obsidian vault scaffold: `raw/` (you own it, immutable) and `wiki/` (agent-owned)
- Two Cursor rules: wiki ops, and Hindsight vs Obsidian boundaries
- `wiki-lint` / `wiki-search` (vault path in `tools/wiki-config.json`)
- Install skill + [`INSTALL.md`](INSTALL.md) — skill stays in this repo; it is not copied into targets

Install these yourself (not vendored here):

- [Obsidian](https://obsidian.md) (or `brew install --cask obsidian`)
- [hindsight-cursor](https://hindsight.vectorize.io/sdks/integrations/cursor) (`pip install` + `init`)

The template vault folder is literally `obsidian/{{PROJECT}}/`. Install renames it (e.g. `obsidian/Acme/`).

## Quick start

```bash
git clone https://github.com/jansyk13/second-brain-starter.git
```

1. Open **this** repo in Cursor (so `install-second-brain` is available).
2. Point the agent at your target project, e.g.:

> Install Second Brain Starter into `/path/to/my-project`. Project name: `MyProject`. Use official Obsidian and `hindsight-cursor`.

Or do it by hand with [`INSTALL.md`](INSTALL.md).

## Models (OpenRouter)

Ids change — pin whatever is current. The split we use:

| Role | Prefer | Where |
|---|---|---|
| Cursor / coding | Qwen | Cursor model picker |
| Hindsight retain | Qwen flash (e.g. `qwen/qwen3.7-flash`) | `~/.hindsight/cursor.json` + daemon `HINDSIGHT_API_LLM_*` |
| Consolidation LLM | GLM (e.g. `z-ai/glm-5.3-flash`) | daemon `HINDSIGHT_API_CONSOLIDATION_LLM_*` |
| Consolidation decisions | Jev (e.g. `typesafe/jev-1.14`) | daemon `HINDSIGHT_API_DECISION_MODEL_*` → `https://openrouter.ai/api` |
| Embeddings | e.g. `perplexity/pplx-embed-v1-0.6b` | daemon `HINDSIGHT_API_EMBEDDINGS_*` |
| Recall rerank | `rrf` (don’t use Jev for recall) | `HINDSIGHT_API_RERANKER_PROVIDER=rrf`, `RECALL_DECISION_MODEL_PROVIDER=none` |

Copy-paste configs: [`INSTALL.md`](INSTALL.md) §4b and [`examples/hindsight-profile.env.example`](examples/hindsight-profile.env.example).

## Needs

- Cursor, Python 3
- Obsidian + `hindsight-cursor` (see above)
- Local Hindsight daemon on `http://127.0.0.1:9077` unless you use cloud
- OpenRouter key for the model stack above
