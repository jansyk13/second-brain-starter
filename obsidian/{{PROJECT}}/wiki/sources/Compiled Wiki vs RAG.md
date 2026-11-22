---
type: source
title: Compiled Wiki vs RAG
created: 2026-11-22
updated: 2026-11-22
status: draft
confidence: medium
sources: []
tags: [example, ingest]
---

# Compiled Wiki vs RAG

> [!info] Citation
> Seed example (Second Brain Starter). Not an external publication.
> Raw file: `raw/EXAMPLE-compiled-wiki-vs-rag.md`

## Summary

Teaching source that contrasts three layers: a compiled LLM wiki (durable, explicitly linked pages), query-time RAG (re-synthesize from chunks each ask), and associative memory (short sticky facts with soft recall). Used as the vault’s golden ingest so agents can see a complete raw → source → concepts → index/log/`hot` pass.

## Key claims

| Claim | Confidence | Notes |
|---|---|---|
| Wiki accumulates synthesis; RAG re-derives it | medium | Core pattern claim |
| Associative memory ≠ wiki | high | Different job; see [[Associative Memory]] |
| Ingest should update only clearly affected pages | medium | Avoid stub spam |

## What it changes

Establishes baseline concepts for this vault’s operating model. No contradictions with prior pages (seed).

## Pages touched

- [[Compiled Knowledge]]
- [[Associative Memory]]
- [[Query-time RAG]]

## Quotes

> A compiled wiki does the opposite — when a source arrives, the maintainer integrates it into durable pages … so later questions start from an already-linked artifact.
