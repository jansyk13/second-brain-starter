# raw/ — immutable sources

Articles, papers, transcripts, dumps, images. You put them here. The agent reads; it never edits this folder.

## Getting sources in

The fast path is [Obsidian Web Clipper](https://obsidian.md/clipper) — it turns a
web article into markdown and drops it here.

1. Install the Clipper browser extension.
2. Point it at this vault, folder `raw/`.
3. Clip an article. Download attachments so images land in `raw/assets/`.

Or drag a PDF or paste markdown by hand. Anything readable works.

## Then what

Tell the agent: `ingest raw/<filename>`.

A finished example already lives here: `EXAMPLE-compiled-wiki-vs-rag.md` (and matching wiki pages). Use it as the pattern; delete it when you have real sources.

## Rules

- Never edit a file here to fix a mistake — note the correction in the wiki page
  that cites it, so the discrepancy stays visible.
- Never delete a source the wiki cites. Move it to `raw/archive/` if you must.
- Filenames become source page titles. Descriptive is better than short.

## Layout

```
raw/
├── assets/     # images and attachments
└── *.md        # clipped articles and pasted text
```
