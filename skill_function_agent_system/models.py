# filename: skill_function_agent_system/models.py
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True, frozen=True)
class SkillMetadata:
    name: str
    description: str
    path: Path
    tags: tuple[str, ...] = ()
    version: str | None = None

    def searchable_text(self) -> str:
        return " ".join((self.name, self.description, *self.tags)).lower()


@dataclass(slots=True, frozen=True)
class FunctionSpec:
    name: str
    description: str
    command: tuple[str, ...]
    path: Path
    timeout_seconds: float = 60.0
    input_format: str = "json"
    output_format: str = "json"


@dataclass(slots=True)
class FunctionResult:
    name: str
    ok: bool
    exit_code: int | None
    stdout: str = ""
    stderr: str = ""
    data: Any = None
    duration_ms: float = 0.0


@dataclass(slots=True)
class LoadedSkill:
    metadata: SkillMetadata
    instructions: str
    references: dict[str, str] = field(default_factory=dict)
    functions: dict[str, FunctionSpec] = field(default_factory=dict)
