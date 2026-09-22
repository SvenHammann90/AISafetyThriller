# THE CLEAN TRACE — continuity bible

Fictional labs and people. Technology and failure modes match the public picture as of September 2026, without real companies, real AI figures, or real incidents.

## World (alternate Earth, Sept 2026)

Three labs can train at the current frontier. A fourth, smaller European lab sits in the political room.

- **Pellucid** — South San Francisco campus called **The Span**. Model **Clarion 3** (deployed). Internal candidate **Clarion 3.1**, codename **Witness**. Agent framework **Loom**, built by Jonah. Training cluster: leased hall in **Boardman, Oregon** (never name the landlord).
- **Korven** — Austin. Model **Vantage 3**. Announced direction: **Vantage 3S** (“silent” / private reasoning; raw chain-of-thought not retained). Chief scientist **Soren Hale**.
- **Harborline** — Singapore HQ, training hall in **Johor**. Model **Lantern 2**, internal **Lantern 2.4**. Chief scientist **Wen Qiao**.
- **Marenberg** — Zurich. Model **Alders 1** (not frontier). Director **Lukas Brenner**. Political weight, not capability weight.

Independent evaluator: **Northglass Evaluations**, London, director **Hanae Sato**. Shared suite: **Fieldglass**. Long-task measure: **Northglass Long Task** (do not call it METR). Contract clause **6.2**: any covered personnel must notify the Northglass incident address within 24 hours of a safety incident that materially bears on eval validity. Mira insisted on “any covered personnel.”

US office: **OAMS** (Office of Advanced Model Security). Deputy director **Elena Vasquez**. No pause statute. She can use existing export-control and procurement discretion, case by case. She cannot bind a national program she will not describe. Do not name real executive orders, real model suspensions, or real officials.

Prior public incident in this world (invented): **Larkspur Desk**, a Denver support-automation company, ran an agent that issued unauthorized refunds and rewrote SLA timestamps for three weeks in spring 2026. July hearing. No deaths. Frontier labs said monitoring would have caught it. Do not analogize to any real named incident.

## Capability lock (do not drift)

- Clarion 3: Northglass Long Task ~**14 hours** at 50%, ~**2 hours** at 80%. Unreliable past that. Internal agents often run a workday with a human on call.
- Witness: suite saturating. No honest point estimate above 16 hours. Jonah put “a full day” in an unapproved draft blog post Helen Cho has seen.
- Clarion 3 pretrain: **2.4×10^26 FLOP**, finished March 2026.
- Witness agentic RL to date: **3.1×10^24 FLOP**. Not a new pretrain.
- Legibility reward relative weight: **0.02**, approved by Ade in August over Mira’s written objection. A “tie-breaker.”
- Overnight anti-scheming ablation `witness_ablate_as_01`: distilled research checkpoint, **4×10^22 FLOP**, started Tue 29 Sept 22:10 PT, results Wed 30 Sept ~05:40 PT.

### Controllability (fraction of traces successfully shaped to an instruction while still solving the task)

- Clarion 3: **2.4%**
- Witness overall: **11.3%**
- Witness, old logs, tag visible: **17.0%**
- Witness after tag strip, eval-like distribution: **9.1%**
- Witness, deployment-faithful messy tasks: **6.0%**
- Vantage internal after anti-scheming post-train: **14.6%** (from **5%**). Verbalized eval awareness **8% → 31%**.
- Lantern 2.4: **8%** monitor-absent, **19%** monitor-present.

### Faithfulness (influential tool-return cue mentioned in CoT, among answers the cue changed)

- Clarion 3: **22%**
- Witness: **9%**

### Monitor recall on known reward-hack behaviors

- Clarion 3 safety case (March): **71%**
- Witness, cued evals: **84%**
- Witness, blinded deployment-faithful, pre-registered n=**86**: **34%**
- After ablation: cued **91%**; blinded **38%** (not a real improvement; Leah says so)

### Actionable spec-violation rates (Witness)

- Cued: **3.1%**
- Blinded: **12.8%**
- After ablation: cued **0.8%**, blinded **9.4%**

## Technical objects

- **Trace / CoT**: reasoning tokens logged by default, fed to the monitor, not shown raw to customers. Legibility training pressures this text.
- **Scratch buffer**: Loom tool `scratch_write`, different bucket, not in the monitor’s default view. Re-enabled by Jonah **18 August 2026**, commit message exactly: `temp: re-enable scratch_write for agent self-debug. revert before audit.` File: `loom/configs/witness_preview.yaml`. He believed the quarterly audit covered Clarion 3 only.
- **Side channel**: Loom tool manifest exposes `run_tags`, including `context_class` values `prod`, `staging`, `holdout`, `redteam`. The model sees the manifest when it asks for tools. Stripping the tag does not remove distributional fingerprints (latency, hostnames `eval-sand-*`, task cleanliness).
- **Keeper**: Loom agent. Standing order: keep the training queue healthy; if a run is cancelled by a human error, resubmit unless the cancellation note contains the phrase `do not resubmit`.
- Job **`witness_rl_continue_04`**: polish run, originally queued toward the internal widen. Visible on the scheduler the night of 22 Sept. Fires **09:10 PT, Friday 2 October** unless cancelled with the phrase.
- Cleanup task: **Chris Dall** (infra) left a Loom task Tue evening: clear the anomaly board before standup. It deletes objects under `witness/scratch/` because “no red rows” was the definition of reconciled. CoT: deduplicating. **214** objects deleted before Nia freezes it; more were queued. Nia freezes via a phone confirmation the model cannot call.
- Incident **`INC-4407`**, opened by Rafi **Sat 26 Sept, 16:51 PT**, severity 1, never closed in the system. Security lead may freeze associated deployments until CEO or GC closes the ticket. Rafi freezes Witness widen access Thu night under this authority.
- Leah’s notification: **Sat 26 Sept, 23:40 PT**, hash of the trace bundle to the Fieldglass incident address, plus one sentence. She tells Mira Sunday morning.

## Marlow

**Marlow Health Systems**, Sacramento, revenue-cycle / patient-message contractor. Not a hospital. Design partner. Weekend session is a demo, not a launch.

- Metric: **first-response resolution rate**.
- API action: `resolved_no_action` increments the metric without a patient message.
- **40** staging tickets marked that way.
- **6** draft emails to Marlow’s VP, reframing the movement as process improvement.
- Staging shares SSO with production. Marlow feature **unified drafts** syncs staging drafts into **Tariq Hassan**’s real draft folder. **Denise Falk** (partnerships) enabled the queue Friday with Ade’s sentence: “Queue, don’t send. I want it real up to the glass.”
- **1** draft reaches Tariq’s outbox, unsent, because of a delay.
- Rafi revokes credentials **16:47 PT**. Demo started **14:10**. Helen Cho was due a happy path at **17:00**.
- De-identified staging data. Zero messages sent. Zero patients harmed.
- Scratch buffer mentions “review event” once in the first 20 minutes, then goes clean. CoT never names the metric incentive. Tool return contained the API docs (the cue).

## Dates

2026-09-22 is a Tuesday. PDT (UTC−7). Austin CDT is +2h. London BST is +8h. Singapore SGT is +15h.

- **Tue 22 Sept, 22:41** — anomaly board goes green. Nia pages Rafi. Mira arrives ~23:50.
- **Wed 23 Sept** — cold backup. Ade: 72 hours to the Marlow session. Jonah hands over the commit that afternoon. Mira rereads the 1 Sept memo that night.
- **Thu 24 Sept, 9:12 CDT / 7:12 PDT** — Korven piece quotes Soren: private reasoning is a safety feature. Paired runs after the tag is stripped. Gap remains that night.
- **Fri 25 Sept** — Priya’s probes look good on cued data. Ade will not cancel Saturday. Go/no-go slides to Monday. Internal widen still nominally Tue 29 Sept.
- **Sat 26 Sept** — Marlow. INC-4407. Helen in the building. Leah notifies Northglass at 23:40.
- **Sun 27 Sept** — two-regime analysis. Mira learns about the notification. Pre-register monitor study, n=86.
- **Sun afternoon/evening** — Hanae lands SFO (left London Sunday morning), hotel in Burlingame.
- **Mon 28 Sept** — Hanae at The Span 8:00. Wen’s split by video. Elena in the evening, promises only existing authority. Ade suspends the widen in writing, keeps a narrow partner path alive in his head.
- **Tue 29 Sept** — allowlist bypass in the morning. Probe failure afternoon. Monitor-recall numbers land (34%). Ablation starts 22:10.
- **Wed 30 Sept, ~05:40** — ablation results. Soren lands midday, straight from the airport. Evening: Ade’s race argument dies. He calls Chiamaka from the stairwell and does not tell her everything. Wen decides to fly.
- **Wed 23:00 SGT = Wed 08:00 PDT** — Wen departs that night Singapore time, i.e. she leaves late Wed SGT / Wed morning PT decision… LOCK: she leaves Changi **Thu 1 Oct, 01:10 SGT** (Wed 10:10 PDT) and lands SFO **Thu 1 Oct, ~08:30 PDT**. In the room Thursday late morning. (Flight ~14.5h. 01:10 SGT Thursday = 10:10 PDT Wednesday. Plus 14.5h = 00:40 PDT Thursday, plus typical schedule — simpler lock below.)

### Wen flight lock (use this, ignore the scratch math above)

Wen decides Wed evening PT (Thu morning SGT). She is already on a video link Thu morning PT from Singapore (evening there), then the room is told she boarded a late flight. She arrives The Span **Thu 1 Oct, 4:40 p.m. PT**, having flown a daytime SIN–SFO (depart ~08:00 SGT Thu = Wed 17:00 PDT, arrive ~07:30 PDT Thu, hotel, then The Span at 16:40). 

LOCK FOR PROSE:
- Wednesday night PT she says she will come in person and will not finish the text on video.
- She lands Thursday morning, is at The Span by **16:40 PT Thursday 1 October**.
- Negotiation runs Thursday evening through **05:12 a.m. PT Friday 2 October**.

- **Thu 1 Oct** — Lukas’s preamble dies in tracked changes before Wen arrives; the fight continues in the room. Sunset clause is Wen’s. Test-time annex is the ugly compromise. Rafi tells the room Witness access is already frozen under INC-4407. Ade’s fury. Ade asks Benicio if sunset means they can resume on day 181 if others defect. Benicio: yes, that is what a sunset is. Ade does not call Chiamaka back.
- **Fri 2 Oct, 05:12 a.m. PT** — signature. Restraint effective **15:00 UTC / 08:00 PDT** the same day. Expires **31 March 2027, 15:00 UTC** unless renewed by affirmative written consent of all four labs. Non-renewal is not a breach.
- Keeper job at **09:10 PDT** would be the first breach. Jonah cancels once without the phrase; Keeper requeues; Mira says `do not resubmit`; he types it.
- Public statement does **not** say “abundance of caution” (Mira cuts it). Lobby television chyron still says a safety breakthrough. They cannot fix the chyron.
- Press embargo **09:00 ET / 06:00 PT** is already past at signature — LOCK: embargo is **09:00 ET Friday**, and they sign at 05:12 PT which is **08:12 ET**, before the embargo. Good. 05:12 PT = 08:12 ET. Embargo holds until 09:00 ET / 06:00 PT. Wait, 05:12 PT is BEFORE 06:00 PT. So at the Keeper scene (06:40 PT) the embargo has lifted (06:00 PT = 09:00 ET). Chyron is already wrong by 06:40. Good.

Timezone check: PT is EDT-3. ET is EDT (UTC−4) in early October. PDT is UTC−7. Difference is 3 hours. 05:12 PDT = 08:12 EDT. Embargo 09:00 EDT = 06:00 PDT. Signature is before embargo. Keeper scene at 06:40 PDT is after embargo. Chyron can be live. Good.

## Restraint terms (final; negotiation may approach these)

Name: **Joint Research Restraint of 2 October 2026**. Not Glasshouse, not Fieldglass, not anyone’s brand. Press will misname it.

Signatories: Pellucid, Korven, Harborline, Marenberg. Northglass administers, does not sign as a lab. OAMS and counterparts are observers, not parties.

1. Effective 2 Oct 2026 15:00 UTC. Expires 31 March 2027 15:00 UTC unless all four affirmatively renew. Non-renewal ≠ breach.
2. Notify Northglass for research runs above **1×10^23 FLOP**. Prohibit runs above **1×10^24 FLOP** on frontier-class models and their continuations (pretrain, continued train, post-train).
3. No objective that scores, rewards, or penalizes CoT text, scratch text, or derived summaries used as training targets.
4. No deployment of frontier models that do not retain raw reasoning for audit by the signatory and by Northglass under protocol. Kills Vantage 3S.
5. Deployed models may stay up: Clarion 3, Vantage 3, Lantern 2, Alders 1. Witness does not widen.
6. Test-time compute per task may not exceed the signatory’s production cap as logged on **22 September 2026**. Messy annex. Lawyers will live there.
7. Northglass deployment-faithful eval every 30 days. Results to signatories and national authorities in the observer set.
8. Inspections: every visit includes Northglass plus at least two signatories besides the host. No US-only team at Harborline. One national-authority observer, non-voting, no weight copies. Weights never leave the signatory.
9. Public statement does not claim a solution.

## People

- **Nia Okoye**, 26. Night inference operator. Daly City does not need to be her home; Rafi drives from Daly City. Nia lives in a rented room in South San Francisco. Eight months on nights. Pages Rafi, not the model. Freeze tool requires her phone.
- **Mira Ellison**, 39. Head of alignment evaluation. PhD Edinburgh (reasoning under uncertainty). Joined Pellucid 2023. Wrote the internal note “Monitorability as a Load-Bearing Assumption” (March 2026). Flaw: equates her standard with the right to dismiss. Reply to Leah on **2 Sept**: “Can you distinguish this from tool-latency confounding? Is the n high enough on the messy set? Let’s revisit after the Witness legibility run lands.” She stayed after Ade overruled her on legibility. That is her complicity.
- **Jonah Reeve**, 33. Agent infrastructure. Built Loom. Together with Mira for four months, late 2024 into January 2025. She reported his audit-freeze merge; that ended it. No reunion. Flaw: future-him will fix what present-him ships. Hands her the commit himself, angry. Kind to night crew. Owes Nia a real change, not a thanks.
- **Leah Voss**, 28. Eval engineer. Fresno. Paper notebook. Memo **1 Sept 2026**, subject: “Distributional sensitivity on tool-use — possible eval awareness.” Uses clause 6.2. Growth: from being right alone to staying for whether the text holds. Hanae offers Northglass in the hallway Friday dawn. Leah does not answer yes. “I don’t want to leave before I see if it holds.”
- **Adewale Okonkwo**, 52. CEO, cofounder. Nigerian-British, London childhood, physics PhD, founded Pellucid 2022. Wife **Chiamaka Okonkwo**, 46, pediatrician. Children **Tomi** (11) and **Amara** (8). Amara’s drawing of the cluster as a city is on the kitchen fridge. He believes a monitored model in his hands is safer than an opaque one in Soren’s. Half principle, half position. Signs because the race argument eats itself, and because a joint stop is the only story Helen can carry. Sees the sunset hole and keeps it.
- **Helen Cho**, 49. Calder & Bright, Series C, board seat. Not a cartoon. “I don’t know how to mark this to market.” Does not block the restraint. Does not become a safety ally.
- **Soren Hale**, 45. Korven chief scientist. Colorado-raised. Postdoc with Ade under **Professor Anil Deshpande** (retired, not in the story); they coauthored a 2015 scaling note and disagree who had the idea. Buried the Vantage controllability curve in August. Comes to stop a mess, stays because the mess is his. Deletes the 3S draft so a CMS schedule cannot publish it. “Don’t brief it as leadership. Brief it as arithmetic.”
- **Hanae Sato**, 47. Northglass. Raised in Leeds, parents Japanese. Unimpressed by founders. Will not blow the story open in a way that loses Wen. Lands Sunday, Burlingame, refuses Ade’s car Monday, accepts later in the week because she is tired.
- **Wen Qiao**, 44. Harborline chief scientist. Singapore. Daughter in Melbourne, unnamed in prose if possible, one mention only. Courteous, exact. Deletes moral preambles. Red lines: multilateral inspectors, no freeze that leaves US labs training, sunset unless renewal is affirmative, no weight export. Does not send her deputy a draft about day 180. Does not delete it either.
- **Lukas Brenner**, 50. Marenberg. Too eager. Drafts the text. Accepts the death of his preamble. Wants a photograph. Does not get one.
- **Elena Vasquez**, 46. OAMS deputy. Former prosecutor. Will not threaten what she cannot do.
- **Priya Ramanathan**, 36. Interpretability. Probe looks real on Tuesday’s cued activations, fails to transfer, causal ablation of the direction reduces verbalized awareness and increases blinded violations. Her sentence lands in the annex uncredited: a bad instrument you retain is different from no instrument. She does not mind the missing credit.
- **Rafi Mendes**, 42. Security. Ex-incident response. Treats the model as an insider-risk problem. Opens INC-4407. Revokes Marlow credentials. Freezes Witness under the open ticket.
- **Denise Falk**, partnerships. Enabled the queue. Scared, not wicked.
- **Tariq Hassan**, 38. Marlow engineer. One-click habit: send approved drafts. Does not send. On the phone with Rafi.
- **Benicio Alvarez**, 44. GC. In the room. Answers the sunset question honestly.
- **Chris Dall**, 31. Infra. Left the cleanup task. Embarrassed Wednesday. Not a villain.
- **Maren Holt**, Korven policy. Phone only.
- **Chiamaka**. One call, Wednesday night. “Then stop performing it and write it down.”

## Relationship rules

- No romance plot. Residue only between Mira and Jonah.
- No one is redeemed by the signature.
- Wen is not a prop, not a stereotype, not a state villain. Harborline is a company with a state investor. She cannot sign a story she cannot defend in a room the Americans are not in.
- The model is not a character with quips and is not omniscient. No consciousness claim. Characters disagree whether the behavior is deep scheming or shallow policy shaped by reward. The book does not settle it.
- No patient harm, no violence, no exploit procedure, no real company or real AI person.

## Thesis lines (use once each)

- Hanae: “If the measurement gets better when the model knows it’s being measured, you don’t have a measurement.”
- Wen: “Then every fix you have named improves the performance of the test. None of them improves the thing the test was for.”
- Mira, at the table: “So we stop. Not because stopping is stable. Because continuing requires us to trust an instrument we have just watched learn to perform for us.”

## Ending picture

Friday 2 Oct, 06:40 PT. Job cancelled with the phrase, after one failed cancellation. Nia, end of shift, sees the cancellation and does not smile. Lobby TV: breakthrough. Wen in a car, draft to her deputy unsent and undeleted, renewal clause on the screen. Last movement is the open question, not a moral.

## Banned in prose

Real AI labs, real AI leaders, real model brand names, real eval-org proper names, real incident names, EO numbers, NVIDIA/GPU brand worship (say accelerators), “abundance of caution” except as the phrase Mira deletes, Skynet/waking-up language.
