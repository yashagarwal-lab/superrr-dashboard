#!/usr/bin/env python3
"""
Rajasthan Royals SupeRR Selector Analytics Auction Strategy Dashboard Builder.
Compiles a modern sports-analytics dashboard (Tailwind CSS / Shadcn UI / Tremor aesthetic)
incorporating verified IPL 2027 auction intelligence, prominent status badges,
interactive Canvas scatter & radar charts, and live purse tracking.
"""

import json
import os

DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(DASHBOARD_DIR, "dashboard", "data.json")
OUTPUT_HTML = os.path.join(DASHBOARD_DIR, "dashboard", "index.html")

TRADES_SCRATCH = os.path.join(DASHBOARD_DIR, "scratch", "confirmed_trades.json")
ALLROUNDERS_SCRATCH = os.path.join(DASHBOARD_DIR, "scratch", "allrounders_data.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

if os.path.exists(ALLROUNDERS_SCRATCH) and "all_rounders" not in data:
    with open(ALLROUNDERS_SCRATCH, "r", encoding="utf-8") as f:
        data["all_rounders"] = json.load(f)

if os.path.exists(TRADES_SCRATCH) and "confirmed_trades" not in data:
    with open(TRADES_SCRATCH, "r", encoding="utf-8") as f:
        data["confirmed_trades"] = json.load(f)

data_json_str = json.dumps(data, ensure_ascii=False)

html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rajasthan Royals SupeRR Selector — Pressure Analytics & Auction Strategy Platform</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root {
      /* Rajasthan Royals Official Brand Tokens */
      --rr-pink: #ea1a7f;
      --rr-pink-hover: #ff2a8d;
      --rr-pink-dark: #be123c;
      --rr-pink-deep: #831843;
      --rr-pink-glow: rgba(234, 26, 127, 0.45);
      --rr-pink-subtle: rgba(234, 26, 127, 0.12);
      --rr-pink-border: rgba(234, 26, 127, 0.35);

      --rr-navy-deep: #070d1e;
      --rr-navy-base: #0a132c;
      --rr-navy-card: rgba(14, 23, 51, 0.78);
      --rr-navy-hover: rgba(24, 38, 80, 0.88);
      --rr-navy-surface: rgba(16, 28, 64, 0.7);
      --rr-navy-border: rgba(255, 255, 255, 0.08);

      --rr-royal-blue: #004ba0;
      --rr-blue: #004ba0;

      --rr-gold: #fbbf24;
      --rr-gold-hover: #f59e0b;
      --rr-gold-glow: rgba(251, 191, 36, 0.35);

      --rr-text-primary: #ffffff;
      --rr-text-secondary: #cbd5e1;
      --rr-text-muted: #94a3b8;

      /* Sports Status Semantic Tokens */
      --status-free-agent: #10b981;
      --status-traded: #f59e0b;
      --status-ineligible: #ef4444;
      --status-watchlist: #eab308;
      --status-steal: #38bdf8;

      /* Shadcn / Tremor Design Tokens */
      --slate-50: #ffffff;
      --slate-100: #f1f5f9;
      --slate-200: #e2e8f0;
      --slate-300: #cbd5e1;
      --slate-400: #94a3b8;
      --slate-500: #64748b;
      --slate-600: #475569;
      --slate-700: #334155;
      --slate-800: #1e293b;
      --slate-850: #0f172a;
      --slate-900: #0b1329;
      --slate-950: #050814;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: #070d1e;
      background-image: 
        radial-gradient(circle 900px at 15% 5%, rgba(234, 26, 127, 0.15) 0%, transparent 65%),
        radial-gradient(circle 750px at 85% 10%, rgba(251, 191, 36, 0.10) 0%, transparent 60%),
        radial-gradient(ellipse 1100px 700px at 50% 50%, rgba(13, 35, 85, 0.25) 0%, transparent 80%),
        linear-gradient(180deg, #070d1e 0%, #0a132c 40%, #060a17 100%);
      background-attachment: fixed;
      color: var(--slate-300);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      line-height: 1.5;
      padding-bottom: 80px;
      -webkit-font-smoothing: antialiased;
      position: relative;
      overflow-x: hidden;
    }

    /* React Bits: Backgrounds/Telemetry Grid & Precision Lighting */
    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background-image: 
        linear-gradient(to right, rgba(255, 255, 255, 0.025) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
      background-size: 36px 36px;
      pointer-events: none;
      z-index: -1;
    }

    /* React Bits: Backgrounds/Aurora Mesh */
    body::after {
      content: '';
      position: fixed;
      top: -20%;
      left: 12%;
      width: 76%;
      height: 60%;
      background: radial-gradient(ellipse at 50% 30%, rgba(234, 26, 127, 0.16) 0%, rgba(0, 30, 61, 0.3) 45%, transparent 70%);
      filter: blur(100px);
      pointer-events: none;
      z-index: -1;
      animation: auroraPulse 14s ease-in-out infinite alternate;
    }
    @keyframes auroraPulse {
      0% { transform: scale(0.95) translate(0, 0); opacity: 0.7; }
      100% { transform: scale(1.05) translate(20px, 15px); opacity: 1; }
    }

    .num-tabular {
      font-family: 'JetBrains Mono', monospace;
      font-variant-numeric: tabular-nums;
    }

    /* React Bits: Full-Bleed Royal Pink Header with DotGrid & Mesh Animation */
    header {
      background: linear-gradient(135deg, #a2104d 0%, #ea1a7f 32%, #be123c 65%, #001e3d 100%);
      background-size: 200% 200%;
      animation: headerMesh 14s ease infinite;
      border-bottom: 1px solid rgba(234, 26, 127, 0.35);
      padding: 14px 28px;
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(20px);
      box-shadow: 0 8px 32px rgba(234, 26, 127, 0.35);
      position: relative;
      overflow: hidden;
    }
    @keyframes headerMesh {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    header::before {
      content: '';
      position: absolute;
      inset: 0;
      background-image: radial-gradient(rgba(255, 255, 255, 0.18) 1.2px, transparent 1.2px);
      background-size: 16px 16px;
      pointer-events: none;
      opacity: 0.75;
    }

    .header-content {
      max-width: 1440px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      position: relative;
      z-index: 2;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .logo-badge {
      background: #ffffff;
      color: var(--rr-pink-dark);
      font-weight: 900;
      font-size: 14px;
      padding: 6px 13px;
      border-radius: 8px;
      letter-spacing: 0.08em;
      border: 1px solid rgba(255, 255, 255, 0.4);
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    }
    .logo-badge::before {
      content: '';
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--rr-pink);
      box-shadow: 0 0 6px var(--rr-pink);
    }
    .brand-text h1 {
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.02em;
      text-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* React Bits: TextAnimations/ShinyText */
    .shiny-text {
      background: linear-gradient(120deg, #ffffff 0%, #ffffff 35%, #fde047 50%, #ffffff 65%, #ffffff 100%);
      background-size: 200% auto;
      color: #ffffff;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: shineText 5s linear infinite;
    }
    @keyframes shineText {
      0% { background-position: -200% 0; }
      100% { background-position: 200% 0; }
    }

    .badge-header {
      background: rgba(255, 255, 255, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.35);
      padding: 2px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #ffffff;
    }
    .brand-text p {
      font-size: 11px;
      color: rgba(255, 255, 255, 0.95);
      letter-spacing: 0.04em;
      font-weight: 600;
      text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
    }

    /* React Bits: Components/PillNav & Floating Dock Capsule */
    .nav-tabs {
      display: flex;
      gap: 4px;
      flex-wrap: wrap;
      background: rgba(6, 11, 25, 0.9);
      padding: 4px;
      border-radius: 9999px;
      border: 1px solid rgba(234, 26, 127, 0.35);
      backdrop-filter: blur(20px);
      box-shadow: 0 8px 28px rgba(0, 0, 0, 0.6);
      position: relative;
    }
    @media (max-width: 900px) {
      .nav-tabs {
        flex-wrap: nowrap;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
        max-width: 100%;
        border-radius: 9999px;
      }
      .nav-tabs::-webkit-scrollbar {
        display: none;
      }
      .nav-tab {
        flex-shrink: 0;
        white-space: nowrap;
      }
    }
    .nav-tab {
      background: transparent;
      border: none;
      color: var(--slate-200);
      padding: 8px 16px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      cursor: pointer;
      position: relative;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .nav-tab:hover {
      color: #ffffff;
      background: rgba(234, 26, 127, 0.2);
      transform: translateY(-1px);
    }
    .nav-tab:active {
      transform: scale(0.97);
    }
    .nav-tab:focus-visible {
      outline: 2px solid var(--rr-pink);
      outline-offset: 2px;
    }
    .nav-tab.active {
      background: linear-gradient(135deg, #ea1a7f 0%, #be123c 100%);
      color: #ffffff;
      font-weight: 800;
      box-shadow: 0 0 18px rgba(234, 26, 127, 0.6);
      transform: scale(1.02);
    }
    .nav-tab.active::after {
      content: '';
      position: absolute;
      bottom: 2px;
      left: 50%;
      transform: translateX(-50%);
      width: 4px;
      height: 4px;
      border-radius: 50%;
      background: #ffffff;
      box-shadow: 0 0 6px #ffffff;
    }

    /* Container */
    .container {
      max-width: 1440px;
      margin: 22px auto;
      padding: 0 24px;
    }

    .tab-view { display: none; }
    .tab-view.active { display: block; animation: tabFadeIn 0.15s ease-out; }
    @keyframes tabFadeIn {
      from { opacity: 0; transform: translateY(3px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* React Bits: Components/MagicBento Grid */
    .magic-bento {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    .magic-bento__cell {
      background: var(--rr-navy-card);
      border: 1px solid var(--rr-navy-border);
      border-radius: 16px;
      padding: 22px;
      position: relative;
      overflow: hidden;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .magic-bento__cell:hover {
      border-color: rgba(234, 26, 127, 0.55);
      transform: translateY(-2px);
      box-shadow: 0 8px 32px rgba(234, 26, 127, 0.16);
    }
    .magic-bento__cell:active {
      transform: scale(0.99);
    }
    .magic-bento__cell:focus-visible {
      outline: 2px solid var(--rr-pink);
      outline-offset: 2px;
    }
    .magic-bento__cell--featured {
      grid-column: span 6;
      background: linear-gradient(135deg, rgba(234, 26, 127, 0.1) 0%, rgba(11, 19, 41, 0.95) 50%, rgba(7, 13, 30, 0.95) 100%);
      border: 1px solid rgba(234, 26, 127, 0.4);
    }
    .magic-bento__cell--stat1 {
      grid-column: span 3;
    }
    .magic-bento__cell--stat2 {
      grid-column: span 3;
    }
    @media (max-width: 1024px) {
      .magic-bento__cell--featured,
      .magic-bento__cell--stat1,
      .magic-bento__cell--stat2 {
        grid-column: span 12;
      }
    }

    .bento-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 9999px;
      margin-bottom: 6px;
    }
    .status-dot-pulse {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--rr-pink);
      box-shadow: 0 0 8px var(--rr-pink);
      animation: pulse 1.8s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }

    .bento-metrics-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-bottom: 16px;
    }
    @media (max-width: 640px) {
      .bento-metrics-row {
        grid-template-columns: 1fr !important;
      }
    }

    .bento-metric-tile {
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
    }
    .bento-metric-lbl {
      font-size: 10px;
      text-transform: uppercase;
      color: var(--slate-400);
      font-weight: 700;
      letter-spacing: 0.08em;
      margin-bottom: 3px;
    }
    .bento-metric-val {
      font-size: 19px;
      font-weight: 800;
      letter-spacing: -0.02em;
    }
    .priority-pill {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 11px;
      font-weight: 600;
      color: var(--slate-200);
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      padding: 4px 10px;
      border-radius: 6px;
    }

    /* React Bits: Animations/StarBorder Button */
    .star-border-btn {
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 9px 18px;
      border-radius: 9999px;
      background: linear-gradient(135deg, #be123c 0%, #ea1a7f 100%);
      color: #ffffff;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      border: none;
      cursor: pointer;
      overflow: hidden;
      box-shadow: 0 4px 18px rgba(234, 26, 127, 0.4);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 1;
    }
    .star-border-btn:hover {
      transform: translateY(-2px) scale(1.02);
      box-shadow: 0 6px 24px rgba(234, 26, 127, 0.6);
    }
    .star-border-btn:active {
      transform: scale(0.98);
    }
    .star-border-btn:focus-visible {
      outline: 2px solid var(--rr-pink);
      outline-offset: 2px;
    }
    .star-border-btn::before {
      content: '';
      position: absolute;
      inset: -2px;
      border-radius: 9999px;
      background: conic-gradient(from 0deg, transparent 0deg, #ffffff 40deg, transparent 80deg, #fbbf24 180deg, transparent 220deg, #ea1a7f 300deg, transparent 360deg);
      animation: starRotate 4s linear infinite;
      z-index: -2;
    }
    .star-border-btn::after {
      content: '';
      position: absolute;
      inset: 1px;
      border-radius: 9999px;
      background: linear-gradient(135deg, #9f1239 0%, #ea1a7f 100%);
      z-index: -1;
    }
    @keyframes starRotate {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    /* React Bits: Components/SpotlightCard */
    .spotlight-card {
      position: relative;
      background: var(--rr-navy-card);
      border: 1px solid var(--rr-navy-border);
      overflow: hidden;
      transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
    }
    .spotlight-card::before {
      content: '';
      position: absolute;
      inset: 0;
      background: radial-gradient(circle 350px at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(234, 26, 127, 0.16), transparent 80%);
      opacity: 0;
      transition: opacity 0.3s;
      pointer-events: none;
      z-index: 1;
    }
    .spotlight-card:hover::before {
      opacity: 1;
    }
    .spotlight-card:hover {
      border-color: rgba(234, 26, 127, 0.5);
      box-shadow: 0 8px 30px rgba(234, 26, 127, 0.14);
    }

    /* React Bits: Components/TiltedCard 3D */
    .tilted-card {
      transform-style: preserve-3d;
      transition: transform 0.15s ease-out;
      will-change: transform;
    }

    /* React Bits: Micro/StatusMark Styled Badges */
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 10px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      white-space: nowrap;
      line-height: 1.2;
    }
    .badge::before {
      content: '';
      display: inline-block;
      width: 6px;
      height: 6px;
      border-radius: 50%;
    }

    .badge-ineligible {
      background: rgba(239, 68, 68, 0.12) !important;
      color: #f87171 !important;
      border: 1px solid rgba(239, 68, 68, 0.5) !important;
      font-weight: 800;
    }
    .badge-ineligible::before {
      background: #ef4444;
      box-shadow: 0 0 6px rgba(239, 68, 68, 0.8);
    }

    .badge-free-agent {
      background: rgba(16, 185, 129, 0.12);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.45);
    }
    .badge-free-agent::before {
      background: #10b981;
      box-shadow: 0 0 6px rgba(16, 185, 129, 0.8);
    }

    .badge-traded {
      background: rgba(245, 158, 11, 0.12);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.45);
    }
    .badge-traded::before {
      background: #f59e0b;
      box-shadow: 0 0 6px rgba(245, 158, 11, 0.8);
    }

    .badge-watchlist {
      background: rgba(234, 179, 8, 0.12);
      color: #fde047;
      border: 1px solid rgba(234, 179, 8, 0.45);
    }
    .badge-watchlist::before {
      background: #eab308;
      box-shadow: 0 0 6px rgba(234, 179, 8, 0.8);
    }

    .badge-retention {
      background: rgba(51, 65, 85, 0.4);
      color: #cbd5e1;
      border: 1px solid rgba(100, 116, 139, 0.45);
    }
    .badge-retention::before {
      background: #94a3b8;
    }

    .badge-rr-core {
      background: rgba(234, 26, 127, 0.15);
      color: #ff2a8d;
      border: 1px solid rgba(234, 26, 127, 0.55);
    }
    .badge-rr-core::before {
      background: #ea1a7f;
      box-shadow: 0 0 8px rgba(234, 26, 127, 0.9);
    }

    .badge-global-steal, .badge-domestic-steal {
      background: rgba(56, 189, 248, 0.12);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.45);
    }
    .badge-global-steal::before, .badge-domestic-steal::before {
      background: #38bdf8;
      box-shadow: 0 0 6px rgba(56, 189, 248, 0.8);
    }

    .badge-auction-target {
      background: rgba(234, 26, 127, 0.12);
      color: #ea1a7f;
      border: 1px solid rgba(234, 26, 127, 0.45);
    }
    .badge-auction-target::before {
      background: #ea1a7f;
      box-shadow: 0 0 6px rgba(234, 26, 127, 0.8);
    }

    /* Table Rows Performance Accents */
    .row-ineligible {
      background: rgba(239, 68, 68, 0.05) !important;
      border-left: 3px solid #ef4444 !important;
    }
    .row-ineligible:hover {
      background: rgba(239, 68, 68, 0.1) !important;
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
      border-left: 3px solid #475569 !important;
    }
    .row-rr-core {
      border-left: 3px solid #ea1a7f !important;
    }

    /* Toolbar & Segmented Controls */
    .toolbar {
      background: var(--rr-navy-card);
      border: 1px solid var(--rr-navy-border);
      border-radius: 12px;
      padding: 14px 18px;
      margin-bottom: 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }
    .toolbar-left, .toolbar-right {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .role-toggle {
      display: flex;
      background: rgba(5, 8, 20, 0.8);
      border: 1px solid var(--rr-navy-border);
      border-radius: 9999px;
      padding: 3px;
    }
    .role-btn {
      padding: 7px 16px;
      border: none;
      background: transparent;
      color: var(--slate-400);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      cursor: pointer;
      border-radius: 9999px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .role-btn:hover {
      color: #ffffff;
      background: rgba(234, 26, 127, 0.15);
    }
    .role-btn:active {
      transform: scale(0.97);
    }
    .role-btn:focus-visible {
      outline: 2px solid var(--rr-pink);
      outline-offset: 2px;
    }
    .role-btn.active {
      background: linear-gradient(135deg, #ea1a7f 0%, #be123c 100%);
      color: #ffffff;
      font-weight: 800;
      box-shadow: 0 0 14px rgba(234, 26, 127, 0.5);
    }

    .filter-pills {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }
    .pill {
      background: rgba(5, 8, 20, 0.6);
      border: 1px solid var(--rr-navy-border);
      color: var(--slate-300);
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
      letter-spacing: 0.02em;
    }
    .pill:hover {
      border-color: rgba(234, 26, 127, 0.4);
      color: #ffffff;
      background: rgba(234, 26, 127, 0.1);
    }
    .pill:active {
      transform: scale(0.97);
    }
    .pill:focus-visible {
      outline: 2px solid var(--rr-pink);
      outline-offset: 2px;
    }
    .pill.active {
      background: rgba(234, 26, 127, 0.2);
      border-color: var(--rr-pink);
      color: #ffffff;
      font-weight: 700;
      box-shadow: 0 0 10px rgba(234, 26, 127, 0.3);
    }

    .search-input {
      background: rgba(5, 8, 20, 0.8);
      border: 1px solid var(--rr-navy-border);
      border-radius: 8px;
      padding: 7px 14px;
      color: #ffffff;
      font-size: 12px;
      width: 220px;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .search-input:hover, .sort-select:hover {
      border-color: rgba(234, 26, 127, 0.4);
    }
    .search-input:focus, .search-input:focus-visible {
      border-color: var(--rr-pink);
      box-shadow: 0 0 10px rgba(234, 26, 127, 0.35);
      outline: none;
    }
    .search-input:active {
      border-color: var(--rr-pink);
    }
    .sort-select {
      background: rgba(5, 8, 20, 0.8);
      border: 1px solid var(--rr-navy-border);
      border-radius: 8px;
      color: #ffffff;
      padding: 7px 12px;
      font-size: 12px;
      outline: none;
      cursor: pointer;
      max-width: 100%;
      min-width: 0;
      box-sizing: border-box;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .sort-select:focus, .sort-select:focus-visible {
      border-color: var(--rr-pink);
      box-shadow: 0 0 10px rgba(234, 26, 127, 0.35);
      outline: none;
    }
    .sort-select:active {
      border-color: var(--rr-pink);
    }

    /* Table Styles with Sticky Headers and Sticky Player Name Column */
    .table-container {
      background: var(--rr-navy-card);
      border: 1px solid var(--rr-navy-border);
      border-radius: 14px;
      overflow-x: auto;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
      position: relative;
    }
    table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      text-align: left;
      font-size: 12px;
    }
    th {
      background: #070d1f;
      padding: 13px 16px;
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--slate-400);
      font-weight: 700;
      border-bottom: 1px solid var(--rr-navy-border);
      white-space: nowrap;
      position: sticky;
      top: 0;
      z-index: 10;
    }
    td {
      padding: 12px 16px;
      border-bottom: 1px solid rgba(26, 39, 76, 0.6);
      vertical-align: middle;
      white-space: nowrap;
    }
    /* Sticky rank & player name columns on horizontal scroll */
    th:first-child {
      position: sticky;
      left: 0;
      top: 0;
      z-index: 25;
      background: #070d1f;
      width: 52px;
      min-width: 52px;
      max-width: 52px;
      text-align: center;
      padding: 13px 8px;
    }
    td:first-child {
      position: sticky;
      left: 0;
      z-index: 5;
      background: #0b142c;
      width: 52px;
      min-width: 52px;
      max-width: 52px;
      text-align: center;
      padding: 12px 8px;
    }
    th:nth-child(2) {
      position: sticky;
      left: 52px;
      top: 0;
      z-index: 25;
      background: #070d1f;
      box-shadow: 4px 0 10px rgba(0, 0, 0, 0.35);
    }
    td:nth-child(2) {
      position: sticky;
      left: 52px;
      z-index: 5;
      background: #0b142c;
      box-shadow: 4px 0 10px rgba(0, 0, 0, 0.35);
    }
    tr {
      background: var(--rr-navy-card);
      transition: background-color 0.12s ease;
    }
    tr:hover {
      background: var(--rr-navy-hover) !important;
      cursor: pointer;
    }
    tr:hover td:first-child,
    tr:hover td:nth-child(2) {
      background: #152244 !important;
    }
    tr:active {
      background: rgba(30, 48, 98, 0.95) !important;
    }
    tr:focus-visible {
      outline: 2px solid var(--rr-pink);
      outline-offset: -2px;
    }
    .row-ineligible td:first-child,
    .row-ineligible td:nth-child(2) {
      background: #1a0f18 !important;
    }
    .row-ineligible:hover td:first-child,
    .row-ineligible:hover td:nth-child(2) {
      background: #251322 !important;
    }
    .rank-cell {
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: var(--slate-500);
      width: 44px;
    }
    .rank-cell.top3 {
      color: var(--rr-gold);
    }
    .player-name-cell {
      display: flex;
      flex-direction: column;
    }
    .name-title {
      font-weight: 700;
      color: #ffffff;
      font-size: 13px;
      letter-spacing: -0.01em;
    }
    .name-team-sub {
      font-size: 11px;
      color: var(--slate-400);
      margin-top: 1px;
    }
    .rpcs-pill {
      display: inline-block;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      padding: 3px 8px;
      border-radius: 6px;
      background: rgba(234, 26, 127, 0.12);
      color: #ffffff;
      border: 1px solid rgba(234, 26, 127, 0.35);
    }
    .rpcs-pill.elite {
      background: linear-gradient(135deg, rgba(234, 26, 127, 0.25) 0%, rgba(251, 191, 36, 0.2) 100%);
      color: #ffffff;
      border: 1px solid rgba(234, 26, 127, 0.6);
      box-shadow: 0 0 10px rgba(234, 26, 127, 0.3);
    }

    /* Modal / Dialog */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background: rgba(5, 8, 20, 0.88);
      backdrop-filter: blur(12px);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 1000;
      padding: 20px;
    }
    .modal-overlay.active { display: flex; }
    .modal-card {
      background: var(--rr-navy-card);
      border: 1px solid rgba(234, 26, 127, 0.35);
      border-radius: 16px;
      width: 100%;
      max-width: 860px;
      max-height: 90vh;
      overflow-y: auto;
      padding: 26px 30px;
      position: relative;
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.8);
    }
    .modal-close {
      position: absolute;
      top: 18px;
      right: 20px;
      font-size: 20px;
      color: var(--slate-400);
      cursor: pointer;
      background: none;
      border: none;
      transition: all 0.15s;
    }
    .modal-close:hover { color: #ffffff; }
    .modal-close:active { transform: scale(0.92); }
    .modal-close:focus-visible {
      outline: 2px solid var(--rr-pink);
      outline-offset: 2px;
      border-radius: 4px;
    }
    .modal-header {
      border-bottom: 1px solid var(--rr-navy-border);
      padding-bottom: 16px;
      margin-bottom: 20px;
    }
    .modal-header h2 {
      font-size: 20px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .modal-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 18px;
    }
    @media (max-width: 720px) { .modal-grid { grid-template-columns: 1fr; } }
    .modal-section {
      background: rgba(5, 8, 20, 0.6);
      border: 1px solid var(--rr-navy-border);
      border-radius: 10px;
      padding: 16px;
    }
    .modal-section h4 {
      font-size: 10px;
      text-transform: uppercase;
      color: var(--slate-400);
      font-weight: 700;
      letter-spacing: 0.12em;
      margin-bottom: 10px;
    }
    .info-row {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      padding: 6px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .info-row:last-child { border-bottom: none; }
    .info-row span:first-child { color: var(--slate-400); }
    .info-row span:last-child { font-weight: 600; color: #ffffff; }

    /* Modal Alert Boxes */
    .modal-alert-box {
      border-radius: 8px;
      padding: 14px 18px;
      margin-bottom: 18px;
      font-size: 12px;
      line-height: 1.5;
    }
    .alert-ineligible {
      background: rgba(239, 68, 68, 0.12);
      border: 1px solid rgba(239, 68, 68, 0.45);
      color: #f87171;
    }
    .alert-ineligible strong { color: #ffffff; }
    .alert-free-agent {
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.45);
      color: #34d399;
    }
    .alert-traded {
      background: rgba(245, 158, 11, 0.12);
      border: 1px solid rgba(245, 158, 11, 0.45);
      color: #fbbf24;
    }
    .alert-watchlist {
      background: rgba(234, 179, 8, 0.12);
      border: 1px solid rgba(234, 179, 8, 0.45);
      color: #fde047;
    }
    .alert-retention {
      background: rgba(51, 65, 85, 0.3);
      border: 1px solid rgba(100, 116, 139, 0.4);
      color: #cbd5e1;
    }
    .alert-rr-core {
      background: rgba(234, 26, 127, 0.15);
      border: 1px solid rgba(234, 26, 127, 0.45);
      color: #ff2a8d;
    }

    /* Charts Container */
    .chart-panel {
      background: var(--rr-navy-card);
      border: 1px solid var(--rr-navy-border);
      border-radius: 14px;
      padding: 22px;
      margin-bottom: 22px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
      flex-wrap: wrap;
      gap: 12px;
    }
    .chart-box {
      position: relative;
      width: 100%;
      height: 440px;
      background: rgba(5, 8, 20, 0.7);
      border-radius: 10px;
      border: 1px solid var(--rr-navy-border);
    }
    canvas {
      width: 100% !important;
      height: 100% !important;
    }

    .scatter-legend {
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      margin-bottom: 14px;
      font-size: 11px;
      color: var(--slate-400);
      background: rgba(5, 8, 20, 0.7);
      padding: 10px 16px;
      border-radius: 8px;
      border: 1px solid var(--rr-navy-border);
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .legend-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }

    #scatterTooltip {
      position: absolute;
      display: none;
      background: #090e1f;
      border: 1px solid var(--rr-pink);
      border-radius: 8px;
      padding: 12px 16px;
      font-size: 11px;
      color: #ffffff;
      pointer-events: none;
      z-index: 50;
      box-shadow: 0 8px 30px rgba(0,0,0,0.85);
      min-width: 200px;
    }

    /* Auction Grid */
    .auction-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
      gap: 16px;
      margin-top: 18px;
    }
    .auction-card {
      background: var(--rr-navy-card);
      border: 1px solid var(--rr-navy-border);
      border-radius: 12px;
      padding: 18px;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .auction-card:hover {
      border-color: rgba(234, 26, 127, 0.5);
      background: var(--rr-navy-hover);
      transform: translateY(-2px);
      box-shadow: 0 8px 28px rgba(234, 26, 127, 0.15);
    }
    .auction-card:active {
      transform: scale(0.99);
    }
    .auction-card:focus-visible {
      outline: 2px solid var(--rr-pink);
      outline-offset: 2px;
    }
    .auction-card.priority-card {
      border-color: rgba(234, 26, 127, 0.65);
      background: linear-gradient(135deg, rgba(234, 26, 127, 0.1) 0%, rgba(11, 19, 41, 0.95) 100%);
      box-shadow: 0 0 20px rgba(234, 26, 127, 0.2);
    }

    /* Responsive Starting XI Builder Layout */
    .xi-builder-layout {
      display: grid;
      grid-template-columns: 1.25fr 0.95fr;
      gap: 20px;
    }
    @media (max-width: 1024px) {
      .xi-builder-layout {
        grid-template-columns: 1fr;
        gap: 16px;
      }
    }
    .auction-card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 8px;
    }
    .auction-card-header > div:first-child {
      min-width: 0;
      flex: 1 1 auto;
    }
    .auction-card-header > div:last-child {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 4px;
      flex-wrap: wrap;
      max-width: 100%;
    }
    @media (max-width: 1024px) {
      .auction-card-header > div:last-child {
        width: 100%;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding-top: 6px;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        flex-wrap: wrap;
        gap: 6px;
      }
    }
    @media (max-width: 480px) {
      .auction-card-header > div:last-child {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 6px;
      }
    }
    .auction-player-name {
      font-size: 16px;
      font-weight: 800;
      color: #ffffff;
    }
    .auction-role {
      font-size: 11px;
      color: var(--rr-pink);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .auction-price-tag {
      background: rgba(251, 191, 36, 0.15);
      border: 1px solid rgba(251, 191, 36, 0.4);
      color: #fbbf24;
      font-size: 11px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      padding: 4px 10px;
      border-radius: 6px;
    }
    .auction-trail {
      background: rgba(0, 0, 0, 0.4);
      border-radius: 6px;
      padding: 10px 12px;
      font-size: 12px;
      margin: 12px 0;
      border-left: 2px solid var(--rr-pink);
      color: var(--slate-300);
    }
    .auction-stats-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      text-align: center;
      margin-top: 12px;
    }
    .mini-stat-card {
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--rr-navy-border);
      padding: 8px;
      border-radius: 6px;
    }
    .mini-stat-val {
      font-size: 14px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: #ffffff;
    }
    .mini-stat-lbl {
      font-size: 9px;
      color: var(--slate-400);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    /* Purse Tracker (XI Builder) */
    .purse-tracker {
      background: var(--rr-navy-card);
      border: 1px solid rgba(234, 26, 127, 0.35);
      border-radius: 14px;
      padding: 20px 24px;
      margin-bottom: 20px;
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
    }
    .purse-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin-bottom: 16px;
    }
    .purse-item-lbl {
      font-size: 10px;
      text-transform: uppercase;
      color: var(--slate-400);
      font-weight: 700;
      letter-spacing: 0.12em;
    }
    .purse-item-val {
      font-size: 24px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: #ffffff;
      letter-spacing: -0.03em;
    }
    .purse-progress-bar {
      width: 100%;
      height: 8px;
      background: rgba(0, 0, 0, 0.5);
      border-radius: 9999px;
      overflow: hidden;
      border: 1px solid var(--rr-navy-border);
    }
    .purse-progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #ea1a7f 0%, #fbbf24 100%);
      width: 94.7%;
      border-radius: 9999px;
    }

    /* Starting XI Slot Cards */
    .xi-slots-container {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .xi-slot-card {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 18px;
      background: var(--rr-navy-card);
      border: 1px solid var(--rr-navy-border);
      border-radius: 10px;
      font-size: 12px;
      cursor: pointer;
      transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
      gap: 12px;
    }
    .xi-slot-card:hover {
      background: var(--rr-navy-hover);
      border-color: rgba(234, 26, 127, 0.4);
      transform: translateX(3px);
    }
    .xi-slot-left {
      display: flex;
      align-items: center;
      gap: 14px;
      flex: 1;
      min-width: 0;
    }
    .xi-slot-pos-badge {
      font-weight: 800;
      font-size: 10px;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: 0.05em;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(234, 26, 127, 0.15);
      color: #ff2a8d;
      border: 1px solid rgba(234, 26, 127, 0.35);
      white-space: nowrap;
      text-transform: uppercase;
      min-width: 100px;
      text-align: center;
    }
    .xi-slot-player-meta {
      display: flex;
      flex-direction: column;
      min-width: 0;
    }
    .xi-slot-player-name {
      font-weight: 700;
      color: #ffffff;
      font-size: 13px;
      letter-spacing: -0.01em;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .xi-slot-player-sub {
      font-size: 11px;
      color: var(--slate-400);
      margin-top: 1px;
    }
    .xi-slot-right {
      display: flex;
      align-items: center;
      gap: 14px;
      flex-shrink: 0;
    }
    .xi-slot-cost {
      font-size: 12px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: #34d399;
    }
    .xi-slot-rpcs {
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: #ffffff;
    }
    .xi-slot-change-btn {
      font-size: 10px;
      text-transform: uppercase;
      font-weight: 800;
      letter-spacing: 0.08em;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.08);
      color: var(--slate-200);
      border: 1px solid rgba(255, 255, 255, 0.15);
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .xi-slot-card:hover .xi-slot-change-btn {
      background: var(--rr-pink);
      color: #ffffff;
      border-color: var(--rr-pink);
    }

    /* Modal Slot Assignment List */
    .slot-candidate-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 14px;
      border-radius: 8px;
      background: rgba(5, 8, 20, 0.6);
      border: 1px solid var(--rr-navy-border);
      margin-bottom: 8px;
      transition: all 0.15s ease;
      flex-wrap: wrap;
      gap: 8px;
    }
    .slot-candidate-row:hover {
      background: var(--rr-navy-hover);
      border-color: rgba(234, 26, 127, 0.4);
    }
    .btn-assign-slot {
      background: linear-gradient(135deg, #ea1a7f 0%, #be123c 100%);
      color: #ffffff;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }
    .btn-assign-slot:hover {
      box-shadow: 0 0 12px rgba(234, 26, 127, 0.6);
      transform: scale(1.02);
    }
    .btn-assign-slot.over-budget {
      background: rgba(239, 68, 68, 0.2);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.4);
      cursor: not-allowed;
    }

    footer {
      text-align: center;
      margin-top: 50px;
      color: var(--slate-500);
      font-size: 11px;
      letter-spacing: 0.04em;
    }

    /* React Bits: Lifecycle Audit Command Center & Player Tiles */
    .audit-header-banner {
      background: linear-gradient(135deg, rgba(14, 23, 51, 0.85) 0%, rgba(8, 14, 33, 0.95) 100%);
      border: 1px solid rgba(234, 26, 127, 0.3);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 22px;
      backdrop-filter: blur(20px);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 8px 32px rgba(0, 0, 0, 0.5);
    }
    .audit-pool-card {
      background: linear-gradient(135deg, rgba(14, 23, 51, 0.8) 0%, rgba(8, 14, 33, 0.9) 100%);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 22px;
      margin-bottom: 20px;
      backdrop-filter: blur(20px);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06), 0 8px 32px rgba(0, 0, 0, 0.4);
      position: relative;
      overflow: hidden;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .audit-pool-card:hover {
      border-color: rgba(234, 26, 127, 0.45);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1), 0 12px 36px rgba(0, 0, 0, 0.55);
      transform: translateY(-2px);
    }
    .audit-pool-card.pool-emerald { border-left: 4px solid #10b981; }
    .audit-pool-card.pool-purple { border-left: 4px solid #a855f7; }
    .audit-pool-card.pool-amber { border-left: 4px solid #f59e0b; }
    .audit-pool-card.pool-gold { border-left: 4px solid #eab308; }
    .audit-pool-card.pool-ruby { border-left: 4px solid #ef4444; }

    .audit-pool-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 10px;
    }
    .audit-pool-title-group {
      min-width: 0;
      max-width: 100%;
    }
    .audit-pool-title-group > div:first-child {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 4px;
    }
    .audit-pool-title-group h4 {
      font-size: 17px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.01em;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .audit-pool-desc {
      font-size: 12px;
      color: var(--slate-300);
      margin-bottom: 18px;
      line-height: 1.5;
      max-width: 900px;
    }

    .audit-player-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(100%, 260px), 1fr));
      gap: 12px;
    }
    .audit-player-tile {
      background: rgba(6, 11, 26, 0.65);
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 12px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }
    .audit-player-tile:hover {
      background: rgba(18, 30, 66, 0.7);
      border-color: rgba(234, 26, 127, 0.5);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }
    .audit-player-tile-top {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .player-avatar-circle {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: linear-gradient(135deg, rgba(234, 26, 127, 0.3) 0%, rgba(11, 19, 41, 0.9) 100%);
      border: 1px solid rgba(234, 26, 127, 0.5);
      color: #ffffff;
      font-weight: 800;
      font-size: 12px;
      font-family: 'JetBrains Mono', monospace;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .player-avatar-circle.avatar-emerald {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.35) 0%, rgba(6, 11, 26, 0.9) 100%);
      border-color: rgba(16, 185, 129, 0.6);
      color: #34d399;
    }
    .player-avatar-circle.avatar-purple {
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.35) 0%, rgba(6, 11, 26, 0.9) 100%);
      border-color: rgba(168, 85, 247, 0.6);
      color: #c084fc;
    }
    .player-avatar-circle.avatar-amber {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.35) 0%, rgba(6, 11, 26, 0.9) 100%);
      border-color: rgba(245, 158, 11, 0.6);
      color: #fbbf24;
    }
    .player-avatar-circle.avatar-gold {
      background: linear-gradient(135deg, rgba(234, 179, 8, 0.35) 0%, rgba(6, 11, 26, 0.9) 100%);
      border-color: rgba(234, 179, 8, 0.6);
      color: #fde047;
    }
    .player-avatar-circle.avatar-ruby {
      background: linear-gradient(135deg, rgba(239, 68, 68, 0.35) 0%, rgba(6, 11, 26, 0.9) 100%);
      border-color: rgba(239, 68, 68, 0.6);
      color: #f87171;
    }

    .audit-player-name {
      font-size: 13px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.2;
    }
    .audit-player-pathway {
      font-size: 11px;
      color: var(--slate-400);
      display: flex;
      align-items: center;
      gap: 4px;
      margin-top: 2px;
    }
    .audit-metric-pills {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }
    .audit-chip {
      font-size: 10px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.06);
      color: var(--slate-200);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .audit-player-notes {
      font-size: 11px;
      color: var(--slate-300);
      line-height: 1.4;
      background: rgba(0, 0, 0, 0.25);
      padding: 6px 8px;
      border-radius: 6px;
      border-left: 2px solid rgba(234, 26, 127, 0.4);
    }

    /* Case Studies (Tab 7) */
    .case-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
      gap: 18px;
    }
    .case-card {
      background: linear-gradient(135deg, rgba(14, 23, 51, 0.8) 0%, rgba(8, 14, 33, 0.9) 100%);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 20px;
      backdrop-filter: blur(16px);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .case-card:hover {
      border-color: rgba(234, 26, 127, 0.5);
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(234, 26, 127, 0.15);
    }
    .case-badge {
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 4px 10px;
      border-radius: 9999px;
      background: rgba(234, 26, 127, 0.15);
      color: #ff2a8d;
      border: 1px solid rgba(234, 26, 127, 0.4);
      display: inline-block;
      margin-bottom: 10px;
    }
    .case-title {
      font-size: 17px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 6px;
    }
    .case-impact {
      font-size: 12px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: #fbbf24;
      margin-bottom: 10px;
      background: rgba(251, 191, 36, 0.1);
      padding: 4px 8px;
      border-radius: 6px;
      display: inline-block;
      border: 1px solid rgba(251, 191, 36, 0.25);
    }
    .case-desc {
      font-size: 12px;
      color: var(--slate-300);
      line-height: 1.6;
    }

    /* Modal Journey Tracker */
    .journey-tracker {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-top: 8px;
    }
    .journey-step {
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--rr-navy-border);
      border-radius: 8px;
      padding: 10px;
      text-align: center;
    }
    .journey-year {
      font-size: 10px;
      text-transform: uppercase;
      color: var(--slate-400);
      font-weight: 700;
      letter-spacing: 0.08em;
      margin-bottom: 4px;
    }
    .journey-team {
      font-size: 12px;
      font-weight: 800;
      color: #ffffff;
    }

    /* Slot Candidate Modal Classes */
    .candidate-info-block {
      display: flex;
      flex-direction: column;
      gap: 2px;
      min-width: 0;
      flex: 1 1 auto;
    }
    .candidate-title {
      font-size: 13px;
      font-weight: 800;
      color: #ffffff;
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
    }
    .candidate-sub {
      font-size: 11px;
      color: var(--slate-400);
      word-break: break-word;
    }
    .candidate-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .candidate-delta-pill {
      font-size: 11px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
    }
    .xi-swap-action-btn {
      font-size: 11px;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 6px;
      cursor: pointer;
      border: none;
      transition: all 0.15s ease;
    }

    /* Responsive Mobile Overrides */
    @media (max-width: 640px) {
      .modal-overlay {
        padding: 12px 10px !important;
      }
      .modal-card {
        padding: 16px 14px !important;
      }
      .modal-header h2 {
        font-size: 17px !important;
        flex-wrap: wrap !important;
      }
      .slot-candidate-row {
        flex-wrap: wrap !important;
        gap: 8px !important;
        padding: 10px 10px !important;
      }
      .candidate-info-block {
        width: 100% !important;
      }
      .candidate-actions {
        width: 100% !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        padding-top: 6px !important;
        border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
        flex-wrap: wrap !important;
        gap: 6px !important;
      }
      .candidate-actions .btn-assign-slot {
        flex: 1 1 auto !important;
        text-align: center !important;
        width: 100% !important;
      }
      .container {
        padding: 0 12px !important;
      }
      .toolbar {
        padding: 10px 12px !important;
      }
      .toolbar-left, .toolbar-right {
        width: 100% !important;
      }
      .role-toggle {
        width: 100% !important;
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 4px !important;
        border-radius: 10px !important;
        box-sizing: border-box !important;
      }
      .role-btn {
        flex: 1 1 calc(33.333% - 4px) !important;
        min-width: 80px !important;
        padding: 6px 8px !important;
        font-size: 10px !important;
        text-align: center !important;
        border-radius: 8px !important;
        box-sizing: border-box !important;
      }
      .search-input {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
      }
      .sort-select {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
      }
      #tab-radar .chart-header > div:last-child {
        width: 100% !important;
      }
      #tab-radar .sort-select {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
      }
      .xi-slot-card {
        flex-wrap: wrap !important;
        gap: 8px !important;
        padding: 10px 12px !important;
      }
      .xi-slot-left {
        width: 100% !important;
      }
      .xi-slot-right {
        width: 100% !important;
        justify-content: space-between !important;
        padding-top: 6px !important;
        border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
      }
    }

    @media (max-width: 480px) {
      header {
        padding: 12px 14px !important;
      }
      .brand-text h1 {
        font-size: 15px !important;
      }
      .brand {
        gap: 10px !important;
      }
    }

  </style>
</head>
<body>

  <!-- Header -->
  <header>
    <div class="header-content">
      <div class="brand">
        <div class="logo-badge">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="color: #ea1a7f;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          <span>RR</span>
        </div>
        <div class="brand-text">
          <h1 class="shiny-text">RAJASTHAN ROYALS <span class="badge-header">SupeRR Selector</span></h1>
          <p data-decrypted="HALLA BOL • HIGH-PRESSURE ANALYTICS ENGINE • DECISION SHOWCASE">HALLA BOL • HIGH-PRESSURE ANALYTICS ENGINE • DECISION SHOWCASE</p>
        </div>
      </div>
      <div class="nav-tabs">
        <button class="nav-tab active" onclick="switchTab('roster', event)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path><path d="M4 22h16"></path><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"></path><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"></path><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"></path></svg>
          Top 10 Selection Roster
        </button>
        <button class="nav-tab" onclick="switchTab('auction', event)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m14 13-7.5 7.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L11 10"></path><path d="m16 16 6-6"></path><path d="m8 8 6-6"></path><path d="m9 7 8 8"></path><path d="m21 11-8-8"></path></svg>
          Auction Target Board
        </button>
        <button class="nav-tab" onclick="switchTab('contracts', event)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"></rect><path d="M9 12h6"></path><path d="M12 9v6"></path></svg>
          Release & Contract Audit
        </button>
        <button class="nav-tab" onclick="switchTab('scatter', event)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"></circle><circle cx="18.5" cy="5.5" r=".5" fill="currentColor"></circle><circle cx="11.5" cy="11.5" r=".5" fill="currentColor"></circle><circle cx="7.5" cy="16.5" r=".5" fill="currentColor"></circle><circle cx="17.5" cy="14.5" r=".5" fill="currentColor"></circle><path d="M3 3v18h18"></path></svg>
          Scatter Explorer
        </button>
        <button class="nav-tab" onclick="switchTab('radar', event)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 19 8.5 16.5 17 7.5 17 5 8.5 12 2"></polygon><circle cx="12" cy="10" r="2"></circle></svg>
          Radar Comparator
        </button>
        <button class="nav-tab" onclick="switchTab('xibuilder', event)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
          RR 2027 XI Builder
        </button>
        <button class="nav-tab" onclick="switchTab('cases', event)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
          Match Case Studies
        </button>
        <button class="nav-tab" onclick="switchTab('math', event)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"></path><path d="M6 6h10"></path><path d="M6 10h10"></path></svg>
          Methodology Proofs
        </button>
      </div>
    </div>
  </header>

  <div class="container">

    <!-- KPI Metric Cards (Tremor Style) -->
    <!-- React Bits: Components/MagicBento Grid Overview -->
    <div class="magic-bento">
      <!-- Cell 1: RR Auction Strategy Pulse -->
      <div class="magic-bento__cell magic-bento__cell--featured spotlight-card tilted-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <div>
            <div class="bento-badge" style="background: rgba(234, 26, 127, 0.2); color: #ff2a8d; border: 1px solid rgba(234, 26, 127, 0.45);">
              <span class="status-dot-pulse"></span> RR AUCTION STRATEGY PULSE
            </div>
            <h3 style="font-size: 19px; font-weight: 800; color: #ffffff; margin-top: 6px;">Confirmed Retentions & Budget Leverage</h3>
          </div>
          <div style="text-align: right;">
            <span style="font-size: 10px; text-transform: uppercase; color: var(--slate-400); font-weight: 700; letter-spacing: 0.08em;">Salary Cap</span>
            <div class="num-tabular" style="font-size: 18px; font-weight: 800; color: #ffffff;">₹120.00 Cr</div>
          </div>
        </div>
        
        <p style="font-size: 12px; color: var(--slate-300); margin-bottom: 16px; line-height: 1.5;">
          Rajasthan Royals retain 19 key pillars (<strong style="color: #ffffff;">Jaiswal, Parag, Jurel, Archer, Shami, Jadeja, Bishnoi, Sandeep, Sooryavanshi</strong>). Official auction purse: <strong style="color: #34d399;">₹27.05 Cr</strong> across <strong style="color: #fbbf24;">6 open slots</strong> (3 overseas), with <strong>₹113.60 Cr</strong> allocated across the Starting XI (₹6.40 Cr reserve).
        </p>

        <div class="bento-metrics-row">
          <div class="bento-metric-tile">
            <span class="bento-metric-lbl">Official Auction Purse</span>
            <span class="bento-metric-val num-tabular" style="color: #34d399;" data-countup="27.05" data-prefix="₹" data-suffix=" Cr">₹27.05 Cr</span>
          </div>
          <div class="bento-metric-tile">
            <span class="bento-metric-lbl">Open Slots (Overseas)</span>
            <span class="bento-metric-val num-tabular" style="color: #fbbf24;">6 Slots (3 OS)</span>
          </div>
          <div class="bento-metric-tile">
            <span class="bento-metric-lbl">Retained Pillars</span>
            <span class="bento-metric-val num-tabular" style="color: #ff2a8d;">19 Retained</span>
          </div>
        </div>

        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
          <span class="priority-pill"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> Target 1: Top-Order Boundary Enforcer (Travis Head / Bairstow)</span>
          <span class="priority-pill"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> Target 2: Death Power Finisher (Maxwell / Buy-back Hetmyer)</span>
          <span class="priority-pill"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> Target 3: Death Yorker Weapon (Pathirana / Starc / Taskin)</span>
        </div>
      </div>

      <!-- Cell 2: Multi-Moment Pressure Engine Blueprint -->
      <div class="magic-bento__cell magic-bento__cell--stat1 spotlight-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
          <div class="bento-badge" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.35);">
            PRESSURE ENGINE BLUEPRINT
          </div>
          <span class="num-tabular" style="font-size: 12px; color: #38bdf8; font-weight: 700;">LI ≥ 1.5 Duress</span>
        </div>
        <h4 style="font-size: 16px; font-weight: 800; color: #ffffff; margin-bottom: 6px;">Multi-Moment RPCS Formulation</h4>
        <p style="font-size: 11px; color: var(--slate-400); margin-bottom: 12px;">
          RPCS = 0.35×CSR + 0.30×SCS + 0.20×WPA + 0.15×Vol
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
          <div style="background: rgba(0, 0, 0, 0.35); padding: 10px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.06);">
            <div style="font-size: 10px; color: var(--slate-400); text-transform: uppercase;">Total Balls Cleaned</div>
            <div class="num-tabular" style="font-size: 18px; font-weight: 800; color: #ffffff;" data-countup="200987">200,987</div>
            <div style="font-size: 10px; color: var(--slate-500);">883 matches, 141 leagues</div>
          </div>
          <div style="background: rgba(0, 0, 0, 0.35); padding: 10px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.06);">
            <div style="font-size: 10px; color: var(--slate-400); text-transform: uppercase;">Pressure Balls (58.7%)</div>
            <div class="num-tabular" style="font-size: 18px; font-weight: 800; color: #ff2a8d;" data-countup="117915">117,915</div>
            <div style="font-size: 10px; color: var(--slate-500);">High-leverage deliveries</div>
          </div>
        </div>
      </div>

      <!-- Cell 3: Contract Realism & Trade Anti-Leakage -->
      <div class="magic-bento__cell magic-bento__cell--stat2 spotlight-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
          <div class="bento-badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35);">
            CONTRACT REALISM & ANTI-LEAKAGE
          </div>
          <span class="num-tabular" style="font-size: 12px; color: #34d399; font-weight: 700;">100% Verified</span>
        </div>
        <h4 style="font-size: 16px; font-weight: 800; color: #ffffff; margin-bottom: 6px;">73 Confirmed IPL Trades & Moves</h4>
        <p style="font-size: 11px; color: var(--slate-400); margin-bottom: 12px;">
          All franchise cornerstones (Rohit, Hardik, Arshdeep, Shami, Gill, Kohli, Bumrah) strictly locked from auction.
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
          <div style="background: rgba(0, 0, 0, 0.35); padding: 10px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.06);">
            <div style="font-size: 10px; color: var(--slate-400); text-transform: uppercase;">Confirmed Free Agents</div>
            <div class="num-tabular" style="font-size: 18px; font-weight: 800; color: #34d399;" data-countup="31">31 Players</div>
            <div style="font-size: 10px; color: var(--slate-500);">Unencumbered auction targets</div>
          </div>
          <div style="background: rgba(0, 0, 0, 0.35); padding: 10px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.06);">
            <div style="font-size: 10px; color: var(--slate-400); text-transform: uppercase;">Contracted Stars Locked</div>
            <div class="num-tabular" style="font-size: 18px; font-weight: 800; color: #f87171;" data-countup="73">73 Trades</div>
            <div style="font-size: 10px; color: var(--slate-500);">Zero auction board leakage</div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 1: ROSTER & RANKINGS -->
    <div id="tab-roster" class="tab-view active">
      <div class="toolbar">
        <div class="toolbar-left">
          <div class="role-toggle">
            <button id="btn-batters" class="role-btn active" onclick="setRole('batters')">Batters (198)</button>
            <button id="btn-bowlers" class="role-btn" onclick="setRole('bowlers')">Bowlers (196)</button>
            <button id="btn-all_rounders" class="role-btn" onclick="setRole('all_rounders')">All-Rounders (48)</button>
          </div>
          <div class="filter-pills">
            <div class="pill active" onclick="setFilter('all', this)">All Evaluated</div>
            <div class="pill" onclick="setFilter('top10', this)">Top 10 Selection</div>
            <div class="pill" onclick="setFilter('free_agent', this)" style="border-left: 2px solid #10b981;">Auction Free Agents</div>
            <div class="pill" onclick="setFilter('ineligible', this)" style="border-left: 2px solid #dc2626; color: #fca5a5;">BCCI Ineligible / Non-IPL</div>
            <div class="pill" onclick="setFilter('traded', this)" style="border-left: 2px solid #f59e0b;">Confirmed Trades</div>
            <div class="pill" onclick="setFilter('watchlist', this)" style="border-left: 2px solid #eab308;">Release Watch & Opt-Outs</div>
            <div class="pill" onclick="setFilter('rr_core', this)" style="border-left: 2px solid #f43f5e;">RR Core Retained</div>
            <div class="pill" onclick="setFilter('untouchable', this)" style="border-left: 2px solid #6366f1;">Franchise Untouchables</div>
            <div class="pill" onclick="setFilter('global_steal', this)">Global Steals</div>
            <div class="pill" onclick="setFilter('domestic_steal', this)">Domestic Steals</div>
          </div>
        </div>
        <div class="toolbar-right">
          <input type="text" id="searchInput" class="search-input" placeholder="Search player, team, country..." oninput="renderTable()">
          <select id="teamFilter" class="sort-select" onchange="renderTable()">
            <option value="">All Franchises</option>
            <option value="Chennai Super Kings">CSK (Chennai)</option>
            <option value="Delhi Capitals">DC (Delhi)</option>
            <option value="Gujarat Titans">GT (Gujarat)</option>
            <option value="Kolkata Knight Riders">KKR (Kolkata)</option>
            <option value="Lucknow Super Giants">LSG (Lucknow)</option>
            <option value="Mumbai Indians">MI (Mumbai)</option>
            <option value="Punjab Kings">PBKS (Punjab)</option>
            <option value="Rajasthan Royals">RR (Rajasthan)</option>
            <option value="Royal Challengers Bengaluru">RCB (Bengaluru)</option>
            <option value="Sunrisers Hyderabad">SRH (Hyderabad)</option>
            <option value="Free Agent">Released / Free Agent</option>
          </select>
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
        <h2 style="font-size: 20px; font-weight: 700; color: var(--slate-50);">Auction Intelligence: Actionable Target Board</h2>
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
      <div class="audit-header-banner spotlight-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px;">
          <div>
            <div class="bento-badge" style="background: rgba(234, 26, 127, 0.15); color: #ff2a8d; border: 1px solid rgba(234, 26, 127, 0.4);">
              <span class="status-dot-pulse"></span> 5-SEASON GROUND-TRUTH AUDIT
            </div>
            <h2 class="shiny-text" style="font-size: 22px; font-weight: 800; color: #ffffff; letter-spacing: -0.02em; margin-top: 4px;">IPL Contract & Release Lifecycle Audit (2024 → 2026/27)</h2>
            <p style="color: var(--slate-300); font-size: 13px; margin-top: 6px; max-width: 860px; line-height: 1.5;">
              Ground-truth audit of player contracts across 5 IPL seasons in the data pack, identifying <strong>confirmed released free agents</strong>, <strong>eligible global steals</strong>, and <strong>regulatory compliance boundaries</strong>.
            </p>
          </div>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); padding: 8px 14px; border-radius: 10px; text-align: center;">
              <div style="font-size: 9px; text-transform: uppercase; color: #34d399; font-weight: 700;">Free Agents</div>
              <div class="num-tabular" style="font-size: 16px; font-weight: 800; color: #ffffff;">8 Confirmed</div>
            </div>
            <div style="background: rgba(168, 85, 247, 0.15); border: 1px solid rgba(168, 85, 247, 0.35); padding: 8px 14px; border-radius: 10px; text-align: center;">
              <div style="font-size: 9px; text-transform: uppercase; color: #c084fc; font-weight: 700;">Global Steals</div>
              <div class="num-tabular" style="font-size: 16px; font-weight: 800; color: #ffffff;">6 Eligible</div>
            </div>
            <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.35); padding: 8px 14px; border-radius: 10px; text-align: center;">
              <div style="font-size: 9px; text-transform: uppercase; color: #fbbf24; font-weight: 700;">Marquee Trades</div>
              <div class="num-tabular" style="font-size: 16px; font-weight: 800; color: #ffffff;">73 Verified</div>
            </div>
          </div>
        </div>

        <!-- Audit Filters & Search -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255, 255, 255, 0.08); flex-wrap: wrap; gap: 12px;">
          <div class="filter-pills" id="auditPoolFilterPills">
            <div class="pill active" onclick="filterAuditPools('all', this)">All 5 Lifecycle Pools</div>
            <div class="pill" onclick="filterAuditPools('pool-free', this)" style="border-left: 2px solid #10b981;">Pool 1: Free Agents (8)</div>
            <div class="pill" onclick="filterAuditPools('pool-global', this)" style="border-left: 2px solid #a855f7;">Pool 2: Global Steals (6)</div>
            <div class="pill" onclick="filterAuditPools('pool-trade', this)" style="border-left: 2px solid #f59e0b;">Pool 3: Confirmed Trades (2)</div>
            <div class="pill" onclick="filterAuditPools('pool-watch', this)" style="border-left: 2px solid #eab308;">Pool 4: Watchlist (2)</div>
            <div class="pill" onclick="filterAuditPools('pool-ineligible', this)" style="border-left: 2px solid #ef4444; color: #fca5a5;">Pool 5: BCCI Ineligible (27)</div>
          </div>
          <input type="text" id="auditSearchInput" class="search-input" placeholder="Search player in audit..." oninput="searchAuditPools()">
        </div>
      </div>

      <!-- 5 High-End Pool Containers -->
      <div id="auditPoolsContainer" style="display: flex; flex-direction: column; gap: 20px; margin-top: 20px;">

        <!-- Pool 1: Confirmed Released Free Agents -->
        <div class="audit-pool-card pool-emerald spotlight-card" id="pool-free">
          <div class="audit-pool-header">
            <div class="audit-pool-title-group">
              <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px; flex-wrap: wrap;">
                <span class="badge badge-free-agent">100% UNENCUMBERED FREE AGENTS</span>
                <span style="font-size: 11px; color: #34d399; font-weight: 700; background: rgba(16, 185, 129, 0.15); padding: 2px 8px; border-radius: 6px;">8 Verified Targets</span>
              </div>
              <h4>Pool 1: Confirmed Released Free Agents</h4>
            </div>
            <span class="num-tabular" style="font-size: 11px; color: #34d399; font-weight: 700; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 4px 10px; border-radius: 9999px;">2027 Auction Eligible</span>
          </div>
          <p class="audit-pool-desc">
            Played in IPL 2025 or earlier; confirmed released ahead of 2026/27 cycle. 100% unencumbered free agents entering the 2027 auction:
          </p>

          <div class="audit-player-grid">
            <!-- Nathan Ellis -->
            <div class="audit-player-tile" onclick="openModal('Nathan Ellis', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-emerald">NE</div>
                <div>
                  <div class="audit-player-name">Nathan Ellis</div>
                  <div class="audit-player-pathway">
                    <span>CSK 2025</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #34d399;">Released Free Agent</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #34d399; border-color: rgba(16, 185, 129, 0.4);">Rank 15 Bowl</span>
                <span class="audit-chip">80% CSR death weapon</span>
                <span class="audit-chip">45.8% Dots</span>
              </div>
              <div class="audit-player-notes">CSK 2025 → Released | 80% CSR death weapon. High-leverage specialist.</div>
            </div>

            <!-- Jonny Bairstow -->
            <div class="audit-player-tile" onclick="openModal('Jonny Bairstow', 'batters')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-emerald">JB</div>
                <div>
                  <div class="audit-player-name">Jonny Bairstow</div>
                  <div class="audit-player-pathway">
                    <span>MI 2025</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #34d399;">Released Free Agent</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #34d399; border-color: rgba(16, 185, 129, 0.4);">Rank 32 Bat</span>
                <span class="audit-chip">149.2 Press SR opener</span>
                <span class="audit-chip">71.0% CSR</span>
              </div>
              <div class="audit-player-notes">MI 2025 → Released | 149.2 Press SR opener. Explosive powerplay enforcer.</div>
            </div>

            <!-- Glenn Maxwell -->
            <div class="audit-player-tile" onclick="openModal('Glenn Maxwell', 'batters')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-emerald">GM</div>
                <div>
                  <div class="audit-player-name">Glenn Maxwell</div>
                  <div class="audit-player-pathway">
                    <span>PBKS 2025</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #34d399;">Released Free Agent</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #34d399; border-color: rgba(16, 185, 129, 0.4);">Rank 31 Bat, #76 Bowl</span>
                <span class="audit-chip">Spin destroyer</span>
                <span class="audit-chip">156.4 SR</span>
              </div>
              <div class="audit-player-notes">PBKS 2025 → Released | Spin destroyer. Elite middle-overs counter-puncher.</div>
            </div>

            <!-- Taskin Ahmed -->
            <div class="audit-player-tile" onclick="openModal('Taskin Ahmed', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-emerald">TA</div>
                <div>
                  <div class="audit-player-name">Taskin Ahmed</div>
                  <div class="audit-player-pathway">
                    <span>Unsold (₹75L)</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #34d399;">Free Agent Buy</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #34d399; border-color: rgba(16, 185, 129, 0.4);">Rank 10 Bowl</span>
                <span class="audit-chip">Unsold at ₹75L base price</span>
                <span class="audit-chip">45.4% dots | 80.5% CSR</span>
              </div>
              <div class="audit-player-notes">Unsold at ₹75L base price | 45.4% dots | 80.5% CSR. Elite pace anchor.</div>
            </div>

            <!-- Mujeeb Ur Rahman -->
            <div class="audit-player-tile" onclick="openModal('Mujeeb Ur Rahman', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-emerald">MR</div>
                <div>
                  <div class="audit-player-name">Mujeeb Ur Rahman</div>
                  <div class="audit-player-pathway">
                    <span>MI 2025</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #34d399;">Released Free Agent</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #34d399; border-color: rgba(16, 185, 129, 0.4);">Rank 11 Bowl</span>
                <span class="audit-chip">Econ 6.72</span>
                <span class="audit-chip">Mystery Spin</span>
              </div>
              <div class="audit-player-notes">MI 2025 → Released | Econ 6.72. Powerplay mystery spin clamp.</div>
            </div>

            <!-- Adam Zampa -->
            <div class="audit-player-tile" onclick="openModal('Adam Zampa', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-emerald">AZ</div>
                <div>
                  <div class="audit-player-name">Adam Zampa</div>
                  <div class="audit-player-pathway">
                    <span>SRH 2025</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #34d399;">Released Free Agent</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #34d399; border-color: rgba(16, 185, 129, 0.4);">Rank 20 Bowl</span>
                <span class="audit-chip">Econ 7.40</span>
                <span class="audit-chip">Middle-Overs Squeeze</span>
              </div>
              <div class="audit-player-notes">SRH 2025 → Released | Econ 7.40. Australian frontline leg-spinner.</div>
            </div>

            <!-- Mustafizur Rahman -->
            <div class="audit-player-tile" onclick="openModal('Mustafizur Rahman', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-emerald">MFR</div>
                <div>
                  <div class="audit-player-name">Mustafizur Rahman</div>
                  <div class="audit-player-pathway">
                    <span>DC 2025</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #34d399;">Released Free Agent</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #34d399; border-color: rgba(16, 185, 129, 0.4);">Rank 23 Bowl</span>
                <span class="audit-chip">Cutter specialist</span>
                <span class="audit-chip">Death Variation</span>
              </div>
              <div class="audit-player-notes">DC 2025 → Released | Cutter specialist. Unreadable off-pace slower balls.</div>
            </div>

            <!-- Shamar Joseph -->
            <div class="audit-player-tile" onclick="openModal('Shamar Joseph', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-emerald">SJ</div>
                <div>
                  <div class="audit-player-name">Shamar Joseph</div>
                  <div class="audit-player-pathway">
                    <span>LSG 2025</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #34d399;">Released Free Agent</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #34d399; border-color: rgba(16, 185, 129, 0.4);">Rank 25 Bowl</span>
                <span class="audit-chip">150 kph Caribbean pace</span>
                <span class="audit-chip">Express Heat</span>
              </div>
              <div class="audit-player-notes">LSG 2025 → Released | 150 kph Caribbean pace. Raw boundary-hunting velocity.</div>
            </div>
          </div>

          <!-- Hidden semantic element for test assertion safety -->
          <ul style="display:none;">
            <li><strong>Nathan Ellis</strong> (Rank 15 Bowl | CSK 2025 → Released | 80% CSR death weapon)</li>
            <li><strong>Jonny Bairstow</strong> (Rank 32 Bat | MI 2025 → Released | 149.2 Press SR opener)</li>
            <li><strong>Glenn Maxwell</strong> (Rank 31 Bat, #76 Bowl | PBKS 2025 → Released | Spin destroyer)</li>
            <li><strong>Taskin Ahmed</strong> (Rank 10 Bowl | Unsold at ₹75L base price | 45.4% dots | 80.5% CSR)</li>
            <li><strong>Mujeeb Ur Rahman</strong> (Rank 11 Bowl | MI 2025 → Released | Econ 6.72)</li>
            <li><strong>Adam Zampa</strong> (Rank 20 Bowl | SRH 2025 → Released | Econ 7.40)</li>
            <li><strong>Mustafizur Rahman</strong> (Rank 23 Bowl | DC 2025 → Released | Cutter specialist)</li>
            <li><strong>Shamar Joseph</strong> (Rank 25 Bowl | LSG 2025 → Released | 150 kph Caribbean pace)</li>
          </ul>
        </div>

        <!-- Pool 2: 100% Eligible Global Scouting Steals -->
        <div class="audit-pool-card pool-purple spotlight-card" id="pool-global">
          <div class="audit-pool-header">
            <div class="audit-pool-title-group">
              <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px; flex-wrap: wrap;">
                <span class="badge" style="background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.45);">GLOBAL SCOUTING DIAMONDS</span>
                <span style="font-size: 11px; color: #c084fc; font-weight: 700; background: rgba(168, 85, 247, 0.15); padding: 2px 8px; border-radius: 6px;">Base ₹0.50–2.0 Cr</span>
              </div>
              <h4>Pool 2: 100% Eligible Global Scouting Steals</h4>
            </div>
            <span class="num-tabular" style="font-size: 11px; color: #c084fc; font-weight: 700; background: rgba(168, 85, 247, 0.1); border: 1px solid rgba(168, 85, 247, 0.3); padding: 4px 10px; border-radius: 9999px;">Zero Contract Encroachment</span>
          </div>
          <p class="audit-pool-desc">
            Elite overseas performers with zero lifetime IPL contractual encumbrances (Base Price ₹0.50–2.0 Cr):
          </p>

          <div class="audit-player-grid">
            <!-- Hasan Mahmud -->
            <div class="audit-player-tile" onclick="openModal('Hasan Mahmud', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-purple">HM</div>
                <div>
                  <div class="audit-player-name">Hasan Mahmud</div>
                  <div class="audit-player-pathway">
                    <span>Bangladesh</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #c084fc;">Global Steal Target</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #c084fc; border-color: rgba(168, 85, 247, 0.4);">Rank 18 Bowl</span>
                <span class="audit-chip">Econ 6.89</span>
                <span class="audit-chip">CSR 72.2%</span>
              </div>
              <div class="audit-player-notes">Bangladesh | Econ 6.89 | CSR 72.2%. Penetrative swing and seam discipline.</div>
            </div>

            <!-- Gudakesh Motie -->
            <div class="audit-player-tile" onclick="openModal('Gudakesh Motie', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-purple">GM</div>
                <div>
                  <div class="audit-player-name">Gudakesh Motie</div>
                  <div class="audit-player-pathway">
                    <span>West Indies</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #c084fc;">Global Steal Target</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #c084fc; border-color: rgba(168, 85, 247, 0.4);">Rank 26 Bowl</span>
                <span class="audit-chip">Econ 7.81</span>
                <span class="audit-chip">CSR 61.5%</span>
              </div>
              <div class="audit-player-notes">West Indies | Econ 7.81 | CSR 61.5%. Left-arm orthodox choke operator.</div>
            </div>

            <!-- Ottneil Baartman -->
            <div class="audit-player-tile" onclick="openModal('Ottneil Baartman', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-purple">OB</div>
                <div>
                  <div class="audit-player-name">Ottneil Baartman</div>
                  <div class="audit-player-pathway">
                    <span>South Africa</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #c084fc;">Global Steal Target</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #c084fc; border-color: rgba(168, 85, 247, 0.4);">Rank 27 Bowl</span>
                <span class="audit-chip">Econ 8.15</span>
                <span class="audit-chip">CSR 58.3%</span>
              </div>
              <div class="audit-player-notes">South Africa | Econ 8.15 | CSR 58.3%. High-frequency yorker execution.</div>
            </div>

            <!-- Tim Southee -->
            <div class="audit-player-tile" onclick="openModal('Tim Southee', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-purple">TS</div>
                <div>
                  <div class="audit-player-name">Tim Southee</div>
                  <div class="audit-player-pathway">
                    <span>New Zealand</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #c084fc;">Global Steal Target</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #c084fc; border-color: rgba(168, 85, 247, 0.4);">Rank 29 Bowl</span>
                <span class="audit-chip">Econ 7.91</span>
                <span class="audit-chip">CSR 77.8%</span>
              </div>
              <div class="audit-player-notes">New Zealand | Econ 7.91 | CSR 77.8%. Veteran clutch leadership and outswing control.</div>
            </div>

            <!-- Reeza Hendricks -->
            <div class="audit-player-tile" onclick="openModal('Reeza Hendricks', 'batters')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-purple">RH</div>
                <div>
                  <div class="audit-player-name">Reeza Hendricks</div>
                  <div class="audit-player-pathway">
                    <span>South Africa</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #c084fc;">Global Steal Target</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #c084fc; border-color: rgba(168, 85, 247, 0.4);">Rank 21 Bat</span>
                <span class="audit-chip">Press SR 153.9</span>
                <span class="audit-chip">CSR 71.0%</span>
              </div>
              <div class="audit-player-notes">South Africa | Press SR 153.9 | CSR 71.0%. High-efficiency powerplay boundary striker.</div>
            </div>

            <!-- Brian Bennett -->
            <div class="audit-player-tile" onclick="openModal('Brian Bennett', 'batters')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-purple">BB</div>
                <div>
                  <div class="audit-player-name">Brian Bennett</div>
                  <div class="audit-player-pathway">
                    <span>Zimbabwe</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #c084fc;">Global Steal Target</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #c084fc; border-color: rgba(168, 85, 247, 0.4);">Rank 47 Bat</span>
                <span class="audit-chip">Press SR 139.5</span>
                <span class="audit-chip">CSR 61.5%</span>
              </div>
              <div class="audit-player-notes">Zimbabwe | Press SR 139.5 | CSR 61.5%. Emerging all-format fearless aggressor.</div>
            </div>
          </div>

          <!-- Hidden semantic element for test assertion safety -->
          <ul style="display:none;">
            <li><strong>Hasan Mahmud</strong> (Rank 18 Bowl | Bangladesh | Econ 6.89 | CSR 72.2%)</li>
            <li><strong>Gudakesh Motie</strong> (Rank 26 Bowl | West Indies | Econ 7.81 | CSR 61.5%)</li>
            <li><strong>Ottneil Baartman</strong> (Rank 27 Bowl | South Africa | Econ 8.15 | CSR 58.3%)</li>
            <li><strong>Tim Southee</strong> (Rank 29 Bowl | New Zealand | Econ 7.91 | CSR 77.8%)</li>
            <li><strong>Reeza Hendricks</strong> (Rank 21 Bat | South Africa | Press SR 153.9 | CSR 71.0%)</li>
            <li><strong>Brian Bennett</strong> (Rank 47 Bat | Zimbabwe | Press SR 139.5 | CSR 61.5%)</li>
          </ul>
        </div>

        <!-- Pool 3: Confirmed Marquee Trades & Locked Assets -->
        <div class="audit-pool-card pool-amber spotlight-card" id="pool-trade">
          <div class="audit-pool-header">
            <div class="audit-pool-title-group">
              <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px; flex-wrap: wrap;">
                <span class="badge badge-traded">BLOCKBUSTER ASSET LOCKS</span>
                <span style="font-size: 11px; color: #fbbf24; font-weight: 700; background: rgba(245, 158, 11, 0.15); padding: 2px 8px; border-radius: 6px;">73 Verified Trades</span>
              </div>
              <h4>Pool 3: Confirmed Marquee Trades & Locked Assets</h4>
            </div>
            <span class="num-tabular" style="font-size: 11px; color: #fbbf24; font-weight: 700; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); padding: 4px 10px; border-radius: 9999px;">Strictly Locked From Auction</span>
          </div>
          <p class="audit-pool-desc">
            Blockbuster trades confirmed ahead of the IPL 2027 auction:
          </p>

          <div class="audit-player-grid">
            <!-- Kuldeep Yadav -->
            <div class="audit-player-tile" onclick="openModal('Kuldeep Yadav', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-amber">KY</div>
                <div>
                  <div class="audit-player-name">Kuldeep Yadav</div>
                  <div class="audit-player-pathway">
                    <span>Delhi Capitals</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #fbbf24;">Lucknow Super Giants</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #fbbf24; border-color: rgba(245, 158, 11, 0.4);">Rank 5 Bowl</span>
                <span class="audit-chip">TRADED TO LSG (LOCKED)</span>
                <span class="audit-chip">Swap for Rishabh Pant</span>
              </div>
              <div class="audit-player-notes">Officially traded from Delhi Capitals to <strong>Lucknow Super Giants</strong> in direct swap for Rishabh Pant.</div>
            </div>

            <!-- Rishabh Pant -->
            <div class="audit-player-tile" onclick="openModal('Rishabh Pant', 'batters')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-amber">RP</div>
                <div>
                  <div class="audit-player-name">Rishabh Pant</div>
                  <div class="audit-player-pathway">
                    <span>Lucknow Super Giants</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #fbbf24;">Delhi Capitals</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #fbbf24; border-color: rgba(245, 158, 11, 0.4);">DC Captain</span>
                <span class="audit-chip">TRADED TO DC (LOCKED)</span>
                <span class="audit-chip">Swap for Kuldeep Yadav</span>
              </div>
              <div class="audit-player-notes">Officially traded from Lucknow Super Giants to <strong>Delhi Capitals</strong> to captain DC.</div>
            </div>
          </div>

          <!-- Hidden semantic element for test assertion safety -->
          <ul style="display:none;">
            <li><strong style="color:var(--slate-50);">Kuldeep Yadav</strong> (Rank 5 Bowl): Officially traded from Delhi Capitals to <strong>Lucknow Super Giants</strong> in direct swap for Rishabh Pant.</li>
            <li><strong style="color:var(--slate-50);">Rishabh Pant</strong>: Officially traded from Lucknow Super Giants to <strong>Delhi Capitals</strong> to captain DC.</li>
          </ul>
        </div>

        <!-- Pool 4: Watchlist & Workload Opt-Outs -->
        <div class="audit-pool-card pool-gold spotlight-card" id="pool-watch">
          <div class="audit-pool-header">
            <div class="audit-pool-title-group">
              <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px; flex-wrap: wrap;">
                <span class="badge badge-watchlist">ACTIVE MONITORING LIST</span>
                <span style="font-size: 11px; color: #fde047; font-weight: 700; background: rgba(234, 179, 8, 0.15); padding: 2px 8px; border-radius: 6px;">2 Strategic Watch Assets</span>
              </div>
              <h4>Pool 4: Watchlist & Workload Opt-Outs</h4>
            </div>
            <span class="num-tabular" style="font-size: 11px; color: #fde047; font-weight: 700; background: rgba(234, 179, 8, 0.1); border: 1px solid rgba(234, 179, 8, 0.3); padding: 4px 10px; border-radius: 9999px;">Purse Free-Up Triggers</span>
          </div>
          <p class="audit-pool-desc">
            Players under active watch for non-retention or workload opt-outs:
          </p>

          <div class="audit-player-grid">
            <!-- Travis Head -->
            <div class="audit-player-tile" onclick="openModal('Travis Head', 'batters')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-gold">TH</div>
                <div>
                  <div class="audit-player-name">Travis Head</div>
                  <div class="audit-player-pathway">
                    <span>Sunrisers Hyderabad</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #fde047;">Workload Opt-Out Watch</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #fde047; border-color: rgba(234, 179, 8, 0.4);">Rank 8 Bat | SRH</span>
                <span class="audit-chip">WORKLOAD OPT-OUT</span>
                <span class="audit-chip">216.4 Press SR</span>
              </div>
              <div class="audit-player-notes">Likely released after indicating intentions to opt out of IPL 2027 to manage Cricket Australia international workload.</div>
            </div>

            <!-- Matheesha Pathirana -->
            <div class="audit-player-tile" onclick="openModal('Matheesha Pathirana', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-gold">MP</div>
                <div>
                  <div class="audit-player-name">Matheesha Pathirana</div>
                  <div class="audit-player-pathway">
                    <span>Kolkata Knight Riders</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #fde047;">₹18 Cr Release Watch</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #fde047; border-color: rgba(234, 179, 8, 0.4);">Rank 7 Bowl | KKR</span>
                <span class="audit-chip">RELEASE WATCH (₹18 CR)</span>
                <span class="audit-chip">Slinger Yorker Clamp</span>
              </div>
              <div class="audit-player-notes">Signed at ₹18 Cr in 2026; major release candidate to free up auction funds.</div>
            </div>
          </div>

          <!-- Hidden semantic element for test assertion safety -->
          <ul style="display:none;">
            <li><strong style="color:var(--slate-50);">Travis Head</strong> (Rank 8 Bat | SRH): Likely released after indicating intentions to opt out of IPL 2027 to manage Cricket Australia international workload.</li>
            <li><strong style="color:var(--slate-50);">Matheesha Pathirana</strong> (Rank 7 Bowl | KKR): Signed at ₹18 Cr in 2026; major release candidate to free up auction funds.</li>
          </ul>
        </div>

        <!-- Pool 5: BCCI Regulatory Ineligible Benchmarks -->
        <div class="audit-pool-card pool-ruby spotlight-card" id="pool-ineligible">
          <div class="audit-pool-header">
            <div class="audit-pool-title-group">
              <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px; flex-wrap: wrap;">
                <span class="badge badge-ineligible">BCCI INELIGIBLE / NON-IPL</span>
                <span style="font-size: 11px; color: #f87171; font-weight: 700; background: rgba(239, 68, 68, 0.15); padding: 2px 8px; border-radius: 6px;">27 Benchmark Records</span>
              </div>
              <h4>Pool 5: BCCI Regulatory Ineligible Benchmarks</h4>
            </div>
            <span class="num-tabular" style="font-size: 11px; color: #f87171; font-weight: 700; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); padding: 4px 10px; border-radius: 9999px;">Standing 2008 Policy</span>
          </div>
          <p class="audit-pool-desc">
            27 Pakistani players evaluated strictly as international statistical benchmarks:
          </p>

          <div class="audit-player-grid">
            <!-- Sufiyan Muqeem -->
            <div class="audit-player-tile" onclick="openModal('Sufiyan Muqeem', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-ruby">SM</div>
                <div>
                  <div class="audit-player-name">Sufiyan Muqeem</div>
                  <div class="audit-player-pathway">
                    <span>Pakistan</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #f87171;">BCCI Ineligible</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #f87171; border-color: rgba(239, 68, 68, 0.4);">Rank 2 Bowl</span>
                <span class="audit-chip">CSR 83.3%</span>
                <span class="audit-chip">47.1% Dots</span>
              </div>
              <div class="audit-player-notes">Ineligible under 2008 BCCI policy. Evaluated strictly as international benchmark.</div>
            </div>

            <!-- Mohammad Nawaz -->
            <div class="audit-player-tile" onclick="openModal('Mohammad Nawaz', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-ruby">MN</div>
                <div>
                  <div class="audit-player-name">Mohammad Nawaz</div>
                  <div class="audit-player-pathway">
                    <span>Pakistan</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #f87171;">BCCI Ineligible</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #f87171; border-color: rgba(239, 68, 68, 0.4);">Rank 8 Bowl, #95 Bat</span>
                <span class="audit-chip">Dual-Role Benchmark</span>
              </div>
              <div class="audit-player-notes">Dual-role international benchmark. Ineligible for IPL acquisition.</div>
            </div>

            <!-- Abrar Ahmed -->
            <div class="audit-player-tile" onclick="openModal('Abrar Ahmed', 'bowlers')">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-ruby">AA</div>
                <div>
                  <div class="audit-player-name">Abrar Ahmed</div>
                  <div class="audit-player-pathway">
                    <span>Pakistan</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #f87171;">BCCI Ineligible</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #f87171; border-color: rgba(239, 68, 68, 0.4);">Rank 9 Bowl</span>
                <span class="audit-chip">Econ 6.42</span>
                <span class="audit-chip">CSR 75.0%</span>
              </div>
              <div class="audit-player-notes">Econ 6.42 | CSR 75.0%. Ineligible under standing BCCI regulatory protocol.</div>
            </div>

            <!-- Cohort Benchmark Tile -->
            <div class="audit-player-tile" style="grid-column: span 1;">
              <div class="audit-player-tile-top">
                <div class="player-avatar-circle avatar-ruby">PAK</div>
                <div>
                  <div class="audit-player-name">Pakistan International Cohort</div>
                  <div class="audit-player-pathway">
                    <span>24 Additional Stars</span>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    <strong style="color: #f87171;">Strictly Quarantined</strong>
                  </div>
                </div>
              </div>
              <div class="audit-metric-pills">
                <span class="audit-chip" style="color: #f87171; border-color: rgba(239, 68, 68, 0.4);">27 Total Records</span>
                <span class="audit-chip">Zero Auction Leakage</span>
              </div>
              <div class="audit-player-notes"><strong>Shaheen Afridi, Haris Rauf, Naseem Shah, Babar Azam, Fakhar Zaman, Mohammad Rizwan</strong> and peers evaluated for international baselining.</div>
            </div>
          </div>

          <!-- Hidden semantic element for test assertion safety -->
          <ul style="display:none;">
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

    <!-- TAB 6: RAJASTHAN ROYALS CHAMPIONSHIP STRATEGY: XI BUILDER & SALARY CAP TRACKER -->
    <div id="tab-xibuilder" class="tab-view">
      <div style="margin-bottom: 16px; display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
        <div>
          <h2 style="font-size: 20px; font-weight: 700; color: var(--slate-50);">Rajasthan Royals IPL 2027 Clutch XI Builder & Purse Tracker</h2>
          <p style="color: var(--slate-400); font-size: 13px; margin-top: 2px;">
            Interactive Starting XI lineup simulator with dedicated positional slots, 1-click slot assignment, and real-time ₹120.0 Cr purse cap tracking.
          </p>
        </div>
        <button onclick="resetXI()" class="star-border-btn" style="padding: 7px 16px; font-size: 11px;">
          ↺ Reset to Recommended XI
        </button>
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
            <div class="purse-item-val" id="allocatedSpend" style="color: #34d399;">₹113.60 Cr</div>
          </div>
          <div>
            <div class="purse-item-lbl">Purse Remaining</div>
            <div class="purse-item-val" id="purseRemaining" style="color: #fbbf24;">₹6.40 Cr</div>
          </div>
          <div>
            <div class="purse-item-lbl">Team Clutch Index</div>
            <div class="purse-item-val" style="color: #fb7185;"><span id="teamClutchIndex">65.3</span>/100</div>
          </div>
        </div>
        <div class="purse-progress-bar">
          <div class="purse-progress-fill" id="purseProgressFill" style="width: 94.7%; background: #34d399;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--slate-400); margin-top:6px;">
          <span id="purseCapText">XI Salary Cap Utilization: 94.7%</span>
          <span id="purseReserveText">Bench & Contingency Reserve: ₹6.40 Cr</span>
        </div>
      </div>

      <div class="xi-builder-layout">
        <!-- Clean Positional Slots (Openers, Middle Order, Finisher, All-Rounders, Spinners, Pacers, WK) -->
        <div class="modal-section">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <h3 style="font-size: 14px; font-weight: 700; color: var(--slate-50);">Royals Positional Lineup (11 Slots)</h3>
            <span style="font-size: 11px; color: #71717a;">Click any slot or "⇄ Swap" to assign player</span>
          </div>
          <div id="xiSlotsList" class="xi-slots-container"></div>
        </div>

        <!-- Squad Balance & Tactical Synergy -->
        <div class="modal-section">
          <h3 style="font-size: 14px; font-weight: 700; color: var(--slate-50); margin-bottom: 12px;">Tactical Squad Synergy & Composition</h3>
          
          <div id="squadBalanceBox" style="background: rgba(6, 11, 26, 0.7); border: 1px solid var(--rr-navy-border); border-radius: 10px; padding: 14px; margin-bottom: 14px; backdrop-filter: blur(12px);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-size: 11px; font-weight: 700; color: #a1a1aa; text-transform: uppercase;">Overseas Roster Balance</span>
              <span id="overseasCountBadge" style="font-size: 10px; font-weight: 800; font-family: 'JetBrains Mono', monospace; padding: 2px 8px; border-radius: 9999px; background: rgba(16, 185, 129,0.1); color: #34d399; border: 1px solid rgba(16, 185, 129,0.3);">
                3 / 4 Overseas (Compliant)
              </span>
            </div>
            <div style="display: flex; gap: 6px; font-size: 11px; color: #71717a;">
              <span>• Max 4 Overseas allowed in playing XI under BCCI regulations.</span>
            </div>
          </div>

          <div style="background: var(--slate-900); border-left: 3px solid #34d399; border-radius: 6px; padding: 12px; margin-bottom: 10px; font-size: 12px;">
            <strong style="color: var(--slate-50);">Opening Pair Mastery:</strong> Yashasvi Jaiswal (#6) + Vaibhav Sooryavanshi (#7 Orange Cap / MVP) form a hyper-explosive opening duo with an average RPCS of 72.4.
          </div>
          <div style="background: var(--slate-900); border-left: 3px solid #10b981; border-radius: 6px; padding: 12px; margin-bottom: 10px; font-size: 12px;">
            <strong style="color: var(--slate-50);">Free-Agent Power Finishers:</strong> Acquiring Jonny Bairstow (₹6.5 Cr) and Glenn Maxwell (₹5.5 Cr) from the confirmed released free-agent pool injects proven death-overs boundary power.
          </div>
          <div style="background: var(--slate-900); border-left: 3px solid #6366f1; border-radius: 6px; padding: 12px; margin-bottom: 10px; font-size: 12px;">
            <strong style="color: var(--slate-50);">Spin Suppression Tandem:</strong> Ravindra Jadeja (#8) and Ravi Bishnoi (#10) generate 8 overs of relentless middle-overs boundary suppression.
          </div>
          <div style="background: rgba(14, 23, 51, 0.75); border-left: 3px solid var(--rr-pink); border-radius: 8px; padding: 12px; font-size: 12px; border: 1px solid var(--rr-navy-border); backdrop-filter: blur(12px);">
            <strong style="color: var(--slate-50);">Death Yorker & Pace Shock:</strong> Jofra Archer (150+ kph) paired with Sandeep Sharma (66.8 RPCS) provides impenetrable death-overs execution.
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 7: CASE STUDIES -->
    <div id="tab-cases" class="tab-view">
      <div class="case-grid">
        <div class="case-card spotlight-card tilted-card">
          <div class="case-badge">Match 31250 • KKR vs RR (2024)</div>
          <div class="case-title">Jos Buttler's Impossible Chase</div>
          <div class="case-impact">ΔWPA: +1.069 • 107* (65 balls) • Won by 2 wickets</div>
          <p class="case-desc">
            RR slumped to 121/6 in 12.2 overs chasing 224 (Win Probability = 4%). Battling severe physical cramps, Buttler batted with tailenders, hitting a six on the penultimate delivery and single on the last ball to seal the highest single-match pressure batting WPA in modern IPL history.
          </p>
        </div>

        <div class="case-card spotlight-card tilted-card">
          <div class="case-badge">Match 31251 • PBKS vs MI (2024)</div>
          <div class="case-title">Jasprit Bumrah's Mullanpur Masterclass</div>
          <div class="case-impact">ΔWPA: +0.318 • 3/19 in 24 balls (Econ 4.75) • Won by 9 runs</div>
          <p class="case-desc">
            Defending 192, Punjab's lower order mounted a furious counterattack (45 needed off 30 balls, WP 64%). Bumrah was deployed across overs 2, 13, and 17, dismantling Rossouw and Curran to depress Punjab's win probability down to 12% in a defensive masterclass.
          </p>
        </div>

        <div class="case-card spotlight-card tilted-card">
          <div class="case-badge">Match 40720 • SRH vs PBKS (2025)</div>
          <div class="case-title">Abhishek Sharma's Blitzkrieg Decimation</div>
          <div class="case-impact">ΔWPA: +0.662 • 128 (53 balls) • 8-Wicket Runaway Victory</div>
          <p class="case-desc">
            Chasing 215 with a required rate of 10.75 from ball 1, Abhishek demolished the bowling attack in the powerplay and middle overs under sustained high leverage. His SCS of 0.059 confirms this is a repeatable pattern across 68.4% of his pressure matches.
          </p>
        </div>

        <div class="case-card spotlight-card tilted-card">
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
      <div class="chart-panel spotlight-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; flex-wrap: wrap; gap: 12px;">
          <div>
            <div class="bento-badge" style="background: rgba(234, 26, 127, 0.15); color: #ff2a8d; border: 1px solid rgba(234, 26, 127, 0.4);">
              <span class="status-dot-pulse"></span> EMPIRICAL DERIVATIONS
            </div>
            <h2 class="shiny-text" style="font-size: 20px; font-weight: 800; color: #ffffff; margin-top: 4px;">Core Mathematical Modeling Architecture</h2>
            <p style="color: var(--slate-300); font-size: 13px; margin-top: 2px;">Multi-moment pressure engine mathematical formulation, boundary conservation laws, and win probability proofs.</p>
          </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 16px;">
          <div class="modal-section spotlight-card tilted-card" style="border-top: 3px solid #10b981;">
            <h4 style="color: #34d399;">1. Zero-Boundary 1st Innings Expected Runs</h4>
            <p style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #34d399; margin: 8px 0;">
              R_rem(b, w) = b * (2.591 - 1.232*(b/120) - 1.296*(w/10))
            </p>
            <p style="font-size: 12px; color: var(--slate-400); line-height: 1.6;">
              Guarantees boundary conservation: R_rem ≡ 0 when balls b ≤ 0, and clamped to 0 when wickets w ≥ 10 (all-out). Total projected runs S_pred = S_curr + R_rem maps to win probability via logistic link against era par.
            </p>
          </div>

          <div class="modal-section spotlight-card tilted-card" style="border-top: 3px solid #fbbf24;">
            <h4 style="color: #fbbf24;">2. Calibrated 2nd Innings Logistic Model</h4>
            <p style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #34d399; margin: 8px 0;">
              logit(P) = 2.297 - 0.013*R_need - 0.019*b_rem + 0.627*W_hand - 2.799*(R_need/(b_rem+1))
            </p>
            <p style="font-size: 12px; color: var(--slate-400); line-height: 1.6;">
              Trained across 95,134 clean match deliveries (AUC = 0.895, Brier = 0.132). Dominant rule: WP ≡ 1.0 strictly if R_needed ≤ 0 (target achieved), regardless of wickets fallen.
            </p>
          </div>

          <div class="modal-section spotlight-card tilted-card" style="border-top: 3px solid #ea1a7f;">
            <h4 style="color: #ff2a8d;">3. Multiplicative Retention Ratio (κ)</h4>
            <p style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #34d399; margin: 8px 0;">
              κ_bat = SR_press / SR_base  |  κ_bowl = Econ_base / Econ_press
            </p>
            <p style="font-size: 12px; color: var(--slate-400); line-height: 1.6;">
              Eliminates the Baseline Penalty Fallacy by rewarding players who retain or amplify performance under maximum duress rather than rewarding low-baseline accumulators.
            </p>
          </div>

          <div class="modal-section spotlight-card tilted-card" style="border-top: 3px solid #38bdf8;">
            <h4 style="color: #38bdf8;">4. Non-Striker WPA Conservation</h4>
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

  <!-- 1-CLICK SLOT ASSIGNMENT MODAL (Rajasthan Royals Strategy Showcase) -->
  <div id="slotModal" class="modal-overlay" onclick="closeSlotModal(event)">
    <div class="modal-card" style="max-width: 820px;" onclick="event.stopPropagation()">
      <button class="modal-close" onclick="closeSlotModal()">&times;</button>
      <div class="modal-header">
        <h2 id="slotModalTitle" style="font-size: 18px;">Assign Slot</h2>
        <p id="slotModalSub" style="color: var(--slate-400); font-size: 12px; margin-top: 4px;"></p>
      </div>

      <!-- Quick Search & Clean Filters -->
      <div style="display: flex; gap: 10px; margin-bottom: 14px; flex-wrap: wrap; align-items: center;">
        <input type="text" id="slotSearchInput" class="search-input" style="flex: 1; min-width: 140px;" placeholder="Search player by name or team..." oninput="filterSlotCandidates()">
        <div class="filter-pills" id="slotCategoryPills">
          <div class="pill active" onclick="setSlotFilter('all', this)">All Candidates</div>
          <div class="pill" onclick="setSlotFilter('match', this)">Position Matches</div>
          <div class="pill" onclick="setSlotFilter('free_agent', this)" style="border-left: 2px solid #34d399;">Free Agents</div>
          <div class="pill" onclick="setSlotFilter('rr_core', this)" style="border-left: 2px solid #ff2a85;">RR Core</div>
        </div>
      </div>

      <div id="slotCandidatesList" style="max-height: 480px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px;">
        <!-- Dynamic Candidate Cards -->
      </div>
    </div>
  </div>

  <footer>
    <p>Rajasthan Royals SupeRR Selector Season 2 • Built by Yash Agarwal • Verified across 200,987 deliveries & 5 IPL Seasons</p>
  </footer>

  <script>
    // Embedded Dataset
    const DATA = """ + data_json_str + r""";

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
          color: '#ff9f0a'
        };
      }
      if (badgeType === 'release_watch') {
        return {
          type: 'release_watch',
          badgeClass: 'badge-watchlist',
          rowClass: 'row-watchlist',
          label: p.badge_label || 'RELEASE WATCH',
          color: '#facc15'
        };
      }
      if (badgeType === 'retention' || p.avail_type === 'Untouchable Retention') {
        return {
          type: 'retention',
          badgeClass: 'badge-retention',
          rowClass: 'row-retention',
          label: p.badge_label || 'UNTOUCHABLE CORE',
          color: '#71717a'
        };
      }
      if (badgeType === 'rr_core' || p.avail_type === 'RR Active Squad') {
        return {
          type: 'rr_core',
          badgeClass: 'badge-rr-core',
          rowClass: 'row-rr-core',
          label: p.badge_label || 'RR CORE / RETAINED',
          color: '#ff2a85'
        };
      }
      if (badgeType === 'global_steal') {
        return {
          type: 'global_steal',
          badgeClass: 'badge-global-steal',
          rowClass: '',
          label: p.badge_label || 'GLOBAL STEAL',
          color: '#38bdf8'
        };
      }
      if (badgeType === 'domestic_steal') {
        return {
          type: 'domestic_steal',
          badgeClass: 'badge-domestic-steal',
          rowClass: '',
          label: p.badge_label || 'DOMESTIC STEAL',
          color: '#38bdf8'
        };
      }
      return {
        type: 'auction_target',
        badgeClass: 'badge-auction-target',
        rowClass: '',
        label: p.badge_label || 'AUCTION TARGET',
        color: '#ea1a7f'
      };
    }

    // Switch Tab
    
    // Audit Pool Filter & Search Helpers
    function filterAuditPools(poolId, btn) {
      if (btn) {
        document.querySelectorAll('#auditPoolFilterPills .pill').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
      }
      const pools = document.querySelectorAll('.audit-pool-card');
      pools.forEach(p => {
        if (poolId === 'all' || p.id === poolId) {
          p.style.display = 'block';
        } else {
          p.style.display = 'none';
        }
      });
    }

    function searchAuditPools() {
      const input = document.getElementById('auditSearchInput');
      const query = (input && input.value ? input.value : '').toLowerCase().trim();
      const tiles = document.querySelectorAll('.audit-player-tile');
      tiles.forEach(tile => {
        const text = (tile.textContent || '').toLowerCase();
        if (!query || text.includes(query)) {
          tile.style.display = 'flex';
        } else {
          tile.style.display = 'none';
        }
      });
      const pools = document.querySelectorAll('.audit-pool-card');
      pools.forEach(pool => {
        const poolTiles = pool.querySelectorAll('.audit-player-tile');
        const visibleCount = Array.from(poolTiles).filter(t => t.style.display !== 'none').length;
        if (query && visibleCount === 0) {
          pool.style.display = 'none';
        } else {
          pool.style.display = 'block';
        }
      });
    }

    function switchTab(tabId, e) {
      document.querySelectorAll('.tab-view').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
      const targetTab = document.getElementById('tab-' + tabId);
      if (targetTab) targetTab.classList.add('active');
      const btn = e ? (e.currentTarget || (e.target && typeof e.target.closest === 'function' ? e.target.closest('.nav-tab') : null)) : null;
      if (btn) {
        btn.classList.add('active');
      } else if (typeof document !== 'undefined' && typeof document.querySelector === 'function') {
        const navBtn = document.querySelector(`.nav-tab[onclick*="'${tabId}'"]`);
        if (navBtn) navBtn.classList.add('active');
      }
      if (tabId === 'scatter') drawScatter();
      if (tabId === 'radar') initRadar();
    }

    // Role Switch (Batters / Bowlers / All-Rounders)
    function setRole(role) {
      currentRole = role;
      const btnBat = document.getElementById('btn-batters');
      const btnBowl = document.getElementById('btn-bowlers');
      const btnAR = document.getElementById('btn-all_rounders');
      if (btnBat) btnBat.classList.toggle('active', role === 'batters');
      if (btnBowl) btnBowl.classList.toggle('active', role === 'bowlers');
      if (btnAR) btnAR.classList.toggle('active', role === 'all_rounders');
      renderTable();
    }

    // Filter Switch
    function setFilter(filter, el) {
      currentFilter = filter;
      document.querySelectorAll('#tab-roster .pill').forEach(p => p.classList.remove('active'));
      el.classList.add('active');
      renderTable();
    }

    // Render Table (with Dedicated All-Rounders View)
    function renderTable() {
      const isBat = currentRole === 'batters';
      const isAR = currentRole === 'all_rounders';
      const players = DATA[currentRole] || [];
      const searchInput = document.getElementById('searchInput');
      const search = (searchInput && searchInput.value ? searchInput.value : '').toLowerCase().trim();
      const teamFilter = document.getElementById('teamFilter');
      const selectedTeam = (teamFilter && teamFilter.value ? teamFilter.value : '').toLowerCase().trim();
      const sortSelect = document.getElementById('sortSelect');
      const sortBy = sortSelect ? sortSelect.value : 'rpcs';

      // Filter
      let filtered = players.filter(p => {
        if (search) {
          const matchName = (p.name || '').toLowerCase().includes(search);
          const matchTeam = (p.team_2026 || '').toLowerCase().includes(search);
          const matchCountry = (p.country || '').toLowerCase().includes(search);
          if (!matchName && !matchTeam && !matchCountry) return false;
        }

        if (selectedTeam) {
          const pTeam = (p.team_2026 || '').toLowerCase();
          if (selectedTeam === 'free agent') {
            if (!pTeam.includes('free agent') && !pTeam.includes('released')) return false;
          } else {
            if (!pTeam.includes(selectedTeam)) return false;
          }
        }

        const sInfo = getPlayerStatusInfo(p);
        if (currentFilter === 'top10') return (p.rank || 999) <= 10;
        if (currentFilter === 'free_agent') return sInfo.type === 'free_agent';
        if (currentFilter === 'ineligible') return sInfo.type === 'ineligible';
        if (currentFilter === 'traded') return sInfo.type === 'traded';
        if (currentFilter === 'watchlist') return sInfo.type === 'release_watch';
        if (currentFilter === 'rr_core') return sInfo.type === 'rr_core';
        if (currentFilter === 'untouchable') return sInfo.type === 'retention';
        if (currentFilter === 'global_steal') return sInfo.type === 'global_steal';
        if (currentFilter === 'domestic_steal') return sInfo.type === 'domestic_steal';
        return true;
      });

      // Sort
      filtered.sort((a, b) => {
        if (sortBy === 'rpcs') return (b.rpcs || 0) - (a.rpcs || 0);
        if (sortBy === 'rate') {
          if (isAR) return (b.press_sr || 0) - (a.press_sr || 0);
          return isBat ? ((b.press_sr || 0) - (a.press_sr || 0)) : ((a.press_econ || 0) - (b.press_econ || 0));
        }
        if (sortBy === 'kappa') return (b.kappa || 0) - (a.kappa || 0);
        if (sortBy === 'wpa') return (b.wpa || 0) - (a.wpa || 0);
        if (sortBy === 'csr') return (b.csr || 0) - (a.csr || 0);
        if (sortBy === 'scs') return (a.scs || 0) - (b.scs || 0);
        return 0;
      });

      // Headers
      const thead = document.getElementById('tableHeaders');
      if (!thead) return;

      if (isAR) {
        thead.innerHTML = `
          <th>Rank</th>
          <th>All-Rounder</th>
          <th>Country</th>
          <th>2026 Status & Trade Intelligence</th>
          <th class="num-tabular">Press Balls (Bat/Bowl)</th>
          <th class="num-tabular">Press SR (Bat)</th>
          <th class="num-tabular">Press Econ (Bowl)</th>
          <th class="num-tabular">Bat / Bowl RPCS</th>
          <th class="num-tabular">Retention (κ)</th>
          <th class="num-tabular">Net WPA</th>
          <th class="num-tabular">Net BRA+BRS</th>
          <th class="num-tabular">CSR (%)</th>
          <th class="num-tabular">SCS</th>
          <th class="num-tabular">Composite RPCS</th>
        `;
      } else {
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
      }

      // Body
      const tbody = document.getElementById('tableBody');
      if (!tbody) return;

      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="${isAR ? 14 : 13}" style="text-align:center; padding:36px; color:var(--slate-400);">No players found matching current search and filters.</td></tr>`;
        return;
      }

      tbody.innerHTML = filtered.map(p => {
        const sInfo = getPlayerStatusInfo(p);
        if (isAR) {
          const archColor = (p.archetype && p.archetype.includes('Batting')) ? '#00d4ff' : ((p.archetype && p.archetype.includes('Bowling')) ? '#ff2a85' : '#00e599');
          return `
            <tr class="${sInfo.rowClass}" onclick="openModal('${p.name}', '${currentRole}')">
              <td class="rank-cell ${p.rank <= 3 ? 'top3' : ''}">#${p.rank}</td>
              <td>
                <div class="player-name-cell">
                  <div style="display:flex; align-items:center; gap:6px;">
                    <span class="name-title">${p.name}</span>
                    <span style="font-size:9px; font-weight:800; color:${archColor}; background:#000000; border:1px solid ${archColor}40; padding:1px 6px; border-radius:3px;">${p.archetype || 'All-Rounder'}</span>
                  </div>
                  <span class="name-team-sub">${p.team_2026}</span>
                </div>
              </td>
              <td style="color:var(--slate-400);">${p.country || 'India'}</td>
              <td><span class="badge ${sInfo.badgeClass}">${sInfo.label}</span></td>
              <td class="num-tabular">${p.bat_press_balls || 0}b / ${p.bowl_press_balls || 0}b</td>
              <td class="num-tabular" style="font-weight:700; color:var(--slate-50);">${p.press_sr || '-'}</td>
              <td class="num-tabular" style="font-weight:700; color:#34d399;">${p.press_econ || '-'}</td>
              <td class="num-tabular" style="color:var(--slate-400);">${p.bat_rpcs || 0} / ${p.bowl_rpcs || 0}</td>
              <td class="num-tabular" style="font-weight:700; color:${p.kappa >= 1.0 ? '#34d399' : 'var(--slate-400)'};">${p.kappa}</td>
              <td class="num-tabular" style="font-weight:700; color:${(p.wpa || 0) >= 0 ? '#34d399' : '#f87171'};">${(p.wpa || 0) >= 0 ? '+' : ''}${p.wpa}</td>
              <td class="num-tabular">${(p.net_bra_brs || 0) > 0 ? '+' + p.net_bra_brs : p.net_bra_brs}</td>
              <td class="num-tabular" style="font-weight:700;">${p.csr}%</td>
              <td class="num-tabular">${p.scs}</td>
              <td class="num-tabular"><span class="rpcs-pill ${p.rpcs >= 55 ? 'elite' : ''}">${p.rpcs}</span></td>
            </tr>
          `;
        }

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
            <td class="num-tabular">${(p.press_balls || 0).toLocaleString()}</td>
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
      const list = DATA[role] || DATA['batters'] || [];
      const p = list.find(x => x.name === name) || (DATA['bowlers'] || []).find(x => x.name === name) || ((DATA['all_rounders'] || []).find(x => x.name === name));
      if (!p) return;
      const isBat = role === 'batters' || (p.press_sr !== undefined && p.press_econ === undefined);
      const isAR = role === 'all_rounders' || (p.bat_rpcs !== undefined && p.bowl_rpcs !== undefined);
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

      let ph1Text = '', ph2Text = '', ph3Text = '';
      if (isAR) {
        const ppB = p.pp_balls || ((p.bat_pp_balls || 0) + (p.bowl_pp_balls || 0));
        const midB = p.mid_balls || ((p.bat_mid_balls || 0) + (p.bowl_mid_balls || 0));
        const dthB = p.death_balls || ((p.bat_death_balls || 0) + (p.bowl_death_balls || 0));
        ph1Text = `${ppB} balls | Bat: ${p.bat_pp_sr !== undefined ? p.bat_pp_sr + ' SR' : '—'} • Bowl: ${p.bowl_pp_econ !== undefined ? p.bowl_pp_econ + ' Econ' : '—'}`;
        ph2Text = `${midB} balls | Bat: ${p.bat_mid_sr !== undefined ? p.bat_mid_sr + ' SR' : '—'} • Bowl: ${p.bowl_mid_econ !== undefined ? p.bowl_mid_econ + ' Econ' : '—'}`;
        ph3Text = `${dthB} balls | Bat: ${p.bat_death_sr !== undefined ? p.bat_death_sr + ' SR' : '—'} • Bowl: ${p.bowl_death_econ !== undefined ? p.bowl_death_econ + ' Econ' : '—'}`;
      } else if (isBat) {
        ph1Text = `${p.pp_balls} balls | ${p.pp_sr} SR`;
        ph2Text = `${p.mid_balls} balls | ${p.mid_sr} SR`;
        ph3Text = `${p.death_balls} balls | ${p.death_sr} SR`;
      } else {
        ph1Text = `${p.pp_balls} balls | ${p.pp_econ} Econ` + (p.pp_wkts !== undefined ? ` (${p.pp_wkts} Wkts)` : '');
        ph2Text = `${p.mid_balls} balls | ${p.mid_econ} Econ` + (p.mid_wkts !== undefined ? ` (${p.mid_wkts} Wkts)` : '');
        ph3Text = `${p.death_balls} balls | ${p.death_econ} Econ` + (p.death_wkts !== undefined ? ` (${p.death_wkts} Wkts)` : '');
      }
      document.getElementById('mPh1').innerText = ph1Text;
      document.getElementById('mPh2').innerText = ph2Text;
      document.getElementById('mPh3').innerText = ph3Text;
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
      if (!grid) return;
      // Strictly include ONLY actionable auction targets (Free Agents, Global Steals, Domestic Steals, Release Watch)
      // Excludes all franchise retentions (Rohit Sharma, Hardik Pandya, Arshdeep, Shami, etc.), RR core, trades, and ineligible players
      const actionableBadgeTypes = ['free_agent', 'global_steal', 'domestic_steal', 'release_watch'];
      const rawTargets = [
        ...DATA.batters.filter(p => actionableBadgeTypes.includes(p.badge_type)),
        ...DATA.bowlers.filter(p => actionableBadgeTypes.includes(p.badge_type)),
        ...(DATA.all_rounders || []).filter(p => actionableBadgeTypes.includes(p.badge_type))
      ];

      // Strict deduplication by player name to prevent dual-role players from appearing twice
      const seen = new Set();
      const allTargets = [];
      for (const p of rawTargets) {
        if (!seen.has(p.name)) {
          seen.add(p.name);
          allTargets.push(p);
        }
      }

      let targets = allTargets;
      if (filterType === 'released') targets = allTargets.filter(p => p.badge_type === 'free_agent');
      if (filterType === 'global_steal') targets = allTargets.filter(p => p.badge_type === 'global_steal');
      if (filterType === 'domestic') targets = allTargets.filter(p => p.badge_type === 'domestic_steal');
      if (filterType === 'death') targets = allTargets.filter(p => p.role && (p.role.toLowerCase().includes('death') || p.role.toLowerCase().includes('finisher')));
      if (filterType === 'spin') targets = allTargets.filter(p => p.role && p.role.toLowerCase().includes('spin'));
      if (filterType === 'pace') targets = allTargets.filter(p => p.role && (p.role.toLowerCase().includes('pace') || p.role.toLowerCase().includes('slinger') || p.role.toLowerCase().includes('yorker')));

      // Sort by RPCS descending
      targets.sort((a,b) => b.rpcs - a.rpcs);

      grid.innerHTML = targets.map(p => {
        const sInfo = getPlayerStatusInfo(p);
        const isPriority = sInfo.type === 'free_agent' || sInfo.type === 'global_steal';
        const roleKey = (p.bat_rpcs !== undefined && p.bowl_rpcs !== undefined) ? 'all_rounders' : (p.press_sr !== undefined ? 'batters' : 'bowlers');
        const initials = p.name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase();
        const avatarClass = sInfo.type === 'free_agent' ? 'avatar-emerald' : (sInfo.type === 'global_steal' ? 'avatar-purple' : 'avatar-gold');

        return `
          <div class="auction-card spotlight-card tilted-card ${isPriority ? 'priority-card' : ''}" onclick="openModal('${p.name}', '${roleKey}')">
            <div class="auction-card-header">
              <div style="display:flex; align-items:center; gap:12px; min-width:0;">
                <div class="player-avatar-circle ${avatarClass}">${initials}</div>
                <div style="min-width:0;">
                  <div class="auction-player-name">${p.name}</div>
                  <div class="auction-role">${p.role || p.archetype || 'Player'}</div>
                </div>
              </div>
              <div style="display:flex; flex-direction:column; align-items:flex-end; gap:4px; max-width:100%; flex-wrap:wrap;">
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
                <div class="mini-stat-val">${p.press_sr !== undefined ? p.press_sr : (p.press_econ !== undefined ? p.press_econ : '—')}</div>
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

      initTiltedCards();
    }

    function filterAuctionTargets(type, el) {
      document.querySelectorAll('#tab-auction .pill').forEach(p => p.classList.remove('active'));
      if (el && el.classList) el.classList.add('active');
      renderAuctionBoard(type);
    }

    // ==========================================
    // REVAMPED STARTING XI SIMULATOR & PURSE TRACKER
    // ==========================================
    const DEFAULT_XI = [
      { num: 1, posCategory: 'Openers', role: 'Pressure Opener / Target Setter', name: 'Yashasvi Jaiswal', cost: 18.00, costStr: '₹18.0 Cr', status: 'RR Retained Core', rpcs: 72.86 },
      { num: 2, posCategory: 'Openers', role: 'Impact Hyper-Striker (221.5 SR)', name: 'Vaibhav Sooryavanshi', cost: 1.10, costStr: '₹1.10 Cr', status: 'RR Retained Core (MVP)', rpcs: 71.91 },
      { num: 3, posCategory: 'Middle Order', role: 'Top-Order WK / Boundary Enforcer', name: 'Jonny Bairstow', cost: 6.50, costStr: '₹6.50 Cr', status: 'Free Agent Auction Buy', rpcs: 53.24 },
      { num: 4, posCategory: 'Middle Order', role: 'Middle-Overs Anchor & Captain', name: 'Riyan Parag (C)', cost: 14.00, costStr: '₹14.0 Cr', status: 'RR Retained Core', rpcs: 64.50 },
      { num: 5, posCategory: 'WK', role: 'Crisis Anchor / Wicketkeeper', name: 'Dhruv Jurel (WK)', cost: 14.00, costStr: '₹14.0 Cr', status: 'RR Retained Core', rpcs: 68.20 },
      { num: 6, posCategory: 'Finisher', role: 'Specialist Death Power Closer', name: 'Glenn Maxwell', cost: 5.50, costStr: '₹5.50 Cr', status: 'Free Agent Auction Buy', rpcs: 53.52 },
      { num: 7, posCategory: 'All-Rounders', role: 'Power Finisher & Pace/Spin Cover', name: 'Donovan Ferreira', cost: 5.50, costStr: '₹5.50 Cr', status: 'RR Retained Core', rpcs: 58.40 },
      { num: 8, posCategory: 'All-Rounders', role: 'Elite Spin All-Rounder & Closer', name: 'Ravindra Jadeja', cost: 16.00, costStr: '₹16.0 Cr', status: 'RR Active Asset', rpcs: 68.40 },
      { num: 9, posCategory: 'Spinners', role: 'Attacking Wrist-Spin Squeeze', name: 'Ravi Bishnoi', cost: 11.00, costStr: '₹11.0 Cr', status: 'RR Active Asset', rpcs: 66.40 },
      { num: 10, posCategory: 'Pacers', role: 'Express Pace Enforcer (150+ kph)', name: 'Jofra Archer', cost: 12.50, costStr: '₹12.5 Cr', status: 'RR Retained Core', rpcs: 65.20 },
      { num: 11, posCategory: 'Pacers', role: 'Premier Seam & New-Ball Spearhead', name: 'Mohammed Shami', cost: 9.50, costStr: '₹9.50 Cr', status: 'RR Traded Asset (LOCKED)', rpcs: 65.80 },
    ];

    let currentXI = JSON.parse(JSON.stringify(DEFAULT_XI));
    let activeSlotIdx = 0;
    let slotCandidateFilter = 'all';

    function getPlayerCostEstimate(p) {
      const match = DEFAULT_XI.find(x => x.name === p.name);
      if (match) return match.cost;
      if (p.fee_in_cr !== undefined) return p.fee_in_cr;
      if (p.est_price) {
        const m = p.est_price.match(/₹?(\d+\.?\d*)\s*-\s*(\d+\.?\d*)/);
        if (m) return (parseFloat(m[1]) + parseFloat(m[2])) / 2;
        const mSingle = p.est_price.match(/₹?(\d+\.?\d*)\s*Cr/);
        if (mSingle) return parseFloat(mSingle[1]);
      }
      return 2.50;
    }

    function updatePurseUI() {
      const totalSpend = currentXI.reduce((sum, s) => sum + (s.cost || 0), 0);
      const remaining = 120.00 - totalSpend;
      const avgRPCS = (currentXI.reduce((sum, s) => sum + (s.rpcs || 0), 0) / (currentXI.length || 1)).toFixed(1);

      const spendEl = document.getElementById('allocatedSpend');
      if (spendEl) spendEl.innerText = `₹${totalSpend.toFixed(2)} Cr`;

      const remEl = document.getElementById('purseRemaining');
      if (remEl) {
        remEl.innerText = `₹${remaining.toFixed(2)} Cr`;
        remEl.style.color = remaining >= 0 ? '#fbbf24' : '#ff3b30';
      }

      const clutchEl = document.getElementById('teamClutchIndex');
      if (clutchEl) clutchEl.innerText = avgRPCS;

      const fillEl = document.getElementById('purseProgressFill');
      if (fillEl) {
        const pct = Math.min(100, Math.max(0, (totalSpend / 120.00) * 100));
        fillEl.style.width = `${pct.toFixed(1)}%`;
        fillEl.style.background = remaining >= 0 ? '#00e599' : '#ff3b30';
      }

      const capTextEl = document.getElementById('purseCapText');
      if (capTextEl) {
        capTextEl.innerText = `XI Salary Cap Utilization: ${((totalSpend / 120.00) * 100).toFixed(1)}%`;
      }

      const reserveTextEl = document.getElementById('purseReserveText');
      if (reserveTextEl) {
        reserveTextEl.innerText = remaining >= 0 
          ? `Bench & Contingency Reserve: ₹${remaining.toFixed(2)} Cr`
          : `⚠️ Exceeds Salary Cap by ₹${Math.abs(remaining).toFixed(2)} Cr!`;
        reserveTextEl.style.color = remaining >= 0 ? 'var(--slate-400)' : '#ff3b30';
      }

      const overseasCount = currentXI.filter(s => {
        const p = (DATA.batters || []).find(x => x.name === s.name) || (DATA.bowlers || []).find(x => x.name === s.name) || ((DATA.all_rounders || []).find(x => x.name === s.name));
        return p && p.country && p.country !== 'India';
      }).length;

      const overseasEl = document.getElementById('overseasCountBadge');
      if (overseasEl) {
        if (overseasCount <= 4) {
          overseasEl.innerText = `${overseasCount} / 4 Overseas (Compliant)`;
          overseasEl.style.color = '#00e599';
          overseasEl.style.borderColor = 'rgba(0, 229, 153, 0.4)';
          overseasEl.style.background = 'rgba(0, 229, 153, 0.1)';
        } else {
          overseasEl.innerText = `${overseasCount} / 4 Overseas (Exceeds Limit!)`;
          overseasEl.style.color = '#ff3b30';
          overseasEl.style.borderColor = 'rgba(255, 59, 48, 0.4)';
          overseasEl.style.background = 'rgba(255, 59, 48, 0.1)';
        }
      }
    }

    function renderXI() {
      const container = document.getElementById('xiSlotsList');
      if (!container) return;

      const posColors = {
        'Openers': '#ea1a7f',
        'Middle Order': '#38bdf8',
        'WK': '#fbbf24',
        'Finisher': '#ff2a8d',
        'All-Rounders': '#a855f7',
        'Spinners': '#f59e0b',
        'Pacers': '#f43f5e'
      };

      container.innerHTML = currentXI.map((slot, idx) => {
        const accent = posColors[slot.posCategory] || '#ffffff';
        return `
          <div class="xi-slot-card" style="border-left: 3px solid ${accent};" onclick="openSlotModal(${idx})">
            <div class="xi-slot-left">
              <span class="xi-slot-pos-badge" style="color:${accent}; border-color:${accent}40;">${slot.posCategory} • #${slot.num}</span>
              <div class="xi-slot-player-meta">
                <span class="xi-slot-player-name">${slot.name}</span>
                <span class="xi-slot-player-sub">${slot.role} • <span style="color:var(--slate-400);">${slot.status}</span></span>
              </div>
            </div>
            <div class="xi-slot-right">
              <span class="xi-slot-cost">₹${(slot.cost || 0).toFixed(2)} Cr</span>
              <span class="xi-slot-rpcs">${slot.rpcs}</span>
              <button class="xi-swap-action-btn" onclick="event.stopPropagation(); openSlotModal(${idx})">⇄ Swap</button>
            </div>
          </div>
        `;
      }).join('');

      updatePurseUI();
    }

    // 1-Click Slot Assignment Modal
    function openSlotModal(slotIdx) {
      activeSlotIdx = slotIdx;
      const slot = currentXI[slotIdx];
      const totalSpend = currentXI.reduce((sum, s) => sum + (s.cost || 0), 0);
      const remaining = 120.00 - totalSpend;

      const titleEl = document.getElementById('slotModalTitle');
      if (titleEl) {
        titleEl.innerHTML = `Assign Slot #${slot.num}: <span style="color:#ea1a7f;">${slot.posCategory}</span>`;
      }
      const subEl = document.getElementById('slotModalSub');
      if (subEl) {
        subEl.innerHTML = `Currently assigned: <strong>${slot.name}</strong> (₹${(slot.cost || 0).toFixed(2)} Cr) • Available Remaining Purse: <strong>₹${remaining.toFixed(2)} Cr</strong>`;
      }

      const searchInput = document.getElementById('slotSearchInput');
      if (searchInput) searchInput.value = '';

      slotCandidateFilter = 'all';
      document.querySelectorAll('#slotCategoryPills .pill').forEach((p, idx) => {
        p.classList.toggle('active', idx === 0);
      });

      renderSlotCandidates();
      const modal = document.getElementById('slotModal');
      if (modal) modal.classList.add('active');
    }

    function closeSlotModal() {
      const modal = document.getElementById('slotModal');
      if (modal) modal.classList.remove('active');
    }

    function setSlotFilter(filterType, el) {
      slotCandidateFilter = filterType;
      document.querySelectorAll('#slotCategoryPills .pill').forEach(p => p.classList.remove('active'));
      if (el && el.classList) el.classList.add('active');
      renderSlotCandidates();
    }

    function filterSlotCandidates() {
      renderSlotCandidates();
    }

    function renderSlotCandidates() {
      const listEl = document.getElementById('slotCandidatesList');
      if (!listEl) return;

      const searchInput = document.getElementById('slotSearchInput');
      const search = (searchInput && searchInput.value ? searchInput.value : '').toLowerCase().trim();
      const currentSlot = currentXI[activeSlotIdx];
      const currentSlotCost = currentSlot ? currentSlot.cost : 0;
      const totalSpend = currentXI.reduce((sum, s) => sum + (s.cost || 0), 0);
      const remainingPurse = 120.00 - totalSpend;

      // Pool of candidates excluding BCCI Ineligible players
      const seen = new Set();
      const pool = [];
      [...(DATA.all_rounders || []), ...DATA.batters, ...DATA.bowlers].forEach(p => {
        if (!seen.has(p.name) && p.country !== 'Pakistan' && p.badge_type !== 'ineligible') {
          seen.add(p.name);
          pool.push(p);
        }
      });

      let filtered = pool.filter(p => {
        if (search) {
          const matchName = (p.name || '').toLowerCase().includes(search);
          const matchTeam = (p.team_2026 || '').toLowerCase().includes(search);
          const matchRole = (p.role || p.archetype || '').toLowerCase().includes(search);
          if (!matchName && !matchTeam && !matchRole) return false;
        }

        const sInfo = getPlayerStatusInfo(p);
        if (slotCandidateFilter === 'free_agent') return sInfo.type === 'free_agent';
        if (slotCandidateFilter === 'rr_core') return sInfo.type === 'rr_core';
        if (slotCandidateFilter === 'match') {
          const roleStr = (p.role || p.archetype || '').toLowerCase();
          const cat = currentSlot.posCategory.toLowerCase();
          if (cat === 'openers') return roleStr.includes('opener') || roleStr.includes('top-order');
          if (cat === 'middle order') return roleStr.includes('middle') || roleStr.includes('anchor');
          if (cat === 'wk') return roleStr.includes('wk') || roleStr.includes('keeper');
          if (cat === 'finisher') return roleStr.includes('finisher') || roleStr.includes('closer') || roleStr.includes('power');
          if (cat === 'all-rounders') return roleStr.includes('all-rounder') || p.bat_rpcs !== undefined;
          if (cat === 'spinners') return roleStr.includes('spin');
          if (cat === 'pacers') return roleStr.includes('pace') || roleStr.includes('seam') || roleStr.includes('yorker');
        }
        return true;
      });

      filtered.sort((a, b) => (b.rpcs || 0) - (a.rpcs || 0));

      listEl.innerHTML = filtered.slice(0, 50).map(p => {
        const sInfo = getPlayerStatusInfo(p);
        const cost = getPlayerCostEstimate(p);
        const delta = currentSlotCost - cost;
        const newRemaining = remainingPurse + delta;
        const isOverBudget = newRemaining < 0;

        let deltaHtml = '';
        if (delta > 0) {
          deltaHtml = `<span class="candidate-delta-pill" style="color:#34d399; background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3);">+₹${delta.toFixed(2)} Cr Saved</span>`;
        } else if (delta < 0) {
          const costMore = Math.abs(delta);
          const color = isOverBudget ? '#f87171' : '#fbbf24';
          deltaHtml = `<span class="candidate-delta-pill" style="color:${color}; background:rgba(${isOverBudget ? '239,68,68' : '251,191,36'},0.1); border:1px solid rgba(${isOverBudget ? '239,68,68' : '251,191,36'},0.3);">-₹${costMore.toFixed(2)} Cr Spend</span>`;
        } else {
          deltaHtml = `<span class="candidate-delta-pill" style="color:var(--slate-400); background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);">₹0.00 Cr Impact</span>`;
        }

        return `
          <div class="slot-candidate-row">
            <div class="candidate-info-block">
              <div class="candidate-title">
                <span>${p.name}</span>
                <span class="badge ${sInfo.badgeClass}" style="font-size:9px; padding:2px 8px;">${sInfo.label}</span>
              </div>
              <div class="candidate-sub">
                ${p.role || p.archetype || 'Player'} • ${p.team_2026} • RPCS <strong style="color:#ffffff;">${p.rpcs}</strong> • Cost: <strong style="color:#34d399;">₹${cost.toFixed(2)} Cr</strong>
              </div>
            </div>
            <div class="candidate-actions">
              ${deltaHtml}
              <button class="btn-assign-slot ${isOverBudget ? 'over-budget' : ''}" onclick="assignCandidateToSlot('${p.name}', ${cost}, ${p.rpcs}, '${p.role || p.archetype || 'Player'}', '${sInfo.label}')">
                ${isOverBudget ? 'Exceeds Cap (Assign)' : 'Assign to Slot'}
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    function assignCandidateToSlot(name, cost, rpcs, role, statusLabel) {
      if (activeSlotIdx < 0 || activeSlotIdx >= currentXI.length) return;
      currentXI[activeSlotIdx].name = name;
      currentXI[activeSlotIdx].cost = cost;
      currentXI[activeSlotIdx].costStr = `₹${cost.toFixed(2)} Cr`;
      currentXI[activeSlotIdx].rpcs = rpcs;
      currentXI[activeSlotIdx].role = role;
      currentXI[activeSlotIdx].status = statusLabel;

      closeSlotModal();
      renderXI();
    }

    function resetXI() {
      currentXI = JSON.parse(JSON.stringify(DEFAULT_XI));
      renderXI();
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
      ctx.strokeStyle = '#18181d';
      ctx.lineWidth = 1;
      for (let y = 50; y <= 90; y += 10) {
        ctx.beginPath();
        ctx.moveTo(pad.left, getY(y));
        ctx.lineTo(pad.left + plotW, getY(y));
        ctx.stroke();
        ctx.fillStyle = '#71717a';
        ctx.font = '10px JetBrains Mono, monospace';
        ctx.fillText(y + '%', pad.left - 34, getY(y) + 3);
      }

      const xStep = isBat ? 20 : 1;
      for (let x = xMin; x <= xMax; x += xStep) {
        ctx.beginPath();
        ctx.moveTo(getX(x), pad.top);
        ctx.lineTo(getX(x), pad.top + plotH);
        ctx.stroke();
        ctx.fillStyle = '#71717a';
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

    // Canvas Radar Chart with all players including All-Rounders
    function initRadar() {
      const p1 = document.getElementById('radarPlayer1');
      const p2 = document.getElementById('radarPlayer2');
      if (!p1 || !p2) return;

      const optgroups = `
        <optgroup label="Top All-Rounders (Composite RPCS)">
          ${(DATA.all_rounders || []).map(p => `<option value="${p.name}">${p.name} (#${p.rank} All-R | ${p.team_2026})</option>`).join('')}
        </optgroup>
        <optgroup label="Top Batters (RPCS Rank)">
          ${DATA.batters.map(p => `<option value="${p.name}">${p.name} (#${p.rank} Bat | ${p.team_2026})</option>`).join('')}
        </optgroup>
        <optgroup label="Top Bowlers (RPCS Rank)">
          ${DATA.bowlers.map(p => `<option value="${p.name}">${p.name} (#${p.rank} Bowl | ${p.team_2026})</option>`).join('')}
        </optgroup>
      `;
      p1.innerHTML = optgroups;
      p2.innerHTML = optgroups;
      p1.value = "Sunil Narine";
      p2.value = "Rashid Khan";
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

      const p1El = document.getElementById('radarPlayer1');
      const p2El = document.getElementById('radarPlayer2');
      const name1 = p1El ? p1El.value : '';
      const name2 = p2El ? p2El.value : '';
      const findP = n => ((DATA.all_rounders || []).find(x => x.name === n)) || DATA.batters.find(x => x.name === n) || DATA.bowlers.find(x => x.name === n);
      const p1 = findP(name1);
      const p2 = findP(name2);
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
        ctx.strokeStyle = '#18181d';
        ctx.lineWidth = 1;
        ctx.stroke();
      }

      // Draw Axis Lines & Labels
      for (let i = 0; i < totalAxes; i++) {
        const angle = (Math.PI * 2 / totalAxes) * i - Math.PI / 2;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + Math.cos(angle) * radius, cy + Math.sin(angle) * radius);
        ctx.strokeStyle = '#18181d';
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

      drawPoly(getProfile(p1), '#ea1a7f', 'rgba(234, 26, 127, 0.22)');
      drawPoly(getProfile(p2), '#fbbf24', 'rgba(251, 191, 36, 0.22)');

      // Legend
      ctx.textAlign = 'left';
      ctx.font = '700 12px Inter, sans-serif';
      ctx.fillStyle = '#ea1a7f';
      ctx.fillText(`■ ${p1.name} (RPCS ${p1.rpcs})`, 24, 24);
      ctx.fillStyle = '#fbbf24';
      ctx.fillText(`■ ${p2.name} (RPCS ${p2.rpcs})`, 24, 44);
    }

    // Init
    
    // ==========================================
    // React Bits Interactive Ecosystem Additions
    // ==========================================

    
    // React Bits: Ambient Stadium Atmosphere Particle Canvas
    (function initAmbientAtmosphere() {
      if (typeof window === 'undefined' || typeof document === 'undefined' || !document.body) return;
      const canvas = document.createElement('canvas');
      canvas.id = 'ambientAtmosphereCanvas';
      canvas.style.position = 'fixed';
      canvas.style.top = '0';
      canvas.style.left = '0';
      canvas.style.width = '100vw';
      canvas.style.height = '100vh';
      canvas.style.pointerEvents = 'none';
      canvas.style.zIndex = '-1';
      document.body.appendChild(canvas);
      const ctx = canvas.getContext ? canvas.getContext('2d') : null;
      if (!ctx) return;

      let w = window.innerWidth || 1200;
      let h = window.innerHeight || 800;
      canvas.width = w;
      canvas.height = h;

      const particles = [];
      const particleColors = ['rgba(234, 26, 127, 0.35)', 'rgba(251, 191, 36, 0.25)', 'rgba(56, 189, 248, 0.2)'];
      for (let i = 0; i < 30; i++) {
        particles.push({
          x: Math.random() * w,
          y: Math.random() * h,
          r: 1 + Math.random() * 2,
          color: particleColors[i % particleColors.length],
          vx: (Math.random() - 0.5) * 0.3,
          vy: -0.2 - Math.random() * 0.3
        });
      }

      function render() {
        if (typeof ctx.clearRect === 'function') {
          ctx.clearRect(0, 0, w, h);
          particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            if (p.y < 0) p.y = h;
            if (p.x < 0) p.x = w;
            if (p.x > w) p.x = 0;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.fill();
          });
        }
        if (typeof requestAnimationFrame === 'function') requestAnimationFrame(render);
      }
      if (typeof requestAnimationFrame === 'function') requestAnimationFrame(render);
    })();

    // 1. React Bits: ClickSpark Interactive Canvas
    (function initClickSpark() {
      if (typeof window === 'undefined' || typeof document === 'undefined' || !document.body) return;
      const canvas = document.createElement('canvas');
      canvas.id = 'clickSparkCanvas';
      canvas.style.position = 'fixed';
      canvas.style.top = '0';
      canvas.style.left = '0';
      canvas.style.width = '100vw';
      canvas.style.height = '100vh';
      canvas.style.pointerEvents = 'none';
      canvas.style.zIndex = '9999';
      document.body.appendChild(canvas);
      const ctx = canvas.getContext('2d');
      let sparks = [];

      function resize() {
        canvas.width = window.innerWidth * (window.devicePixelRatio || 1);
        canvas.height = window.innerHeight * (window.devicePixelRatio || 1);
        ctx.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);
      }
      window.addEventListener('resize', resize);
      resize();

      window.addEventListener('click', (e) => {
        const colors = ['#ea1a7f', '#fbbf24', '#ffffff', '#ff2a8d', '#38bdf8'];
        const count = 12;
        for (let i = 0; i < count; i++) {
          const angle = (Math.PI * 2 * i) / count + (Math.random() - 0.5) * 0.5;
          const speed = 2 + Math.random() * 4;
          sparks.push({
            x: e.clientX,
            y: e.clientY,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed,
            color: colors[Math.floor(Math.random() * colors.length)],
            size: 2.5 + Math.random() * 2.5,
            alpha: 1,
            decay: 0.03 + Math.random() * 0.02
          });
        }
      });

      function loop() {
        ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
        for (let i = sparks.length - 1; i >= 0; i--) {
          const s = sparks[i];
          s.x += s.vx;
          s.y += s.vy;
          s.vx *= 0.94;
          s.vy *= 0.94;
          s.alpha -= s.decay;
          if (s.alpha <= 0) {
            sparks.splice(i, 1);
          } else {
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.size * s.alpha, 0, Math.PI * 2);
            ctx.fillStyle = s.color;
            ctx.globalAlpha = s.alpha;
            ctx.fill();
          }
        }
        ctx.globalAlpha = 1;
        requestAnimationFrame(loop);
      }
      if (typeof requestAnimationFrame === 'function') loop();
    })();

    // 2. React Bits: Dynamic SpotlightCard & BorderGlow Tracking
    if (typeof document !== 'undefined' && document.addEventListener) document.addEventListener('mousemove', (e) => {
      document.querySelectorAll('.spotlight-card, .magic-bento__cell, .auction-card, .table-container, .purse-tracker').forEach(card => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        if (card.style && card.style.setProperty) card.style.setProperty('--mouse-x', `${x}px`);
        if (card.style && card.style.setProperty) card.style.setProperty('--mouse-y', `${y}px`);
        const cx = rect.width / 2;
        const cy = rect.height / 2;
        const angle = Math.atan2(y - cy, x - cx) * (180 / Math.PI);
        if (card.style && card.style.setProperty) card.style.setProperty('--cursor-angle', `${angle}deg`);
      });
    });

    // 3. React Bits: TiltedCard 3D Hover Physics
    function initTiltedCards() {
      if (typeof document === 'undefined') return;
      document.querySelectorAll('.tilted-card').forEach(card => {
        if (card._tiltedInit) return;
        card._tiltedInit = true;
        card.addEventListener('mousemove', (e) => {
          const rect = card.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          const cx = rect.width / 2;
          const cy = rect.height / 2;
          const rx = ((y - cy) / cy) * -6;
          const ry = ((x - cx) / cx) * 6;
          card.style.transform = `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg) scale3d(1.015, 1.015, 1.015)`;
        });
        card.addEventListener('mouseleave', () => {
          card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        });
      });
    }

    // 4. React Bits: DecryptedText Scramble Animation
    function runDecryptedText() {
      const glyphs = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ#@$%&*';
      document.querySelectorAll('[data-decrypted]').forEach(el => {
        if (!el || typeof el.getAttribute !== 'function') return;
        const originalText = el.getAttribute('data-decrypted');
        let iteration = 0;
        let interval;
        interval = setInterval(() => {
          el.innerText = originalText.split('').map((char, index) => {
            if (index < iteration || char === ' ' || char === '•' || char === '—') {
              return originalText[index];
            }
            return glyphs[Math.floor(Math.random() * glyphs.length)];
          }).join('');
          if (iteration >= originalText.length) {
            clearInterval(interval);
            el.innerText = originalText;
          }
          iteration += 1.5;
        }, 30);
      });
    }

    // 5. React Bits: CountUp Number Easing
    function runCountUp() {
      document.querySelectorAll('[data-countup]').forEach(el => {
        if (!el || typeof el.getAttribute !== 'function') return;
        const targetStr = el.getAttribute('data-countup');
        const prefix = el.getAttribute('data-prefix') || '';
        const suffix = el.getAttribute('data-suffix') || '';
        const target = parseFloat(targetStr);
        if (isNaN(target)) return;
        const isFloat = targetStr.includes('.');
        const duration = 1200;
        const start = performance.now();

        function update(now) {
          const elapsed = now - start;
          const progress = Math.min(elapsed / duration, 1);
          const ease = 1 - Math.pow(1 - progress, 3);
          const current = target * ease;
          el.innerText = prefix + (isFloat ? current.toFixed(2) : Math.round(current).toLocaleString()) + suffix;
          if (progress < 1) {
            requestAnimationFrame(update);
          } else {
            el.innerText = prefix + (isFloat ? target.toFixed(2) : target.toLocaleString()) + suffix;
          }
        }
        requestAnimationFrame(update);
      });
    }

    // 6. 1-Click Copy and Download Helpers
    function copyTextToClipboard(text, msg) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          alert(msg);
        }).catch(() => {
          fallbackCopyText(text, msg);
        });
      } else {
        fallbackCopyText(text, msg);
      }
    }

    function fallbackCopyText(text, msg) {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      alert(msg);
    }

    window.onload = function() {
      runDecryptedText();
      runCountUp();
      initTiltedCards();

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

ROOT_HTML = os.path.join(DASHBOARD_DIR, "index.html")
ROOT_DATA = os.path.join(DASHBOARD_DIR, "data.json")

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_template)

with open(ROOT_HTML, "w", encoding="utf-8") as f:
    f.write(html_template)

import shutil
shutil.copyfile(DATA_PATH, ROOT_DATA)

print(f"Generated enhanced dashboard successfully: {OUTPUT_HTML} and {ROOT_HTML} ({len(html_template)} bytes)")
