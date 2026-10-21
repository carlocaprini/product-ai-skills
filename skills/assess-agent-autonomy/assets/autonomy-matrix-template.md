# Autonomy matrix template

This is an optional handoff artifact, not the default answer format. Use it only when the user explicitly requests a reusable/full matrix, or when at least six materially different actions with different owners or control regimes require one. Otherwise use the compact form below and do not load or reproduce the full schema.

## Compact default

| Action | Tier | Decisive reason / unknown | Required control or next step |
| --- | --- | --- | --- |
| `<atomic action>` | `<tier>` | `<only what changes the decision>` | `<control, approval, recovery, or rollout step>` |

State shared controls, cross-action hazards, owner and rollout once after the table.

## Full handoff matrix

Use only the columns that materially affect the decision. Split compound actions into separate rows and omit empty or repetitive columns.

| Action | Principal / object | Data and consequence | Evidence / unknowns | Tier | Allowed scope | Approval | Enforced controls | Observability | Failure / retry / recovery | Rollout evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<atomic action>` | `<who acts on what>` | `<sensitivity, external effect, blast radius, reversibility>` | `<verified, provided/unverified — source, inferred, unknown>` | `<assist/read, propose only, bounded execute, explicit approve per action, disallowed/specialist>` | `<least-privilege objects, users, environment>` | `<owner, exact binding, expiry>` | `<policy checks, caps, validation, rate limits, idempotency>` | `<minimal logs, alerts, stop signal>` | `<prevention, reconciliation, retry rule, rollback/compensation/manual repair>` | `<shadow/proposal/bounded test and advance/retreat condition>` |

## Cross-action hazards

- Chaining or delegation:
- Shared credentials or privilege escalation:
- Stale state or approval:
- Aggregate rate/financial/data exposure:
- External effects that cannot truly be undone:

## Decision summary

- Allowed now:
- Conditional / approval required:
- Not yet safe:
- Missing control or owner decision:
- Smallest safe rollout step:
- Accountable owner and next review condition:
