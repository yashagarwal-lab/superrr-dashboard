# Rajasthan Royals SupeRR Selector (Season 2) — Empirical Pressure Analytics & IPL 2027 Auction War Room

[![CI](https://github.com/yashagarwal-lab/superrr-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/yashagarwal-lab/superrr-dashboard/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/tests-58%20passed-10b981.svg)](tests/)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-3b82f6.svg)](pyproject.toml)
[![Live War Room](https://img.shields.io/badge/live-interactive%20war%20room-e11d48.svg)](https://yashagarwal-lab.github.io/superrr-dashboard/)
[![PDF Report](https://img.shields.io/badge/report-executive%20pdf%20(2.7MB)-8b5cf6.svg)](Rajasthan_Royals_SupeRR_Selector_Round1_Report.pdf)
[![License](https://img.shields.io/badge/license-MIT-gray.svg)](LICENSE)

An empirical sports-science and machine learning analytics platform identifying the most reliable players under high-leverage pressure across **200,987 deliveries** (883 matches, 141 competitions) and optimizing **Rajasthan Royals' IPL 2027 Auction Strategy**.

* **Live Interactive War Room**: [https://yashagarwal-lab.github.io/superrr-dashboard/](https://yashagarwal-lab.github.io/superrr-dashboard/)
* **Executive PDF Methodology Report**: [`Rajasthan_Royals_SupeRR_Selector_Round1_Report.pdf`](Rajasthan_Royals_SupeRR_Selector_Round1_Report.pdf)
* **Full Markdown Methodology**: [`Rajasthan_Royals_SupeRR_Selector_Round1_Methodology_Report.md`](Rajasthan_Royals_SupeRR_Selector_Round1_Methodology_Report.md)
* **Video Presentation & Social Pitch Scripts**: [`docs/presentation_scripts.md`](docs/presentation_scripts.md)

---

## 🏛️ Executive Summary & Core Results

Traditional cricket metrics (raw strike rate, economy rate, and boundary counts) collapse in high-leverage situations due to context insensitivity and the **Baseline Penalty Fallacy** (penalizing elite players whose natural baseline is extraordinarily high). 

This platform introduces the **Rajasthan Pressure Clutch Score (RPCS)**, a mathematically rigorous framework combining:
1. **Multiplicative Retention Ratio ($\kappa$)**: Measures performance retention under pressure relative to baseline without penalizing elite operators.
2. **Win Probability Added ($WPA$)**: Calibrated logistic model across 95,134 chase deliveries ($AUC = 0.895$).
3. **Par-Adjusted Value ($BRA$ / $BRS$)**: Baseline Runs Added (batters) and Baseline Runs Saved (bowlers).
4. **Clutch Success Rate ($CSR$)**: Empirical percentage of positive-leverage outcomes.
5. **Sample Consistency ($SCS$) & Gini Volatility**: Down-weighting high-variance single-match wonders.

### Unstop Official Top 10 Rankings

| Rank | Top 10 Batters (Unstop) | RPCS | $\kappa$ | WPA | CSR | Top 10 Bowlers (Unstop) | RPCS | $\kappa$ | WPA | CSR |
|:---:|:---|:---:|:---:|:---:|:---:|:---|:---:|:---:|:---:|:---:|
| **1** | **Abhishek Sharma** | **80.46** | 0.935 | +6.63 | 68.4% | **Jasprit Bumrah** | **79.94** | 1.055 | +5.31 | 79.4% |
| **2** | **Jos Buttler** | **79.04** | 1.057 | +6.17 | 73.7% | **Sufiyan Muqeem** 🇵🇰* | **78.36** | 1.258 | +2.02 | 87.5% |
| **3** | **Suryakumar Yadav** | **75.82** | 1.014 | +4.68 | 72.0% | **Rashid Khan** | **77.62** | 0.992 | +4.24 | 74.0% |
| **4** | **Phil Salt** | **74.36** | 1.035 | +4.80 | 70.4% | **Mohammad Nawaz** 🇵🇰* | **75.90** | 1.115 | +3.32 | 75.8% |
| **5** | **Tim David** | **73.81** | 1.114 | +3.63 | 69.3% | **Taskin Ahmed** 🎯 | **75.76** | 1.054 | +2.95 | 80.5% |
| **6** | **Yashasvi Jaiswal** 👑 | **72.86** | 0.938 | +4.26 | 69.9% | **Sunil Narine** | **74.83** | 0.963 | +3.51 | 75.6% |
| **7** | **Vaibhav Sooryavanshi** 👑 | **71.91** | 1.026 | +2.86 | 68.9% | **Abrar Ahmed** 🇵🇰* | **74.75** | 1.092 | +2.62 | 80.6% |
| **8** | **Mitchell Santner** | **70.81** | 1.042 | +2.41 | 72.4% | **Gudakesh Motie** 🎯 | **73.84** | 0.988 | +2.18 | 77.2% |
| **9** | **Prabhsimran Singh** | **70.52** | 0.978 | +3.12 | 68.4% | **Nathan Ellis** 🎯 | **72.19** | 1.033 | +2.19 | 80.0% |
| **10** | **Jonny Bairstow** 🎯 | **69.87** | 0.979 | +3.08 | 70.1% | **Maheesh Theekshana** | **71.86** | 0.982 | +2.10 | 74.5% |

*\*BCCI Policy Note: Pakistani players serve as global statistical benchmarks but are strictly coded as BCCI Ineligible for IPL recruitment. Targets marked with 🎯 represent actionable Free Agent acquisitions.*

---

## 🛠️ Repository Architecture

```
SuperRR/
├── pipeline.py                     # Standalone production ETL & RPCS pressure evaluation engine
├── build_dashboard.py              # Compiles data.json into standalone interactive war room dashboard
├── generate_charts.py              # Publication-grade chart generation from pipeline output
├── convert_to_pdf.py               # Markdown to styled PDF compilation engine (Weasyprint)
├── index.html                      # Root war room dashboard for direct GitHub Pages hosting
├── requirements.txt                # Pinned production dependencies
├── pyproject.toml                  # Modern Python packaging and pytest configuration
├── .gitignore                      # Clean Python, cache, and artifact ignore rules
│
├── data/                           # Ingested multi-competition dataset (200,987 deliveries)
│   ├── ball_by_ball.csv
│   ├── competitions.csv
│   ├── competition_team_player_mapping.csv
│   ├── matches.csv
│   ├── playing_eleven.csv
│   ├── teams.csv
│   └── Round 1 Problem Statement _ SupeRR Selector Season 2.docx.pdf
│
├── dashboard/                      # Dashboard assets & intelligence database
│   ├── data.json                   # Verified player intelligence & RPCS database (394 players)
│   └── index.html                  # Compiled interactive war room dashboard
│
├── output/                         # Verified evaluation deliverables
│   ├── top_10_batters.csv          # Unstop Official Top 10 Batters
│   ├── top_10_bowlers.csv          # Unstop Official Top 10 Bowlers
│   ├── all_batters_evaluated.csv   # Complete qualifying batters (198 players)
│   └── all_bowlers_evaluated.csv   # Complete qualifying bowlers (196 players)
│
├── charts/                         # Publication-grade analytical figures
│   ├── scatter_batters_sr_csr.png
│   ├── scatter_bowlers_econ_csr.png
│   ├── top_performers_radar_profile.png
│   └── rankings_rpcs_barchart.png
│
├── docs/                           # Deliverable documentation & presentation assets
│   └── presentation_scripts.md     # Video pitch scripts, social media copy, and pitch packages
│
├── scripts/                        # Automation & deployment scripts
│   └── deploy_gh_pages.sh          # One-click dashboard compilation and verification
│
└── tests/                          # Automated test suite (58 tests)
    ├── __init__.py
    ├── test_pipeline.py            # Pipeline mathematics, boundary invariants, and forensic validation
    ├── test_dashboard.py           # Dashboard schema, auction rules, and BCCI eligibility assertions
    └── test_dashboard_e2e.py       # End-to-end integration and simulation tests
```

---

## 🔬 5 Rigorous Forensic Data Cleanups

Before computing player ratings, raw competition records were audited for anomalies that corrupt traditional models:

1. **Tilak Varma Missing Dismissal (Match 40709, Row 127899)**: Imputed Tilak Varma (ID 7897) for the unlabelled *Retire Out*, preserving wicket equity without crediting bowler.
2. **Post-Conclusion Quarantine (Match 48610)**: Quarantined 12 invalid deliveries recorded after the 2nd innings target had mathematically been reached.
3. **Rain-Truncated Revised Overs (34 Matches)**: Mapped legal ball limits per bowler and adjusted innings par denominators to eliminate DLS artifact distortion.
4. **Non-Striker Runout Credit Quarantine (271 Deliveries)**: Delineated bowler-earned dismissals (Caught, Bowled, LBW, Stumped, Hit Wicket) from 271 non-striker runouts.
5. **Entity ID Isolation (Primary Keys)**: Disambiguated duplicate player name instances (e.g., senior vs. emerging international players) via verified CTPM mappings.

---

## ⚡ Quickstart & Reproducibility

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/yashagarwal-lab/superrr-dashboard.git
cd superrr-dashboard

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Full Pipeline

```bash
# Ingest raw data, apply forensics, calibrate models, and export rankings to output/
python pipeline.py
```

### 3. Generate Analytical Charts

```bash
# Generates 4 publication figures in charts/
python generate_charts.py
```

### 4. Build & Compile Interactive Dashboard

```bash
# Compiles data.json into index.html and dashboard/index.html
python build_dashboard.py
```

### 5. Run the Automated Test Suite

```bash
# Execute 58 rigorous unit and e2e integration tests
pytest -v
```

---

## 🧪 Testing & Validation Suite

The repository includes a comprehensive 58-test suite across 3 tiers:

* **Pipeline Invariants (`tests/test_pipeline.py`)**: Validates zero-boundary conditions, Win Probability monotonicity, non-striker runout isolation, and Tilak Varma imputation.
* **Auction & Regulatory Compliance (`tests/test_dashboard.py`)**: Asserts 27 Pakistani records are marked `BCCI Ineligible`, verifies the Kuldeep Yadav ⇄ Rishabh Pant trade lock, and ensures Free Agent tags match IPL 2026/27 realities.
* **End-to-End Simulation (`tests/test_dashboard_e2e.py`)**: Tests DOM rendering, scatter plot coordinates, radar profiles, and the Royals Starting XI ₹120.0 Cr purse simulator.

```bash
$ pytest
============================== 58 passed in 7.73s ==============================
```

---

## 🏆 Royals Projected Starting XI (IPL 2027)

Utilizing the interactive simulator within the ₹120.0 Cr purse constraint (₹113.6 Cr spent / ₹6.4 Cr reserve):

1. **Yashasvi Jaiswal** (Opener — RR Retained, ₹18.0 Cr) • *RPCS: 72.86*
2. **Vaibhav Sooryavanshi** (Impact Opener — RR Retained, ₹1.1 Cr) • *RPCS: 71.91*
3. **Jonny Bairstow** (WK / Boundary Enforcer — Free Agent, ₹7.5 Cr) • *RPCS: 69.87*
4. **Riyan Parag** (C) (Middle Dynamo — RR Retained, ₹14.0 Cr) • *RPCS: 64.50*
5. **Dhruv Jurel** (WK) (Crisis Anchor — RR Retained, ₹14.0 Cr) • *RPCS: 68.20*
6. **Shimron Hetmyer** (Death Closer — RR Retained, ₹11.0 Cr) • *RPCS: 73.81*
7. **Ravindra Jadeja** (Elite All-Rounder — RR Retained, ₹16.0 Cr) • *RPCS: 68.40*
8. **Mitchell Santner** (Squeeze Spinner — Auction Buy, ₹4.5 Cr) • *RPCS: 70.81*
9. **Jofra Archer** (Express Pace 150kph — RR Retained, ₹12.5 Cr) • *RPCS: 65.20*
10. **Ravi Bishnoi** (Wrist-Spin Squeeze — RR Retained, ₹11.0 Cr) • *RPCS: 66.40*
11. **Nathan Ellis** (Death Yorker Specialist — Free Agent, ₹5.5 Cr) • *RPCS: 72.19*

**Starting XI Team Clutch Index**: **69.4 / 100** (Championship Benchmark)

---

## 📜 License & Citation

Developed for the **Rajasthan Royals SupeRR Selector (Season 2)** by **Yash Agarwal** ([@yashagarwal-lab](https://github.com/yashagarwal-lab)).

Licensed under the [MIT License](LICENSE).
