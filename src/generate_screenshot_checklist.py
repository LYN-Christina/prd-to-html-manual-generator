from __future__ import annotations

import argparse
import csv
from pathlib import Path

from utils import ensure_dir, read_json, write_text


def checklist_rows(slides: list[dict]) -> list[dict]:
    rows = []
    for slide in slides:
        if slide.get("slide_type") != "operation_dual_screen":
            continue
        scene_id = slide.get("scene_id") or slide["slide_id"].lower()
        role = slide.get("target_role", "待确认")
        rows.append(
            {
                "slide_id": slide["slide_id"],
                "scene_id": scene_id,
                "role": role,
                "pc_required": "Y",
                "mobile_required": "Y",
                "pc_filename": f"screenshots/pc/{scene_id}.png",
                "mobile_filename": f"screenshots/mobile/{scene_id}.png",
                "required_data_state": "使用 fake 或测试数据；状态需与页面主题一致",
                "privacy_notes": "不要出现真实客户、真实医院、真实价格、真实账号",
                "status": "todo",
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, rows: list[dict]) -> None:
    lines = [
        "# 截图清单",
        "",
        "| slide_id | scene_id | role | PC 截图 | 移动端截图 | 数据状态 |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['slide_id']} | {row['scene_id']} | {row['role']} | "
            f"`{row['pc_filename']}` | `{row['mobile_filename']}` | {row['required_data_state']} |"
        )
    lines.extend(
        [
            "",
            "## 截图要求",
            "",
            "- 使用 fake 或测试数据。",
            "- 不要出现真实客户、医院、价格、账号、手机号、邮箱。",
            "- 操作演示页必须同时准备 PC 截图和移动端截图。",
            "- 若某端暂无页面，请保留空缺，HTML 会生成「待补充截图」占位。",
        ]
    )
    write_text(path, "\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate screenshot checklist from slide plan.")
    parser.add_argument("--slide-plan", type=Path, default=Path("plans/slide_plan.json"))
    parser.add_argument("--out-md", type=Path, default=Path("plans/screenshot_checklist.md"))
    parser.add_argument("--out-csv", type=Path, default=Path("plans/screenshot_checklist.csv"))
    args = parser.parse_args()

    slides = read_json(args.slide_plan)
    rows = checklist_rows(slides)
    write_md(args.out_md, rows)
    if rows:
        write_csv(args.out_csv, rows)
    print(f"screenshot tasks: {len(rows)}")


if __name__ == "__main__":
    main()
