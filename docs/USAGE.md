# 编程任务看板使用指南

适合把 Codex / DeepSeek 协作任务拆成有验收条件的步骤。在本地 JSON 保存状态，以 HTML 看板或 Markdown 清单回顾进度。

## 示例命令

```bash
python main.py --board outputs/demo-board.json init
python main.py --board outputs/demo-board.json add "Implement parser" --accept "Empty and Unicode inputs pass"
python main.py --board outputs/demo-board.json move T001 doing
python main.py --board outputs/demo-board.json move T001 done --evidence "Unit tests passed"
python main.py --board outputs/demo-board.json export --out outputs/demo
```

## 数据约定

全局 `--board` 必须写在 init/add/move/export/list 子命令之前。add 必填 `--accept`，可重复 `--depends T001`。todo 只能进入 doing；doing 可退回 todo 或进入 done；done 可退回 todo。完成需 `--evidence` 非空；存在 doing/done 的依赖方时不能直接重开前置任务。最多建议 500 个任务。锁文件用于本机单写入者协调，非多人分布式服务；异常退出后应确认无写入进程再处理遗留 `.lock`。HTML 导出是快照，修改任务通过 CLI。

## 常见问题

- 路径不存在：从仓库根目录运行命令，给含空格的路径加引号。
- JSON 解析失败：使用 UTF-8，删除尾随逗号，查看报错行和字段。
- 输出被拒绝：确认目录可写，不要使用系统目录。
- 中文输出：入口自动配置 UTF-8；编辑器也应使用 UTF-8。
- HTML 报告：是本地快照，不需要服务器；不要把真实私密数据提交到公共仓库。

## 验证流程

运行单元测试与 `python smoke.py`。示例测试必须验证完整 CLI 链路，发布包使用固定源文件清单，并附 SHA-256。

[返回 README](../README.md) · [官网](https://nbpojia.lol) · [TG 社群](https://t.me/HaoNB_6666)
