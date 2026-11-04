#!/usr/bin/env python3
"""Validate the separate public community knowledge index without dependencies."""
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "community_catalog.json"
TYPES = {"senior_advice", "campus_tip", "student_opinion", "rule_discussion", "official_reference"}
SOURCES = {"firsthand", "personal_opinion", "official_public", "public_secondary"}
FIELDS = {"id", "title", "entry_type", "topic", "tags", "scope", "path", "status", "source_category", "source_note", "published_at", "reviewed_at", "consent_to_publish"}

def validate():
    errors = []
    try:
        data = json.loads(INDEX.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return [f"community catalog unreadable: {e}"]
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    entries = data.get("items")
    if not isinstance(entries, list):
        return errors + ["items must be array"]
    seen_ids, seen_paths = set(), set()
    for i, item in enumerate(entries, 1):
        p = f"item {i}"
        if not isinstance(item, dict):
            errors.append(f"{p}: expected object")
            continue
        for k in FIELDS - {"tags", "consent_to_publish"}:
            if not isinstance(item.get(k), str) or not item[k].strip():
                errors.append(f"{p}: required string {k}")
        if not isinstance(item.get("tags"), list) or not all(isinstance(t, str) and t.strip() for t in item.get("tags", [])):
            errors.append(f"{p}: tags must be string list")
        if item.get("consent_to_publish") is not True:
            errors.append(f"{p}: publication consent required")
        if item.get("entry_type") not in TYPES:
            errors.append(f"{p}: unknown entry_type")
        if item.get("source_category") not in SOURCES:
            errors.append(f"{p}: unknown source_category")
        if item.get("status") != "published":
            errors.append(f"{p}: unapproved entries cannot appear in catalog")
        ident = item.get("id")
        if isinstance(ident, str):
            import re
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,79}", ident):
                errors.append(f"{p}: ID must be stable ascii slug")
            if ident in seen_ids:
                errors.append(f"{p}: duplicate ID")
            seen_ids.add(ident)
        for k in ("published_at", "reviewed_at"):
            try:
                datetime.date.fromisoformat(item[k])
            except (ValueError, KeyError, TypeError):
                errors.append(f"{p}: invalid ISO date {k}")
        path = item.get("path")
        if isinstance(path, str):
            q = Path(path)
            if (not path.startswith("校园经验/条目/") or q.is_absolute()
                    or ".." in q.parts or chr(92) in path or q.suffix != ".md"
                    or not (ROOT / q).is_file()
                    or not (ROOT / q).resolve().is_relative_to(ROOT.resolve())):
                errors.append(f"{p}: unsafe or absent publication path {path}")
            if path in seen_paths:
                errors.append(f"{p}: duplicate path")
            seen_paths.add(path)
        if item.get("entry_type") == "official_reference":
            if item.get("source_category") != "official_public":
                errors.append(f"{p}: official_reference requires official_public source")
            for k in ("official_url", "effective_date"):
                if not isinstance(item.get(k), str) or not item[k].strip():
                    errors.append(f"{p}: official_reference missing {k}")
            try:
                datetime.date.fromisoformat(item["effective_date"])
            except (KeyError, ValueError, TypeError):
                errors.append(f"{p}: official_reference invalid effective_date")
            if not str(item.get("official_url", "")).startswith("https://"):
                errors.append(f"{p}: official_url must be HTTPS")
        elif item.get("source_category") == "official_public":
            errors.append(f"{p}: non-official_reference cannot claim official_public status")
    return errors

if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print("ERROR:", problem)
        raise SystemExit(1)
    print("PASS: community catalog format, provenance and publication status valid")
