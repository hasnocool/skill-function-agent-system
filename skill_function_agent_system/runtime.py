# filename: skill_function_agent_system/runtime.py
from __future__ import annotations

from pathlib import Path

from .discovery import SkillDiscovery
from .executor import FunctionExecutor
from .loader import SkillLoader
from .models import FunctionResult, LoadedSkill, SkillMetadata
from .registry import SkillRegistry


class AgentRuntime:
    """Core runtime: discover cheaply, load lazily, execute functions asynchronously."""

    def __init__(self, skills_root: Path, max_function_concurrency: int = 8) -> None:
        self.registry = SkillRegistry(skills_root)
        self.loader = SkillLoader()
        self.executor = FunctionExecutor(max_function_concurrency)
        self._discovery: SkillDiscovery | None = None

    def index(self) -> tuple[SkillMetadata, ...]:
        skills = self.registry.scan()
        self._discovery = SkillDiscovery(skills)
        return skills

    def search(self, query: str, limit: int = 8) -> list[tuple[SkillMetadata, float]]:
        if self._discovery is None:
            self.index()
        assert self._discovery is not None
        return self._discovery.search(query, limit)

    def load(self, name: str) -> LoadedSkill:
        if not self.registry.skills:
            self.index()
        metadata = next((s for s in self.registry.skills if s.name == name), None)
        if metadata is None:
            raise KeyError(f"Unknown Skill: {name}")
        return self.loader.load(metadata)

    async def call(self, skill_name: str, function_name: str, payload=None) -> FunctionResult:
        skill = self.load(skill_name)
        spec = skill.functions.get(function_name)
        if spec is None:
            raise KeyError(f"Unknown function {function_name!r} in Skill {skill_name!r}")
        return await self.executor.execute(spec, payload)
