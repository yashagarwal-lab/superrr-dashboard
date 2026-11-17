# Rajasthan Royals SupeRR Selector (Season 2) — Presentation & Media Scripts

**Author**: Yash Agarwal  
**Event**: Rajasthan Royals SupeRR Selector — Round 1  
**Deliverable**: Video Presentation Scripts, Social Media Content, and War Room Pitch Package  
**Official Handles to Tag**: `@rajasthanroyals` & `@unstop.world`

---

## 1. 60-Second Video Presentation Pitch Script (YouTube / Drive / Loom)

* **Target Length**: 60 seconds (145–160 words)
* **Tone**: Confident, analytical, executive sports-science delivery.
* **Setup**: Split screen or Picture-in-Picture showing your face alongside the [Interactive War Room Dashboard](file:///home/yashagarwal/Code/SuperRR/dashboard/index.html).

| Time | Visual / Screen Recording Cue | Spoken Voiceover Script |
|:---|:---|:---|
| **0:00 – 0:08** | Screen showing terminal executing `pytest test_pipeline.py` (13 green passes) transitioning to the 3D dark-mode dashboard header. | *"Most IPL auction analytics make a fatal error: they pick players who are permanently locked, or get deceived by surface-level run rates. Here is how we engineered an empirical, championship-ready clutch model for Rajasthan Royals."* |
| **0:08 – 0:20** | Cursor dragging across the Scatter Plot in Tab 1, highlighting Tim David's 195.55 SR and Abhishek Sharma's +6.63 WPA. | *"We ingested 200,987 deliveries across 883 matches, calibrating a ball-by-ball Win Probability Added model with an 89.5% AUC. Along the way, we isolated 5 hidden data anomalies — including 271 non-striker runouts and rain-revised overs."* |
| **0:20 – 0:35** | Clicking Tab 2 (Multi-Moment Radar Comparator), overlaying Jasprit Bumrah vs. Sufiyan Muqeem across 6 metric axes. | *"To solve the Baseline Penalty Fallacy, our Multiplicative Retention Ratio ($\kappa$) proves that elite players like Bumrah and Abhishek don't choke — their baseline is simply world-class."* |
| **0:35 – 0:48** | Navigating to Tab 3 (Auction War Room Board), toggling the BCCI Ineligibility banner and selecting Released Free Agent Nathan Ellis. | *"Crucially, while Pakistani bowlers rank high in raw international data, BCCI regulations make them ineligible for the IPL. We separated global statistical benchmarks from actual auction buys, targeting 56 confirmed released free agents."* |
| **0:48 – 1:00** | Clicking Tab 4 (Royals Clutch XI), showing the ₹113.6 Cr lineup with an aggregate 69.4 Clutch Rating, ending on the PDF report cover. | *"By securing Jonny Bairstow and Nathan Ellis to flank our retained core of Jaiswal and Parag, we built a 69.4 RPCS Starting XI within a ₹120 Cr cap. That is data-driven cricket reality."* |

---

## 2. 30–45 Second Viral Reel / Shorts Script (Instagram & TikTok)

* **Audio**: Upbeat, high-tech instrumental background track (low volume).
* **Format**: 9:16 Vertical video. Record your screen while talking into a lapel mic or camera.

* **[0:00 – 0:05] HOOK (Fast cut to terminal output)**  
  * *Text on screen*: "Why 99% of IPL Auction models are WRONG 🏏📉"  
  * *Voiceover*: *"If your IPL auction model recommends buying players Rajasthan Royals can't legally sign... your model is broken."*

* **[0:05 – 0:15] THE DATA MINEFIELD (Screen recording of `Rajasthan_Royals_SupeRR_Selector_Round1_Methodology_Report.md`)**  
  * *Text on screen*: "5 Hidden Data Traps ⚠️"  
  * *Voiceover*: *"We analyzed 200,987 deliveries across 883 matches for Rajasthan Royals' SupeRR Selector. We caught 34 rain matches where overs were recorded in legal balls, and 271 runouts where the non-striker was dismissed!"*

* **[0:15 – 0:30] THE WAR ROOM FIX (Screen recording of `dashboard/index.html`)**  
  * *Text on screen*: "Regulatory Realism ⚖️"  
  * *Voiceover*: *"While Sufiyan Muqeem and Mohammad Nawaz shine in global T20Is, BCCI policy excludes Pakistani players from the IPL auction. So we built two parallel engines: global mathematical benchmarks for the Unstop dropdown, and actionable auction free agents like Nathan Ellis and Jonny Bairstow for the RR War Room!"*

* **[0:30 – 0:40] THE STARTING XI (Zoom in on the Royals Clutch XI Simulator)**  
  * *Text on screen*: "RR 2027 Clutch XI • RPCS 69.4 🏆"  
  * *Voiceover*: *"The final squad? A 69.4 clutch rating Starting XI fitting inside the ₹120 Cr purse. Check the link in bio for the full interactive dashboard and PDF report!"*

---

## 3. High-Engagement LinkedIn Thought Leadership Post

```markdown
🏏 Can pure mathematics and forensic data science solve the IPL 2027 Auction?

For Round 1 of the Rajasthan Royals SupeRR Selector (Season 2), I analyzed all 200,987 deliveries across 883 T20 matches in the tournament data pack to build a multi-moment Win Probability Added (WPA) framework for clutch performance.

Here are the 4 core breakthroughs from our war room:

1️⃣ The Baseline Penalty Fallacy:
Traditional pressure metrics evaluate delta performance (Pressure Stat − Baseline Stat). This creates an unfair mathematical penalty for generational superstars:
- If a batter averages a 187 baseline SR (Abhishek Sharma) and strikes at 175 under pressure, a naive model flags them as "choking" (−12 SR).
- If a batter averages 115 and scores at 125, the naive model awards them a +10 "clutch boost"!
We resolved this using a Multiplicative Retention Ratio (κ = Press / Base), proving that Abhishek Sharma and Jasprit Bumrah maintain world-class output despite astronomical baselines.

2️⃣ Exposing 5 Critical Data Traps:
A naive data ingestion would have corrupted any player rating:
• The "Revised Overs" Column Quirk: In 34 rain-affected matches, columns recorded legal balls allotted (114, 90, 72) rather than decimal overs, breaking standard RRR formulas.
• Non-Striker Runouts: In 271 out of 600 run-outs (45.2%), the dismissed batter was the non-striker.
• Tilak Varma's tactical 'Retire Out' (Row 127,899) and 12 phantom deliveries in Match 48610 quarantined.

3️⃣ War Room Regulatory Realism:
While Sufiyan Muqeem (Econ 5.15) and Mohammad Nawaz rank in the global Top 10 across all international fixtures, BCCI policy precludes Pakistani players from the IPL auction.
We separated:
- Global Mathematical Benchmarks (for the Unstop dropdown rankings)
- Actionable Auction Target Pools (56 Confirmed Released Free Agents like Jonny Bairstow and Nathan Ellis, plus Global Scouting Steals like Taskin Ahmed).

4️⃣ Rajasthan Royals 2027 Starting XI Blueprint:
Accounting for RR's real-world 2026 acquisitions (Ravindra Jadeja and Ravi Bishnoi) alongside retained stars Yashasvi Jaiswal and Riyan Parag, our projected Starting XI achieves an aggregate 69.4 / 100 Clutch Rating within an optimized ₹113.6 Cr commitment (leaving ₹6.4 Cr surplus).

Explore the production-grade Interactive Dashboard and our 40-page technical methodology report below!

Interactive Dashboard: https://yashagarwal-lab.github.io/superrr-dashboard/
GitHub Repository: https://github.com/yashagarwal-lab/superrr-dashboard

Huge thanks to @rajasthanroyals and @unstop.world for this incredible challenge!

#RajasthanRoyals #SupeRRSelector #IPL2027 #SportsAnalytics #DataScience #CricketAnalytics #Python #MachineLearning
```

---

## 4. Twitter / X Deep-Dive Thread (6 Tweets)

* **Tweet 1 (Hook)**:  
  How do you pick the most reliable players under pressure for @rajasthanroyals?  
  I audited all 200,987 balls across 883 matches for #SupeRRSelector Round 1 with @unstop.world.  
  Here is how calibrated Win Probability + data forensics changed everything 🧵👇 [Attach Dashboard Screenshot]

* **Tweet 2 (Data Forensics)**:  
  Before modeling, we caught 5 hidden data quirks in the tournament dataset:  
  ⚠️ 34 rain matches had allotted balls (114, 90) stored in decimal overs columns  
  ⚠️ 45.2% of runouts dismissed the non-striker, NOT the striker  
  ⚠️ 12 phantom deliveries in Match 48610 quarantined.  
  13/13 unit tests passing!

* **Tweet 3 (Mathematical Breakthrough)**:  
  Why naive RRR ≥ 8.0 fails:  
  1. It discards 100% of 1st-innings deliveries (defending totals!).  
  2. It ignores wicket loss context.  
  We built a 4-archetype Leverage Index + calibrated logistic regression model (AUC 0.895, Brier 0.132) ensuring zero first-innings blindspots.

* **Tweet 4 (The Top 10 Dropdown Picks)**:  
  Top 10 Batters: Abhishek Sharma (#1), Jos Buttler, SKY, Phil Salt, Tim David, Yashasvi Jaiswal, Vaibhav Sooryavanshi, Travis Head, Virat Kohli, Prabhsimran Singh.  
  Top 10 Bowlers: Jasprit Bumrah (#1), Sufiyan Muqeem, Rashid Khan, Sunil Narine, Kuldeep Yadav, Mitchell Santner, Matheesha Pathirana, Mohammad Nawaz, Abrar Ahmed, Taskin Ahmed.

* **Tweet 5 (Auction Realism & BCCI Policy)**:  
  Regulatory realism matters: Pakistani stars rank high internationally, but BCCI policy precludes them from the IPL.  
  In RR's War Room, they serve as Statistical Benchmarks, while we target 56 Confirmed Released Free Agents (Nathan Ellis, Jonny Bairstow, Glenn Maxwell).

* **Tweet 6 (The Final XI & Links)**:  
  Result: A 69.4 RPCS Starting XI committing ₹113.6 Cr with a ₹6.4 Cr purse reserve.  
  Check out our live Interactive Dashboard & 40-page methodology report:  
  🔗 https://yashagarwal-lab.github.io/superrr-dashboard/  
  @rajasthanroyals @unstop.world #HallaBol #CricketTwitter

