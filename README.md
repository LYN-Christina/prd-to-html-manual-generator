# PRD to HTML Manual Generator

A lightweight workflow for generating B2B product operation manuals from PRDs and screenshots.

一个最小可用的 B 端产品操作手册生成工具，用于把 PRD、截图和人工审核结果整理成可浏览、可检查、可手动转 PPT 的 HTML 版操作手册分镜稿。

```text
PRD → 初版大纲 → 截图清单 → 手动上传截图 → HTML 分镜稿
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

## 快速开始

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 运行 demo：

```bash
python src/run_v1.py --project examples/demo_project
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

运行：

```bash
python src/run_v1.py --project your_project
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
PRD → 大纲 → 截图清单 → 手动上传截图 → HTML
```

暂不包含自动截图、PPTX 自动生成、复杂审批校验或在线协作能力。