import json
import subprocess
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'scripts'))
from validate_catalog import validate
from build_ai_index import render

class RepositoryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))

    def test_catalog_valid(self):
        self.assertEqual(validate(),[])

    def test_generated_index_current(self):
        self.assertEqual((ROOT/'AI_INDEX.md').read_text(encoding='utf-8'),render(self.doc))

    def test_index_does_not_invent_exam_years(self):
        paper=[x for x in self.doc['items'] if x['kind']=='authorized_past_paper']
        self.assertFalse(any(x.get('year') is None for x in paper))
        # No historic dates are invented for original mock exams.
        self.assertTrue(all(x['year'] is None for x in self.doc['items'] if x['kind']=='original_mock'))

    def test_question_ids_unique_for_mock(self):
        import re
        for item in self.doc['items']:
            if item['kind']!='original_mock':continue
            content=(ROOT/item['path']).read_text(encoding='utf-8')
            ids=re.findall(r'^#{2,4} (Q\d{3})\b',content,flags=re.M)
            self.assertTrue(ids,f'{item["id"]} lacks stable Q IDs')
            self.assertEqual(len(ids),len(set(ids)))
            self.assertIn('非历年真题',content)

    def test_agent_entrypoints_exist(self):
        for fn in ['README.md','AI_START_HERE.md','AGENTS.md','MAINTAINER_PLAYBOOK.md','prompts/STUDENT_CONNECT.md','prompts/MAINTAINER_AGENT.md']:
            self.assertTrue((ROOT/fn).is_file(),fn)

if __name__=='__main__':unittest.main()
