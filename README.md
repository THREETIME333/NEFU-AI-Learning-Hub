# NEFU AI Learning Hub · 东北林业大学 AI 直连课程资料库

> 学生自发维护的**非官方**开源项目，与东北林业大学官方没有隶属或背书关系。**学生只需向自己常用的 AI 说课程与年份，AI 负责读取真题、逐题讲解；AI 可在授权后代学生提交勘误提案。**

## 🤖 学生最快使用方式（无需下载试卷）

在**已经具有 GitHub 文件读取功能**的 ChatGPT、Codex、Claude Code 或 DeepSeek Agent 中说：

> 请读取 GitHub 仓库 `THREETIME333/NEFU-AI-Learning-Hub` 的 `AI_START_HERE.md` 和 `catalog.json`。我要复习数据结构期末，先查找真实收录的历年真题；找到则从第一题开始讲，找不到就如实告诉我，并用已有原创模拟题辅导。不要编造原卷。

[打开完整 AI 入口与兼容说明](AI_START_HERE.md) · [GitHub / DeepSeek 接入](docs/CONNECTORS.md) · [AI 智能体操作协议](AGENTS.md)

**不是所有网页聊天模型都能直接浏览 GitHub。** 只有客户端实际启用了 GitHub 连接或 MCP 工具时才能自动读取；普通 DeepSeek 网页版不保证支持这一流程。

**当前库存状态：还没有经许可核实可公开发布的历年原卷。** 仓库目前提供学校资源入口、原创复习笔记、原创自测卷。不能把模拟卷称为真题，也不能编造不存在的年份。

## 🧭 AI 检索标准流程

```text
学生说“学数据结构 2023 期末”
     ↓
AI 读取 catalog.json（唯一事实索引）
     ↓
按 course / year / kind 筛选
     ├─ 有真实匹配：打开文档，逐题讲解并引用题号与路径
     └─ 没有匹配：坦白告知缺失，推荐已有模拟卷/笔记
     ↓
学生学习、纠错
     ↓（只有学生同意公开脱敏修正 + AI 有写权限）
AI 建 Issue / PR → 校验脚本 → 管理员审核 → 合并 → 反哺全体同学
```

[AI 可读目录（自动生成）](AI_INDEX.md) · [机器目录 catalog.json](catalog.json)

## 📚 现有课程与资源

- [数据结构复习导航](课程/数据结构/复习导航.md) · [原创自测卷（非真题）](原创练习/数据结构-原创自测卷01.md)
- [离散数学复习导航](课程/离散数学/复习导航.md)
- [学校公开资源导航](学校资源/官方资源导航.md)

## 🛠 给维护 AI / 仓库拥有者

- [管理员操作手册](MAINTAINER_PLAYBOOK.md) · [可直接使用的管理员提示词](prompts/MAINTAINER_AGENT.md) · [投稿协议](CONTRIBUTING.md)
- 使用 Markdown + `catalog.json`，只靠 Python 标准库校验，暂时无需付费模型 API、数据库或网站后台。
- 添加新资源后运行：`python scripts/build_ai_index.py && python scripts/validate_catalog.py && python -m unittest discover -s tests -v`。
- GitHub Actions 在 PR 时检查数据和索引；主分支最好开启保护、要求可信任的维护者最终批准。**AI 并非天然 24 小时在线，未经部署后台服务就不会自动处理所有 Issues。**

## 🔒 公共资源准入

完整历年原卷：需有可核查的发布权利和来源；校内未公开不等于允许转载。学生回忆：只整理可分享的考点经验，不能伪装成原卷。原创模拟：标注非真题。不要导出原私人 `University-Knowledge`、Obsidian、Notion 的私人数据。

如果模型无法直接访问仓库，可选用 [原静态页面原型](index.html) 浏览资料，但**项目的核心是 AI 直读仓库**，而非手动复制内容。
