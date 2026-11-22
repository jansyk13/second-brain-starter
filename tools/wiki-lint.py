#!/usr/bin/env python3
"""Structural lint for the wiki.

Usage:
    python3 tools/wiki-lint.py            # report
    python3 tools/wiki-lint.py --strict   # exit 1 on any finding (for CI)

Requires tools/wiki-config.json with {"vault": "obsidian/<Name>"}.
See wiki-config.example.json.

Exit codes: 0 clean (or non-strict), 1 findings under --strict, 2 setup error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "wiki-config.json"

VALID_TYPES = {"source", "concept", "entity", "comparison", "analysis", "overview"}
VALID_STATUS = {"stub", "draft", "stable"}
VALID_CONFIDENCE = {"low", "medium", "high"}
META_PAGES = {"index", "log", "hot", "dashboard"}
SKIP_DIRS = {"templates"}

STALE_DAYS = 180

FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
FENCE_RE = re.compile(r"```.*?```|`[^`\n]*`", re.DOTALL)


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


class Finding:
    __slots__ = ("level", "kind", "where", "detail")

    def __init__(self, level: str, kind: str, where: str, detail: str) -> None:
        self.level = level
        self.kind = kind
        self.where = where
        self.detail = detail

    def __str__(self) -> str:
        return f"[{self.level}] {self.kind:<16} {self.where:<38} {self.detail}"


def parse_frontmatter(text: str) -> dict[str, str] | None:
    m = FM_RE.match(text)
    if not m:
        return None
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t", "-")):
            continue
        key, _, val = line.partition(":")
        if val:
            out[key.strip()] = val.strip().strip("\"'")
    return out


def parse_date(value: str) -> date | None:
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Structural lint for the wiki.")
    ap.add_argument("--strict", action="store_true", help="exit 1 if anything is found")
    args = ap.parse_args()

    vault = load_vault()
    wiki = vault / "wiki"
    raw = vault / "raw"

    if not wiki.is_dir():
        print(f"wiki not found: {wiki}", file=sys.stderr)
        return 2

    findings: list[Finding] = []

    pages: dict[Path, str] = {}
    for path in sorted(wiki.rglob("*.md")):
        if SKIP_DIRS & set(path.relative_to(wiki).parts):
            continue
        try:
            pages[path] = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            findings.append(Finding("error", "unreadable", str(path), str(exc)))

    by_stem: dict[str, Path] = {p.stem: p for p in pages}
    by_lower: dict[str, str] = {stem.lower(): stem for stem in by_stem}
    today = date.today()

    for path, text in pages.items():
        rel = str(path.relative_to(wiki))
        stem = path.stem
        is_meta = stem in META_PAGES
        fm = parse_frontmatter(text)

        if fm is None:
            if not is_meta:
                findings.append(Finding("error", "no-frontmatter", rel, "missing YAML block"))
            continue

        for key in ("type", "title", "created", "updated", "status", "confidence"):
            if key not in fm:
                findings.append(Finding("error", "fm-missing-key", rel, f"missing {key}"))

        ptype = fm.get("type", "")
        if ptype and ptype not in VALID_TYPES:
            findings.append(Finding("error", "fm-bad-type", rel, ptype))
        status = fm.get("status", "")
        if status and status not in VALID_STATUS:
            findings.append(Finding("error", "fm-bad-status", rel, status))
        conf = fm.get("confidence", "")
        if conf and conf not in VALID_CONFIDENCE:
            findings.append(Finding("error", "fm-bad-confidence", rel, conf))

        updated = parse_date(fm.get("updated", ""))
        if fm.get("updated") and updated is None:
            findings.append(Finding("error", "fm-bad-date", rel, f"updated={fm['updated']!r}"))
        elif updated and (today - updated).days > STALE_DAYS:
            findings.append(
                Finding("warn", "stale", rel, f"updated {(today - updated).days}d ago")
            )

        if not is_meta and ptype != "source":
            srcs = fm.get("sources", "")
            if srcs in ("", "[]"):
                if conf != "low":
                    findings.append(
                        Finding(
                            "warn",
                            "no-sources",
                            rel,
                            f"confidence={conf or 'unset'} but no sources",
                        )
                    )

    inbound: dict[str, int] = {stem: 0 for stem in by_stem}
    for path, text in pages.items():
        rel = str(path.relative_to(wiki))
        body = FENCE_RE.sub("", text)
        for target in WIKILINK_RE.findall(body):
            target = target.strip()
            if not target:
                continue
            name = Path(target).name
            if name in by_stem or name.lower() in by_lower:
                inbound[by_lower.get(name.lower(), name)] += 1
            elif (vault / f"{target}.md").exists() or (vault / target).exists():
                continue
            else:
                findings.append(Finding("warn", "dead-link", rel, f"[[{target}]]"))

    for stem, path in by_stem.items():
        if stem in META_PAGES:
            continue
        fm = parse_frontmatter(pages[path]) or {}
        if fm.get("type") == "overview":
            continue
        if inbound.get(stem, 0) == 0:
            findings.append(
                Finding("warn", "orphan", str(path.relative_to(wiki)), "no inbound links")
            )

    index_path = wiki / "index.md"
    if index_path.exists():
        index_body = FENCE_RE.sub("", index_path.read_text(encoding="utf-8"))
        indexed = {Path(t.strip()).name for t in WIKILINK_RE.findall(index_body)}
        for stem, path in by_stem.items():
            if stem in META_PAGES:
                continue
            fm = parse_frontmatter(pages[path]) or {}
            if fm.get("type") == "overview":
                continue
            if stem.lower() not in {i.lower() for i in indexed}:
                findings.append(
                    Finding("error", "not-in-index", str(path.relative_to(wiki)), "no index row")
                )
        for name in sorted(indexed):
            if name not in by_stem and name.lower() not in by_lower:
                findings.append(Finding("error", "index-dead-entry", "index.md", f"[[{name}]]"))
    else:
        findings.append(Finding("error", "no-index", "index.md", "file missing"))

    if raw.is_dir():
        corpus = "\n".join(pages.values())
        for path in raw.rglob("*"):
            if path.is_file() and path.name != "README.md" and path.name != ".gitkeep":
                if path.name not in corpus and path.stem not in corpus:
                    findings.append(
                        Finding(
                            "warn",
                            "un-ingested",
                            str(path.relative_to(vault)),
                            "no wiki page references this file",
                        )
                    )

    findings.sort(key=lambda f: (f.level != "error", f.kind, f.where))
    errors = sum(1 for f in findings if f.level == "error")
    warns = len(findings) - errors

    if not findings:
        print(f"clean — {len(pages)} pages, no findings")
        return 0

    for f in findings:
        print(f)
    print(f"\n{len(pages)} pages · {errors} errors · {warns} warnings")

    return 1 if (args.strict and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
