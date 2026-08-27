#!/usr/bin/env python3
"""Validate the public, industry-neutral operational-planning skill contract."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
README = ROOT / "README.md"

EXPECTED_NAME = "designing-operational-plans"
REQUIRED_HEADINGS = (
    "# Designing Operational Plans",
    "## Overview",
    "## When to Use",
    "## Source Discipline",
    "## Operating Architecture",
    "## Core Workflow",
    "## Output Modes",
    "## Action Matrix",
    "## Measurement System",
    "## Decision Quality Checks",
    "## Quick Example",
    "## Common Mistakes",
    "## Final Gate",
)
REQUIRED_CONCEPTS = (
    "已知事实",
    "判断假设",
    "方案建议",
    "待确认事项",
    "业务目标",
    "用户目标",
    "过程目标",
    "成果目标",
    "长期目标",
    "触达 → 转化 → 入场 → 激活 → 参与 → 交付 → 反馈 → 留存 → 复购／转介绍",
    "决策版 + 执行版",
    "领先指标",
    "滞后指标",
    "建议值",
)
# These code-point sequences represent excluded domain vocabulary without
# embedding that vocabulary in the public repository's human-readable text.
EXCLUDED_CODEPOINTS = (
    (0x516C, 0x76CA),
    (0x6444, 0x5F71),
    (0x76F8, 0x673A),
    (0x955C, 0x5934),
    (0x5916, 0x62CD),
    (0x8BC4, 0x7247),
    (0x5B66, 0x5458),
    (0x8BFE, 0x7A0B),
    (0x4FF1, 0x4E50, 0x90E8),
    (0x5DE5, 0x4EBA, 0x6587, 0x5316, 0x5BAB),
    (0x5357, 0x4EAC),
    (0x57CE, 0x5E02, 0x5F71, 0x50CF),
    (0x5668, 0x6750, 0x4F53, 0x9A8C),
)
PLACEHOLDERS = ("TODO", "TBD", "XXX", "待补充")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.S)
    assert match, "missing or malformed YAML frontmatter"
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def main() -> int:
    skill_text = SKILL.read_text(encoding="utf-8")
    readme_text = README.read_text(encoding="utf-8")
    combined = skill_text + "\n" + readme_text
    frontmatter = parse_frontmatter(skill_text)

    assert frontmatter.get("name") == EXPECTED_NAME, "wrong skill name"
    description = frontmatter.get("description", "")
    assert description.startswith("Use when"), "description must start with 'Use when'"
    assert len(description) <= 500, "description is too long"

    for heading in REQUIRED_HEADINGS:
        assert heading in skill_text, f"missing heading: {heading}"
    for concept in REQUIRED_CONCEPTS:
        assert concept in skill_text, f"missing concept: {concept}"
    for codepoints in EXCLUDED_CODEPOINTS:
        term = "".join(chr(codepoint) for codepoint in codepoints)
        assert term not in combined, "excluded domain vocabulary found"
    for placeholder in PLACEHOLDERS:
        assert placeholder not in combined, f"unresolved placeholder: {placeholder}"

    output_modes = skill_text[skill_text.index("## Output Modes"):skill_text.index("## Action Matrix")]
    assert len(re.findall(r"(?m)^\d+\. ", output_modes)) >= 16, "standard output mode is incomplete"
    final_gate = skill_text[skill_text.index("## Final Gate"):]
    assert len(re.findall(r"(?m)^- \[ \] ", final_gate)) >= 12, "final gate is incomplete"
    assert "**记事型表达：**" in skill_text and "**架构型表达：**" in skill_text, "example pair is incomplete"

    print("PASS: public operational-planning skill contract and domain isolation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
