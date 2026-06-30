# PRD to HTML Manual Generator

A lightweight workflow for generating B2B product operation manuals from PRDs and screenshots.

一个最小可用的 B 端产品操作手册生成工具，用于把 PRD、截图和人工审核结果整理成可浏览、可检查、可手动转 PPT 的 HTML 版操作手册分镜稿。

```text
PRD → 初版大纲 → 截图清单 → 人工确认 / 修改 → 手动上传截图 → HTML 分镜稿
```

V1 聚焦轻量流程，不追求全自动 PPT，也不做自动截图。它更适合产品、实施、培训同学快速搭建手册初稿，再根据实际系统页面进行人工校对和补充。

## 安全提醒

本仓库只包含通用脚本、HTML 模板、文档和 fake demo。`examples/demo_project` 使用虚拟示例数据，不包含真实客户资料。

发布或使用自己的项目资料前，请确认：

- 不提交 `.env`。
- 不提交真实账号、密码、cookie、token 或会话文件。
- 不提交真实 PRD、真实截图、真实 HTML/PDF/PPT 交付物。
- 不提交客户名称、医院名称、真实价格、手机号、邮箱或真实人员信息。
- 使用 `examples/demo_project` 作为公开演示；真实项目请放在本地工作目录中，并确认已被 `.gitignore` 忽略。

## 适用场景

这个工具适合以下项目形态：

- PC 端产品操作手册
- 移动端产品操作手册
- PC + 移动端双端产品操作手册

版式规则：

- 双端项目采用「左 PC + 右移动端」并列版式。
- 单端项目使用单端操作页。
- 如果截图暂未准备好，HTML 会显示「待补充截图」占位。
- 如果截图命名无法匹配，应在人工审核时确认配对关系。

## V1 能做什么

- 解析 PRD 文档或 Markdown 示例 PRD。
- 生成初版手册大纲。
- 生成页级 slide plan。
- 生成截图清单。
- 在生成 HTML 前要求人工确认大纲和截图清单。
- 允许人工修改大纲、slide plan 和截图清单后再继续。
- 读取手动上传的 PC / 移动端截图。
- 生成一个可浏览的 HTML 操作手册分镜稿。

## 目录结构

```text
.
├─ config/                  # 通用配置模板
├─ examples/demo_project/    # fake demo 数据，不含真实客户资料
├─ src/                      # V1 最小流程脚本
├─ templates/                # HTML 模板与内联样式
├─ .gitignore
├─ LICENSE
├─ MIGRATION_CHECKLIST.md
├─ README.md
└─ requirements.txt
```

## No-code usage with AI agents

不会代码的产品经理、实施顾问或培训交付人员，也可以使用这个项目。

你可以把本仓库链接、PRD 文件和截图文件夹交给 Codex / Trae / WorkBuddy / Cursor 等 AI coding agent，让 agent 按照 [AGENT_GUIDE.md](AGENT_GUIDE.md) 自动运行 V1 流程：

```text
PRD → 大纲 → 截图清单 → 人工确认 / 修改 → 手动上传截图 → HTML
```

推荐给 AI agent 的输入包括：

- 本 GitHub 仓库链接
- `input/PRD.docx`
- `screenshots/pc/` 和 / 或 `screenshots/mobile/`

Agent 会先生成大纲和截图清单，并停下来让你确认或修改。若大纲和截图清单符合需求，请按截图清单完成截图、使用清单要求的文件名，并放入 `screenshots/pc/` 和 / 或 `screenshots/mobile/`。确认无误后，再继续生成 `output/manual.html` 和 `output/html_build_report.md`。

请注意：不要向 agent 上传 `.env`、账号密码、生产系统链接、token、cookie 或未脱敏的敏感截图。

## 快速开始

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 运行 demo（一次性跑完整流程，仅用于示例）：

```bash
python src/run_v1.py --project examples/demo_project --stage all --skip-review
```

3. 查看输出：

```text
examples/demo_project/output/manual.html
examples/demo_project/output/html_build_report.md
```

## 使用自己的项目

准备如下目录：

```text
your_project/
├─ input/
│  └─ PRD.docx
├─ screenshots/
│  ├─ pc/
│  └─ mobile/
└─ output/
```

第一步：生成大纲和截图清单，然后停止等待人工确认。

```bash
python src/run_v1.py --project your_project --stage plan
```

请人工检查并按需修改：

```text
your_project/plans/manual_outline.md
your_project/plans/slide_plan.json
your_project/plans/screenshot_checklist.md
your_project/plans/screenshot_checklist.csv
your_project/plans/REVIEW_REQUIRED.md
```

说明：HTML 页面结构主要依据 `slide_plan.json` 生成；截图清单主要用于指导人工准备截图。若要调整页面标题、角色、步骤或页面顺序，请优先修改 `slide_plan.json`。若大纲和截图清单符合需求，请按照 `screenshot_checklist.md` 完成截图、按要求命名，并放入 `screenshots/pc/` 和 / 或 `screenshots/mobile/`。

确认无误后，在 `your_project/plans/` 下创建：

```text
REVIEW_APPROVED.md
```

第二步：上传截图后生成 HTML。

```bash
python src/run_v1.py --project your_project --stage html
```

如果是单端项目，可以只准备对应端的截图目录；缺少的截图会在 HTML 中以占位形式呈现，便于后续补图和人工确认。

## 截图命名建议

推荐按业务场景命名，方便自动匹配：

```text
screenshots/pc/submit_application.png
screenshots/mobile/submit_application.png
```

命名不一致时也可以先生成 HTML，再根据报告和页面占位进行人工调整。

## 当前版本范围

V1 只覆盖最小可用流程：

```text
PRD → 大纲 → 截图清单 → 人工确认 / 修改 → 手动上传截图 → HTML
```

暂不包含自动截图、PPTX 自动生成、复杂审批校验或在线协作能力。