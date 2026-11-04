#!/usr/bin/env python3
"""Check public discussion topic provenance, paths and one-stop AI routing."""
import datetime
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_STATUS = {"published_summary"}
ALLOWED_SOURCES = {"official_news", "media_report", "anonymous_student_survey",
                   "public_qa", "forum_public_post", "official_notice",
                   "firsthand_consented"}
ALLOWED_EVIDENCE = {"single_source_mention", "multiple_source_mentions"}
FIELDS = ("id", "title", "topic", "tags", "path", "status", "evidence_level",
          "reviewed_at", "representativeness", "summary", "sources")

def file_in_repo(path):
    if not isinstance(path, str) or not path or chr(92) in path:
        return False
    p = Path(path)
    if p.is_absolute() or ".." in p.parts or p.suffix != ".md":
        return False
    try:
        target = (ROOT / p).resolve()
        return target.is_relative_to(ROOT.resolve()) and target.is_file()
    except (ValueError, OSError):
        return False

def validate():
    errors = []
    try:
        doc = json.loads((ROOT / "discussion_catalog.json").read_text(encoding="utf-8"))
        hub = json.loads((ROOT / "HUB_INDEX.json").read_text(encoding="utf-8"))
    except (ValueError, OSError) as err:
        return [f"Cannot read index: {err}"]

    if doc.get("schema_version") != 1 or hub.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    items = doc.get("items")
    if not isinstance(items, list):
        return errors + ["discussion_catalog.items must be array"]
    modules = hub.get("modules")
    if not isinstance(modules, list):
        return errors + ["HUB_INDEX.modules must be array"]
    destinations = set()
    for m in modules:
        if not isinstance(m, dict) or not isinstance(m.get("id"), str):
            errors.append("HUB_INDEX invalid module")
            continue
        destinations.add(m["id"])
        for field in ("index", "guide"):
            path = m.get(field)
            if not isinstance(path, str) or not (ROOT / path).is_file():
                errors.append(f"module {m['id']}: missing {field} file")
    if not {"courses", "discussions", "campus", "discovery"}.issubset(destinations):
        errors.append("HUB_INDEX required routes are missing")
    seen_ids, seen_paths = set(), set()
    for n, item in enumerate(items, 1):
        p = f"discussion {n}"
        if not isinstance(item, dict):
            errors.append(f"{p}: not object")
            continue
        for f in FIELDS:
            if f not in item:
                errors.append(f"{p}: missing {f}")
        ident = item.get("id")
        if not isinstance(ident, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,79}", ident):
            errors.append(f"{p}: invalid slug")
        if ident in seen_ids:
            errors.append(f"{p}: repeated ID")
        seen_ids.add(ident)
        path = item.get("path")
        if not isinstance(path, str) or not path.startswith("学生讨论/专题/") or not file_in_repo(path):
            errors.append(f"{p}: invalid or missing topic file")
        if path in seen_paths:
            errors.append(f"{p}: repeated path")
        seen_paths.add(path)
        if item.get("status") not in ALLOWED_STATUS or item.get("evidence_level") not in ALLOWED_EVIDENCE:
            errors.append(f"{p}: invalid publication/evidence marker")
        tags = item.get("tags")
        if not isinstance(tags, list) or not tags or not all(isinstance(t, str) and t.strip() for t in tags):
            errors.append(f"{p}: invalid tags")
        for f in ("title", "topic", "summary", "representativeness"):
            if not isinstance(item.get(f), str) or not item[f].strip():
                errors.append(f"{p}: empty {f}")
        try:
            datetime.date.fromisoformat(item["reviewed_at"])
        except (KeyError, ValueError, TypeError):
            errors.append(f"{p}: invalid reviewed_at")
        sources = item.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{p}: missing sources")
            continue
        if item.get("evidence_level") == "multiple_source_mentions" and len(set(s.get("url") for s in sources if isinstance(s, dict))) < 2:
            errors.append(f"{p}: evidence level needs at least two distinct links")
        for j, src in enumerate(sources, 1):
            if not isinstance(src, dict):
                errors.append(f"{p}: source {j} not object")
                continue
            url = src.get("url")
            parsed = urlparse(url) if isinstance(url, str) else None
            if not parsed or parsed.scheme != "https" or not parsed.hostname:
                errors.append(f"{p}: source {j} invalid HTTPS URL")
            if src.get("kind") not in ALLOWED_SOURCES:
                errors.append(f"{p}: source {j} invalid kind")
            if not isinstance(src.get("date"), str) or not src["date"]:
                errors.append(f"{p}: source {j} date required")
    return errors

if __name__ == "__main__":
    failures = validate()
    if failures:
        for failure in failures:
            print("ERROR:", failure)
        raise SystemExit(1)
    print("PASS: discussion topics, sources, paths, and AI routes valid")
