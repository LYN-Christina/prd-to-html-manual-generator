# GitHub 迁移清单

本目录是从真实项目中抽离出来的 GitHub V1 版工具骨架。迁移时只保留通用能力，不携带任何真实交付资料。

## 已迁移 / 重写为通用版本

- `README.md`：通用项目说明。
- `.gitignore`：忽略真实输入、截图、输出、账号和缓存。
- `requirements.txt`：Python 最小依赖。
- `LICENSE`：MIT License。
- `config/*.yaml`：通用配置模板。
- `templates/manual_template.html`：可复用 HTML 手册模板。
- `src/*.py`：V1 最小流程脚本。
- `examples/demo_project/`：纯 fake demo 数据。

## 明确没有迁移

- 真实 PRD：`input/PRD.docx`
- 真实 PC 截图：`screenshots/pc/`
- 真实移动端截图：`screenshots/mobile/`
- 真实 HTML / PDF / PPT：`output/`
- 真实账号：`.env`
- 浏览器会话：`.auth/`
- 本次项目计划和报告：`plans/`、`reports/`

## 发布前必须检查

- [ ] `git status` 中没有 `.env`。
- [ ] `git status` 中没有 `.auth/`。
- [ ] `git status` 中没有真实 `input/`。
- [ ] `git status` 中没有真实 `screenshots/`。
- [ ] `git status` 中没有真实 `output/`。
- [ ] 搜索仓库内是否存在客户名称、账号、IP、密码、医院、价格等敏感内容。

## V1 范围

V1 只实现：

```text
PRD → 大纲 → 截图清单 → 手动上传截图 → HTML
```

暂不实现：

- 自动登录真实系统
- 自动 PC 截图
- 微信小程序自动化
- PPTX 自动生成
- PDF 导出
- PRD 与实际页面自动差异审核
