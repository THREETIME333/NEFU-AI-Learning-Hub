#!/usr/bin/env python3
"""Build the human/agent readable, deterministic index from catalog.json.

Usage: python scripts/build_ai_index.py [--check]
No network, no third-party packages, no model/API charges.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog.json"
TARGET = ROOT / "AI_INDEX.md"
KIND = {
    "official_link": "官方公开资源入口（非试卷）",
    "authorized_past_paper": "经许可完整历年试卷（不代表官方认证）",
    "student_recollection": "学生考点回忆（非原卷）",
    "original_mock": "原创模拟（非真题）",
    "study_note": "课程笔记",
}

def clean(s):
    return str(s).replace("|", "\\|").replace("\n", " ").strip()

def render(doc):
    entries = doc.get("items", [])
    if not isinstance(entries, list):
        raise ValueError("catalog.items is not an array")
    groups = {}
    for item in entries:
        groups.setdefault(item["course"], []).append(item)
    lines = [
        "# AI_INDEX · 课程资料索引（由 catalog.json 自动生成）",
        "",
        "> ⚠️ 该索引供快速浏览，`catalog.json` 才是机器读取的唯一目录真值。**未列出的年份或试卷 = 尚未收录**；不允许编造。",
        "> 本项目为学生自发的非官方学习资源；学生回忆、原创模拟、公开资源入口与经许可历年卷必须严格区分。",
        "",
        f"- 共收录 **{len(entries)}** 条可定位资源。",
        f"- 经许可完整历年卷：**{sum(x['kind']=='authorized_past_paper' for x in entries)}** 条。",
        f"- 原创模拟卷：**{sum(x['kind']=='original_mock' for x in entries)}** 条。",
        "",
        "## 给 AI 的读取协议",
        "",
        "1. 先实际读取 `catalog.json`，按 `course`、`year`、`term`、`kind` 精确检索。",
        "2. 打开条目的 `path` 文件；列出来源、文件路径、稳定题号。未打开不得凭印象讲题。",
        "3. 有对应授权真题则如实逐题教学；否则说明**当前未收录该真题**并提供已存在的模拟或讲义。",
        "4. 需要贡献时读 `AGENTS.md`，学生同意且具备权限后由 AI 提交去个人化的 Issue / PR。",
        "",
    ]
    for course in sorted(groups):
        lines += [f"## {clean(course)}", "", "| ID | 标题 | 类型 | 年份 | 学期 | 核验标记 | 路径 |", "|---|---|---|---|---|---|---|"]
        for item in sorted(groups[course],key=lambda x:(x["year"] is None, str(x["year"] or ""), x["id"])):
            lines.append("| " + " | ".join([
                f"`{clean(item['id'])}`",
                clean(item["title"]),
                clean(KIND[item["kind"]]),
                str(item["year"]) if item["year"] is not None else "未标注",
                clean(item["term"]),
                f"`{clean(item['verification'])}`",
                f"[{clean(item['path'])}](<{item['path']}>)",
            ]) + " |")
        lines += [""]
    lines += ["---", "", "_此文档由 `python scripts/build_ai_index.py` 生成。请修改 `catalog.json`，不要手工修改本文件。_", ""]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Exit nonzero if AI_INDEX.md is missing or stale")
    args=ap.parse_args()
    doc=json.loads(CATALOG.read_text(encoding="utf-8"))
    expected=render(doc)
    if args.check:
        if not TARGET.is_file() or TARGET.read_text(encoding="utf-8") != expected:
            print("FAIL: AI_INDEX.md is missing/stale; run python scripts/build_ai_index.py")
            return 1
        print("PASS: AI_INDEX.md matches catalog.json")
        return 0
    TARGET.write_text(expected,encoding="utf-8")
    print("Generated AI_INDEX.md")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
