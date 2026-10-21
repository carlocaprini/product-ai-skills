# Product decision edge cases

Open this reference only when a decision needs deeper distinction between feasibility, evidence, reversal or the value of more information.

## Hard constraints versus preferences

**Hard blocker:** The user supplies a concrete non-negotiable requirement or an action depends on an unverified critical authorization; do not rank its supposed benefits against noncompliance. Mark the proposed path BLOCKED / conditional on verification. Do not independently invent a legal obligation, policy interpretation or permission.

**Preference:** Strategy fit, delivery speed, team preference, cost or effort may be compared as soft criteria. A preference becomes a binding constraint only when the decision owner explicitly says so.

## Decision horizons

Separate the precise immediate action from the long-term product direction:
- **Act tomorrow?** A dangerous irreversible action may merit RECOMMEND AGAINST now.
- **Eventually retire/change the feature?** It may merit VALIDATE FIRST as a different, subsequent decision.
One response can mention both, but put the actual requested action in the lead verdict; don't label both as equal "modes" for the same choice.

## Information and research economy

Use the cheapest decision-changing source already available: segmentation of existing telemetry, prior support/feedback, known contractual dependencies, or operational incident history. Suggest new user observation only if existing signals cannot distinguish paths or the observed *why* is absent. A five-person interview sample may generate qualitative hypotheses; it cannot prove a population-level rate. A cheap reversible pilot may be more informative than a lengthy upfront validation.

## Evidence quality and comparability

**Observed/source-backed:** personally inspected source, known date and coverage; still may be biased.
**Provided/unverified:** stated in the request but not independently inspected. Preserve the named source exactly: Sales-reported, Support-reported, stakeholder assertion, customer-survey response, or requester-provided. Use **user-reported** only when the evidence actually came from users/customers.
**Inferred:** theory derived from observed/reported context; identify falsifier.
**Unknown:** absent/conflicting data likely to affect choice; do not treat as zero.

Apparent contradictions require checking **population/segment, user job/question, measurement window, sample, method and outcome**. A survey about desired features and interviews about workflow friction may both be true.

## Reversibility includes externalities

Code rollback alone does not reverse customer disruption, trust, consumed capacity, contract or data impacts. Conversely, an opt-in feature that is readily disabled and inexpensive may justify a time-boxed pilot despite incomplete market research.

## Outcome-changing check

Choose one observation or experiment that could cause an *actual different decision*; specify owner and checkpoint. Avoid vanity metrics, arbitrary numerical thresholds, or obligatory RICE/Kano/ICE scoring. Separate known stakeholder-approved thresholds from a suggested starting hypothesis.
