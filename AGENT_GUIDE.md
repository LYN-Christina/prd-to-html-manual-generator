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
PRD → outline → screenshot checklist → human review/edit → manual screenshot upload → HTML manual
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
5. Run the plan stage to generate the outline and screenshot checklist.
6. Return the generated outline and screenshot checklist to the user for review.
7. Let the user review and edit any missing, incorrect, or unclear items.
8. If the user confirms the outline and checklist are correct, ask the user to capture screenshots according to the checklist, use the required filenames, and place them in the required screenshot folders.
9. After the user confirms the outline/checklist, create `your_project/plans/REVIEW_APPROVED.md`.
10. Run the HTML stage.
11. Return `output/manual.html` and the build report to the user.

The plan stage is intentionally separated from the HTML stage. Do not continue to HTML for a real user project until the user confirms the outline and screenshot checklist.

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

First run: generate outline and screenshot checklist only.

```bash
python src/run_v1.py --project your_project --stage plan
```

Ask the user to review and, if needed, edit:

```text
your_project/plans/manual_outline.md
your_project/plans/slide_plan.json
your_project/plans/screenshot_checklist.md
your_project/plans/screenshot_checklist.csv
your_project/plans/REVIEW_REQUIRED.md
```

Important: HTML page structure is generated mainly from `slide_plan.json`. The screenshot checklist is primarily a human capture guide. If the user wants to change page titles, roles, steps, page order, or scene IDs, update `slide_plan.json` before running the HTML stage. If the outline and checklist meet the user needs, ask the user to follow `screenshot_checklist.md`, use the required filenames, and place screenshots into `screenshots/pc/` and / or `screenshots/mobile/`.

After the user confirms the outline and checklist, create:

```text
your_project/plans/REVIEW_APPROVED.md
```

Then generate HTML:

```bash
python src/run_v1.py --project your_project --stage html
```

For demo or automated tests only, the full workflow can be run with:

```bash
python src/run_v1.py --project examples/demo_project --stage all --skip-review
```

Current V1 entry command is:

```bash
python src/run_v1.py --project your_project --stage plan
python src/run_v1.py --project your_project --stage html
```

If the project entry script changes in a future version, use the actual entry command in the repository instead.

## 5. Reminders the agent should give the user

Before processing user materials, remind the user:

- Do not upload real account passwords.
- Do not upload `.env` files.
- Do not upload production system links.
- If screenshots contain sensitive information, mask or anonymize them first.
- Do not include real customer names, real hospital names, real prices, phone numbers, emails, tokens, cookies, or session files.
- If screenshots are not ready, the agent can still run the plan stage first.

Before generating HTML, remind the user:

- Review the outline.
- Review the slide plan.
- Review the screenshot checklist.
- If the outline and checklist are approved, ask the user to capture screenshots, use the required filenames, and place them in the specified folders.
- Confirm unclear pages or missing scenarios.

## 6. Results the agent should return to the user

After the plan stage, return these files or file paths:

```text
your_project/plans/manual_outline.md
your_project/plans/slide_plan.json
your_project/plans/screenshot_checklist.md
your_project/plans/screenshot_checklist.csv
your_project/plans/REVIEW_REQUIRED.md
```

After the HTML stage, return these files or file paths:

```text
your_project/output/manual.html
your_project/output/html_build_report.md
```

Important: in V1, the screenshot checklist is generated under `plans/`, not `output/`.

Also summarize:

- missing screenshot pages,
- pages that need manual confirmation,
- whether PC screenshots were found,
- whether mobile screenshots were found,
- what the user changed during manual review,
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

Please run the V1 workflow in two stages.

Stage 1:
Run the plan stage first. Generate the outline, slide plan, and screenshot checklist. Stop and show them to me for review. Do not generate the final HTML yet. If the outline and screenshot checklist meet my needs, remind me to capture screenshots according to the checklist, use the required filenames, and put them in the specified screenshot folders.

Stage 2:
After I confirm or edit the outline and screenshot checklist, create plans/REVIEW_APPROVED.md and run the HTML stage. Then generate the HTML operation manual.

Please return:
- plans/manual_outline.md
- plans/slide_plan.json
- plans/screenshot_checklist.md
- output/manual.html
- output/html_build_report.md
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
- Run the plan stage first.
- Show the outline and screenshot checklist clearly.
- Stop before HTML generation until the user confirms.
- Do not invent missing pages.
- Use placeholders when screenshots are missing.
- Ask for confirmation when screenshot pairing is unclear.
- Return the final HTML path and report path at the end.