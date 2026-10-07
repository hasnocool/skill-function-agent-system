# filename: skill_function_agent_system/frontmatter.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class Frontmatter:
    values: dict[str, Any]
    body: str


def parse_frontmatter(text: str) -> Frontmatter:
    if not text.startswith("---"):
        return Frontmatter({}, text)

    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return Frontmatter({}, text)

    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return Frontmatter({}, text)

    values: dict[str, Any] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value.startswith("[") and value.endswith("]"):
            value = tuple(x.strip().strip('"').strip("'") for x in value[1:-1].split(",") if x.strip())
        values[key] = value

    return Frontmatter(values, "\n".join(lines[end + 1:]).lstrip())
