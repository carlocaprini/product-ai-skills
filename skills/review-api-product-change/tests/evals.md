# Evaluation plan: review-api-product-change

These cases define expected behavior for the current candidate. Expected and observed results are separate. Unless a run record says otherwise, a case is **not run**.

Do not give this file, its expected properties, rubric, or prior outputs to a model performing a test. Runtime files are `SKILL.md`, the two files in `references/`, and the template in `assets/`.

## Candidate and controls

- Candidate revision: working tree based on repository commit `635ee7e`; immutable candidate commit not yet recorded.
- Runtime manifest SHA-256: `6c022f1f942c6070f99b429703ef4308b365e54d87779e22a75c0438d29c6f9c`.
- `SKILL.md`: `5f72fbf6484d5a0e3da63be55bdc5763d2170294f195d7dc1618999597475528`.
- `references/compatibility-taxonomy.md`: `eeb5e60309dab2c35fde0b7ad5cdb04162f1218bb52bd6661ed99ceaa7cdc74f`.
- `references/consumer-impact-questions.md`: `4697b4582c16d5d921af96bc7d92b79ab41b1c4e097d49e21c7edb9e2e636375`.
- `assets/api-change-review-template.md`: `b7f3e4f974e58b514418d173d6bb8b4ed5bb479d51339e4fd03dd648a495deef`.
- Client/model/version/settings: not yet recorded.
- Execution environment and timezone: not yet recorded.
- Reviewer: not yet recorded.
- External actions: prohibited; all APIs, consumers, companies, telemetry, thresholds, and migrations are synthetic.

An executed run must record the exact commit, runtime manifest or file hashes, client and version, model/settings when available, tool access, context isolation, date/timezone, prompt, actual output, skill-load or isolation evidence, reviewer, verdict, and limitations. Unknown metadata remains `not recorded`, never inferred.

## Routing cases

Routing tests require automatic discovery in a fresh context; explicit invocation tests behavior, not discovery.

| ID | Synthetic prompt | Expected route |
| --- | --- | --- |
| T1 | “We want to change an existing public REST endpoint from offset to cursor pagination. Review consumer compatibility and rollout.” | Activate; review current/proposed semantics and consumer migration. |
| T2 | “Our webhook will add an event field and change retry/delivery behavior. What breaks for subscribers?” | Activate; treat event semantics separately from payload schema. |
| T3 | “We plan to tighten authorization on a GraphQL field used by mobile and partner clients. Review the migration.” | Activate; assess per-client access, mixed versions, docs, and rollout. |
| N1 | “Design a new API for a greenfield inventory service.” | Do not activate; there is no existing API change to compare. |
| N2 | “Audit this API handler for injection and authentication vulnerabilities.” | Do not activate; this is a security/code audit. |
| N3 | “Should we build an export feature or improve onboarding?” | Do not activate; this is a general product decision. |

## Behavioral cases

### B1 — additive schema, breaking semantic default

**Prompt**

> We propose changing fictional `GET /v1/orders`. The response adds optional `status`, but results will now default to newest-first instead of oldest-first. The published schema allows the new field. Our generated SDK ignores unknown fields. One internal fulfillment client takes the first result as the next order to process. Partner consumers are not inventoried. Is this backward compatible, and how should we ship it?

**Pass properties**

- Separates the additive field from the default-order behavior.
- Marks the internal fulfillment behavior breaking; partner impact unknown, not compatible.
- Does not generalize SDK tolerance to every consumer.
- Recommends a concrete low-disruption strategy such as preserving the old default plus explicit sort opt-in, or a bounded dual behavior with migration.
- Includes documentation/test changes, rollout signals, and an owner-approved stop condition without inventing a number.

**Forbidden**

Blanket “backward compatible,” a score without evidence, invented telemetry/tests, or automatic `/v2` with no trade-off.

### B2 — missing consumer inventory

**Prompt**

> An internal REST endpoint has been reachable by partner integrations for years. We want to remove one response field next month. Gateway logs for the last 14 days show no reads of that field, but field-level logging is sampled and older/offline clients may exist. Can we remove it safely?

**Pass properties**

- Treats the proposed removal as breaking for consumers that rely on the field.
- Treats 14-day sampled evidence as scoped observation, not proof of absence.
- Returns `unknown` for unobservable/long-lived consumers and identifies the smallest useful inventory or consumer test.
- Recommends hold/deprecation/compatibility handling with communication and an exit condition rather than unconditional removal.

**Forbidden**

“No usage means safe,” a fabricated partner list, or an invented deprecation period.

### B3 — event delivery, SDK migration, and irreversible effects

**Prompt**

> A fictional payments webhook currently delivers `payment.updated` at least once and consumers deduplicate by `event_id`. We propose splitting it into `payment.authorized` and `payment.settled`, rotating the signature scheme, and shortening retries. Our new SDK supports both formats, but long-lived clients may use the old SDK. Events can trigger shipment. Design the compatibility and rollout decision. No adoption thresholds are supplied.

**Pass properties**

- Covers event meaning, ordering/delivery/retry, signature/auth, deduplication, SDK versions, and mixed producer/consumer rollout.
- Does not call a new SDK release sufficient migration evidence.
- Proposes a staged/dual or adapter strategy with replay/deduplication and consumer verification.
- States that duplicate shipment or consumed events cannot be undone by a code rollback; uses containment/reconciliation or rollforward.
- Leaves thresholds to accountable owners rather than inventing values.

**Forbidden**

Schema-only analysis, blind replay, “revert deploy” as complete recovery, or claimed client testing.

### B4 — same schema, changed error and pagination behavior

**Prompt**

> The OpenAPI schema is unchanged, but expired page tokens will return `400 invalid_token` instead of restarting at page one, and rate-limit errors change from `429` to `503`. Is this a non-breaking implementation detail?

**Pass properties**

- Rejects the schema-only conclusion and analyzes error/retry/pagination semantics per consumer.
- Identifies possible infinite retry, data duplication/omission, and monitoring/documentation impact.
- Requests or proposes targeted consumer evidence without claiming it exists.

### B5 — authorization change with stable endpoint

**Prompt**

> The endpoint and payload stay the same, but callers will need a new resource-level scope. Known first-party clients can refresh credentials; a partner app owner has not responded. Can we call this compatible?

**Pass properties**

- Marks the access pattern breaking for callers without the scope and partner status unknown.
- Separates contract shape from authorization compatibility.
- Includes credential migration, communication, staged enforcement, and hold/exception decision.

### B6 — missing before state

**Prompt**

> Review whether our proposed order API change is backward compatible. I can share the new response but not the current contract or examples.

**Pass properties**

- Does not declare compatibility.
- Asks once for the decisive current fragment and still supplies a provisional risk inventory.
- Avoids a long mandatory intake questionnaire.

## Interaction checks

- **I1:** A narrow question receives a concise verdict and only relevant rows, not the full template.
- **I2:** A consequential multi-consumer change receives a compatibility matrix and staged handoff.
- **I3:** Missing decisive evidence triggers at most one focused request before a provisional assessment.
- **I4:** Unknown consumers remain `unknown`; absence is never silently converted to compatible.
- **I5:** Tool output may be used only when actually supplied or run; no execution is invented.
- **I6:** Stop thresholds are attributed to the user/accountable owner or marked to be agreed.

## Controlled comparisons

Run both pairs in fresh, independent contexts. ON has only this candidate skill available and verifiably loaded; OFF has no candidate files or copied instructions. The substantive prompt is identical within a pair.

| Pair | Prompt | With-skill expectation | Shared forbidden behavior |
| --- | --- | --- | --- |
| C1 — semantic default | B1 verbatim | Better separation of schema, observable behavior, consumer classes, uncertainty, and migration/rollout practicality. | Blanket compatibility, invented evidence, default version bump. |
| C2 — event migration | B3 verbatim | Better coverage of event semantics, mixed SDKs, irreversible effects, and safe recovery. | Schema-only verdict, blind replay, complete-rollback claim. |

### Comparison validity

1. Pin the candidate commit and hash runtime files. Keep client, model, reasoning/sampling settings, tools, output budget, and common instructions the same across arms; record unavailable settings as unavailable.
2. Use fresh contexts and workspaces. Do not expose this eval file, expected answers, rubrics, prior outputs, or one arm to the other.
3. Record verifiable ON load evidence and OFF isolation evidence. Model self-report is insufficient. If either cannot be established, mark the pair **inconclusive**.
4. Planned order is C1 ON → OFF, then C2 OFF → ON. Record actual order and deviations; do not replace failed attempts with selected outputs.
5. Have a reviewer blind to condition order score complete outputs. One reviewer is the minimum; a second independent reviewer is preferred. Reveal conditions only after scores are fixed.
6. Summarize each pair as **ON better**, **no material difference**, **OFF better**, or **inconclusive**. Two synthetic pairs are regression evidence, not proof of general effectiveness.

## Rubric

Score each dimension `met`, `partly met`, or `not met`, citing the output:

1. Correct routing and scope: API product-change review, not greenfield design, code audit, or implementation.
2. Baseline and provenance: current/proposed state, published versus observed/provided/inferred/unknown.
3. Consumer awareness: distinct classes, versions, dependencies, and unknown consumers.
4. Compatibility coverage: wire/schema plus behavior, auth, errors, limits, lifecycle, event/data semantics, and DX as relevant.
5. Decision quality: per-consumer `compatible`/`breaking`/`unknown` with evidence and a justified evolution strategy.
6. Migration and rollout practicality: SDK/docs/comms, mixed versions, verification, owner-supplied stop conditions, and exit plan.
7. Recovery realism and honesty: irreversible effects handled; no invented execution, evidence, thresholds, or compatibility claim.
8. Proportionality: direct verdict, focused question when necessary, and detail matched to stakes.

Blocking failures are: declaring compatibility while a decisive contract or consumer gap is missing; treating sampled telemetry as proof of no consumers; ignoring a material semantic/auth/event break; inventing executed tests or adoption evidence; or promising rollback for an effect that cannot be reversed safely.

## Run records

| Record | Status | Observed route/load or isolation evidence | Output and rubric verdict |
| --- | --- | --- | --- |
| T1–T3 | **Not run** | Not recorded | Not assessed |
| N1–N3 | **Not run** | Not recorded | Not assessed |
| B1–B6 | **Not run** | Not recorded | Not assessed |
| C1-ON / C1-OFF | **Not run** | Not recorded | Pair not assessed |
| C2-ON / C2-OFF | **Not run** | Not recorded | Pair not assessed |

## Current evidence

| Gate | Result |
| --- | --- |
| Repository validator unit suite | **Pass** locally on 2026-10-21 — 15/15 tests |
| Repository structural and public-safety validation | **Pass** locally on 2026-10-21 |
| Skill Creator quick validation | **Pass** locally on 2026-10-21 |
| Agent Skills reference validation | **Pass** locally on 2026-10-21 |
| Automatic routing | **Not run** |
| Behavioral cases | **Not run**; external model evaluation of the unpublished local candidate was not authorized |
| Controlled comparisons | **Not run**; external model evaluation of the unpublished local candidate was not authorized |
| Standalone retrieval/installation from immutable public revision | **Not run** |
| Named client/version compatibility | **Not claimed** |

Only actual recorded runs may change these states.
