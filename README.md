# 单文件个人作品集模板 | Single-File Portfolio Template

> Apple 风格极简高级感 + 人文气质的**个人作品集网站模板**。
> 整站构建为 **一个 HTML 文件**：所有图片以 Base64 内嵌，零外部依赖——双击即开、离线可用、微信/邮件直接发送、任意静态托管一键部署。

![Tech](https://img.shields.io/badge/依赖-零外部框架-brightgreen) ![Size](https://img.shields.io/badge/产物-单文件~2MB-blue) ![License](https://img.shields.io/badge/License-MIT-orange)

---

## ✨ 特性

- **真·单文件产物**：`build.py` 把结构母版与图片资产库合并为一个自包含 HTML，不依赖任何 CDN/图片文件夹
- **Apple 风设计系统**：暖白底 + 深墨绿 + 陶土橘，衬线标题 × 无衬线正文，柔和阴影与丝滑缓动
- **7 大区块**：毛玻璃导航 / Hero 双行入场 / 关于我 + 四维数据 / 专长 + 技能矩阵 / 精选作品 / 荣誉汇编时间线 / 深色联系区块
- **证书弹窗画廊**：荣誉条目点击即弹出证书原件，支持多图缩略图切换（内置隐私提示：上传前请脱敏）
- **工程 Case Study 抽屉**：项目卡片可挂载结构化复盘（挑战 → 方案 → 量化指标 → 迭代史 → 图集），示例见第一张作品卡
- **全局动效**：滚动显现、鼠标跟随光晕、锚点平滑滚动、`prefers-reduced-motion` 无障碍适配
- **响应式**：1024 / 768 / 480 三档断点，移动端汉堡菜单
- **纯本地构建**：只需 Python 3 + Pillow，不需要 Node/框架/包管理器

## 🚀 快速开始（3 步）

```bash
# 0) 环境：Python 3.8+，安装依赖
pip install Pillow

# 1) 配置您的个人信息
copy profile.example.json profile.json     # macOS/Linux: cp profile.example.json profile.json
#    编辑 profile.json，填入姓名/简介/联系方式/数据指标
python configure.py

# 2) 构建
python build.py

# 3) 打开产物
output/index.html   # 双击即可预览，可直接部署
```

> 未配置 `profile.json` 也能构建——页面会以「你的名字」等占位文案显示，方便先看效果。

## 🖼️ 添加您的真实图片（证书 / 项目图 / 肖像）

```bash
# 把图片压缩并注入资产库（自动缩放至最长边 1100px、质量 78）
python add_asset.py --key my_cert_01 --file "D:\证书\国奖证书.jpg"
```

然后在 `template.html` 中引用：

```html
<!-- 单图 -->
onclick="openLightbox(RES.my_cert_01, '全国大学生机器人大赛 一等奖', '一句话描述')"

<!-- 多图画廊 -->
onclick="openLightbox([RES.my_render, RES.my_cert_01], '项目标题', '描述')"
```

模板自带的 `demo_cert_*` / `demo_render_*` / `avatar` 均为程序生成的**占位图**，替换后可删除。

### 启用工程 Case Study 抽屉（可选进阶）

在 `template.html` 中找到 `const CASE_STUDIES = {...}`，参照内置的 `demo` 键的结构，为您的项目写一份复盘（挑战/方案/量化指标/迭代史/图集），然后在作品卡片的 `openLightbox(...)` 第 4 个参数传入 `CASE_STUDIES.your_key`。

## 👥 适合谁

- 工科学生/工程师做**保研复试、求职、竞赛答辩**配套的作品集主页
- 想要一个**不依赖建站平台、数据完全自持**的个人站点
- 喜欢Apple 风、但不想从零写 CSS 的人

## 🔒 隐私与脱敏清单（重要）

本模板**不包含任何真实个人信息**（示例人物、证书均为程序生成的占位内容）。您在使用时也请遵守：

- [ ] 证书/证明扫描件：遮挡**证件号、二维码、家庭住址**等敏感字段后再 `add_asset.py` 注入
- [ ] 志愿时长等官方证明：仅保留姓名与时长即可
- [ ] `profile.json` 含真实联系方式：**已被 `.gitignore` 排除**，切勿手动加入版本库
- [ ] 公开部署前，通读一遍 `output/index.html` 或用浏览器内搜索检查姓名/电话
- [ ] 若部署到公网，考虑用 GitHub Pages 私有仓库 + Vercel 等方案控制可见性

## 📁 目录结构

```
├── template.html          # 结构母版（文案/CSS/区块都在这里改）
├── profile.example.json   # 站点信息示例（复制为 profile.json 填写）
├── configure.py           # 把 profile.json 回填进母版占位符
├── build.py               # 母版 + 资产库 → 单文件 output/index.html
├── add_asset.py           # 压缩图片并注入资产库
├── assets/
│   └── res_assets.json    # 图片资产库（Base64），默认为演示占位图
├── docs/ARCHITECTURE.md   # 架构与二次开发指南
└── output/                # 构建产物（git 忽略）
```

## 🧭 数据流

```
profile.json ──configure.py──▶ template.html（占位符回填）
                                     │
assets/res_assets.json ───────────▶ build.py ──▶ output/index.html（单文件成品）
```

## ❓FAQ

**Q: 为什么产物有 2MB 左右？** 图片全部 Base64 内嵌所致——这是"单文件零依赖"的代价，换来的是随处可发、离线秒开。证书图越大产物越大，`add_asset.py` 已自动压缩。

**Q: 能部署上线吗？** 能。`output/index.html` 是纯静态文件，GitHub Pages / Vercel / Netlify / 云服务器均可。

**Q: 想改配色/字体？** 全部 CSS 变量集中在 `template.html` 顶部的 `:root`，改 6 个颜色变量即可整站换肤。

**Q: 移动端适配？** 已内置三档响应式断点与触摸友好的弹窗，无需额外处理。

## 📄 License

[MIT](LICENSE) — 可自由用于个人/商业项目，请保留 LICENSE 文件。**构建产物中如您填入了真实个人信息，其隐私责任由使用者自行承担。**
