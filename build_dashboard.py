#!/usr/bin/env python3
"""
Rajasthan Royals SupeRR Selector Analytics War Room Dashboard Builder.
Compiles a modern sports-analytics dashboard (Tailwind CSS / Shadcn UI / Tremor aesthetic)
incorporating verified IPL 2027 auction intelligence, prominent status badges,
interactive Canvas scatter & radar charts, and live purse tracking.
"""

import json
import os

DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(DASHBOARD_DIR, "dashboard", "data.json")
OUTPUT_HTML = os.path.join(DASHBOARD_DIR, "dashboard", "index.html")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

data_json_str = json.dumps(data, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rajasthan Royals SupeRR Selector — Pressure Analytics & IPL 2027 Auction War Room</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root {
      --slate-950: #090d16;
      --slate-900: #0f172a;
      --slate-850: #131d33;
      --slate-800: #1e293b;
      --slate-700: #334155;
      --slate-600: #475569;
      --slate-400: #94a3b8;
      --slate-300: #cbd5e1;
      --slate-200: #e2e8f0;
      --slate-50: #f8fafc;
      --rr-pink: #f43f5e;
      --rr-pink-muted: rgba(244, 63, 94, 0.15);
      --rr-blue: #1e3a8a;
      --rr-navy: #0f2347;
      --emerald: #10b981;
      --amber: #f59e0b;
      --yellow: #eab308;
      --red: #ef4444;
      --red-dark: #dc2626;
      --indigo: #6366f1;
      --purple: #a855f7;
      --sky: #0ea5e9;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--slate-950);
      color: var(--slate-200);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      line-height: 1.5;
      padding-bottom: 60px;
      -webkit-font-smoothing: antialiased;
    }

    .num-tabular {
      font-family: 'JetBrains Mono', monospace;
      font-variant-numeric: tabular-nums;
    }

    /* Header */
    header {
      background-color: rgba(9, 13, 22, 0.95);
      border-bottom: 1px solid var(--slate-800);
      padding: 14px 28px;
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(12px);
    }
    .header-content {
      max-width: 1440px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .logo-badge {
      background-color: #e11d48;
      color: white;
      font-weight: 800;
      font-size: 16px;
      padding: 6px 12px;
      border-radius: 6px;
      letter-spacing: 0.5px;
      border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .brand-text h1 {
      font-size: 18px;
      font-weight: 700;
      color: var(--slate-50);
      letter-spacing: -0.3px;
    }
    .brand-text h1 span {
      color: #fb7185;
      font-weight: 600;
    }
    .brand-text p {
      font-size: 12px;
      color: var(--slate-400);
    }

    /* Nav Tabs */
    .nav-tabs {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      background-color: var(--slate-900);
      padding: 4px;
      border-radius: 8px;
      border: 1px solid var(--slate-800);
    }
    .nav-tab {
      background: transparent;
      border: none;
      color: var(--slate-400);
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .nav-tab:hover {
      color: var(--slate-50);
      background: rgba(255, 255, 255, 0.04);
    }
    .nav-tab.active {
      background: var(--slate-800);
      color: var(--slate-50);
      box-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }

    /* Main Container */
    .container {
      max-width: 1440px;
      margin: 20px auto;
      padding: 0 24px;
    }

    /* Tab Views */
    .tab-view { display: none; }
    .tab-view.active { display: block; animation: tabFadeIn 0.2s ease-out; }
    @keyframes tabFadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Metric Cards (Tremor / Shadcn style) */
    .hero-stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 14px;
      margin-bottom: 20px;
    }
    .stat-card {
      background: var(--slate-900);
      border: 1px solid var(--slate-800);
      border-radius: 8px;
      padding: 16px 18px;
      transition: border-color 0.15s ease;
    }
    .stat-card:hover {
      border-color: var(--slate-700);
    }
    .stat-label {
      font-size: 11px;
      text-transform: uppercase;
      color: var(--slate-400);
      font-weight: 600;
      letter-spacing: 0.5px;
    }
    .stat-value {
      font-size: 22px;
      font-weight: 700;
      margin: 4px 0 2px 0;
      color: var(--slate-50);
      font-family: 'JetBrains Mono', monospace;
    }
    .stat-sub {
      font-size: 11px;
      color: var(--slate-400);
      line-height: 1.4;
    }

    /* Status Badges */
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 10px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      white-space: nowrap;
      line-height: 1.2;
    }
    .badge-ineligible {
      background: #dc2626 !important;
      color: #ffffff !important;
      border: 1px solid #b91c1c;
      font-weight: 800;
    }
    .badge-free-agent {
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .badge-traded {
      background: rgba(245, 158, 11, 0.15);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .badge-watchlist {
      background: rgba(234, 179, 8, 0.15);
      color: #facc15;
      border: 1px solid rgba(234, 179, 8, 0.4);
    }
    .badge-retention {
      background: rgba(99, 102, 241, 0.15);
      color: #a5b4fc;
      border: 1px solid rgba(99, 102, 241, 0.4);
    }
    .badge-rr-core {
      background: rgba(244, 63, 94, 0.15);
      color: #fb7185;
      border: 1px solid rgba(244, 63, 94, 0.4);
    }
    .badge-global-steal {
      background: rgba(168, 85, 247, 0.15);
      color: #d8b4fe;
      border: 1px solid rgba(168, 85, 247, 0.4);
    }
    .badge-domestic-steal {
      background: rgba(14, 165, 233, 0.15);
      color: #7dd3fc;
      border: 1px solid rgba(14, 165, 233, 0.4);
    }
    .badge-auction-target {
      background: rgba(148, 163, 184, 0.12);
      color: #94a3b8;
      border: 1px solid rgba(148, 163, 184, 0.25);
    }

    /* Table Rows Visual Styling */
    .row-ineligible {
      background: rgba(220, 38, 38, 0.12) !important;
      border-left: 3px solid #dc2626 !important;
    }
    .row-ineligible:hover {
      background: rgba(220, 38, 38, 0.18) !important;
    }
    .row-free-agent {
      border-left: 3px solid #10b981 !important;
    }
    .row-traded {
      border-left: 3px solid #f59e0b !important;
    }
    .row-watchlist {
      border-left: 3px solid #eab308 !important;
    }
    .row-retention {
      border-left: 3px solid #6366f1 !important;
    }
    .row-rr-core {
      border-left: 3px solid #f43f5e !important;
    }

    /* Toolbar */
    .toolbar {
      background: var(--slate-900);
      border: 1px solid var(--slate-800);
      border-radius: 8px;
      padding: 12px 16px;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }
    .toolbar-left, .toolbar-right {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .role-toggle {
      display: flex;
      background: var(--slate-950);
      border: 1px solid var(--slate-800);
      border-radius: 6px;
      overflow: hidden;
      padding: 2px;
    }
    .role-btn {
      padding: 5px 12px;
      border: none;
      background: transparent;
      color: var(--slate-400);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      border-radius: 4px;
      transition: all 0.15s;
    }
    .role-btn.active {
      background: var(--slate-800);
      color: var(--slate-50);
    }
    .filter-pills {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }
    .pill {
      background: var(--slate-950);
      border: 1px solid var(--slate-800);
      color: var(--slate-400);
      padding: 5px 11px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }
    .pill:hover {
      border-color: var(--slate-700);
      color: var(--slate-200);
    }
    .pill.active {
      background: var(--slate-800);
      border-color: var(--slate-600);
      color: var(--slate-50);
    }
    .search-input {
      background: var(--slate-950);
      border: 1px solid var(--slate-800);
      border-radius: 6px;
      padding: 6px 12px;
      color: var(--slate-50);
      font-size: 12px;
      width: 200px;
      outline: none;
      transition: border-color 0.15s;
    }
    .search-input:focus {
      border-color: var(--slate-600);
    }
    .sort-select {
      background: var(--slate-950);
      border: 1px solid var(--slate-800);
      border-radius: 6px;
      color: var(--slate-50);
      padding: 6px 10px;
      font-size: 12px;
      outline: none;
      cursor: pointer;
    }

    /* Table Component */
    .table-container {
      background: var(--slate-900);
      border: 1px solid var(--slate-800);
      border-radius: 8px;
      overflow-x: auto;
      box-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 12px;
    }
    th {
      background: #0b1120;
      padding: 10px 14px;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--slate-400);
      font-weight: 700;
      border-bottom: 1px solid var(--slate-800);
      white-space: nowrap;
    }
    td {
      padding: 11px 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      vertical-align: middle;
      white-space: nowrap;
    }
    tr:hover {
      background: rgba(30, 41, 59, 0.5);
      cursor: pointer;
    }
    .rank-cell {
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: var(--slate-400);
      width: 44px;
    }
    .rank-cell.top3 {
      color: #fbbf24;
    }
    .player-name-cell {
      display: flex;
      flex-direction: column;
    }
    .name-title {
      font-weight: 700;
      color: var(--slate-50);
      font-size: 13px;
    }
    .name-team-sub {
      font-size: 11px;
      color: var(--slate-400);
    }
    .rpcs-pill {
      display: inline-block;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      padding: 2px 7px;
      border-radius: 4px;
      background: rgba(244, 63, 94, 0.12);
      color: #fb7185;
      border: 1px solid rgba(244, 63, 94, 0.25);
    }
    .rpcs-pill.elite {
      background: rgba(16, 185, 129, 0.12);
      color: #34d399;
      border-color: rgba(16, 185, 129, 0.3);
    }

    /* Modal / Dialog (Shadcn style) */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(4px);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 1000;
      padding: 20px;
    }
    .modal-overlay.active { display: flex; }
    .modal-card {
      background: var(--slate-900);
      border: 1px solid var(--slate-800);
      border-radius: 10px;
      width: 100%;
      max-width: 840px;
      max-height: 90vh;
      overflow-y: auto;
      padding: 24px 28px;
      position: relative;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .modal-close {
      position: absolute;
      top: 16px;
      right: 18px;
      font-size: 20px;
      color: var(--slate-400);
      cursor: pointer;
      background: none;
      border: none;
    }
    .modal-close:hover { color: var(--slate-50); }
    .modal-header {
      border-bottom: 1px solid var(--slate-800);
      padding-bottom: 14px;
      margin-bottom: 18px;
    }
    .modal-header h2 {
      font-size: 20px;
      font-weight: 700;
      color: var(--slate-50);
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .modal-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 16px;
    }
    @media (max-width: 720px) { .modal-grid { grid-template-columns: 1fr; } }
    .modal-section {
      background: var(--slate-950);
      border: 1px solid var(--slate-800);
      border-radius: 8px;
      padding: 14px;
    }
    .modal-section h4 {
      font-size: 11px;
      text-transform: uppercase;
      color: var(--slate-400);
      font-weight: 700;
      letter-spacing: 0.5px;
      margin-bottom: 10px;
    }
    .info-row {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      padding: 5px 0;
      border-bottom: 1px solid rgba(255,255,255,0.03);
    }
    .info-row:last-child { border-bottom: none; }
    .info-row span:first-child { color: var(--slate-400); }
    .info-row span:last-child { font-weight: 600; color: var(--slate-50); }

    /* Modal Alert Boxes */
    .modal-alert-box {
      border-radius: 6px;
      padding: 12px 14px;
      margin-bottom: 16px;
      font-size: 12px;
      line-height: 1.5;
    }
    .alert-ineligible {
      background: rgba(220, 38, 38, 0.15);
      border: 1px solid #dc2626;
      color: #fca5a5;
    }
    .alert-ineligible strong { color: #ffffff; }
    .alert-free-agent {
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid #10b981;
      color: #6ee7b7;
    }
    .alert-traded {
      background: rgba(245, 158, 11, 0.12);
      border: 1px solid #f59e0b;
      color: #fcd34d;
    }
    .alert-watchlist {
      background: rgba(234, 179, 8, 0.12);
      border: 1px solid #eab308;
      color: #fde047;
    }
    .alert-retention {
      background: rgba(99, 102, 241, 0.12);
      border: 1px solid #6366f1;
      color: #c7d2fe;
    }
    .alert-rr-core {
      background: rgba(244, 63, 94, 0.12);
      border: 1px solid #f43f5e;
      color: #fecdd3;
    }

    /* Contract Progression */
    .journey-tracker {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-top: 8px;
      text-align: center;
    }
    .journey-step {
      background: var(--slate-900);
      border: 1px solid var(--slate-800);
      border-radius: 6px;
      padding: 8px;
    }
    .journey-year {
      font-size: 10px;
      color: var(--slate-400);
      font-weight: 700;
      text-transform: uppercase;
    }
    .journey-team {
      font-size: 12px;
      font-weight: 700;
      margin-top: 2px;
      color: var(--slate-50);
    }

    /* Charts Container */
    .chart-panel {
      background: var(--slate-900);
      border: 1px solid var(--slate-800);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
    }
    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 12px;
    }
    .chart-box {
      position: relative;
      width: 100%;
      height: 420px;
    }
    canvas {
      width: 100% !important;
      height: 100% !important;
    }

    /* Scatter Legend */
    .scatter-legend {
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      margin-bottom: 12px;
      font-size: 11px;
      color: var(--slate-400);
      background: var(--slate-950);
      padding: 8px 12px;
      border-radius: 6px;
      border: 1px solid var(--slate-800);
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .legend-dot {
      width: 9px;
      height: 9px;
      border-radius: 50%;
    }

    /* Scatter Hover Tooltip */
    #scatterTooltip {
      position: absolute;
      display: none;
      background: var(--slate-900);
      border: 1px solid var(--slate-700);
      border-radius: 6px;
      padding: 8px 12px;
      font-size: 11px;
      color: var(--slate-50);
      pointer-events: none;
      z-index: 50;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
      min-width: 180px;
    }

    /* Auction Board Grid */
    .auction-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 16px;
      margin-top: 16px;
    }
    .auction-card {
      background: var(--slate-900);
      border: 1px solid var(--slate-800);
      border-radius: 8px;
      padding: 16px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .auction-card:hover {
      border-color: var(--slate-600);
      transform: translateY(-2px);
    }
    .auction-card.priority-card {
      border-color: rgba(16, 185, 129, 0.4);
      background: #0f1c24;
    }
    .auction-card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 10px;
    }
    .auction-player-name {
      font-size: 15px;
      font-weight: 700;
      color: var(--slate-50);
    }
    .auction-role {
      font-size: 11px;
      color: #fb7185;
      font-weight: 600;
      text-transform: uppercase;
    }
    .auction-price-tag {
      background: var(--slate-950);
      border: 1px solid var(--slate-800);
      color: #fbbf24;
      font-size: 11px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      padding: 3px 8px;
      border-radius: 4px;
    }
    .auction-trail {
      background: var(--slate-950);
      border-radius: 6px;
      padding: 10px;
      font-size: 12px;
      margin: 10px 0;
      border-left: 3px solid var(--slate-700);
      color: var(--slate-300);
    }
    .auction-stats-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      text-align: center;
      margin-top: 10px;
    }
    .mini-stat-card {
      background: var(--slate-950);
      border: 1px solid var(--slate-800);
      padding: 6px;
      border-radius: 4px;
    }
    .mini-stat-val {
      font-size: 13px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: var(--slate-50);
    }
    .mini-stat-lbl {
      font-size: 10px;
      color: var(--slate-400);
      text-transform: uppercase;
    }

    /* Purse Tracker (XI Builder) */
    .purse-tracker {
      background: var(--slate-900);
      border: 1px solid var(--slate-800);
      border-radius: 8px;
      padding: 16px 20px;
      margin-bottom: 18px;
    }
    .purse-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin-bottom: 12px;
    }
    .purse-item-lbl {
      font-size: 11px;
      text-transform: uppercase;
      color: var(--slate-400);
      font-weight: 600;
    }
    .purse-item-val {
      font-size: 20px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: var(--slate-50);
    }
    .purse-progress-bar {
      width: 100%;
      height: 8px;
      background: var(--slate-950);
      border-radius: 4px;
      overflow: hidden;
      border: 1px solid var(--slate-800);
    }
    .purse-progress-fill {
      height: 100%;
      background: #10b981;
      width: 94.7%;
      border-radius: 4px;
    }
    .xi-slot {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 9px 12px;
      background: var(--slate-950);
      border: 1px solid var(--slate-800);
      border-radius: 6px;
      margin-bottom: 6px;
      font-size: 12px;
    }
    .xi-slot-num {
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: #fb7185;
      width: 24px;
    }
    .xi-slot-name {
      font-weight: 600;
      color: var(--slate-50);
      flex: 1;
      margin: 0 10px;
    }
    .xi-slot-role {
      font-size: 11px;
      color: var(--slate-400);
    }
    .xi-slot-cost {
      font-size: 11px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
      color: #fbbf24;
      margin-right: 12px;
    }
    .xi-slot-rpcs {
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: #34d399;
    }

    /* Case Studies & Math */
    .case-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
    }
    .case-card {
      background: var(--slate-900);
      border: 1px solid var(--slate-800);
      border-radius: 8px;
      padding: 18px;
    }
    .case-badge {
      font-size: 11px;
      font-weight: 700;
      color: #fb7185;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 4px;
    }
    .case-title {
      font-size: 16px;
      font-weight: 700;
      color: var(--slate-50);
      margin-bottom: 8px;
    }
    .case-impact {
      background: var(--slate-950);
      border-left: 3px solid #10b981;
      padding: 8px 12px;
      border-radius: 0 4px 4px 0;
      margin: 10px 0;
      font-size: 12px;
      font-weight: 600;
      color: #6ee7b7;
      font-family: 'JetBrains Mono', monospace;
    }
    .case-desc {
      font-size: 12px;
      color: var(--slate-300);
      line-height: 1.6;
    }

    footer {
      text-align: center;
      margin-top: 40px;
      color: var(--slate-400);
      font-size: 12px;
    }
  </style>
</head>
<body>

  <!-- Header -->
  <header>
    <div class="header-content">
      <div class="brand">
        <div class="logo-badge">RR</div>
        <div class="brand-text">
          <h1>SupeRR Selector <span>War Room</span></h1>
          <p>Multi-Moment Pressure Analytics & Verified IPL 2027 Auction Intelligence</p>
        </div>
      </div>
      <div class="nav-tabs">
        <button class="nav-tab active" onclick="switchTab('roster', event)">Unstop Top 10 Roster</button>
        <button class="nav-tab" onclick="switchTab('auction', event)">Auction Target Board</button>
        <button class="nav-tab" onclick="switchTab('contracts', event)">Release & Contract Audit</button>
        <button class="nav-tab" onclick="switchTab('scatter', event)">Scatter Explorer</button>
        <button class="nav-tab" onclick="switchTab('radar', event)">Radar Comparator</button>
        <button class="nav-tab" onclick="switchTab('xibuilder', event)">RR 2027 XI Builder</button>
        <button class="nav-tab" onclick="switchTab('cases', event)">Match Case Studies</button>
        <button class="nav-tab" onclick="switchTab('math', event)">Methodology Proofs</button>
      </div>
    </div>
  </header>

  <div class="container">

    <!-- KPI Metric Cards (Tremor Style) -->
    <div class="hero-stats">
      <div class="stat-card">
        <div class="stat-label">Deliveries Analyzed</div>
        <div class="stat-value">200,987</div>
        <div class="stat-sub">Cleaned balls across 883 matches, 141 competitions (200,999 raw; 12 phantom balls quarantined)</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">High-Pressure Balls</div>
        <div class="stat-value">117,915</div>
        <div class="stat-sub">58.7% match-critical deliveries under sustained match duress (LI ≥ 1.5)</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Released Free Agents</div>
        <div class="stat-value">31 Players</div>
        <div class="stat-sub">Confirmed unencumbered players entering 2027 auction (Ellis, Bairstow, Maxwell, Taskin)</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Global Scouting Pool</div>
        <div class="stat-value">100% Eligible</div>
        <div class="stat-sub">Overseas gems with 0 IPL contractual commitments at base price (Taskin, Mahmud, Motie)</div>
      </div>
    </div>

    <!-- TAB 1: ROSTER / UNSTOP DROPDOWNS -->
    <div id="tab-roster" class="tab-view active">
      <div class="toolbar">
        <div class="toolbar-left">
          <div class="role-toggle">
            <button id="btn-batters" class="role-btn active" onclick="setRole('batters')">Batters (198)</button>
            <button id="btn-bowlers" class="role-btn" onclick="setRole('bowlers')">Bowlers (196)</button>
          </div>
          <div class="filter-pills">
            <div class="pill active" onclick="setFilter('all', this)">All Evaluated (394)</div>
            <div class="pill" onclick="setFilter('top10', this)">Unstop Top 10</div>
            <div class="pill" onclick="setFilter('free_agent', this)" style="border-left: 2px solid #10b981;">Auction Free Agents</div>
            <div class="pill" onclick="setFilter('ineligible', this)" style="border-left: 2px solid #dc2626; color: #fca5a5;">BCCI Ineligible / Non-IPL</div>
            <div class="pill" onclick="setFilter('traded', this)" style="border-left: 2px solid #f59e0b;">Confirmed Trades</div>
            <div class="pill" onclick="setFilter('watchlist', this)" style="border-left: 2px solid #eab308;">Release Watch & Opt-Outs</div>
            <div class="pill" onclick="setFilter('rr_core', this)" style="border-left: 2px solid #f43f5e;">RR Core Retained</div>
            <div class="pill" onclick="setFilter('untouchable', this)" style="border-left: 2px solid #6366f1;">Franchise Untouchables</div>
            <div class="pill" onclick="setFilter('global_steal', this)">Global Steals</div>
          </div>
        </div>
        <div class="toolbar-right">
          <input type="text" id="searchInput" class="search-input" placeholder="Search player or team..." oninput="renderTable()">
          <select id="sortSelect" class="sort-select" onchange="renderTable()">
            <option value="rpcs">Sort: RPCS Rating</option>
            <option value="rate">Sort: Pressure SR / Econ</option>
            <option value="kappa">Sort: Retention Ratio (κ)</option>
            <option value="wpa">Sort: Win Probability Added (WPA)</option>
            <option value="csr">Sort: Clutch Success Rate (CSR)</option>
            <option value="scs">Sort: Outlier Resilience (1-SCS)</option>
          </select>
        </div>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr id="tableHeaders"></tr>
          </thead>
          <tbody id="tableBody"></tbody>
        </table>
      </div>
    </div>

    <!-- TAB 2: REALISTIC AUCTION TARGET BOARD -->
    <div id="tab-auction" class="tab-view">
      <div style="margin-bottom: 16px;">
        <h2 style="font-size: 20px; font-weight: 700; color: var(--slate-50);">IPL 2027 Auction War Room: Actionable Target Board</h2>
        <p style="color: var(--slate-400); font-size: 13px; margin-top: 2px;">
          Separating untouchable core retentions (Kohli, Bumrah, SKY, Narine, Salt, Buttler) from high-leverage players Rajasthan Royals can <strong>actively bid for and buy</strong> at the mini-auction.
        </p>
      </div>

      <div style="background: rgba(220, 38, 38, 0.08); border-left: 4px solid #dc2626; padding: 12px 16px; border-radius: 6px; margin-bottom: 16px; font-size: 12px; color: var(--slate-300); line-height: 1.5;">
        <strong style="color: #ffffff;">BCCI Regulatory Eligibility Compliance:</strong> Pakistani players evaluated in our multi-competition dataset (such as Sufiyan Muqeem #2 Bowl, Mohammad Nawaz #8 Bowl, Abrar Ahmed #9 Bowl) are designated as <em>BCCI Ineligible / Non-IPL</em> and strictly excluded from this auction board under the standing 2008 BCCI policy. The board below contains strictly <strong>100% auction-eligible players</strong> available for acquisition by Rajasthan Royals.
      </div>

      <div class="toolbar">
        <div class="filter-pills">
          <div class="pill active" onclick="filterAuctionTargets('all', this)">All Actionable Targets</div>
          <div class="pill" onclick="filterAuctionTargets('released', this)" style="border-left: 2px solid #10b981;">Confirmed Released Free Agents</div>
          <div class="pill" onclick="filterAuctionTargets('global_steal', this)">Global Scouting Steals</div>
          <div class="pill" onclick="filterAuctionTargets('domestic', this)">Domestic Value Gems (&lt; ₹3 Cr)</div>
          <div class="pill" onclick="filterAuctionTargets('death', this)">Death Power Finishers</div>
          <div class="pill" onclick="filterAuctionTargets('spin', this)">Lockdown Spin Generals</div>
          <div class="pill" onclick="filterAuctionTargets('pace', this)">Death & PP Pace Enforcers</div>
        </div>
      </div>

      <div class="auction-grid" id="auctionGrid"></div>
    </div>

    <!-- TAB 3: CONTRACT & RELEASE TRACKER -->
    <div id="tab-contracts" class="tab-view">
      <div style="margin-bottom: 16px;">
        <h2 style="font-size: 20px; font-weight: 700; color: var(--slate-50);">IPL Contract & Release Lifecycle Audit (2024 → 2026/27)</h2>
        <p style="color: var(--slate-400); font-size: 13px; margin-top: 2px;">
          Ground-truth audit of player contracts across 5 IPL seasons in the data pack, identifying <strong>confirmed released free agents</strong>, <strong>eligible global steals</strong>, and <strong>regulatory compliance boundaries</strong>.
        </p>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin-bottom: 20px;">
        <div class="modal-section" style="border-left: 3px solid #10b981;">
          <h4 style="color: #34d399;">Pool 1: Confirmed Released Free Agents</h4>
          <p style="font-size: 12px; color: var(--slate-400); margin-bottom: 8px;">
            Played in IPL 2025 or earlier; confirmed released ahead of 2026/27 cycle. 100% unencumbered free agents entering the 2027 auction:
          </p>
          <ul style="font-size: 12px; padding-left: 18px; color: var(--slate-300); line-height: 1.8;">
            <li><strong style="color:var(--slate-50);">Nathan Ellis</strong> (Rank 15 Bowl | CSK 2025 → Released | 80% CSR death weapon)</li>
            <li><strong style="color:var(--slate-50);">Jonny Bairstow</strong> (Rank 32 Bat | MI 2025 → Released | 149.2 Press SR opener)</li>
            <li><strong style="color:var(--slate-50);">Glenn Maxwell</strong> (Rank 31 Bat, #76 Bowl | PBKS 2025 → Released | Spin destroyer)</li>
            <li><strong style="color:var(--slate-50);">Taskin Ahmed</strong> (Rank 10 Bowl | Unsold at ₹75L base price | 45.4% dots | 80.5% CSR)</li>
            <li><strong style="color:var(--slate-50);">Mujeeb Ur Rahman</strong> (Rank 11 Bowl | MI 2025 → Released | Econ 6.72)</li>
            <li><strong style="color:var(--slate-50);">Adam Zampa</strong> (Rank 20 Bowl | SRH 2025 → Released | Econ 7.40)</li>
            <li><strong style="color:var(--slate-50);">Mustafizur Rahman</strong> (Rank 23 Bowl | DC 2025 → Released | Cutter specialist)</li>
            <li><strong style="color:var(--slate-50);">Shamar Joseph</strong> (Rank 25 Bowl | LSG 2025 → Released | 150 kph Caribbean pace)</li>
          </ul>
        </div>

        <div class="modal-section" style="border-left: 3px solid #a855f7;">
          <h4 style="color: #d8b4fe;">Pool 2: 100% Eligible Global Scouting Steals</h4>
          <p style="font-size: 12px; color: var(--slate-400); margin-bottom: 8px;">
            Elite overseas performers with zero lifetime IPL contractual encumbrances (Base Price ₹0.50–2.0 Cr):
          </p>
          <ul style="font-size: 12px; padding-left: 18px; color: var(--slate-300); line-height: 1.8;">
            <li><strong style="color:var(--slate-50);">Hasan Mahmud</strong> (Rank 18 Bowl | Bangladesh | Econ 6.89 | CSR 72.2%)</li>
            <li><strong style="color:var(--slate-50);">Gudakesh Motie</strong> (Rank 26 Bowl | West Indies | Econ 7.81 | CSR 61.5%)</li>
            <li><strong style="color:var(--slate-50);">Ottneil Baartman</strong> (Rank 27 Bowl | South Africa | Econ 8.15 | CSR 58.3%)</li>
            <li><strong style="color:var(--slate-50);">Tim Southee</strong> (Rank 29 Bowl | New Zealand | Econ 7.91 | CSR 77.8%)</li>
            <li><strong style="color:var(--slate-50);">Reeza Hendricks</strong> (Rank 21 Bat | South Africa | Press SR 153.9 | CSR 71.0%)</li>
            <li><strong style="color:var(--slate-50);">Brian Bennett</strong> (Rank 47 Bat | Zimbabwe | Press SR 139.5 | CSR 61.5%)</li>
          </ul>
        </div>

        <div class="modal-section" style="border-left: 3px solid #f59e0b;">
          <h4 style="color: #fbbf24;">Pool 3: Confirmed Marquee Trades & Locked Assets</h4>
          <p style="font-size: 12px; color: var(--slate-400); margin-bottom: 8px;">
            Blockbuster trades confirmed ahead of the IPL 2027 auction:
          </p>
          <ul style="font-size: 12px; padding-left: 18px; color: var(--slate-300); line-height: 1.8;">
            <li><strong style="color:var(--slate-50);">Kuldeep Yadav</strong> (Rank 5 Bowl): Officially traded from Delhi Capitals to <strong>Lucknow Super Giants</strong> in direct swap for Rishabh Pant.</li>
            <li><strong style="color:var(--slate-50);">Rishabh Pant</strong>: Officially traded from Lucknow Super Giants to <strong>Delhi Capitals</strong> to captain DC.</li>
          </ul>
        </div>

        <div class="modal-section" style="border-left: 3px solid #eab308;">
          <h4 style="color: #facc15;">Pool 4: Watchlist & Workload Opt-Outs</h4>
          <p style="font-size: 12px; color: var(--slate-400); margin-bottom: 8px;">
            Players under active watch for non-retention or workload opt-outs:
          </p>
          <ul style="font-size: 12px; padding-left: 18px; color: var(--slate-300); line-height: 1.8;">
            <li><strong style="color:var(--slate-50);">Travis Head</strong> (Rank 8 Bat | SRH): Likely released after indicating intentions to opt out of IPL 2027 to manage Cricket Australia international workload.</li>
            <li><strong style="color:var(--slate-50);">Matheesha Pathirana</strong> (Rank 7 Bowl | KKR): Signed at ₹18 Cr in 2026; major release candidate to free up auction funds.</li>
          </ul>
        </div>

        <div class="modal-section" style="border-left: 3px solid #dc2626;">
          <h4 style="color: #f87171;">Pool 5: BCCI Regulatory Ineligible Benchmarks</h4>
          <p style="font-size: 12px; color: var(--slate-400); margin-bottom: 8px;">
            27 Pakistani players evaluated strictly as international statistical benchmarks:
          </p>
          <ul style="font-size: 12px; padding-left: 18px; color: var(--slate-300); line-height: 1.8;">
            <li><strong style="color:var(--slate-50);">Sufiyan Muqeem</strong> (Rank 2 Bowl | CSR 83.3% | 47.1% Dots | Ineligible under 2008 BCCI policy)</li>
            <li><strong style="color:var(--slate-50);">Mohammad Nawaz</strong> (Rank 8 Bowl, #95 Bat | Dual-role international benchmark)</li>
            <li><strong style="color:var(--slate-50);">Abrar Ahmed</strong> (Rank 9 Bowl | Econ 6.42 | CSR 75.0%)</li>
            <li><strong style="color:var(--slate-50);">Shaheen Afridi, Haris Rauf, Naseem Shah, Babar Azam, Fakhar Zaman, Mohammad Rizwan</strong></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- TAB 4: SCATTER EXPLORER -->
    <div id="tab-scatter" class="tab-view">
      <div class="chart-panel">
        <div class="chart-header">
          <div>
            <h3 id="scatterTitle" style="font-size: 16px; font-weight: 700; color: var(--slate-50);">Batting Pressure Strike Rate vs. Clutch Success Rate (CSR)</h3>
            <p style="color: var(--slate-400); font-size: 12px;">Top-right quadrant identifies elite performers who combine acceleration with match consistency under duress.</p>
          </div>
          <div class="role-toggle">
            <button id="scatter-bat-btn" class="role-btn active" onclick="setScatterRole('batters')">Batters</button>
            <button id="scatter-bowl-btn" class="role-btn" onclick="setScatterRole('bowlers')">Bowlers</button>
          </div>
        </div>

        <div class="scatter-legend">
          <div class="legend-item"><span class="legend-dot" style="background:#dc2626;"></span> BCCI Ineligible (Pak)</div>
          <div class="legend-item"><span class="legend-dot" style="background:#10b981;"></span> Released Free Agent</div>
          <div class="legend-item"><span class="legend-dot" style="background:#f59e0b;"></span> Confirmed Trade</div>
          <div class="legend-item"><span class="legend-dot" style="background:#eab308;"></span> Watchlist / Opt-Out</div>
          <div class="legend-item"><span class="legend-dot" style="background:#f43f5e;"></span> RR Core Retained</div>
          <div class="legend-item"><span class="legend-dot" style="background:#6366f1;"></span> Franchise Untouchable</div>
          <div class="legend-item"><span class="legend-dot" style="background:#a855f7;"></span> Global Steal</div>
          <div class="legend-item"><span class="legend-dot" style="background:#64748b;"></span> Auction Target</div>
        </div>

        <div class="chart-box">
          <canvas id="scatterCanvas"></canvas>
          <div id="scatterTooltip"></div>
        </div>
      </div>
    </div>

    <!-- TAB 5: RADAR COMPARATOR -->
    <div id="tab-radar" class="tab-view">
      <div class="chart-panel">
        <div class="chart-header">
          <div>
            <h3 style="font-size: 16px; font-weight: 700; color: var(--slate-50);">Multi-Moment 6-Axis Radar Comparison Engine</h3>
            <p style="color: var(--slate-400); font-size: 12px;">Compare any two players in the 394-player database across Volume, WPA, Par Differential, κ Retention, CSR, and Outlier Resilience.</p>
          </div>
          <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <select id="radarPlayer1" class="sort-select" onchange="drawRadar()"></select>
            <select id="radarPlayer2" class="sort-select" onchange="drawRadar()"></select>
          </div>
        </div>
        <div class="chart-box" style="height: 480px;">
          <canvas id="radarCanvas"></canvas>
        </div>
      </div>
    </div>

    <!-- TAB 6: XI BUILDER -->
    <div id="tab-xibuilder" class="tab-view">
      <div style="margin-bottom: 16px;">
        <h2 style="font-size: 20px; font-weight: 700; color: var(--slate-50);">Rajasthan Royals IPL 2027 Clutch XI Builder & Purse Tracker</h2>
        <p style="color: var(--slate-400); font-size: 13px; margin-top: 2px;">Simulating Rajasthan Royals' starting lineup combining retained core with targeted free-agent acquisitions within the ₹120.0 Cr purse cap.</p>
      </div>

      <!-- Live ₹120 Cr Purse Tracker -->
      <div class="purse-tracker">
        <div class="purse-grid">
          <div>
            <div class="purse-item-lbl">Total Auction Purse</div>
            <div class="purse-item-val">₹120.00 Cr</div>
          </div>
          <div>
            <div class="purse-item-lbl">Allocated XI Spend</div>
            <div class="purse-item-val" style="color: #34d399;">₹113.60 Cr</div>
          </div>
          <div>
            <div class="purse-item-lbl">Purse Remaining</div>
            <div class="purse-item-val" style="color: #fbbf24;">₹6.40 Cr</div>
          </div>
          <div>
            <div class="purse-item-lbl">Team Clutch Index</div>
            <div class="purse-item-val" style="color: #fb7185;"><span id="teamClutchIndex">65.3</span>/100</div>
          </div>
        </div>
        <div class="purse-progress-bar">
          <div class="purse-progress-fill"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--slate-400); margin-top:6px;">
          <span>XI Salary Cap Utilization: 94.7%</span>
          <span>Bench & Contingency Reserve: ₹6.40 Cr</span>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div class="modal-section">
          <h3 style="font-size: 14px; font-weight: 700; color: var(--slate-50); margin-bottom: 12px;">Royals Projected Starting XI</h3>
          <div id="xiSlotsList"></div>
        </div>

        <div class="modal-section">
          <h3 style="font-size: 14px; font-weight: 700; color: var(--slate-50); margin-bottom: 12px;">Tactical War-Room Squad Synergy</h3>
          <div style="background: var(--slate-900); border-left: 3px solid #f43f5e; border-radius: 6px; padding: 12px; margin-bottom: 10px; font-size: 12px;">
            <strong style="color: var(--slate-50);">Opening Pair Mastery:</strong> Yashasvi Jaiswal (#6) + Vaibhav Sooryavanshi (#7 Orange Cap / MVP) form a hyper-explosive opening duo with an average RPCS of 72.4.
          </div>
          <div style="background: var(--slate-900); border-left: 3px solid #10b981; border-radius: 6px; padding: 12px; margin-bottom: 10px; font-size: 12px;">
            <strong style="color: var(--slate-50);">Free-Agent Power Finishers:</strong> Acquiring Jonny Bairstow (₹6.5 Cr) and Glenn Maxwell (₹5.5 Cr) from the confirmed released free-agent pool injects proven death-overs boundary power.
          </div>
          <div style="background: var(--slate-900); border-left: 3px solid #6366f1; border-radius: 6px; padding: 12px; margin-bottom: 10px; font-size: 12px;">
            <strong style="color: var(--slate-50);">Spin Suppression Tandem:</strong> Ravindra Jadeja (#8) and Ravi Bishnoi (#10) generate 8 overs of relentless middle-overs boundary suppression.
          </div>
          <div style="background: var(--slate-900); border-left: 3px solid #eab308; border-radius: 6px; padding: 12px; font-size: 12px;">
            <strong style="color: var(--slate-50);">Death Yorker & Pace Shock:</strong> Jofra Archer (150+ kph) paired with Sandeep Sharma (66.8 RPCS) provides impenetrable death-overs execution.
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 7: CASE STUDIES -->
    <div id="tab-cases" class="tab-view">
      <div class="case-grid">
        <div class="case-card">
          <div class="case-badge">Match 31250 • KKR vs RR (2024)</div>
          <div class="case-title">Jos Buttler's Impossible Chase</div>
          <div class="case-impact">ΔWPA: +1.069 • 107* (65 balls) • Won by 2 wickets</div>
          <p class="case-desc">
            RR slumped to 121/6 in 12.2 overs chasing 224 (Win Probability = 4%). Battling severe physical cramps, Buttler batted with tailenders, hitting a six on the penultimate delivery and single on the last ball to seal the highest single-match pressure batting WPA in modern IPL history.
          </p>
        </div>

        <div class="case-card">
          <div class="case-badge">Match 31251 • PBKS vs MI (2024)</div>
          <div class="case-title">Jasprit Bumrah's Mullanpur Masterclass</div>
          <div class="case-impact">ΔWPA: +0.318 • 3/19 in 24 balls (Econ 4.75) • Won by 9 runs</div>
          <p class="case-desc">
            Defending 192, Punjab's lower order mounted a furious counterattack (45 needed off 30 balls, WP 64%). Bumrah was deployed across overs 2, 13, and 17, dismantling Rossouw and Curran to depress Punjab's win probability down to 12% in a defensive masterclass.
          </p>
        </div>

        <div class="case-card">
          <div class="case-badge">Match 40720 • SRH vs PBKS (2025)</div>
          <div class="case-title">Abhishek Sharma's Blitzkrieg Decimation</div>
          <div class="case-impact">ΔWPA: +0.662 • 128 (53 balls) • 8-Wicket Runaway Victory</div>
          <p class="case-desc">
            Chasing 215 with a required rate of 10.75 from ball 1, Abhishek demolished the bowling attack in the powerplay and middle overs under sustained high leverage. His SCS of 0.059 confirms this is a repeatable pattern across 68.4% of his pressure matches.
          </p>
        </div>

        <div class="case-card">
          <div class="case-badge">Match 50138 • DC vs GT (2026)</div>
          <div class="case-title">Rashid Khan's 1-Run Defence</div>
          <div class="case-impact">ΔWPA: +0.544 • 3/17 in 24 balls (Econ 4.25) • Won by 1 run</div>
          <p class="case-desc">
            Defending a modest 158, Delhi Capitals cruised to 95/2 needing 64 off 48 balls (WP 82%). Rashid bowled overs 11, 13, 15, and 17, taking 3 key wickets to trigger a catastrophic batting collapse that preserved a 1-run triumph.
          </p>
        </div>
      </div>
    </div>

    <!-- TAB 8: METHODOLOGY PROOFS -->
    <div id="tab-math" class="tab-view">
      <div class="chart-panel">
        <h2 style="font-size: 20px; font-weight: 700; color: var(--slate-50); margin-bottom: 16px;">Core Mathematical Modeling Architecture</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
          <div class="modal-section">
            <h4 style="color: #34d399;">1. Zero-Boundary 1st Innings Expected Runs</h4>
            <p style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #34d399; margin: 8px 0;">
              R_rem(b, w) = b * (2.591 - 1.232*(b/120) - 1.296*(w/10))
            </p>
            <p style="font-size: 12px; color: var(--slate-400); line-height: 1.6;">
              Guarantees boundary conservation: R_rem ≡ 0 when balls b ≤ 0, and clamped to 0 when wickets w ≥ 10 (all-out). Total projected runs S_pred = S_curr + R_rem maps to win probability via logistic link against era par.
            </p>
          </div>

          <div class="modal-section">
            <h4 style="color: #34d399;">2. Calibrated 2nd Innings Logistic Model</h4>
            <p style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #34d399; margin: 8px 0;">
              logit(P) = 2.297 - 0.013*R_need - 0.019*b_rem + 0.627*W_hand - 2.799*(R_need/(b_rem+1))
            </p>
            <p style="font-size: 12px; color: var(--slate-400); line-height: 1.6;">
              Trained across 95,134 clean match deliveries (AUC = 0.895, Brier = 0.132). Dominant rule: WP ≡ 1.0 strictly if R_needed ≤ 0 (target achieved), regardless of wickets fallen.
            </p>
          </div>

          <div class="modal-section">
            <h4 style="color: #34d399;">3. Multiplicative Retention Ratio (κ)</h4>
            <p style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #34d399; margin: 8px 0;">
              κ_bat = SR_press / SR_base  |  κ_bowl = Econ_base / Econ_press
            </p>
            <p style="font-size: 12px; color: var(--slate-400); line-height: 1.6;">
              Eliminates the Baseline Penalty Fallacy by rewarding players who retain or amplify performance under maximum duress rather than rewarding low-baseline accumulators.
            </p>
          </div>

          <div class="modal-section">
            <h4 style="color: #34d399;">4. Non-Striker WPA Conservation</h4>
            <p style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #34d399; margin: 8px 0;">
              ΔWP_striker + ΔWP_dismissed ≡ ΔWP_delivery
            </p>
            <p style="font-size: 12px; color: var(--slate-400); line-height: 1.6;">
              Credits striker for runs scored while isolating negative wicket loss debit against the 271 non-striker run-outs and Tilak Varma's tactical retire-out (Match 40709).
            </p>
          </div>
        </div>
      </div>
    </div>

  </div>

  <!-- PLAYER CARD MODAL (Shadcn Dialog Style) -->
  <div id="playerModal" class="modal-overlay" onclick="closeModal(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <button class="modal-close" onclick="closeModal()">&times;</button>
      <div class="modal-header">
        <h2 id="mName">Player Name <span id="mTag" class="badge badge-free-agent">Free Agent</span></h2>
        <p id="mRole" style="color: var(--slate-400); font-size: 12px; margin-top: 2px;">Role Title</p>
      </div>

      <div id="mAlertContainer"></div>

      <div class="modal-grid">
        <div class="modal-section">
          <h4>Clutch Performance Metrics</h4>
          <div class="info-row"><span>RPCS Rating</span><span id="mRPCS" class="num-tabular">80.46</span></div>
          <div class="info-row"><span>Pressure Balls</span><span id="mBalls" class="num-tabular">1,242</span></div>
          <div class="info-row"><span id="mRateLbl">Pressure SR</span><span id="mRate" class="num-tabular">174.8</span></div>
          <div class="info-row"><span id="mBaseLbl">Baseline SR</span><span id="mBaseRate" class="num-tabular">186.9</span></div>
          <div class="info-row"><span>Retention Ratio (κ)</span><span id="mKappa" class="num-tabular">0.935</span></div>
          <div class="info-row"><span>Win Probability Added (WPA)</span><span id="mWPA" class="num-tabular">+6.63</span></div>
          <div class="info-row"><span id="mParLbl">Runs Above Par (BRA)</span><span id="mPar" class="num-tabular">+425.2</span></div>
          <div class="info-row"><span>Clutch Success Rate (CSR)</span><span id="mCSR" class="num-tabular">68.4%</span></div>
          <div class="info-row"><span>Outlier Spike Share (SCS)</span><span id="mSCS" class="num-tabular">0.059</span></div>
        </div>

        <div class="modal-section">
          <h4>Phase Execution Breakdown</h4>
          <div class="info-row"><span id="mPh1Lbl">Powerplay</span><span id="mPh1" class="num-tabular">997 balls | 173.9 SR</span></div>
          <div class="info-row"><span id="mPh2Lbl">Middle Overs</span><span id="mPh2" class="num-tabular">191 balls | 173.3 SR</span></div>
          <div class="info-row"><span id="mPh3Lbl">Death Overs</span><span id="mPh3" class="num-tabular">54 balls | 196.3 SR</span></div>
          <div class="info-row"><span>Boundary Percentage</span><span id="mBdry" class="num-tabular">28.6%</span></div>
          <div class="info-row"><span>Dot Ball Percentage</span><span id="mDot" class="num-tabular">37.0%</span></div>
        </div>
      </div>

      <!-- Contract Progression Section -->
      <div class="modal-section" style="margin-bottom: 16px;">
        <h4>Empirical IPL Contract Lifecycle (2024 → 2026/27)</h4>
        <div class="journey-tracker">
          <div class="journey-step">
            <div class="journey-year">IPL 2024 Team</div>
            <div class="journey-team" id="mTeam24">Kolkata Knight Riders</div>
          </div>
          <div class="journey-step">
            <div class="journey-year">IPL 2025 Team</div>
            <div class="journey-team" id="mTeam25">Mumbai Indians</div>
          </div>
          <div class="journey-step">
            <div class="journey-year">IPL 2026/27 Status</div>
            <div class="journey-team" id="mTeam26" style="color: #34d399;">RELEASED (Free Agent)</div>
          </div>
        </div>
      </div>

      <div class="modal-section">
        <h4>Rajasthan Royals Scouting & Auction Intelligence</h4>
        <div class="info-row"><span>Auction Availability Verdict</span><span id="mStatus" style="color: #fbbf24;">Released Free Agent</span></div>
        <div class="info-row"><span>Estimated Auction Bracket</span><span id="mTier" style="color: #34d399;">₹2.0 - 4.0 Cr</span></div>
        <div style="margin-top: 10px; font-size: 12px; color: var(--slate-300); line-height: 1.6;" id="mNote">
          Played for MI in 2025; released ahead of 2026. 100% auction free agent entering IPL 2027.
        </div>
      </div>
    </div>
  </div>

  <footer>
    <p>Rajasthan Royals SupeRR Selector Season 2 • Built by Yash Agarwal • Verified across 200,987 deliveries & 5 IPL Seasons</p>
  </footer>

  <script>
    // Embedded Dataset
    const DATA = """ + data_json_str + """;

    let currentRole = 'batters';
    let currentFilter = 'all';
    let currentSearch = '';

    // Central Status Classifier
    function getPlayerStatusInfo(p) {
      const badgeType = p.badge_type || 'auction_target';
      if (badgeType === 'ineligible' || p.country === 'Pakistan') {
        return {
          type: 'ineligible',
          badgeClass: 'badge-ineligible',
          rowClass: 'row-ineligible',
          label: p.badge_label || 'BCCI INELIGIBLE / NON-IPL',
          color: '#ef4444'
        };
      }
      if (badgeType === 'free_agent' || (p.avail_type && p.avail_type.includes('Released'))) {
        return {
          type: 'free_agent',
          badgeClass: 'badge-free-agent',
          rowClass: 'row-free-agent',
          label: p.badge_label || 'AUCTION FREE AGENT',
          color: '#10b981'
        };
      }
      if (badgeType === 'traded') {
        return {
          type: 'traded',
          badgeClass: 'badge-traded',
          rowClass: 'row-traded',
          label: p.badge_label || 'CONFIRMED TRADE',
          color: '#f59e0b'
        };
      }
      if (badgeType === 'release_watch') {
        return {
          type: 'release_watch',
          badgeClass: 'badge-watchlist',
          rowClass: 'row-watchlist',
          label: p.badge_label || 'RELEASE WATCH',
          color: '#eab308'
        };
      }
      if (badgeType === 'retention' || p.avail_type === 'Untouchable Retention') {
        return {
          type: 'retention',
          badgeClass: 'badge-retention',
          rowClass: 'row-retention',
          label: p.badge_label || 'UNTOUCHABLE CORE',
          color: '#6366f1'
        };
      }
      if (badgeType === 'rr_core' || p.avail_type === 'RR Active Squad') {
        return {
          type: 'rr_core',
          badgeClass: 'badge-rr-core',
          rowClass: 'row-rr-core',
          label: p.badge_label || 'RR CORE / RETAINED',
          color: '#f43f5e'
        };
      }
      if (badgeType === 'global_steal') {
        return {
          type: 'global_steal',
          badgeClass: 'badge-global-steal',
          rowClass: '',
          label: p.badge_label || 'GLOBAL STEAL',
          color: '#a855f7'
        };
      }
      if (badgeType === 'domestic_steal') {
        return {
          type: 'domestic_steal',
          badgeClass: 'badge-domestic-steal',
          rowClass: '',
          label: p.badge_label || 'DOMESTIC STEAL',
          color: '#0ea5e9'
        };
      }
      return {
        type: 'auction_target',
        badgeClass: 'badge-auction-target',
        rowClass: '',
        label: p.badge_label || 'AUCTION TARGET',
        color: '#64748b'
      };
    }

    // Switch Tab
    function switchTab(tabId, e) {
      document.querySelectorAll('.tab-view').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
      const targetTab = document.getElementById('tab-' + tabId);
      if (targetTab) targetTab.classList.add('active');
      if (e && e.target) e.target.classList.add('active');
      if (tabId === 'scatter') drawScatter();
      if (tabId === 'radar') initRadar();
    }

    // Role Switch
    function setRole(role) {
      currentRole = role;
      document.getElementById('btn-batters').classList.toggle('active', role === 'batters');
      document.getElementById('btn-bowlers').classList.toggle('active', role === 'bowlers');
      renderTable();
    }

    // Filter Switch
    function setFilter(filter, el) {
      currentFilter = filter;
      document.querySelectorAll('#tab-roster .pill').forEach(p => p.classList.remove('active'));
      el.classList.add('active');
      renderTable();
    }

    // Render Table
    function renderTable() {
      const isBat = currentRole === 'batters';
      const players = DATA[currentRole];
      const search = (document.getElementById('searchInput').value || '').toLowerCase().trim();
      const sortBy = document.getElementById('sortSelect').value;

      // Filter
      let filtered = players.filter(p => {
        if (search) {
          const matchName = p.name.toLowerCase().includes(search);
          const matchTeam = (p.team_2026 || '').toLowerCase().includes(search);
          const matchCountry = (p.country || '').toLowerCase().includes(search);
          if (!matchName && !matchTeam && !matchCountry) return false;
        }

        const sInfo = getPlayerStatusInfo(p);
        if (currentFilter === 'top10') return p.rank <= 10;
        if (currentFilter === 'free_agent') return sInfo.type === 'free_agent';
        if (currentFilter === 'ineligible') return sInfo.type === 'ineligible';
        if (currentFilter === 'traded') return sInfo.type === 'traded';
        if (currentFilter === 'watchlist') return sInfo.type === 'release_watch';
        if (currentFilter === 'rr_core') return sInfo.type === 'rr_core';
        if (currentFilter === 'untouchable') return sInfo.type === 'retention';
        if (currentFilter === 'global_steal') return sInfo.type === 'global_steal';
        return true;
      });

      // Sort
      filtered.sort((a, b) => {
        if (sortBy === 'rpcs') return b.rpcs - a.rpcs;
        if (sortBy === 'rate') return isBat ? (b.press_sr - a.press_sr) : (a.press_econ - b.press_econ);
        if (sortBy === 'kappa') return b.kappa - a.kappa;
        if (sortBy === 'wpa') return b.wpa - a.wpa;
        if (sortBy === 'csr') return b.csr - a.csr;
        if (sortBy === 'scs') return a.scs - b.scs;
        return 0;
      });

      // Headers
      const thead = document.getElementById('tableHeaders');
      thead.innerHTML = `
        <th>Rank</th>
        <th>Player</th>
        <th>Country</th>
        <th>2026 Status & Trade Intelligence</th>
        <th class="num-tabular">Pressure Balls</th>
        <th class="num-tabular">${isBat ? 'Press SR' : 'Press Econ'}</th>
        <th class="num-tabular">${isBat ? 'Base SR' : 'Base Econ'}</th>
        <th class="num-tabular">Retention (κ)</th>
        <th class="num-tabular">WPA</th>
        <th class="num-tabular">${isBat ? 'BRA' : 'BRS'}</th>
        <th class="num-tabular">CSR (%)</th>
        <th class="num-tabular">SCS</th>
        <th class="num-tabular">RPCS</th>
      `;

      // Body
      const tbody = document.getElementById('tableBody');
      tbody.innerHTML = filtered.map(p => {
        const sInfo = getPlayerStatusInfo(p);
        return `
          <tr class="${sInfo.rowClass}" onclick="openModal('${p.name}', '${currentRole}')">
            <td class="rank-cell ${p.rank <= 3 ? 'top3' : ''}">#${p.rank}</td>
            <td>
              <div class="player-name-cell">
                <span class="name-title">${p.name}</span>
                <span class="name-team-sub">${p.team_2026}</span>
              </div>
            </td>
            <td style="color:var(--slate-400);">${p.country || 'India'}</td>
            <td><span class="badge ${sInfo.badgeClass}">${sInfo.label}</span></td>
            <td class="num-tabular">${p.press_balls.toLocaleString()}</td>
            <td class="num-tabular" style="font-weight:700; color:${isBat ? 'var(--slate-50)' : '#34d399'};">${isBat ? p.press_sr : p.press_econ}</td>
            <td class="num-tabular" style="color:var(--slate-400);">${isBat ? p.base_sr : p.base_econ}</td>
            <td class="num-tabular" style="font-weight:700; color:${p.kappa >= 1.0 ? '#34d399' : 'var(--slate-400)'};">${p.kappa}</td>
            <td class="num-tabular" style="font-weight:700; color:${p.wpa >= 0 ? '#34d399' : '#f87171'};">${p.wpa >= 0 ? '+' : ''}${p.wpa}</td>
            <td class="num-tabular">${p.bra !== undefined ? (p.bra > 0 ? '+' + p.bra : p.bra) : (p.brs > 0 ? '+' + p.brs : p.brs)}</td>
            <td class="num-tabular" style="font-weight:700;">${p.csr}%</td>
            <td class="num-tabular">${p.scs}</td>
            <td class="num-tabular"><span class="rpcs-pill ${p.rpcs >= 75 ? 'elite' : ''}">${p.rpcs}</span></td>
          </tr>
        `;
      }).join('');
    }

    // Modal
    function openModal(name, role) {
      const p = DATA[role].find(x => x.name === name);
      if (!p) return;
      const isBat = role === 'batters';
      const sInfo = getPlayerStatusInfo(p);

      document.getElementById('mName').innerHTML = `${p.name} <span class="badge ${sInfo.badgeClass}">${sInfo.label}</span>`;
      document.getElementById('mRole').innerText = `${p.role} • ${p.country || 'India'}`;
      document.getElementById('mRPCS').innerText = p.rpcs;
      document.getElementById('mBalls').innerText = p.press_balls.toLocaleString();
      document.getElementById('mRateLbl').innerText = isBat ? 'Pressure Strike Rate' : 'Pressure Economy';
      document.getElementById('mRate').innerText = isBat ? p.press_sr : p.press_econ;
      document.getElementById('mBaseLbl').innerText = isBat ? 'Baseline Strike Rate' : 'Baseline Economy';
      document.getElementById('mBaseRate').innerText = isBat ? p.base_sr : p.base_econ;
      document.getElementById('mKappa').innerText = p.kappa + (p.kappa >= 1.0 ? ' (Amplifies Under Pressure)' : ' (Mild Regression)');
      document.getElementById('mWPA').innerText = (p.wpa >= 0 ? '+' : '') + p.wpa;
      document.getElementById('mParLbl').innerText = isBat ? 'Runs Above Par (BRA)' : 'Bowling Runs Saved (BRS)';
      document.getElementById('mPar').innerText = isBat ? (p.bra > 0 ? '+' + p.bra : p.bra) : (p.brs > 0 ? '+' + p.brs : p.brs);
      document.getElementById('mCSR').innerText = p.csr + '%';
      document.getElementById('mSCS').innerText = p.scs + (p.scs < 0.1 ? ' (Ultra-Consistent)' : ' (Moderate Concentration)');

      document.getElementById('mPh1').innerText = `${p.pp_balls} balls | ${isBat ? p.pp_sr + ' SR' : p.pp_econ + ' Econ' + (p.pp_wkts !== undefined ? ' (' + p.pp_wkts + ' Wkts)' : '')}`;
      document.getElementById('mPh2').innerText = `${p.mid_balls} balls | ${isBat ? p.mid_sr + ' SR' : p.mid_econ + ' Econ' + (p.mid_wkts !== undefined ? ' (' + p.mid_wkts + ' Wkts)' : '')}`;
      document.getElementById('mPh3').innerText = `${p.death_balls} balls | ${isBat ? p.death_sr + ' SR' : p.death_econ + ' Econ' + (p.death_wkts !== undefined ? ' (' + p.death_wkts + ' Wkts)' : '')}`;
      document.getElementById('mBdry').innerText = (p.bdry_pct !== undefined ? p.bdry_pct + '%' : 'N/A');
      document.getElementById('mDot').innerText = p.dot_pct + '%';

      // Contract history
      document.getElementById('mTeam24').innerText = p.team_2024 || 'None';
      document.getElementById('mTeam25').innerText = p.team_2025 || 'None';
      document.getElementById('mTeam26').innerText = p.team_2026 || 'Free Agent';

      document.getElementById('mStatus').innerText = sInfo.label;
      document.getElementById('mTier').innerText = p.est_price || p.tier || 'Base Price';
      document.getElementById('mNote').innerText = p.trade_notes || p.desc || p.rr_note;

      // Status Alert Box
      const alertContainer = document.getElementById('mAlertContainer');
      let alertHtml = '';
      if (sInfo.type === 'ineligible') {
        alertHtml = `
          <div class="modal-alert-box alert-ineligible">
            <strong>⚠️ BCCI Regulatory Ineligibility:</strong> This player is ineligible for IPL player auctions, registration, or franchise squad selection under standing BCCI policy restricting Pakistan-registered players enacted in 2008. Evaluated strictly as an international statistical benchmark for multi-moment pressure modeling.
          </div>
        `;
      } else if (sInfo.type === 'traded') {
        alertHtml = `
          <div class="modal-alert-box alert-traded">
            <strong>🔄 Confirmed Franchise Trade:</strong> ${p.trade_notes || 'Officially traded and locked ahead of IPL 2027.'}
          </div>
        `;
      } else if (sInfo.type === 'release_watch') {
        alertHtml = `
          <div class="modal-alert-box alert-watchlist">
            <strong>⚠️ High-Risk Watchlist / Opt-Out:</strong> ${p.trade_notes || 'Release candidate or workload management opt-out.'}
          </div>
        `;
      } else if (sInfo.type === 'free_agent') {
        alertHtml = `
          <div class="modal-alert-box alert-free-agent">
            <strong>✅ Confirmed Unencumbered Free Agent:</strong> ${p.trade_notes || 'Confirmed not retained; 100% available auction buy.'}
          </div>
        `;
      } else if (sInfo.type === 'retention') {
        alertHtml = `
          <div class="modal-alert-box alert-retention">
            <strong>👑 Franchise Core Untouchable Retention:</strong> ${p.trade_notes || 'Non-negotiable franchise retention.'}
          </div>
        `;
      } else if (sInfo.type === 'rr_core') {
        alertHtml = `
          <div class="modal-alert-box alert-rr-core">
            <strong>🌸 Rajasthan Royals Squad Core Asset:</strong> ${p.trade_notes || 'Active squad core asset for Rajasthan Royals.'}
          </div>
        `;
      }
      alertContainer.innerHTML = alertHtml;

      document.getElementById('playerModal').classList.add('active');
    }

    function closeModal() {
      document.getElementById('playerModal').classList.remove('active');
    }

    // Auction Board
    function renderAuctionBoard(filterType) {
      const grid = document.getElementById('auctionGrid');
      // Exclude Untouchables, RR Core, Traded players, and Ineligible Pakistani players
      const allTargets = [
        ...DATA.batters.filter(p => p.badge_type !== 'retention' && p.badge_type !== 'ineligible' && p.badge_type !== 'rr_core' && p.badge_type !== 'traded'),
        ...DATA.bowlers.filter(p => p.badge_type !== 'retention' && p.badge_type !== 'ineligible' && p.badge_type !== 'rr_core' && p.badge_type !== 'traded')
      ];

      let targets = allTargets;
      if (filterType === 'released') targets = allTargets.filter(p => p.badge_type === 'free_agent');
      if (filterType === 'global_steal') targets = allTargets.filter(p => p.badge_type === 'global_steal');
      if (filterType === 'domestic') targets = allTargets.filter(p => p.badge_type === 'domestic_steal');
      if (filterType === 'death') targets = allTargets.filter(p => p.role && (p.role.toLowerCase().includes('death') || p.role.toLowerCase().includes('finisher')));
      if (filterType === 'spin') targets = allTargets.filter(p => p.role && p.role.toLowerCase().includes('spin'));
      if (filterType === 'pace') targets = allTargets.filter(p => p.role && (p.role.toLowerCase().includes('pace') || p.role.toLowerCase().includes('slinger') || p.role.toLowerCase().includes('yorker')));

      // Sort by RPCS
      targets.sort((a,b) => b.rpcs - a.rpcs);

      grid.innerHTML = targets.map(p => {
        const sInfo = getPlayerStatusInfo(p);
        const isPriority = sInfo.type === 'free_agent' || sInfo.type === 'global_steal';
        const roleKey = p.press_sr !== undefined ? 'batters' : 'bowlers';

        return `
          <div class="auction-card ${isPriority ? 'priority-card' : ''}" onclick="openModal('${p.name}', '${roleKey}')">
            <div class="auction-card-header">
              <div>
                <div class="auction-player-name">${p.name}</div>
                <div class="auction-role">${p.role}</div>
              </div>
              <div style="display:flex; flex-direction:column; align-items:flex-end; gap:4px;">
                <span class="badge ${sInfo.badgeClass}">${sInfo.label}</span>
                <div class="auction-price-tag">${p.est_price || p.tier || '₹0.5–2.0 Cr'}</div>
              </div>
            </div>
            <div class="auction-trail">
              <strong>IPL Trail:</strong> 2024: ${p.team_2024 || 'None'} → 2025: ${p.team_2025 || 'None'} → <strong>2026: ${p.team_2026}</strong><br>
              <span style="font-size:11px; color:var(--slate-400); margin-top:4px; display:inline-block;">${p.trade_notes || p.desc || p.rr_note}</span>
            </div>
            <div class="auction-stats-row">
              <div class="mini-stat-card">
                <div class="mini-stat-val">${p.rpcs}</div>
                <div class="mini-stat-lbl">RPCS Rating</div>
              </div>
              <div class="mini-stat-card">
                <div class="mini-stat-val">${p.press_sr !== undefined ? p.press_sr : p.press_econ}</div>
                <div class="mini-stat-lbl">${p.press_sr !== undefined ? 'Press SR' : 'Press Econ'}</div>
              </div>
              <div class="mini-stat-card">
                <div class="mini-stat-val">${p.csr}%</div>
                <div class="mini-stat-lbl">Clutch CSR</div>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    function filterAuctionTargets(type, el) {
      document.querySelectorAll('#tab-auction .pill').forEach(p => p.classList.remove('active'));
      el.classList.add('active');
      renderAuctionBoard(type);
    }

    // XI Builder
    const DEFAULT_XI = [
      { num: 1, role: 'Pressure Opener / Target Setter', name: 'Yashasvi Jaiswal', cost: '₹18.0 Cr', status: 'RR Retained Core', rpcs: 72.86 },
      { num: 2, role: 'Impact Hyper-Striker (221.5 SR)', name: 'Vaibhav Sooryavanshi', cost: '₹1.10 Cr', status: 'RR Retained Core (MVP)', rpcs: 71.91 },
      { num: 3, role: 'Top-Order WK / Boundary Enforcer', name: 'Jonny Bairstow', cost: '₹6.50 Cr', status: 'Free Agent Auction Buy', rpcs: 53.24 },
      { num: 4, role: 'Middle-Overs Anchor & Captain', name: 'Riyan Parag (C)', cost: '₹14.0 Cr', status: 'RR Retained Core', rpcs: 64.50 },
      { num: 5, role: 'Crisis Anchor / Wicketkeeper', name: 'Dhruv Jurel (WK)', cost: '₹14.0 Cr', status: 'RR Retained Core', rpcs: 68.20 },
      { num: 6, role: 'Specialist Death Power Closer', name: 'Shimron Hetmyer', cost: '₹11.0 Cr', status: 'RR Retained Core', rpcs: 67.40 },
      { num: 7, role: 'Spin Destroyer & Power Closer', name: 'Glenn Maxwell', cost: '₹5.50 Cr', status: 'Free Agent Auction Buy', rpcs: 53.52 },
      { num: 8, role: 'Elite Spin All-Rounder & Closer', name: 'Ravindra Jadeja', cost: '₹16.0 Cr', status: 'RR Active Asset', rpcs: 68.40 },
      { num: 9, role: 'Express Pace Enforcer (150+ kph)', name: 'Jofra Archer', cost: '₹12.5 Cr', status: 'RR Retained Core', rpcs: 65.20 },
      { num: 10, role: 'Attacking Wrist-Spin Squeeze', name: 'Ravi Bishnoi', cost: '₹11.0 Cr', status: 'RR Active Asset', rpcs: 66.40 },
      { num: 11, role: 'Veteran Death Yorker Operator', name: 'Sandeep Sharma', cost: '₹4.00 Cr', status: 'RR Retained Core', rpcs: 66.80 },
    ];

    function renderXI() {
      const container = document.getElementById('xiSlotsList');
      container.innerHTML = DEFAULT_XI.map(slot => `
        <div class="xi-slot">
          <div class="xi-slot-num">#${slot.num}</div>
          <div class="xi-slot-name">
            <div>${slot.name}</div>
            <div class="xi-slot-role">${slot.role} • <span style="color:var(--slate-400);">${slot.status}</span></div>
          </div>
          <div class="xi-slot-cost">${slot.cost}</div>
          <div class="xi-slot-rpcs">${slot.rpcs}</div>
        </div>
      `).join('');
      const avg = (DEFAULT_XI.reduce((acc, x) => acc + x.rpcs, 0) / DEFAULT_XI.length).toFixed(1);
      document.getElementById('teamClutchIndex').innerText = avg;
    }

    // Canvas Scatter Plot with Interactive Hover Tooltip
    let scatterRole = 'batters';
    let scatterPoints = [];

    function setScatterRole(role) {
      scatterRole = role;
      document.getElementById('scatter-bat-btn').classList.toggle('active', role === 'batters');
      document.getElementById('scatter-bowl-btn').classList.toggle('active', role === 'bowlers');
      document.getElementById('scatterTitle').innerText = role === 'batters'
        ? 'Batting Pressure Strike Rate vs. Clutch Success Rate (CSR)'
        : 'Bowling Pressure Economy Rate vs. Clutch Success Rate (CSR)';
      drawScatter();
    }

    function drawScatter(hoveredPoint = null) {
      const canvas = document.getElementById('scatterCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const width = canvas.parentElement.clientWidth;
      const height = canvas.parentElement.clientHeight;
      canvas.width = width * window.devicePixelRatio;
      canvas.height = height * window.devicePixelRatio;
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);

      const isBat = scatterRole === 'batters';
      const players = DATA[scatterRole];

      ctx.clearRect(0, 0, width, height);

      // Plot margins
      const pad = { top: 30, right: 30, bottom: 46, left: 54 };
      const plotW = width - pad.left - pad.right;
      const plotH = height - pad.top - pad.bottom;

      const xMin = isBat ? 110 : 4.5;
      const xMax = isBat ? 230 : 10.5;
      const yMin = 40;
      const yMax = 95;

      const getX = val => pad.left + ((val - xMin) / (xMax - xMin)) * plotW;
      const getY = val => pad.top + plotH - ((val - yMin) / (yMax - yMin)) * plotH;

      // Grid lines
      ctx.strokeStyle = '#1e293b';
      ctx.lineWidth = 1;
      for (let y = 50; y <= 90; y += 10) {
        ctx.beginPath();
        ctx.moveTo(pad.left, getY(y));
        ctx.lineTo(pad.left + plotW, getY(y));
        ctx.stroke();
        ctx.fillStyle = '#64748b';
        ctx.font = '10px JetBrains Mono, monospace';
        ctx.fillText(y + '%', pad.left - 34, getY(y) + 3);
      }

      const xStep = isBat ? 20 : 1;
      for (let x = xMin; x <= xMax; x += xStep) {
        ctx.beginPath();
        ctx.moveTo(getX(x), pad.top);
        ctx.lineTo(getX(x), pad.top + plotH);
        ctx.stroke();
        ctx.fillStyle = '#64748b';
        ctx.font = '10px JetBrains Mono, monospace';
        ctx.fillText(isBat ? x : x.toFixed(1), getX(x) - 10, pad.top + plotH + 18);
      }

      // Axis labels
      ctx.fillStyle = '#cbd5e1';
      ctx.font = '11px Inter, sans-serif';
      ctx.fillText(isBat ? 'Pressure Strike Rate →' : 'Pressure Economy (Lower is Better) ←', width / 2 - 80, height - 12);

      ctx.save();
      ctx.translate(16, height / 2 + 50);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText('Clutch Success Rate (CSR %) →', 0, 0);
      ctx.restore();

      // Cache scatter points for hit-testing
      scatterPoints = [];

      players.forEach(p => {
        const xVal = isBat ? p.press_sr : p.press_econ;
        const yVal = p.csr;
        const px = getX(xVal);
        const py = getY(yVal);
        const sInfo = getPlayerStatusInfo(p);
        const isTop10 = p.rank <= 10;
        const radius = isTop10 ? 5.5 : 3.5;

        scatterPoints.push({ player: p, x: px, y: py, r: radius, color: sInfo.color, statusInfo: sInfo });

        ctx.beginPath();
        ctx.arc(px, py, radius, 0, Math.PI * 2);
        ctx.fillStyle = sInfo.color;
        ctx.fill();

        // Label Top 5 or Free Agents in Top 20
        if (isTop10 || (sInfo.type === 'free_agent' && p.rank <= 25)) {
          ctx.fillStyle = '#e2e8f0';
          ctx.font = '600 10px Inter, sans-serif';
          const lastName = p.name.split(' ').pop();
          ctx.fillText(lastName, px + 7, py - 3);
        }
      });

      // Hover ring
      if (hoveredPoint) {
        ctx.beginPath();
        ctx.arc(hoveredPoint.x, hoveredPoint.y, hoveredPoint.r + 4, 0, Math.PI * 2);
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();
      }
    }

    // Attach Scatter Tooltip Events
    function setupScatterHover() {
      const canvas = document.getElementById('scatterCanvas');
      const tooltip = document.getElementById('scatterTooltip');
      if (!canvas || !tooltip) return;

      canvas.addEventListener('mousemove', e => {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;

        let nearest = null;
        let minDist = 14;

        for (let pt of scatterPoints) {
          const dist = Math.hypot(mx - pt.x, my - pt.y);
          if (dist < minDist) {
            minDist = dist;
            nearest = pt;
          }
        }

        if (nearest) {
          drawScatter(nearest);
          const p = nearest.player;
          const s = nearest.statusInfo;
          const isBat = scatterRole === 'batters';
          tooltip.style.display = 'block';
          tooltip.style.left = (mx + 15) + 'px';
          tooltip.style.top = Math.max(10, my - 30) + 'px';
          tooltip.innerHTML = `
            <div style="font-weight:700; color:#ffffff; font-size:12px;">${p.name} (#${p.rank})</div>
            <div style="color:${s.color}; font-weight:700; font-size:10px; margin:2px 0;">${s.label}</div>
            <div style="color:var(--slate-400); font-size:11px;">Team: ${p.team_2026}</div>
            <div style="margin-top:4px; font-family:'JetBrains Mono',monospace; font-size:11px;">
              <span>RPCS: <strong style="color:#fb7185;">${p.rpcs}</strong></span> • 
              <span>${isBat ? 'SR' : 'Econ'}: <strong style="color:#34d399;">${isBat ? p.press_sr : p.press_econ}</strong></span> • 
              <span>CSR: <strong>${p.csr}%</strong></span>
            </div>
          `;
        } else {
          tooltip.style.display = 'none';
          drawScatter();
        }
      });

      canvas.addEventListener('mouseleave', () => {
        tooltip.style.display = 'none';
        drawScatter();
      });
    }

    // Canvas Radar Chart with all 394 players
    function initRadar() {
      const p1 = document.getElementById('radarPlayer1');
      const p2 = document.getElementById('radarPlayer2');

      const optgroups = `
        <optgroup label="Top Batters (RPCS Rank)">
          ${DATA.batters.map(p => `<option value="${p.name}">${p.name} (#${p.rank} Bat | ${p.team_2026})</option>`).join('')}
        </optgroup>
        <optgroup label="Top Bowlers (RPCS Rank)">
          ${DATA.bowlers.map(p => `<option value="${p.name}">${p.name} (#${p.rank} Bowl | ${p.team_2026})</option>`).join('')}
        </optgroup>
      `;
      p1.innerHTML = optgroups;
      p2.innerHTML = optgroups;
      p1.value = "Yashasvi Jaiswal";
      p2.value = "Abhishek Sharma";
      drawRadar();
    }

    function drawRadar() {
      const canvas = document.getElementById('radarCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const width = canvas.parentElement.clientWidth;
      const height = canvas.parentElement.clientHeight;
      canvas.width = width * window.devicePixelRatio;
      canvas.height = height * window.devicePixelRatio;
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);

      ctx.clearRect(0, 0, width, height);

      const name1 = document.getElementById('radarPlayer1').value;
      const name2 = document.getElementById('radarPlayer2').value;
      const p1 = DATA.batters.find(x => x.name === name1) || DATA.bowlers.find(x => x.name === name1);
      const p2 = DATA.batters.find(x => x.name === name2) || DATA.bowlers.find(x => x.name === name2);
      if (!p1 || !p2) return;

      const axes = ['Pressure Volume', 'WPA Impact', 'Par Differential', 'Retention (κ)', 'Clutch Rate (CSR)', 'Outlier Resilience'];
      const cx = width / 2;
      const cy = height / 2;
      const radius = Math.min(width, height) * 0.35;
      const totalAxes = axes.length;

      // Draw Web Rings
      for (let level = 1; level <= 5; level++) {
        const r = (radius / 5) * level;
        ctx.beginPath();
        for (let i = 0; i < totalAxes; i++) {
          const angle = (Math.PI * 2 / totalAxes) * i - Math.PI / 2;
          const x = cx + Math.cos(angle) * r;
          const y = cy + Math.sin(angle) * r;
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.strokeStyle = '#1e293b';
        ctx.lineWidth = 1;
        ctx.stroke();
      }

      // Draw Axis Lines & Labels
      for (let i = 0; i < totalAxes; i++) {
        const angle = (Math.PI * 2 / totalAxes) * i - Math.PI / 2;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + Math.cos(angle) * radius, cy + Math.sin(angle) * radius);
        ctx.strokeStyle = '#1e293b';
        ctx.stroke();

        const lx = cx + Math.cos(angle) * (radius + 22);
        const ly = cy + Math.sin(angle) * (radius + 22);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '11px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(axes[i], lx, ly);
      }

      // Draw Player Polygons
      const getProfile = p => [
        Math.min(1, p.press_balls / 1400),
        Math.min(1, Math.max(0, p.wpa / 7)),
        Math.min(1, Math.max(0, (p.bra || p.brs || 0) / 450)),
        Math.min(1, Math.max(0, (p.kappa - 0.7) / 0.5)),
        p.csr / 100,
        1 - p.scs
      ];

      const drawPoly = (vals, color, fill) => {
        ctx.beginPath();
        for (let i = 0; i < totalAxes; i++) {
          const angle = (Math.PI * 2 / totalAxes) * i - Math.PI / 2;
          const r = radius * vals[i];
          const x = cx + Math.cos(angle) * r;
          const y = cy + Math.sin(angle) * r;
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.strokeStyle = color;
        ctx.lineWidth = 2.5;
        ctx.stroke();
        ctx.fillStyle = fill;
        ctx.fill();
      };

      drawPoly(getProfile(p1), '#f43f5e', 'rgba(244, 63, 94, 0.2)');
      drawPoly(getProfile(p2), '#10b981', 'rgba(16, 185, 129, 0.2)');

      // Legend
      ctx.textAlign = 'left';
      ctx.font = '600 12px Inter, sans-serif';
      ctx.fillStyle = '#fb7185';
      ctx.fillText(`■ ${p1.name} (RPCS ${p1.rpcs})`, 24, 24);
      ctx.fillStyle = '#34d399';
      ctx.fillText(`■ ${p2.name} (RPCS ${p2.rpcs})`, 24, 44);
    }

    // Init
    window.onload = function() {
      renderTable();
      renderAuctionBoard('all');
      renderXI();
      setupScatterHover();
    };
    window.onresize = function() {
      if (document.getElementById('tab-scatter').classList.contains('active')) drawScatter();
      if (document.getElementById('tab-radar').classList.contains('active')) drawRadar();
    };
  </script>
</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Generated enhanced dashboard successfully: {OUTPUT_HTML} ({len(html_template)} bytes)")
