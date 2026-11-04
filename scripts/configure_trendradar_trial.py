#!/usr/bin/env python3
"""Configure a read-only NEFU TrendRadar trial from a pinned upstream checkout.

Only public hot-list titles are used. No credentials, paid AI, cookies, or
student/private data are required. This script does not publish results.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: configure_trendradar_trial.py <TrendRadar directory>")
        return 2

    root = Path(sys.argv[1]).resolve()
    target = root / "config" / "config.yaml"
    if not target.is_file():
        print(f"Missing upstream configuration: {target}")
        return 2

    config = yaml.safe_load(target.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("Unexpected TrendRadar config format")

    # Keep scope narrow: these are HOT LISTS, not ordinary campus forum posts.
    allowed = {"tieba", "bilibili-hot-search", "baidu"}
    platforms = config["platforms"]
    platforms["enabled"] = True
    platforms["sources"] = [
        source for source in platforms["sources"] if source["id"] in allowed
    ]
    seen = {source["id"] for source in platforms["sources"]}
    if seen != allowed:
        raise ValueError(f"Upstream platform IDs changed: missing {allowed - seen}")

    config["rss"]["enabled"] = False
    config["schedule"]["enabled"] = False
    config["filter"]["method"] = "keyword"
    config["report"]["mode"] = "current"
    config["storage"]["backend"] = "local"
    config["storage"]["formats"]["html"] = True
    config["notification"]["enabled"] = False
    config["ai_analysis"]["enabled"] = False
    config["ai_translation"]["enabled"] = False
    config["app"]["timezone"] = "Asia/Shanghai"

    # Do not output or store credentials. Use only the upstream public APIs.
    target.write_text(
        yaml.safe_dump(config, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    keywords = """[GLOBAL_FILTER]

[WORD_GROUPS]

[东北林业大学]
东北林业大学
东北林大
东林校园
东林宿舍
东林食堂
东林转专业
东林考研
NEFU
"""
    (root / "config" / "frequency_words.txt").write_text(
        keywords, encoding="utf-8"
    )
    print("Prepared TrendRadar public-hotlist pilot: 3 sources, free/no AI/no notifications")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
