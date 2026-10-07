# Skill Repository Contract

The runtime and Skill catalog are deliberately separate repositories.

## Runtime

hasnocool/skill-function-agent-system owns:

- registry
- discovery
- lazy loading
- model-facing context shaping
- function execution
- concurrency
- security policy
- CLI
- tests

## Skills

hasnocool/hasnocool-skills owns:

- SKILL.md files
- references
- function manifests
- function implementations
- domain organization

## Installation

Clone both repositories independently.

Then:

    export HASNOCOOL_SKILLS_DIR=/absolute/path/to/hasnocool-skills

The runtime does not copy Skills into its source tree.

## Security

A Skill function is executable code. Only point HASNOCOOL_SKILLS_DIR at a trusted catalog or execute functions inside an appropriate sandbox/container. The runtime deliberately uses exec-style subprocess invocation rather than a shell, but that does not make untrusted code safe.
