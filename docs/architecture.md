# Architecture

## Separation of concerns

This repository contains runtime code only.

The independent Skill catalog belongs in:

    hasnocool/hasnocool-skills

The runtime never embeds the catalog. Point it at a checkout using:

    HASNOCOOL_SKILLS_DIR=/path/to/hasnocool-skills

## Progressive disclosure

1. Scan SKILL.md frontmatter.
2. Keep only name, description, tags, path and version in the registry.
3. Search metadata for a user request.
4. Load SKILL.md only for selected Skills.
5. Load references only when explicitly requested.
6. Discover function manifests only after a Skill is selected.
7. Execute functions asynchronously.
8. Return compact structured results to the model.

## Token strategy

The runtime is intentionally designed so that large implementation files, reference documents, and function source code are not automatically loaded into model context.

The model-facing adapter should expose metadata first and fetch full Skill/function details only after relevance is established.

## Function strategy

Functions are executable programs described by JSON manifests. Commands are passed directly to asyncio.create_subprocess_exec; no shell is used. JSON input is sent through stdin and JSON output is parsed when possible.

This makes deterministic work cheap in model context while keeping execution outside the prompt.

## Scaling

A catalog can contain thousands of Skills. For very large catalogs, replace the simple lexical discovery implementation with embeddings, BM25, SQLite FTS5, or a hybrid index without changing the Skill storage format.
