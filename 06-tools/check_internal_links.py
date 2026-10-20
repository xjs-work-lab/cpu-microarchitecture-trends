#!/usr/bin/env python3
"""Check repository-relative Markdown links; external links are not accessed."""
import re
from pathlib import Path
from urllib.parse import unquote

root = Path(__file__).resolve().parents[1]
missing = []
pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
for doc in root.rglob("*.md"):
    for n, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
        for url in pattern.findall(line):
            url = unquote(url.split("#")[0])
            if not url or url.startswith(("http:", "https:", "mailto:", "/", "data:")):
                continue
            if not (doc.parent / url).exists():
                missing.append(f"{doc.relative_to(root)}:{n} -> {url}")
if missing:
    raise SystemExit("\n".join(missing))
print("Internal Markdown links OK")
