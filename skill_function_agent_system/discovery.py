# filename: skill_function_agent_system/discovery.py
from __future__ import annotations

import re

from .models import SkillMetadata


def _terms(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9][a-z0-9_-]{1,}", text.lower())}


class SkillDiscovery:
    def __init__(self, skills: tuple[SkillMetadata, ...]) -> None:
        self.skills = skills

    def search(self, query: str, limit: int = 8) -> list[tuple[SkillMetadata, float]]:
        wanted = _terms(query)
        scored: list[tuple[SkillMetadata, float]] = []

        for skill in self.skills:
            terms = _terms(skill.searchable_text())
            if not wanted:
                score = 0.0
            else:
                overlap = wanted & terms
                score = len(overlap) / len(wanted)
                if skill.name.lower() in query.lower():
                    score += 0.5
            if score > 0:
                scored.append((skill, score))

        scored.sort(key=lambda item: (-item[1], item[0].name))
        return scored[:limit]
