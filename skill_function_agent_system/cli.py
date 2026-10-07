# filename: skill_function_agent_system/cli.py
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

from .runtime import AgentRuntime


def _runtime() -> AgentRuntime:
    root = os.environ.get("HASNOCOOL_SKILLS_DIR")
    if not root:
        raise SystemExit("Set HASNOCOOL_SKILLS_DIR to the checkout of hasnocool-skills.")
    return AgentRuntime(Path(root))


def main() -> None:
    parser = argparse.ArgumentParser(description="Skill Function Agent System")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("index")
    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=8)

    load = sub.add_parser("load")
    load.add_argument("name")

    funcs = sub.add_parser("functions")
    funcs.add_argument("query")
    funcs.add_argument("--limit", type=int, default=8)

    call = sub.add_parser("call")
    call.add_argument("skill")
    call.add_argument("function")
    call.add_argument("--json", default=None)

    args = parser.parse_args()
    runtime = _runtime()

    if args.command == "index":
        for skill in runtime.index():
            print(f"{skill.name}\t{skill.description}")

    elif args.command in {"search", "functions"}:
        for skill, score in runtime.search(args.query, args.limit):
            loaded = runtime.load(skill.name) if args.command == "functions" else None
            if loaded is None:
                print(f"{score:.3f}\t{skill.name}\t{skill.description}")
            else:
                for fn in loaded.functions.values():
                    print(f"{score:.3f}\t{skill.name}\t{fn.name}\t{fn.description}")

    elif args.command == "load":
        skill = runtime.load(args.name)
        print(skill.instructions)

    elif args.command == "call":
        payload = json.loads(args.json) if args.json else None
        result = asyncio.run(runtime.call(args.skill, args.function, payload))
        print(json.dumps({
            "name": result.name,
            "ok": result.ok,
            "exit_code": result.exit_code,
            "data": result.data,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration_ms": result.duration_ms,
        }, indent=2))
