from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run V1 flow: PRD -> outline -> screenshot checklist -> HTML.")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--prd", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    project = args.project.resolve()
    prd = args.prd or (project / "input" / "PRD.docx")
    if not prd.exists():
        md_prd = project / "input" / "PRD.fake.md"
        if md_prd.exists():
            prd = md_prd
        else:
            raise FileNotFoundError(f"PRD not found: {prd}")

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
    run([sys.executable, str(root / "src" / "build_html.py"), "--project", str(project)])


if __name__ == "__main__":
    main()
