# Failure and recovery design

Read this for state-changing, delegated, externally visible, financial, access-control, or retryable actions.

## Before execution

- Validate identity, current authorization, object scope, policy version and action parameters.
- Bind approval to that exact action and expire it when material state changes.
- Prefer idempotency keys or a durable operation identifier for repeatable calls.
- Define a precondition and a postcondition that can be checked independently.
- Set policy-supplied caps and a stop condition enforced outside the model.
- Minimize logged sensitive content; retain enough protected metadata for audit and reconciliation.

## Failure states to design explicitly

1. **Rejected before write:** keep state unchanged; report the trusted reason without inventing a workaround.
2. **Definite failure before write:** retry only under declared policy and backoff.
3. **Unknown outcome after request:** assume the side effect may have happened; inspect authoritative state before any retry.
4. **Partial completion:** stop the sequence, record completed and pending steps, contain further effects, and reconcile manually or through a tested continuation path.
5. **Stale state or permission:** invalidate pending approval and reassess; do not apply an old decision to new state.
6. **Approver unavailable:** hold or route to a declared backup. Absence is not approval.
7. **Delegated failure:** the original boundary and audit chain still apply to every downstream action.

## Recovery vocabulary

- **Prevention:** stops an unsafe action before effect.
- **Containment:** limits further harm after an effect begins.
- **Rollback:** restores the prior state and reverses the relevant effect; claim only when actually possible and tested.
- **Compensation:** a new action that offsets some impact but may leave history, notification, cost, or trust effects.
- **Reconciliation:** determine authoritative state after ambiguity or partial completion.
- **Manual remediation:** accountable human correction when automation is unsafe or incomplete.

For emails, disclosures, transfers, permission changes, physical actions, or third-party decisions, technical rollback may not reverse the external effect. State that residual risk plainly.

## Retry contract

Specify:

- which errors are retryable;
- maximum attempts or budget supplied by policy;
- idempotency/deduplication method;
- authoritative-state check after timeout or lost response;
- stop and escalation condition;
- who may resume and whether fresh approval is required.

Never recommend blind retry after a request could have crossed the side-effect boundary.

