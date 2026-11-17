# Rajasthan Royals — SupeRR Selector Season 2, Round 1
## Clutch Performance in T20 Cricket: A Reliability-Adjusted Framework

**Author:** Yash Agarwal &nbsp;|&nbsp; **Date:** November 17, 2026
**Dataset:** January 22, 2022 – November 1, 2026 &nbsp;|&nbsp; 883 Matches &nbsp;|&nbsp; 200,987 Deliveries &nbsp;|&nbsp; 141 Competitions

---

## Quick Results

| Category | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **Top Batters** | Abhishek Sharma | Jos Buttler | Suryakumar Yadav | Phil Salt | Tim David | Yashasvi Jaiswal | Vaibhav Sooryavanshi | Travis Head | Virat Kohli | Prabhsimran Singh |
| **Top Bowlers** | Jasprit Bumrah | Sufiyan Muqeem | Rashid Khan | Sunil Narine | Kuldeep Yadav | Mitchell Santner | Matheesha Pathirana | Mohammad Nawaz | Abrar Ahmed | Taskin Ahmed |

---

## 1. Executive Summary

Standard T20 metrics treat every delivery equally. This framework measures what players do *when the game is on the line* — 117,915 high-pressure deliveries identified across 883 matches.

**Core methodology:**
1. **Dynamic Leverage Index (LI ≥ 1.5) + 4 Pressure Archetypes** — identifies pressure deliveries across both innings.
2. **Win Probability Models** — 1st-innings polynomial expected-runs model; 2nd-innings logistic model (AUC = 0.895, Brier = 0.132).
3. **Win Probability Added (WPA)** — delivery-level value attribution; handles 271 non-striker run-outs and 1 tactical retire-out.
4. **Multiplicative Retention Ratio (κ)** — eliminates baseline bias that penalises already-elite players.
5. **RPCS composite score (0–100)** — synthesises WPA, par advantage, κ, consistency rate, and outlier resilience.

Top 5 rankings are identical at sample-size thresholds of 150, 175, and 200 pressure balls.

---

## 2. Data & Integrity Audit

### 2.1 Dataset

| File | Rows | Role |
|:---|:---:|:---|
| `ball_by_ball.csv` | 200,999 | Primary delivery log (12 quarantined → 200,987 clean) |
| `matches.csv` | 883 | Match metadata & outcomes |
| `competitions.csv` | 141 | Competition editions & format |
| `competition_team_player_mapping.csv` | 6,413 | Master player register |
| `playing_eleven.csv` | 28,381 | Starting XIs & Impact Player subs |

Format: 401 T20 (domestic/IPL) + 482 T20I. IPL seasons 2022–2026 (371 matches). Impact Player era: 291 matches (IPL 2023–2026).

### 2.2 Five Forensic Cleanups

| # | Issue | Fix |
|:---:|:---|:---|
| 1 | **Tilak Varma retire-out (Match 40709):** `dismissed_player_id = NaN` — phantom wicket | Imputed Varma's ID (7897); bowler Shardul Thakur receives zero wicket credit |
| 2 | **Post-conclusion deliveries (Match 48610):** 12 balls logged after target was reached | Quarantine all deliveries where cumulative 2nd-innings runs ≥ target, applied globally |
| 3 | **Revised overs encoding (25 rain matches):** columns store ball counts, not decimal overs | Treat columns directly as ball allotments (e.g. 114 = 114 balls, not 684) |
| 4 | **Non-striker run-outs (271 cases):** default pipeline penalises the striker | WPA split: striker gets runs component, dismissed non-striker absorbs wicket penalty |
| 5 | **Duplicate player IDs (7 names):** e.g. "Rashid Khan" has ID 4722 (AFG/GT, 153 wkts) and ID 20172 (Nepal, 0 balls) | Use `player_id` as inviolable primary key throughout; Rashid Khan → ID 4722 |

---

## 3. Pressure Definition

### 3.1 Why RRR ≥ 8.0 Fails

Three problems: (1) ignores the entire 1st innings; (2) ignores resources — RRR = 10.0 with 9 wickets and 30 balls is easy, with 1 wicket and 6 balls it's a crisis; (3) in the Impact Player era, IPL par is ~9.46 rpo, so RRR = 8.0 is comfortable.

### 3.2 Leverage Index

$$LI_t = \frac{|WP(\text{boundary}) - WP(\text{wicket})|}{\overline{\Delta WP}}$$

where $\overline{\Delta WP} = 0.1142$ across all 200,987 clean deliveries. LI ≥ 1.5 → High Pressure; LI ≥ 3.0 → Extreme Pressure.

### 3.3 Four Pressure Archetypes

| Archetype | Criteria | Deliveries |
|:---|:---|:---:|
| Leverage Spike | LI ≥ 1.5 | 49,690 |
| Chase Escalation | 2nd inn: RRR ≥ 9.5, or ≤18 balls needing >15 | 49,599 |
| Target Death | ≤30 balls left: all 1st inn, or 2nd inn with RRR ≥ 7.0 | 41,505 |
| Early Crisis | Overs 1–6: ≥3 wkts down, or ≤20 runs in 18 balls | 6,943 |
| **Union** | | **117,915 (58.7%)** |

Pressure deliveries show +51.3% mean |ΔWP|, +35.6% wicket rate, and +15.9% boundary rate vs. all deliveries — confirming the definition is well-calibrated.

---

## 4. Performance Measurement

### 4.1 Win Probability Added (WPA)

$$\Delta WP_t = WP(\text{State}_{t+1}) - WP(\text{State}_t)$$

Batters receive positive WPA for scoring, negative for dismissals. Bowlers receive $WPA_{bowl} = -\Delta WP_t$.

### 4.2 1st-Innings Win Probability

$$R_{rem}(b, w) = b \cdot \left(2.591 - 1.232 \cdot \frac{b}{120} - 1.296 \cdot \frac{w}{10}\right)$$

Mapped to win probability via a logistic function calibrated per format: IPL par = 189.1 runs (9.46 rpo); T20I par = 168.1 runs (8.41 rpo).

### 4.3 2nd-Innings Win Probability

Regularised logistic regression on 95,134 clean 2nd-innings deliveries:

$$\text{logit}(P_{chase}) = \beta_0 + \beta_1 R_{needed} + \beta_2 b_{rem} + \beta_3 W_{in\,hand} + \beta_4 \cdot RRR$$

Key coefficients: wickets in hand (+0.627/wkt), required run rate (−2.799). AUC = 0.895, Brier = 0.132. Hard overrides: target achieved → WP = 1.0; out of balls/wickets → WP = 0.0.

### 4.4 Non-Striker WPA Equity

For non-striker run-outs/retire-outs:
- Striker receives: $\Delta WP_{striker} = WP(\text{runs, no wicket}) - WP_{pre}$
- Dismissed non-striker absorbs: $\Delta WP_{dismissed} = WP_{post} - WP(\text{runs, no wicket})$

The two components sum exactly to the delivery's total ΔWP (algebraic identity).

### 4.5 Multiplicative Retention Ratio (κ)

$$\kappa_{bat} = \frac{SR_{pressure}}{SR_{baseline}}, \qquad \kappa_{bowl} = \frac{Econ_{baseline}}{Econ_{pressure}}$$

κ > 1.0 means the player *improves* under pressure. Avoids penalising elite baselines that are hard to surpass (e.g. Bumrah's κ = 0.973 against a 6.84 baseline economy is vastly different from a mediocre baseline).

---

## 5. Fair Comparisons & Adjustments

**Sample floor:** Minimum **150 pressure balls** (batters faced / bowlers bowled). At 150 balls, the 95% CI for strike rate is ~±6.2 points. Result: **198 batters** and **196 bowlers** qualify.

**Era calibration:** Impact Player rule inflated IPL par by ~21 runs/innings vs. T20Is. All WPA equations adjust for this.

**Competition tier:** The 150-ball floor naturally filters developmental-only players. Players with material developmental volume are flagged in their rankings note.

---

## 6. Top 10 Rankings

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

*Reserves: Rohit Sharma (61.50), Nicholas Pooran (60.66), Sai Sudharsan (59.76), Tilak Varma (59.71), Fakhar Zaman (59.33).*

**Metric guide:** Press. SR = strike rate under pressure. BRA = batting runs added above par. WPA = win probability added. CSR = % of pressure matches with positive contribution. SCS = fraction of total positive WPA from single best match (lower = more consistent). RPCS = composite score (0–100).

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

*Reserves: Mujeeb Ur Rahman (65.39), Yuzvendra Chahal (64.31), Sakib Hussain (64.27), Krunal Pandya (63.57), Nathan Ellis (63.17).*

> [!NOTE]
> **Pakistani players (Muqeem #2, Nawaz #8, Abrar #9)** are BCCI-ineligible for IPL. Rankings reflect the global mathematical truth; for RR auction purposes they serve as performance benchmarks only.

---

## 7. RPCS Formula & Limitations

### 7.1 Composite Score

$$RPCS = \left(0.30 \cdot \widetilde{WPA} + 0.25 \cdot \widetilde{Par\_Adj} + 0.20 \cdot \widetilde{\kappa} + 0.15 \cdot CSR + 0.10 \cdot (1 - SCS)\right) \times 100$$

All terms are min-max normalised across the qualifying pool.

| Component | Weight | Rationale |
|:---|:---:|:---|
| Win Probability Added (WPA) | 30% | Most direct measure of match impact |
| Par-Adjusted Runs (BRA/BRS) | 25% | Raw run-rate advantage, independent of WP mechanics |
| Retention Ratio (κ) | 20% | Does pressure actually affect this player? |
| Clutch Success Rate (CSR) | 15% | Penalises boom-or-bust profiles |
| Outlier Resilience (1 − SCS) | 10% | Guards against single-match flukes |

Varying the WPA weight from 0.25 to 0.35 leaves the Top 3 (both batters and bowlers) unchanged.

### 7.2 Known Limitations

1. **Fielding & captaincy** — WPA assigns 100% of a wicket to the bowler; exceptional catches and direct hits are not separately credited.
2. **Pitch & dew variance** — ERA and phase pars are global; venue-specific covariates are not modelled.
3. **Developmental competition tier** — Muqeem (Rank 2, 260 balls) has some developmental volume; a future model could apply Bayesian shrinkage priors.
4. **Injury & fatigue** — matches are treated as independent events; bowler workload is not modelled.

---

## 8. RR IPL 2027 Auction Strategy

### 8.1 Retained Core & Tactical Voids

- **Retained:** Jaiswal (₹18.0 Cr), Sooryavanshi (₹1.1 Cr), Parag-C (₹14.0 Cr), Jurel-WK (₹14.0 Cr), Hetmyer (₹11.0 Cr), Archer (₹12.5 Cr), Sandeep (₹4.0 Cr), Priyansh Arya (~₹2.0 Cr); Jadeja & Bishnoi (2026 assets)
- **Departed:** Sanju Samson (now CSK, 2026), Jos Buttler (GT 2025–26)

| Void | Need | Priority Targets |
|:---|:---|:---|
| Dynamic top-order WK / Opening partner | Replaces Samson | Jonny Bairstow (Free Agent), Phil Salt (RCB) |
| Death-over finisher | Power closer who amplifies under pressure | Tim David (RCB), Glenn Maxwell (Free Agent) |
| Death yorker specialist | Partners Archer & Sandeep in overs 18–20 | Nathan Ellis (Free Agent), Taskin Ahmed (Global Steal) |

### 8.2 Auction Target Portfolio

#### Tier 1 — Batters

| Player | Status | Press. Balls | Press. SR | κ | CSR | Target Price |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **Jonny Bairstow** | Free Agent | 520 | 155.73 | 1.041 | 74.1% | ₹5.0–7.5 Cr |
| **Glenn Maxwell** | Free Agent | 562 | 172.67 | 1.073 | 56.5% | ₹4.5–6.5 Cr |
| **Andre Russell** | Free Agent | 398 | 180.24 | 1.054 | 58.7% | ₹6.0–8.5 Cr |
| **Faf du Plessis** | Free Agent | 412 | 152.57 | 1.059 | 66.0% | ₹2.0–3.5 Cr |

#### Tier 2 — Spinners

| Player | Status | Press. Balls | Press. Econ | κ | CSR | Target Price |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **Mujeeb Ur Rahman** | Free Agent | 502 | 6.75 | 1.004 | 78.8% | ₹2.5–4.0 Cr |
| **Adam Zampa** | Free Agent | 482 | 8.37 | 0.982 | 71.7% | ₹2.0–3.5 Cr |
| **Maheesh Theekshana** | Free Agent | 441 | 7.73 | 0.980 | 69.8% | ₹2.5–4.0 Cr |

#### Tier 3 — Pacers

| Player | Status | Press. Balls | Press. Econ | κ | CSR | Target Price |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **Nathan Ellis** | Free Agent | 668 | 7.97 | 0.994 | 80.0% | ₹3.0–4.5 Cr |
| **Taskin Ahmed** | Global Steal (0 IPL matches) | 732 | 7.44 | 1.030 | 80.5% | ₹1.5–3.0 Cr |
| **Mustafizur Rahman** | Free Agent | 512 | 7.81 | 0.953 | 69.6% | ₹2.0–3.5 Cr |
| **Shamar Joseph** | Free Agent | 328 | 8.78 | 1.077 | 68.2% | ₹1.5–3.0 Cr |

#### Tier 4 — Domestic Gems

| Player | Status | Key Metric | CSR | Target Price |
|:---|:---|:---|:---:|:---:|
| **Sakib Hussain** | Uncapped (KKR reserve) | SR κ = 1.121, CSR 90% | 90.0% | ₹0.3–0.8 Cr |
| **Naman Dhir** | Emerging finisher | 185.88 Press. SR, κ = 1.104 | 66.7% | ₹1.0–2.5 Cr |

### 8.3 Projected RR IPL 2027 Starting XI

| Pos | Player | Role | Contract | RPCS |
|:---:|:---|:---|:---|:---:|
| 1 | Yashasvi Jaiswal | Pressure Opener | Retained (₹18.0 Cr) | 72.86 |
| 2 | Vaibhav Sooryavanshi | Hyper-Striker (221 SR) | Retained (₹1.1 Cr) | 71.91 |
| 3 | Jonny Bairstow | WK / Boundary Enforcer | Auction (₹6.5 Cr) | 53.24 |
| 4 | Riyan Parag (C) | Middle-Order Anchor | Retained (₹14.0 Cr) | 64.50 |
| 5 | Dhruv Jurel (WK) | Crisis Anchor / Finisher | Retained (₹14.0 Cr) | 68.20 |
| 6 | Shimron Hetmyer | Death Power Closer | Retained (₹11.0 Cr) | 67.40 |
| 7 | Glenn Maxwell | Spin Destroyer | Auction (₹5.5 Cr) | 53.52 |
| 8 | Ravindra Jadeja | Spin All-Rounder | 2026 Asset (₹16.0 Cr) | 68.40 |
| 9 | Jofra Archer | Express Pacer | Retained (₹12.5 Cr) | 65.20 |
| 10 | Ravi Bishnoi | Wrist-Spin Squeeze | 2026 Asset (₹11.0 Cr) | 66.40 |
| 11 | Sandeep Sharma | Death Yorker Operator | Retained (₹4.0 Cr) | 66.80 |
| IMP | Nathan Ellis | Death Yorker Specialist | Auction (₹3.5 Cr) | 63.17 |
| Sub | Priyansh Arya | Powerplay Enforcer (197 SR) | Retained (~₹2.0 Cr) | 60.15 |

**Total commitment: ₹119.6 Cr** (₹120 Cr purse; ₹0.4 Cr remaining) | **Starting XI avg. RPCS: 65.31**

---

## 9. Reproducibility

### Test Suite (13/13 Passing — 7.82s)

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
test_top_10_batters_unstop_match            PASSED
test_top_10_bowlers_unstop_match            PASSED
test_multiplicative_retention_ratio         PASSED
test_rank_stability_across_floors           PASSED
```

### Submission Checklist

- [x] Top 10 Batters: `output/top_10_batters.csv`
- [x] Top 10 Bowlers: `output/top_10_bowlers.csv`
- [x] Full evaluations: `output/all_batters_evaluated.csv` (198 players), `output/all_bowlers_evaluated.csv` (196 players)
- [x] Dropdown 1:1 match verified against `competition_team_player_mapping.csv`
- [x] 4 diagnostic charts in `charts/`
- [x] 13/13 automated tests passing
- [x] Rank stability verified at 150 / 175 / 200 ball thresholds
- [x] Model: AUC 0.895, Brier 0.132
- [x] 5 forensic cleanups documented and unit-tested
- [x] Dashboard: [https://yashagarwal-lab.github.io/superrr-dashboard/](https://yashagarwal-lab.github.io/superrr-dashboard/)
