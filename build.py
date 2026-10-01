# -*- coding: utf-8 -*-
"""
一键构建脚本
============
template.html (已配置的结构母版) + assets/res_assets.json (图片资产库)
→ 注入合并 → 生成 100% 独立的单文件 HTML（所有图片 Base64 内嵌，零外部依赖）

用法:
    python build.py
产物: output/index.html （双击即可离线打开，可直接部署到 GitHub Pages / 任意静态托管）
"""
import json
import os
import sys

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(SITE_DIR, 'template.html')
RES_JSON_PATH = os.path.join(SITE_DIR, 'assets', 'res_assets.json')
OUTPUT_PATH = os.path.join(SITE_DIR, 'output', 'index.html')

PLACEHOLDER = '__RES_JSON_PLACEHOLDER__'


def build():
    for p in (TEMPLATE_PATH, RES_JSON_PATH):
        if not os.path.exists(p):
            print(f'[错误] 缺少必需文件: {p}')
            sys.exit(1)

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    with open(RES_JSON_PATH, 'r', encoding='utf-8') as f:
        res = json.load(f)

    empty_keys = [k for k, v in res.items() if not v or len(v) < 100]
    if empty_keys:
        print(f'[警告] 以下 {len(empty_keys)} 项资产为空（对应图片位置将无法显示）: {empty_keys}')

    if PLACEHOLDER not in template:
        print('[错误] template.html 中找不到占位符 __RES_JSON_PLACEHOLDER__，母版可能已损坏')
        sys.exit(1)

    html = template.replace(PLACEHOLDER, json.dumps(res, ensure_ascii=False), 1)

    # 红线自检
    tokens = sorted(set(__import__('re').findall(r'__[A-Z0-9_]+__', html)))
    if tokens:
        print(f'[提示] 仍有 {len(tokens)} 个信息占位符未配置（先运行 configure.py）: {tokens}')

    guards = {
        '占位符已完整注入': PLACEHOLDER not in html,
        'RES 资产库已内嵌': 'const RES' in html,
        'HTML 结尾完整': html.rstrip().endswith('</html>'),
    }
    for name, ok in guards.items():
        print(f"  {'PASS' if ok else 'FAIL'} - {name}")
    if not all(guards.values()):
        print('[错误] 自检未通过，终止构建')
        sys.exit(1)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    size_mb = os.path.getsize(OUTPUT_PATH) / 1024 / 1024
    print(f'构建完成: {OUTPUT_PATH} ({size_mb:.2f} MB, {len(res)} 项图片资产)')
    print('双击即可离线打开；也可将 output/index.html 部署到 GitHub Pages 等任意静态托管。')


if __name__ == '__main__':
    build()
