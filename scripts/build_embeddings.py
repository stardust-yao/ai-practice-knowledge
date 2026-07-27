import json, hashlib
from pathlib import Path

ENTRIES_DIR = Path("/Users/liyao/work/AI实践项目/腾讯工程实践学习/knowledge/entries")
OUTPUT = Path("/Users/liyao/work/AI实践项目/腾讯工程实践学习/knowledge/.embeddings.json")

def extract_frontmatter(text, field):
    import re
    m = re.search(rf'^{field}:\s*(.+)$', text, re.MULTILINE)
    return m.group(1).strip() if m else ""

embeddings = {"model": "placeholder", "updated": "", "concepts": {}}
for md_file in sorted(ENTRIES_DIR.glob("*.md")):
    content = md_file.read_text(encoding="utf-8")
    desc = extract_frontmatter(content, "description")
    h = hashlib.sha256((desc + md_file.stem).encode()).digest()
    embeddings["concepts"][md_file.stem] = list(h[:32])

from datetime import datetime, timezone, timedelta
CST = timezone(timedelta(hours=8))
embeddings["updated"] = datetime.now(CST).isoformat()
OUTPUT.write_text(json.dumps(embeddings, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(embeddings['concepts'])} concepts indexed")
