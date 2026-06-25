from __future__ import annotations

import argparse
import html
import os
from pathlib import Path

from utils import ensure_dir, read_json, read_text, write_text


IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".webp", ".svg"]


def find_image(directory: Path, scene_id: str) -> Path | None:
    if not directory.exists():
        return None
    candidates = []
    for path in directory.rglob("*"):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            score = 0
            name = path.stem.lower()
            if scene_id.lower() == name:
                score += 100
            if scene_id.lower() in name:
                score += 50
            for token in scene_id.lower().split("_"):
                if token and token in name:
                    score += 5
            if score:
                candidates.append((score, path))
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: (-item[0], str(item[1])))[0][1]


def rel(from_file: Path, target: Path) -> str:
    return Path(os.path.relpath(target.resolve(), from_file.parent.resolve())).as_posix()


def render_content_page(slide: dict, page_no: int) -> str:
    title = html.escape(slide["slide_title"])
    goal = html.escape(slide.get("learning_goal", ""))
    role = html.escape(slide.get("target_role", "全员"))
    return f"""
<section class="page">
  <span class="role">{role}</span>
  <h2>{title}</h2>
  <div class="content-card">
    <p>{goal}</p>
    <ul>
      <li>本页内容由 PRD 初步生成，请结合实际系统页面审核。</li>
      <li>如与实际页面不一致，以最终截图和业务确认结果为准。</li>
    </ul>
  </div>
  <div class="footer">Page {page_no}</div>
</section>
"""


def render_operation_page(slide: dict, page_no: int, pc_img: Path | None, mobile_img: Path | None, output_file: Path) -> str:
    title = html.escape(slide["slide_title"])
    role = html.escape(slide.get("target_role", "待确认"))
    scene_id = slide.get("scene_id", slide["slide_id"].lower())
    pc_html = (
        f'<img src="{html.escape(rel(output_file, pc_img))}" alt="PC screenshot">'
        if pc_img
        else '<div class="placeholder">待补充 PC 截图</div>'
    )
    mobile_html = (
        f'<img src="{html.escape(rel(output_file, mobile_img))}" alt="Mobile screenshot">'
        if mobile_img
        else '<div class="placeholder">待补充移动端截图</div>'
    )
    steps = slide.get("key_steps") or ["进入页面", "查看信息", "完成操作", "确认结果"]
    step_html = "\n".join(f'<div class="step">{html.escape(step)}</div>' for step in steps[:5])
    confirm = "" if pc_img and mobile_img else '<div class="confirm">需人工确认 / 补图</div>'
    return f"""
<section class="page">
  <span class="role">{role}</span>
  <h2>{title}</h2>
  <div class="dual" data-scene="{html.escape(scene_id)}">
    <div class="shot-card">
      <div class="shot-label">PC 端截图</div>
      {pc_html}
    </div>
    <div class="shot-card mobile-frame">
      <div class="shot-label">移动端截图</div>
      {mobile_html}
    </div>
  </div>
  {confirm}
  <div class="steps">{step_html}</div>
  <div class="footer">Page {page_no}</div>
</section>
"""


def build_html(project: Path) -> dict:
    slide_plan = project / "plans" / "slide_plan.json"
    template = Path(__file__).resolve().parents[1] / "templates" / "manual_template.html"
    output_file = project / "output" / "manual.html"
    pc_dir = project / "screenshots" / "pc"
    mobile_dir = project / "screenshots" / "mobile"

    slides = read_json(slide_plan)
    sections = []
    used_pc = set()
    used_mobile = set()
    missing_pc = []
    missing_mobile = []

    for i, slide in enumerate(slides, start=1):
        if slide.get("slide_type") == "operation_dual_screen":
            scene_id = slide.get("scene_id", slide["slide_id"].lower())
            pc_img = find_image(pc_dir, scene_id)
            mobile_img = find_image(mobile_dir, scene_id)
            if pc_img:
                used_pc.add(str(pc_img))
            else:
                missing_pc.append(slide["slide_title"])
            if mobile_img:
                used_mobile.add(str(mobile_img))
            else:
                missing_mobile.append(slide["slide_title"])
            sections.append(render_operation_page(slide, i, pc_img, mobile_img, output_file))
        else:
            sections.append(render_content_page(slide, i))

    html_doc = read_text(template).replace("{{ title }}", html.escape(slides[0]["slide_title"])).replace("{{ sections }}", "\n".join(sections))
    write_text(output_file, html_doc)
    report = {
        "html": str(output_file),
        "total_pages": len(slides),
        "used_pc_screenshots": len(used_pc),
        "used_mobile_screenshots": len(used_mobile),
        "missing_pc_pages": missing_pc,
        "missing_mobile_pages": missing_mobile,
    }
    lines = [
        "# HTML 构建报告",
        "",
        f"- HTML 总页数：{report['total_pages']}",
        f"- 使用 PC 截图数量：{report['used_pc_screenshots']}",
        f"- 使用移动端截图数量：{report['used_mobile_screenshots']}",
        f"- 缺少 PC 截图页面：{', '.join(missing_pc) if missing_pc else '无'}",
        f"- 缺少移动端截图页面：{', '.join(missing_mobile) if missing_mobile else '无'}",
        "",
        "## 后续建议",
        "",
        "- 浏览 HTML，确认每个操作页是否符合左 PC、右移动端的表达方式。",
        "- 对缺图页面补充截图后重新运行构建命令。",
        "- 手动转 PPT 时可按每个 section 作为一页分镜。",
    ]
    write_text(project / "output" / "html_build_report.md", "\n".join(lines))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Build HTML manual from slide plan and screenshots.")
    parser.add_argument("--project", type=Path, default=Path("."))
    args = parser.parse_args()

    ensure_dir(args.project / "output")
    report = build_html(args.project)
    print(f"html: {report['html']}")


if __name__ == "__main__":
    main()
