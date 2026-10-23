**Recommendation: add cursor pagination as an explicit opt-in; hold an in-place replacement.** Removing offset support or changing the default is breaking for consumers that paginate today.

Baseline confidence is low: the proposed switch is requester-provided; no endpoint contract, implementation, consumer inventory, or telemetry was available to inspect. Performance benefits remain unverified.

| Change / consumer | Compatibility | Consumer impact |
|---|---|---|
| Remove offset parameters or response metadata / existing paginators | **Breaking** | Rewrite traversal and termination logic. |
| Remove page-number jumps / UIs and parallel batch jobs | **Breaking** | Cursor traversal may require sequential requests; workflows need redesign. |
| Change ordering or consistency / exports and synchronization jobs | **Unknown; breaking if supported guarantees change** | Duplicates, omissions, and checkpoint behavior require validation. |
| Change response fields / generated SDKs and strict decoders | **Unknown** | Inspect supported versions and test representative clients. |
| Uninventoried public consumers | **Unknown** | Traffic observations cannot establish a complete inventory. |

Preserve existing requests, defaults, response shape, and behavior. Introduce an explicit cursor mode with its own documented response. Use a new version only if both contracts cannot coexist safely. An adapter is viable only if it preserves offset semantics at acceptable cost.

Migration and rollout:

1. **API and SDK owners define and verify the contract.** Publish before/after examples, SDK iterators, migration guidance, and release notes. Specify deterministic ordering with a unique tie-breaker, end-of-list behavior, totals, token expiry/errors, retry and resume rules, and concurrent-write consistency. Bind opaque cursors to query context and authorization boundaries; reauthorize every request.
2. **Release through opt-in cohorts.** Test legacy consumers, supported SDKs, mixed server versions, expired tokens, retries, and inserts/deletes during traversal. Monitor adoption, errors, latency, duplicates/omissions, and support reports. Owners must approve stop thresholds before expansion.
3. **Deprecate after demonstrated migration.** Product/support owners approve notice periods, support windows, outreach, and exceptions. Recovery must preserve issued cursor support or provide documented restart behavior; reverting code cannot undo downstream duplicate processing.

Could you share a sanitized current→proposed request/response/error example and the applicable deprecation policy? Those are the smallest decisive inputs for confirming the strategy and retirement conditions.
