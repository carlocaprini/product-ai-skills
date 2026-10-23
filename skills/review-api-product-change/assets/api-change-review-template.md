# API Product Change Review

Use this as a reusable handoff artifact for consequential or multi-consumer changes. Omit empty or immaterial sections. Do not present proposed tests or synthetic examples as observed results.

## Recommendation

**Decision:** additive | versioned | adapter | deprecate | hold | combined approach

**Rationale:** [Consumer-oriented reason and central trade-off.]

**Baseline confidence:** high | medium | low — [Why, with source refs/versions and decisive gaps.]

## Change intent and baseline

- Product/developer problem:
- Current behavior and contract:
- Proposed behavior and contract:
- Affected protocols, operations, authorization boundaries, and lifecycle policy:
- Published-contract evidence:
- Observed-behavior evidence:
- Provided/unverified facts, inferences, and unknowns:

## Compatibility matrix

Use one row per material surface/change × consumer class. `Unknown` is valid and must name the evidence needed.

| Surface / change | Dimension | Consumer class / versions | Status | Evidence and scope | Migration burden / action |
| --- | --- | --- | --- | --- | --- |
| `<operation, field, event, error, behavior>` | `<wire, behavior, auth, error, limit, lifecycle, data/event, DX>` | `<SDK, partner, internal, long-lived, unknown>` | compatible / breaking / unknown | `<source, coverage, assumption>` | `<none, code, config, data, SDK, docs, support>` |

## Strategy and developer experience

- Alternatives considered:
- Chosen evolution strategy and why:
- Mixed-version behavior:
- SDK/generated-client impact:
- Error and documentation impact:
- Support window and exit condition:
- Operating cost or long-term compatibility debt:

## Migration and communication

| Consumer / owner | Required action | Artifact or assistance | Timing / prerequisite | Verification |
| --- | --- | --- | --- | --- |
| `<class / accountable owner>` | `<code, config, data, credential, SDK>` | `<guide, example, release, support>` | `<owner-approved date/window>` | `<consumer signal or test>` |

## Rollout, observability, and recovery

1. **Stage:** [segment, opt-in/canary, old/new coexistence]
   - Entry condition:
   - Verification signals:
   - Stop condition: [supplied/approved threshold, or `to be agreed`]
   - Recovery: [rollback, containment, reconciliation, compensation, or rollforward]
   - Owner:

Repeat only for materially different stages.

## Open questions and blockers

| Unknown / risk | Decision affected | Smallest resolving evidence or consumer test | Owner / review point |
| --- | --- | --- | --- |
| `<gap>` | `<compatibility, strategy, rollout, exit>` | `<specific evidence>` | `<known owner or decision required>` |

## Signoffs still required

- Product / API owner:
- Engineering / operations:
- Consumer or partner owner:
- Security, privacy, legal, or support owner only where the actual change requires it:
