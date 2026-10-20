# Contributing

Contributions must be reviewable, public-safe, and limited to material that can be distributed in this repository.

## Before opening a pull request

- Use an issue to describe the problem or contribution before making a substantial change.
- Keep one independently reviewable concern per pull request.
- Use only original, licensed, or clearly attributable public material.
- Use synthetic examples. Do not include customer information, private project details, real transcripts, credentials, local filesystem paths, or internal planning material.
- Do not claim installation, compatibility, evaluation success, or release status without reproducible evidence in the same change.

## Skill package contract

A package lives at `skills/<skill-name>/` and must be usable without another package or repository.

- `SKILL.md` is required.
- `references/` and `assets/` are optional and exist only when used.
- `tests/evals.md` records the public test plan and sanitized observations; it is not runtime instruction content.
- Runtime references stay inside the package and use relative paths.
- Do not add symlinks, executables, generated archives, vendored dependencies, or empty directories.
- Do not introduce a router, supervisor, command system, or repository-wide runtime dependency through an individual package.

See [docs/authoring.md](docs/authoring.md) for the portable format and [docs/quality-and-evals.md](docs/quality-and-evals.md) for evidence requirements.

## Local checks

Run:

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py .
python -m unittest discover -s tests -v
for skill in skills/*; do if [ -d "$skill" ]; then skills-ref validate "$skill"; fi; done
```

Both commands must pass before review. They are deterministic and make no network or paid-provider calls.

## Pull request checklist

- The diff contains only public material required by the change.
- New or changed links are real, safe, and attributable.
- Any example is synthetic and clearly presented as an example.
- Any observed evaluation result is distinguished from an expected result.
- Compatibility and installation statements identify the tested client, version, environment, date, and limitations.
- The validation commands pass on the pull request commit.
