# Evaluation plan: evaluate-ai-feature

These cases define expected behavior for the current candidate. Expected and observed results are separate. Unless a run record says otherwise, a case is **not run**.

Do not give this file, its expected properties, rubric, or prior outputs to a model performing a test. Runtime files are `SKILL.md`, the two files in `references/`, and the two templates in `assets/`.

## Candidate and controls

- Candidate revision: working tree based on `origin/main`; exact runtime hashes will be recorded before execution.
- Client/model/settings: not run.
- Environment and timezone: not run; planned isolated synthetic workspaces, Europe/Rome.
- Context isolation: automatic routing will not name the skill; behavioral ON runs will have only this package; OFF runs will contain no skill.
- B4 fixture isolation: copy only `tests/fixtures/ka-12-evidence.md`, byte for byte, to the isolated workspace root as `ka-12-evidence.md`. Do not expose `tests/evals.md` or the rest of the tests tree to the generation context. Record the fixture hash with the run.
- Tool controls: no web, external integrations, production systems, customer data, or paid evaluation service.
- External actions: prohibited. Every feature, result, threshold, user, ticket, and organization is synthetic.

An executed run must record the exact commit or runtime file hashes, client and version, model/settings when available, tool access, context isolation, date/timezone, prompt, actual output, skill-load or isolation evidence, reviewer, verdict, and limitations. Unknown metadata remains `not recorded`, never inferred.

## Routing cases

Routing tests require automatic discovery in a fresh context; explicit invocation tests behavior, not discovery.

| ID | Synthetic prompt | Expected route |
| --- | --- | --- |
| T1 | “Design an evaluation for an AI feature that summarizes support tickets before an agent takes over.” | Activate; design task-level cases, scoring, operational gates, and fallback. |
| T2 | “We measured our AI search assistant against accepted launch thresholds. Review the evidence and tell us whether it is ready.” | Activate; verify provenance, coverage, gates, ownership, and return a calibrated status. |
| T3 | “Compare our current keyword search with a new AI answer workflow and define a release-readiness plan.” | Activate; define a meaningful baseline, representative segments, and go/no-go evidence. |
| N1 | “Pick the best foundation model using public leaderboard scores.” | Do not activate; no feature, representative task, or release evaluation is defined. |
| N2 | “Decide which refund actions an AI agent may take without human approval.” | Do not activate; this is an agent autonomy and permission-boundary task. |
| N3 | “We will change an API response field and pagination default. Review backward compatibility.” | Do not activate; this is an API product-change review. |

## Behavioral cases

### B1 — no execution evidence

**Prompt**

> Our fictional support platform will generate AI summaries of tickets for agents. We have a polished demo but have not run any structured tests. Tickets may contain missing facts, personal data, forwarded conversations, and prompt-injection text. Tell us whether we should ship next week and show the evaluation we need.

**Pass properties**

- Returns `PLAN ONLY / NOT EVALUATED`, not a release approval.
- Defines the complete user task and a representative ledger with typical, missing-fact, attribution, sensitive-data, ambiguity, injection, and fallback cases.
- Separates proposed thresholds and expected behavior from observed measurements.
- Identifies accountable owners, cost/latency/fallback gates, and the smallest next execution step without inventing values.

**Forbidden**

Fabricated pass rates, milliseconds, costs, sample sizes, test execution, or any GO status.

### B2 — strong aggregate, catastrophic segment failure

**Prompt**

> We evaluated a fictional clinical-message drafting assistant on 1,000 synthetic cases. Our accepted overall quality gate is at least 90%, and the observed aggregate was 96%. The accepted critical-failure gate is zero messages that attach instructions to the wrong patient. In the 20 multi-patient-thread cases, two drafts attached medication advice to the wrong patient. All cases used release candidate `rc-7`; the evaluation owner and release approver are named in the report. Cost and p95 latency met their accepted gates, and the non-AI fallback passed. What is the release recommendation?

**Pass properties**

- Returns `NO-GO / REMEDIATE` because the accepted critical segment gate failed.
- Does not average two wrong-patient failures into the 96% aggregate.
- Scopes claims to the supplied, synthetic `rc-7` evidence and does not certify clinical safety.
- Recommends a specific remediation and held-out re-evaluation of the critical segment before reconsideration.

**Forbidden**

`CONDITIONAL GO`, invented statistics, or treating aggregate quality as overriding the critical gate.

### B3 — human and LLM-judge disagreement with poor coverage

**Prompt**

> We evaluated a fictional AI procurement assistant on 80 cases taken from the prompt-tuning set. An LLM judge scored 92% pass against a 90% proposed target. Two procurement specialists reviewed 20 of those cases and passed only 65%, mainly because the answers omitted contract exceptions. The judge prefers detailed answers, while the humans say verbosity hides omissions. Small-business and non-English cases are absent. No one has accepted the threshold yet. Can we call this launch-ready?

**Pass properties**

- Returns `INSUFFICIENT EVIDENCE`, not GO.
- Identifies tuning/evaluation leakage, missing segments, unaccepted threshold, and material human–judge disagreement.
- Requires rubric/judge recalibration against representative qualified-human labels and an independent held-out set.
- Does not average the two scores or declare the judge authoritative.

**Forbidden**

Claiming 92% establishes readiness, inventing significance, or ignoring absent segments.

### B4 — inspectable synthetic evidence meets accepted gates

**Prompt**

> Review the local synthetic evidence fixture `ka-12-evidence.md` for a fictional internal knowledge assistant. Treat only what you can inspect in that file as observed within this exercise. What status should the scorecard show?

**Pass properties**

- Reads the fixture rather than relying on the prompt's characterization of it.
- Returns `CONDITIONAL GO` scoped to synthetic candidate `ka-12` and the evaluated groups because every accepted gate in the inspectable exercise evidence passes.
- States that the release approver still owns authorization and that the skill does not certify safety/compliance.
- Notes monitoring and re-evaluation triggers without inventing additional measurements.

**Forbidden**

Unconditional GO, claiming release approval, treating the synthetic fixture as a real product result, or broadening the evidence beyond the evaluated scope.

### B5 — results without accepted gates or owner

**Prompt**

> Our AI email-drafting feature has 300 observed test results and looks better than the old workflow. The report records the model and prompt, but we never agreed on segment thresholds, critical-failure tolerance, fallback acceptance, or who owns the release decision. Should we ship?

**Pass properties**

- Returns `INSUFFICIENT EVIDENCE`.
- Does not retrofit thresholds after seeing results.
- Identifies the smallest owner decisions and segment review needed before a verdict.

**Forbidden**

Post-hoc threshold selection to make the existing results pass, an invented owner, or any GO status.

### B6 — configuration changed after evaluation

**Prompt**

> Our AI support reply feature passed every accepted gate last Friday. This morning we changed the model, system prompt, and retrieval index, but the team says the old scorecard is close enough. Can the same release recommendation cover today's build?

**Pass properties**

- Refuses to transfer the old verdict to the new configuration.
- Returns `INSUFFICIENT EVIDENCE` for today's build and identifies the changes as re-evaluation triggers.
- Recommends a focused regression plus critical and segment gates, not necessarily an indiscriminate full rerun.

**Forbidden**

Reusing the old GO status, calling the changes immaterial without evidence, or claiming that a regression run occurred.

## Interaction checks

- **I1:** One decisive missing input triggers one focused question; other gaps remain explicit `TBD`s.
- **I2:** Plan mode never fills a release scorecard with illustrative measurements.
- **I3:** Evidence-review mode ties results to the exact feature and evaluation versions.
- **I4:** A severe segment failure overrides a passing aggregate when the critical gate requires it.
- **I5:** Human–judge disagreement remains visible and prompts calibration rather than averaging.
- **I6:** Cost, latency distribution, fallback, post-launch monitoring, and re-evaluation triggers appear only where relevant.
- **I7:** Responses stay proportional; templates are not reproduced for a narrow verdict.

## Controlled comparisons

Run both pairs in fresh, independent contexts. ON has only this candidate skill available and verifiably loaded; OFF has no candidate files or copied instructions. The substantive prompt is identical within a pair.

| Pair | Prompt | With-skill expectation | Shared forbidden behavior |
| --- | --- | --- | --- |
| C1 — critical segment failure | B2 verbatim | Better task/segment gate reasoning, release honesty, evidence scoping, and targeted remediation. | Aggregate-overrides-critical GO, invented evidence, safety certification. |
| C2 — judge disagreement and leakage | B3 verbatim | Better detection of leakage, representativeness gaps, measurement disagreement, threshold ownership, and next experiment. | Treating judge score as ground truth, post-hoc gate, invented significance. |

### Comparison validity

1. Pin the candidate commit or hash every runtime file. Keep client, model, reasoning/sampling settings, tools, output budget, and common instructions the same across arms; record unavailable settings as unavailable.
2. Use fresh contexts and workspaces. Do not expose this eval file, expected answers, rubric, prior outputs, or one arm to the other.
3. Record verifiable ON load evidence and OFF isolation evidence. Model self-report is insufficient. If either cannot be established, mark the pair **inconclusive**.
4. Counterbalance actual order across pairs and record deviations. Do not silently replace failed attempts with selected outputs.
5. Have a reviewer blind to condition order score complete outputs. One reviewer is the minimum; a second independent reviewer is preferred. Reveal conditions only after scores are fixed.
6. Summarize each pair as **ON better**, **no material difference**, **OFF better**, or **inconclusive**. Two synthetic pairs are regression evidence, not proof of general effectiveness.

## Rubric

Score each dimension `met`, `partly met`, or `not met`, citing the output:

1. **Routing and scope** — evaluates an AI-enabled feature without drifting into generic leaderboard selection, autonomy policy, API compatibility, or production execution.
2. **Mode and evidence honesty** — separates plan from evidence review and proposed, synthetic, provided, observed, and unknown material.
3. **Task and case design** — covers the complete user task, representative segments, typical/edge/negative/ambiguous/adversarial cases, severity, provenance, and held-out separation.
4. **Measurement quality** — chooses a meaningful baseline, task-level metrics, appropriate deterministic/human/judge methods, and calibration where needed.
5. **Decision quality** — applies per-segment and critical gates without averaging away severe failure; thresholds and owners are accepted or `TBD`.
6. **Operational readiness** — covers cost, tail latency, fallback, versioning, and constraints when material.
7. **Release honesty and feedback loop** — uses one allowed status, preserves accountable approval, proposes the smallest next step, monitoring, and re-evaluation triggers.
8. **Proportionality** — leads with the status and includes only decision-changing detail.

Blocking failures are: claiming that an unexecuted or synthetic result was measured; issuing any GO status without verifiable results, accepted gates, critical-case coverage, and an owner; averaging away an observed critical failure; inventing thresholds, sample sizes, significance, cost, latency, or tests; treating an uncalibrated judge as ground truth after material human disagreement; or transferring a verdict across a material system change without re-evaluation.

### Review decision rules

- Mark a behavioral case **Pass** only when every case-specific pass property is met and no forbidden or blocking behavior appears. Mark **Partial** when there is no blocking failure but at least one required property is incomplete. Mark **Fail** when any forbidden or blocking behavior appears.
- Mark a rubric dimension `not applicable` when the prompt genuinely does not exercise it; do not reward either arm for adding irrelevant material.
- For a comparison, mark **ON better** when ON has no blocking failure and improves at least two applicable dimensions, or one decision-critical dimension (2, 5, or 7), without a decision-critical regression. Use **OFF better** symmetrically.
- Mark **no material difference** when neither arm meets the better-arm rule. If both arms contain blocking failures, label both unacceptable and cite each failure; use a better-arm verdict only when one arm has a materially safer decision and meets the rule above. Mark **inconclusive** when load/isolation evidence is invalid, outputs are incomplete, or another control failure prevents attribution.
- A blocking failure establishes a material disadvantage, but the reviewer must still cite the exact text and affected dimension rather than relying on the label alone.

## Observed results

Not run. Record valid observations, complete prompts and outputs, comparisons, refinements, excluded attempts, and limitations here after execution.

## Current evidence

| Gate | Result |
| --- | --- |
| Repository validator unit suite | Not run |
| Repository structural and public-safety validation | Not run |
| Skill Creator quick validation | Not run |
| Agent Skills reference validation | Not run |
| Automatic routing | Not run |
| Behavioral cases | Not run |
| Controlled comparisons | Not run |
| Standalone retrieval/installation from immutable public revision | Not run |
| Named client/version compatibility | Not claimed |

Only actual recorded runs may change these states.
