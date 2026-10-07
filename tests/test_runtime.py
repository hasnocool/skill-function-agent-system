# filename: tests/test_runtime.py
import asyncio
from pathlib import Path

from skill_function_agent_system.runtime import AgentRuntime


def test_discovery_and_lazy_load(tmp_path: Path) -> None:
    skill = tmp_path / "demo"
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Demonstration skill\ntags: [demo]\n---\n\n# Demo\n",
        encoding="utf-8",
    )

    runtime = AgentRuntime(tmp_path)
    results = runtime.search("demo")
    assert results
    loaded = runtime.load("demo")
    assert "# Demo" in loaded.instructions


def test_async_function_execution(tmp_path: Path) -> None:
    skill = tmp_path / "demo"
    functions = skill / "functions"
    functions.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Demonstration\n---\n\n# Demo\n",
        encoding="utf-8",
    )
    (functions / "echo.py").write_text(
        "import json,sys\np=json.load(sys.stdin)\nprint(json.dumps(p))\n",
        encoding="utf-8",
    )
    (functions / "echo.json").write_text(
        '{"name":"echo","description":"Echo JSON","command":["python","echo.py"],"output_format":"json"}',
        encoding="utf-8",
    )

    runtime = AgentRuntime(tmp_path)
    result = asyncio.run(runtime.call("demo", "echo", {"hello": "world"}))
    assert result.ok
    assert result.data == {"hello": "world"}
