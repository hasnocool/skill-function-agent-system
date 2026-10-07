# filename: skill_function_agent_system/batch.py
from __future__ import annotations

import asyncio
from typing import Any, Iterable

from .executor import FunctionExecutor
from .models import FunctionResult, FunctionSpec


async def execute_many(
    executor: FunctionExecutor,
    jobs: Iterable[tuple[FunctionSpec, Any]],
) -> list[FunctionResult]:
    """Run independent functions concurrently under the executor semaphore."""
    return await asyncio.gather(
        *(executor.execute(spec, payload) for spec, payload in jobs)
    )
