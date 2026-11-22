# EXAMPLE — Compiled wiki vs query-time RAG

> Seed source for the vault. Safe to leave in place after install; delete once you have real sources. The agent should treat this like any other `raw/` file.

## Claim

Most LLM-over-documents setups re-discover knowledge on every question: retrieve chunks, synthesize, discard the synthesis. A compiled wiki does the opposite — when a source arrives, the maintainer integrates it into durable pages (entities, concepts, contradictions) so later questions start from an already-linked artifact.

## What stays different

- **Compiled knowledge (wiki):** explicit pages, wikilinks, human-readable history, citation chains back to immutable raw files.
- **Query-time RAG:** fast over a corpus you have not curated; weak at accumulating synthesis and flagging contradictions across sessions.
- **Associative memory (e.g. Hindsight):** soft links, consolidation, and recall of short sticky facts — not a substitute for either of the above.

## Practical loop

1. Drop a source into `raw/` (immutable).
2. Ingest: write a source page, update only the concept/entity pages the source clearly touches.
3. Query from `index.md` (and search if needed); file hard-won answers as comparison/analysis pages.
4. Lint for orphans, dead links, and pages missing from the index.
