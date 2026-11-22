---
type: concept
title: Compiled Knowledge
created: 2026-11-22
updated: 2026-11-22
status: draft
confidence: medium
sources: ["[[Compiled Wiki vs RAG]]"]
tags: [example, wiki]
---

# Compiled Knowledge

_Durable, explicitly linked notes that an LLM maintains between you and immutable raw sources._

## What it is

Instead of answering every question by retrieving raw chunks, the agent integrates each source into wiki pages — concepts, entities, comparisons — and keeps those pages current. The synthesis lives in the vault; later queries start from `index.md` and existing links.

## Why it matters

Cross-source contradictions and entity facts compound over time instead of being rediscovered. Obsidian is the IDE; the agent is the maintainer; `raw/` stays immutable.

## Mechanics

Ingest writes a [[Compiled Wiki vs RAG|source page]] and updates only pages the source clearly touches. Queries cite `[[wikilinks]]`. Hard-won answers become comparison/analysis pages. Lint catches orphans and index gaps.

## Open questions

- When does a single vault’s `index.md` stop being scannable enough?

## Related

- [[Query-time RAG]]
- [[Associative Memory]]

## Sources

- [[Compiled Wiki vs RAG]]
