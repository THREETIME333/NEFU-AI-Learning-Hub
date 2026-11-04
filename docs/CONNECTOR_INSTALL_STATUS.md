# 国内平台开源工具：云端安装验证及其真实限制

> 本页面区分 **安装通过**、**能访问真实内容**、**已经长期部署** 三件完全不同的事。不要把 GitHub Actions 的临时环境误认为永久云服务器。

## 云端安装测试

工作流：[`NEFU Connector Install Smoke Tests`](../.github/workflows/nefu-connectors-smoke.yml)

首次 PR 测试可在 Pull Request → Checks 查看。工作流合并后仅提供手动触发（`workflow_dispatch`），**没有定时运行，不会无限消耗 GitHub Actions 算力**。

| 项目 | 云端测试内容 | 需要什么才可能长期使用 | 东林校园信息能否直接获得 |
|---|---|---|---|
| [RSSHub](https://github.com/DIYgod/RSSHub) | Docker 安装、启动和 `/healthz` 自检 | 持续在线的主机、有效的站点 RSS 路由 | 取决于具体 RSS 路由及平台权限；不是任意关键词的全网搜索 |
| [DailyHotApi](https://github.com/imsyy/DailyHotApi) | Node 依赖安装和构建 | 持续在线的服务或受支持的 Serverless 部署 | 仅热门榜单，不能替代东林吧内搜索 |
| [BilibiliPlayer](https://github.com/Yaemikoreal/BilibiliPlayer) | Python 依赖安装、入口语法检查 | 支持 MCP 的客户端；部分操作需要 B站扫码登录 | 需要实际搜索接口测试；安装通过不代表已登录 |
| [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) | Go 源码构建可执行程序 | 浏览器会话、登录授权和持久运行环境 | 未登录、未采集；不能保证云端 IP 可用 |
| [tieba-mcp](https://github.com/f25h-233/tieba-mcp) | Node/Python 依赖安装和语法检查 | 浏览器、运行环境和合法的站点访问权限 | 不运行浏览器签名或平台请求；不绕过 403、验证码 |
| [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) | uv 安装 Python 项目依赖和编译配置 | 浏览器、可能需要扫码登录、持久存储 | 未启动爬虫；只做安装验证 |
| [EasySpider](https://github.com/NaiboWang/EasySpider) | 源码结构检查 | **Windows/macOS 等桌面图形环境** | GitHub Actions 无图形桌面，**不视为已经安装** |

### 用户可以直接做什么？

- 手机查看本仓库：随时可用，**无需开电脑**。
- 手机查看 GitHub Actions 检查结果：随时可用。
- GitHub Actions 按需运行某个采集脚本：仅限允许访问的公开来源，且需另行开发。
- 手机随时连接一个已启动的 RSSHub/MCP API：**尚未实现**，需要持续在线的服务及安全访问控制。

### 安全边界

- 测试使用临时 GitHub 托管 Linux Runner，运行完成自动回收，不产生常驻服务。
- GitHub Token 限定为 `contents: read`；检出不保留凭据；不加载用户账号、Cookies、API 密钥、扫码凭证。
- 软件源固定到特定 Git 提交，便于审核。RSSHub Docker 镜像使用公开 `latest` 标签，仅作临时验证，不应在生产使用可漂移标签。
- 仅验证可安装、可编译或可启动，不批量访问小红书、贴吧、抖音，不绕过限制，不获取或保存评论全文。
- 公开知识库收录的内容仍需人工复核来源、时间、版权与隐私。
- 只有真正通过 PR 测试的步骤才可以标为“安装验证成功”，且仅指 **GitHub Actions 临时安装**。
- 如果 Github Actions 运行失败，请保留错误日志并修复，不要用猜测填写结果。

### 优先级建议

先选择能合法、稳定、低成本获取到**具体东林校园话题**的来源。热榜只是校园讨论来源中的辅助渠道，不应为了软件数量盲目安装七套长期服务。
