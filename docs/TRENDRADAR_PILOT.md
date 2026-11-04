# TrendRadar 东林公开热榜云端试装（实验性）

这是一个**独立的、只读的 Github Actions 试运行**，不是安装到手机/Windows，也不是把 TrendRadar 原始代码直接复制进本仓库。

## 工作原理

- 任务在 GitHub 的临时 Linux Runner 上，读取固定版本的 [TrendRadar](https://github.com/sansan0/TrendRadar)。
- 只检查 **百度热搜、贴吧热榜、B站热搜**中的标题，并过滤“东北林业大学、东北林大、东林宿舍、NEFU”等关键词。
- 禁止付费 AI 分析、翻译和推送；不配置 API Key、平台 Cookie、代理、远程数据库和自动发布。
- 运行结束，将生成的公开 HTML 报告（如有）保存为 GitHub Actions Artifact，保留 7 天。手机上登录 GitHub 后可以下载查看。
- 如果热榜没有东林相关标题，**结果可能为空**。这不表示没有学生发帖，也不代表爬取了东林吧的普通帖子。
- 任何数据只可用作待核查线索，不能自动写入 `community_catalog.json` 或推断学校现行政策。

## 安全和费用

- 使用本公开仓库的标准 GitHub-hosted Runner。无需单独云服务器或付款方式。
- `permissions: contents: read` 且 checkout 不保留 GitHub 凭据；不向上游代码传入个人 Secrets。
- 依赖从上游固定提交 `946f52aa0704883f666c322888b8cd9af4cbcfff` 解析并安装。固定提交减少更新漂移，但依旧属于执行第三方代码，需要审核。
- 由于上游 API、站点限制等原因，可能出现可运行但拿不到目标内容的情况。
- 不托管长期数据库；历史、去重和持续订阅仍需独立存储方案，不可宣称已实现。
- 只有此 PR 被人工合并进入 `main` 后，GitHub Actions 的每天 **北京时间 15:23** 定时任务才会生效。PR 审核阶段只做一次 CI 试运行。

## 检查方法

1. 打开本 PR 的 **Checks** → `NEFU Public Hotlist Pilot (TrendRadar)`。
2. 依次检查依赖安装、配置和抓取步骤日志；不能仅凭绿色对勾判断有东林内容。
3. 在本次 Action 运行页面找到 `Artifacts`，下载 `nefu-public-hotlist-preview`（仅当有 HTML 输出）。
4. 如要停用：在 Actions 页面禁用该工作流，或删除本文件并提交。此前的每日维护任务不受影响。

## 不包含什么

这不是 RSSHub 或 MediaCrawler 的常驻云端安装，也不是贴吧指定关键词/帖子搜索，更不是小红书和抖音评论采集。如果以后要升级这些功能，应独立评估平台允许的访问范围、登录策略和是否真正需要云服务器。
