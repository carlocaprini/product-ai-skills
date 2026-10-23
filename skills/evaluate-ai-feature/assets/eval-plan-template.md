# AI feature evaluation plan

Use this template for a reusable evaluation handoff. Remove irrelevant sections, keep unknowns as `TBD`, and distinguish proposed design from observed evidence.

## 1. Decision and feature boundary

- Feature / user task:
- Intended user outcome:
- Decision this evaluation informs:
- Evaluation mode: Plan / Evidence review
- Release scope and target segments:
- System boundary and version: model, prompt, retrieval, tools, policies, human review, fallback
- Accountable evaluation owner:
- Release approver:
- Material unknowns:

## 2. Outcome hypotheses

| Layer | Hypothesis | Signal | Baseline | Limitation |
| --- | --- | --- | --- | --- |
| User / business |  |  |  |  |
| Task / system quality |  |  |  |  |
| Risk / safety |  |  |  |  |
| Operations |  |  |  |  |

Delete layers that do not change this decision; explain material exclusions.

## 3. Versioned case ledger

| ID | User context / task | Scenario and segment | Input and system context | Expected behavior | Reference evidence | Severity | Pass/fail signal | Provenance | Split / version |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | Typical / edge / negative / ambiguity / OOD / abuse | Retrieved evidence, tool state, policy, or other context |  |  |  |  | Synthetic / authorized / public | Dev / held-out |

Document privacy, retention, access, de-identification, and deletion rules for any production-derived data.

## 4. Evaluation method

- Baseline and why it represents the product decision:
- Deterministic checks:
- Human reviewer qualifications, rubric, blinding, agreement, and adjudication:
- LLM judge model/prompt/rubric, calibration set, human agreement, and bias controls:
- Online metric or experiment design, authorization, attribution, and stopping policy:
- Leakage and representativeness controls:

## 5. Metrics and release gates

| Metric / failure rule | Segment | Threshold or stop gate | Critical? | Evidence source | Owner | Action on miss |
| --- | --- | --- | --- | --- | --- | --- |
|  |  | Accepted value or `TBD` | Yes / No |  |  |  |

Do not invent thresholds, sample sizes, significance, latency, or cost targets. Record who must accept each `TBD`.

## 6. Operational constraints and fallback

- Cost per completed task and budget:
- Latency distribution and target percentiles:
- Throughput / concurrency:
- Dependency and timeout behavior:
- Fallback trigger, behavior, owner, observability, and recovery:
- Data protection and retention limits:

## 7. Execution and audit record

- Case-ledger and rubric versions:
- Feature/model/prompt/retrieval/tool/policy versions:
- Environment and date:
- Sample and exclusions:
- Raw/auditable result location:
- Deviations, failed attempts, and limitations:

## 8. Decision and feedback loop

- Status: `PLAN ONLY / NOT EVALUATED`, `INSUFFICIENT EVIDENCE`, `NO-GO / REMEDIATE`, or `CONDITIONAL GO`
- Evidence supporting the status:
- Approval still required:
- Smallest next experiment or fix:
- Post-launch monitoring:
- Re-evaluation triggers:
