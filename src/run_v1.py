from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


APPROVAL_FILE = "REVIEW_APPROVED.md"
REVIEW_FILE = "REVIEW_REQUIRED.md"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def resolve_prd(project: Path, prd_arg: Path | None) -> Path:
    prd = prd_arg or (project / "input" / "PRD.docx")
    if prd.exists():
        return prd
    md_prd = project / "input" / "PRD.fake.md"
    if md_prd.exists():
        return md_prd
    raise FileNotFoundError(f"PRD not found: {prd}")


def write_review_required(plans: Path) -> None:
    plans.mkdir(parents=True, exist_ok=True)
    review_path = plans / REVIEW_FILE
    if review_path.exists():
        return
    review_path.write_text(
        "# Manual review required\n\n"
        "The outline and screenshot checklist have been generated. Please confirm whether they meet your needs before generating HTML.\n\n"
        "## 1. Review and edit if needed\n\n"
        "Please review these files:\n\n"
        "- `manual_outline.md`\n"
        "- `slide_plan.json`\n"
        "- `screenshot_checklist.md`\n"
        "- `screenshot_checklist.csv`\n\n"
        "Check for missing scenes, wrong page titles, incorrect roles, unclear screenshot tasks, "
        "and sensitive information.\n\n"
        "HTML page structure is generated mainly from `slide_plan.json`. "
        "The screenshot checklist is primarily a human capture guide.\n\n"
        "## 2. Prepare screenshots after approval\n\n"
        "If the outline and screenshot checklist are correct, take screenshots according to `screenshot_checklist.md`, "
        "use the required filenames, and put the files into the required folders.\n\n"
        "Typical folders are:\n\n"
        "```text\n"
        "your_project/screenshots/pc/\n"
        "your_project/screenshots/mobile/\n"
        "```\n\n"
        "## 3. Approve and generate HTML\n\n"
        f"When review and screenshot preparation are complete, create `{APPROVAL_FILE}` in this same `plans/` directory. "
        "Then run:\n\n"
        "```bash\n"
        "python src/run_v1.py --project your_project --stage html\n"
        "```\n",
        encoding="utf-8",
    )


def run_plan_stage(root: Path, project: Path, prd: Path, skip_review: bool = False) -> None:
    plans = project / "plans"
    run([sys.executable, str(root / "src" / "parse_prd.py"), str(prd), "--out", str(plans / "parsed_prd.json")])
    run([
        sys.executable,
        str(root / "src" / "generate_outline.py"),
        "--parsed",
        str(plans / "parsed_prd.json"),
        "--out-md",
        str(plans / "manual_outline.md"),
        "--out-json",
        str(plans / "slide_plan.json"),
    ])
    run([
        sys.executable,
        str(root / "src" / "generate_screenshot_checklist.py"),
        "--slide-plan",
        str(plans / "slide_plan.json"),
        "--out-md",
        str(plans / "screenshot_checklist.md"),
        "--out-csv",
        str(plans / "screenshot_checklist.csv"),
    ])
    write_review_required(plans)
    if skip_review:
        print("\nPlan stage complete. --skip-review is enabled, so HTML generation may continue.")
        print("Use --skip-review only for demos or automated tests.")
    else:
        print("\nPlan stage complete. Please confirm the outline and screenshot checklist before generating HTML:")
        print(f"- Outline: {plans / 'manual_outline.md'}")
        print(f"- Slide plan: {plans / 'slide_plan.json'}")
        print(f"- Screenshot checklist: {plans / 'screenshot_checklist.md'}")
        print(f"- Review guide: {plans / REVIEW_FILE}")
        print("\nIf the outline/checklist need changes, edit the files above first.")
        print("If they meet your needs, take screenshots according to the checklist, use the required filenames,")
        print("and place them in the required folders, such as screenshots/pc/ and screenshots/mobile/.")
        print(f"\nAfter review and screenshot preparation, create: {plans / APPROVAL_FILE}")
        print("Then run: python src/run_v1.py --project your_project --stage html")


def ensure_review_approved(project: Path, skip_review: bool) -> None:
    if skip_review:
        return
    approval_path = project / "plans" / APPROVAL_FILE
    if approval_path.exists():
        return
    raise FileNotFoundError(
        "Manual review has not been approved yet. "
        f"Review the outline and screenshot checklist, then create: {approval_path}. "
        "Alternatively, use --skip-review only for demos or automated tests."
    )


def run_html_stage(root: Path, project: Path, skip_review: bool) -> None:
    slide_plan = project / "plans" / "slide_plan.json"
    if not slide_plan.exists():
        raise FileNotFoundError(
            f"Slide plan not found: {slide_plan}. Run --stage plan first."
        )
    ensure_review_approved(project, skip_review)
    run([sys.executable, str(root / "src" / "build_html.py"), "--project", str(project)])
    print("\nHTML stage complete:")
    print(f"- {project / 'output' / 'manual.html'}")
    print(f"- {project / 'output' / 'html_build_report.md'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run V1 flow with a manual review gate.")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--prd", type=Path, default=None)
    parser.add_argument(
        "--stage",
        choices=["plan", "html", "all"],
        default="plan",
        help="plan: generate outline/checklist and stop; html: build HTML after approval; all: run both stages.",
    )
    parser.add_argument(
        "--skip-review",
        action="store_true",
        help="Skip the manual approval file check. Use only for demos or automated tests.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    project = args.project.resolve()

    if args.stage in {"plan", "all"}:
        prd = resolve_prd(project, args.prd)
        run_plan_stage(root, project, prd, args.skip_review)

    if args.stage in {"html", "all"}:
        run_html_stage(root, project, args.skip_review)


if __name__ == "__main__":
    main()
