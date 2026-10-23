# Consumer impact questions

Use only the smallest set that can change the compatibility or rollout decision. These are prompts for targeted investigation, not a mandatory questionnaire.

## Establish who depends on the surface

- Which internal, partner, public, webhook, event, batch, or generated-code consumers are known?
- What evidence identifies them: gateway logs, registry, support records, contracts, SDK telemetry, subscriber inventory, or owner confirmation?
- What time window, environment, sampling, and coverage limits apply to that evidence?
- Which consumers may be unobservable: cached clients, offline/batch jobs, self-hosted deployments, proxies, long-lived mobile/desktop versions, or indirect downstream users?
- Who owns each consumer class, and who can accept a migration or support-window decision?

Treat “no traffic observed” as scoped evidence, not proof of no consumers.

## Understand actual dependency

- Which operations, fields, errors, headers, events, orderings, timing, limits, and side effects does each class rely on?
- Are clients generated or hand-written? Do they reject unknown fields or enum values?
- Do they depend on undocumented behavior, examples, or SDK abstractions rather than the nominal contract?
- Which versions remain in use, and can they be updated remotely?
- What happens when old and new clients or producers/consumers coexist?
- Are there partner, contractual, regulatory, accessibility, localization, or support commitments that constrain timing?

## Size the migration burden

- Does a consumer need code, configuration, credentials/scopes, data, SDK, tests, or operational runbooks changed?
- Are before/after examples and failure modes clear enough for independent migration?
- Is a compatibility adapter, dual path, replay, backfill, or data transformation required?
- Who supplies SDK/generated-client releases, and how do consumers receive them?
- How long does adoption realistically take for long-lived or partner clients?
- What is the cost of operating both paths, and who owns that cost?

## Plan communication and support

- Where will the change be discoverable: reference docs, changelog, release notes, dashboard, email, partner channel, or SDK release?
- What exact behavior, error, authorization, timing, and rollback limitations must be documented?
- Which consumers need direct outreach or migration assistance?
- What dates, support window, escalation path, and exception policy have accountable owners approved?
- How will questions and migration defects be triaged without treating silence as adoption?

## Verify rollout and exit

- Can rollout be segmented by consumer, operation, version, tenant, or opt-in?
- Which contract, consumer, replay, mixed-version, load, or failure tests address the actual risk?
- Which adoption, error, latency, retry, duplicate, support, or business signals indicate harm?
- What user-supplied or owner-approved threshold pauses the rollout? If none exists, record it as a decision still required.
- Can code, data, events, notifications, and external effects all be reversed? If not, what containment, reconciliation, compensation, or rollforward is safe?
- What evidence permits retirement of the compatibility path, and who signs off?

## Resolve unknowns proportionately

For each material unknown, record:

1. the decision it blocks or could change;
2. the smallest practical evidence source or consumer test;
3. an owner;
4. a review point;
5. what result would change the strategy.

Do not invent numeric gates, force exhaustive research for a low-impact reversible opt-in, or delay an obvious hold when a high-impact breaking action lacks a consumer path.
