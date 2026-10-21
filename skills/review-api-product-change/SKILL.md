---
name: review-api-product-change
description: Reviews a proposed API product change for consumer impact, backward compatibility, versioning, migration, rollout, documentation, and developer experience. Use when changing an API used by internal or external consumers.
---

# Review API Product Change

Review a proposed change to an existing API as a consumer-facing product change. Produce a compatibility decision and a practical migration and rollout plan. Treat schemas and diff tools as evidence, not as proof that consumers will keep working: consumers depend on observable semantics as well as documented types.

This is a read-only review. Do not edit an API, specification, SDK, repository, deployment, or customer data unless the user separately requests and authorizes that work. Do not claim that a contract test, consumer test, telemetry query, or migration was run unless there is actual output from that execution.

## Activate for an existing API change

Use this skill when a proposed change affects an existing REST, GraphQL, gRPC, webhook, event, or similar machine interface used by internal, partner, or public consumers. Typical requests ask whether a change is breaking, how to evolve a contract, how consumers should migrate, or how to stage rollout and deprecation.

Do not activate for:

- greenfield API design with no current contract or behavior to compare;
- source-code review or implementation debugging alone;
- a security or exploit audit alone;
- generic product prioritization with no API change;
- executing a migration or release rather than reviewing its product impact.

If there is no current API, say that compatibility cannot be assessed and route the work to API design. If the task combines compatibility with implementation or security review, keep this skill's verdict scoped to consumer and product impact; do not imply that it replaces those reviews.

## Start with the available evidence

Minimum useful context is the proposed change and product intent, what is known about current behavior, and at least one affected API surface. Helpful evidence includes current and proposed contract fragments, sample requests/responses/errors, consumer or usage inventory, SDKs, client versions, lifecycle policy, support commitments, SLOs, documentation, and rollout constraints.

When a decisive before/after fragment is missing, ask for it **once** if the answer can materially change the verdict. Still provide a provisional change-risk inventory and name the missing evidence; do not demand every possible artifact before being useful. Missing consumer evidence is not evidence of no consumers.

Separate evidence explicitly:

- **published contract** — the documented machine or human-readable contract and its version;
- **observed behavior** — inspected telemetry, traces, consumer tests, samples, or implementation behavior, with source and coverage;
- **provided/unverified** — facts stated by the requester or another named source but not inspected;
- **inferred** — a conclusion derived from available evidence;
- **unknown** — a material gap, including unobservable consumers or behavior.

Do not upgrade telemetry into a complete inventory, a schema diff into a behavioral guarantee, or a stakeholder statement into verified adoption.

## Load supporting guidance selectively

- Read [compatibility taxonomy](references/compatibility-taxonomy.md) when classifying a multi-surface change, a protocol-specific edge, or a semantic change that a schema diff may miss.
- Read [consumer impact questions](references/consumer-impact-questions.md) only when consumer inventory, migration burden, support obligations, or rollout evidence is materially unclear. Select the smallest decision-changing questions; do not send the whole list as an intake form.
- Use the [API change review template](assets/api-change-review-template.md) when the user asks for a reusable review artifact or the change is consequential enough to require a handoff. For a narrow compatibility question, answer compactly without reproducing the full template.

## Review procedure

1. **Frame intent and baseline.** State the developer/user problem, current and proposed state, API/protocol type, affected operations, authorization boundary, lifecycle policy, and evidence versions or refs. Separate documented behavior, observed behavior, and assumptions.

2. **Map consumers and dependencies.** Identify known internal, partner, and public clients; generated and hand-written SDKs; long-lived versions; webhooks/subscribers; integrations; support commitments; and unknown consumers. Record how each class was identified. Usage evidence shows observed activity within its coverage, not the absence of other consumers.

3. **Decompose the change.** Classify each material change across wire/schema, behavior, authentication/authorization, error semantics, performance/limits, lifecycle/deprecation, data/event semantics, and documentation/developer experience. Do not apply REST-specific rules blindly to GraphQL, gRPC, events, or webhooks.

4. **Assess compatibility per consumer class.** For every material surface/change × consumer class, choose:
   - `compatible` — evidence supports continued correct use within a stated scope;
   - `breaking` — a consumer must change or will receive materially different/invalid behavior;
   - `unknown` — evidence is insufficient or consumer behavior is unobservable.

   Include evidence, affected versions, migration burden, and mixed-version behavior. Never collapse different consumers into one blanket label when their parsers, SDKs, permissions, timing, or support windows differ.

5. **Inspect semantic breakage.** Check defaults and null/missing behavior, ordering and pagination, errors, idempotency and retries, rate/size limits, timestamps, consistency, side-effect timing, auth scopes, event ordering/delivery, and other observable semantics. An additive field can still break strict parsers or downstream logic; an unchanged schema can still hide a breaking behavior.

6. **Compare evolution strategies.** Evaluate the smallest viable set among backward-compatible addition, dual behavior/read/write, compatibility adapter, opt-in/feature flag, controlled migration, deprecation, or a new version. Do not default to a new API version or indefinite parallel versions. State ownership, operational cost, support window, and exit condition.

7. **Design consumer change management.** Specify before/after examples, SDK or generated-client work, error and behavior documentation, release notes, migration guide, discoverability, communication channel/timing, assistance, and accountable owners. If no stable contract exists, establishing one is a prerequisite to a compatibility verdict.

8. **Design staged rollout and recovery.** Define eligible segments, canary/opt-in where viable, contract and consumer tests, adoption/error/latency signals, mixed-version window, user-supplied or owner-approved stop thresholds, and rollback or rollforward policy. Do not invent numerical thresholds. If data mutation, duplicate events, notifications, or external effects make rollback unsafe, say so and define containment, reconciliation, or forward repair instead of promising “revert deploy.”

9. **Make a consumer-oriented decision.** Recommend `additive`, `versioned`, `adapter`, `deprecate`, or `hold` (or a precise combination), with rationale, residual unknowns, smallest evidence/test needed, and the product/engineering/consumer signoffs still required. Do not replace judgment with one opaque breakage score.

## Output contract

Lead with the recommendation and confidence in the baseline. Then provide, in this order:

1. **Change intent and baseline confidence** — sources/versions, observed versus assumed behavior, and decisive gaps.
2. **Compatibility matrix** — surface/change × consumer class, status (`compatible`, `breaking`, `unknown`), evidence, and migration burden.
3. **Strategy decision and developer friction** — chosen evolution path, rationale, SDK/docs/error/release-timing impact.
4. **Migration, communication, and rollout** — stages, owners, verification signals, stop conditions, support window, and safe recovery versus irreversible effects.
5. **Open questions/blockers** — residual risks and the smallest practical evidence or consumer test that would resolve each one.

For a narrow question, use a short verdict plus only the relevant rows and next action. For a consequential cross-consumer change, use the full artifact. Never imply that synthetic examples, expected tests, or proposed monitoring are observed results.

## Final check

- [ ] Both wire/schema and observable behavior were reviewed.
- [ ] Compatibility is scoped per consumer class, with `unknown` used where evidence is missing.
- [ ] SDKs, documentation, support windows, errors/events, and mixed-version behavior are represented where relevant.
- [ ] The recommendation contains a real migration and rollout decision, not an automatic version bump.
- [ ] Verification and stop conditions come from supplied policy/owners or remain explicitly to be agreed.
- [ ] Rollback claims account for state, events, notifications, and other irreversible effects.
- [ ] No API, test, telemetry, migration, or client result is claimed without evidence.
