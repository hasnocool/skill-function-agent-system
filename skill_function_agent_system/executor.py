# filename: skill_function_agent_system/executor.py
from __future__ import annotations

import asyncio
import json
import time
from typing import Any

from .models import FunctionResult, FunctionSpec


class FunctionExecutor:
    def __init__(self, max_concurrency: int = 8) -> None:
        self._semaphore = asyncio.Semaphore(max_concurrency)

    async def execute(self, spec: FunctionSpec, payload: Any = None) -> FunctionResult:
        async with self._semaphore:
            started = time.perf_counter()
            stdin = ""
            if payload is not None:
                stdin = json.dumps(payload, separators=(",", ":"))

            try:
                process = await asyncio.create_subprocess_exec(
                    *spec.command,
                    cwd=spec.path,
                    stdin=asyncio.subprocess.PIPE if stdin else asyncio.subprocess.DEVNULL,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(stdin.encode() if stdin else None),
                    timeout=spec.timeout_seconds,
                )
                duration_ms = (time.perf_counter() - started) * 1000
                text_out = stdout.decode("utf-8", errors="replace")
                text_err = stderr.decode("utf-8", errors="replace")
                data: Any = None
                if spec.output_format == "json" and text_out.strip():
                    try:
                        data = json.loads(text_out)
                    except json.JSONDecodeError:
                        data = None

                return FunctionResult(
                    name=spec.name,
                    ok=process.returncode == 0,
                    exit_code=process.returncode,
                    stdout=text_out,
                    stderr=text_err,
                    data=data,
                    duration_ms=duration_ms,
                )
            except asyncio.TimeoutError:
                try:
                    process.kill()
                    await process.wait()
                except (UnboundLocalError, ProcessLookupError):
                    pass
                return FunctionResult(
                    name=spec.name,
                    ok=False,
                    exit_code=None,
                    stderr=f"Function timed out after {spec.timeout_seconds:.1f}s",
                    duration_ms=(time.perf_counter() - started) * 1000,
                )
            except OSError as exc:
                return FunctionResult(
                    name=spec.name,
                    ok=False,
                    exit_code=None,
                    stderr=str(exc),
                    duration_ms=(time.perf_counter() - started) * 1000,
                )
