# Product & AI Skills

Four Agent Skills for recurring product decisions: what to build, how much autonomy to give an agent, how to change an API safely, and how to evaluate an AI feature.

They are meant to make assumptions, missing evidence, and decision boundaries visible. Each skill is a self-contained package with documented evaluation evidence, not a prompt that claims to have the answer.

## Explore the skills

- [**Review a product decision**](skills/review-product-decision/SKILL.md) — Compare options, constraints and evidence before committing to an investment or direction.
- [**Assess agent autonomy**](skills/assess-agent-autonomy/SKILL.md) — Decide which actions an agent can take, what requires approval, and how to recover from failures.
- [**Review an API product change**](skills/review-api-product-change/SKILL.md) — Consider existing consumers, compatibility, migration paths and rollout.
- [**Evaluate an AI feature**](skills/evaluate-ai-feature/SKILL.md) — Define meaningful task-level evaluation and interpret evidence before release.

## An example

Suppose a team is deciding whether to build a custom reporting dashboard or start with a simpler export. A few requests have come from Sales, but the team has little evidence of how often the reports would be used.

That is a question for [`review-product-decision`](skills/review-product-decision/SKILL.md). The skill is designed to return a short, conditional Decision Brief: a recommendation, the material trade-off, what is known versus assumed, and the next check or decision that matters. This is an illustrative scenario, not a claimed test result.

## Try one

Read the relevant [skill instructions](skills/) and the [verified installation and compatibility evidence](docs/compatibility.md) before adding a package to your AI client. The documented tests cover specific package revisions and Codex CLI versions; they are not a promise of compatibility with every client.

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

All four packages were anonymously downloaded from immutable public commits, extracted as standalone packages, validated, and checked for positive and near-miss routing with the recorded Codex CLI versions. See the [compatibility record](docs/compatibility.md) and each package's evaluation evidence for exact revisions, hashes, controls, outputs, and limitations.

## License

Licensed under the [Apache License 2.0](LICENSE).
