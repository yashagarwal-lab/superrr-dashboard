import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# Load official evaluated metrics from production pipeline output
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
bat_eval = pd.read_csv(os.path.join(OUTPUT_DIR, "all_batters_evaluated.csv"))
bowl_eval = pd.read_csv(os.path.join(OUTPUT_DIR, "all_bowlers_evaluated.csv"))

CHARTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# 1. Batters Scatter Plot: Pressure SR vs CSR
fig, ax = plt.subplots(figsize=(11, 7), dpi=300)

x = bat_eval['press_sr']
y = bat_eval['csr'] * 100
sizes = bat_eval['press_balls'] / 2.0
colors = bat_eval['rpcs']

scatter = ax.scatter(x, y, s=sizes, c=colors, cmap='plasma', alpha=0.75, edgecolors='black', linewidth=0.8)
cbar = plt.colorbar(scatter, ax=ax, pad=0.02)
cbar.set_label('Reliability-Adjusted Pressure Composite Score (RPCS)', fontsize=10, weight='bold')

# Quadrant reference lines
med_x = 155.0
med_y = 65.0
ax.axvline(med_x, color='#777777', linestyle='--', alpha=0.6, linewidth=1)
ax.axhline(med_y, color='#777777', linestyle='--', alpha=0.6, linewidth=1)

# Annotate Top 10 Batters
top10_bat = bat_eval.sort_values(by='rpcs', ascending=False).head(10)
for idx, r in top10_bat.iterrows():
    name = r['player_name']
    ax.annotate(
        f"{name}\n({r['press_sr']:.0f} SR, {r['csr']*100:.0f}%)",
        xy=(r['press_sr'], r['csr'] * 100),
        xytext=(5, 5),
        textcoords='offset points',
        fontsize=8.5,
        fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.85, edgecolor="#cccccc")
    )

ax.text(195, 88, 'ELITE CLUTCH FINISHERS\n(High SR, High CSR)', fontsize=11, color='#0d47a1', weight='bold', ha='center',
        bbox=dict(boxstyle="square,pad=0.3", facecolor="#e3f2fd", alpha=0.8))
ax.text(125, 88, 'CRISIS ACCUMULATORS\n(Low SR, High CSR)', fontsize=10, color='#37474f', weight='bold', ha='center')
ax.text(195, 45, 'VOLATILE PINCH HITTERS\n(High SR, Low CSR)', fontsize=10, color='#b71c1c', weight='bold', ha='center')

ax.set_title('T20 Batting Under Pressure: Strike Rate vs Clutch Success Rate (CSR)', fontsize=14, weight='bold', pad=15)
ax.set_xlabel('Strike Rate in High-Pressure Deliveries (SR_press)', fontsize=11, weight='bold')
ax.set_ylabel('Clutch Success Rate (% Innings Net Positive WPA / BRA)', fontsize=11, weight='bold')
ax.set_xlim(110, 235)
ax.set_ylim(35, 95)

plt.tight_layout()
scatter_bat_path = os.path.join(CHARTS_DIR, "scatter_batters_sr_csr.png")
plt.savefig(scatter_bat_path, dpi=300)
plt.close()
print(f"Saved {scatter_bat_path}")

# 2. Bowlers Scatter Plot: Pressure Economy vs CSR
fig, ax = plt.subplots(figsize=(11, 7), dpi=300)

# We invert X so lower economy (better) appears to the right
x_econ = bowl_eval['press_econ']
y_b_csr = bowl_eval['csr'] * 100
b_sizes = bowl_eval['press_balls'] / 2.0
b_colors = bowl_eval['rpcs']

scatter = ax.scatter(x_econ, y_b_csr, s=b_sizes, c=b_colors, cmap='viridis', alpha=0.75, edgecolors='black', linewidth=0.8)
cbar = plt.colorbar(scatter, ax=ax, pad=0.02)
cbar.set_label('Reliability-Adjusted Pressure Composite Score (RPCS)', fontsize=10, weight='bold')

# Quadrant reference lines
ax.axvline(7.5, color='#777777', linestyle='--', alpha=0.6, linewidth=1)
ax.axhline(70.0, color='#777777', linestyle='--', alpha=0.6, linewidth=1)

# Annotate Top 10 Bowlers
top10_bowl = bowl_eval.sort_values(by='rpcs', ascending=False).head(10)
for idx, r in top10_bowl.iterrows():
    name = r['player_name']
    ax.annotate(
        f"{name}\n({r['press_econ']:.2f} Econ, {r['csr']*100:.0f}%)",
        xy=(r['press_econ'], r['csr'] * 100),
        xytext=(5, 5),
        textcoords='offset points',
        fontsize=8.5,
        fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.85, edgecolor="#cccccc")
    )

# Invert x axis: lower economy is better!
ax.invert_xaxis()

ax.text(6.0, 92, 'LOCKDOWN PRESSURE SPECIALISTS\n(Sub-7.0 Economy, High CSR)', fontsize=11, color='#1b5e20', weight='bold', ha='center',
        bbox=dict(boxstyle="square,pad=0.3", facecolor="#e8f5e9", alpha=0.8))
ax.text(9.5, 92, 'WICKETS AT HIGH COST\n(High Econ, High CSR)', fontsize=10, color='#e65100', weight='bold', ha='center')
ax.text(9.5, 45, 'PRESSURE LEAKERS\n(High Econ, Low CSR)', fontsize=10, color='#b71c1c', weight='bold', ha='center')

ax.set_title('T20 Bowling Under Pressure: Economy Rate vs Clutch Success Rate (CSR)', fontsize=14, weight='bold', pad=15)
ax.set_xlabel('Economy Rate in High-Pressure Deliveries (Inverted Axis: Lower is Better)', fontsize=11, weight='bold')
ax.set_ylabel('Clutch Success Rate (% Spells Net Positive WPA / BRS)', fontsize=11, weight='bold')
ax.set_xlim(11.0, 4.5)
ax.set_ylim(40, 96)

plt.tight_layout()
scatter_bowl_path = os.path.join(CHARTS_DIR, "scatter_bowlers_econ_csr.png")
plt.savefig(scatter_bowl_path, dpi=300)
plt.close()
print(f"Saved {scatter_bowl_path}")

# 3. Top Performers Radar / Profile Comparison
from math import pi

categories = ['Clutch Volume', 'Win Added (WPA)', 'Par Diff (BRA/BRS)', 'Retention (κ)', 'Clutch Rate (CSR)', 'Consistency (1-SCS)']
N = len(categories)

# Let's create comparison radar charts for top 3 batters and top 3 bowlers
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), subplot_kw=dict(polar=True), dpi=300)

def plot_radar(ax, data_row, color, label, is_batter=True):
    # Normalized 0-1 metrics
    vals = [
        min(1.0, data_row['press_balls'] / 1400.0),
        min(1.0, max(0.0, data_row['press_wpa'] / 7.0)),
        min(1.0, max(0.0, (data_row['press_bra' if is_batter else 'press_brs'] + 50) / 450.0)),
        min(1.0, max(0.0, (data_row['kappa_bat' if is_batter else 'kappa_bowl'] - 0.8) / 0.4)),
        data_row['csr'],
        1.0 - data_row['scs']
    ]
    vals += vals[:1]
    ax.plot(angles, vals, color=color, linewidth=2, linestyle='solid', label=label)
    ax.fill(angles, vals, color=color, alpha=0.15)

# Batter Radar
colors_bat = ['#e63946', '#1d3557', '#2a9d8f']
for i, (idx, r) in enumerate(top10_bat.head(3).iterrows()):
    plot_radar(ax1, r, colors_bat[i], f"{r['player_name']} (RPCS {r['rpcs']:.1f})", is_batter=True)

ax1.set_theta_offset(pi / 2)
ax1.set_theta_direction(-1)
ax1.set_xticks(angles[:-1])
ax1.set_xticklabels(categories, fontsize=9, weight='bold')
ax1.set_rlabel_position(0)
ax1.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax1.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], color="grey", size=7)
ax1.set_ylim(0, 1.05)
ax1.set_title("Top 3 Clutch Batters Multi-Dimensional Profile", size=12, weight='bold', pad=20)
ax1.legend(loc='upper right', bbox_to_anchor=(0.1, 1.15), fontsize=8.5)

# Bowler Radar
colors_bowl = ['#457b9d', '#e76f51', '#2b9348']
for i, (idx, r) in enumerate(top10_bowl.head(3).iterrows()):
    plot_radar(ax2, r, colors_bowl[i], f"{r['player_name']} (RPCS {r['rpcs']:.1f})", is_batter=False)

ax2.set_theta_offset(pi / 2)
ax2.set_theta_direction(-1)
ax2.set_xticks(angles[:-1])
ax2.set_xticklabels(categories, fontsize=9, weight='bold')
ax2.set_rlabel_position(0)
ax2.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax2.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], color="grey", size=7)
ax2.set_ylim(0, 1.05)
ax2.set_title("Top 3 Clutch Bowlers Multi-Dimensional Profile", size=12, weight='bold', pad=20)
ax2.legend(loc='upper right', bbox_to_anchor=(0.1, 1.15), fontsize=8.5)

plt.suptitle("SuperRR Multi-Moment Consistency Radar (SupeRR Selector Season 2)", fontsize=14, weight='bold', y=0.98)
plt.tight_layout()
radar_path = os.path.join(CHARTS_DIR, "top_performers_radar_profile.png")
plt.savefig(radar_path, dpi=300)
plt.close()
print(f"Saved {radar_path}")

# 4. Top 10 Batters & Bowlers RPCS Horizontal Bar Charts
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)

top10_bat_sorted = top10_bat.sort_values(by='rpcs', ascending=True)
colors_b = plt.cm.plasma(np.linspace(0.4, 0.9, 10))
bars1 = ax1.barh(top10_bat_sorted['player_name'], top10_bat_sorted['rpcs'], color=colors_b, edgecolor='black', linewidth=0.6)
ax1.set_xlabel('RPCS (0 - 100)', fontsize=11, weight='bold')
ax1.set_title('Top 10 Batters Under Pressure', fontsize=12, weight='bold')
ax1.set_xlim(50, 85)
for bar in bars1:
    ax1.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.2f}", va='center', ha='left', fontsize=8.5, weight='bold')

top10_bowl_sorted = top10_bowl.sort_values(by='rpcs', ascending=True)
colors_bw = plt.cm.viridis(np.linspace(0.4, 0.9, 10))
bars2 = ax2.barh(top10_bowl_sorted['player_name'], top10_bowl_sorted['rpcs'], color=colors_bw, edgecolor='black', linewidth=0.6)
ax2.set_xlabel('RPCS (0 - 100)', fontsize=11, weight='bold')
ax2.set_title('Top 10 Bowlers Under Pressure', fontsize=12, weight='bold')
ax2.set_xlim(50, 85)
for bar in bars2:
    ax2.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.2f}", va='center', ha='left', fontsize=8.5, weight='bold')

plt.suptitle('Official SupeRR Selector Season 2 — Definitive Rankings', fontsize=14, weight='bold')
plt.tight_layout()
bars_path = os.path.join(CHARTS_DIR, "rankings_rpcs_barchart.png")
plt.savefig(bars_path, dpi=300)
plt.close()
print(f"Saved {bars_path}")
