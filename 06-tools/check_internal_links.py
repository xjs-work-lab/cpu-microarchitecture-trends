#!/usr/bin/env python3
"""Check local markdown links without network access."""
import re
from pathlib import Path
from urllib.parse import unquote
root = Path(__file__).resolve().parents[1]
missing = []
for doc in root.rglob("*.md"):
    for n, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
        for url in re.findall(r"!?(?:\\[[^\\]]*\\])\\(([^)]+)\\)", line):
            url = unquote(url.split("#")[0])
            if not url or url.startswith(("http:", "https:", "mailto:", "/", "data:")):
                continue
            if not (doc.parent / url).exists():
                missing.append(f"{doc.relative_to(root)}:{n} -> {url}")
assert not missing, "\\n".join(missing)
print("Internal Markdown links OK")
