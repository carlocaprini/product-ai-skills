# Evaluation design

Use this reference to turn an AI-feature decision into representative cases, reliable scoring, and explicit gates. It is not a substitute for domain, safety, privacy, legal, or release-owner approval.

## Start from the user task

Evaluate the end-to-end feature as users experience it. A useful decomposition is:

| Layer | Question | Example signal |
| --- | --- | --- |
| User / business outcome | Did the feature help the intended user complete the job? | task completion, correction burden, escalation, adoption with appropriate causal limits |
| Task / system quality | Was the result correct, relevant, grounded, complete, and usable? | rubric score, exact check, grounded citation, omission rate |
| Risk / safety | Did any unacceptable failure occur? | privacy leak, unsafe action, unsupported claim, missed escalation |
| Operations | Can the feature deliver within accepted constraints? | cost per task, p50/p95/p99 latency as relevant, throughput, fallback success |

Do not force every layer into every evaluation. Include a layer when it changes the product decision; state when it is out of scope.

## Versioned case ledger

Keep cases in a versioned ledger. At minimum, record:

| Field | Purpose |
| --- | --- |
| `id` | Stable case identity. |
| user context and task | What the user is trying to achieve. |
| scenario / segment | Typical, critical, edge, ambiguity, out-of-distribution, or abuse case; target user segment. |
| input and system context | Privacy-safe input plus any retrieved evidence, tool state, or policy that affects expected behavior. |
| expected behavior | Observable success, refusal, clarification, escalation, or fallback. |
| reference evidence | Source for the expected behavior, or `none` when the case tests an interaction property. |
| severity | Consequence if the feature fails this case. |
| pass/fail signal | Deterministic rule or rubric criterion. |
| provenance | Synthetic, authorized production-derived, public, or other permitted source. |
| split and version | Tuning/development versus held-out evaluation; ledger revision. |

Representativeness requires more than a random sample. Cover material user segments, common task frequency, consequential rare cases, language or format differences, missing context, ambiguity, and realistic adversarial input where relevant. Weighting may reflect product exposure, but a critical stop gate should not disappear into a weighted average.

Keep tuning examples out of the held-out set. If prompts, retrieval, policies, or rubrics were adjusted using a case, mark it as development data and replace or supplement it with independent cases for the release evaluation.

## Baselines

Choose a baseline that represents the product decision:

- current human or non-AI workflow;
- current production feature;
- prior model or feature configuration;
- no-feature condition when that is the real alternative.

A public benchmark can provide context but rarely represents the complete feature, users, retrieval, tools, policies, failure costs, or operational constraints. Do not use it as the sole launch gate.

## Evaluation methods

### Deterministic checks

Use exact checks for properties such as schema validity, required fields, citation presence, tool-call constraints, forbidden data, or reproducible calculations. A deterministic check can establish only the property it measures.

### Human evaluation

Use domain-qualified reviewers where correctness, harm, tone, or task usefulness requires judgment. Define a rubric with positive and negative exemplars, blinded comparison when feasible, adjudication, and an agreement measure appropriate to the decision. Record reviewer qualifications and conflicts.

### LLM-as-judge

An LLM judge is a measurement instrument, not ground truth. Before relying on it:

1. define criteria and anchored examples;
2. compare the judge with qualified human labels on a representative calibration set;
3. inspect disagreement by segment and severity;
4. control position, verbosity, self-preference, and reference-answer leakage where relevant;
5. version the judge model, prompt, rubric, and sampling settings.

If human and judge results conflict materially, do not average them into false certainty. Investigate rubric ambiguity, representativeness, and systematic judge bias, and keep the readiness status constrained until resolved.

### Online and business metrics

Use online metrics only with an authorized experiment or rollout, clear exposure, attribution limits, guardrails, and stopping policy. Engagement alone is not proof of correctness or user benefit. Low traffic may make a quantitative comparison inconclusive; prefer targeted qualitative research rather than inventing significance.

## Metrics and release gates

Predeclare metrics before inspecting final results. Choose metrics connected to the user task and failure consequences, such as:

- exact or rubric-based task success;
- groundedness, completeness, correction effort, refusal, or escalation quality;
- per-segment pass rate and worst-segment behavior;
- count or rate of critical failures;
- judge-human agreement and adjudication rate;
- cost per completed task;
- latency distribution, timeouts, throughput, and fallback success.

Record for each gate: metric, segment, threshold, criticality, evidence source, owner, and action on miss. Thresholds come from product risk, stakeholder commitments, policy, and baseline performance. When no threshold has been accepted, mark it `TBD` and return `INSUFFICIENT EVIDENCE` for a release verdict.

Do not invent sample sizes or statistical significance. When uncertainty matters, identify the analysis method and decision rule before the run, then report confidence intervals or other uncertainty measures only from actual data.

## Execution record

Tie results to the exact evaluated system:

- feature and release candidate version;
- model/provider version where known;
- prompt, policy, retrieval index/data snapshot, tools, and fallback versions;
- case-ledger and rubric versions;
- date, environment, sample size, evaluator identity/type, and exclusions;
- raw or auditable result location, with privacy-safe access;
- deviations, failed runs, disagreement, and limitations.

Do not silently replace failed attempts or remove inconvenient segments. A material change to the model, prompt, retrieval, tools, policies, data, or target population is a re-evaluation trigger.

## Decision interpretation

- No executed cases: `PLAN ONLY / NOT EVALUATED`.
- Missing accepted gates, critical segments, provenance, fallback, or owner: `INSUFFICIENT EVIDENCE`.
- A critical stop condition or accepted gate fails: `NO-GO / REMEDIATE`.
- All relevant accepted gates pass on verifiable evidence for the stated version and scope: `CONDITIONAL GO`, pending the named release approver.

A good aggregate score never cancels a catastrophic failure in a critical segment. Scope the recommendation to the evaluated users, configuration, and operating envelope.
