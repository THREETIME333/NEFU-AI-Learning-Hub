# 如何让 AI 真正读取仓库（避免虚假承诺）

**重要**：把 URL 粘贴给一个聊天机器人 ≠ 这个机器人已经获得读取整个仓库的能力。必须检查客户端是否真的暴露 GitHub 文件读取/搜索工具。

## A. ChatGPT

在支持 GitHub 插件/连接的会话中，由学生连接自己的 GitHub 后，把仓库设为可读取范围；AI 通过连接工具打开 `catalog.json` 和指定 `path`。有时会话没有启用工具，此时不能假称已读取。

## B. Codex / Claude Code / GitHub Copilot 等 Agent

可使用本地 `git clone`，或配置官方 GitHub MCP Server：https://github.com/github/github-mcp-server 。**日常学习使用只读授权即可**，不需要把管理员写权限交给每位学生。

## C. DeepSeek

DeepSeek 模型 API 有工具调用能力，但模型不自带 GitHub 文件访问工具。学生需要选一个支持 GitHub MCP/外部工具的 Agent 客户端，以 DeepSeek 作为其模型。具体接法由客户端决定；普通 DeepSeek 网页版不能保证实现本项目的完整直连体验。

## D. 什么才算接入成功？

让 AI 回答测试题：

> 请实际读取 `catalog.json`。告诉我数据结构目前有几条资源、各自的 `id`、`kind` 和 `path`；再检索是否有 2023 年数据结构期末真题。不得根据 README 猜测。

如果 AI 回答“有 2023 真题”，但索引没有，就说明没有正确检索或在幻觉；须停止直接教学并排查连接。

## 读写权限分离

- **Tutor**：只读资料，不需要 GitHub 写权限。
- **Contributor Agent**：获学生授权时创建 Issue/PR。
- **Maintainer Agent**：以维护者身份审查并提交 PR，不应直接改保护分支。

没有一个“通用的、打开即可让所有大模型访问 GitHub”的神奇提示词。仓库提供跨模型兼容的数据协议，具体工具接入仍由学生的 AI 客户端决定。
