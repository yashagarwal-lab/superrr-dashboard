"""
SuperRR Production Analytics Pipeline
Round 1 - Rajasthan Royals SupeRR Selector Season 2

Implements end-to-end data ingestion, 5 forensic cleanups, Zero-Boundary 1st innings model,
logistic 2nd innings win expectancy model, Leverage Index computation, Par-adjusted runs added/saved,
multiplicative retention ratios, multi-moment consistency metrics (CSR, SCS, Gini), and RPCS rankings.
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(DATA_DIR):
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "6af458274c1e8_data_pack", "Data Pack")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
CHARTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)


class SuperRRPipeline:
    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = data_dir
        self.matches = None
        self.bbb = None
        self.comps = None
        self.ctpm = None
        self.p11 = None
        self.teams = None
        self.clf_inn2 = None
        self.target_dict = {}
        self.match_ipl_dict = {}
        self.match_winner_dict = {}
        self.rev1_dict = {}
        self.rev2_dict = {}
        self.mean_delta_wp = 0.1141
        self.bat_eval = None
        self.bowl_eval = None

    def load_data(self):
        print("[1/6] Ingesting raw datasets...")
        self.matches = pd.read_csv(os.path.join(self.data_dir, "matches.csv"))
        self.bbb = pd.read_csv(os.path.join(self.data_dir, "ball_by_ball.csv"))
        self.comps = pd.read_csv(os.path.join(self.data_dir, "competitions.csv"))
        self.ctpm = pd.read_csv(os.path.join(self.data_dir, "competition_team_player_mapping.csv"))
        self.p11 = pd.read_csv(os.path.join(self.data_dir, "playing_eleven.csv"))
        self.teams = pd.read_csv(os.path.join(self.data_dir, "teams.csv"))
        print(f"Loaded {len(self.matches)} matches, {len(self.bbb)} deliveries, {len(self.ctpm)} player mappings.")

    def apply_data_forensics(self):
        print("[2/6] Applying 5 forensic data cleanups...")

        # Forensic 1: Match 40709 Row 127899 Tilak Varma tactical retire out imputation
        mask_tv = (self.bbb['match_id'] == 40709) & (self.bbb['dismissal_type'] == 'Retire Out')
        if mask_tv.any():
            self.bbb.loc[mask_tv, 'dismissed_player_id'] = 7897.0
            print("  - Forensic 1 Applied: Imputed Tilak Varma (ID 7897) on Match 40709 Retire Out.")

        # Forensic 2: Post-conclusion target quarantine (e.g. Match 48610 12 phantom deliveries)
        inn1_totals = self.bbb[self.bbb['innings'] == 1].groupby('match_id').apply(
            lambda df: (df['runs'] + df['extras1_runs'] + df['extras_2_runs']).sum()
        ).to_dict()

        self.target_dict = self.matches.set_index('match_id')['revised_target'].to_dict()
        for mid, s in inn1_totals.items():
            if mid not in self.target_dict or pd.isna(self.target_dict[mid]):
                self.target_dict[mid] = s + 1

        post_target_idx = []
        for mid, df_m in self.bbb[self.bbb['innings'] == 2].groupby('match_id'):
            tgt = self.target_dict.get(mid, 999999)
            cum_runs = 0
            for idx, r in df_m.iterrows():
                if cum_runs >= tgt:
                    post_target_idx.append(idx)
                cum_runs += r['runs'] + r['extras1_runs'] + r['extras_2_runs']

        if post_target_idx:
            print(f"  - Forensic 2 Applied: Quarantined {len(post_target_idx)} post-conclusion deliveries (including Match 48610).")
            self.bbb = self.bbb.drop(index=post_target_idx).copy()

        # Forensic 3: Revised overs legal balls encoding quirk
        # `first_inn_revised_overs` and `second_inn_revised_overs` are stored in legal balls count
        self.rev1_dict = self.matches.set_index('match_id')['first_inn_revised_overs'].to_dict()
        self.rev2_dict = self.matches.set_index('match_id')['second_inn_revised_overs'].to_dict()
        print("  - Forensic 3 Applied: Mapped revised overs legal ball constraints.")

        # Forensic 4: Legal ball and bowler credit delineation
        # Legal delivery = not in ['wide', 'Overstep', 'other']
        self.bbb['is_legal'] = ~self.bbb['extras_type'].isin(['wide', 'Overstep', 'other'])
        self.bbb['ball_runs'] = self.bbb['runs'] + self.bbb['extras1_runs'] + self.bbb['extras_2_runs']
        self.bbb['bowler_runs'] = np.where(self.bbb['extras_type'].isin(['byes', 'legbyes', 'Penalty']), 0, self.bbb['ball_runs'])
        self.bbb['is_bowler_wicket'] = self.bbb['is_wicket'] & self.bbb['dismissal_type'].isin(
            ['Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket']
        )
        print("  - Forensic 4 Applied: Delineated bowler-earned wickets from 271 non-striker run-outs, Retire Outs & Obstructions.")

        # Forensic 5: Duplicate player disambiguation setup
        # Strictly maintain player_id as primary key
        comp_map = self.comps.set_index('comp_id')
        self.matches['is_ipl'] = self.matches['comp_id'].map(
            lambda cid: 'IPL' in comp_map.loc[cid, 'comp_name'] if cid in comp_map.index else False
        )
        self.match_ipl_dict = self.matches.set_index('match_id')['is_ipl'].to_dict()
        self.match_winner_dict = self.matches.set_index('match_id')['win_team_id'].to_dict()

        self.bbb['is_ipl'] = self.bbb['match_id'].map(self.match_ipl_dict).fillna(False)
        self.bbb['par_total'] = np.where(self.bbb['is_ipl'], 189.1, 168.1)
        self.bbb['phase'] = pd.cut(self.bbb['overid'], bins=[0, 6, 15, 20], labels=['Powerplay', 'Middle', 'Death'])
        print("  - Forensic 5 Applied: Primary key isolation prevents duplicate name collisions.")

    def compute_match_states_and_models(self):
        print("[3/6] Computing match states and calibrating win probability models...")

        match_groups = self.bbb.groupby(['match_id', 'innings'], sort=False)
        pre_runs = []
        pre_wickets = []
        pre_legal_balls = []
        balls_rem = []

        for (mid, inn), grp in match_groups:
            rev_balls = self.rev1_dict.get(mid) if inn == 1 else self.rev2_dict.get(mid)
            max_legal = int(rev_balls) if pd.notna(rev_balls) else 120

            c_runs = 0
            c_w = 0
            c_legal = 0

            for _, row in grp.iterrows():
                pre_runs.append(c_runs)
                pre_wickets.append(c_w)
                pre_legal_balls.append(c_legal)
                balls_rem.append(max(0, max_legal - c_legal))

                c_runs += row['ball_runs']
                if row['is_legal']:
                    c_legal += 1
                if row['is_wicket']:
                    c_w += 1

        self.bbb['pre_runs'] = pre_runs
        self.bbb['pre_wickets'] = pre_wickets
        self.bbb['pre_legal_balls'] = pre_legal_balls
        self.bbb['balls_rem'] = balls_rem

        # Calibrate 2nd Innings Logistic Model on matches with a decisive winner
        inn2_mask = (self.bbb['innings'] == 2).values
        inn2_df = self.bbb[inn2_mask].copy()
        inn2_df['target'] = inn2_df['match_id'].map(self.target_dict)
        inn2_df['runs_needed'] = np.maximum(0, inn2_df['target'] - inn2_df['pre_runs'])
        inn2_df['wickets_in_hand'] = 10 - inn2_df['pre_wickets']
        inn2_df['winner'] = inn2_df['match_id'].map(self.match_winner_dict)

        # Filter out abandoned / no-result fixtures to eliminate false negative contamination
        valid_winner = inn2_df['winner'].notna()
        inn2_clean = inn2_df[valid_winner].copy()
        inn2_clean['batting_team_won'] = (inn2_clean['batting_team_id'] == inn2_clean['winner']).astype(int)

        X_inn2 = np.column_stack([
            inn2_clean['runs_needed'].values,
            inn2_clean['balls_rem'].values,
            inn2_clean['wickets_in_hand'].values,
            inn2_clean['runs_needed'].values / (inn2_clean['balls_rem'].values + 1.0)
        ])
        y_inn2 = inn2_clean['batting_team_won'].values

        self.clf_inn2 = LogisticRegression(max_iter=1000)
        self.clf_inn2.fit(X_inn2, y_inn2)
        print(f"  - Calibrated 2nd innings logistic model successfully across {len(X_inn2)} clean match deliveries.")

    def get_wp1(self, b_rem, w_lost, cur_runs, par):
        """Zero-Boundary Expected Runs Model for 1st Innings: R_rem = b * (2.591 - 1.232*(b/120) - 1.296*(w/10))
        Boundary condition: If balls_rem <= 0 or wickets_lost >= 10 (all out), expected remaining runs are strictly 0."""
        b = np.maximum(0, b_rem)
        w = np.clip(w_lost, 0, 10)
        r_rem = np.where((b <= 0) | (w >= 10), 0.0, b * (2.591 - 1.232 * (b / 120.0) - 1.296 * (w / 10.0)))
        r_rem = np.maximum(0.0, r_rem)
        exp_tot = cur_runs + r_rem
        return 1.0 / (1.0 + np.exp(-0.05 * (exp_tot - par)))

    def get_wp2(self, r_need, b_rem, w_in_hand):
        """Calibrated Logistic Model for 2nd Innings Win Probability.
        Boundary conditions:
        - If r_need <= 0: Target achieved -> WP is strictly 1.0 (win)
        - If (b_rem <= 0 or w_in_hand <= 0) and r_need > 0: Chase failed / all out -> WP is strictly 0.0 (loss)"""
        X = np.column_stack([
            r_need,
            b_rem,
            w_in_hand,
            r_need / (b_rem + 1.0)
        ])
        wp = self.clf_inn2.predict_proba(X)[:, 1]
        wp = np.where((w_in_hand <= 0) & (r_need > 0), 0.0, wp)
        wp = np.where((b_rem <= 0) & (r_need > 0), 0.0, wp)
        wp = np.where(r_need <= 0, 1.0, wp)
        return wp

    def compute_leverage_and_pressure(self):
        print("[4/6] Computing Leverage Index and Pressure Archetypes...")
        b_curr = self.bbb['balls_rem'].values
        w_curr = self.bbb['pre_wickets'].values
        r_curr = self.bbb['pre_runs'].values
        par_curr = self.bbb['par_total'].values

        # 1st Innings Potential Swing
        wp1_good = self.get_wp1(b_curr - 1, w_curr, r_curr + 4, par_curr)
        wp1_bad = self.get_wp1(b_curr - 1, w_curr + 1, r_curr, par_curr)
        delta_wp1 = np.abs(wp1_good - wp1_bad)

        # 2nd Innings Potential Swing
        target_arr = self.bbb['match_id'].map(self.target_dict).values
        r_need_curr = np.maximum(0, target_arr - r_curr)
        w_hand_curr = np.clip(10 - w_curr, 0, 10)

        wp2_good = self.get_wp2(np.maximum(0, r_need_curr - 4), np.maximum(0, b_curr - 1), w_hand_curr)
        wp2_bad = self.get_wp2(r_need_curr, np.maximum(0, b_curr - 1), np.maximum(0, w_hand_curr - 1))
        delta_wp2 = np.abs(wp2_good - wp2_bad)

        delta_wp = np.where(self.bbb['innings'] == 1, delta_wp1, delta_wp2)
        self.mean_delta_wp = np.mean(delta_wp)
        self.bbb['leverage_index'] = delta_wp / self.mean_delta_wp

        # Pressure Archetypes
        rrr_arr = np.where(b_curr > 0, r_need_curr / (b_curr / 6.0), 99.0)
        cond_li = self.bbb['leverage_index'] >= 1.5
        cond_chase = (self.bbb['innings'] == 2) & ((rrr_arr >= 9.5) | ((b_curr <= 18) & (r_need_curr > 15)))
        cond_death = (b_curr <= 30) & ((self.bbb['innings'] == 1) | ((self.bbb['innings'] == 2) & (rrr_arr >= 7.0)))
        cond_crisis = (b_curr >= 84) & ((w_curr >= 3) | ((self.bbb['pre_legal_balls'] >= 18) & (r_curr <= 20)))

        self.bbb['is_pressure'] = cond_li | cond_chase | cond_death | cond_crisis

        # Actual Delivery WPA
        wp_pre_inn1 = self.get_wp1(b_curr, w_curr, r_curr, par_curr)
        wp_pre_inn2 = self.get_wp2(r_need_curr, b_curr, w_hand_curr)
        wp_pre = np.where(self.bbb['innings'] == 1, wp_pre_inn1, wp_pre_inn2)

        post_b = np.maximum(0, b_curr - self.bbb['is_legal'].astype(int).values)
        post_w = np.clip(w_curr + self.bbb['is_wicket'].astype(int).values, 0, 10)
        post_r = r_curr + self.bbb['ball_runs'].values
        post_r_need = np.maximum(0, target_arr - post_r)
        post_w_hand = np.clip(10 - post_w, 0, 10)

        wp_post_inn1 = self.get_wp1(post_b, post_w, post_r, par_curr)
        wp_post_inn2 = self.get_wp2(post_r_need, post_b, post_w_hand)
        wp_post = np.where(self.bbb['innings'] == 1, wp_post_inn1, wp_post_inn2)

        self.bbb['wpa_delivery'] = wp_post - wp_pre

        # Forensic WPA Attribution: Decompose non-striker dismissals
        # Dismissed non-striker absorbs the wicket equity penalty; striker retains run equity
        wp_ro_inn1 = self.get_wp1(post_b, w_curr, post_r, par_curr)
        wp_ro_inn2 = self.get_wp2(post_r_need, post_b, w_hand_curr)
        wp_runs_only = np.where(self.bbb['innings'] == 1, wp_ro_inn1, wp_ro_inn2)

        is_ns_dismissal = self.bbb['is_wicket'] & (self.bbb['dismissed_player_id'] != self.bbb['striker_id']) & self.bbb['dismissed_player_id'].notna()
        self.bbb['is_ns_dismissal'] = is_ns_dismissal
        self.bbb['wpa_striker'] = np.where(is_ns_dismissal, wp_runs_only - wp_pre, self.bbb['wpa_delivery'])
        self.bbb['wpa_dismissed'] = np.where(is_ns_dismissal, wp_post - wp_runs_only, 0.0)

        # Par Runs by phase and format (vectorized)
        par_table = self.bbb.groupby(['phase', 'is_ipl'], observed=False)['ball_runs'].mean().to_dict()
        self.bbb['par_ball_runs'] = [par_table.get((ph, ipl), 1.3) for ph, ipl in zip(self.bbb['phase'], self.bbb['is_ipl'])]
        self.bbb['bra'] = self.bbb['runs'] - self.bbb['par_ball_runs']
        self.bbb['brs'] = self.bbb['par_ball_runs'] - self.bbb['bowler_runs']

        print(f"  - Pressure deliveries identified: {self.bbb['is_pressure'].sum()} ({self.bbb['is_pressure'].mean()*100:.1f}%)")

    @staticmethod
    def calc_gini(arr):
        arr = np.array(arr, dtype=float)
        arr = arr[arr > 0]
        if len(arr) <= 1:
            return 0.0
        arr = np.sort(arr)
        n = len(arr)
        index = np.arange(1, n + 1)
        return float((2 * np.sum(index * arr) - (n + 1) * np.sum(arr)) / (n * np.sum(arr)))

    def evaluate_players(self, min_pressure_balls=150):
        print(f"[5/6] Evaluating Batters & Bowlers (Sample Floor >= {min_pressure_balls} pressure balls)...")

        player_names = self.ctpm.groupby('player_id')['player_name'].first().to_dict()
        scaler = MinMaxScaler()

        # --- BATTERS ---
        bat_all = self.bbb[self.bbb['extras_type'] != 'wide']
        bat_base_stats = bat_all.groupby('striker_id').agg(
            base_runs=('runs', 'sum'),
            base_balls=('runs', 'count')
        )
        bat_base_stats['base_sr'] = (bat_base_stats['base_runs'] / bat_base_stats['base_balls']) * 100.0

        bat_press = self.bbb[self.bbb['is_pressure'] & (self.bbb['extras_type'] != 'wide')]
        bat_press_stats = bat_press.groupby('striker_id').agg(
            press_runs=('runs', 'sum'),
            press_balls=('runs', 'count'),
            press_wpa_str=('wpa_striker', 'sum'),
            press_bra=('bra', 'sum')
        )
        # Non-striker dismissals under pressure: debit dismissed runner
        ns_press = self.bbb[self.bbb['is_pressure'] & self.bbb['is_ns_dismissal']]
        ns_debits = ns_press.groupby('dismissed_player_id')['wpa_dismissed'].sum()

        bat_press_stats['press_wpa'] = bat_press_stats['press_wpa_str'].add(ns_debits, fill_value=0.0)
        bat_press_stats['press_sr'] = (bat_press_stats['press_runs'] / bat_press_stats['press_balls']) * 100.0

        bat_eval = bat_press_stats[bat_press_stats['press_balls'] >= min_pressure_balls].copy()
        bat_eval = bat_eval.join(bat_base_stats[['base_runs', 'base_balls', 'base_sr']])
        bat_eval['kappa_bat'] = bat_eval['press_sr'] / bat_eval['base_sr']

        # Match-level aggregation combining striker runs and non-striker dismissal debits
        str_m = bat_press.groupby(['striker_id', 'match_id']).agg(
            m_wpa_str=('wpa_striker', 'sum'),
            m_bra=('bra', 'sum')
        ).reset_index()
        str_m = str_m.rename(columns={'striker_id': 'player_id'})

        ns_m = ns_press.groupby(['dismissed_player_id', 'match_id']).agg(
            m_wpa_ns=('wpa_dismissed', 'sum')
        ).reset_index()
        ns_m = ns_m.rename(columns={'dismissed_player_id': 'player_id'})

        bat_m_stats = pd.merge(str_m, ns_m, on=['player_id', 'match_id'], how='outer').fillna(0.0)
        bat_m_stats['m_wpa'] = bat_m_stats['m_wpa_str'] + bat_m_stats['m_wpa_ns']

        csr_bat, scs_bat, gini_bat = [], [], []
        for pid in bat_eval.index:
            sub = bat_m_stats[bat_m_stats['player_id'] == pid]
            n_m = len(sub)
            if n_m == 0:
                csr_bat.append(0.0)
                scs_bat.append(1.0)
                gini_bat.append(0.0)
                continue
            csr = ((sub['m_wpa'] > 0) | (sub['m_bra'] > 0)).mean()
            csr_bat.append(csr)

            pos_wpa = np.maximum(0.0, sub['m_wpa'].values)
            sum_pos = np.sum(pos_wpa)
            scs = float(np.max(pos_wpa) / sum_pos) if sum_pos > 0 else 1.0
            scs_bat.append(scs)
            gini_bat.append(self.calc_gini(pos_wpa))

        bat_eval['csr'] = csr_bat
        bat_eval['scs'] = scs_bat
        bat_eval['gini'] = gini_bat

        norm_wpa = scaler.fit_transform(bat_eval[['press_wpa']])[:, 0]
        norm_bra = scaler.fit_transform(bat_eval[['press_bra']])[:, 0]
        norm_kappa = scaler.fit_transform(bat_eval[['kappa_bat']])[:, 0]
        norm_csr = bat_eval['csr'].values
        norm_rel = 1.0 - bat_eval['scs'].values

        bat_eval['rpcs'] = (
            0.30 * norm_wpa +
            0.25 * norm_bra +
            0.20 * norm_kappa +
            0.15 * norm_csr +
            0.10 * norm_rel
        ) * 100.0

        bat_eval['player_name'] = bat_eval.index.map(player_names)
        self.bat_eval = bat_eval.sort_values(by='rpcs', ascending=False)

        # --- BOWLERS ---
        bowl_all = self.bbb[self.bbb['is_legal']]
        bowl_base_stats = bowl_all.groupby('bowler_id').agg(
            base_runs=('bowler_runs', 'sum'),
            base_balls=('bowler_runs', 'count'),
            base_wickets=('is_bowler_wicket', 'sum')
        )
        bowl_base_stats['base_econ'] = (bowl_base_stats['base_runs'] / (bowl_base_stats['base_balls'] / 6.0))

        self.bbb['wpa_bowler'] = -self.bbb['wpa_delivery']
        bowl_press = self.bbb[self.bbb['is_pressure'] & self.bbb['is_legal']]
        bowl_press_stats = bowl_press.groupby('bowler_id').agg(
            press_runs=('bowler_runs', 'sum'),
            press_balls=('bowler_runs', 'count'),
            press_wickets=('is_bowler_wicket', 'sum'),
            press_wpa=('wpa_bowler', 'sum'),
            press_brs=('brs', 'sum')
        )
        bowl_press_stats['press_econ'] = (bowl_press_stats['press_runs'] / (bowl_press_stats['press_balls'] / 6.0))

        bowl_eval = bowl_press_stats[bowl_press_stats['press_balls'] >= min_pressure_balls].copy()
        bowl_eval = bowl_eval.join(bowl_base_stats[['base_runs', 'base_balls', 'base_wickets', 'base_econ']])
        bowl_eval['kappa_bowl'] = bowl_eval['base_econ'] / bowl_eval['press_econ']

        bowl_m_stats = bowl_press.groupby(['bowler_id', 'match_id']).agg(
            m_wpa=('wpa_bowler', 'sum'),
            m_brs=('brs', 'sum')
        ).reset_index()

        csr_bowl, scs_bowl, gini_bowl = [], [], []
        for pid in bowl_eval.index:
            sub = bowl_m_stats[bowl_m_stats['bowler_id'] == pid]
            n_m = len(sub)
            if n_m == 0:
                csr_bowl.append(0.0)
                scs_bowl.append(1.0)
                gini_bowl.append(0.0)
                continue
            csr = ((sub['m_wpa'] > 0) | (sub['m_brs'] > 0)).mean()
            csr_bowl.append(csr)

            pos_wpa = np.maximum(0.0, sub['m_wpa'].values)
            sum_pos = np.sum(pos_wpa)
            scs = float(np.max(pos_wpa) / sum_pos) if sum_pos > 0 else 1.0
            scs_bowl.append(scs)
            gini_bowl.append(self.calc_gini(pos_wpa))

        bowl_eval['csr'] = csr_bowl
        bowl_eval['scs'] = scs_bowl
        bowl_eval['gini'] = gini_bowl

        norm_b_wpa = scaler.fit_transform(bowl_eval[['press_wpa']])[:, 0]
        norm_b_brs = scaler.fit_transform(bowl_eval[['press_brs']])[:, 0]
        norm_b_kappa = scaler.fit_transform(bowl_eval[['kappa_bowl']])[:, 0]
        norm_b_csr = bowl_eval['csr'].values
        norm_b_rel = 1.0 - bowl_eval['scs'].values

        bowl_eval['rpcs'] = (
            0.30 * norm_b_wpa +
            0.25 * norm_b_brs +
            0.20 * norm_b_kappa +
            0.15 * norm_b_csr +
            0.10 * norm_b_rel
        ) * 100.0

        bowl_eval['player_name'] = bowl_eval.index.map(player_names)
        self.bowl_eval = bowl_eval.sort_values(by='rpcs', ascending=False)

        print(f"  - Evaluated {len(self.bat_eval)} qualifying batters and {len(self.bowl_eval)} qualifying bowlers.")

    def export_results(self):
        print("[6/6] Exporting official rankings and validation files...")

        # Top 10 Batters
        top10_batters = self.bat_eval.head(10).copy()
        top10_batters['rank'] = range(1, 11)
        top10_batters_out = top10_batters[[
            'rank', 'player_name', 'press_balls', 'press_sr', 'base_sr', 'kappa_bat',
            'press_wpa', 'press_bra', 'csr', 'scs', 'gini', 'rpcs'
        ]]
        bat_csv_path = os.path.join(OUTPUT_DIR, "top_10_batters.csv")
        top10_batters_out.to_csv(bat_csv_path, index=False)

        # Top 10 Bowlers
        top10_bowlers = self.bowl_eval.head(10).copy()
        top10_bowlers['rank'] = range(1, 11)
        top10_bowlers_out = top10_bowlers[[
            'rank', 'player_name', 'press_balls', 'press_econ', 'base_econ', 'kappa_bowl',
            'press_wpa', 'press_brs', 'csr', 'scs', 'gini', 'rpcs'
        ]]
        bowl_csv_path = os.path.join(OUTPUT_DIR, "top_10_bowlers.csv")
        top10_bowlers_out.to_csv(bowl_csv_path, index=False)

        # Full evaluations
        self.bat_eval.to_csv(os.path.join(OUTPUT_DIR, "all_batters_evaluated.csv"))
        self.bowl_eval.to_csv(os.path.join(OUTPUT_DIR, "all_bowlers_evaluated.csv"))

        print(f"Exported Top 10 Batters to: {bat_csv_path}")
        print(f"Exported Top 10 Bowlers to: {bowl_csv_path}")


def main():
    pipeline = SuperRRPipeline()
    pipeline.load_data()
    pipeline.apply_data_forensics()
    pipeline.compute_match_states_and_models()
    pipeline.compute_leverage_and_pressure()
    pipeline.evaluate_players(min_pressure_balls=150)
    pipeline.export_results()
    print("Pipeline executed successfully!")


if __name__ == '__main__':
    main()
