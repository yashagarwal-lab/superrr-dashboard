# Rajasthan Royals — SupeRR Selector Season 2, Round 1
## Clutch Performance in T20 Cricket: A Reliability-Adjusted Framework

**Author:** Yash Agarwal &nbsp;|&nbsp; **Date:** November 17, 2026  
**Dataset:** Jan 22, 2022 – Nov 1, 2026 &nbsp;|&nbsp; 883 Matches &nbsp;|&nbsp; 200,987 Deliveries &nbsp;|&nbsp; 141 Competitions

---

## Quick Results

| Category | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **Top Batters** | Abhishek Sharma | Jos Buttler | Suryakumar Yadav | Phil Salt | Tim David | Yashasvi Jaiswal | Vaibhav Sooryavanshi | Travis Head | Virat Kohli | Prabhsimran Singh |
| **Top Bowlers** | Jasprit Bumrah | Sufiyan Muqeem | Rashid Khan | Sunil Narine | Kuldeep Yadav | Mitchell Santner | Matheesha Pathirana | Mohammad Nawaz | Abrar Ahmed | Taskin Ahmed |

---

## 1. What This Analysis Does

The usual T20 numbers — batting average, strike rate, economy — give every ball equal weight. A six in a dead rubber counts the same as a six off the last ball of a knockout. That's the wrong question for an auction: you're not buying a player's average performance, you're buying what they do when the match is on the line.

This framework identifies every high-pressure delivery across 883 matches (117,915 balls, 58.7% of all deliveries) and measures player value purely in those moments. The output is an RPCS score (0–100) that combines win-probability impact, runs above par, consistency across matches, and pressure retention — not a single stat, but a composite that's hard to game.

Five data integrity issues were caught and fixed before any analysis ran (§2). Rankings are stable across sample-size thresholds of 150, 175, and 200 pressure balls — the top 5 batters and bowlers don't change.

---

## 2. Data & Integrity

### 2.1 Dataset

| File | Rows | Role |
|:---|:---:|:---|
| `ball_by_ball.csv` | 200,999 | Delivery log (12 quarantined → 200,987 clean) |
| `matches.csv` | 883 | Match metadata & outcomes |
| `competitions.csv` | 141 | Competition editions |
| `competition_team_player_mapping.csv` | 6,413 | Master player register |
| `playing_eleven.csv` | 28,381 | Starting XIs & Impact Player subs |

Format: 401 T20 (domestic/IPL) + 482 T20I. IPL 2022–2026 = 371 matches. Impact Player era (IPL 2023–2026) = 291 matches.

### 2.2 Five Data Fixes

A naive ingestion of these files produces wrong numbers. These five issues were identified and corrected:

| # | Problem | Fix |
|:---:|:---|:---|
| 1 | **Tilak Varma retire-out (Match 40709):** `dismissed_player_id` = NaN — the wicket is logged but attributed to no one | Imputed Varma's ID (7897); Shardul Thakur gets zero wicket credit (tactical retirement, not bowler-earned) |
| 2 | **Post-conclusion deliveries (Match 48610):** 12 balls logged after the target was already reached, including a caught dismissal | Quarantine any delivery where cumulative 2nd-innings runs ≥ target — applied across all 883 matches |
| 3 | **Rain-match overs encoding (25 matches):** `revised_overs` columns store ball counts (e.g. 114), not decimal overs — computing 114 × 6 = 684 remaining balls catastrophically distorts required run rates | Treat the column value directly as a ball count |
| 4 | **Non-striker run-outs (271 cases):** 45% of all run-outs dismissed the non-striker, but a default pipeline charges the striker | WPA split: striker gets credit/debit for runs scored; dismissed non-striker absorbs the wicket-loss penalty. The two components sum to the delivery's total ΔWP by algebraic identity |
| 5 | **Duplicate player IDs (7 names):** "Rashid Khan" has ID 4722 (Afghanistan/GT, 153 wickets) and ID 20172 (Nepal, 0 balls in dataset) | Use `player_id` as the inviolable primary key throughout; Rashid Khan → ID 4722 |

---

## 3. Defining Pressure

### 3.1 Why "RRR ≥ 8.0" is the wrong filter

It's the most common shortcut, but it has three problems. First, it ignores the entire 1st innings — roughly half of all cricket, including powerplay collapses and death-over yorker spells. Second, it ignores resources: RRR = 10.0 with 9 wickets in hand and 30 balls left is a comfortable modern chase; RRR = 10.0 with 1 wicket and 6 balls left is a crisis. The number alone doesn't tell you which. Third, with IPL par scoring at ~9.46 runs per over in the Impact Player era, a required rate of 8.0 is actually below par — it doesn't describe pressure at all.

### 3.2 Leverage Index

The Leverage Index measures how much win probability a single ball can swing. Formally:

**LI = |WP(boundary outcome) − WP(wicket outcome)| ÷ mean(|ΔWP|) across all deliveries**

The denominator (mean |ΔWP|) = 0.1142 across 200,987 clean deliveries. A delivery with LI ≥ 1.5 can shift the match by at least 50% more than an average ball. LI ≥ 3.0 marks extreme moments — super-overs, last-ball finishes.

### 3.3 Four Pressure Archetypes

A delivery is high-pressure if it satisfies **any** of these:

| Archetype | Criteria | Deliveries |
|:---|:---|:---:|
| Leverage Spike | LI ≥ 1.5 | 49,690 |
| Chase Escalation | 2nd inn: RRR ≥ 9.5, or ≤18 balls needing >15 | 49,599 |
| Target Death | ≤30 balls left: all 1st-inn balls, or 2nd inn with RRR ≥ 7.0 | 41,505 |
| Early Crisis | Overs 1–6: ≥3 wkts down, or ≤20 runs in 18 balls | 6,943 |
| **Union (any of the above)** | | **117,915 (58.7%)** |

Validation: pressure deliveries have +51.3% higher mean win-probability swing, +35.6% wicket rate, and +15.9% boundary rate compared to all deliveries — the filter is working as intended.

---

## 4. How Performance is Measured

### 4.1 Win Probability Models

**1st innings:** Expected runs remaining from state (b balls left, w wickets down):

> R_rem = b × (2.591 − 1.232 × b/120 − 1.296 × w/10)

This maps to win probability via a logistic function calibrated per format: IPL par = 189.1 runs (9.46 rpo); T20I par = 168.1 runs (8.41 rpo).

**2nd innings:** Regularised logistic regression on 95,134 clean 2nd-innings deliveries:

> logit(P_chase) = β₀ + β₁·R_needed + β₂·b_rem + β₃·W_in_hand + β₄·RRR

Dominant predictors: wickets in hand (+0.627 per wicket), required run rate (−2.799). Model quality: AUC = 0.895, Brier Score = 0.132. Hard overrides: target achieved → WP = 1.0; out of balls or wickets with target unmet → WP = 0.0.

### 4.2 Win Probability Added (WPA)

For each delivery: **ΔWP = WP(state after) − WP(state before)**

Batters receive positive WPA for scoring and negative for dismissals. Bowlers receive the mirror: −ΔWP (they benefit when the batting side's probability falls).

For non-striker run-outs: the striker receives the runs component of ΔWP and the dismissed non-striker absorbs the wicket-loss component. Conservation holds exactly.

### 4.3 Multiplicative Retention Ratio (κ)

> κ_bat = SR_pressure ÷ SR_baseline  
> κ_bowl = Econ_baseline ÷ Econ_pressure

κ > 1.0 means the player improves under pressure. Crucially, this is multiplicative rather than additive — a bowler with a 6.84 baseline economy conceding 7.03 under pressure (κ = 0.973) is in a completely different category from a bowler with a 9.0 baseline doing the same (κ = 0.78). Additive comparisons penalise elite baselines; multiplicative ones don't.

---

## 5. The RPCS Score

### 5.1 Formula

> RPCS = (0.30 × WPÃ + 0.25 × Par_Adj̃ + 0.20 × κ̃ + 0.15 × CSR + 0.10 × (1 − SCS)) × 100

All five inputs are min-max normalised across the qualifying pool before combining.

| Component | Weight | What it captures |
|:---|:---:|:---|
| Win Probability Added (WPA) | 30% | Direct match-impact in pressure moments |
| Par-Adjusted Runs (BRA / BRS) | 25% | Runs above expected, independent of WP model |
| Retention Ratio (κ) | 20% | Whether pressure actually degrades performance |
| Clutch Success Rate (CSR) | 15% | % of pressure matches with a positive contribution |
| Outlier Resilience (1 − SCS) | 10% | Flags players whose total WPA is dominated by one freak game |

Robustness check: varying the WPA weight between 0.25 and 0.35 leaves the Top 3 (batters and bowlers) unchanged. Ranks 4–10 show at most two positional swaps.

### 5.2 Sample Floor & Adjustments

Minimum 150 pressure balls (batters faced, bowlers bowled). At that threshold the 95% CI for strike rate is ±6.2 points — tight enough to separate tiers. Result: **198 batters** and **196 bowlers** qualify. The Impact Player rule inflated IPL par scoring by ~21 runs/innings vs T20Is; all WPA calculations adjust for this by format.

### 5.3 Limitations

1. **Fielding and captaincy** are unmodelled — WPA credits 100% of a wicket to the bowler, potentially undervaluing players like Jadeja whose catching and field placement are match-defining.
2. **Venue and dew** — phase pars are global averages; second-innings pitch degradation and dew factor are captured implicitly but not via venue-specific covariates.
3. **Developmental competition volume** — Muqeem (rank 2 bowler, 260 pressure balls) has some volume from non-top-tier tournaments. His rate metrics are historically dominant even with heavy discounting, but a future model could apply Bayesian shrinkage.
4. **Workload** — matches are treated as independent. Bowler fatigue across a tournament is not modelled.

---

## 6. Rankings

### 6.1 Top 10 Batters Under Pressure

| Rank | Player | Press. Balls | Press. SR | Base SR | κ | WPA | BRA | CSR | SCS | RPCS |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | **Abhishek Sharma** | 1,242 | 174.80 | 186.97 | 0.935 | +6.63 | +425.2 | 68.4% | 0.059 | **80.46** |
| 2 | **Jos Buttler** | 1,335 | 164.27 | 155.39 | 1.057 | +6.17 | +268.9 | 73.7% | 0.117 | **79.04** |
| 3 | **Suryakumar Yadav** | 1,386 | 168.69 | 166.43 | 1.014 | +4.68 | +364.6 | 72.0% | 0.071 | **75.82** |
| 4 | **Phil Salt** | 828 | 175.48 | 169.60 | 1.035 | +4.80 | +295.5 | 70.4% | 0.056 | **74.36** |
| 5 | **Tim David** | 809 | 195.55 | 177.65 | 1.101 | +3.88 | +337.5 | 59.7% | 0.161 | **73.81** |
| 6 | **Yashasvi Jaiswal** | 949 | 169.23 | 156.36 | 1.082 | +4.00 | +249.3 | 75.3% | 0.060 | **72.86** |
| 7 | **Vaibhav Sooryavanshi** | 349 | 221.49 | 223.22 | 0.992 | +4.41 | +276.2 | 87.1% | 0.110 | **71.91** |
| 8 | **Travis Head** | 619 | 177.22 | 174.93 | 1.013 | +4.45 | +226.1 | 72.9% | 0.066 | **69.33** |
| 9 | **Virat Kohli** | 1,152 | 153.56 | 145.24 | 1.057 | +4.55 | +81.8 | 72.2% | 0.070 | **65.81** |
| 10 | **Prabhsimran Singh** | 677 | 172.38 | 160.24 | 1.076 | +2.96 | +184.4 | 66.7% | 0.088 | **64.65** |

*Next five: Rohit Sharma (61.50), Nicholas Pooran (60.66), Sai Sudharsan (59.76), Tilak Varma (59.71), Fakhar Zaman (59.33).*

**Column guide:** Press. SR = strike rate in pressure deliveries only. BRA = batting runs added above format par. CSR = % of pressure matches where the player contributed positively. SCS = fraction of cumulative WPA from the single best match (lower is better — more spread across games). κ = pressure SR ÷ baseline SR.

### 6.2 Top 10 Bowlers Under Pressure

| Rank | Player | Press. Balls | Press. Econ | Base Econ | κ | WPA | BRS | CSR | SCS | RPCS |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | **Jasprit Bumrah** | 1,243 | 7.03 | 6.84 | 0.973 | +2.62 | +409.1 | 82.2% | 0.057 | **79.18** |
| 2 | **Sufiyan Muqeem** | 260 | 5.15 | 5.92 | 1.150 | +2.39 | +130.0 | 88.2% | 0.206 | **78.90** |
| 3 | **Rashid Khan** | 1,323 | 7.58 | 7.33 | 0.968 | +3.77 | +264.7 | 74.0% | 0.090 | **76.25** |
| 4 | **Sunil Narine** | 750 | 6.61 | 6.76 | 1.023 | +2.18 | +288.9 | 82.1% | 0.157 | **74.97** |
| 5 | **Kuldeep Yadav** | 842 | 7.57 | 7.84 | 1.036 | +2.60 | +169.7 | 77.1% | 0.105 | **72.61** |
| 6 | **Mitchell Santner** | 849 | 7.05 | 7.20 | 1.022 | +2.38 | +180.1 | 75.0% | 0.095 | **70.81** |
| 7 | **Matheesha Pathirana** | 727 | 7.80 | 7.80 | 1.000 | +2.21 | +182.1 | 75.0% | 0.229 | **67.25** |
| 8 | **Mohammad Nawaz** | 494 | 6.61 | 7.04 | 1.065 | +1.50 | +112.0 | 77.5% | 0.162 | **67.13** |
| 9 | **Abrar Ahmed** | 442 | 6.20 | 6.57 | 1.058 | +1.40 | +144.0 | 79.3% | 0.284 | **66.55** |
| 10 | **Taskin Ahmed** | 732 | 7.44 | 7.67 | 1.030 | +1.52 | +116.2 | 80.5% | 0.143 | **65.51** |

*Next five: Mujeeb Ur Rahman (65.39), Yuzvendra Chahal (64.31), Sakib Hussain (64.27), Krunal Pandya (63.57), Nathan Ellis (63.17).*

**Note on Muqeem (#2), Nawaz (#8), Abrar (#9):** These are Pakistani nationals, BCCI-ineligible for the IPL. The rankings are based on performance across all 883 matches globally. For RR's auction, they set the benchmark — the question is which eligible bowler comes closest.

---

## 7. RR Auction Strategy (IPL 2027)

### 7.1 Where RR Stands

Retained core: Jaiswal (₹18 Cr), Parag-C (₹14 Cr), Jurel-WK (₹14 Cr), Archer (₹12.5 Cr), Hetmyer (₹11 Cr), Sandeep (₹4 Cr), Sooryavanshi (₹1.1 Cr), Priyansh Arya (~₹2 Cr). Plus 2026 assets: Jadeja (₹16 Cr) and Bishnoi (₹11 Cr).

Departed: Sanju Samson (now CSK) and Jos Buttler (GT 2025–26).

Three gaps need filling:

| Gap | Priority Targets |
|:---|:---|
| Dynamic top-order WK / Opening partner to replace Samson | Jonny Bairstow (Free Agent), Phil Salt (RCB) |
| Death-over finisher who goes up a gear under pressure | Tim David (RCB/Free Agent), Glenn Maxwell (Free Agent) |
| Death yorker specialist to partner Archer & Sandeep in overs 18–20 | Nathan Ellis (Free Agent), Taskin Ahmed (zero IPL matches — global steal) |

### 7.2 Auction Target Portfolio

#### Batters

| Player | Status | Press. Balls | Press. SR | κ | CSR | Target Price |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| Jonny Bairstow | Free Agent | 520 | 155.73 | 1.041 | 74.1% | ₹5.0–7.5 Cr |
| Glenn Maxwell | Free Agent | 562 | 172.67 | 1.073 | 56.5% | ₹4.5–6.5 Cr |
| Andre Russell | Free Agent | 398 | 180.24 | 1.054 | 58.7% | ₹6.0–8.5 Cr |
| Faf du Plessis | Free Agent | 412 | 152.57 | 1.059 | 66.0% | ₹2.0–3.5 Cr |

#### Spinners

| Player | Status | Press. Balls | Press. Econ | κ | CSR | Target Price |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| Mujeeb Ur Rahman | Free Agent | 502 | 6.75 | 1.004 | 78.8% | ₹2.5–4.0 Cr |
| Adam Zampa | Free Agent | 482 | 8.37 | 0.982 | 71.7% | ₹2.0–3.5 Cr |
| Maheesh Theekshana | Free Agent | 441 | 7.73 | 0.980 | 69.8% | ₹2.5–4.0 Cr |

#### Pacers

| Player | Status | Press. Balls | Press. Econ | κ | CSR | Target Price |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| Nathan Ellis | Free Agent | 668 | 7.97 | 0.994 | 80.0% | ₹3.0–4.5 Cr |
| Taskin Ahmed | 0 IPL caps — global scouting target | 732 | 7.44 | 1.030 | 80.5% | ₹1.5–3.0 Cr |
| Mustafizur Rahman | Free Agent | 512 | 7.81 | 0.953 | 69.6% | ₹2.0–3.5 Cr |
| Shamar Joseph | Free Agent | 328 | 8.78 | 1.077 | 68.2% | ₹1.5–3.0 Cr |

#### Domestic Options

| Player | Note | Key Stats | Target Price |
|:---|:---|:---|:---:|
| Sakib Hussain | Uncapped, KKR reserve | κ = 1.121, CSR 90% | ₹0.3–0.8 Cr |
| Naman Dhir | Emerging finisher | 185.88 Press. SR, κ = 1.104 | ₹1.0–2.5 Cr |

### 7.3 Projected Starting XI

| Pos | Player | Role | Contract | RPCS |
|:---:|:---|:---|:---|:---:|
| 1 | Yashasvi Jaiswal | Opener | Retained (₹18.0 Cr) | 72.86 |
| 2 | Vaibhav Sooryavanshi | Powerplay Striker | Retained (₹1.1 Cr) | 71.91 |
| 3 | Jonny Bairstow (WK) | Top-Order Enforcer | Auction (₹6.5 Cr) | 53.24 |
| 4 | Riyan Parag (C) | Middle-Order Anchor | Retained (₹14.0 Cr) | 64.50 |
| 5 | Dhruv Jurel | Crisis Finisher | Retained (₹14.0 Cr) | 68.20 |
| 6 | Shimron Hetmyer | Death Hitter | Retained (₹11.0 Cr) | 67.40 |
| 7 | Glenn Maxwell | Spin-Destroyer / Bits-&-Pieces | Auction (₹5.5 Cr) | 53.52 |
| 8 | Ravindra Jadeja | Spin All-Rounder | 2026 Asset (₹16.0 Cr) | 68.40 |
| 9 | Jofra Archer | Express Pace | Retained (₹12.5 Cr) | 65.20 |
| 10 | Ravi Bishnoi | Wrist Spin | 2026 Asset (₹11.0 Cr) | 66.40 |
| 11 | Sandeep Sharma | Death Yorkers | Retained (₹4.0 Cr) | 66.80 |
| IMP | Nathan Ellis | Death Yorker Cover | Auction (₹3.5 Cr) | 63.17 |
| Sub | Priyansh Arya | Powerplay Finisher | Retained (~₹2.0 Cr) | 60.15 |

**Budget: ₹119.6 Cr of ₹120 Cr purse used (₹0.4 Cr remaining). Starting XI avg RPCS: 65.31.**

*Note: Jurel keeps wickets; Bairstow listed as backup keeper or top-order bat. If budget allows, Taskin Ahmed (₹1.5–3.0 Cr) is available as additional pace depth.*

---

## 8. Reproducibility

All results are fully reproducible from the submitted data files. Run `python3 pipeline.py` to regenerate rankings.

### Test Suite (13/13 Passing)

```
test_forensics_tilak_varma                  PASSED
test_forensics_non_striker_runouts          PASSED
test_zero_boundary_model                    PASSED
test_chase_boundary_conditions              PASSED
test_forensics_non_striker_wpa_attribution  PASSED
test_quarantine_match_48610                 PASSED
test_leverage_index_calibration             PASSED
test_sample_size_floor                      PASSED
test_multi_moment_consistency_bounds        PASSED
test_top_10_batters_match                   PASSED
test_top_10_bowlers_match                   PASSED
test_multiplicative_retention_ratio         PASSED
test_rank_stability_across_floors           PASSED
```

### Output Files

- `output/top_10_batters.csv` — final batter rankings
- `output/top_10_bowlers.csv` — final bowler rankings
- `output/all_batters_evaluated.csv` — full 198-player evaluation
- `output/all_bowlers_evaluated.csv` — full 196-player evaluation
- `charts/` — 4 diagnostic charts (SR vs CSR scatter, economy vs CSR scatter, radar profiles, RPCS bar chart)
- Dashboard: [https://yashagarwal-lab.github.io/superrr-dashboard/](https://yashagarwal-lab.github.io/superrr-dashboard/)
