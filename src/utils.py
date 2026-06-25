from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(text: str, fallback: str = "scene") -> str:
    text = text.strip().lower()
    replacements = {
        "新增": "create",
        "提交": "submit",
        "查看": "view",
        "列表": "list",
        "详情": "detail",
        "审批": "approve",
        "通过": "pass",
        "拒绝": "reject",
        "转签": "transfer",
        "反馈": "feedback",
        "延期": "extension",
        "查询": "search",
        "消息": "message",
    }
    for source, target in replacements.items():
        text = text.replace(source, f" {target} ")
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text or fallback
