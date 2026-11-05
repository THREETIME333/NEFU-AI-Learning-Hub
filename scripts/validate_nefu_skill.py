#!/usr/bin/env python3
"""Verify the shareable, instruction-only NEFU Campus Skill (stdlib only)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = ROOT / ".agents" / "skills" / "nefu-campus"
MAIN = SKILL_ROOT / "SKILL.md"
REFERENCE_NAMES = {"RETRIEVAL.md", "TEACHING.md", "CAMPUS_QA.md",
                   "CONTRIBUTION.md", "INSTALL.md"}
INDEX_TARGETS = {"catalog.json", "discussion_catalog.json",
                 "community_catalog.json", "HUB_INDEX.json"}

def validate() -> list[str]:
    errors: list[str] = []
    try:
        text = MAIN.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"Missing skill main file: {exc}"]
    parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.M)
    if len(parts) < 3 or parts[0].strip():
        return ["SKILL.md must start with YAML frontmatter separated by ---"]
    frontmatter, body = parts[1], parts[2]
    if any(re.match(r"^\s*[&*!][^\s]*", l) for l in frontmatter.splitlines()):
        errors.append("No YAML anchors, aliases or custom tags are needed")
    metadata: dict[str,str] = {}
    for line in frontmatter.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([a-z][a-z0-9_-]*):\s*(.+?)\s*", line)
        if not match:
            errors.append(f"Malformed frontmatter line: {line[:60]}")
            continue
        k, v = match.groups()
        if k in metadata:
            errors.append(f"Duplicate metadata key {k}")
        metadata[k] = v.strip().strip("'\"")
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("Skill name must be lowercase-hyphenated and at most 64 chars")
    if name != SKILL_ROOT.name:
        errors.append("Skill name must match skill folder")
    if not description or len(description) > 1024:
        errors.append("Skill description must be 1..1024 characters")
    if len(body.splitlines()) > 500:
        errors.append("SKILL.md too long; move detail into references")
    for fname in REFERENCE_NAMES:
        reference = SKILL_ROOT / "references" / fname
        if not reference.is_file():
            errors.append(f"Missing skill reference: {fname}")
        if f"(references/{fname})" not in body:
            errors.append(f"SKILL.md does not link required reference: {fname}")
    for rel in re.findall(r"\]\((references/[^)#?]+)\)", body):
        path = (SKILL_ROOT / rel).resolve()
        try:
            path.relative_to(SKILL_ROOT.resolve())
        except ValueError:
            errors.append(f"Skill reference escapes its directory: {rel}")
            continue
        if not path.is_file():
            errors.append(f"Skill reference does not exist: {rel}")
    for index in INDEX_TARGETS:
        if not (ROOT / index).is_file():
            errors.append(f"Missing referenced repository index: {index}")
        if index not in body:
            errors.append(f"SKILL.md must mention index: {index}")
    try:
        hub = json.loads((ROOT / "HUB_INDEX.json").read_text(encoding="utf-8"))
        if not isinstance(hub, dict) or not isinstance(hub.get("modules"), list):
            raise ValueError("Hub index must contain a modules array")
        module_targets: set[str] = set()
        module_ids: set[str] = set()
        for module in hub["modules"]:
            if not isinstance(module, dict):
                errors.append("Hub module must be an object")
                continue
            ident = module.get("id")
            if not isinstance(ident, str) or not ident:
                errors.append("Hub module missing id")
            elif ident in module_ids:
                errors.append(f"Duplicate hub module id: {ident}")
            else:
                module_ids.add(ident)
            for field in ("index", "guide"):
                rel = module.get(field)
                if not isinstance(rel, str) or not rel.strip():
                    errors.append(f"Hub module {ident} missing {field}")
                    continue
                normalized = rel.replace("\\", "/")
                destination = (ROOT / normalized).resolve()
                if (Path(normalized).is_absolute()
                        or not destination.is_relative_to(ROOT.resolve())
                        or not destination.is_file()):
                    errors.append(f"Hub module {ident} has missing/unsafe {field}: {rel}")
                if field == "index":
                    module_targets.add(rel)
        for name in ("catalog.json", "discussion_catalog.json", "community_catalog.json"):
            if name not in module_targets:
                errors.append(f"Hub route missing {name}")
    except (ValueError, OSError, TypeError) as exc:
        errors.append(f"Cannot check HUB_INDEX.json routing: {exc}")
    # Safety and teaching prose is reviewed as content. CI enforces its linked
    # instructions and actual routes, not fragile matches on Chinese adjectives.
    return errors

if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print("ERROR:", problem)
        raise SystemExit(1)
    print("PASS: NEFU Campus Skill metadata, reference links and hub routes")
