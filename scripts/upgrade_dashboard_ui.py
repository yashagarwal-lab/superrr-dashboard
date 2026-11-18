import re

def update_build_dashboard():
    with open('build_dashboard.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update switchTab to fix SVG event.target bug
    old_switch = """    function switchTab(tabId, e) {
      document.querySelectorAll('.tab-view').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
      const targetTab = document.getElementById('tab-' + tabId);
      if (targetTab) targetTab.classList.add('active');
      if (e && e.target) e.target.classList.add('active');
      if (tabId === 'scatter') drawScatter();
      if (tabId === 'radar') initRadar();
    }"""

    new_switch = """    function switchTab(tabId, e) {
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
    }"""

    assert old_switch in content, "old_switch not found"
    content = content.replace(old_switch, new_switch, 1)

    # 2. Update searchAuditPools to hide empty pool cards
    old_search_audit = """    function searchAuditPools() {
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
    }"""

    new_search_audit = """    function searchAuditPools() {
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
    }"""

    assert old_search_audit in content, "old_search_audit not found"
    content = content.replace(old_search_audit, new_search_audit, 1)

    # 3. Update openModal to fix 'undefined Econ' for all-rounders
    old_modal_phases = """      document.getElementById('mPh1').innerText = `${p.pp_balls} balls | ${isBat ? p.pp_sr + ' SR' : p.pp_econ + ' Econ' + (p.pp_wkts !== undefined ? ' (' + p.pp_wkts + ' Wkts)' : '')}`;
      document.getElementById('mPh2').innerText = `${p.mid_balls} balls | ${isBat ? p.mid_sr + ' SR' : p.mid_econ + ' Econ' + (p.mid_wkts !== undefined ? ' (' + p.mid_wkts + ' Wkts)' : '')}`;
      document.getElementById('mPh3').innerText = `${p.death_balls} balls | ${isBat ? p.death_sr + ' SR' : p.death_econ + ' Econ' + (p.death_wkts !== undefined ? ' (' + p.death_wkts + ' Wkts)' : '')}`;"""

    new_modal_phases = """      let ph1Text = '', ph2Text = '', ph3Text = '';
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
      document.getElementById('mPh3').innerText = ph3Text;"""

    assert old_modal_phases in content, "old_modal_phases not found"
    content = content.replace(old_modal_phases, new_modal_phases, 1)

    # 4. Update renderAuctionBoard to deduplicate players and add avatar initials + spotlight + 3d tilt
    old_render_auction = """    function renderAuctionBoard(filterType) {
      const grid = document.getElementById('auctionGrid');
      // Strictly include ONLY actionable auction targets (Free Agents, Global Steals, Domestic Steals, Release Watch)
      // Excludes all franchise retentions (Rohit Sharma, Hardik Pandya, Arshdeep, Shami, etc.), RR core, trades, and ineligible players
      const actionableBadgeTypes = ['free_agent', 'global_steal', 'domestic_steal', 'release_watch'];
      const allTargets = [
        ...DATA.batters.filter(p => actionableBadgeTypes.includes(p.badge_type)),
        ...DATA.bowlers.filter(p => actionableBadgeTypes.includes(p.badge_type))
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
    }"""

    new_render_auction = """    function renderAuctionBoard(filterType) {
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
              <div style="display:flex; align-items:center; gap:12px;">
                <div class="player-avatar-circle ${avatarClass}">${initials}</div>
                <div>
                  <div class="auction-player-name">${p.name}</div>
                  <div class="auction-role">${p.role || p.archetype || 'Player'}</div>
                </div>
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
    }"""

    assert old_render_auction in content, "old_render_auction not found"
    content = content.replace(old_render_auction, new_render_auction, 1)

    # 5. Tab 2 Filter buttons: ensure filterAuctionTargets updates pills
    old_filter_auction = """    function filterAuctionTargets(type, el) {
      document.querySelectorAll('#tab-auction .pill').forEach(p => p.classList.remove('active'));
      el.classList.add('active');
      renderAuctionBoard(type);
    }"""

    new_filter_auction = """    function filterAuctionTargets(type, el) {
      document.querySelectorAll('#tab-auction .pill').forEach(p => p.classList.remove('active'));
      if (el && el.classList) el.classList.add('active');
      renderAuctionBoard(type);
    }"""

    assert old_filter_auction in content, "old_filter_auction not found"
    content = content.replace(old_filter_auction, new_filter_auction, 1)

    # 6. Tab 6 Whoop remnants removal
    content = content.replace("<!-- TAB 6: WHOOP-INSPIRED XI BUILDER & SELECTION PANEL -->", "<!-- TAB 6: RAJASTHAN ROYALS CHAMPIONSHIP COMMAND CENTER: XI BUILDER & SALARY CAP TRACKER -->")
    content = content.replace("Whoop-inspired Starting XI lineup simulator", "Interactive Starting XI lineup simulator")
    content = content.replace("<!-- 1-CLICK SLOT ASSIGNMENT MODAL (Whoop Redesign) -->", "<!-- 1-CLICK SLOT ASSIGNMENT MODAL (Rajasthan Royals Command Center) -->")

    # Replace Tab 6 reset button inline dark style with star-border-btn
    old_reset_btn = """<button onclick="resetXI()" style="background: #111116; border: 1px solid #272733; color: #a1a1aa; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; padding: 7px 14px; border-radius: 6px; cursor: pointer; transition: all 0.12s;" onmouseover="this.style.color='#ffffff'; this.style.borderColor='#3f3f50';" onmouseout="this.style.color='#a1a1aa'; this.style.borderColor='#272733';">
          ↺ Reset to Recommended XI
        </button>"""

    new_reset_btn = """<button onclick="resetXI()" class="star-border-btn" style="padding: 7px 16px; font-size: 11px;">
          ↺ Reset to Recommended XI
        </button>"""

    assert old_reset_btn in content, "old_reset_btn not found"
    content = content.replace(old_reset_btn, new_reset_btn, 1)

    # Replace Tab 6 squad balance box and cards
    old_squad_box = """<div id="squadBalanceBox" style="background: #040406; border: 1px solid #16161b; border-radius: 6px; padding: 12px; margin-bottom: 14px;">"""
    new_squad_box = """<div id="squadBalanceBox" style="background: rgba(6, 11, 26, 0.7); border: 1px solid var(--rr-navy-border); border-radius: 10px; padding: 14px; margin-bottom: 14px; backdrop-filter: blur(12px);">"""
    assert old_squad_box in content, "old_squad_box not found"
    content = content.replace(old_squad_box, new_squad_box, 1)

    old_death_box = """<div style="background: var(--slate-900); border-left: 3px solid #ff3b30; border-radius: 6px; padding: 12px; font-size: 12px;">
            <strong style="color: var(--slate-50);">Death Yorker & Pace Shock:</strong> Jofra Archer (150+ kph) paired with Sandeep Sharma (66.8 RPCS) provides impenetrable death-overs execution.
          </div>"""
    new_death_box = """<div style="background: rgba(14, 23, 51, 0.75); border-left: 3px solid var(--rr-pink); border-radius: 8px; padding: 12px; font-size: 12px; border: 1px solid var(--rr-navy-border); backdrop-filter: blur(12px);">
            <strong style="color: var(--slate-50);">Death Yorker & Pace Shock:</strong> Jofra Archer (150+ kph) paired with Sandeep Sharma (66.8 RPCS) provides impenetrable death-overs execution.
          </div>"""
    assert old_death_box in content, "old_death_box not found"
    content = content.replace(old_death_box, new_death_box, 1)

    # Replace posColors in renderXI
    old_pos_colors = """      const posColors = {
        'Openers': '#00e599',
        'Middle Order': '#00d4ff',
        'WK': '#ff9f0a',
        'Finisher': '#ff2a85',
        'All-Rounders': '#a855f7',
        'Spinners': '#6366f1',
        'Pacers': '#ff3b30'
      };"""

    new_pos_colors = """      const posColors = {
        'Openers': '#ea1a7f',
        'Middle Order': '#38bdf8',
        'WK': '#fbbf24',
        'Finisher': '#ff2a8d',
        'All-Rounders': '#a855f7',
        'Spinners': '#f59e0b',
        'Pacers': '#f43f5e'
      };"""

    assert old_pos_colors in content, "old_pos_colors not found"
    content = content.replace(old_pos_colors, new_pos_colors, 1)

    # Replace slotModal title color
    content = content.replace('titleEl.innerHTML = `Assign Slot #${slot.num}: <span style="color:#00e599;">${slot.posCategory}</span>`;',
                            'titleEl.innerHTML = `Assign Slot #${slot.num}: <span style="color:#ea1a7f;">${slot.posCategory}</span>`;')

    # Replace slot candidate cost color
    content = content.replace('Cost: <strong style="color:#00e599;">₹${cost.toFixed(2)} Cr</strong>',
                            'Cost: <strong style="color:#34d399;">₹${cost.toFixed(2)} Cr</strong>')

    # Replace delta pills in renderSlotCandidates
    old_delta_pill = """        let deltaHtml = '';
        if (delta > 0) {
          deltaHtml = `<span class="candidate-delta-pill" style="color:#00e599; background:rgba(0,229,153,0.08); border:1px solid rgba(0,229,153,0.3);">+₹${delta.toFixed(2)} Cr Saved</span>`;
        } else if (delta < 0) {
          const costMore = Math.abs(delta);
          const color = isOverBudget ? '#ff3b30' : '#ff9f0a';
          deltaHtml = `<span class="candidate-delta-pill" style="color:${color}; background:rgba(${isOverBudget ? '255,59,48' : '255,159,10'},0.08); border:1px solid rgba(${isOverBudget ? '255,59,48' : '255,159,10'},0.3);">-₹${costMore.toFixed(2)} Cr Spend</span>`;
        } else {
          deltaHtml = `<span class="candidate-delta-pill" style="color:#71717a; background:#111115; border:1px solid #22222a;">₹0.00 Cr Impact</span>`;
        }"""

    new_delta_pill = """        let deltaHtml = '';
        if (delta > 0) {
          deltaHtml = `<span class="candidate-delta-pill" style="color:#34d399; background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3);">+₹${delta.toFixed(2)} Cr Saved</span>`;
        } else if (delta < 0) {
          const costMore = Math.abs(delta);
          const color = isOverBudget ? '#f87171' : '#fbbf24';
          deltaHtml = `<span class="candidate-delta-pill" style="color:${color}; background:rgba(${isOverBudget ? '239,68,68' : '251,191,36'},0.1); border:1px solid rgba(${isOverBudget ? '239,68,68' : '251,191,36'},0.3);">-₹${costMore.toFixed(2)} Cr Spend</span>`;
        } else {
          deltaHtml = `<span class="candidate-delta-pill" style="color:var(--slate-400); background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);">₹0.00 Cr Impact</span>`;
        }"""

    assert old_delta_pill in content, "old_delta_pill not found"
    content = content.replace(old_delta_pill, new_delta_pill, 1)

    # Replace radar colors
    old_radar_poly = """      drawPoly(getProfile(p1), '#ff2a85', 'rgba(255, 42, 133, 0.16)');
      drawPoly(getProfile(p2), '#00e599', 'rgba(0, 229, 153, 0.16)');

      // Legend
      ctx.textAlign = 'left';
      ctx.font = '600 12px Inter, sans-serif';
      ctx.fillStyle = '#fb7185';
      ctx.fillText(`■ ${p1.name} (RPCS ${p1.rpcs})`, 24, 24);
      ctx.fillStyle = '#34d399';
      ctx.fillText(`■ ${p2.name} (RPCS ${p2.rpcs})`, 24, 44);"""

    new_radar_poly = """      drawPoly(getProfile(p1), '#ea1a7f', 'rgba(234, 26, 127, 0.22)');
      drawPoly(getProfile(p2), '#fbbf24', 'rgba(251, 191, 36, 0.22)');

      // Legend
      ctx.textAlign = 'left';
      ctx.font = '700 12px Inter, sans-serif';
      ctx.fillStyle = '#ea1a7f';
      ctx.fillText(`■ ${p1.name} (RPCS ${p1.rpcs})`, 24, 24);
      ctx.fillStyle = '#fbbf24';
      ctx.fillText(`■ ${p2.name} (RPCS ${p2.rpcs})`, 24, 44);"""

    assert old_radar_poly in content, "old_radar_poly not found"
    content = content.replace(old_radar_poly, new_radar_poly, 1)

    # 7. Add spotlight and tilted-card classes to Tab 7 case cards
    old_cases = """    <!-- TAB 7: CASE STUDIES -->
    <div id="tab-cases" class="tab-view">
      <div class="case-grid">
        <div class="case-card">"""

    new_cases = """    <!-- TAB 7: CASE STUDIES -->
    <div id="tab-cases" class="tab-view">
      <div class="case-grid">
        <div class="case-card spotlight-card tilted-card">"""

    assert old_cases in content, "old_cases not found"
    content = content.replace(old_cases, new_cases, 1)
    content = content.replace('<div class="case-card">', '<div class="case-card spotlight-card tilted-card">')

    # 8. Add spotlight and tilted-card classes to Tab 8 methodology cards
    old_math = """    <!-- TAB 8: METHODOLOGY PROOFS -->
    <div id="tab-math" class="tab-view">
      <div class="chart-panel">
        <h2 style="font-size: 20px; font-weight: 700; color: var(--slate-50); margin-bottom: 16px;">Core Mathematical Modeling Architecture</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
          <div class="modal-section">"""

    new_math = """    <!-- TAB 8: METHODOLOGY PROOFS -->
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
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
          <div class="modal-section spotlight-card tilted-card" style="border-top: 3px solid #10b981;">"""

    assert old_math in content, "old_math not found"
    content = content.replace(old_math, new_math, 1)

    # Replace other 3 math modal-sections with spotlight-card tilted-card
    old_m2 = """          <div class="modal-section">
            <h4 style="color: #34d399;">2. Calibrated 2nd Innings Logistic Model</h4>"""
    new_m2 = """          <div class="modal-section spotlight-card tilted-card" style="border-top: 3px solid #fbbf24;">
            <h4 style="color: #fbbf24;">2. Calibrated 2nd Innings Logistic Model</h4>"""
    assert old_m2 in content, "old_m2 not found"
    content = content.replace(old_m2, new_m2, 1)

    old_m3 = """          <div class="modal-section">
            <h4 style="color: #34d399;">3. Multiplicative Retention Ratio (κ)</h4>"""
    new_m3 = """          <div class="modal-section spotlight-card tilted-card" style="border-top: 3px solid #ea1a7f;">
            <h4 style="color: #ff2a8d;">3. Multiplicative Retention Ratio (κ)</h4>"""
    assert old_m3 in content, "old_m3 not found"
    content = content.replace(old_m3, new_m3, 1)

    old_m4 = """          <div class="modal-section">
            <h4 style="color: #34d399;">4. Non-Striker WPA Conservation</h4>"""
    new_m4 = """          <div class="modal-section spotlight-card tilted-card" style="border-top: 3px solid #38bdf8;">
            <h4 style="color: #38bdf8;">4. Non-Striker WPA Conservation</h4>"""
    assert old_m4 in content, "old_m4 not found"
    content = content.replace(old_m4, new_m4, 1)

    # 9. Update initTiltedCards so it doesn't re-bind and handles dynamically rendered cards
    old_tilted = """    // 3. React Bits: TiltedCard 3D Hover Physics
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
    }"""

    new_tilted = """    // 3. React Bits: TiltedCard 3D Hover Physics
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
    }"""

    assert old_tilted in content, "old_tilted not found"
    content = content.replace(old_tilted, new_tilted, 1)

    with open('build_dashboard.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully updated build_dashboard.py with all enhancements!")

if __name__ == '__main__':
    update_build_dashboard()
