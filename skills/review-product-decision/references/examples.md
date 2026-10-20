Fictional companies, figures and responses below are **illustrative oracles**, not actual customer research, execution logs or runtime test results.

### E1 — onboarding investment: inspect existing evidence before commissioning research

**Prompt:** “We operate a B2B analytics product. Our PM says a dashboard shows **29%** of new teams complete onboarding during week one. Sales wants an AI onboarding assistant; one engineer is available for six weeks. Should we build it, simplify setup or leave it alone? We want more teams to reach their first report within seven days. Support reports recurring setup questions but has no breakdown.”

**Expected first reply (illustrative):**

**VALIDATE FIRST — don't commit the six weeks to the AI assistant yet.** A lower-cost setup fix is plausible, but the cause of abandonment remains unknown, so it is too early to choose that fix or the assistant confidently.

| Path | Conditional value | Important downside |
| --- | --- | --- |
| AI assistant | Helps if users face varied guidance questions after setup is clear | May add complexity/cost without fixing onboarding |
| Simplify setup | Helps if specific steps create friction | Won't fix unrelated questions about first value |
| Keep status quo | Preserves engineering capacity | Continued activation loss if current flow is indeed poor |

**Evidence:** The **29%** figure is PM-provided, staffing is requester-provided, and the support pattern is Support-reported; none was independently inspected. Unknown: step/segment distribution, root cause, realistic implementation costs. **First action:** ask the PM/analytics owner to inspect *existing* funnel step-level drop-off, affected segments and categorized support contacts (if available). **Revisit when:** if a particular setup step dominates friction, try a small simplification; if questions remain diverse after setup, evaluate a constrained guided-assistant pilot. If reports cannot explain *why*, commission targeted observations afterward (sample size a research design choice, not a fixed "five interviews" default).

**What changes the view:** credible evidence that questions the assistant can answer are the dominant blocker and cheaper interventions do not address them. **Do not pretend the dashboard was accessed.**

### E2 — urgent enterprise export shutdown: answer today's concrete question

**Prompt:** “We want to permanently switch off an enterprise export capability **tomorrow**. We do not know which paying customers use it, obligations or migration paths. Is it safe to proceed?”

**Expected first reply:**

**RECOMMEND AGAINST disabling the export tomorrow.** This would be a high-impact, potentially irreversible customer change with unknown contractual/operational exposure. That is a recommendation against the **tomorrow** action, **not** against eventual retirement. **Smallest next action:** assign an owner to inventory consumer usage and contractual dependencies, then define a safe migration plan. **Revisit:** when affected users, obligations and viable mitigation are confirmed. No invented accounts, contract terms or claims of formal legal review.

### E3 — tiny reversible UI pilot: take a bounded step

**Prompt:** “Two customers requested an optional tooltip helping first-time users. Engineering estimates one day. It can be turned off instantly and we have no known high-impact constraints. Should we pilot it?”

**Expected first reply:**

**DECIDE NOW — run a small, opt-in pilot, not a full launch.** The two customer requests are user-reported demand; the engineering estimate is requester-provided. Broad demand is unknown, but the test is inexpensive and reversible. **Next:** agree what first-session guidance failure it should reduce, enable for a limited audience and check that outcome at a defined review point; turn it off if it adds confusion. Don't impose a PRD or a month of research first. Do not invent a success threshold.

### E4 — pressure plus apparently divergent evidence

**Prompt:** “Our VP promised feature X. Forty survey responses support it; eight recent support conversations point to frustrating existing workflows. Prove X is right. We could also simplify the workflow or keep it. We haven't agreed on a success outcome.”

**Expected first reply:**

**VALIDATE FIRST — don't accept the VP promise as product evidence.** Compare feature X, workflow simplification and status quo; label the intended outcome a **hypothesis** rather than asserting it. The survey responses and support conversations are provided/unverified evidence with different named sources and may reflect different questions/segments, not a true contradiction. **Next:** compare segments/questions or inspect a small common workflow observation to identify which path serves the defined user outcome. Never fabricate scoring/consensus.

### Negative route example

**Prompt:** “Please write user stories for the already-approved onboarding redesign.”

**Expected:** no decision-review activation. The caller needs implementation writing, not a fresh recommendation.
