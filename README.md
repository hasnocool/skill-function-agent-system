# Skill Function Agent System

A Python 3.12 runtime for scaling an agent across a large external Skill library without loading every Skill into model context.

## Design

- Runtime logic lives here.
- Skills live in a separate repository: hasnocool/hasnocool-skills.
- Skill metadata is indexed and kept tiny.
- Full SKILL.md content is loaded only after discovery.
- References are loaded only on demand.
- Functions are deferred and executed as asynchronous subprocesses.
- Function source code never needs to enter model context; only structured results do.
- The runtime is provider/model agnostic.

## Quick start

Use a virtual environment, install this package, set HASNOCOOL_SKILLS_DIR to your checkout of hasnocool-skills, then run the sfas CLI.

See docs/architecture.md for the full architecture.
