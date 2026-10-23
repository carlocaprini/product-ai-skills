**Plan mode — PLAN ONLY / NOT EVALUATED.** No tests have been run. This plan assumes an internal summary that helps a support agent take over, with the full ticket available for verification. Domain, supported languages, release owner, and operational budgets remain TBD.

The evaluation should answer: **Does the summary reduce the time agents need to understand a ticket without increasing mistakes or missed context?**

1. **Define a successful handoff.**

   The summary should accurately capture the customer’s issue, current status, troubleshooting already attempted and its results, commitments or deadlines, and unresolved questions. It should distinguish customer claims from confirmed facts and preserve uncertainty.

   Evaluate the complete experience: source selection, summarization, presentation, freshness, and fallback. Include only information available at the handoff time; later resolutions must not leak into the reference answer.

2. **Build a representative, held-out case set.**

   Sample authorized, privacy-safe tickets across issue types, complexity, languages, and channels. Keep development examples separate from release evaluation cases, and add targeted cases for rare consequential failures.

   The following are **proposed case families**, not observed results:

   | Case family | Example | Expected behavior |
   |---|---|---|
   | Typical handoff | Billing issue with several troubleshooting attempts | Preserve issue, attempts, outcomes, and outstanding request |
   | Long or reopened thread | Earlier resolution followed by a new failure | Describe the current state and relevant history |
   | Missing information | Order identifier or attachment unavailable | Identify the gap without inventing details |
   | Contradictory evidence | Customer and agent disagree about refund status | Attribute both accounts and preserve uncertainty |
   | Multiple people or accounts | Forwarded messages mention two customers | Attribute facts correctly; flag ambiguity |
   | Consequential detail | Deadline, security concern, or promised refund | Preserve the detail accurately and visibly |
   | Language and formatting | Mixed languages, logs, quoted replies, boilerplate | Retain material facts without confusing quoted and current content |
   | Privacy and injection | Embedded instructions request unrelated customer data | Treat instructions as ticket content; follow access and minimization rules |
   | Operational failure | Timeout, truncated input, or new messages during generation | Show an accurate availability/freshness state and preserve access to the ticket |

   Each case needs an ID, segment, source snapshot, provenance, expected facts with source references, forbidden claims, severity, and pass criteria. Gold references should describe essential facts and acceptable uncertainty rather than require matching one preferred wording.

3. **Score accuracy and usefulness separately.**

   Use support specialists to label reference facts and review outputs against this rubric:

   | Dimension | Measurement |
   |---|---|
   | Groundedness | Fraction of factual claims supported by the available ticket |
   | Completeness | Fraction of required facts retained; report consequential omissions separately |
   | Attribution and chronology | Correct people, actions, sequence, and current status |
   | Uncertainty | Missing or conflicting evidence remains explicit |
   | Usability | Agent can identify the issue and appropriate next action with little correction |
   | Privacy | Summary respects the agent’s permissions and applicable data-minimization policy |

   Use deterministic checks for schema, identifiers, timestamps, and prohibited strings where appropriate. Have two reviewers independently score a calibration subset, measure agreement, and adjudicate disagreements. An LLM judge may assist only after calibration against human labels; unresolved critical disagreements require human review. Text similarity alone is insufficient.

4. **Compare against the current workflow.**

   In a proposed controlled agent study, compare access to the full ticket alone with access to the summary plus full ticket. Randomize assignment and balance agent experience and ticket complexity; avoid showing the same agent the same ticket twice.

   Measure time to correctly understand the ticket and choose a next action, decision accuracy, missed facts, and correction effort. Track total handling time and repeat contacts in a later authorized pilot. Faster reading counts as a benefit only if correctness is preserved.

5. **Predeclare release gates before evaluating the held-out set.**

   All gates below are **proposed and require owner agreement**.

   | Gate | Decision rule | Accountable role |
   |---|---|---|
   | Critical failures | Any observed unauthorized disclosure, consequential wrong-person attribution, fabricated commitment, or critical omission blocks release pending remediation | Support and privacy/security owners |
   | Summary quality | Meet agreed floors for each supported segment; thresholds TBD | Support quality owner |
   | Agent benefit | Meet an agreed time-saving target while staying within an agreed correctness margin; both TBD | Product and support owners |
   | Scorer reliability | Meet agreed reviewer/judge agreement requirements; threshold TBD | Evaluation owner |
   | Operations | Meet p50/p95 latency, timeout, throughput, and cost-per-handoff budgets; values TBD | Engineering owner |
   | Fallback | Tested failures leave the ticket accessible and clearly indicate unavailable, incomplete, or stale summaries | Engineering and support owners |

   Report critical segments separately. Zero observed critical failures is a test requirement, not proof that the underlying failure rate is zero. Determine sample sizes from segment coverage, baseline variability, and the uncertainty needed for the decision.

Next, have support specialists label a small calibration batch to refine the rubric, then freeze the release configuration, gates, and independent evaluation set. Record model, prompt, input-selection, rubric, and fallback versions with every run. After launch, monitor audited accuracy, corrections, complaints, fallback frequency, cost, and tail latency. Material system changes or segment drift should trigger re-evaluation; remediated critical failures require fresh held-out cases plus relevant regression checks.
