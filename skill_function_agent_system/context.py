# filename: skill_function_agent_system/context.py
from __future__ import annotations

from .models import LoadedSkill, SkillMetadata


def discovery_context(results: list[tuple[SkillMetadata, float]]) -> list[dict[str, object]]:
    """Return the small model-facing discovery layer."""
    return [
        {
            "name": skill.name,
            "description": skill.description,
            "tags": skill.tags,
            "score": round(score, 4),
        }
        for skill, score in results
    ]


def skill_context(skill: LoadedSkill) -> dict[str, object]:
    """Return a loaded Skill without eagerly including reference files."""
    return {
        "name": skill.metadata.name,
        "description": skill.metadata.description,
        "instructions": skill.instructions,
        "functions": [
            {
                "name": fn.name,
                "description": fn.description,
                "input_format": fn.input_format,
                "output_format": fn.output_format,
            }
            for fn in skill.functions.values()
        ],
    }
