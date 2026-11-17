import re

with open("build_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Header and Nav Styles with React Bits Colored Header & Dock
old_header_css = """    /* Stealth Athletic Header */
    header {
      background: rgba(0, 0, 0, 0.94);
      border-bottom: 1px solid #16161a;
      padding: 12px 28px;
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(16px);
    }
    .header-content {
      max-width: 1440px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .logo-badge {
      background: #000000;
      color: #ffffff;
      font-weight: 800;
      font-size: 13px;
      padding: 5px 11px;
      border-radius: 6px;
      letter-spacing: 0.1em;
      border: 1px solid #27272a;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .logo-badge::before {
      content: '';
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #ff2a85;
      box-shadow: 0 0 8px #ff2a85;
    }
    .brand-text h1 {
      font-size: 17px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.03em;
    }
    .brand-text h1 span {
      color: #ff2a85;
      font-weight: 700;
    }
    .brand-text p {
      font-size: 11px;
      color: #71717a;
      letter-spacing: 0.02em;
    }

    /* Segmented Navigation Tabs */
    .nav-tabs {
      display: flex;
      gap: 3px;
      flex-wrap: wrap;
      background: #0c0c0e;
      padding: 3px;
      border-radius: 6px;
      border: 1px solid #18181d;
    }
    .nav-tab {
      background: transparent;
      border: none;
      color: #71717a;
      padding: 6px 13px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      cursor: pointer;
      transition: all 0.12s ease;
    }
    .nav-tab:hover {
      color: #ffffff;
      background: #141418;
    }
    .nav-tab.active {
      background: #1c1c22;
      color: #ffffff;
      box-shadow: 0 1px 3px rgba(0,0,0,0.6);
    }"""

new_header_css = """    /* React Bits: Full-Bleed Colored Header with Dot-Grid & Mesh Waves */
    header {
      background: linear-gradient(135deg, #be123c 0%, #e11d48 30%, #9f1239 65%, #1e1b4b 100%);
      background-size: 200% 200%;
      animation: headerMesh 14s ease infinite;
      border-bottom: 1px solid rgba(255, 255, 255, 0.2);
      padding: 14px 28px;
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(20px);
      box-shadow: 0 8px 32px rgba(225, 29, 72, 0.35);
      position: relative;
      overflow: hidden;
    }
    @keyframes headerMesh {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    /* React Bits: Dot Grid Pattern */
    header::before {
      content: '';
      position: absolute;
      inset: 0;
      background-image: radial-gradient(rgba(255, 255, 255, 0.18) 1.2px, transparent 1.2px);
      background-size: 16px 16px;
      pointer-events: none;
      opacity: 0.7;
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
      color: #be123c;
      font-weight: 900;
      font-size: 14px;
      padding: 6px 13px;
      border-radius: 8px;
      letter-spacing: 0.08em;
      border: 1px solid rgba(255, 255, 255, 0.4);
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }
    .logo-badge::before {
      content: '';
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #e11d48;
      box-shadow: 0 0 6px #e11d48;
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
    /* React Bits: Shiny Text Shimmer Animation */
    .shiny-text {
      background: linear-gradient(120deg, #ffffff 0%, #ffffff 35%, #fed7aa 50%, #ffffff 65%, #ffffff 100%);
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

    .brand-text h1 span {
      background: rgba(255, 255, 255, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.3);
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
      color: rgba(255, 255, 255, 0.9);
      letter-spacing: 0.02em;
      font-weight: 500;
      text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }

    /* React Bits: Floating Dock Navigation Capsule */
    .nav-tabs {
      display: flex;
      gap: 3px;
      flex-wrap: wrap;
      background: rgba(0, 0, 0, 0.45);
      padding: 4px;
      border-radius: 9999px;
      border: 1px solid rgba(255, 255, 255, 0.22);
      backdrop-filter: blur(14px);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }
    .nav-tab {
      background: transparent;
      border: none;
      color: rgba(255, 255, 255, 0.88);
      padding: 7px 15px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      cursor: pointer;
      transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .nav-tab:hover {
      color: #ffffff;
      background: rgba(255, 255, 255, 0.18);
      transform: translateY(-1px);
    }
    .nav-tab.active {
      background: #ffffff;
      color: #000000;
      font-weight: 800;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
      transform: scale(1.02);
    }"""

if old_header_css in code:
    code = code.replace(old_header_css, new_header_css)
    print("Replaced header CSS successfully!")
else:
    print("Could not find exact old_header_css, trying regex replacement...")
    # fallback regex
    pattern = re.compile(r'/\* Stealth Athletic Header \*/.*?/\* Container \*/', re.DOTALL)
    code = pattern.sub(new_header_css + "\n\n    /* Container */", code)
    print("Replaced via regex!")

# 2. Update React Bits Card Hover & Spotlight
card_hover_addon = """
    /* React Bits: Spotlight Card Depth & Glow */
    .stat-card, .auction-card, .case-card, .table-container, .purse-tracker {
      position: relative;
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s, box-shadow 0.2s;
    }
    .stat-card:hover, .auction-card:hover, .case-card:hover {
      border-color: rgba(225, 29, 72, 0.5);
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(225, 29, 72, 0.12);
    }
"""

if "/* React Bits: Spotlight Card" not in code:
    code = code.replace("/* Container */", card_hover_addon + "\n    /* Container */")

# 3. Add ShinyText class to HTML header
code = code.replace('<h1>SupeRR Selector <span>War Room</span></h1>', '<h1 class="shiny-text">SupeRR Selector <span>War Room</span></h1>')

with open("build_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Saved build_dashboard.py with React Bits colored header & dock!")
