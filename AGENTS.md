# LLM Wiki — Agent Contract

Brought in by Second Brain Starter.

Karpathy-style LLM Wiki: you curate `raw/`, the agent maintains `wiki/`, Obsidian is the editor.

> Fill in Project identity after install. Don’t change the schema below without explicit approval.

Working language: English (domain abbreviations OK). Frontmatter keys stay English. Don’t dump Hindsight memories back into the vault as if they were sources.

---

## 1. Project identity

| Field | Value |
|---|---|
| Project | `{{PROJECT}}` |
| Purpose | _What this knowledge base is for_ |
| Owner | _Who curates raw/ and decisions_ |
| Domain notes | _Optional ICP, stack, constraints_ |

---

## 2. Knowledge architecture

| System | Role |
|---|---|
| **Obsidian** (`obsidian/{{PROJECT}}/`) | Long-form notes, research, playbooks |
| **Hindsight** | Short cross-session memory (official `hindsight-cursor`) |
| **Cursor** | Agent; hooks/MCP from official init |

Don’t paste whole wiki pages into Hindsight. Don’t rebuild the vault from memory snippets. Long writeups → wiki; decisions/prefs → Hindsight.

Session start: `wiki/hot.md`, then `wiki/index.md`. Topic switch: `recall`, then index/search.

---

## 3. LLM Wiki schema

### Layout

```
repo/
├── AGENTS.md                      # this contract (edit only with explicit approval)
├── CLAUDE.md                      # short pointer
├── tools/                         # wiki-search.py, wiki-lint.py, wiki-config.json
└── obsidian/{{PROJECT}}/          # vault root (wikilinks are vault-absolute by filename)
    ├── raw/                       # LAYER 1 — human, immutable
    └── wiki/                      # LAYER 2 — agent-owned
        ├── index.md               # catalog — read FIRST on every query
        ├── log.md                 # append-only activity log
        ├── hot.md                 # ~500 words current context
        ├── overview.md
        ├── dashboard.md
        ├── sources/ concepts/ entities/ comparisons/ analyses/ slides/ templates/
```

| Layer | Path | Rule |
|---|---|---|
| Raw | `raw/` | **Immutable.** Never write, rename, or delete. |
| Wiki | `wiki/` | Agent creates and maintains. |
| Schema | `AGENTS.md` | Human-owned. Propose changes; wait for approval. |

**Non-negotiables:** every new page gets an `index.md` row in the same pass; every edit bumps `updated`; never silently overwrite conflicting claims—use `> [!contradiction]`; citation chains terminate in `raw/` via a `sources/` page.

### Frontmatter

Required on every wiki page except `index.md`, `log.md`, `hot.md`, `dashboard.md`:

```yaml
---
type: concept            # source | concept | entity | comparison | analysis | slide | overview
title: Example
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft            # stub | draft | stable
confidence: medium       # low | medium | high
sources: ["[[Source Page]]"]
tags: [lowercase-hyphenated]
---
```

Do not invent new `type` / `status` values without proposing in `log.md` and waiting for approval.

### Linking

`[[Wikilinks]]` inside the vault; `[text](https://url)` for external only. Link generously. In tables escape aliases: `[[Note\|Alias]]`.

### Operations

| Phrase | Action |
|---|---|
| **ingest `<file>`** | Read `raw/` source → discuss takeaways (unless batch) → write `wiki/sources/` page → update ~10–15 affected pages → `index.md` + `hot.md` → append `log.md` → bump `updated`. |
| **query / what do I know about X** | Read `index.md` → optional `python3 tools/wiki-search.py "<terms>"` → answer with `[[citations]]` → file durable answers to `comparisons/` or `analyses/` → log gaps. |
| **lint the wiki** | `python3 tools/wiki-lint.py` + judgment (contradictions, staleness, missing pages, gaps) → file `wiki/analyses/Lint YYYY-MM-DD.md` → fix mechanical issues; ask before resolving substantive contradictions. |

`index.md`: grouped by type, alphabetical rows, one concrete retrieval-oriented summary line each.

`log.md`: append-only, newest at bottom, prefix `## [YYYY-MM-DD] ingest|query|lint|gap | …`.

`hot.md`: ≤~500 words, rewritten (not appended) when working context changes.

### Style

Plain markdown; prose in concept articles; tables for comparisons; callouts for attention. State uncertainty explicitly. Prefer filing knowledge into the wiki over leaving it in chat.

```markdown
> [!contradiction] Conflicting claim
> Source A says X; [[Source B]] says Y. Unresolved.
```
