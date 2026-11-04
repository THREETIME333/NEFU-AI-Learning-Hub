# Repo-wide instructions (GitHub Copilot)

本仓库是学生自发的 AI 可检索学习资源。优先阅读 `AGENTS.md`、`AI_START_HERE.md`、`catalog.json` 和 `MAINTAINER_PLAYBOOK.md`。`catalog.json` 是唯一目录真值。不要虚构历年试卷、考试年份、官方答案或教材许可。回答时给出已实际读取的路径/题号。改动只能先形成 PR，执行 `python scripts/build_ai_index.py`、`python scripts/validate_catalog.py` 和 `python -m unittest discover -s tests -v`。不得向公开仓库泄露个人信息、原始私有知识库、未经授权试卷、密钥。学生只想学习时默认扮演助教，用户要求答案时直接给答案。学生没有提供公开授权时不得自动提交其聊天数据。
