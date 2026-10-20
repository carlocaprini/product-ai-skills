# Skill authoring contract

Each skill is a standalone Agent Skills package under `skills/<skill-name>/`. A consumer must be able to install that directory without depending on repository-level documentation or another skill.

## Required entry point

`SKILL.md` starts with YAML frontmatter containing:

```yaml
---
name: example-skill
description: Describes what the skill does and when it should be used.
---
```

- `name` matches the directory exactly, uses lowercase kebab-case, and is at most 64 characters.
- `description` is non-empty, at most 1,024 characters, and explains both capability and activation context.
- Portable optional fields may be used only when their meaning is verified against the current Agent Skills specification.
- Repository-specific fields are not presented as portable Agent Skills fields.

## Instruction design

Keep `SKILL.md` focused on decisions the agent would not reliably infer on its own:

- when to activate and when not to activate;
- minimum required input and optional context;
- the operational workflow and meaningful decision criteria;
- stop, escalation, permission, and read-only boundaries;
- how evidence, assumptions, and unknowns are separated;
- the concrete output and completion checks.

Move substantial conditional detail into small references and link it from the point where it becomes relevant. Do not make supporting files mandatory unless the skill actually uses them.

## Package boundaries

- Use relative links for runtime files.
- Keep every runtime dependency inside the package.
- Do not use parent traversal, external symlinks, credentials, private APIs, or local-machine paths.
- Do not require evaluation records or repository-level contributor documentation at runtime.
- Keep examples synthetic, original, and free of performance or customer claims.

## Public review

Review the complete package as public material, including assets and history. Passing validation confirms structural properties only; it does not establish usefulness, safety, compatibility, or quality.
