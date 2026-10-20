# Quality and evaluation policy

Quality evidence is separated into three distinct layers. A result in one layer never implies a result in another.

## Static validation

Static checks run automatically and without AI-provider credentials. They cover repository safety, package naming, `SKILL.md` frontmatter, local references, package confinement, and the validator's own tests.

Static validity does not mean that a skill installs, triggers correctly, produces a useful result, or works in a particular client.

## Routing and behavioral evaluation

Each published package keeps a public `tests/evals.md` record containing:

- at least three positive activation prompts;
- at least three negative or near-miss prompts, including overlap with adjacent capabilities;
- at least three behavior cases covering sufficient evidence, missing critical input, and a contradictory or high-impact case;
- at least two controlled comparisons using the same rubric with and without the skill.

Each case records an identifier, synthetic prompt, expected route, context, expected output properties, forbidden behavior, reviewer rubric, environment and client version, date, observed result, and limitations.

Expected and observed results remain separate. An evaluation that has not been executed is marked `not run`; it is never recorded as passing.

## Portability and installation evidence

Before a package is described as published or compatible, install it by itself from an immutable public revision in a clean environment. Record the exact source revision, command or manual procedure, installed files, client and version, date, a positive activation check, a near miss, and known limitations.

The following states remain distinct:

- structurally valid;
- installed;
- activated as expected;
- behaviorally reviewed;
- verified on a named client and version.

Evaluation records contain only synthetic or sanitized public material. Paid or externally hosted evaluation is not part of pull request validation.
