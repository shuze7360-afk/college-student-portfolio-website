# -*- coding: utf-8 -*-
"""
新增图片资产工具
================
把一张图片压缩后注入 assets/res_assets.json（供 template.html 中 RES.<key> 引用）。

用法示例:
    python add_asset.py --key my_cert_01 --file "D:\\证书\\获奖证书.jpg"
    python add_asset.py --key render_arm --file render.png --max-dim 1400 --quality 85

注入后的引用方式:
    onclick="openLightbox(RES.my_cert_01, '证书标题', '一句话描述')"
    多图画廊: onclick="openLightbox([RES.a, RES.b], '标题', '描述')"

⚠️ 隐私提醒: 上传证书/证明前，请先对原件做好脱敏（遮挡证件号、二维码、家庭住址等）。
"""
import argparse
import base64
import io
import json
import os
import sys

from PIL import Image

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
RES_JSON_PATH = os.path.join(SITE_DIR, 'assets', 'res_assets.json')


def image_to_data_uri(path, max_dim=1100, quality=78):
    im = Image.open(path)
    if im.mode in ('RGBA', 'P', 'LA'):
        bg = Image.new('RGB', im.size, (255, 255, 255))
        if im.mode != 'P':
            bg.paste(im, mask=im.split()[-1])
        else:
            bg.paste(im.convert('RGBA'))
        im = bg
    elif im.mode != 'RGB':
        im = im.convert('RGB')

    w, h = im.size
    if max(w, h) > max_dim:
        ratio = max_dim / float(max(w, h))
        im = im.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)

    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=quality, optimize=True)
    kb = len(buf.getvalue()) / 1024
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode(), im.size, kb


def main():
    ap = argparse.ArgumentParser(description='向 assets/res_assets.json 注入新图片资产')
    ap.add_argument('--key', required=True, help='资产键名，如 my_cert_01')
    ap.add_argument('--file', required=True, help='源图片路径 (jpg/png/webp)')
    ap.add_argument('--max-dim', type=int, default=1100, help='最长边像素上限 (默认 1100)')
    ap.add_argument('--quality', type=int, default=78, help='JPEG 质量 1-95 (默认 78)')
    args = ap.parse_args()

    if not os.path.exists(args.file):
        print(f'[错误] 图片不存在: {args.file}')
        sys.exit(1)

    with open(RES_JSON_PATH, 'r', encoding='utf-8') as f:
        res = json.load(f)

    uri, size, kb = image_to_data_uri(args.file, args.max_dim, args.quality)
    res[args.key] = uri

    with open(RES_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False)

    print(f'已注入资产: RES.{args.key}  (压缩后 {kb:.1f} KB, 尺寸 {size[0]}x{size[1]})')
    print(f'资产库现有 {len(res)} 项。下一步：在 template.html 中引用 RES.{args.key}，然后 python build.py')


if __name__ == '__main__':
    main()
