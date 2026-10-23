# AI feature release scorecard

Use only for a versioned feature and evaluation record. Enter `Not run` for unexecuted cases and `TBD` for gates not accepted by an accountable owner. Synthetic examples are never observed results.

## Scope and provenance

- Feature / release candidate:
- Evaluated system version: model, prompt, retrieval, tools, policies, fallback
- Case-ledger and rubric versions:
- Evaluation date and environment:
- Evaluators / scorers and calibration evidence:
- Evidence locations:
- Target users, segments, and exclusions:
- Accountable evaluation owner:
- Release approver:

## Coverage

| Segment / case family | Planned | Executed | Missing or excluded | Representativeness limitation |
| --- | ---: | ---: | --- | --- |
| Typical |  |  |  |  |
| Edge |  |  |  |  |
| Negative / expected refusal |  |  |  |  |
| Ambiguity / out-of-distribution |  |  |  |  |
| Abuse / injection |  |  |  |  |
| Critical segment(s) |  |  |  |  |

## Quality, risk, and operations

| Gate | Segment | Accepted threshold | Observed result | Evidence state | Pass / fail / not run | Owner / action |
| --- | --- | --- | --- | --- | --- | --- |
| Task success / rubric |  |  |  | Observed / provided-unverified / not run |  |  |
| Critical failure rule |  |  |  |  |  |  |
| Human–judge agreement |  |  |  |  |  |  |
| Cost per task |  |  |  |  |  |  |
| Latency p50 / p95 / p99 as relevant |  |  |  |  |  |  |
| Fallback |  |  |  |  |  |  |

Report severe failures individually. Do not average a critical segment into the aggregate.

## Confidence and limitations

- Sample size and uncertainty method:
- Leakage / overlap check:
- Evaluator disagreement and adjudication:
- Missing segments or operational evidence:
- Configuration changes since the run:
- What this evidence does **not** establish:

## Release recommendation

- Status: `PLAN ONLY / NOT EVALUATED`, `INSUFFICIENT EVIDENCE`, `NO-GO / REMEDIATE`, or `CONDITIONAL GO`
- Scope of recommendation:
- Gates passed:
- Gates failed or not run:
- Approval still required:
- Smallest next action:
- Post-launch monitoring and stop signals:
- Re-evaluation triggers:
