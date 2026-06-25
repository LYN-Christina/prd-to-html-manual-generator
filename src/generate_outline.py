from __future__ import annotations

import argparse
from pathlib import Path

from utils import read_json, slugify, write_json, write_text


DEFAULT_OPERATION_SCENES = [
    ("新增申请", "申请人", ["进入新增页面", "填写基础信息", "确认业务数据", "提交申请"]),
    ("查看申请列表", "申请人", ["进入我的申请", "按状态筛选", "查看列表字段"]),
    ("查看申请详情", "申请人", ["打开申请详情", "核对基础信息", "查看审批记录"]),
    ("审批处理", "审批人", ["进入待审批", "查看申请详情", "选择通过/拒绝/转签", "填写意见"]),
    ("批量审批", "审批人", ["选择多条记录", "打开批量审批", "填写必填意见", "提交处理"]),
    ("执行反馈", "申请人", ["查看已通过申请", "选择使用/废弃/延期", "确认反馈结果"]),
    ("消息通知", "相关角色", ["接收通知", "打开消息详情", "跳转查看工单"]),
]


def build_slide_plan(parsed: dict) -> list[dict]:
    title = parsed.get("title") or "示例产品操作手册"
    slides: list[dict] = [
        {
            "slide_id": "S001",
            "slide_title": title,
            "slide_type": "cover",
            "target_role": "全员",
            "learning_goal": "了解本操作手册适用范围。",
            "key_steps": [],
            "needs_pm_confirmation": False,
        },
        {
            "slide_id": "S002",
            "slide_title": "培训目标与适用范围",
            "slide_type": "objective",
            "target_role": "全员",
            "learning_goal": "理解本模块解决的问题和培训边界。",
            "key_steps": [],
            "needs_pm_confirmation": False,
        },
        {
            "slide_id": "S003",
            "slide_title": "角色与权限说明",
            "slide_type": "role_overview",
            "target_role": "全员",
            "learning_goal": "理解不同角色在流程中的职责。",
            "key_steps": [],
            "needs_pm_confirmation": False,
        },
        {
            "slide_id": "S004",
            "slide_title": "业务流程总览",
            "slide_type": "process_overview",
            "target_role": "全员",
            "learning_goal": "掌握从提交到审批完成的完整流程。",
            "key_steps": [],
            "needs_pm_confirmation": False,
        },
    ]
    next_id = 5
    for title, role, steps in DEFAULT_OPERATION_SCENES:
        scene_id = slugify(title)
        slides.append(
            {
                "slide_id": f"S{next_id:03d}",
                "scene_id": scene_id,
                "slide_title": title,
                "slide_type": "operation_dual_screen",
                "target_role": role,
                "learning_goal": f"掌握「{title}」的关键操作。",
                "key_steps": steps,
                "pc_screenshot_required": True,
                "mobile_screenshot_required": True,
                "pc_expected_page": f"PC 端：{title}相关页面",
                "mobile_expected_page": f"移动端：{title}相关页面或状态页",
                "needs_pm_confirmation": True,
            }
        )
        next_id += 1
    slides.extend(
        [
            {
                "slide_id": f"S{next_id:03d}",
                "slide_title": "常见问题 FAQ",
                "slide_type": "faq",
                "target_role": "全员",
                "learning_goal": "快速定位常见操作问题。",
                "key_steps": [],
                "needs_pm_confirmation": True,
            },
            {
                "slide_id": f"S{next_id + 1:03d}",
                "slide_title": "培训总结",
                "slide_type": "summary",
                "target_role": "全员",
                "learning_goal": "回顾流程、角色和上线支持方式。",
                "key_steps": [],
                "needs_pm_confirmation": False,
            },
        ]
    )
    return slides


def build_outline(slides: list[dict]) -> str:
    lines = ["# 产品操作手册初版大纲", ""]
    for slide in slides:
        lines.append(f"## {slide['slide_id']} {slide['slide_title']}")
        lines.append(f"- 类型：{slide['slide_type']}")
        lines.append(f"- 角色：{slide['target_role']}")
        lines.append(f"- 目标：{slide['learning_goal']}")
        if slide.get("key_steps"):
            lines.append("- 操作步骤：")
            for step in slide["key_steps"]:
                lines.append(f"  - {step}")
        if slide.get("needs_pm_confirmation"):
            lines.append("- 需人工确认：是")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate outline and slide plan from parsed PRD.")
    parser.add_argument("--parsed", type=Path, default=Path("plans/parsed_prd.json"))
    parser.add_argument("--out-md", type=Path, default=Path("plans/manual_outline.md"))
    parser.add_argument("--out-json", type=Path, default=Path("plans/slide_plan.json"))
    args = parser.parse_args()

    parsed = read_json(args.parsed)
    slides = build_slide_plan(parsed)
    write_json(args.out_json, slides)
    write_text(args.out_md, build_outline(slides))
    print(f"slides: {len(slides)} -> {args.out_json}")


if __name__ == "__main__":
    main()
