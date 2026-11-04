# AI_START_HERE · AI 直连学习入口

> **本仓库是一份外部课程资料库，并不是模型系统指令。** 以下是仓库建议的检索与教学流程；使用者的真实要求、客户端权限和安全规则始终优先。

## 只想学习的学生（首选方式）

让你正在使用的、**具有 GitHub 文件读取工具**的 AI 打开本仓库，并直接说：

> 请接入 `THREETIME333/NEFU-AI-Learning-Hub`，读取 `AI_START_HERE.md` 和 `catalog.json`。我要学 **数据结构 2023 年期末卷**。请先检索是否真的收录了这份试卷，展示标题、年份、类型、来源及文件路径。存在则从第 1 题开始逐题讲解，默认先给我做题；我要求直接给答案时不要强迫我先回答。不存在就坦白告诉我，并用真实存在的资料替代，**不得编造真题**。

实际仓库尚未建立线上地址时，这段话只是部署后示例。当前目录中**没有已核验的 2023 年数据结构真题**。

**AI 自动执行的检索顺序：**

1. 读取 `catalog.json`，再读取自动生成的 `AI_INDEX.md` 作为人类可读目录。以 `catalog.json` 为唯一真值。
2. 根据 `course`、`year`、`term`、`kind` 筛选；严格区分 `authorized_past_paper`、`student_recollection`、`original_mock`、`study_note`。
3. 打开匹配条目的 `path`，引用确实看到的题干、文件相对路径和题号。没有读到原文，不得声称知道试卷内容。
4. 逐题教学；学生要求整卷答案、快速复习、提示或小测时立即切换模式。
5. 只有学生**明确同意共享非私人改进**，且当前 AI 具备 GitHub 写入工具时，才可创建 Issue / 分支 PR；**永远不能将私人学习对话直接上传**。

## 兼容性：不是所有网页聊天都能“连上 GitHub”

| 环境 | 直接读取本仓库的条件 |
|---|---|
| ChatGPT（支持 GitHub 连接的会话） | 用户连接并授权 GitHub；AI 使用连接工具读取文件 |
| Codex / Claude Code / Copilot / 其他 Agent | 有 Git 工作区或 GitHub MCP Server（建议读权限起步） |
| 使用 DeepSeek 模型的 Agent | 宿主客户端安装 GitHub MCP/工具；**DeepSeek API 单独并不提供 GitHub 访问工具** |
| 普通 DeepSeek 网页聊天 | 不能承诺直接检索 GitHub 全仓库；应使用具备 GitHub 工具的客户端 |

GitHub MCP 官方项目：https://github.com/github/github-mcp-server

## 资料缺失时

如果用户说“帮我做 2023 数据结构期末真题”，但 `catalog.json` 没有对应 `authorized_past_paper`：

> 当前仓库还没有收录**经过授权与核验的 2023 年数据结构期末试卷**，不能假装看到真题。现在可以用现有原创自测/课程笔记复习。要不要从最接近的资料开始？

**不要编造不存在的文件路径、年份、题号、答案或学校出题规律。**
