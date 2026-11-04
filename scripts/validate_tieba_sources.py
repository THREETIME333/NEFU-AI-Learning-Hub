#!/usr/bin/env python3
"""Validate third-party source leads without fetching or scraping any website."""
import datetime
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "sources/tieba/candidates.json"
REQUIRED = ("id", "url", "topic", "source_title", "source_year", "discovered_at", "access", "status", "content_type", "summary", "rights", "verify_against")
FORBIDDEN = {"author", "username", "uid", "ip", "ip_location", "avatar", "body", "raw_text", "full_text", "comments", "replies", "phone", "qq", "wechat", "email"}
MAX_SUMMARY = 600

def validate():
    try:
        doc = json.loads(SOURCE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        return [f"Cannot load candidates.json: {err}"]
    errors = []
    if doc.get("schema_version") != 1:
        errors.append("Unsupported schema_version")
    items = doc.get("items")
    if not isinstance(items, list):
        return errors + ["items must be an array"]
    seen_ids, seen_urls = set(), set()
    for i, item in enumerate(items, start=1):
        p = f"candidate {i}"
        if not isinstance(item, dict):
            errors.append(f"{p}: not an object")
            continue
        for field in REQUIRED:
            if field not in item or item[field] is None or item[field] == "":
                errors.append(f"{p}: missing {field}")
        for field in FORBIDDEN.intersection(item):
            errors.append(f"{p}: forbidden personal/raw-text field {field}")
        ident = item.get("id")
        if not isinstance(ident, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,79}", ident):
            errors.append(f"{p}: malformed id")
        if ident in seen_ids:
            errors.append(f"{p}: duplicate id")
        seen_ids.add(ident)
        url = item.get("url")
        if not isinstance(url, str) or not re.fullmatch(r"https://tieba\.baidu\.com/p/[0-9]+", url):
            errors.append(f"{p}: must link to a specific public Tieba thread")
        if url in seen_urls:
            errors.append(f"{p}: duplicate URL")
        seen_urls.add(url)
        year = item.get("source_year")
        if type(year) is not int or not 2000 <= year <= 2100:
            errors.append(f"{p}: invalid source_year")
        try:
            datetime.date.fromisoformat(item["discovered_at"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"{p}: invalid discovered_at")
        if item.get("status") != "candidate_unreviewed":
            errors.append(f"{p}: candidates cannot be presented as published")
        if not isinstance(item.get("summary"), str) or len(item["summary"]) > MAX_SUMMARY:
            errors.append(f"{p}: summary must be short, independent paraphrase")
        if not str(item.get("rights", "")).startswith("link_and_independent_summary_only"):
            errors.append(f"{p}: no third-party repost rights presumed")
    return errors

if __name__ == "__main__":
    mistakes = validate()
    if mistakes:
        for mistake in mistakes:
            print("ERROR:", mistake)
        raise SystemExit(1)
    print("PASS: Tieba source leads are link-only, unreviewed, and contain no raw user metadata")
