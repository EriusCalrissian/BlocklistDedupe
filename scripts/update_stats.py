"""Write the source list and blocklist size statistics into README.md between their markers."""

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "configuration.json"
OUTPUT = ROOT / "dist" / "blocklist-main.txt"
README = ROOT / "README.md"
TITLE = re.compile(r"^[!#]\s*Title\s*:\s*(.+)$", re.IGNORECASE)


def count_rules(lines):
    return sum(1 for line in lines if line.strip() and not line.lstrip().startswith(("!", "#")))


def parse_title(lines):
    """Return the "Title:" from the comment header, which ends at the first rule."""
    for line in lines:
        line = line.strip()
        if not line or (line.startswith("[") and line.endswith("]")):
            continue
        if not line.startswith(("!", "#")):
            return None
        match = TITLE.match(line)
        if match:
            return match.group(1).strip()
    return None


def source_name(source, lines):
    return source.get("name") or (lines and parse_title(lines)) or source["source"].rstrip("/").rsplit("/", 1)[-1]


def fetch_lines(url):
    request = urllib.request.Request(url, headers={"User-Agent": "BlocklistDedupe"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read().decode("utf-8", errors="replace").splitlines()


def replace_section(readme, name, lines):
    start, end = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
    pattern = re.compile(re.escape(start) + ".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(readme):
        sys.exit(f"{name} markers not found in {README.name}")
    return pattern.sub(lambda _: "\n".join([start, *lines, end]), readme)


def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    sources = []
    for source in config["sources"]:
        try:
            lines = fetch_lines(source["source"])
        except Exception as error:
            print(f"Failed to fetch {source['source']}: {error}", file=sys.stderr)
            lines = None
        count = None if lines is None else count_rules(lines)
        sources.append((source_name(source, lines), source, count))

    total = sum(count for _, _, count in sources if count is not None)
    merged = count_rules(OUTPUT.read_text(encoding="utf-8").splitlines())
    removed = total - merged
    percent = removed / total * 100 if total else 0

    stats = [
        "| | Rules |",
        "| --- | ---: |",
        f"| Sum of all sources | {total:,} |",
        f"| Merged list | **{merged:,}** |",
        f"| Removed (duplicates, redundant subdomains, exclusions) | {removed:,} (**{percent:.1f}%**) |",
    ]

    source_table = [
        "| Source | Format | Rules |",
        "| --- | --- | ---: |",
    ]
    for name, source, count in sources:
        rules = "n/a" if count is None else f"{count:,}"
        name = name.replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")
        source_table.append(f"| [{name}]({source['source']}) | {source.get('type', 'adblock')} | {rules} |")

    readme = README.read_text(encoding="utf-8")
    readme = replace_section(readme, "stats", stats)
    readme = replace_section(readme, "sources", source_table)
    README.write_text(readme, encoding="utf-8")
    print(f"Sources: {total:,}, merged: {merged:,}, removed: {removed:,} ({percent:.1f}%)")


if __name__ == "__main__":
    main()
