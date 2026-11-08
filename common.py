"""Small local-only IO and report helpers; no network requests."""
import html
import json
import os
from pathlib import Path
import sys
import tempfile

SITE = 'https://nbpojia.lol'
TELEGRAM = 'https://t.me/HaoNB_6666'
ADMIN = 'https://t.me/HaoNB_666'
VERSION = '1.0.0'


def configure_console():
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='backslashreplace')


def read_json(path, max_bytes=5_000_000):
    path = Path(path)
    if path.stat().st_size > max_bytes:
        raise ValueError('JSON exceeds the configured size limit')
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, delete=False) as output:
            temporary = Path(output.name)
            output.write(text)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def write_json(path, data):
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def report(title, data, extra=''):
    e = html.escape
    return '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>''' + e(title) + '''</title><style>
*{box-sizing:border-box}body{margin:0;background:#f4f6f2;color:#193b32;font:15px/1.7 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:44px 24px}header{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #dce6dc;padding-bottom:24px;gap:20px}.mark{background:#176651;color:white;border-radius:10px;padding:8px 12px;font-weight:800}h1{font-size:clamp(28px,4vw,42px);line-height:1.3;margin:38px 0 14px}a{color:#176651}nav{display:flex;gap:18px;flex-wrap:wrap}.hint{color:#6b7e73;font-size:13px}.panel{padding:24px;background:white;border:1px solid #dce6dc;border-radius:16px;margin:22px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.8 ui-monospace,Consolas,monospace;background:#edf2e8;padding:20px;border-radius:12px;max-height:650px;overflow:auto}table{border-collapse:collapse;width:100%;font-size:12px}td,th{border:1px solid #dce6dc;padding:8px;text-align:left;overflow-wrap:anywhere}.diff{overflow:auto}.diff table{width:auto;min-width:100%}.diff_add{background:#dcf3d8}.diff_sub{background:#f7d9d5}.diff_chg{background:#fff0b8}footer{font-size:12px;border-top:1px solid #dce6dc;margin-top:36px;padding-top:20px}.columns{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.task{margin:10px 0;padding:15px;background:#edf2e8;border-radius:10px}.task h3{font-size:15px;margin:0}@media(max-width:650px){.columns{grid-template-columns:1fr}header{align-items:flex-start;flex-direction:column}main{padding:25px 16px}}</style><main><header><span class="mark">NB / CODEX</span><nav><a href="''' + SITE + '''">NB破甲官网 ↗</a><a href="''' + TELEGRAM + '''">Telegram 社群 ↗</a><a href="''' + ADMIN + '''">管理员 ↗</a></nav></header><h1>''' + e(title) + '''</h1><p class="hint">Codex / codex破甲 / DeepSeek破甲 / 破甲工具箱 · Local tools, clear evidence.</p>''' + extra + '<section class="panel"><h2>报告数据</h2><pre>' + e(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)) + '''</pre></section><footer>本报告由本地工具生成，不连接模型 API。结果取决于输入资料与规则；“破甲”为 NB 品牌及社区关键词。<br><a href="''' + SITE + '''">了解 NB破甲</a> · <a href="''' + TELEGRAM + '''">加入 Telegram 交流群</a></footer></main></html>'''
