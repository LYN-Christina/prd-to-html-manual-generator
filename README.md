# B2B Product Manual HTML Generator V1

一个最小可用的 B 端产品操作手册生成流程：

```text
PRD → 初版大纲 → 截图清单 → 手动上传截图 → HTML 分镜稿
```

V1 目标不是全自动生成 PPT，而是快速产出一个可浏览、可审核、可手动转 PPT 的 HTML 版产品操作手册。

## 核心原则

- PRD 只作为初始规划依据，最终内容以实际系统截图和人工审核为准。
- 操作演示页默认采用「左 PC 端截图 + 右移动端截图」的双端并列版式。
- 移动端小程序截图采用人工上传，不依赖 Playwright。
- 不提交 `.env`、真实账号、真实 PRD、真实截图、真实 HTML/PDF/PPT。
- 本仓库只保留通用脚本、模板、fake demo 和文档。

## 目录结构

```text
.
├─ config/                  # 通用配置模板
├─ examples/demo_project/    # 虚拟 demo 数据，不含真实客户资料
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

2. 复制 demo 项目到工作目录：

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

如果没有截图，HTML 会显示「待补充截图」占位；如果截图命名无法匹配，会在报告中提示人工确认。

## 截图命名建议

推荐按业务场景命名，方便自动配对：

```text
screenshots/pc/submit_application.png
screenshots/mobile/submit_application.png
```

移动端截图可以来自微信小程序人工截图，上传后只要放入 `screenshots/mobile/` 即可。

## 安全提醒

发布到 GitHub 前请确认：

- 没有真实 PRD。
- 没有真实截图。
- 没有 `.env`。
- 没有账号、密码、cookie、token、会话文件。
- 没有客户名称、医院名称、真实价格、真实人员信息。
