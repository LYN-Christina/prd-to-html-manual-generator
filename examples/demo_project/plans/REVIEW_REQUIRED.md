# Manual review required

The outline and screenshot checklist have been generated. Please confirm whether they meet your needs before generating HTML.

## 1. Review and edit if needed

Please review these files:

- `manual_outline.md`
- `slide_plan.json`
- `screenshot_checklist.md`
- `screenshot_checklist.csv`

Check for missing scenes, wrong page titles, incorrect roles, unclear screenshot tasks, and sensitive information.

HTML page structure is generated mainly from `slide_plan.json`. The screenshot checklist is primarily a human capture guide.

## 2. Prepare screenshots after approval

If the outline and screenshot checklist are correct, take screenshots according to `screenshot_checklist.md`, use the required filenames, and put the files into the required folders.

Typical folders are:

```text
your_project/screenshots/pc/
your_project/screenshots/mobile/
```

## 3. Approve and generate HTML

When review and screenshot preparation are complete, create `REVIEW_APPROVED.md` in this same `plans/` directory. Then run:

```bash
python src/run_v1.py --project your_project --stage html
```
