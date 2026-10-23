# Product & AI Skills

Focused Agent Skills for better product decisions.

## Current status

This repository contains four Agent Skill packages, public authoring and evaluation guidance, and deterministic validation tooling:

- [`review-product-decision`](skills/review-product-decision/SKILL.md) reviews an unresolved consequential product choice and produces a concise, conditional Decision Brief.
- [`assess-agent-autonomy`](skills/assess-agent-autonomy/SKILL.md) recommends action-level autonomy, approval, enforcement, recovery, and rollout boundaries for AI agents.
- [`review-api-product-change`](skills/review-api-product-change/SKILL.md) reviews an existing API change for per-consumer compatibility, migration, developer experience, and staged rollout.
- [`evaluate-ai-feature`](skills/evaluate-ai-feature/SKILL.md) designs task-level AI feature evaluations and interprets versioned evidence into calibrated release-readiness recommendations.

Observed synthetic behavioral evidence is recorded for all four packages. Public-source standalone extraction and scoped Codex CLI checks are verified for `assess-agent-autonomy` at immutable commit `33a67ee942f02780981c8d526f4251ccc1967078`, `review-api-product-change` at `585a7fc59bbd21671ceb67be086938a6010c6df2`, and `evaluate-ai-feature` at `1693662a2f3bac4fad57c8b5d901f7e894946253`. Final-candidate public-origin verification for `review-product-decision` remains pending. These are package- and client-version-scoped observations, not releases or cross-client compatibility claims.

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
for skill in skills/*; do if [ -d "$skill" ]; then skills-ref validate "$skill"; fi; done
```

The repository validator checks public safety, valid typed `SKILL.md` YAML frontmatter, package boundaries, inline and reference-style local Markdown links, and common secret or local-path leaks. CI also runs the version-pinned Agent Skills reference validator and scans every commit introduced by a pull request so that adding and later deleting unsafe content does not bypass the public-safety gate. Automated checks complement, but do not replace, human review of everything intended to become public.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), [the authoring contract](docs/authoring.md), and [the quality and evaluation policy](docs/quality-and-evals.md) before proposing a change.

## Compatibility and installation

The `assess-agent-autonomy`, `review-api-product-change`, and `evaluate-ai-feature` packages were anonymously downloaded from immutable public commits, extracted as standalone packages, validated, and checked for positive and near-miss routing with the recorded Codex CLI versions. See the [compatibility record](docs/compatibility.md) and each package's evaluation evidence for exact revisions, hashes, controls, outputs, and limitations.

## License

Licensed under the [Apache License 2.0](LICENSE).
