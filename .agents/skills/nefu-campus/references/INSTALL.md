# 给同学：NEFU Campus Skill 使用与安装指南

GitHub 项目地址：https://github.com/THREETIME333/NEFU-AI-Learning-Hub

**先记住：直接把 GitHub 链接发给 AI，不等于 AI 自动安装 Skill。** 只要 AI 已有 GitHub/网页读取功能，也可以**不安装 Skill**，按链接使用资料库。

## 最简单：不安装 Skill

对支持 GitHub 文件读取的 AI（如正确配置仓库访问能力的 DSH/Agent）发：

> 请读取 https://github.com/THREETIME333/NEFU-AI-Learning-Hub 的 HUB_INDEX.json，帮我查一下东林数据结构复习资料，附上来源和日期。没有就直说。

如果它说无法访问 GitHub，就需要更换支持 GitHub/网页读取的客户端或配置连接；不要以为发过链接就已经接入。

## Codex：安装整个 Skill 文件夹

### 方法 A：仓库内自动发现

1. 把项目 clone 或下载到本地。
2. 在项目目录用 Codex 打开工作区。
3. Codex 可以从仓库的 `.agents/skills/nefu-campus/SKILL.md` 发现这一 Skill。若没有显示可重新打开会话。
4. 可以明确告诉 Codex：“使用 nefu-campus Skill，回答东林宿舍的常见问题。”

注意：在**别的项目或普通对话中**，Codex 不会仅因知道这个 URL，就自动获得本仓库 Skill。

### 方法 B：在别的项目也使用

将整个 `.agents/skills/nefu-campus/` 文件夹复制到个人 Skill 目录 `~/.agents/skills/nefu-campus/`（Windows 通常是用户主目录下的 `.agents\\skills\\nefu-campus`）。复制的是完整文件夹，包含 `SKILL.md` 和 `references/`。

你也可以询问已启用的 Codex `$skill-installer`，让它从这个公开 GitHub 项目的 Skill 目录安装；在执行下载/修改前先确认来源。

## Claude Code：手动放入其 Skill 路径

将整个 `nefu-campus` 文件夹复制到项目的 `.claude/skills/nefu-campus/` 或用户层 `~/.claude/skills/nefu-campus/`，再在 Claude Code 中提问。具体支持细节以所用版本官方说明为准。

## DSH、DeepSeek 和其他 AI

- DSH 是否支持 Skill 自动安装取决于你使用的具体版本和插件能力，不作一概保证。
- 不支持自动安装也没关系：只要有 GitHub 读取能力，读取 `HUB_INDEX.json` 就能使用当前知识库。
- 普通 DeepSeek 网页聊天未必有 GitHub 文件工具，不能声称只发链接就一定生效。
- 如果只是想发布校园咨询和经验，先阅读 `references/CONTRIBUTION.md` 或直接在 GitHub 投稿；公开前注意匿名和隐私。

## 试用是否成功？

问 AI：

> 请实际读取 NEFU AI Learning Hub 的 HUB_INDEX.json 和 catalog.json，列出数据结构相关条目及其 kind，告诉我目前有没有已授权的2023年原卷。不要猜测。

能引用**真实存在的文件及路径**才算完成接入。仅靠模型记忆猜答案不能算。

## 隐私与安全

只读学习不需要向 AI 提供 GitHub 账号密码或私人 API Key。不要将自己的聊天全文、学号、实名邮箱或者校内需登录资料自动推送到公有仓库。
