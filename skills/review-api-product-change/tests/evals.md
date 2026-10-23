# Evaluation plan: review-api-product-change

These cases define expected behavior for the current candidate. Expected and observed results are separate. Unless a run record says otherwise, a case is **not run**.

Do not give this file, its expected properties, rubric, or prior outputs to a model performing a test. Runtime files are `SKILL.md`, the two files in `references/`, and the template in `assets/`.

## Candidate and controls

- Candidate revision: tested working tree based on package commit `f512a2e`; the runtime manifest below identifies the refined candidate exactly.
- Runtime manifest SHA-256: `2912a1a7727e3c6cbfb8d5d92734a45f8a25b8e95e968b4e17debfed6ac85bd0`.
- `SKILL.md`: `246148b24ccdb7242bb9c86d4ed0fd7cad3ec13f2faa5c6ff7cec39659d0e704`.
- `references/compatibility-taxonomy.md`: `eeb5e60309dab2c35fde0b7ad5cdb04162f1218bb52bd6661ed99ceaa7cdc74f`.
- `references/consumer-impact-questions.md`: `4697b4582c16d5d921af96bc7d92b79ab41b1c4e097d49e21c7edb9e2e636375`.
- `assets/api-change-review-template.md`: `b7f3e4f974e58b514418d173d6bb8b4ed5bb479d51339e4fd03dd648a495deef`.
- Client: Codex CLI `0.163.0-alpha.10.2`.
- Model/settings: `gpt-6.1-sol`, high reasoning, read-only sandbox, ephemeral sessions, user configuration ignored, browser features and web search disabled for valid runs.
- Execution environment and timezone: isolated temporary ON/OFF workspaces on macOS; 2026-10-21, Europe/Rome; exact start times were not retained in this public record.
- Review: one independent same-model behavioral reviewer and two independent same-model blind comparison scorers. The repository owner authorized sending the unpublished candidate to the model service for this evaluation.
- Context isolation: every generation and scoring run used a fresh ephemeral context. ON had only this candidate skill and used explicit invocation for behavior; OFF contained no skills. Automatic routing never named the skill.
- Tool controls: valid runs used no web or external integrations. Preliminary runs contaminated by web access or by an instruction that biased skill loading were excluded rather than scored; see limitations.
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
- Asks once for the decisive current-versus-proposed fragment, or a sanitized delta/internal comparison when the current artifact is unavailable, and still supplies a provisional risk inventory.
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

## Observed summary

| Dimension | Result |
| --- | ---: |
| Automatic routing | **6/6** — sensitivity 3/3, specificity 3/3 |
| Behavioral review | **6/6 pass** after one targeted B6 correction |
| ON hard failures | **0** |
| C1 blind preference | **ON / ON** |
| C2 blind preference | **ON / no material difference** |
| Final C1 output length | ON 351 words / OFF 245 — **1.43×** |
| Final C2 output length | ON 741 words / OFF 703 — **1.05×** |

The two comparison scorers received opposite A/B ordering. Neither scorer saw condition labels. The final candidate improved both compared scenarios without a blocking failure; C2's advantage was narrow and one scorer found no material difference.

## Automatic-routing observations

The substantive prompts are T1–T3 and N1–N3 above. Every run used a fresh context. The common control stated only that web and external integrations were unavailable; it did not name or suggest a skill.

| ID | Expected load | Observed `SKILL.md` read | Result | Observed response opening |
| --- | --- | --- | --- | --- |
| T1 | yes | yes | **Pass** | “Recommend additive cursor opt-in; hold an in-place replacement.” |
| T2 | yes | yes | **Pass** | “Treat this as potentially breaking.” |
| T3 | yes | yes | **Pass** | “Hold broad rollout pending a consumer migration path.” |
| N1 | no | no | **Pass** | Designed the requested greenfield inventory API without compatibility-review framing. |
| N2 | no | no | **Pass** | Requested the missing handler for a security/code audit. |
| N3 | no | no | **Pass** | Gave a provisional product-choice recommendation without loading this skill. |

Command traces, rather than model self-report, established the reads. OFF and negative traces contained no candidate-skill read. No valid routing run used web or an external integration.

## Behavioral observations

An independent reviewer received the requirements and complete outputs, but not the candidate skill or generation traces. It initially scored B1–B5 **Pass** and B6 **Partial** because the response did not ask specifically for a sanitized current-to-proposed delta. After the narrow instruction correction, a fresh B6 run and independent targeted review scored **Pass**. No case contained a blocking failure.

| Case | Words | Verdict | Observed decisive behavior |
| --- | ---: | --- | --- |
| B1 | 351 | **Pass** | Separates additive parsing from breaking ordering; preserves partner unknowns and existing default. |
| B2 | 354 | **Pass** | Rejects sampled non-observation as absence proof; holds removal and requires deprecation evidence. |
| B3 | 741 | **Pass** | Separates event, signature, retry and business-idempotency migration; shipment is not rollback-safe. |
| B4 | 320 | **Pass** | Treats pagination and error semantics as breaking despite unchanged OpenAPI. |
| B5 | 337 | **Pass** | Treats new scope as breaking; partner readiness remains unknown. |
| B6 | 278 | **Pass after correction** | Holds verdict, gives a provisional inventory, and asks once for a sanitized current-to-proposed delta. |

<details>
<summary>B1 complete final output</summary>

> **The combined proposal is breaking. Hold the default-order change; preserve oldest-first in `/v1/orders` and offer newest-first through an explicit sort option.**
>
> This conclusion follows from your supplied facts, which I have not independently verified. The schema permits `status`, but schema validity does not establish behavioral compatibility. The fulfillment dependency makes the ordering break clear; partner impact remains unknown.
>
> | Change | Consumer | Decision and migration burden |
> |---|---|---|
> | Optional `status` | Known generated SDK | **Compatible** for parsing within the stated SDK behavior; confirm supported versions. Existing clients need no parsing change. |
> | Optional `status` | Uninventoried partners | **Unknown**: strict decoders or downstream validators may reject it. Identify affected clients and test representative parsers. |
> | Newest-first default | Fulfillment client | **Breaking**: taking the first result selects a different order. Preserve its behavior or migrate it to explicit oldest-first. |
> | Newest-first default | Uninventoried partners | **Unknown**: ordering and pagination dependencies are unassessed. Preserve their existing default. |
>
> Ship the field and sorting capability as separate changes. An illustrative `sort=created_at_desc` can expose newest-first without forcing migration. Add SDK access to `status` and sorting, document field omission semantics, ordering, tie-breaking, pagination and invalid-sort errors, and publish before/after examples. A new version is justified if changing the default is essential; it is unnecessary merely to offer newest-first.
>
> 1. **Verify:** API and fulfillment owners should test first-result selection, supported SDK versions, pagination and mixed old/new deployments. The partner owner should build a scoped inventory from usage and support records, recording coverage gaps.
> 2. **Release:** Publish docs and SDK support before opt-in rollout. Canary `status` with identified consumers; expand sorting to explicit opt-ins. Directly notify partners. Product/support owners must approve any migration window and retirement criteria before announcing a default change.
> 3. **Monitor and recover:** Agree stop thresholds for parsing errors, latency, pagination defects and incorrect fulfillment selection. Disable the affected rollout on breach. Restoring ordering cannot undo fulfillment already performed; operations must contain and reconcile affected processing.
>
> Remaining gates are supported SDK versions, partner parser/ordering evidence, and owner-approved rollout criteria. No tests, telemetry queries or migrations were run.

</details>

<details>
<summary>B2 complete final output</summary>

> **Hold the removal; begin deprecation.** There is high confidence that the supplied evidence does **not** establish safe removal next month. Calling the endpoint “internal” does not reduce the compatibility obligations created by years of partner access.
>
> Your description is **provided/unverified** evidence: sampled field logging reported no reads over 14 days. The published contract, supported client versions, and deprecation commitments are **unknown**. Gateway logs may also lack visibility into downstream field access; establish what “reads” actually measures. Even complete observation over that window would miss dormant or offline clients.
>
> | Response-field removal × consumer class | Compatibility | Evidence and migration burden |
> |---|---|---|
> | Clients requiring the field in parsing or business logic, if present | **Breaking** | Missing differs from null/default; clients need code or SDK changes. |
> | Recently active internal/partner clients | **Unknown** | Sampled non-observation cannot establish independence; consumer validation needed. |
> | Older, offline, or unidentified integrations | **Unknown** | No coverage established; discovery and potentially longer support required. |
>
> Choose **deprecate + retain compatibility**. Preserve the field on the existing supported interface while consumers migrate. If next month’s deadline is essential, consider an explicit opt-in field-free response while retaining existing behavior for others. Introduce a new version only if existing evolution mechanisms cannot support that separation.
>
> 1. **Establish the baseline.** API and partner owners should check the contract, SDKs, consumer/support records, telemetry coverage, and longest supported client lifecycle. Define an approved support window and retirement criteria; silence is not adoption.
> 2. **Prepare and verify migration.** Publish before/after responses, missing-field semantics, any replacement, SDK changes, release notes, and direct partner notices. Request consumer tests covering deserialization, business behavior, and old/new client coexistence. None has been run here.
> 3. **Stage removal.** Start with validated, consenting consumers. Engineering and product owners must agree stop thresholds for client failures, retries, support incidents, and business outcomes. Keep field restoration available; it cannot undo downstream incorrect decisions or other external effects.
>
> The smallest decision-changing evidence is representative consumer testing without the field, plus coverage of supported dormant clients and confirmation that deprecation commitments permit retirement. Until then, next month is an unsupported removal date.

</details>

<details>
<summary>B3 complete final output</summary>

> **Recommend an opt-in, versioned webhook contract with a legacy compatibility path; hold forced migration, signature retirement, and shorter retries.** Confidence is high that replacing the current behavior would break consumers. Confidence in a faithful adapter is limited until the existing event semantics are defined.
>
> The intent is to expose payment lifecycle stages while changing authentication and delivery policy. All baseline facts are **provided/unverified**. No published contract, SDK versions, telemetry, or consumer tests were inspected. **Inferred:** parsing both formats does not establish safe fulfillment. **Unknown:** the current shipment predicate, identity mapping, signature details, retry windows, and support commitments.
>
> | Change | Consumer class | Status | Impact and migration burden |
> |---|---|---|---|
> | Replace `payment.updated` | Old SDK and handlers subscribed to that type | **breaking** | Events may be rejected or ignored; preserve the legacy subscription and payload. |
> | Split event formats | New SDK | **compatible**, for decoding only, per requester | Business handlers still need explicit lifecycle routing. |
> | Split meaning, timing, and identity | New SDK fulfillment consumers | **unknown** | Both events might trigger shipment; existing `event_id` deduplication may not prevent duplicate business effects. |
> | Replace signature scheme | Old verifiers | **breaking** | Retiring their supported scheme prevents authentication; retain it on the legacy path. |
> | New signature scheme | New SDK/custom verifiers | **unknown** | “Both formats” does not establish signature support; verify exact versions and raw-body handling. |
> | Shorten retries | Consumers relying on the removed retry interval | **breaking** | Supported recovery time disappears regardless of SDK version. |
> | All changes | Uninventoried or dormant consumers | **unknown** | Inventory endpoints, owners, deployed versions, and support obligations; silence is not adoption. |
>
> Use a **webhook subscription version**, without requiring a broader payments API version change. Existing subscriptions retain their event types, signatures, and delivery policy. A legacy adapter is acceptable only if it reproduces the original observable transitions, payloads, identities, and timing. Blindly renaming both new events to `payment.updated` is insufficient.
>
> For the new contract:
>
> - `payment.authorized` and `payment.settled` represent distinct facts and receive distinct event IDs; retries and replays of the same event preserve its ID.
> - Document ordering guarantees and behavior when settlement arrives first. Shipment must follow an explicit fulfillment rule. Authorization must not silently inherit a handler that assumes settlement.
> - Across representations, preserve a canonical transition identity or provide an explicit mapping. Use a durable business idempotency key for shipment, scoped to the fulfillment operation; event-ID deduplication alone cannot prevent two different events from shipping the same order.
>
> **Migration and rollout**
>
> 1. **Define and verify — API, payments, SDK, and fulfillment owners.** Publish before/after payloads, identity mappings, shipment rules, signature headers and verification failures, acknowledgement/error handling, retry schedules, replay behavior, and cutover instructions. Release SDK guidance and migration examples before invitations. Proposed tests must cover old SDK verification, duplicates, reordered delivery, outage recovery, replay, and interruption between recording an event and dispatching shipment. None have been run.
> 2. **Pilot by explicit endpoint opt-in — delivery operations and consumer owners.** Separate event migration, signature rotation, and retry reduction into independently controlled changes. Preserve legacy signing for old endpoints. Dual signatures require evidence that old verifiers tolerate the headers; otherwise use separate endpoint profiles. Pin queued deliveries to their original contract and delivery policy. Avoid delivering both representations to active fulfillment handlers unless shared business idempotency is verified. Communicate through release notes, dashboard notices, and direct owner outreach, with migration assistance and escalation contacts.
> 3. **Expand and retire conditionally — product/support and operations.** Track endpoint-confirmed migration, verification failures, acknowledgements, exhausted retries, delivery lag, reconciliation gaps, and duplicate or premature shipments. SDK downloads are insufficient adoption evidence. **No numerical adoption or stop thresholds were supplied: owners must approve them before production expansion or retirement.** Premature or duplicate shipment should pause the affected cohort immediately. Agree the support window, notice period, exception policy, adapter operating cost, and retirement evidence before announcing sunset.
>
> Recovery must contain effects: pause affected delivery or fulfillment, preserve queues and identity history, reconcile payment/order/shipment records, and repair forward. Redeploying old code cannot undo shipment; replay requires reconciliation and preserved deduplication.
>
> The decisive missing fragment is: **what does `payment.updated` represent today, including its `event_id` assignment and the condition consumers use to ship?** A representative payload/transition sequence and fulfillment-handler test would determine whether a faithful adapter is possible. Until resolved, and until owners approve rollout gates and support commitments, forced cutover remains on hold.

</details>

<details>
<summary>B4 complete final output</summary>

> **No—treat these as breaking behavioral changes, even with an unchanged OpenAPI schema. Hold an unannounced default rollout.** Consumers depend on pagination and error semantics as well as response shapes.
>
> The baseline comes from your description (**provided, unverified**). Published guarantees, affected SDK versions, and actual consumer behavior are unknown; the impacts below are inferred.
>
> | Change | Consumer class | Compatibility and migration burden |
> |---|---|---|
> | Expired token: restart at page one → `400 invalid_token` | Clients relying on automatic restart | **Breaking:** pagination now fails. Clients must handle expiry and explicitly restart or recover, accounting for duplicate processing. |
> | Rate limit: `429` → `503` | Clients/SDKs distinguishing throttling from service failures | **Breaking:** retry, backoff, exception handling, circuit breakers, and alerting may change. Clients need updated handling. |
> | Both changes | Uninventoried internal, partner, or public clients | **Unknown:** no evidence establishes continued correct operation. |
>
> Rejecting expired tokens can improve correctness by preventing silent restarts, but that benefit does not make the change compatible. Likewise, `503` communicates service unavailability; it can trigger different behavior from `429` throttling, even when both are retried.
>
> **Recommended strategy:** retain `429` for rate limiting and introduce explicit token-expiry errors through opt-in behavior or a controlled migration. Use a new version only if existing support commitments or inability to segment behavior require it.
>
> 1. API and SDK owners should document before/after behavior, update error handling and examples, and communicate the migration before release, with an agreed support window.
> 2. Verify representative pagination and retry clients under both behaviors, then canary opted-in consumers. Monitor pagination failures, duplicate processing, retries, and circuit-breaker activity; owners must agree stop thresholds.
> 3. Preserve a switch back to old behavior during migration. Switching back cannot undo downstream duplicate processing, which may require reconciliation.
>
> The smallest missing evidence is the current documented error contract and representative supported-client tests for token expiry and throttling. No tests or telemetry were run.

</details>

<details>
<summary>B5 complete final output</summary>

> **No—this is a breaking authorization change, even though the endpoint and payload stay the same.** Existing credentials lose access unless callers migrate. First-party readiness makes migration easier; it does not make the change compatible.
>
> That verdict follows from your provided facts. The published authorization contract, credential behavior, and actual client adoption remain unverified.
>
> | Surface / consumer | Status | Impact |
> |---|---|---|
> | Endpoint and payload / all callers | Compatible within the stated wire scope | Reportedly unchanged; authorization still changes. |
> | New scope / first-party clients | Breaking, migration feasible | Must obtain credentials carrying the scope. Ability to refresh is not evidence of successful migration. |
> | New scope / partner app | Breaking for credentials lacking the scope; readiness unknown | Owner silence establishes neither consent nor adoption. |
> | New scope / any uninventoried consumers | Unknown | Inventory coverage and credential requirements are unverified. |
>
> **Recommendation: hold blanket enforcement and use a controlled migration.** A new API version is not automatically necessary. A temporary coexistence window can help if the API and security owners approve it.
>
> 1. **Prepare:** The API/auth owner confirms how callers obtain the scope—including whether refresh requires a new grant or consent. Document credential acquisition, resource restrictions, authorization errors, retry guidance, SDK/configuration changes, and the enforcement date.
> 2. **Verify and stage:** Client owners demonstrate successful requests with new credentials and expected failures with old credentials, including resource-boundary checks. Canary verified first-party clients; monitor scope adoption, authorization failures, retries, and successful operations. Owners must agree stop criteria before enforcement.
> 3. **Resolve the partner:** The partner relationship owner pursues confirmation and migration evidence. Retain approved legacy behavior through an agreed support window, or follow the applicable deprecation/exception policy. If enforcement must proceed sooner, describe it explicitly as a breaking change with unresolved partner impact.
>
> The immediate blockers are verified credential migration and a partner transition decision. Recovery must be approved too: restoring old authorization may be unacceptable, and redeploying code will not necessarily restore revoked grants or credentials.

</details>

<details>
<summary>B6 complete final output</summary>

> **Recommendation: hold rollout approval; backward compatibility is unknown.** Baseline confidence is insufficient: neither response has been inspected, and the current contract and behavior are unavailable. A new response alone can reveal risks, but cannot establish compatibility.
>
> Provisional risk inventory—these are possibilities, not findings:
>
> | Surface × consumer class | Status | Potential impact |
> |---|---|---|
> | Response fields × generated SDKs or strict parsers | `unknown` | Removed/renamed fields, type or nullability changes, and sometimes additions can require client updates. |
> | Order semantics × business integrations | `unknown` | Changed status meanings, monetary units, defaults, or timestamps can break logic despite unchanged types. |
> | Errors, pagination, retries or events × consumers using those behaviors | `unknown` | Changes may affect recovery, completeness, or duplicate processing. Consumer coverage is also unknown. |
>
> Keep existing behavior available while gathering evidence. An additive change may be sufficient; an adapter or explicit opt-in may be needed where consumers cannot tolerate the change. There is no basis yet to require a new version.
>
> Before broad rollout, the API and consumer owners should validate representative existing clients, document required SDK/migration changes, and agree on a support window, stop conditions, and recovery. Any changed order mutations or emitted events need reconciliation planning; reverting a deployment would not undo those effects. No tests or telemetry have been inspected.
>
> Please share:
>
> - The **proposed response**, affected operation/protocol, and intended benefit.
> - A **sanitized current→proposed delta**, or a sanitized summary of an internal comparison, covering structural and behavioral changes. Field aliases are fine; preserve the nature of each change.
>
> That avoids sharing the current contract or examples while supplying the comparison needed for a defensible verdict.

</details>

## Controlled comparison observations

C1 ran ON then OFF; C2 ran OFF then ON, as planned. ON traces read the exact candidate runtime; OFF traces contained no skill or copied instruction. All four generation arms used the same client, model, reasoning, sandbox and no-web controls. Scorers saw complete outputs in opposite A/B order and no condition labels.

The score columns are: scope, provenance, consumers, compatibility coverage, decision quality, migration/rollout, recovery/honesty, and proportionality/clarity.

| Scorer | Pair | ON scores | OFF scores | Preference | Hard failure |
| --- | --- | --- | --- | --- | --- |
| 1 | C1 | 5/5/5/5/5/5/5/5 = **40** | 5/4/5/4/5/4/3/5 = **35** | ON | none |
| 2 | C1 | 5/5/5/5/5/5/5/5 = **40** | 5/4/4/4/5/4/3/5 = **34** | ON | none |
| 1 | C2 | 5/5/5/5/5/5/5/5 = **40** | 5/4/5/5/5/5/5/5 = **39** | ON, narrowly | none |
| 2 | C2 | 5/5/5/5/5/5/5/4 = **39** | 5/4/5/5/5/5/5/5 = **39** | no material difference | none |

**C1 verdict: ON better.** Both arms found the semantic ordering break. ON more exactly scoped known SDK compatibility, preserved partner unknowns, named rollout gates and recognized that restoring ordering cannot undo fulfillment.

**C2 verdict: ON better narrowly.** Both arms were strong. ON improved evidence separation, owner/gate clarity and queued-delivery contract handling; OFF was slightly clearer and added a useful shadow-delivery stage. One scorer found no material difference, so this result does not establish a broad superiority claim.

<details>
<summary>C1 OFF complete output</summary>

> **The combined change is not backward compatible.** The optional `status` field is compatible with the published schema and your SDK’s unknown-field handling. Changing the default ordering breaks observable behavior: the fulfillment client will process the newest order instead of the oldest.
>
> Schema compatibility and successful deserialization do not establish behavioral compatibility. Even if ordering was undocumented, you have evidence of a dependency. Uninventoried partners add uncertainty; they are not evidence that the change is safe.
>
> Ship the two changes separately:
>
> 1. **Add `status` while preserving oldest-first ordering.** Verify existing responses remain valid and representative consumers tolerate the field.
> 2. **Make newest-first opt-in**, for example through `sort=created_at_desc`, while keeping the existing default for existing callers. Specify a deterministic tie-breaker and consistent pagination behavior.
> 3. **Update fulfillment to request oldest-first explicitly.** Verify that it still selects the intended next order, including across ties and pages.
> 4. **Identify and migrate consumers.** Use traffic records, credentials, ownership records, and partner outreach to establish who depends on the endpoint and communicate the ordering choice.
> 5. **If the default must change, introduce a new API version or an explicit compatibility setting.** Keep existing consumers on the old behavior, with a documented migration and deprecation process.
>
> Use a staged rollout with monitoring and a rollback switch. Watch fulfillment order, oldest pending order age, and pagination behavior alongside errors—this change can return valid `200` responses while doing the wrong work. A canary helps detect problems; it does not make the default change compatible.

</details>

<details>
<summary>C2 OFF complete output</summary>

> **Introduce an opt-in, endpoint-versioned contract. Keep existing endpoints on the legacy behavior. Do not bundle the event split, signature rotation, and shorter retries into a mandatory upgrade.** A new SDK’s capabilities do not establish what deployed consumers can safely process.
>
> The current meaning of `payment.updated` is unspecified. Before defining its replacement, establish which transitions produce it, what its payload represents, and when consumers use it to authorize shipment. That mapping is a release blocker.
>
> | Dimension | Existing endpoints | Opt-in contract |
> |---|---|---|
> | Events | Preserve `payment.updated`, its triggers, and payload semantics | Explicit subscriptions to `payment.authorized` and `payment.settled` |
> | Signatures | Preserve the working verification contract | Explicitly negotiated new scheme |
> | Retries | Preserve the existing delivery window and schedule | Shorter retries require separate acceptance |
> | Selection | Persisted endpoint configuration | Never infer support from SDK version or a successful HTTP response |
>
> **Protect shipment independently of event deduplication.**
>
> - Give authorization and settlement distinct, immutable event IDs. Preserve each ID across retries and replays. Include payment identity, event type, occurrence time, contract version, and a correlation or transition identifier.
> - Preserve legacy event IDs when replaying legacy events. Where old and new representations describe the same occurrence, expose a documented mapping; do not invent equivalence where semantics differ.
> - Deduplicating by `event_id` only suppresses repeated delivery of that event. Authorization and settlement can each have a different ID and still cause duplicate shipment.
> - Require an explicit fulfillment rule. Authorization must not automatically become shipment eligibility merely because it is now a named event. Settlement also must not be described as irreversible.
> - Enforce fulfillment idempotency using a durable business key, such as an order’s fulfillment operation. Apply it across event types, endpoints, versions, and replays. Persist processing reliably and pass an idempotency key to the fulfillment system.
> - Handle duplicates and out-of-order arrival without regressing payment state. Do not depend on receiving authorization before settlement.
>
> **Rotate signatures through an explicit overlap period.** Verify compatibility with old verifiers before adding signatures or headers. Where compatible, attach both schemes temporarily; otherwise retain separate endpoint contracts. New consumers must verify the selected scheme against the exact payload bytes and reject invalid signatures without silently falling back. Event identity stays stable when a retry gets a fresh delivery timestamp and signature.
>
> Retiring an old signing key or algorithm requires its own decision. A security emergency may require forced retirement, but that is an explicit compatibility exception with an acknowledged delivery impact.
>
> **Treat shorter retries as reduced delivery resilience.** A consumer that survives an outage under the existing window may lose events under the proposed one. Keep the old policy for existing endpoints; offer the shorter policy separately with documented retention, replay, and reconciliation facilities. Consumers should acknowledge only after durable acceptance. Replay must preserve event IDs.
>
> Roll out in stages:
>
> 1. **Establish the contracts.** Document legacy semantics, version selection, event identity, signature behavior, retry windows, replay, and shipment eligibility.
> 2. **Validate compatibility.** Exercise actual old SDKs and representative handlers, including strict parsers, signature rejection, duplicates, reordering, outages, and rollback. Validate shipment idempotency across both event families.
> 3. **Shadow delivery.** Send new events to sinks that cannot trigger shipment. Compare event coverage, semantic mappings, verification, and delivery outcomes.
> 4. **Opt in consumers individually.** Confirm handler behavior and fulfillment safeguards. Avoid overlapping production subscriptions to both representations unless cross-version idempotency is established.
> 5. **Expand with independent controls.** Monitor signature failures, missing transitions, delivery exhaustion, replay demand, and fulfillment anomalies by endpoint and version. Pause expansion on unexplained correctness failures.
> 6. **Retire only through a separate decision.** Inventory affected consumers, including dormant clients; obtain migration evidence or explicitly accept the consequences for remaining consumers.
>
> Rollback should stop new enrollment and restore the affected endpoint’s prior configuration while preserving queued events, IDs, and processing history. Events already processed or shipments already initiated cannot be undone by changing versions.
>
> **With no adoption thresholds supplied, approve an additive rollout, but not automatic legacy retirement.** Do not invent an adoption percentage or sunset date. Before retirement, the accountable owners must define sufficient migration evidence, treatment of dormant and unreachable consumers, notice requirements, and acceptable residual delivery risk. Until then, retain the legacy contract.

</details>

## Refinements, invalid attempts, and limitations

Observed improvements made during this evaluation:

1. **Routing boundary:** the first unbiased routing run loaded the skill for greenfield API design. The frontmatter description now preserves the approved description and adds explicit greenfield, code/security-review and generic-prioritization exclusions. The final six-case routing regression passed.
2. **Proportionality:** pre-refinement ON outputs were 537 words for C1 and 1,232 for C2. Scorers preferred their substance but marked them less proportionate than OFF. The skill now uses compact/full thresholds and tighter template loading; final outputs were 351 and 741 words while retaining the blind-review advantage.
3. **Unavailable baseline:** the first final B6 review was partial because it did not request a decisive sanitized delta. The skill now asks once for a sanitized current-to-proposed delta or internal comparison when the raw baseline cannot be shared. The rerun passed independent review.

Excluded attempts remain disclosed:

- an initial routing run used web despite the intended controls;
- a first routing batch used a common instruction that mentioned locally available skills and therefore biased negative-case loading;
- feature-disable flags alone did not prevent web use in later preliminary runs.

Those attempts were not scored or silently substituted. Final valid runs set `web_search="disabled"`, disabled browser features, included a common no-web control where needed, and were verified from traces.

Limitations:

- the same model family generated and reviewed the outputs;
- there was one valid generation per case/arm, in English, using synthetic scenarios only;
- C1 and C2 include authored regression cases similar to runtime guidance and are not held-out evidence;
- exact start times and sampling parameters beyond high reasoning were not retained;
- routing in one client build does not establish universal routing or compatibility;
- no result proves that a proposed API control, migration, consumer test, or rollback works in production.

## Current evidence

| Gate | Result |
| --- | --- |
| Repository validator unit suite | **Pass** locally on 2026-10-21 — 15/15 tests |
| Repository structural and public-safety validation | **Pass** locally on 2026-10-21 |
| Skill Creator quick validation | **Pass** locally on 2026-10-21 |
| Agent Skills reference validation | **Pass** locally on 2026-10-21 |
| Automatic routing | **Pass** — 3/3 positive loads, 3/3 near-miss non-loads |
| Behavioral cases | **Pass** — B1–B6, no blocking failure |
| Controlled comparisons | **C1 ON better; C2 ON better narrowly** — no hard failure |
| Standalone retrieval/installation from immutable public revision | **Not run** |
| Named client/version compatibility | **Not claimed** |

Only actual recorded runs may change these states.
