"""Contract and offline retrieval smoke tests for the portable NEFU Campus Skill.

These tests intentionally validate real routes and files, not exact Chinese
wording in the documentation. They do not claim to exercise a live AI model.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from validate_nefu_skill import validate, SKILL_ROOT


class NEFUSkillTests(unittest.TestCase):
    def read_repo_file(self, relative_path):
        """Resolve a repository-relative document without path traversal."""
        self.assertIsInstance(relative_path, str)
        self.assertTrue(relative_path.strip())
        self.assertNotIn("\\", relative_path)
        destination = (ROOT / relative_path).resolve()
        self.assertTrue(destination.is_relative_to(ROOT.resolve()), relative_path)
        self.assertTrue(destination.is_file(), relative_path)
        return destination.read_text(encoding="utf-8")

    def test_skill_contract(self):
        self.assertEqual(validate(), [])

    def test_all_hub_routes_open_real_indexes_and_guides(self):
        hub = json.loads(self.read_repo_file("HUB_INDEX.json"))
        expected = {
            "courses": "catalog.json",
            "discussions": "discussion_catalog.json",
            "campus": "community_catalog.json",
        }
        routes = {module["id"]: module for module in hub["modules"]}
        self.assertTrue(set(expected) | {"discovery"} <= routes.keys())
        # The discovery snapshot changes over time; do not pin a dated filename.
        self.assertTrue(
            routes["discovery"]["index"].startswith("sources/platform-scan/")
        )
        expected["discovery"] = routes["discovery"]["index"]
        for module_id, index_path in expected.items():
            with self.subTest(module=module_id):
                module = routes[module_id]
                self.assertEqual(module["index"], index_path)
                guide = self.read_repo_file(module["guide"])
                self.assertTrue(guide.strip())
                data = json.loads(self.read_repo_file(module["index"]))
                if module_id == "discovery":
                    self.assertIsInstance(data["leads"], list)
                    self.assertTrue(
                        self.read_repo_file(data["summary_path"]).strip()
                    )
                else:
                    self.assertIsInstance(data["items"], list)
                    for item in data["items"]:
                        self.assertTrue(
                            self.read_repo_file(item["path"]).strip(),
                            item["path"],
                        )

    def test_student_example_questions_reach_real_documents(self):
        """Keep the four README examples answerable without inventing entries."""
        hub = json.loads(self.read_repo_file("HUB_INDEX.json"))
        indexes = {mod["id"]: mod["index"] for mod in hub["modules"]}
        examples = [
            ("data structure review", "courses", "数据结构"),
            ("dormitory discussions", "discussions", "宿舍"),
            ("major transfer policy", "campus", "转专业"),
        ]
        for description, module_id, keyword in examples:
            with self.subTest(question=description):
                data = json.loads(self.read_repo_file(indexes[module_id]))
                matches = [
                    item for item in data["items"]
                    if keyword in " ".join(
                        str(item.get(field, "")) for field in
                        ("course", "title", "topic", "tags")
                    )
                ]
                self.assertTrue(matches, f"No indexed material for {description}")
                self.assertTrue(self.read_repo_file(matches[0]["path"]).strip())
        discovery = json.loads(self.read_repo_file(indexes["discovery"]))
        self.assertTrue(
            any(entry.get("platform") == "tieba" for entry in discovery["coverage"])
        )

    def test_skill_references_are_available(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for name in (
            "RETRIEVAL.md", "TEACHING.md", "CAMPUS_QA.md",
            "CONTRIBUTION.md", "INSTALL.md",
        ):
            with self.subTest(reference=name):
                self.assertIn(f"(references/{name})", skill)
                reference = SKILL_ROOT / "references" / name
                self.assertTrue(reference.is_file(), name)
                self.assertTrue(reference.read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    unittest.main()
