# Codex Task Board · 编程任务看板

**Codex / codex破甲 / DeepSeek / DeepSeek破甲 / 破甲 开发者工具系列**

[![CI](https://github.com/HaoHaolovestolearn/codex-task-board/actions/workflows/ci.yml/badge.svg)](https://github.com/HaoHaolovestolearn/codex-task-board/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

### NB破甲入口

**[🌐 项目官网](https://nbpojia.lol) · [💬 Telegram 社群](https://t.me/HaoNB_6666) · [📚 破甲教程](https://nbpojia.lol/tutorials/armor) · [🔌 API 教程](https://nbpojia.lol/tutorials/api)**

使用问题、示例交流和版本反馈可到 TG 群；需要联系管理员：[HaoNB_666](https://t.me/HaoNB_666)。请勿在群内发送密钥或私有源码。

## 这个项目解决什么

适合把 Codex / DeepSeek 协作任务拆成有验收条件的步骤。在本地 JSON 保存状态，以 HTML 看板或 Markdown 清单回顾进度。

本项目是 NB破甲社区的独立开源工具。`codex破甲`、`DeepSeek破甲` 和 `破甲` 用于标识社区系列；具体能力以本仓库代码和示例为准。项目与 OpenAI / DeepSeek 无官方隶属关系。

## 功能

- todo → doing → done，要求实际验收证据才能完成。
- 支持任务依赖，检查未知 ID、循环和未完成前置任务。
- 原子写入与本地写锁减少并发覆盖，初始化不覆盖旧数据。
- 导出三列离线 HTML、Markdown 和原始 JSON。

## 三分钟开始

需要 Python 3.10 或更高版本（CI 验证 Python 3.12）。Linux / macOS 可将 `python` 替换为 `python3`；Windows 可使用 `py -3`。只使用标准库，无需 pip 安装依赖。

```bash
git clone https://github.com/HaoHaolovestolearn/codex-task-board.git
cd codex-task-board
python main.py --board outputs/demo-board.json init
python main.py --board outputs/demo-board.json add "Implement parser" --accept "Empty and Unicode inputs pass"
python main.py --board outputs/demo-board.json move T001 doing
python main.py --board outputs/demo-board.json move T001 done --evidence "Unit tests passed"
python main.py --board outputs/demo-board.json export --out outputs/demo
```

命令在 `outputs/` 生成结果。用浏览器直接打开对应的 `.html` 文件即可查看离线报告，报告顶部和底部保留官网与 Telegram 社群入口。输入数据保留在本机，工具不调用模型接口；点击外部社群/官网链接时才会打开相应网站。

完整演示可运行：

```bash
python smoke.py
python main.py --help
```

`smoke.py` 在临时目录中验证示例，结束后清理结果；要保留报告请运行上面的 CLI 命令。

## 输入、输出与边界

全局 `--board` 必须写在 init/add/move/export/list 子命令之前。add 必填 `--accept`，可重复 `--depends T001`。todo 只能进入 doing；doing 可退回 todo 或进入 done；done 可退回 todo。完成需 `--evidence` 非空；存在 doing/done 的依赖方时不能直接重开前置任务。最多建议 500 个任务。锁文件用于本机单写入者协调，非多人分布式服务；异常退出后应确认无写入进程再处理遗留 `.lock`。HTML 导出是快照，修改任务通过 CLI。

更多字段和错误处理见 [使用指南](docs/USAGE.md)。示例均为虚构演示数据。

## 验证与自动发布

```bash
python -m unittest discover -s tests -v
python smoke.py
python build_release.py
```

每次提交 / Pull Request 自动在 Linux、Windows、macOS 运行测试和完整示例，并验证源码压缩包可构建。推送 `v*` 标签时，测试成功后自动发布 Source ZIP 与 SHA-256 校验文件。首版为 **v1.0.0**；[下载发布版本](https://github.com/HaoHaolovestolearn/codex-task-board/releases)。源码包需要 Python，不是独立可执行程序。

## 五个独立工具

| 项目 | 主要用途 |
| --- | --- |
| [Codex Context Pack](https://github.com/HaoHaolovestolearn/codex-context-pack) | 代码上下文打包器 |
| [Codex Prompt Check](https://github.com/HaoHaolovestolearn/codex-prompt-check) | 提示词模板检查器 |
| [Codex Usage Ledger](https://github.com/HaoHaolovestolearn/codex-usage-ledger) | Token 用量账本 |
| [Codex Response Diff](https://github.com/HaoHaolovestolearn/codex-response-diff) | 模型回答对比器 |
| [Codex Task Board](https://github.com/HaoHaolovestolearn/codex-task-board) | 编程任务看板 |

它们各自维护源码、示例、测试、CI 与 Release，可以单独使用。

## English

Codex Task Board is a local-first Python developer utility for Codex and DeepSeek workflows. 管理任务状态、依赖、验收条件，并导出本地 HTML 看板. It uses the Python standard library, produces reviewable local outputs, and does not send input data to a model service. NB Pojia is a community label; this repository is independently maintained.

## 参与和联系

欢迎提交带复现输入和预期行为的 Issue / PR。参见 [贡献指南](CONTRIBUTING.md)、[更新记录](CHANGELOG.md) 和 [MIT 许可证](LICENSE)。

**[NB破甲官网](https://nbpojia.lol) · [加入 Telegram 社群](https://t.me/HaoNB_6666)**
