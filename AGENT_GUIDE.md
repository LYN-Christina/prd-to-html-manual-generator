# AGENT_GUIDE.md

This guide is written for AI coding agents such as Codex, Trae, WorkBuddy, Cursor, or similar tools.

目标用户是不熟悉代码的产品经理、实施顾问、培训交付人员。他们可以把 GitHub 仓库链接、PRD 文件和截图文件夹交给 AI coding agent，让 agent 运行本项目并生成 HTML 产品操作手册。

## 1. Task for the AI Agent

This repository is a PRD-to-HTML manual workflow. It helps generate a B2B product operation manual from:

- a PRD document,
- manually prepared screenshots,
- and a lightweight HTML template.

The V1 workflow is:

```text
PRD → outline → screenshot checklist → manual screenshot upload → HTML manual
```

The final deliverable is an editable/reviewable HTML storyboard, usually located at:

```text
your_project/output/manual.html
```

## 2. Agent execution flow

As the AI agent, follow this flow:

1. Clone or open this repository.
2. Install Python dependencies.
3. Create a user project directory.
4. Put the user PRD into `your_project/input/PRD.docx`.
5. Run the workflow for the first time to generate the outline and screenshot checklist.
6. Ask the user to upload screenshots according to the checklist.
7. Run the workflow again after screenshots are uploaded.
8. Return `output/manual.html` and the build report to the user.

The first run can be useful even when screenshots are not ready. It will generate placeholder pages and a screenshot checklist.

## 3. Standard project directory

Create or ask the user to prepare this directory structure:

```text
your_project/
├── input/
│   └── PRD.docx
├── screenshots/
│   ├── pc/
│   └── mobile/
└── output/
```

Notes:

- For PC-only projects, use `screenshots/pc/`.
- For mobile-only projects, use `screenshots/mobile/`.
- For dual-end projects, use both `screenshots/pc/` and `screenshots/mobile/`.
- If screenshots are missing, the generated HTML will show placeholder areas.

## 4. Commands the agent should run

Install dependencies:

```bash
pip install -r requirements.txt
```

First run, before screenshots are complete:

```bash
python src/run_v1.py --project your_project
```

After the user uploads screenshots, run again:

```bash
python src/run_v1.py --project your_project
```

Current V1 entry command is:

```bash
python src/run_v1.py --project your_project
```

If the project entry script changes in a future version, use the actual entry command in the repository instead.

## 5. Reminders the agent should give the user

Before processing user materials, remind the user:

- Do not upload real account passwords.
- Do not upload `.env` files.
- Do not upload production system links.
- If screenshots contain sensitive information, mask or anonymize them first.
- Do not include real customer names, real hospital names, real prices, phone numbers, emails, tokens, cookies, or session files.
- If screenshots are not ready, the agent can still generate an HTML placeholder version first.

## 6. Results the agent should return to the user

After running the workflow, return these files or file paths:

```text
your_project/output/manual.html
your_project/output/html_build_report.md
your_project/plans/screenshot_checklist.md
your_project/plans/screenshot_checklist.csv
```

Important: in V1, the screenshot checklist is generated under `plans/`, not `output/`.

Also summarize:

- missing screenshot pages,
- pages that need manual confirmation,
- whether PC screenshots were found,
- whether mobile screenshots were found,
- where the final HTML manual is located.

## 7. Prompt template for users

Users can copy this prompt into Codex / Trae / WorkBuddy / Cursor:

```text
Please open this GitHub repository and follow AGENT_GUIDE.md.

Repository:
<PASTE_GITHUB_REPOSITORY_URL_HERE>

My PRD is located at:
input/PRD.docx

My screenshots are located under:
screenshots/

Please run the V1 workflow.
First, generate the outline and screenshot checklist.
If screenshots are already available, continue and generate the HTML operation manual.

Please return:
- output/manual.html
- output/html_build_report.md
- plans/screenshot_checklist.md
- a list of missing screenshots
- a list of pages that need manual confirmation

Do not upload or expose any account passwords, .env files, production system links, tokens, cookies, or sensitive customer data.
If screenshots contain sensitive information, remind me to mask them before generating the final manual.
```

## 8. Limitations

V1 intentionally keeps the workflow lightweight:

- V1 does not automatically log in to systems.
- V1 does not automatically capture screenshots.
- V1 does not generate PPTX files.
- V1 outputs an HTML storyboard/manual.
- The HTML can later be manually converted into PPT or printed/exported as PDF.

## 9. Recommended agent behavior

When working with a non-technical user:

- Use plain language.
- Explain where the user should put the PRD and screenshots.
- Run the first pass even if screenshots are incomplete.
- Show the screenshot checklist clearly.
- Do not invent missing pages.
- Use placeholders when screenshots are missing.
- Ask for confirmation when screenshot pairing is unclear.
- Return the final HTML path and report path at the end.