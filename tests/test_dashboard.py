import json
import os
import subprocess
from html.parser import HTMLParser

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(ROOT_DIR, "dashboard", "data.json")
HTML_PATH = os.path.join(ROOT_DIR, "dashboard", "index.html")

def test_data_json_counts():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        d = json.load(f)
    assert len(d['batters']) == 198
    assert len(d['bowlers']) == 196

def test_kuldeep_yadav_trade():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        d = json.load(f)
    for cat in ['batters', 'bowlers']:
        p = next(x for x in d[cat] if x['name'] == 'Kuldeep Yadav')
        assert p['team_2026'] == 'Lucknow Super Giants'
        assert p['badge_type'] == 'traded'
        assert p['badge_label'] == 'TRADED TO LSG (LOCKED)'
        assert 'Rishabh Pant' in p['trade_notes']

def test_taskin_ahmed_free_agent():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        d = json.load(f)
    taskin = next(x for x in d['bowlers'] if x['name'] == 'Taskin Ahmed')
    assert taskin['team_2026'] == 'RELEASED (Free Agent)'
    assert taskin['badge_type'] == 'free_agent'
    assert taskin['badge_label'] == 'UNSOLD FREE AGENT (AVAILABLE)'
    assert taskin['auction_status'] == 'Confirmed Released / Free Agent'
    assert '75L' in taskin['trade_notes']

def test_pakistani_players_ineligible():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        d = json.load(f)
    pak_count = 0
    for cat in ['batters', 'bowlers']:
        for p in d[cat]:
            if p.get('country') == 'Pakistan':
                pak_count += 1
                assert p['eligibility'] == 'BCCI Ineligible'
                assert p['auction_status'] == 'BCCI Ineligible / Non-IPL'
                assert p['badge_type'] == 'ineligible'
                assert p['badge_label'] == 'BCCI INELIGIBLE / NON-IPL'
    assert pak_count == 27

def test_watchlist_head_pathirana():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        d = json.load(f)
    head = next(x for x in d['batters'] if x['name'] == 'Travis Head')
    assert head['badge_type'] == 'release_watch'
    assert head['badge_label'] == 'WORKLOAD OPT-OUT'
    assert 'opt out' in head['trade_notes']

    pathirana = next(x for x in d['bowlers'] if x['name'] == 'Matheesha Pathirana')
    assert pathirana['badge_type'] == 'release_watch'
    assert pathirana['badge_label'] == 'RELEASE WATCH (₹18 CR)'
    assert '18.0 Cr' in pathirana['trade_notes']

def test_core_untouchables():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        d = json.load(f)
    names = ['Virat Kohli', 'Suryakumar Yadav', 'Phil Salt', 'Tim David', 'Prabhsimran Singh',
             'Sunil Narine', 'Mitchell Santner', 'Jasprit Bumrah', 'Rashid Khan', 'Jos Buttler', 'Abhishek Sharma']
    for name in names:
        found = False
        for cat in ['batters', 'bowlers']:
            for p in d[cat]:
                if p['name'] == name:
                    found = True
                    assert p['badge_type'] == 'retention'
                    assert p['badge_label'] == 'UNTOUCHABLE CORE'
                    assert p['auction_status'] == 'Franchise Core / Untouchable Retention'
                    if name == 'Sunil Narine':
                        assert p['country'] == 'West Indies'
        assert found

def test_rr_core_retentions():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        d = json.load(f)
    jaiswal = next(x for x in d['batters'] if x['name'] == 'Yashasvi Jaiswal')
    assert jaiswal['badge_type'] == 'rr_core'
    assert 'trade inquiries' in jaiswal['trade_notes']

    sooryavanshi = next(x for x in d['batters'] if x['name'] == 'Vaibhav Sooryavanshi')
    assert sooryavanshi['badge_type'] == 'rr_core'
    assert 'Orange Cap' in sooryavanshi['trade_notes']

def test_dual_role_synchronization():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        d = json.load(f)
    batters_dict = {p['name']: p for p in d['batters']}
    bowlers_dict = {p['name']: p for p in d['bowlers']}
    shared = set(batters_dict.keys()).intersection(set(bowlers_dict.keys()))
    assert len(shared) == 48
    for name in shared:
        b = batters_dict[name]
        bw = bowlers_dict[name]
        for key in ['country', 'team_2026', 'eligibility', 'auction_status', 'badge_type', 'badge_label', 'avail_type', 'tag', 'category', 'status', 'trade_notes']:
            assert b[key] == bw[key], f"Mismatch for {name} on {key}"

def test_html_structure_and_styling():
    assert os.path.exists(HTML_PATH)
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # HTML parsing check
    class Parser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.count = 0
        def handle_starttag(self, tag, attrs):
            self.count += 1
    p = Parser()
    p.feed(html)
    assert p.count > 300

    # Status badges
    assert 'badge-ineligible' in html
    assert 'row-ineligible' in html
    assert 'badge-free-agent' in html
    assert 'badge-traded' in html
    assert 'badge-watchlist' in html
    assert 'badge-retention' in html
    assert 'badge-rr-core' in html

    # Status labels
    assert 'BCCI INELIGIBLE / NON-IPL' in html
    assert 'UNSOLD FREE AGENT (AVAILABLE)' in html
    assert 'TRADED TO LSG (LOCKED)' in html
    assert 'WORKLOAD OPT-OUT' in html
    assert 'RELEASE WATCH (₹18 CR)' in html
    assert 'UNTOUCHABLE CORE' in html
    assert 'RR CORE / RETAINED' in html

    # Purse tracker
    assert '₹120.00 Cr' in html
    assert '₹113.60 Cr' in html
    assert '₹6.40 Cr' in html

    # Clean styling
    assert 'tabular-nums' in html
    assert 'rgba(234, 26, 142, 0.4)' not in html
    assert '🏆 Unstop Dropdowns' not in html

def test_franchise_cornerstones_not_auction_targets():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        d = json.load(f)

    # 1. Rohit Sharma (Mumbai Indians Icon)
    rohit = next(x for x in d['batters'] if x['name'] == 'Rohit Sharma')
    assert rohit['badge_type'] == 'retention'
    assert rohit['badge_label'] == 'UNTOUCHABLE CORE'
    assert rohit['team_2026'] == 'Mumbai Indians'
    assert 'Mumbai Indians icon' in rohit['trade_notes']
    assert rohit['auction_status'] == 'Franchise Core / Untouchable Retention'

    # 2. Hardik Pandya (MI Captain - Traded)
    hardik = next(x for x in d['bowlers'] if x['name'] == 'Hardik Pandya')
    assert hardik['badge_type'] == 'traded'
    assert hardik['badge_label'] == 'TRADED TO MI (LOCKED)'
    assert hardik['team_2026'] == 'Mumbai Indians'
    assert 'marquee trade' in hardik['trade_notes']

    # 3. Arshdeep Singh (PBKS ₹18 Cr RTM)
    arshdeep = next(x for x in d['bowlers'] if x['name'] == 'Arshdeep Singh')
    assert arshdeep['badge_type'] == 'retention'
    assert arshdeep['badge_label'] == 'UNTOUCHABLE CORE'
    assert arshdeep['team_2026'] == 'Punjab Kings'
    assert '18 Cr' in arshdeep['trade_notes']

    # 4. Mohammed Shami (Contracted Spearhead)
    shami = next(x for x in d['bowlers'] if x['name'] == 'Mohammed Shami')
    assert shami['badge_type'] == 'retention'
    assert shami['badge_label'] == 'UNTOUCHABLE CORE'
    assert 'Premier Indian pace spearhead' in shami['trade_notes']

    # 5. Shubman Gill (GT Captain)
    gill = next(x for x in d['batters'] if x['name'] == 'Shubman Gill')
    assert gill['badge_type'] == 'retention'
    assert gill['badge_label'] == 'UNTOUCHABLE CORE'
    assert gill['team_2026'] == 'Gujarat Titans'

def test_auction_board_strict_exclusion():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        d = json.load(f)

    all_players = d['batters'] + d['bowlers']
    actionable_targets = [
        p for p in all_players
        if p.get('badge_type') not in ['retention', 'ineligible', 'rr_core', 'traded']
    ]

    disallowed_names = [
        'Rohit Sharma', 'Hardik Pandya', 'Arshdeep Singh', 'Mohammed Shami',
        'Shubman Gill', 'Virat Kohli', 'Jasprit Bumrah', 'Suryakumar Yadav',
        'Sufiyan Muqeem', 'Yashasvi Jaiswal', 'Nicholas Pooran', 'Heinrich Klaasen'
    ]

    for name in disallowed_names:
        assert not any(p['name'] == name for p in actionable_targets), f"{name} should NOT be in auction board!"

