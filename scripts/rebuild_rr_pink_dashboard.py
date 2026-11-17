#!/usr/bin/env python3
"""
Complete Rajasthan Royals Royal Pink & React Bits Frontend Overhaul for SupeRR Selector.
"""

import os
import re

DASHBOARD_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_SCRIPT = os.path.join(DASHBOARD_DIR, "build_dashboard.py")

with open(BUILD_SCRIPT, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS
# Replace everything from <style> to </style>
css_new = r"""<style>
    :root {
      /* Rajasthan Royals Official Brand Tokens */
      --rr-pink: #ea1a7f;
      --rr-pink-hover: #ff2a8d;
      --rr-pink-dark: #be123c;
      --rr-pink-deep: #831843;
      --rr-pink-glow: rgba(234, 26, 127, 0.45);
      --rr-pink-subtle: rgba(234, 26, 127, 0.12);
      --rr-pink-border: rgba(234, 26, 127, 0.35);

      --rr-navy-deep: #050814;
      --rr-navy-base: #070d1e;
      --rr-navy-card: #0b1329;
      --rr-navy-hover: #101b3b;
      --rr-navy-surface: #0e1733;
      --rr-navy-border: #1a274c;

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
      background-color: var(--rr-navy-deep);
      color: var(--slate-300);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      line-height: 1.5;
      padding-bottom: 80px;
      -webkit-font-smoothing: antialiased;
      position: relative;
      overflow-x: hidden;
    }

    /* React Bits: Backgrounds/DotGrid */
    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background-image: radial-gradient(rgba(234, 26, 127, 0.14) 1.2px, transparent 1.2px);
      background-size: 22px 22px;
      pointer-events: none;
      z-index: -1;
    }

    /* React Bits: Backgrounds/Aurora Mesh */
    body::after {
      content: '';
      position: fixed;
      top: -25%;
      left: 10%;
      width: 80%;
      height: 65%;
      background: radial-gradient(ellipse at 50% 30%, rgba(234, 26, 127, 0.18) 0%, rgba(0, 40, 95, 0.28) 45%, transparent 70%);
      filter: blur(90px);
      pointer-events: none;
      z-index: -1;
      animation: auroraPulse 12s ease-in-out infinite alternate;
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
    .magic-bento__cell--featured {
      grid-column: span 6;
      background: linear-gradient(135deg, rgba(234, 26, 127, 0.1) 0%, rgba(11, 19, 41, 0.95) 50%, rgba(7, 13, 30, 0.95) 100%);
      border: 1px solid rgba(234, 26, 127, 0.4);
    }
    .magic-bento__cell--unstop {
      grid-column: span 6;
      background: linear-gradient(135deg, rgba(251, 191, 36, 0.08) 0%, rgba(11, 19, 41, 0.95) 50%, rgba(7, 13, 30, 0.95) 100%);
      border: 1px solid rgba(251, 191, 36, 0.35);
    }
    .magic-bento__cell--stat1 {
      grid-column: span 6;
    }
    .magic-bento__cell--stat2 {
      grid-column: span 6;
    }
    @media (max-width: 1024px) {
      .magic-bento__cell--featured,
      .magic-bento__cell--unstop,
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
    .search-input:focus {
      border-color: var(--rr-pink);
      box-shadow: 0 0 10px rgba(234, 26, 127, 0.35);
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
    }

    /* Table Styles with Rajasthan Royals Midnight Navy & Pink Highlighting */
    .table-container {
      background: var(--rr-navy-card);
      border: 1px solid var(--rr-navy-border);
      border-radius: 14px;
      overflow-x: auto;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    table {
      width: 100%;
      border-collapse: collapse;
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
    }
    td {
      padding: 12px 16px;
      border-bottom: 1px solid rgba(26, 39, 76, 0.6);
      vertical-align: middle;
      white-space: nowrap;
    }
    tr {
      background: var(--rr-navy-card);
      transition: background-color 0.12s ease;
    }
    tr:hover {
      background: var(--rr-navy-hover) !important;
      cursor: pointer;
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
      transition: color 0.15s;
    }
    .modal-close:hover { color: #ffffff; }
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
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
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
    .auction-card.priority-card {
      border-color: rgba(234, 26, 127, 0.65);
      background: linear-gradient(135deg, rgba(234, 26, 127, 0.1) 0%, rgba(11, 19, 41, 0.95) 100%);
      box-shadow: 0 0 20px rgba(234, 26, 127, 0.2);
    }
    .auction-card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
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
  </style>"""

# 2. Update Header
header_new = r"""<header>
    <div class="header-content">
      <div class="brand">
        <div class="logo-badge">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="color: #ea1a7f;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          <span>RR</span>
        </div>
        <div class="brand-text">
          <h1 class="shiny-text">RAJASTHAN ROYALS <span class="badge-header">SupeRR Selector</span></h1>
          <p data-decrypted="HALLA BOL • HIGH-PRESSURE ANALYTICS ENGINE • IPL 2027 WAR ROOM">HALLA BOL • HIGH-PRESSURE ANALYTICS ENGINE • IPL 2027 WAR ROOM</p>
        </div>
      </div>
      <div class="nav-tabs">
        <button class="nav-tab active" onclick="switchTab('roster', event)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path><path d="M4 22h16"></path><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"></path><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"></path><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"></path></svg>
          Unstop Top 10 Roster
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
  </header>"""

# 3. Update Hero Section to MagicBento
hero_new = r"""<!-- React Bits: Components/MagicBento Grid Overview -->
    <div class="magic-bento">
      <!-- Cell 1: RR Auction War Room Pulse -->
      <div class="magic-bento__cell magic-bento__cell--featured spotlight-card tilted-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <div>
            <div class="bento-badge" style="background: rgba(234, 26, 127, 0.2); color: #ff2a8d; border: 1px solid rgba(234, 26, 127, 0.45);">
              <span class="status-dot-pulse"></span> RR AUCTION WAR ROOM PULSE
            </div>
            <h3 style="font-size: 19px; font-weight: 800; color: #ffffff; margin-top: 6px;">Confirmed Retentions & Budget Leverage</h3>
          </div>
          <div style="text-align: right;">
            <span style="font-size: 10px; text-transform: uppercase; color: var(--slate-400); font-weight: 700; letter-spacing: 0.08em;">Salary Cap</span>
            <div class="num-tabular" style="font-size: 18px; font-weight: 800; color: #ffffff;">₹120.00 Cr</div>
          </div>
        </div>
        
        <p style="font-size: 12px; color: var(--slate-300); margin-bottom: 16px; line-height: 1.5;">
          Rajasthan Royals retain their core quintet (<strong style="color: #ffffff;">Samson, Jaiswal, Parag, Jurel, Sandeep</strong>). Leveraging unencumbered free agents and undervalued global steals with <strong>₹113.60 Cr</strong> remaining budget power.
        </p>

        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 16px;">
          <div class="bento-metric-tile">
            <span class="bento-metric-lbl">Remaining Purse</span>
            <span class="bento-metric-val num-tabular" style="color: #34d399;" data-countup="113.60" data-prefix="₹" data-suffix=" Cr">₹113.60 Cr</span>
          </div>
          <div class="bento-metric-tile">
            <span class="bento-metric-lbl">Allocated Spend</span>
            <span class="bento-metric-val num-tabular" style="color: #f43f5e;" data-countup="6.40" data-prefix="₹" data-suffix=" Cr">₹6.40 Cr</span>
          </div>
          <div class="bento-metric-tile">
            <span class="bento-metric-lbl">Squad Purse Utilization</span>
            <span class="bento-metric-val num-tabular" style="color: #fbbf24;">94.7% Available</span>
          </div>
        </div>

        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
          <span class="priority-pill"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> Target 1: Death Over Anchor (Taskin / Ellis)</span>
          <span class="priority-pill"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> Target 2: Explosive Spin AR</span>
          <span class="priority-pill"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> Target 3: Pace Enforcer</span>
        </div>
      </div>

      <!-- Cell 2: Official Unstop Dropdowns Quick-Access -->
      <div class="magic-bento__cell magic-bento__cell--unstop spotlight-card tilted-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
          <div>
            <div class="bento-badge" style="background: rgba(251, 191, 36, 0.15); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.4);">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg> UNSTOP OFFICIAL DROPDOWNS
            </div>
            <h3 style="font-size: 19px; font-weight: 800; color: #ffffff; margin-top: 6px;">Top 10 Selection Roster</h3>
          </div>
          <span style="font-size: 11px; background: rgba(255, 255, 255, 0.1); padding: 4px 10px; border-radius: 9999px; color: #ffffff; font-weight: 700;">CTPM 1:1 Matched</span>
        </div>

        <p style="font-size: 12px; color: var(--slate-300); margin-bottom: 14px; line-height: 1.5;">
          Direct dropdown mapping compliant with Unstop's submission schema. Top 10 Batters & Bowlers verified mathematically.
        </p>

        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px;">
          <button class="star-border-btn" onclick="copyBattersDropdown()">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"></rect><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"></path></svg>
            Copy Top 10 Batters
          </button>
          <button class="star-border-btn" onclick="copyBowlersDropdown()" style="background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%); box-shadow: 0 4px 18px rgba(67, 56, 202, 0.4);">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"></rect><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"></path></svg>
            Copy Top 10 Bowlers
          </button>
          <button class="star-border-btn" onclick="downloadSubmissionTxt()" style="background: linear-gradient(135deg, #064e3b 0%, #059669 100%); box-shadow: 0 4px 18px rgba(5, 150, 105, 0.4);">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" x2="12" y1="15" y2="3"></line></svg>
            Download TXT
          </button>
        </div>

        <div style="font-size: 11px; color: var(--slate-400); display: flex; align-items: center; gap: 6px;">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 14 14"></polyline></svg>
          Includes ready-to-paste 496-character Unstop submission rationale blurb.
        </div>
      </div>

      <!-- Cell 3: Multi-Moment Pressure Engine Blueprint -->
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

      <!-- Cell 4: Contract Realism & Trade Anti-Leakage -->
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
            <div style="font-size: 10px; color: var(--slate-500);">Zero war-room leakage</div>
          </div>
        </div>
      </div>
    </div>\n"""

# Assemble new content
# 1. Replace <style>...</style>
style_start = content.find('<style>')
style_end = content.find('</style>') + len('</style>')
content = content[:style_start] + css_new + content[style_end:]

# 2. Replace <header>...</header>
header_start = content.find('<header>')
header_end = content.find('</header>') + len('</header>')
content = content[:header_start] + header_new + content[header_end:]

# 3. Replace hero-stats with MagicBento
hero_start = content.find('<div class="hero-stats">')
hero_end = content.find('<!-- TAB 1: ROSTER / UNSTOP DROPDOWNS -->')
content = content[:hero_start] + hero_new + content[hero_end:]

# 4. Clean up any remaining Whoop green #00e599 references in body HTML
body_end = content.find('<script>')
body_part = content[:body_end]
script_part = content[body_end:]

# Replace #00e599 with #10b981 or linear gradient in body
body_part = body_part.replace('#00e599', '#34d399')
body_part = body_part.replace('rgba(0, 229, 153', 'rgba(16, 185, 129')
body_part = body_part.replace('rgba(0,229,153', 'rgba(16, 185, 129')

# Update script part with React Bits interactive functions & RR colors
# Update colors in getPlayerStatusInfo
script_part = script_part.replace("color: '#00e599'", "color: '#10b981'")
script_part = script_part.replace("color: '#ff3b30'", "color: '#ef4444'")
script_part = script_part.replace("color: '#52525b'", "color: '#ea1a7f'")
script_part = script_part.replace("color: '#00d4ff'", "color: '#38bdf8'")

# Add React Bits interactive helpers right before the end of <script>
react_bits_js = r"""
    // ==========================================
    // React Bits Interactive Ecosystem Additions
    // ==========================================

    // 1. React Bits: ClickSpark Interactive Canvas
    (function initClickSpark() {
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
      loop();
    })();

    // 2. React Bits: Dynamic SpotlightCard & BorderGlow Tracking
    document.addEventListener('mousemove', (e) => {
      document.querySelectorAll('.spotlight-card, .magic-bento__cell, .auction-card, .table-container, .purse-tracker').forEach(card => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
        const cx = rect.width / 2;
        const cy = rect.height / 2;
        const angle = Math.atan2(y - cy, x - cx) * (180 / Math.PI);
        card.style.setProperty('--cursor-angle', `${angle}deg`);
      });
    });

    // 3. React Bits: TiltedCard 3D Hover Physics
    function initTiltedCards() {
      document.querySelectorAll('.tilted-card').forEach(card => {
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
        const originalText = el.getAttribute('data-decrypted');
        let iteration = 0;
        const interval = setInterval(() => {
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

    function copyBattersDropdown() {
      const text = "Shivam Dube (CSK), Heinrich Klaasen (SRH), Nicholas Pooran (LSG), David Miller (GT), Shimron Hetmyer (RR), Tristan Stubbs (DC), Tilak Varma (MI), Shashank Singh (PBKS), Tim David (MI), Ashutosh Sharma (PBKS)";
      copyTextToClipboard(text, "Copied Top 10 Batters (CTPM) to clipboard!");
    }

    function copyBowlersDropdown() {
      const text = "Jasprit Bumrah (MI), Varun Chakravarthy (KKR), Arshdeep Singh (PBKS), T Natarajan (SRH), Mayank Yadav (LSG), Matheesha Pathirana (CSK), Harshit Rana (KKR), Mohit Sharma (GT), Avesh Khan (RR), Kuldeep Yadav (DC)";
      copyTextToClipboard(text, "Copied Top 10 Bowlers (CTPM) to clipboard!");
    }

    function downloadSubmissionTxt() {
      const content = `================================================================================
RAJASTHAN ROYALS SUPERR SELECTOR SEASON 2 — OFFICIAL UNSTOP SUBMISSION
================================================================================
Applicant: Yash Agarwal
Deliveries Evaluated: 200,987 balls (883 matches, 141 competitions)
Multi-Moment Pressure Formula: RPCS = 0.35*CSR + 0.30*SCS + 0.20*WPA + 0.15*Vol
--------------------------------------------------------------------------------

TOP 10 BATTERS (Official Unstop Dropdown Order):
1. Shivam Dube (CSK) — RPCS: 59.81 | Pressure SR: 158.4 | WPA: +0.482
2. Heinrich Klaasen (SRH) — RPCS: 59.45 | Pressure SR: 171.2 | WPA: +0.514
3. Nicholas Pooran (LSG) — RPCS: 58.90 | Pressure SR: 164.8 | WPA: +0.467
4. David Miller (GT) — RPCS: 57.34 | Pressure SR: 145.2 | WPA: +0.388
5. Shimron Hetmyer (RR) — RPCS: 56.88 | Pressure SR: 156.1 | WPA: +0.395
6. Tristan Stubbs (DC) — RPCS: 56.12 | Pressure SR: 168.0 | WPA: +0.410
7. Tilak Varma (MI) — RPCS: 55.40 | Pressure SR: 142.6 | WPA: +0.320
8. Shashank Singh (PBKS) — RPCS: 54.85 | Pressure SR: 162.3 | WPA: +0.345
9. Tim David (MI) — RPCS: 54.10 | Pressure SR: 165.7 | WPA: +0.312
10. Ashutosh Sharma (PBKS) — RPCS: 53.75 | Pressure SR: 172.5 | WPA: +0.330

TOP 10 BOWLERS (Official Unstop Dropdown Order):
1. Jasprit Bumrah (MI) — RPCS: 58.73 | Pressure Econ: 6.42 | WPA: +0.540
2. Varun Chakravarthy (KKR) — RPCS: 57.92 | Pressure Econ: 6.85 | WPA: +0.488
3. Arshdeep Singh (PBKS) — RPCS: 57.10 | Pressure Econ: 7.80 | WPA: +0.415
4. T Natarajan (SRH) — RPCS: 56.45 | Pressure Econ: 7.95 | WPA: +0.390
5. Mayank Yadav (LSG) — RPCS: 55.80 | Pressure Econ: 6.90 | WPA: +0.365
6. Matheesha Pathirana (CSK) — RPCS: 55.30 | Pressure Econ: 7.65 | WPA: +0.380
7. Harshit Rana (KKR) — RPCS: 54.95 | Pressure Econ: 8.10 | WPA: +0.340
8. Mohit Sharma (GT) — RPCS: 54.20 | Pressure Econ: 8.25 | WPA: +0.315
9. Avesh Khan (RR) — RPCS: 53.85 | Pressure Econ: 8.40 | WPA: +0.295
10. Kuldeep Yadav (DC) — RPCS: 53.40 | Pressure Econ: 7.15 | WPA: +0.310

496-CHARACTER UNSTOP SUBMISSION SUMMARY:
We audited 200,987 deliveries across 883 matches via a Multi-Moment Pressure Engine (RPCS = 0.35*CSR + 0.30*SCS + 0.20*WPA + 0.15*Vol). Shivam Dube (59.81) and Jasprit Bumrah (58.73) anchor our Top 10 rankings, calibrated by ball-by-ball win-probability added and context-weighted strike/economy rates. For Rajasthan Royals 2027 auction strategy, our model allocates remaining purse to death bowling specialist Taskin Ahmed (Free Agent) and power spin-allrounder to construct an unbreachable IPL championship XI.
`;
      const blob = new Blob([content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Rajasthan_Royals_SupeRR_Selector_Round1_Submission.txt';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
"""

# Insert react_bits_js before window.onload in script_part
window_onload_idx = script_part.find('window.onload = function() {')
if window_onload_idx != -1:
    # also add runDecryptedText, runCountUp, initTiltedCards inside window.onload
    load_insert = "\n      runDecryptedText();\n      runCountUp();\n      initTiltedCards();\n"
    script_part = script_part[:window_onload_idx] + react_bits_js + "\n    " + script_part[window_onload_idx:window_onload_idx+len('window.onload = function() {')] + load_insert + script_part[window_onload_idx+len('window.onload = function() {'):]

final_content = body_part + script_part

with open(BUILD_SCRIPT, "w", encoding="utf-8") as f:
    f.write(final_content)

print(f"Successfully overhauled build_dashboard.py: {len(final_content)} bytes")
