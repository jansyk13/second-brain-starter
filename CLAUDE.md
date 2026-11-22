# CLAUDE.md

LLM Wiki + Hindsight. Read `AGENTS.md` first — schema, linking, ingest/query/lint. This file is just a pointer.

Language: English (abbreviations OK).

## Quick orientation

- Vault root: `obsidian/{{PROJECT}}/` — open in Obsidian.
- `obsidian/{{PROJECT}}/raw/` — **immutable** sources. Read only; never write.
- `obsidian/{{PROJECT}}/wiki/` — compiled wiki. You own this layer.
- Start session: `wiki/hot.md`, then `wiki/index.md`.
- Start query: `wiki/index.md`.

## Non-negotiables

- Never write to `raw/`.
- Edit `AGENTS.md` only with explicit approval.
- Every new page gets an `index.md` row in the same pass.
- Every edit bumps `updated` in frontmatter.
- Never silently overwrite a conflicting claim — use `> [!contradiction]`.
- File durable query answers into the wiki; do not leave them only in chat.

## Tools

```bash
python3 tools/wiki-search.py "attention mechanism"   # BM25 over wiki/
python3 tools/wiki-lint.py                            # structural health check
```

## Commands

| Phrase | Operation |
|---|---|
| "ingest `<file>`" | ingest procedure in `AGENTS.md` |
| "what do I know about X" | query procedure |
| "lint the wiki" | lint procedure |
