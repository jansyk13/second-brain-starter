---
type: concept
title: Query-time RAG
created: 2026-11-22
updated: 2026-11-22
status: draft
confidence: medium
sources: ["[[Compiled Wiki vs RAG]]"]
tags: [example, retrieval]
---

# Query-time RAG

_Retrieve relevant chunks at ask time and synthesize an answer without accumulating a durable wiki layer._

## What it is

Classic LLM-over-documents: upload or index files, retrieve on each question, generate, discard the synthesis. Fast over uncurated corpora; weak at long-lived contradiction tracking and entity maintenance.

## Why it matters

Useful as a contrast class for this vault. The starter’s wiki layer exists because RAG alone does not compound.

## Mechanics

Chunk → embed/index → retrieve → generate. No requirement to update shared concept pages between questions.

## Open questions

- Hybrid setups (RAG over `raw/` plus a compiled wiki) — when worth it?

## Related

- [[Compiled Knowledge]]
- [[Associative Memory]]

## Sources

- [[Compiled Wiki vs RAG]]
