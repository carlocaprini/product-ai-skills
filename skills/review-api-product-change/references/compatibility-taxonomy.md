# API compatibility taxonomy

Use this reference to classify material changes consistently. It is a decision aid, not a substitute for protocol documentation, consumer tests, or an organization-specific lifecycle policy.

## Compatibility status

Assign status per change and consumer class, never globally by default.

### Compatible

Available evidence supports the consumer continuing to operate correctly within a stated scope and version range. Record what was checked. “Additive,” “optional,” or “schema-valid” is not sufficient by itself.

### Breaking

The consumer must change, loses access, receives invalid data, produces a materially different result, or violates a supported expectation. A break may be wire-visible, semantic, operational, or contractual.

### Unknown

Evidence is missing, coverage is unclear, behavior is undocumented, consumers are unobservable, or mixed-version operation has not been established. Unknown is not a softer form of compatible. Name the smallest evidence that could resolve it.

## Change dimensions

| Dimension | Examples to inspect | Commonly missed consumer effect |
| --- | --- | --- |
| Wire / schema | operation, field, type, requiredness, enum, cardinality, serialization | strict parsers, generated clients, unknown-enum handling |
| Behavior | defaults, null vs missing, ordering, filtering, pagination, consistency, side-effect timing | correct parsing but wrong business result |
| Auth / permission | scope, identity, tenancy, token, ownership | unchanged endpoint becomes inaccessible or over-broad |
| Error semantics | status/code, error body, retryability, partial success | clients retry, suppress, or surface the wrong outcome |
| Performance / limits | latency, payload, quotas, timeouts, rate/size caps | timeouts, memory pressure, throttling, batch failure |
| Lifecycle | version support, deprecation, sunset, preview/stable status | unsupported long-lived clients or surprise retirement |
| Data / event semantics | meaning, ordering, delivery, duplication, replay, retention | duplicate effects, missed events, invalid reconciliation |
| Documentation / DX | examples, SDKs, generated code, discoverability, release notes | nominally compatible change still imposes hidden migration work |

## Semantic checks that schema diffs miss

- Field becomes present with a new default, or `null`, missing, and empty values change meaning.
- Default sort order changes, destabilizing first-item logic, pagination, or caches.
- Pagination token format or validity changes while the response shape remains stable.
- Status or error code, message structure, partial-success behavior, or retryability changes.
- Idempotency keys, deduplication windows, retry guidance, or side-effect timing change.
- Rate, size, timeout, consistency, precision, timezone, or timestamp behavior changes.
- Authorization scope or tenant/resource ownership rules change.
- A new enum value reaches a generated or exhaustive client.
- Event/webhook ordering, at-least-once delivery, replay, signature, retry, or dead-letter behavior changes.
- An additive field changes a downstream mapping, validation rule, signature, hash, cache key, or UI assumption.

## Worked synthetic example

This example is fictional. It is an illustrative review, not evidence that an API, telemetry source, migration, or client test was inspected or run.

`GET /v1/orders` currently returns oldest-first results. A proposal adds optional `status` and changes the default to newest-first. A generated SDK is known to ignore unknown fields; one fulfillment client takes the first result as the next order to process; partner consumers are not inventoried.

| Change | Consumer | Status | Reason / action |
| --- | --- | --- | --- |
| Optional `status` | Known generated-SDK client | compatible within stated SDK behavior | Confirm the actual supported SDK versions and document the field. |
| Optional `status` | Unknown partner parsers | unknown | Identify strict decoders or run a representative consumer test; do not generalize from the known SDK. |
| Default ordering | Fulfillment client | breaking | Its first-result behavior changes. Preserve oldest-first by default and add an explicit sort option, or migrate the client before changing the default. |
| Default ordering | Uninventoried partners | unknown | Keep existing behavior while inventory and opt-in migration proceed. |

A low-disruption recommendation is an additive sort parameter with the old default, explicit new behavior, before/after examples, and a consumer test for order-dependent clients. A later default change needs observed adoption, partner communication, an agreed support window and owner-defined stop criteria. The new field does not make the combined proposal “backward compatible.”

## Protocol-specific prompts

### REST / HTTP

Check methods and paths, parameters, content types, status codes, headers, caching, conditional requests, pagination, idempotency, redirects, and request/response compatibility. A new optional response field is not universally safe for strict decoders.

### GraphQL

Check nullability, field and argument removal, enum expansion, default arguments, resolver behavior, authorization, errors/partial data, persisted queries, introspection policy, and client-code generation. Schema availability does not prove resolver semantics.

### gRPC / Protobuf

Check field numbers and reuse, wire type, presence/default semantics, unknown fields, enums, oneof membership, method/service changes, generated-code versions, deadlines, status codes, and mixed old/new deployments. Never reuse removed field numbers.

### Events / webhooks

Check event identity/version, payload, meaning, ordering, delivery guarantee, deduplication key, retries, replay, retention, signature/authentication, subscriber lag, and producer/consumer deployment order. Schema compatibility alone does not establish safe processing.

## Evolution strategy trade-offs

| Strategy | Fits when | Main cost or risk | Exit condition to define |
| --- | --- | --- | --- |
| Backward-compatible addition | consumers can ignore or opt into behavior safely | hidden semantic or strict-parser break | adoption and old-path retirement evidence |
| Dual behavior / read / write | old and new consumers must coexist temporarily | divergence, reconciliation, operating cost | migration coverage and convergence check |
| Compatibility adapter | translation can isolate consumers from a change | adapter ownership, fidelity, extra failure mode | consumer migration or durable ownership decision |
| Opt-in / feature flag | behavior can be segmented safely | flag drift, mixed-state testing | explicit graduation/removal rule |
| Controlled migration | consumers can move on a coordinated schedule | support and coordination burden | named owners and verified completion |
| Deprecation / sunset | old behavior has a defined supported exit | abandoned or long-lived consumers | support window and exception policy |
| New version | contract must intentionally diverge | duplicated docs/SDKs/operations; split adoption | version support and retirement plan |
| Hold | decisive evidence or a safe path is absent | delayed value | smallest blocking evidence or design change |

Do not call a data or event migration reversible merely because application code can be redeployed. Distinguish code rollback, state rollback, compensation, reconciliation, containment, and rollforward.
