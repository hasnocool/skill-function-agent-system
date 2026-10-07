# filename: skill_function_agent_system/loader.py
from __future__ import annotations

import json
from pathlib import Path

from .frontmatter import parse_frontmatter
from .models import FunctionSpec, LoadedSkill, SkillMetadata


class SkillLoader:
    def load(self, metadata: SkillMetadata) -> LoadedSkill:
        skill_file = metadata.path / "SKILL.md"
        fm = parse_frontmatter(skill_file.read_text(encoding="utf-8"))

        functions: dict[str, FunctionSpec] = {}
        function_dir = metadata.path / "functions"
        if function_dir.is_dir():
            for manifest in sorted(function_dir.glob("*.json")):
                spec = json.loads(manifest.read_text(encoding="utf-8"))
                functions[spec["name"]] = FunctionSpec(
                    name=spec["name"],
                    description=spec.get("description", ""),
                    command=tuple(spec["command"]),
                    path=manifest.parent,
                    timeout_seconds=float(spec.get("timeout_seconds", 60)),
                    input_format=spec.get("input_format", "json"),
                    output_format=spec.get("output_format", "json"),
                )

        return LoadedSkill(
            metadata=metadata,
            instructions=fm.body,
            references={},
            functions=functions,
        )

    def load_reference(self, skill: LoadedSkill, relative_path: str) -> str:
        candidate = (skill.metadata.path / relative_path).resolve()
        if skill.metadata.path.resolve() not in candidate.parents:
            raise ValueError("Reference path escapes the Skill directory")
        if not candidate.is_file():
            raise FileNotFoundError(relative_path)
        content = candidate.read_text(encoding="utf-8")
        skill.references[relative_path] = content
        return content
