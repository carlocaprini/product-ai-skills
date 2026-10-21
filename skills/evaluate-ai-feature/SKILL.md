---
name: evaluate-ai-feature
description: Designs a release-readiness evaluation for an AI feature, covering success criteria, golden and negative cases, quality thresholds, cost, latency, fallback, and go/no-go evidence. Use when deciding whether an AI-powered feature is ready to ship.
---

# Evaluate AI Feature

Design an evaluation for a complete AI-enabled user task, or assess supplied results against predeclared release gates. Measure whether the feature works well enough for its intended users, not merely whether individual model responses sound plausible.

Separate user or business outcome, task and system quality, safety or consequential failure, and operational cost and latency. Address only the dimensions relevant to the feature, but never average away a severe failure in a critical segment.

This skill designs evaluations and interprets evidence. It does not run production experiments by default, certify safety or compliance, or grant release approval. Do not claim that a test ran, a result was measured, or a threshold was met unless the user supplies verifiable evidence or separately authorizes an actual execution.

## Activate for an AI feature evaluation

Use this skill when the user wants to:

- design representative evals for an AI-enabled feature or workflow;
- decide launch readiness from supplied measurements and accepted gates;
- compare an AI workflow with the current non-AI or prior-feature baseline;
- diagnose evaluation gaps, segment regressions, grader disagreement, cost, latency, fallback, or drift.

Do not activate for:

- choosing a foundation model from a public leaderboard without a feature and representative task context;
- defining an agent's action permissions, approvals, or autonomy boundary;
- reviewing an API contract change for consumer compatibility;
- generic product prioritization with no AI-feature evaluation question;
- treating a polished demo, anecdote, or synthetic example as launch evidence.

If the user asks to execute an eval, first separate evaluation design from the requested execution. Use only authorized tools, data, environments, and spend; preserve the user's approval boundaries and report planned versus executed work distinctly.

## Choose the evaluation mode

State the mode before giving a readiness status:

1. **Plan mode** — tests have not been run, or the user wants an eval design. Produce an evaluation plan and return `PLAN ONLY / NOT EVALUATED`.
2. **Evidence-review mode** — observed results exist. Check their provenance, version, coverage, scorer reliability, thresholds, owners, and limitations before making a conditional readiness recommendation.

Do not convert proposed cases, expected outcomes, fictional scorecards, or unverified summaries into observed evidence.

## Start with the minimum evidence

Minimum useful input is the feature or user task, intended outcome, and known failure consequences. Helpful context includes system boundary, target users and segments, representative examples, current baseline, launch scope, constraints, cost and latency targets, fallback, and accountable owners.

For a readiness assessment, also require:

- observed results tied to a dated feature configuration;
- accepted thresholds and critical stop gates;
- an accountable owner or approver.

If one missing input could materially change the design or verdict, ask for the **single highest-impact missing item**. Otherwise proceed with a provisional plan and explicit `TBD` fields. Never invent an operational target, sample size, statistical significance, or acceptable failure rate.

Label evidence consistently:

- **observed** — inspected result with source, sample, date, and system version;
- **provided / unverified** — reported by the requester or named source but not inspected;
- **proposed** — a test, threshold, or control awaiting owner agreement;
- **synthetic illustration** — fictional example that is not release evidence;
- **unknown / TBD** — a material gap.

## Load supporting material selectively

- Read [evaluation design](references/evaluation-design.md) when choosing case coverage, baselines, scorers, metrics, thresholds, or human calibration.
- Read [edge and negative cases](references/edge-and-negative-cases.md) for high-consequence domains, segment regressions, prompt injection, privacy, unsafe success criteria, grader disagreement, drift, or fallback failure.
- Use the [eval plan template](assets/eval-plan-template.md) only when the user asks for a reusable handoff or the evaluation spans multiple segments, scorer types, owners, and release gates.
- Use the [release scorecard template](assets/release-scorecard-template.md) only for evidence-review mode or when the user asks how future results should be recorded. Leave unmeasured cells `Not run`; never fill them with illustrative numbers.

## Evaluation workflow

1. **Frame the feature and decision.** Record the user job, intended outcome, usage scenario, target segments, release scope, system boundary, owner, and the decision the evidence must support. Include prompt, model, retrieval, tools, policies, and human review only where they are part of the feature.

2. **Map outcomes and consequential failures.** Define correct and useful behavior, then distinguish cosmetic errors from omissions, unsupported claims, privacy leaks, unsafe actions, poor escalation, and other severe failures. Identify critical segments and realistic worst cases before choosing aggregate metrics.

3. **Build a representative, versioned case ledger.** Include typical, edge, negative, ambiguous, out-of-distribution, and abuse or injection cases as relevant. Each case needs an ID, user context, segment, expected behavior, reference evidence, severity, pass/fail signal, and provenance. Keep tuning examples separate from held-out evaluation cases. Use authorized privacy-safe data or clearly labeled synthetic fixtures.

4. **Choose the baseline and evaluation method.** Compare with the current non-AI workflow, prior feature, or no-feature condition when meaningful. Use deterministic checks for objective properties, calibrated human review for judgment, LLM judges only with rubric exemplars and human-agreement evidence, and online metrics only when an authorized experiment and attribution design exist.

5. **Predeclare metrics and gates.** Define per-segment quality, critical failure tolerance, human-review rules, cost per task, latency distribution where tails matter, throughput, fallback behavior, and owner-approved release gates. Prefer task-level and pairwise criteria over vague impressions. Do not optimize one metric while ignoring a severe failure mode.

6. **Inspect execution evidence.** In evidence-review mode, distinguish planned from executed cases and record sample size, date, feature/model/prompt/retrieval/tool versions, rubric and scorer versions, missing segments, leakage, disagreement, uncertainty, and operational conditions. A later material configuration change invalidates the earlier result for that configuration until re-evaluated.

7. **Make a calibrated recommendation.** Use exactly one status:
   - `PLAN ONLY / NOT EVALUATED` — no valid execution evidence exists;
   - `INSUFFICIENT EVIDENCE` — required cases, thresholds, provenance, fallback, or ownership are missing;
   - `NO-GO / REMEDIATE` — observed evidence demonstrates a critical failure or misses an accepted gate;
   - `CONDITIONAL GO` — verifiable evidence meets documented gates for the stated scope and named approvers still own release authorization.

   Never issue an unconditional `GO`, safety certification, or compliance approval.

8. **Close the feedback loop.** Recommend the smallest next experiment or fix, post-launch monitoring for quality drift, correction or complaint, fallback, cost, and tail latency, plus re-evaluation triggers for model, prompt, retrieval, tool, policy, data, or segment changes.

## Output contract

Lead with the mode, status, scope, and evidence confidence. Then provide only what the mode supports:

1. **Objective and boundary** — user task, outcome, system/version, segments, decision owner, and material unknowns.
2. **Case and scoring design** — representative ledger summary, baseline, evaluator method, rubric, and severe-failure rules.
3. **Gates and operational constraints** — per-segment thresholds, cost/latency/fallback budgets, owner, and unresolved `TBD`s.
4. **Evidence or gaps** — observed results by segment when supplied; otherwise `Not run`, never fictional measurements.
5. **Recommendation and next action** — one allowed status, approval still needed, smallest useful follow-up, monitoring, and re-evaluation triggers.

For a narrow planning question, keep the response compact: status, one case table, proposed gates, and next action. Use the full templates only under their loading rules. More detail is warranted when failure severity, multiple segments, scorer disagreement, or operational trade-offs change the release decision.

## Final check

- [ ] The complete user task, not isolated response style, is being evaluated.
- [ ] Typical, edge, negative, ambiguity, and critical-segment cases are represented where relevant.
- [ ] Tuning and evaluation data are separated; provenance and feature version are recorded.
- [ ] Baseline, rubric, scorer reliability, per-segment gates, cost, latency, and fallback are explicit or `TBD`.
- [ ] Aggregate results do not hide a severe segment failure.
- [ ] Planned, synthetic, provided, and observed evidence remain distinct.
- [ ] The status follows the four allowed outcomes and does not overstate release authority.
- [ ] The next experiment, monitoring, and re-evaluation triggers are actionable.
