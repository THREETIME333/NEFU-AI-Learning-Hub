"""Executable contract tests for the portable NEFU Campus Skill."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from validate_nefu_skill import validate, SKILL_ROOT

class NEFUSkillTests(unittest.TestCase):
    def test_skill_contract(self):
        self.assertEqual(validate(), [])

    def test_skill_is_procedural_not_snapshot(self):
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("HUB_INDEX.json", text)
        self.assertIn("discussion_catalog.json", text)
        self.assertIn("community_catalog.json", text)
        self.assertIn("catalog.json", text)
        self.assertIn("按需", text)
        self.assertIn("不能", text)
        self.assertIn("不", text)

    def test_safe_contribution_workflow(self):
        text = (SKILL_ROOT / "references" / "CONTRIBUTION.md").read_text(encoding="utf-8")
        self.assertIn("明确同意", text)
        self.assertIn("脱敏", text)
        self.assertIn("Issue", text)
        self.assertIn("PR", text)

    def test_beginner_instructions_not_promise_auto_install(self):
        text = (SKILL_ROOT / "references" / "INSTALL.md").read_text(encoding="utf-8")
        self.assertIn("不等于", text)
        self.assertIn("HUB_INDEX.json", text)
        self.assertIn("DSH", text)
        self.assertIn("Codex", text)

if __name__ == "__main__":
    unittest.main()
