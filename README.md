# Product & AI Skills

Focused Agent Skills for better product decisions.

## Current status

This repository contains one Agent Skill package, public authoring and evaluation guidance, and deterministic validation tooling:

- [`review-product-decision`](skills/review-product-decision/SKILL.md) reviews an unresolved consequential product choice and produces a concise, conditional Decision Brief.

No installation command, client compatibility claim, observed behavioral evaluation result, or release is currently published.

The absence of those claims is intentional: they will appear only when the corresponding public artifacts have been reviewed and verified.

## Repository boundary

This repository is the canonical home for distributable Product & AI Agent Skill packages and their public quality evidence. It does not contain a website application, private workflows, personal material, customer data, or credentials.

When packages are present, each one is self-contained under `skills/<skill-name>/`:

```text
skills/<skill-name>/
├── SKILL.md
├── references/   # only when the skill needs supporting instructions
├── assets/       # only when the skill produces or reuses files
└── tests/
    └── evals.md  # public test plan and observed, sanitized evidence
```

Empty package directories and placeholder skills are not kept in the repository.

## Validation

The checks use a version-pinned YAML parser and do not call an AI provider or external service:

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py .
python -m unittest discover -s tests -v
skills-ref validate skills/review-product-decision
```

The repository validator checks public safety, valid typed `SKILL.md` YAML frontmatter, package boundaries, inline and reference-style local Markdown links, and common secret or local-path leaks. CI also runs the version-pinned Agent Skills reference validator and scans every commit introduced by a pull request so that adding and later deleting unsafe content does not bypass the public-safety gate. Automated checks complement, but do not replace, human review of everything intended to become public.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), [the authoring contract](docs/authoring.md), and [the quality and evaluation policy](docs/quality-and-evals.md) before proposing a change.

## Compatibility and installation

No client or installation path is currently declared as verified. The evidence required before adding such a claim is documented in [docs/compatibility.md](docs/compatibility.md).

## License

No public license has been granted yet. Until a `LICENSE` file is added, the repository contents remain subject to the default rights retained by the copyright holder.
