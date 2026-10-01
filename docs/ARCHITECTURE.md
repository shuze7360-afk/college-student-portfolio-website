# 架构与二次开发指南（ARCHITECTURE）

> 本文档面向想深度定制本模板的开发者。模板本身不含任何真实个人信息。

## 1. 核心设计思想

**"结构 + 资产"分离，构建期合体为单文件：**

```
template.html  ──┐
                 ├─▶ build.py ──▶ output/index.html（自包含单文件）
res_assets.json ─┘
```

- `template.html` 中图片位置全部写成 `RES.<key>` 引用，头部有一个
  `const RES = __RES_JSON_PLACEHOLDER__;` 占位脚本
- `assets/res_assets.json` 是键值对形式的图片资产库（`key → data URI`）
- `build.py` 把 JSON 注入占位符，产物即无任何外部引用的自包含 HTML

## 2. 页面区块（自上而下）

| 区块 | id | 说明 |
|---|---|---|
| 固定导航 | `navbar` | 64px 吸顶，滚动>50px 毛玻璃，移动端汉堡菜单 |
| Hero | `hero` | 100vh，双行标题逐行上升入场，滚动指示器 |
| 关于我 | `about` | 4:5 肖像卡 + 三段经历 + 四维数据统计 |
| 专长领域 | `expertise` | 3 张能力卡 + 四列技能矩阵 |
| 精选作品 | `work` | 2 列卡片，可挂载 Case Study 抽屉 |
| 荣誉汇编 | `credentials` | 双栏时间线（竞赛/在校荣誉），点击弹证书 |
| 联系方式 | `contact` | 深色反色区块 + 联系卡片列表 |
| 页脚 | `footer` | 版权 + 快速导航 |

## 3. 关键 JS 接口

```js
// 弹窗：单图 / 多图画廊 / 挂载 Case Study
openLightbox(RES.key, '标题', '描述')
openLightbox([RES.a, RES.b], '标题', '描述')
openLightbox([RES.img, ...], '标题', '描述', CASE_STUDIES.your_key)
```

**CASE_STUDIES 条目结构**（详见 `template.html` 中 `demo` 键示例）：

```json
{
  "meta": "赛事/项目定位一句话",
  "roles": ["角色1", "角色2"],
  "challenge": { "title": "设计挑战", "text": "…", "pains": ["…"] },
  "solution":  { "title": "核心攻坚方案", "items": [{ "k": "要点", "v": "展开" }] },
  "metrics":   { "title": "量化指标", "items": [{ "v": "0.52 s", "l": "单件节拍" }] },
  "iterations":[{ "v": "V1", "t": "阶段", "d": "说明" }],
  "gallery":   [{ "src": "data:image/jpeg;base64,…", "caption": "说明" }]
}
```

## 4. 设计系统（改肤入口）

所有设计变量集中在 `template.html` 的 `:root`：

| 变量 | 默认值 | 用途 |
|---|---|---|
| `--bg` | `#FBFBF9` | 暖白背景 |
| `--primary` | `#2C5F4F` | 深墨绿主色 |
| `--accent` | `#E8A87C` | 陶土橘点缀 |
| `--text` | `#1C1C1E` | 近黑正文 |
| `--radius-lg` | `22px` | 大圆角（卡片/肖像） |
| `--ease-out` | `cubic-bezier(0.16,1,0.3,1)` | 全局缓动 |

⚠️ **大数字排版铁律**：数据统计数字必须使用等高数字（Lining Figures），
`.stat-number` 已内置 `font-feature-settings:"lnum" 1,"tnum" 1` 与系统字体栈。
不要把标题的衬线体（Cormorant Garamond）套到数字上——其旧式数字高低不齐。

## 5. 新增一个荣誉条目的完整流程

```bash
# 1. 注入证书（先脱敏！）
python add_asset.py --key my_cert_20 --file "证书.jpg"

# 2. 在 template.html 的 credentials 区块加一行（参照现有 award-row）
#    <div class="award-row" onclick="openLightbox(RES.my_cert_20, '赛事名', '一句话')">
#      <span class="award-year">2026.01</span>
#      <div>
#        <div class="award-info-title">赛事全名</div>
#        <div class="award-info-sub">主办方/备注</div>
#      </div>
#      <span class="award-badge badge-gold">国家级一等奖</span>
#    </div>

# 3. 构建
python build.py
```

徽章配色：`badge-gold` 金橙（国奖/重量级）｜`badge-green` 墨绿（省奖/一等奖级）｜`badge-gray` 灰（其他）。
列表默认倒序（最新在最上）；每栏超过 4 条自动出现"展开更多"折叠。

## 6. 构建脚本红线自检

`build.py` 每次构建会检查：占位符已注入、RES 已内嵌、HTML 完整。
`configure.py` 会报告未回填的 `__TOKEN__`。

## 7. 技术要点备忘

- 全部图标为内联 SVG（线性风格 stroke 1.5~2）
- 字体：Cormorant Garamond（标题衬线）+ Manrope（正文无衬线），Google Fonts 引入，
  离线时回退系统字体（`-apple-system / PingFang SC / Microsoft YaHei`）
- 滚动显现：`IntersectionObserver`，阈值 0.1，单次触发，`.reveal-delay-1..4` 错落
- 鼠标光晕：`requestAnimationFrame` + 0.08 插值系数，移动端隐藏
- `prefers-reduced-motion` 下全部动画降级为瞬时
