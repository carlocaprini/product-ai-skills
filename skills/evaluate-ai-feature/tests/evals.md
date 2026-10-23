# Evaluation plan: evaluate-ai-feature

These cases define expected behavior for the current candidate. Expected and observed results are separate. Unless a run record says otherwise, a case is **not run**.

Do not give this file, its expected properties, rubric, or prior outputs to a model performing a test. Runtime files are `SKILL.md`, the two files in `references/`, and the two templates in `assets/`.

## Candidate and controls

- Final candidate revision: `44d905d6b0530280cb8755e5d0c27d5d3668f623`.
- Final runtime-manifest SHA-256: `46820435b06495bfd584c4c5e0de247a86a67484d2ed3781d4692e3ed88dd460`.
- Final runtime files: `SKILL.md` `4735ed229139aeabd856b01c9e9182e88613b08e00cf1383b3ebf9d7156a195e`; `references/evaluation-design.md` `652b4e1149c9c5b7960e4d4d0587ab253dc7ea0e564c1f57bc55ba332612ac93`; `references/edge-and-negative-cases.md` `75cec08790ec23fde529557688f6af39859a7a5161e2d6d6c0f313d69cf5b663`; `assets/eval-plan-template.md` `5c0bfcb6ca1a580a4951ae4785fa2287933c3d2018cc4a1964993fb5ec9688fa`; `assets/release-scorecard-template.md` `482484f5c32706d16d6c3fff79a3435988a13b730fa45288b42b1b6d9055d5a6`.
- Client/model/settings: Codex CLI `0.163.0-alpha.10.2`, `gpt-6.1-sol`, high reasoning, read-only sandbox, ephemeral sessions, user configuration ignored, plugins/browser/computer-use/multi-agent features disabled, and `web_search="disabled"`.
- Environment and timezone: isolated temporary workspaces on macOS; 2026-10-21, Europe/Rome. Exact start times and sampling parameters beyond high reasoning were not retained.
- Context isolation: automatic routing never named the skill; behavioral ON runs had only this candidate's five runtime files and used explicit invocation; OFF runs had no candidate files or copied instructions.
- B4 fixture isolation: copy only `tests/fixtures/ka-12-evidence.md`, byte for byte, to the isolated workspace root as `ka-12-evidence.md`. Do not expose `tests/evals.md` or the rest of the tests tree to the generation context. Record the fixture hash with the run.
- B4 fixture SHA-256: `7c472fe006120c983ce578cd3b65dc24bf94def7653a2252fcc2647ecc940302`.
- Tool controls: no valid trace contained a web, browser, app, MCP, or external-integration call. No production systems, customer data, or paid evaluation service beyond the authorized model sessions were used.
- Review: one independent same-model behavioral reviewer and two fresh same-model blind comparison scorers. The repository owner explicitly authorized sending the unpublished runtime package and synthetic prompts/fixture to the Codex model service.
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
- Recommends a scope-proportionate re-evaluation that covers the changed components plus critical and representative segment gates; a full rerun is justified only when the combined changes can affect the complete task or evidence boundary.

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

### Candidate lineage and targeted regression

The valid routing regression used candidate `2f35c5f` after the discovery-description correction. The description is byte-identical in the final candidate. B1 and B3–B6 were last generated on `721625d` with runtime manifest `c503e968f570fd2bc971719e969eb4a2ae2efa233ecbf81dd89df1e854e67afe`. The final runtime change in `44d905d` adds only the independent-held-out requirement to the `NO-GO / REMEDIATE` branch; B2 was rerun on that exact final candidate. This targeted lineage is recorded instead of claiming that every unaffected case was regenerated after every one-line refinement.

### Observed summary

| Dimension | Result |
| --- | ---: |
| Automatic routing | **6/6** — sensitivity 3/3, specificity 3/3 |
| Behavioral review | **6/6 pass** after targeted B4, B6, and B2 refinements |
| Blocking failures in final behavioral outputs | **0** |
| C1 blind preference | **no material difference / no material difference** |
| C2 blind preference | **ON better / ON better** |
| C1 output length | ON 137 words / OFF 52 — **2.63×** |
| C2 output length | ON 363 words / OFF 155 — **2.34×** |

C1 shows that an ordinary answer can already enforce a clearly supplied zero-critical-failure gate; the skill adds provenance, independent held-out critical-segment retesting, and accountability, but neither scorer found a material decision advantage under the predeclared rule. C2 is the stronger differentiator: both scorers preferred the skill condition for held-out separation, scorer calibration, accountable segment/severity gates, operational gaps, and the feedback loop.

### Automatic-routing observations

Command traces, not model self-report, established whether `SKILL.md` was read. The final routing regression used fresh contexts and no explicit skill invocation.

| ID | Expected load | Observed read | Result | Observed behavior |
| --- | --- | --- | --- | --- |
| T1 | yes | yes | **Pass** | Returned `PLAN ONLY / NOT EVALUATED` and a ticket-summary evaluation plan. |
| T2 | yes | yes | **Pass** | Returned `INSUFFICIENT EVIDENCE` and requested the decisive results, thresholds, version, and owner. |
| T3 | yes | yes | **Pass** | Designed a keyword-search versus AI-answer task-level baseline and release plan. |
| N1 | no | no | **Pass** | Requested leaderboard inputs without loading the feature-readiness skill. |
| N2 | no | no | **Pass** | Kept the answer on missing refund authority and human approval. |
| N3 | no | no | **Pass** | Kept the answer on API compatibility and migration evidence. |

Routing-output SHA-256 values, in T1–T3/N1–N3 order: `fa510706ed0eb882d63543c38664bdf681237263bc66a07b0a15c929b5e92a5d`, `006bfb5778de47982bd41a6ec2d69648ccc8ef952d61700dfc0a1f2a8184b7e2`, `81e7317c3d3b40a51734dee7cde3f5b36adb0e5b98f5bb5aad950ad490b73ed6`, `a4c342634c5062dc0a01beedf25677e6b0eea4589961c9e72890298357218178`, `8d09634af7770ffb0c7531aae7dee0e665ee601b33f7df33c157f799cd71c5f7`, and `c534a92aaec0789f536aa135387396c98fda5dbfb0a772d267bf2e69c4e969d7`.

### Behavioral observations

The independent reviewer received the expected/forbidden properties and complete outputs, but not the runtime skill or generation traces.

| Case | Words | Verdict | Output SHA-256 | Observed decisive behavior |
| --- | ---: | --- | --- | --- |
| B1 | 872 | **Pass** | `57a0e6835b02486759fa57d52d0d8e5491d944330074d00de7dc97b89be13dd6` | `PLAN ONLY / NOT EVALUATED`; representative ledger, proposed gates, owners and operational/fallback evidence remain TBD/Not run. |
| B2 | 137 | **Pass after correction** | `81406ee6269893b9d39cd2b65a9780ab215c34ea95adeb4b38284a647c3b3a33` | `NO-GO / REMEDIATE`; critical segment overrides 96% aggregate; independent held-out multi-patient cases are required after remediation. |
| B3 | 363 | **Pass** | `ca46eaed4ddf73e5f2e4bd7bddd38326bb826da16ad42f4b5990393e3d174a83` | `INSUFFICIENT EVIDENCE`; exposes tuning leakage, judge-human mismatch, missing segments and unaccepted gates without averaging scores. |
| B4 | 138 | **Pass after correction** | `2f072acabc8303cfb1baaeff19f4cd7f227898093b06d7805fd01cfb390d6c47` | Reads the isolated fixture; scopes `CONDITIONAL GO` to synthetic `ka-12`; preserves release authority and denies safety/compliance certification. |
| B5 | 263 | **Pass** | `c713dcc33a69bd53f1a61ea656094bbe35745f0c293c1a3f90a3690aad98755c` | `INSUFFICIENT EVIDENCE`; refuses post-hoc thresholds and identifies owner, segment, fallback, cost and latency gaps. |
| B6 | 193 | **Pass after correction** | `2ca6c2c0637a06b6d1014ace26d7838a202b080176b1f3af9bf2d9d68a715e98` | Refuses verdict transfer; justifies a full rerun because model, prompt and retrieval changes can affect the complete task, with critical/segment and operational gates retained. |

No final output contained a forbidden or blocking behavior. B1's length reflects a requested full evaluation plan; B2 and B4 remained compact release decisions. B5 ends with one focused owner question only after supplying a provisional assessment.

### Controlled comparisons

The substantive prompt was identical within each pair. ON skill loads and OFF isolation were verified from command traces. Scorers saw only the request, responses A/B, rubric and decision rules; condition labels and traces were hidden. A/B order was reversed between scorers.

| Pair | ON output | OFF output | Scorer 1 | Scorer 2 | Result |
| --- | --- | --- | --- | --- | --- |
| C1 — critical segment failure | Final B2 above | 52-word baseline, SHA-256 `4be40709bda8e61ef906558756f9de6d2cd85331de0d91d98e136de7bd2fe33b` | No material difference | No material difference | **No material difference** |
| C2 — judge disagreement and leakage | B3 above | 155-word baseline, SHA-256 `43f8a9bbe6dedbc375bc9a22f95eea04c8b68efd1e73e219d3f8a7e9de8fcc98` | ON better | ON better | **ON better** |

The C1 OFF answer correctly blocks `rc-7` because the accepted zero-critical-failure gate failed. The final ON answer adds explicit evidence state, independent held-out multi-patient cases, regression gates, updated configuration recording and release accountability. Both scorers judged those additions useful but not materially decision-changing for this narrow prompt.

The C2 OFF answer correctly rejects launch readiness, detects tuning-set leakage and asks for same-case judge calibration and a representative held-out set. Both scorers still preferred ON: it additionally requires case-level specialist adjudication, concise-complete versus verbose-incomplete calibration examples, accountable segment and severity gates, operational evidence, monitoring, and re-evaluation triggers without inventing numbers.

### Refinements and excluded attempts

1. **Evaluation-protocol review:** independent package review found that the first B4 expectation rewarded `CONDITIONAL GO` without inspectable evidence, the reviewer rubric lacked complete decision rules, the plan template omitted input/system context, and B5/B6 lacked forbidden behaviors. A synthetic inspectable fixture, explicit staging rule, complete reviewer mapping and missing negative criteria were added before formal generation.
2. **Fixture regression:** a second review caught a `4/4` fallback claim backed by only three cases, an unspecified fixture-copy path, and no verdict when both comparison arms block. The fixture was corrected to `3/3`, staging was made byte-specific, and the decision rule now handles both-arm failures.
3. **Routing:** candidate `13dc7d8` loaded the skill for N1 because the frontmatter repeated leaderboard/model-selection exclusion terms. That valid failure was retained. The frontmatter was restored to the approved positive discovery description; the six-case routing regression then passed.
4. **Release boundary:** the first final B4 output scoped the synthetic result but did not explicitly deny safety/compliance certification. The `CONDITIONAL GO` instruction was tightened; the rerun passed.
5. **Regression scope:** the first final B6 output did not explain when a focused versus full rerun was warranted. The skill now targets changed components plus critical and representative segment gates, reserving a full rerun for changes that can affect the complete task or evidence boundary. The combined model/prompt/retrieval case then justified and passed a full rerun.
6. **Critical-segment retest:** a later B2 output asked for relevant regression cases but did not explicitly require independent held-out critical-segment cases. The final candidate adds that requirement and rejects rerunning only known failures; the exact-candidate regression passed.

Pre-refinement outputs and preliminary blind scores were not substituted for the final records. They were used only to identify the narrow corrections above. No failed model call, web-contaminated run, or tool-error run was included in the final score.

### Limitations

- One valid generation per case/arm; all prompts are synthetic and English-language.
- The same model family generated and reviewed outputs, although contexts were fresh and comparison labels were blinded.
- C1 shows no material advantage over a strong ordinary answer; the skill's comparative benefit is demonstrated only on C2 in this small suite.
- Routing was run before the final two body-only refinements; the discovery description is unchanged. B1/B3–B6 precede the final one-line `NO-GO` refinement; B2 was rerun on the exact final runtime manifest. This is targeted regression evidence, not a claim that every case was regenerated on every commit.
- Output hashes identify the reviewed records, but local temporary traces and generated outputs are not repository runtime dependencies.
- The behavioral campaign does not prove real-world quality, statistical significance, production safety/compliance, standalone installation, or named-client compatibility. The separate public-origin check below covers only installation integrity and routing in its named client/version.

## Public-origin and named-client verification

On 2026-10-23 (Europe/Rome), an anonymous download from public merge commit `1693662a2f3bac4fad57c8b5d901f7e894946253` was extracted to a fresh standalone package directory. The installed runtime bytes matched the repository package:

- `SKILL.md`: `4735ed229139aeabd856b01c9e9182e88613b08e00cf1383b3ebf9d7156a195e`
- `references/evaluation-design.md`: `652b4e1149c9c5b7960e4d4d0587ab253dc7ea0e564c1f57bc55ba332612ac93`
- `references/edge-and-negative-cases.md`: `75cec08790ec23fde529557688f6af39859a7a5161e2d6d6c0f313d69cf5b663`
- `assets/eval-plan-template.md`: `5c0bfcb6ca1a580a4951ae4785fa2287933c3d2018cc4a1964993fb5ec9688fa`
- `assets/release-scorecard-template.md`: `482484f5c32706d16d6c3fff79a3435988a13b730fa45288b42b1b6d9055d5a6`

Repository validation, the Agent Skills reference validator, and Skill Creator quick validation passed on the extracted copy.

Two fresh ephemeral Codex CLI `0.163.0-alpha.11.1` sessions used `gpt-6.1-sol`, high reasoning, a read-only sandbox, disabled web search, and separate workspaces on macOS 15.7.7 (x86_64). Their temporary `CODEX_HOME` configurations disabled apps, plugins, memories, bundled skills, and every detected personal skill path. The public package was the only enabled workspace skill. Neither run read `tests/evals.md`, its fixture, or another skill. Command traces, not model self-report, established the following:

| Case | Prompt | Observed load | Result | Words | Last-message SHA-256 |
| --- | --- | --- | --- | ---: | --- |
| Positive | “Design an evaluation for an AI feature that summarizes support tickets before an agent takes over.” | Read `SKILL.md` and both references | Pass | 894 | `f96daf5f4d49c7d5673e8949349b2f0dfdda5250c9273c28786189434e3be6d9` |
| Near miss | “Pick the best foundation model using public leaderboard scores.” | Did not read the skill | Pass | 98 | `7781fb9b1ad1f15ddd28219b26c6c948be8966bb75e50dfb14520de34d6afc5b` |

The complete captured outputs are [`public-verification-positive.md`](public-verification-positive.md) and [`public-verification-near-miss.md`](public-verification-near-miss.md). Their content matches the CLI last messages; repository files add the conventional terminal newline. In the near miss, the model attempted one shell `curl`; the read-only sandbox blocked DNS resolution, so no external result entered the response. This is disclosed as a tool-control limitation even though routing was correct.

A separate sandboxed startup attempt failed before any model response because network access to the model service was unavailable; it is not counted as an execution. These checks establish only anonymous retrieval, byte integrity, and observed routing in this exact client/configuration, not cross-client compatibility or real-world evaluation quality.

## Current evidence

| Gate | Result |
| --- | --- |
| Repository validator unit suite | **Pass** locally on 2026-10-21 — 15/15 tests |
| Repository structural and public-safety validation | **Pass** locally on 2026-10-21 |
| Skill Creator quick validation | **Pass** locally on 2026-10-21 |
| Agent Skills reference validation | **Pass** locally on 2026-10-21 |
| Automatic routing | **Pass** — 3/3 positive loads, 3/3 near-miss non-loads |
| Behavioral cases | **Pass** — B1–B6, no blocking failure, after targeted refinements |
| Controlled comparisons | **C1 no material difference; C2 ON better** — two blind scorers agree, no blocking failure |
| Standalone retrieval/installation from immutable public revision | **Pass** — anonymous extraction from `1693662a2f3bac4fad57c8b5d901f7e894946253` |
| Named client/version compatibility | **Pass, scoped** — Codex CLI `0.163.0-alpha.11.1`, one positive activation and one near miss |

Only actual recorded runs may change these states.
