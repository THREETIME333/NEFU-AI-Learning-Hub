#!/usr/bin/env python3
"""Offline validation: catalog path safety, provenance, inventory, and exam IDs."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAT = ROOT / "catalog.json"
KINDS = {'official_link','authorized_past_paper','student_recollection','original_mock','study_note'}
VERIFICATIONS = {'official','permission_checked','reviewed','unverified'}
ALLOWED_PAPER_TYPES = {'midterm','final','quiz','other'}

def validate():
    errors=[]
    try:
        doc=json.loads(CAT.read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError) as e:
        return [f'catalog.json cannot be read as JSON: {e}']
    if doc.get('schema_version') != 1:
        errors.append('schema_version must be 1')
    items=doc.get('items')
    if not isinstance(items,list):
        return errors+['items must be an array']
    ids=set()
    paths=set()
    for n,item in enumerate(items,1):
        pfx=f'item {n}'
        if not isinstance(item,dict):
            errors.append(f'{pfx}: must be an object')
            continue
        for key in ('id','title','course','kind','term','path','verification','source','description'):
            if not isinstance(item.get(key),str) or not item.get(key,'').strip():
                errors.append(f'{pfx}: missing or invalid {key}')
        ident=item.get('id')
        if isinstance(ident,str):
            if not re.fullmatch(r'[a-z0-9][a-z0-9-]{1,79}',ident): errors.append(f'{pfx}: id must be stable ASCII slug')
            if ident in ids: errors.append(f'{pfx}: duplicate id {ident}')
            ids.add(ident)
        kind=item.get('kind')
        if kind not in KINDS: errors.append(f'{pfx}: invalid kind')
        verification=item.get('verification')
        if verification not in VERIFICATIONS: errors.append(f'{pfx}: invalid verification')
        year=item.get('year')
        if year is not None and (type(year) is not int or not 2000 <= year <= 2100):
            errors.append(f'{pfx}: year must be 2000..2100 integer or null')
        path=item.get('path')
        if isinstance(path,str) and path:
            posix=path.replace('\\','/')
            q=Path(posix)
            if (q.is_absolute() or posix.startswith(('/', '\\')) or ':' in posix or
                '..' in q.parts or '.' in q.parts or posix.startswith('.')):
                errors.append(f'{pfx}: unsafe path {path}')
            elif q.suffix.lower() != '.md':
                errors.append(f'{pfx}: material path must point to a Markdown file')
            elif not (ROOT/q).is_file() or not (ROOT/q).resolve().is_relative_to(ROOT.resolve()):
                errors.append(f'{pfx}: missing or unsafe file {path}')
            if posix in paths: errors.append(f'{pfx}: duplicate material path {path}')
            paths.add(posix)
        if kind == 'authorized_past_paper':
            if verification != 'permission_checked': errors.append(f'{pfx}: authorized paper must be permission_checked')
            if year is None: errors.append(f'{pfx}: authorized paper needs confirmed year')
            for key in ('rights_basis','source_evidence','reviewer','paper_type'):
                if not isinstance(item.get(key),str) or not item.get(key).strip():
                    errors.append(f'{pfx}: authorized paper missing {key}')
            if item.get('paper_type') not in ALLOWED_PAPER_TYPES:
                errors.append(f'{pfx}: paper_type must be midterm/final/quiz/other')
        if kind == 'original_mock' and year is not None:
            errors.append(f'{pfx}: mock cannot have historical exam year')
        if kind == 'official_link' and year is not None:
            errors.append(f'{pfx}: official link navigation cannot pretend to be exam year')
    return errors

if __name__=='__main__':
    failures=validate()
    if failures:
        print('FAILED catalog validation:')
        for failure in failures:print(' -',failure)
        raise SystemExit(1)
    print('PASS: catalog is valid, source types are explicit, material paths exist')
