import os
import pytest
import numpy as np
import pandas as pd
from pipeline import SuperRRPipeline, DATA_DIR

@pytest.fixture(scope="module")
def pipeline_instance():
    p = SuperRRPipeline(DATA_DIR)
    p.load_data()
    p.apply_data_forensics()
    p.compute_match_states_and_models()
    p.compute_leverage_and_pressure()
    p.evaluate_players(min_pressure_balls=150)
    return p

def test_forensics_tilak_varma(pipeline_instance):
    """Test that Row 127899 in Match 40709 has dismissed_player_id imputed to 7897 (Tilak Varma)."""
    # Note: Row index might be modified if rows dropped, so check by match_id and overid
    tv_row = pipeline_instance.bbb[
        (pipeline_instance.bbb['match_id'] == 40709) &
        (pipeline_instance.bbb['dismissal_type'] == 'Retire Out')
    ]
    assert len(tv_row) == 1
    assert tv_row.iloc[0]['dismissed_player_id'] == 7897.0
    assert tv_row.iloc[0]['is_wicket'] == True
    # Bowler should not get credit for retire out
    assert tv_row.iloc[0]['is_bowler_wicket'] == False

def test_forensics_non_striker_runouts(pipeline_instance):
    """Test that all 271 non-striker run outs have bowler credit == False."""
    ns_ro = pipeline_instance.bbb[
        (pipeline_instance.bbb['dismissal_type'] == 'RunOut') &
        (pipeline_instance.bbb['dismissed_player_id'] == pipeline_instance.bbb['non_striker_id'])
    ]
    assert len(ns_ro) == 271
    assert (ns_ro['is_bowler_wicket'] == False).all()

def test_zero_boundary_model(pipeline_instance):
    """Test that 1st innings model produces exactly 0 runs remaining when balls remaining is 0 OR when wickets lost >= 10 (all out)."""
    # 1. Zero legal balls remaining
    for w in range(11):
        assert pipeline_instance.get_wp1(b_rem=0, w_lost=w, cur_runs=150, par=189.1) == pytest.approx(
            1.0 / (1.0 + np.exp(-0.05 * (150 - 189.1))), rel=1e-5
        )
    # 2. All-out condition (10 wickets lost) with positive balls remaining
    for b in [6, 12, 30, 60, 120]:
        assert pipeline_instance.get_wp1(b_rem=b, w_lost=10, cur_runs=150, par=189.1) == pytest.approx(
            1.0 / (1.0 + np.exp(-0.05 * (150 - 189.1))), rel=1e-5
        )

def test_chase_boundary_conditions(pipeline_instance):
    """Test 2nd innings win probability boundary invariants (target achieved vs chase failed)."""
    # Target reached (r_need <= 0) must be 1.0 regardless of balls or wickets
    assert pipeline_instance.get_wp2(np.array([0]), np.array([0]), np.array([0]))[0] == 1.0
    assert pipeline_instance.get_wp2(np.array([0]), np.array([12]), np.array([5]))[0] == 1.0
    assert pipeline_instance.get_wp2(np.array([-2]), np.array([0]), np.array([0]))[0] == 1.0

    # Chase exhausted / all out while runs still needed must be strictly 0.0
    assert pipeline_instance.get_wp2(np.array([1]), np.array([0]), np.array([5]))[0] == 0.0
    assert pipeline_instance.get_wp2(np.array([10]), np.array([12]), np.array([0]))[0] == 0.0

def test_forensics_non_striker_wpa_attribution(pipeline_instance):
    """Test that non-striker dismissals properly attribute wicket debits to the dismissed player rather than the striker."""
    # Look at Match 40709 Row 127899 (Tilak Varma retire out, striker Hardik Pandya)
    tv_row = pipeline_instance.bbb[
        (pipeline_instance.bbb['match_id'] == 40709) &
        (pipeline_instance.bbb['dismissal_type'] == 'Retire Out')
    ].iloc[0]
    assert tv_row['dismissed_player_id'] == 7897.0
    assert tv_row['striker_id'] == 3330 # Hardik Pandya
    # Hardik Pandya (striker) faced 0 runs scored ball, striker WPA should not absorb the wicket loss
    assert tv_row['wpa_dismissed'] < 0.0 # Tilak Varma absorbs the negative wicket debit
    # Delivery WPA perfectly equals sum of striker and dismissed runner WPA
    assert tv_row['wpa_delivery'] == pytest.approx(tv_row['wpa_striker'] + tv_row['wpa_dismissed'], rel=1e-5)

def test_quarantine_match_48610(pipeline_instance):
    """Test that all 12 post-conclusion phantom deliveries in Match 48610 were quarantined."""
    m48610 = pipeline_instance.bbb[(pipeline_instance.bbb['match_id'] == 48610) & (pipeline_instance.bbb['innings'] == 2)]
    # Target was 115, reached at over 13 ball 6
    assert (m48610['overid'] <= 13).all()
    # Ghost dismissal of Phil Salt off Dasun Shanaka in over 15 was purged
    salt_dismissals = m48610[(m48610['striker_name'] == 'Phil Salt') & m48610['is_wicket']]
    assert len(salt_dismissals) == 0

def test_leverage_index_calibration(pipeline_instance):
    """Test that average leverage index is close to 1.0 and non-negative."""
    li = pipeline_instance.bbb['leverage_index'].values
    assert (li >= 0).all()
    assert np.isclose(np.mean(li), 1.0, atol=0.05)

def test_sample_size_floor(pipeline_instance):
    """Test that every evaluated player satisfies >= 150 pressure balls floor."""
    assert (pipeline_instance.bat_eval['press_balls'] >= 150).all()
    assert (pipeline_instance.bowl_eval['press_balls'] >= 150).all()

def test_multi_moment_consistency_bounds(pipeline_instance):
    """Test CSR, SCS, and Gini are within valid mathematical bounds [0, 1]."""
    for df in [pipeline_instance.bat_eval, pipeline_instance.bowl_eval]:
        assert (df['csr'] >= 0.0).all() and (df['csr'] <= 1.0).all()
        assert (df['scs'] >= 0.0).all() and (df['scs'] <= 1.0).all()
        assert (df['gini'] >= 0.0).all() and (df['gini'] <= 1.0).all()

def test_top_10_batters_unstop_match(pipeline_instance):
    """Test that Top 10 Batters match exactly with CTPM dropdown strings."""
    top10_batters = pipeline_instance.bat_eval.head(10)['player_name'].tolist()
    ctpm_names = set(pipeline_instance.ctpm['player_name'].unique())
    assert len(top10_batters) == 10
    assert len(set(top10_batters)) == 10 # No duplicates
    for name in top10_batters:
        assert name in ctpm_names, f"Batter {name} not found in CTPM!"

def test_top_10_bowlers_unstop_match(pipeline_instance):
    """Test that Top 10 Bowlers match exactly with CTPM dropdown strings."""
    top10_bowlers = pipeline_instance.bowl_eval.head(10)['player_name'].tolist()
    ctpm_names = set(pipeline_instance.ctpm['player_name'].unique())
    assert len(top10_bowlers) == 10
    assert len(set(top10_bowlers)) == 10 # No duplicates
    for name in top10_bowlers:
        assert name in ctpm_names, f"Bowler {name} not found in CTPM!"

def test_multiplicative_retention_ratio(pipeline_instance):
    """Test that multiplicative retention ratio kappa eliminates baseline penalty."""
    # Check that kappa is defined and positive
    assert (pipeline_instance.bat_eval['kappa_bat'] > 0).all()
    assert (pipeline_instance.bowl_eval['kappa_bowl'] > 0).all()

def test_rank_stability_across_floors(pipeline_instance):
    """Test that Top 5 Batters and Bowlers remain robust and invariant across sample size floors (150 vs 200)."""
    p = pipeline_instance
    top5_bat_150 = p.bat_eval.head(5)['player_name'].tolist()
    top5_bowl_150 = p.bowl_eval.head(5)['player_name'].tolist()

    # Re-evaluate with floor = 200
    p.evaluate_players(min_pressure_balls=200)
    top5_bat_200 = p.bat_eval.head(5)['player_name'].tolist()
    top5_bowl_200 = p.bowl_eval.head(5)['player_name'].tolist()

    # Reset back to 150 for pipeline integrity
    p.evaluate_players(min_pressure_balls=150)

    # Batters maintain exact 1:1 top-5 ordering; bowlers maintain exact identical top-5 set
    assert top5_bat_150 == top5_bat_200
    assert set(top5_bowl_150) == set(top5_bowl_200)
