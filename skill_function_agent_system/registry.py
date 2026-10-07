# filename: skill_function_agent_system/registry.py
from __future__ import annotations

import json
from pathlib import Path

from .frontmatter import parse_frontmatter
from .models import SkillMetadata


class SkillRegistry:
    def __init__(self, skills_root: Path) -> None:
        self.skills_root = skills_root.expanduser().resolve()
        self._skills: dict[str, SkillMetadata] = {}

    @property
    def skills(self) -> tuple[SkillMetadata, ...]:
        return tuple(self._skills.values())

    def scan(self) -> tuple[SkillMetadata, ...]:
        self._skills.clear()
        if not self.skills_root.exists():
            raise FileNotFoundError(f"Skills directory does not exist: {self.skills_root}")

        for skill_file in sorted(self.skills_root.rglob("SKILL.md")):
            try:
                fm = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
                name = str(fm.values.get("name") or skill_file.parent.name)
                description = str(fm.values.get("description") or "")
                tags = fm.values.get("tags", ())
                if isinstance(tags, str):
                    tags = (tags,)
                metadata = SkillMetadata(
                    name=name,
                    description=description,
                    path=skill_file.parent,
                    tags=tuple(tags),
                    version=fm.values.get("version"),
                )
                self._skills[name] = metadata
            except (OSError, UnicodeError):
                continue
        return self.skills

    def save_index(self, destination: Path) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = [
            {
                "name": s.name,
                "description": s.description,
                "path": str(s.path.relative_to(self.skills_root)),
                "tags": list(s.tags),
                "version": s.version,
            }
            for s in self.skills
        ]
        destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def load_index(self, source: Path) -> tuple[SkillMetadata, ...]:
        payload = json.loads(source.read_text(encoding="utf-8"))
        self._skills = {
            item["name"]: SkillMetadata(
                name=item["name"],
                description=item.get("description", ""),
                path=self.skills_root / item["path"],
                tags=tuple(item.get("tags", ())),
                version=item.get("version"),
            )
            for item in payload
        }
        return self.skills
