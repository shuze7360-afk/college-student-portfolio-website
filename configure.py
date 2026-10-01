# -*- coding: utf-8 -*-
"""
站点信息配置工具
================
读取 profile.json，把 template.html 中的 __TOKEN__ 占位符替换为您的真实信息。

用法:
    cp profile.example.json profile.json   # Windows 用 copy
    # 编辑 profile.json 填入您的信息
    python configure.py
    python build.py

说明:
- configure.py 直接修改 template.html（Git 会记录差异，随时可回滚）
- 可重复运行：已替换过的内容不再包含占位符，脚本会提示"无占位符可替换"
"""
import json
import os
import re
import sys

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(SITE_DIR, 'template.html')
PROFILE_PATH = os.path.join(SITE_DIR, 'profile.json')


def main():
    if not os.path.exists(PROFILE_PATH):
        print('[错误] 未找到 profile.json。请先：')
        print('  1. 复制 profile.example.json 为 profile.json')
        print('  2. 编辑填入您的真实信息')
        print('  3. 再运行 python configure.py')
        sys.exit(1)

    with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
        profile = json.load(f)

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        tpl = f.read()

    tokens = sorted(set(re.findall(r'__[A-Z0-9_]+__', tpl)))
    # __RES_JSON_PLACEHOLDER__ 由 build.py 注入图片资产库，configure.py 不处理
    tokens = [t for t in tokens if t != '__RES_JSON_PLACEHOLDER__']
    if not tokens:
        print('template.html 中已无占位符（可能已配置过）。如需重新配置，请 git checkout template.html')
        return

    missing_in_profile = []
    for tok in tokens:
        key = tok.strip('_').lower()
        if key in profile and str(profile[key]).strip():
            tpl = tpl.replace(tok, str(profile[key]))
        else:
            missing_in_profile.append((tok, key))

    if missing_in_profile:
        print('[警告] 以下占位符在 profile.json 中缺少对应字段，将原样保留：')
        for tok, key in missing_in_profile:
            print(f'  {tok}  (请在 profile.json 增加 "{key}" 字段)')

    with open(TEMPLATE_PATH, 'w', encoding='utf-8') as f:
        f.write(tpl)

    left = sorted(set(re.findall(r'__[A-Z0-9_]+__', tpl)))
    if left:
        print(f'[提示] 仍有 {len(left)} 个占位符未替换（保留为空也可先构建预览）:', left)
    else:
        print('[OK] 全部占位符已替换完成！接下来运行 python build.py 构建站点')


if __name__ == '__main__':
    main()
