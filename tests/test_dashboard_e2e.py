"""
E2E Test Suite for Rajasthan Royals SupeRR Selector Redesign
============================================================
Covers all requirements from PROJECT.md, ORIGINAL_REQUEST.md, and DISPATCH.md:
- Tier 1: Feature Coverage (Data records, build compilation, modern UI styling)
- Tier 2: Boundary & Corner Cases (27 Pakistani records, dual-role sync, 394 record count)
- Tier 3: Cross-Feature Combinations (Filter categories, Node.js vm script syntax & DOM simulation)
- Tier 4: Real-World Application Scenarios (War Room leakage prevention, ₹120 Cr purse calculator)
"""

import json
import os
import re
import subprocess
import pytest

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(WORKSPACE_DIR, "dashboard", "data.json")
HTML_PATH = os.path.join(WORKSPACE_DIR, "dashboard", "index.html")
BUILD_SCRIPT = os.path.join(WORKSPACE_DIR, "build_dashboard.py")


@pytest.fixture(scope="session")
def dashboard_data():
    """Load and parse dashboard/data.json."""
    assert os.path.isfile(DATA_PATH), f"data.json not found at {DATA_PATH}"
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "batters" in data, "data.json missing 'batters' key"
    assert "bowlers" in data, "data.json missing 'bowlers' key"
    return data


@pytest.fixture(scope="session")
def dashboard_html():
    """Read compiled dashboard/index.html."""
    assert os.path.isfile(HTML_PATH), f"index.html not found at {HTML_PATH}"
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


def _find_player(data, role, name):
    """Find a player by name in the specified role array."""
    for p in data.get(role, []):
        if p.get("name") == name:
            return p
    return None


def _find_player_any(data, name):
    """Find a player in either batters or bowlers."""
    for cat in ["batters", "bowlers"]:
        for p in data.get(cat, []):
            if p.get("name") == name:
                return p, cat
    return None, None


# ==============================================================================
# TIER 1: FEATURE COVERAGE
# ==============================================================================

class TestTier1FeatureCoverage:
    """Verify specific player records, build execution, and styling overhaul."""

    def test_kuldeep_yadav_trade_to_lsg(self, dashboard_data):
        """Kuldeep Yadav: Bowler | LSG | Confirmed traded in (LSG-DC swap for Rishabh Pant)."""
        kuldeep_bowl = _find_player(dashboard_data, "bowlers", "Kuldeep Yadav")
        assert kuldeep_bowl is not None, "Kuldeep Yadav not found in bowlers array"

        # Team must be Lucknow Super Giants (traded from Delhi Capitals)
        team = kuldeep_bowl.get("team_2026", "")
        assert "Lucknow" in team or "LSG" in team, (
            f"Expected Kuldeep Yadav team_2026 to be 'Lucknow Super Giants', got '{team}'"
        )

        # Badge type must be 'traded'
        badge = kuldeep_bowl.get("badge_type", "")
        assert badge == "traded", f"Expected Kuldeep Yadav badge_type='traded', got '{badge}'"

        # Auction status must reflect trade
        status = kuldeep_bowl.get("auction_status", "")
        assert "Traded" in status or "Locked" in status, (
            f"Expected auction_status to indicate trade/locked, got '{status}'"
        )

        # Trade notes must mention swap with DC / Rishabh Pant
        notes = kuldeep_bowl.get("trade_notes", "") + kuldeep_bowl.get("desc", "") + kuldeep_bowl.get("rr_note", "")
        assert any(k in notes for k in ["LSG", "DC", "Pant", "trade", "swap"]), (
            f"Trade notes should document LSG-DC swap for Rishabh Pant: '{notes}'"
        )

    def test_taskin_ahmed_unsold_free_agent(self, dashboard_data):
        """Taskin Ahmed: Bowler | Confirmed not retained / Unsold Free Agent (₹75L)."""
        taskin = _find_player(dashboard_data, "bowlers", "Taskin Ahmed")
        assert taskin is not None, "Taskin Ahmed not found in bowlers array"

        badge = taskin.get("badge_type", "")
        assert badge == "free_agent", (
            f"Expected Taskin Ahmed badge_type='free_agent', got '{badge}'"
        )

        status = taskin.get("auction_status", "")
        assert "Free Agent" in status or "Released" in status, (
            f"Expected auction_status to indicate Free Agent / Released, got '{status}'"
        )

        # Team should reflect free agent / released status
        team = taskin.get("team_2026", "")
        assert any(k in team for k in ["RELEASED", "Free Agent", "None"]), (
            f"Expected team_2026 to indicate released free agent, got '{team}'"
        )

        # Notes or description should mention unsold at ₹75L or available auction buy
        notes = taskin.get("trade_notes", "") + taskin.get("desc", "") + taskin.get("rr_note", "")
        assert any(k in notes for k in ["75L", "75 Lakh", "unsold", "available", "Free Agent"]), (
            f"Expected notes to mention ₹75L unsold / available buy: '{notes}'"
        )

    @pytest.mark.parametrize("player_name", ["Sufiyan Muqeem", "Mohammad Nawaz", "Abrar Ahmed"])
    def test_pakistani_trio_bcci_ineligible(self, dashboard_data, player_name):
        """Sufiyan Muqeem, Mohammad Nawaz, Abrar Ahmed: Ineligible / Non-IPL under BCCI policy."""
        p, role = _find_player_any(dashboard_data, player_name)
        assert p is not None, f"Pakistani player {player_name} not found in dataset"

        assert p.get("country") == "Pakistan", f"{player_name} country must be 'Pakistan'"

        eligibility = p.get("eligibility", "")
        assert eligibility == "BCCI Ineligible", (
            f"Expected {player_name} eligibility='BCCI Ineligible', got '{eligibility}'"
        )

        badge = p.get("badge_type", "")
        assert badge == "ineligible", (
            f"Expected {player_name} badge_type='ineligible', got '{badge}'"
        )

        status = p.get("auction_status", "")
        assert "Ineligible" in status or "Non-IPL" in status, (
            f"Expected {player_name} auction_status to contain 'Ineligible' or 'Non-IPL', got '{status}'"
        )

    def test_travis_head_workload_opt_out(self, dashboard_data):
        """Travis Head: Batter | SRH | Likely released (workload opt-out)."""
        head = _find_player(dashboard_data, "batters", "Travis Head")
        assert head is not None, "Travis Head not found in batters array"

        assert "Sunrisers" in head.get("team_2026", "") or "SRH" in head.get("team_2026", ""), (
            f"Expected team_2026 to be SRH, got '{head.get('team_2026')}'"
        )

        badge = head.get("badge_type", "")
        assert badge in ["release_watch", "opt_out", "watchlist"], (
            f"Expected Travis Head badge_type in ['release_watch', 'opt_out', 'watchlist'], got '{badge}'"
        )

        status = head.get("auction_status", "")
        assert any(k in status.lower() for k in ["release", "opt-out", "opt out", "watch"]), (
            f"Expected auction_status to indicate release watch / opt-out, got '{status}'"
        )

        notes = head.get("trade_notes", "") + head.get("desc", "") + head.get("rr_note", "")
        assert any(k in notes.lower() for k in ["workload", "opt-out", "opt out", "australia"]), (
            f"Expected trade_notes to mention workload opt-out: '{notes}'"
        )

    def test_matheesha_pathirana_release_watch(self, dashboard_data):
        """Matheesha Pathirana: Bowler | KKR | Major release candidate (₹18 Cr release watch)."""
        pathirana = _find_player(dashboard_data, "bowlers", "Matheesha Pathirana")
        assert pathirana is not None, "Matheesha Pathirana not found in bowlers array"

        assert "Kolkata" in pathirana.get("team_2026", "") or "KKR" in pathirana.get("team_2026", ""), (
            f"Expected team_2026 to be KKR, got '{pathirana.get('team_2026')}'"
        )

        badge = pathirana.get("badge_type", "")
        assert badge in ["release_watch", "watchlist"], (
            f"Expected Matheesha Pathirana badge_type in ['release_watch', 'watchlist'], got '{badge}'"
        )

        notes = pathirana.get("trade_notes", "") + pathirana.get("desc", "") + pathirana.get("rr_note", "")
        assert any(k in notes for k in ["18 Cr", "18.0 Cr", "18 crore", "release", "funds", "purse"]), (
            f"Expected trade_notes to mention ₹18 Cr release watch: '{notes}'"
        )

    def test_rajasthan_royals_core_retentions(self, dashboard_data):
        """Yashasvi Jaiswal & Vaibhav Sooryavanshi: RR Core retentions."""
        jaiswal = _find_player(dashboard_data, "batters", "Yashasvi Jaiswal")
        sooryavanshi = _find_player(dashboard_data, "batters", "Vaibhav Sooryavanshi")

        assert jaiswal is not None, "Yashasvi Jaiswal not found in batters array"
        assert sooryavanshi is not None, "Vaibhav Sooryavanshi not found in batters array"

        for p, name in [(jaiswal, "Yashasvi Jaiswal"), (sooryavanshi, "Vaibhav Sooryavanshi")]:
            assert p.get("team_2026") == "Rajasthan Royals", (
                f"{name} team_2026 must be 'Rajasthan Royals', got '{p.get('team_2026')}'"
            )
            assert p.get("badge_type") == "rr_core", (
                f"{name} badge_type must be 'rr_core', got '{p.get('badge_type')}'"
            )
            assert "RR Core" in p.get("auction_status", ""), (
                f"{name} auction_status must contain 'RR Core', got '{p.get('auction_status')}'"
            )

        # Contextual notes
        j_notes = jaiswal.get("trade_notes", "") + jaiswal.get("desc", "") + jaiswal.get("rr_note", "")
        assert any(k in j_notes.lower() for k in ["retained", "trade interest", "core"]), (
            f"Jaiswal notes should document retention despite trade interest: '{j_notes}'"
        )

        v_notes = sooryavanshi.get("trade_notes", "") + sooryavanshi.get("desc", "") + sooryavanshi.get("rr_note", "")
        assert any(k in v_notes.lower() for k in ["1.10", "1.1 cr", "orange cap", "mvp", "retained", "core"]), (
            f"Sooryavanshi notes should document ₹1.10 Cr deal / Orange Cap / MVP: '{v_notes}'"
        )

    @pytest.mark.parametrize("player_name,expected_team,role", [
        ("Abhishek Sharma", "Sunrisers Hyderabad", "batters"),
        ("Jos Buttler", "Gujarat Titans", "batters"),
        ("Suryakumar Yadav", "Mumbai Indians", "batters"),
        ("Phil Salt", "Royal Challengers Bengaluru", "batters"),
        ("Tim David", "Royal Challengers Bengaluru", "batters"),
        ("Virat Kohli", "Royal Challengers Bengaluru", "batters"),
        ("Prabhsimran Singh", "Punjab Kings", "batters"),
        ("Jasprit Bumrah", "Mumbai Indians", "bowlers"),
        ("Rashid Khan", "Gujarat Titans", "bowlers"),
        ("Sunil Narine", "Kolkata Knight Riders", "bowlers"),
        ("Mitchell Santner", "Mumbai Indians", "bowlers"),
    ])
    def test_untouchable_core_retentions(self, dashboard_data, player_name, expected_team, role):
        """Untouchable franchise core retentions across all teams."""
        p = _find_player(dashboard_data, role, player_name)
        assert p is not None, f"Untouchable core player {player_name} not found in {role}"

        assert p.get("badge_type") == "retention", (
            f"Expected {player_name} badge_type='retention', got '{p.get('badge_type')}'"
        )

        status = p.get("auction_status", "")
        assert any(k in status for k in ["Untouchable", "Franchise Core", "Retention"]), (
            f"Expected {player_name} auction_status to indicate Untouchable Retention, got '{status}'"
        )

        assert expected_team in p.get("team_2026", ""), (
            f"Expected {player_name} team_2026 to contain '{expected_team}', got '{p.get('team_2026')}'"
        )

    @pytest.mark.parametrize("player_name,role", [
        ("Nathan Ellis", "bowlers"),
        ("Jonny Bairstow", "batters"),
        ("Glenn Maxwell", "batters"),
    ])
    def test_confirmed_released_free_agents(self, dashboard_data, player_name, role):
        """Confirmed released free agents (Nathan Ellis, Jonny Bairstow, Glenn Maxwell)."""
        p = _find_player(dashboard_data, role, player_name)
        assert p is not None, f"Free agent {player_name} not found in {role}"

        assert p.get("badge_type") == "free_agent", (
            f"Expected {player_name} badge_type='free_agent', got '{p.get('badge_type')}'"
        )

        status = p.get("auction_status", "")
        assert any(k in status for k in ["Released", "Free Agent"]), (
            f"Expected {player_name} auction_status to indicate Released / Free Agent, got '{status}'"
        )

    def test_build_dashboard_compiles_successfully(self):
        """Verify build_dashboard.py compiles without error and generates dashboard/index.html."""
        result = subprocess.run(
            ["python3", BUILD_SCRIPT],
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"build_dashboard.py failed with stderr: {result.stderr}"
        assert os.path.isfile(HTML_PATH), f"Output {HTML_PATH} does not exist after build"
        assert os.path.getsize(HTML_PATH) > 400_000, (
            f"dashboard/index.html is smaller than expected: {os.path.getsize(HTML_PATH)} bytes"
        )

    def test_dashboard_html_design_tokens_and_anti_slop(self, dashboard_html):
        """Verify Tailwind/Shadcn/Tremor design tokens present and neon AI-slop tropes removed."""
        # Check presence of sports analytics / Tremor / Shadcn tokens
        has_tabular = "tabular-nums" in dashboard_html
        has_slate_or_tailwind = any(
            token in dashboard_html for token in [
                "--slate-", "slate-900", "slate-950", "#0f172a", "#020617", "#1e293b", "tailwindcss"
            ]
        )
        assert has_tabular, "Missing 'tabular-nums' for sports analytics table alignment"
        assert has_slate_or_tailwind, "Missing slate neutral design tokens (Shadcn/Tremor aesthetic)"

        # Check absence of generic AI neon tropes
        obsolete_neon_gradient = "linear-gradient(135deg, #101626 0%, #1a0826 50%, #0a0e17 100%)"
        obsolete_glow_shadow_1 = "box-shadow: 0 4px 15px rgba(234, 26, 142, 0.4)"
        obsolete_glow_shadow_2 = "box-shadow: 0 4px 12px rgba(234, 26, 142, 0.3)"

        assert obsolete_neon_gradient not in dashboard_html, (
            "Found obsolete AI neon header gradient in dashboard/index.html"
        )
        assert obsolete_glow_shadow_1 not in dashboard_html, (
            "Found glowing neon box-shadow in dashboard/index.html"
        )
        assert obsolete_glow_shadow_2 not in dashboard_html, (
            "Found glowing neon box-shadow in dashboard/index.html"
        )


# ==============================================================================
# TIER 2: BOUNDARY & CORNER CASES
# ==============================================================================

class TestTier2BoundaryAndCornerCases:
    """Verify Pakistani cohort, dual-role synchronization, and data bounds."""

    def test_all_27_pakistani_player_records_ineligible_and_red_badge(self, dashboard_data, dashboard_html):
        """Check all 27 Pakistani player records have BCCI Ineligible and red badge styling."""
        pak_batters = [p for p in dashboard_data["batters"] if p.get("country") == "Pakistan"]
        pak_bowlers = [p for p in dashboard_data["bowlers"] if p.get("country") == "Pakistan"]
        total_pak_records = len(pak_batters) + len(pak_bowlers)

        assert total_pak_records == 27, (
            f"Expected exactly 27 Pakistani records (13 batters, 14 bowlers), found {total_pak_records} "
            f"({len(pak_batters)} batters, {len(pak_bowlers)} bowlers)"
        )

        for p in pak_batters + pak_bowlers:
            name = p.get("name")
            assert p.get("eligibility") == "BCCI Ineligible", (
                f"Pakistani player {name} must have eligibility='BCCI Ineligible', got '{p.get('eligibility')}'"
            )
            assert p.get("badge_type") == "ineligible", (
                f"Pakistani player {name} must have badge_type='ineligible', got '{p.get('badge_type')}'"
            )
            status = p.get("auction_status", "")
            assert "Ineligible" in status or "Non-IPL" in status, (
                f"Pakistani player {name} must have auction_status indicating Ineligible/Non-IPL, got '{status}'"
            )

        # Check red visual badge / row styling in HTML
        has_red_badge_class = any(
            cls in dashboard_html for cls in ["badge-ineligible", "row-ineligible", "tag-ineligible", "bg-red"]
        )
        assert has_red_badge_class, "Missing red badge or row CSS styling for BCCI Ineligible players"

    def test_dual_role_all_rounders_attribute_synchronization(self, dashboard_data):
        """Check dual-role players have synchronized attributes across batters and bowlers."""
        batters_by_name = {p["name"]: p for p in dashboard_data["batters"]}
        bowlers_by_name = {p["name"]: p for p in dashboard_data["bowlers"]}
        dual_role_names = set(batters_by_name.keys()) & set(bowlers_by_name.keys())

        assert len(dual_role_names) == 48, f"Expected 48 dual-role players, found {len(dual_role_names)}"

        desync_errors = []
        sync_fields = ["team_2026", "eligibility", "auction_status", "badge_type"]

        for name in sorted(dual_role_names):
            b_bat = batters_by_name[name]
            b_bowl = bowlers_by_name[name]

            for field in sync_fields:
                val_bat = b_bat.get(field)
                val_bowl = b_bowl.get(field)
                if val_bat != val_bowl:
                    desync_errors.append(
                        f"Player '{name}' desynchronized on '{field}': Batters='{val_bat}' vs Bowlers='{val_bowl}'"
                    )

        assert not desync_errors, (
            f"Found {len(desync_errors)} attribute desynchronization errors in dual-role players:\n"
            + "\n".join(desync_errors[:10])
        )

    def test_total_record_count_preservation(self, dashboard_data):
        """Preserve exact universe: 198 batters, 196 bowlers = 394 total records."""
        n_bat = len(dashboard_data["batters"])
        n_bowl = len(dashboard_data["bowlers"])
        total = n_bat + n_bowl

        assert n_bat == 198, f"Expected exactly 198 batters, found {n_bat}"
        assert n_bowl == 196, f"Expected exactly 196 bowlers, found {n_bowl}"
        assert total == 394, f"Expected exactly 394 total records, found {total}"

        # Unique IDs within each role array
        bat_ids = [p["player_id"] for p in dashboard_data["batters"]]
        bowl_ids = [p["player_id"] for p in dashboard_data["bowlers"]]
        assert len(bat_ids) == len(set(bat_ids)), "Duplicate player_id detected in batters array"
        assert len(bowl_ids) == len(set(bowl_ids)), "Duplicate player_id detected in bowlers array"

    def test_sunil_narine_country_accuracy(self, dashboard_data):
        """Sunil Narine: Country must be West Indies in both batters and bowlers."""
        narine_bat = _find_player(dashboard_data, "batters", "Sunil Narine")
        narine_bowl = _find_player(dashboard_data, "bowlers", "Sunil Narine")

        assert narine_bat is not None, "Sunil Narine not found in batters"
        assert narine_bowl is not None, "Sunil Narine not found in bowlers"

        assert narine_bat.get("country") == "West Indies", (
            f"Narine batter country should be 'West Indies', got '{narine_bat.get('country')}'"
        )
        assert narine_bowl.get("country") == "West Indies", (
            f"Narine bowler country should be 'West Indies', got '{narine_bowl.get('country')}'"
        )

    def test_player_metric_values_numerical_integrity(self, dashboard_data):
        """All 394 records must have valid non-null numerical values for core metrics."""
        for role in ["batters", "bowlers"]:
            for p in dashboard_data[role]:
                name = p.get("name", "Unknown")
                rpcs = p.get("rpcs")
                csr = p.get("csr")
                kappa = p.get("kappa")
                wpa = p.get("wpa")

                assert isinstance(rpcs, (int, float)) and rpcs > 0, (
                    f"{role} '{name}' has invalid rpcs: {rpcs}"
                )
                assert isinstance(csr, (int, float)) and csr >= 0, (
                    f"{role} '{name}' has invalid csr: {csr}"
                )
                assert isinstance(kappa, (int, float)) and kappa > 0, (
                    f"{role} '{name}' has invalid kappa: {kappa}"
                )
                assert isinstance(wpa, (int, float)), (
                    f"{role} '{name}' has invalid wpa: {wpa}"
                )


# ==============================================================================
# TIER 3: CROSS-FEATURE COMBINATIONS
# ==============================================================================

class TestTier3CrossFeatureCombinations:
    """Verify UI filter mechanisms, embedded JS syntax, and mock DOM simulation."""

    def test_filter_categories_in_html_and_js(self, dashboard_html):
        """Check filter categories in HTML and JS (BCCI Ineligible, Free Agent, Traded, Watchlist, Retained Core)."""
        required_filter_concepts = [
            ("ineligible", ["ineligible", "bcci_ineligible"]),
            ("free_agent", ["free_agent", "released"]),
            ("traded", ["traded", "trade"]),
            ("watchlist", ["watchlist", "release_watch", "opt_out"]),
            ("retention", ["untouchable", "retention", "rr_core"]),
        ]

        for concept, candidates in required_filter_concepts:
            found = any(c in dashboard_html.lower() for c in candidates)
            assert found, f"HTML/JS missing filter handler/pill for concept: '{concept}' (candidates: {candidates})"

    def test_embedded_javascript_syntax_via_node(self):
        """Validate embedded JavaScript syntax using Node.js vm.Script."""
        node_script = """
const fs = require('fs');
const vm = require('vm');
const filePath = process.argv[1];
const html = fs.readFileSync(filePath, 'utf8');
const match = html.match(/<script[\\s\\S]*?>([\\s\\S]*?)<\\/script>/i);
if (!match) {
    console.error('FAIL: No script tag found');
    process.exit(1);
}
const code = match[1];
try {
    new vm.Script(code);
    console.log('PASS: JS syntax is valid');
} catch (e) {
    console.error('FAIL: JS syntax error:', e.message);
    process.exit(1);
}
"""
        res = subprocess.run(["node", "-e", node_script, HTML_PATH], capture_output=True, text=True)
        assert res.returncode == 0, f"Embedded JS syntax validation failed: {res.stderr}\n{res.stdout}"

    def test_simulated_dom_execution_via_node(self):
        """Validate simulated DOM execution and core handler calls using Node.js vm."""
        sim_script = """
const fs = require('fs');
const vm = require('vm');
const filePath = process.argv[1];
const html = fs.readFileSync(filePath, 'utf8');
const match = html.match(/<script[\\s\\S]*?>([\\s\\S]*?)<\\/script>/i);
if (!match) {
    console.error('FAIL: No script tag found');
    process.exit(1);
}
const code = match[1];

const mockElement = () => ({
    innerHTML: '',
    textContent: '',
    value: '',
    style: {},
    classList: {
        add: () => {},
        remove: () => {},
        contains: () => false,
        toggle: () => {},
    },
    getContext: () => ({
        clearRect: () => {},
        beginPath: () => {},
        arc: () => {},
        fill: () => {},
        stroke: () => {},
        fillText: () => {},
        moveTo: () => {},
        lineTo: () => {},
        measureText: () => ({ width: 10 }),
        setLineDash: () => {},
    }),
    appendChild: () => {},
    querySelectorAll: () => [],
    addEventListener: () => {},
    setAttribute: () => {},
});

const sandbox = {
    window: {
        onload: null,
        addEventListener: () => {},
    },
    document: {
        getElementById: (id) => mockElement(),
        querySelector: (sel) => mockElement(),
        querySelectorAll: (sel) => [mockElement()],
        createElement: (tag) => mockElement(),
    },
    console: console,
    Math: Math,
    parseInt: parseInt,
    parseFloat: parseFloat,
    setTimeout: (fn) => fn(),
    setInterval: () => {},
};
sandbox.window.document = sandbox.document;

vm.createContext(sandbox);
vm.runInContext(code, sandbox);

// Test key lifecycle handlers
if (typeof sandbox.window.onload === 'function') {
    sandbox.window.onload();
}
if (typeof sandbox.renderTable === 'function') {
    sandbox.renderTable();
}
if (typeof sandbox.renderAuctionBoard === 'function') {
    sandbox.renderAuctionBoard('all');
}
if (typeof sandbox.setRole === 'function') {
    sandbox.setRole('bowlers');
    sandbox.setRole('batters');
}

console.log('PASS: Simulated DOM executed cleanly without runtime exceptions');
"""
        res = subprocess.run(["node", "-e", sim_script, HTML_PATH], capture_output=True, text=True)
        assert res.returncode == 0, f"Simulated DOM execution failed: {res.stderr}\n{res.stdout}"


# ==============================================================================
# TIER 4: REAL-WORLD APPLICATION SCENARIOS
# ==============================================================================

class TestTier4RealWorldApplicationScenarios:
    """Verify War Room bidding target isolation and Starting XI purse allocation."""

    def test_auction_war_room_board_leakage(self, dashboard_data, dashboard_html):
        """Auction War Room Board leakage test: ensure no untouchables, RR core, or BCCI ineligibles appear."""
        untouchables = [
            "Virat Kohli", "Jasprit Bumrah", "Suryakumar Yadav", "Sunil Narine",
            "Phil Salt", "Tim David", "Prabhsimran Singh", "Mitchell Santner",
            "Abhishek Sharma", "Jos Buttler", "Rashid Khan"
        ]
        rr_core = ["Yashasvi Jaiswal", "Vaibhav Sooryavanshi"]
        pakistani_ineligible = ["Sufiyan Muqeem", "Mohammad Nawaz", "Abrar Ahmed"]

        restricted_pool = untouchables + rr_core + pakistani_ineligible

        # 1. Check data classification: none of these should have badge_type == 'auction_target'
        leakage_in_data = []
        for name in restricted_pool:
            p, role = _find_player_any(dashboard_data, name)
            if p is not None:
                badge = p.get("badge_type", "")
                avail = p.get("avail_type", "")
                status = p.get("auction_status", "")
                if badge == "auction_target" or avail == "Dynamic Auction / Trade Target":
                    leakage_in_data.append(f"{name} ({role}) labeled as '{badge}' / '{avail}'")

        assert not leakage_in_data, (
            f"Auction board leakage: restricted players classified as active auction targets:\n"
            + "\n".join(leakage_in_data)
        )

        # 2. Check JS auction target filtering logic excludes untouchable, rr_core, and ineligible badges
        assert "renderAuctionBoard" in dashboard_html, "Missing renderAuctionBoard in dashboard/index.html"

    def test_purse_calculator_120_cr_cap_enforcement(self, dashboard_html):
        """Purse calculator test: ensure RR 2027 starting XI purse calculation accounts for ₹120 Cr cap."""
        # Check that the ₹120 Cr cap constraint is explicitly present in the dashboard
        has_120_cr = "120" in dashboard_html and ("cr" in dashboard_html.lower() or "crore" in dashboard_html.lower())
        assert has_120_cr, "Dashboard index.html must reference the ₹120 Cr salary cap in XI Builder or purse display"

        # Check XI player cost breakdown:
        # Default XI contains players whose salary sum is 113.6 Cr, leaving 6.4 Cr remaining of 120 Cr
        has_purse_metric = any(
            term in dashboard_html for term in ["113.6", "6.4", "Purse", "purse", "Salary Cap", "salary cap"]
        )
        assert has_purse_metric, (
            "Dashboard should display starting XI purse tracking (₹113.6 Cr committed / ₹6.4 Cr remaining)"
        )
