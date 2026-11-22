#!/usr/bin/env python3
"""BM25 search over the wiki.

Usage:
    python3 tools/wiki-search.py "attention mechanism"
    python3 tools/wiki-search.py --limit 5 --all "transformer"

Requires tools/wiki-config.json with {"vault": "obsidian/<Name>"}.

Exit codes: 0 on results, 1 on no results, 2 on usage/setup error.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "wiki-config.json"

DEFAULT_DIRS = ("wiki", "raw")

K1 = 1.5
B = 0.75

TOKEN_RE = re.compile(r"[a-z0-9]+")
FM_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)


def load_vault() -> Path:
    if not CONFIG_PATH.is_file():
        print(
            f"missing {CONFIG_PATH.relative_to(ROOT)} — copy wiki-config.example.json "
            "to wiki-config.json and set vault path",
            file=sys.stderr,
        )
        sys.exit(2)
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"invalid wiki-config.json: {exc}", file=sys.stderr)
        sys.exit(2)
    rel = data.get("vault")
    if not rel or not isinstance(rel, str):
        print('wiki-config.json must contain "vault": "obsidian/<Name>"', file=sys.stderr)
        sys.exit(2)
    return (ROOT / rel).resolve()


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def strip_frontmatter(text: str) -> str:
    return FM_RE.sub("", text, count=1)


def load_documents(vault: Path, dirs: tuple[str, ...]) -> list[tuple[Path, str]]:
    docs: list[tuple[Path, str]] = []
    for d in dirs:
        root = vault / d
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            if "templates" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            docs.append((path, strip_frontmatter(text)))
    return docs


def search(query: str, docs, limit: int) -> list[tuple[float, Path, str]]:
    q_tokens = tokenize(query)
    if not q_tokens:
        return []

    tokenized = [tokenize(text) for _, text in docs]
    doc_lens = [len(t) for t in tokenized]
    avgdl = sum(doc_lens) / len(doc_lens) if doc_lens else 0.0
    n_docs = len(docs)

    df: Counter[str] = Counter()
    for toks in tokenized:
        unique = set(toks)
        for q in set(q_tokens):
            if q in unique:
                df[q] += 1

    idf = {
        q: math.log(1 + (n_docs - df[q] + 0.5) / (df[q] + 0.5)) for q in set(q_tokens)
    }

    results: list[tuple[float, Path, str]] = []
    for (path, _), toks, dl in zip(docs, tokenized, doc_lens):
        if not toks:
            continue
        tf = Counter(toks)
        score = 0.0
        for q in q_tokens:
            if tf[q] == 0:
                continue
            denom = tf[q] + K1 * (1 - B + B * dl / avgdl)
            score += idf[q] * tf[q] * (K1 + 1) / denom
        if score > 0:
            results.append((score, path, _))

    results.sort(key=lambda r: r[0], reverse=True)
    return results[:limit]


def snippet(text: str, query: str, width: int = 160) -> str:
    terms = set(tokenize(query))
    best, best_hits = "", -1
    for line in text.splitlines():
        hits = len(terms & set(tokenize(line)))
        if hits > best_hits and line.strip():
            best, best_hits = line.strip(), hits
    if not best:
        return ""
    return best if len(best) <= width else best[: width - 1].rstrip() + "…"


def main() -> int:
    ap = argparse.ArgumentParser(description="BM25 search over the wiki.")
    ap.add_argument("query", nargs="+", help="search terms")
    ap.add_argument("--limit", "-n", type=int, default=10, help="max results (default 10)")
    ap.add_argument(
        "--all",
        action="store_true",
        help="search raw/ as well as wiki/ (default: wiki only)",
    )
    args = ap.parse_args()

    vault = load_vault()
    if not vault.is_dir():
        print(f"vault not found: {vault}", file=sys.stderr)
        return 2

    query = " ".join(args.query)
    dirs = DEFAULT_DIRS if args.all else ("wiki",)
    docs = load_documents(vault, dirs)
    if not docs:
        print(f"no markdown files under {', '.join(dirs)}", file=sys.stderr)
        return 1

    hits = search(query, docs, args.limit)
    if not hits:
        print(f"no results for {query!r}")
        return 1

    for score, path, text in hits:
        rel = path.relative_to(vault)
        print(f"{score:6.2f}  {rel}")
        snip = snippet(text, query)
        if snip:
            print(f"        {snip}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
