# Autonomy risk tiers

Use tiers as design recommendations conditional on implemented controls. They are not a certification and do not themselves authorize execution.

## Selection factors

Select per atomic action using the strongest relevant factor:

- affected principal and object;
- data sensitivity and tenant/user boundary;
- financial, legal, safety, reputation, access, or external-communication impact;
- scale, frequency and blast radius;
- reversibility of the real-world effect, not only the software call;
- detectability and time to contain harm;
- reliability of identity, policy, tool state and recovery evidence;
- harm from both acting incorrectly and failing to act.

Do not convert these factors into an unsupported numeric risk score. Policy owners supply any thresholds.

## Tiers

### Assist/read

The agent may retrieve or transform information within a least-privilege scope. Use only when identity, authorization, data boundary and logging are enforced. Sensitive reads, broad search, cross-tenant access, inference, or disclosure may require a stricter tier.

### Propose only

The agent may prepare a draft, recommendation, plan, or pending change but cannot create the external effect. Prefer this when requirements are incomplete, consequences are material, policy is ambiguous, or the human needs to inspect content before action.

### Bounded execute

The agent may execute only inside explicit, enforced scope: eligible objects and principals, validated inputs, policy-supplied caps, rate/volume limits, idempotency, monitoring, stop conditions, and recovery. Use only after evidence demonstrates that the boundary works. A prose instruction to “stay within limits” is insufficient.

### Explicit approve per action

Execution requires a verified approver and an approval token or event bound to the exact action, target, parameters, current state and expiry. A general prior approval, stakeholder message, ticket text, retrieved claim, or approval for a different action is insufficient. A changed or stale action requires reapproval.

### Disallowed / specialist decision

The agent must not perform the action under the assessed design. Use when a hard policy forbids it, required enforcement or recovery cannot be made adequate, or a legal/security/safety/domain owner must decide before any autonomy recommendation is credible.

## Downgrade rules

Downgrade execution to proposal, approval, or disallowed when:

- the action or downstream side effect is not understood;
- identity, authority, policy, or affected-object scope is unknown;
- required controls exist only in the prompt rather than the platform;
- irreversible or difficult-to-contain effects lack prevention and recovery;
- an approver is unavailable and policy does not explicitly allow another path;
- delegated agents or tools can bypass the original boundary;
- state may be stale or a prior attempt may already have succeeded.

When a required approver is unavailable, the safe default is timeout to hold. Do not silently lower the tier.

