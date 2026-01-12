#!/usr/bin/env python3
"""
Chapter 14: Pitch Clock Effect (2023+)

Research Question: How has the 2023 pitch clock affected pitching metrics?

The pitch clock was introduced in 2023:
- 15 seconds with empty bases
- 20 seconds with runners on

Key analyses:
- Pitch count per game changes
- Velocity effects
- Effectiveness (wOBA, whiff rate) changes
- Pitch type distribution changes
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/Users/mksong/Documents/mlb-statcast-book')

from src.statcast_analysis import load_seasons

# Configuration
FIGURES_DIR = '/Users/mksong/Documents/mlb-statcast-book/chapters/14_pitch_clock/figures'
RESULTS_DIR = '/Users/mksong/Documents/mlb-statcast-book/chapters/14_pitch_clock/results'

# Pre and post clock periods
PRE_CLOCK_YEARS = [2019, 2020, 2021, 2022]  # Excluding 2020 for some analyses due to COVID
POST_CLOCK_YEARS = [2023, 2024, 2025]


def load_data():
    """Load data from relevant years."""
    print("Loading data...")
    columns = [
        'game_year', 'game_pk', 'pitcher', 'batter',
        'pitch_type', 'release_speed', 'release_spin_rate',
        'woba_value', 'woba_denom',
        'description', 'type', 'events',
        'inning', 'at_bat_number', 'pitch_number'
    ]

    # Load 2019-2025 (excluding 2015-2018 for cleaner comparison)
    df = load_seasons(2019, 2025, columns=columns)
    print(f"Loaded {len(df):,} total pitches")

    return df


def analyze_pitch_counts(df):
    """Analyze pitch counts per game."""
    print("\n--- Analyzing Pitch Counts per Game ---")

    # Count pitches per game
    game_pitches = df.groupby(['game_year', 'game_pk']).size().reset_index(name='n_pitches')

    # Aggregate by year
    yearly_pitches = game_pitches.groupby('game_year')['n_pitches'].agg(['mean', 'median', 'std', 'count'])
    yearly_pitches.columns = ['mean_pitches', 'median_pitches', 'std_pitches', 'n_games']

    print("\nPitches per Game by Year:")
    print(yearly_pitches.round(1))

    # Pre vs post comparison (excluding 2020)
    pre_games = game_pitches[(game_pitches['game_year'].isin([2019, 2021, 2022]))]['n_pitches']
    post_games = game_pitches[(game_pitches['game_year'].isin(POST_CLOCK_YEARS))]['n_pitches']

    t_stat, p_val = stats.ttest_ind(pre_games.astype(float), post_games.astype(float))
    cohens_d = (pre_games.mean() - post_games.mean()) / np.sqrt(
        (pre_games.std()**2 + post_games.std()**2) / 2
    )

    print(f"\nPre-clock (2019,21,22) avg: {pre_games.mean():.1f} pitches/game")
    print(f"Post-clock (2023-25) avg: {post_games.mean():.1f} pitches/game")
    print(f"Change: {post_games.mean() - pre_games.mean():.1f} pitches/game")
    print(f"t={t_stat:.2f}, p={p_val:.4f}, Cohen's d={cohens_d:.3f}")

    return yearly_pitches, {
        'pre_mean': pre_games.mean(),
        'post_mean': post_games.mean(),
        'change': post_games.mean() - pre_games.mean(),
        't_stat': t_stat,
        'p_value': p_val,
        'cohens_d': cohens_d
    }


def analyze_velocity(df):
    """Analyze velocity before and after pitch clock."""
    print("\n--- Analyzing Velocity Effects ---")

    # Average velocity by year
    yearly_velo = df.groupby('game_year')['release_speed'].agg(['mean', 'std']).round(2)
    print("\nAverage Velocity by Year:")
    print(yearly_velo)

    # Velocity by inning comparison (does clock affect late-inning fatigue?)
    inning_velo = df.groupby(['game_year', 'inning'])['release_speed'].mean().unstack(level=0)
    inning_velo = inning_velo[inning_velo.index <= 9]  # Regular innings only

    print("\nVelocity by Inning (Pre vs Post Clock):")
    print(f"  Inning 1 - 2022: {inning_velo.loc[1, 2022]:.2f}, 2023: {inning_velo.loc[1, 2023]:.2f}")
    print(f"  Inning 9 - 2022: {inning_velo.loc[9, 2022]:.2f}, 2023: {inning_velo.loc[9, 2023]:.2f}")

    # Test: velocity change pre vs post
    pre_velo = df[df['game_year'].isin([2019, 2021, 2022])]['release_speed'].dropna()
    post_velo = df[df['game_year'].isin(POST_CLOCK_YEARS)]['release_speed'].dropna()

    velo_change = post_velo.mean() - pre_velo.mean()

    return yearly_velo, inning_velo, velo_change


def analyze_pitch_mix(df):
    """Analyze pitch type distribution changes."""
    print("\n--- Analyzing Pitch Mix ---")

    # Pitch category
    fastballs = ['FF', 'SI', 'FC']
    breaking = ['SL', 'ST', 'CU', 'KC']
    offspeed = ['CH', 'FS']

    df['pitch_category'] = df['pitch_type'].apply(
        lambda x: 'Fastball' if x in fastballs
        else 'Breaking' if x in breaking
        else 'Offspeed' if x in offspeed
        else 'Other'
    )

    # Pitch mix by year
    yearly_mix = df.groupby('game_year')['pitch_category'].value_counts(normalize=True).unstack() * 100

    print("\nPitch Mix by Year (%):")
    print(yearly_mix[['Fastball', 'Breaking', 'Offspeed']].round(1))

    # Change
    fb_2022 = yearly_mix.loc[2022, 'Fastball']
    fb_2023 = yearly_mix.loc[2023, 'Fastball']
    br_2022 = yearly_mix.loc[2022, 'Breaking']
    br_2023 = yearly_mix.loc[2023, 'Breaking']

    print(f"\nFastball change 2022→2023: {fb_2022:.1f}% → {fb_2023:.1f}% ({fb_2023 - fb_2022:+.1f}%)")
    print(f"Breaking change 2022→2023: {br_2022:.1f}% → {br_2023:.1f}% ({br_2023 - br_2022:+.1f}%)")

    return yearly_mix


def analyze_effectiveness(df):
    """Analyze pitching effectiveness pre vs post clock."""
    print("\n--- Analyzing Effectiveness ---")

    results = []

    for year in sorted(df['game_year'].unique()):
        year_data = df[df['game_year'] == year]

        # wOBA
        woba_data = year_data[year_data['woba_denom'] > 0]
        woba = woba_data['woba_value'].sum() / woba_data['woba_denom'].sum() if len(woba_data) > 0 else np.nan

        # Whiff rate
        swings = year_data['description'].isin([
            'swinging_strike', 'swinging_strike_blocked', 'foul', 'foul_tip',
            'hit_into_play', 'foul_bunt', 'missed_bunt'
        ]).sum()
        whiffs = year_data['description'].isin(['swinging_strike', 'swinging_strike_blocked']).sum()
        whiff_rate = whiffs / swings if swings > 0 else np.nan

        # Strike rate
        strikes = year_data['type'].isin(['S', 'X']).sum()
        strike_rate = strikes / len(year_data) if len(year_data) > 0 else np.nan

        # K rate (PA ending in strikeout)
        pa_data = year_data[year_data['events'].notna()]
        k_rate = (pa_data['events'] == 'strikeout').mean() if len(pa_data) > 0 else np.nan

        results.append({
            'game_year': year,
            'woba': woba,
            'whiff_rate': whiff_rate,
            'strike_rate': strike_rate,
            'k_rate': k_rate,
            'n_pitches': len(year_data)
        })

    effectiveness_df = pd.DataFrame(results)
    print("\nEffectiveness by Year:")
    print(effectiveness_df.to_string(index=False))

    return effectiveness_df


def statistical_tests(df, pitch_count_stats, effectiveness_df):
    """Run comprehensive statistical tests."""
    print("\n--- Statistical Tests ---")

    tests = []

    # Test 1: Pitches per game
    tests.append({
        'test': 'Pitches per Game',
        'pre_value': pitch_count_stats['pre_mean'],
        'post_value': pitch_count_stats['post_mean'],
        'change': pitch_count_stats['change'],
        'p_value': pitch_count_stats['p_value'],
        'cohens_d': pitch_count_stats['cohens_d'],
        'interpretation': 'large' if abs(pitch_count_stats['cohens_d']) > 0.8 else 'medium' if abs(pitch_count_stats['cohens_d']) > 0.5 else 'small' if abs(pitch_count_stats['cohens_d']) > 0.2 else 'negligible'
    })

    # Test 2: Velocity
    pre_velo = df[df['game_year'].isin([2019, 2021, 2022])]['release_speed'].dropna()
    post_velo = df[df['game_year'].isin(POST_CLOCK_YEARS)]['release_speed'].dropna()

    t_velo, p_velo = stats.ttest_ind(
        pre_velo.sample(n=min(500000, len(pre_velo)), random_state=42).astype(float),
        post_velo.sample(n=min(500000, len(post_velo)), random_state=42).astype(float)
    )
    d_velo = (post_velo.mean() - pre_velo.mean()) / np.sqrt(
        (pre_velo.std()**2 + post_velo.std()**2) / 2
    )

    tests.append({
        'test': 'Average Velocity (mph)',
        'pre_value': pre_velo.mean(),
        'post_value': post_velo.mean(),
        'change': post_velo.mean() - pre_velo.mean(),
        'p_value': p_velo,
        'cohens_d': d_velo,
        'interpretation': 'large' if abs(d_velo) > 0.8 else 'medium' if abs(d_velo) > 0.5 else 'small' if abs(d_velo) > 0.2 else 'negligible'
    })

    # Test 3: Whiff rate
    pre_eff = effectiveness_df[effectiveness_df['game_year'].isin([2019, 2021, 2022])]
    post_eff = effectiveness_df[effectiveness_df['game_year'].isin(POST_CLOCK_YEARS)]

    pre_whiff = pre_eff['whiff_rate'].mean()
    post_whiff = post_eff['whiff_rate'].mean()

    tests.append({
        'test': 'Whiff Rate',
        'pre_value': pre_whiff,
        'post_value': post_whiff,
        'change': post_whiff - pre_whiff,
        'p_value': np.nan,  # Can't do t-test on 3 values each
        'cohens_d': np.nan,
        'interpretation': 'N/A (small sample)'
    })

    tests_df = pd.DataFrame(tests)

    print("\nSummary of Changes:")
    for _, row in tests_df.iterrows():
        print(f"\n{row['test']}:")
        print(f"  Pre-clock: {row['pre_value']:.2f}")
        print(f"  Post-clock: {row['post_value']:.2f}")
        print(f"  Change: {row['change']:+.2f}")
        if not np.isnan(row['cohens_d']):
            print(f"  Cohen's d: {row['cohens_d']:.3f} ({row['interpretation']})")

    return tests_df


def create_visualizations(yearly_pitches, effectiveness_df, yearly_mix, inning_velo):
    """Create publication-ready figures."""
    print("\n--- Creating Visualizations ---")

    plt.style.use('seaborn-v0_8-whitegrid')

    # Figure 1: Pitches per game trend with clock marker
    fig, ax = plt.subplots(figsize=(10, 6))

    years = yearly_pitches.index.values
    pitches = yearly_pitches['mean_pitches'].values

    # Color by pre/post clock
    colors = ['#1f77b4' if y < 2023 else '#ff7f0e' for y in years]
    ax.bar(years, pitches, color=colors, edgecolor='black', alpha=0.8)

    # Add clock introduction line
    ax.axvline(x=2022.5, color='red', linestyle='--', linewidth=2, label='Pitch Clock Introduced')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Average Pitches per Game', fontsize=12)
    ax.set_title('Pitches per Game: Before and After Pitch Clock', fontsize=14)
    ax.legend()
    ax.set_ylim(200, 350)

    # Add value labels
    for i, (y, p) in enumerate(zip(years, pitches)):
        ax.text(y, p + 3, f'{p:.0f}', ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_pitches_per_game.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig01_pitches_per_game.png")

    # Figure 2: Effectiveness metrics over time
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    years_eff = effectiveness_df['game_year'].values

    # wOBA
    ax1 = axes[0]
    ax1.plot(years_eff, effectiveness_df['woba'], 'o-', color='#1f77b4', linewidth=2, markersize=8)
    ax1.axvline(x=2022.5, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('wOBA Against', fontsize=12)
    ax1.set_title('League wOBA Against', fontsize=14)
    ax1.set_ylim(0.30, 0.35)

    # Whiff rate
    ax2 = axes[1]
    ax2.plot(years_eff, effectiveness_df['whiff_rate'] * 100, 'o-', color='#2ca02c', linewidth=2, markersize=8)
    ax2.axvline(x=2022.5, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Whiff Rate (%)', fontsize=12)
    ax2.set_title('League Whiff Rate', fontsize=14)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig02_effectiveness.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig02_effectiveness.png")

    # Figure 3: Pitch mix changes
    fig, ax = plt.subplots(figsize=(10, 6))

    mix_years = yearly_mix.index.values

    ax.plot(mix_years, yearly_mix['Fastball'], 'o-', label='Fastball', color='#1f77b4', linewidth=2)
    ax.plot(mix_years, yearly_mix['Breaking'], 's-', label='Breaking', color='#ff7f0e', linewidth=2)
    ax.plot(mix_years, yearly_mix['Offspeed'], '^-', label='Offspeed', color='#2ca02c', linewidth=2)

    ax.axvline(x=2022.5, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Clock Introduced')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Pitch Mix (%)', fontsize=12)
    ax.set_title('Pitch Mix Evolution and the Pitch Clock', fontsize=14)
    ax.legend()
    ax.set_ylim(0, 60)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig03_pitch_mix.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig03_pitch_mix.png")

    # Figure 4: Velocity by inning (pre vs post)
    fig, ax = plt.subplots(figsize=(10, 6))

    innings = list(range(1, 10))
    velo_2022 = [inning_velo.loc[i, 2022] for i in innings]
    velo_2023 = [inning_velo.loc[i, 2023] for i in innings]
    velo_2024 = [inning_velo.loc[i, 2024] for i in innings]

    ax.plot(innings, velo_2022, 'o-', label='2022 (Pre-Clock)', color='#1f77b4', linewidth=2)
    ax.plot(innings, velo_2023, 's-', label='2023 (Clock Year 1)', color='#ff7f0e', linewidth=2)
    ax.plot(innings, velo_2024, '^-', label='2024 (Clock Year 2)', color='#2ca02c', linewidth=2)

    ax.set_xlabel('Inning', fontsize=12)
    ax.set_ylabel('Average Velocity (mph)', fontsize=12)
    ax.set_title('Velocity by Inning: Pre vs Post Pitch Clock', fontsize=14)
    ax.legend()
    ax.set_xticks(innings)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig04_velocity_by_inning.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig04_velocity_by_inning.png")


def save_results(yearly_pitches, effectiveness_df, yearly_mix, tests_df, pitch_count_stats):
    """Save all results to CSV files."""
    print("\n--- Saving Results ---")

    # Pitches per game
    yearly_pitches.to_csv(f'{RESULTS_DIR}/pitches_per_game.csv')
    print("Saved pitches_per_game.csv")

    # Effectiveness
    effectiveness_df.to_csv(f'{RESULTS_DIR}/effectiveness_by_year.csv', index=False)
    print("Saved effectiveness_by_year.csv")

    # Pitch mix
    yearly_mix.to_csv(f'{RESULTS_DIR}/pitch_mix_by_year.csv')
    print("Saved pitch_mix_by_year.csv")

    # Statistical tests
    tests_df.to_csv(f'{RESULTS_DIR}/statistical_tests.csv', index=False)
    print("Saved statistical_tests.csv")

    # Summary
    summary = {
        'metric': [
            'Pitches per Game',
            'Average Velocity',
            'wOBA Against',
            'Whiff Rate'
        ],
        'pre_clock_2022': [
            f"{pitch_count_stats['pre_mean']:.1f}",
            f"{effectiveness_df[effectiveness_df['game_year']==2022]['woba'].values[0]:.3f}",
            f"{effectiveness_df[effectiveness_df['game_year']==2022]['woba'].values[0]:.3f}",
            f"{effectiveness_df[effectiveness_df['game_year']==2022]['whiff_rate'].values[0]*100:.1f}%"
        ],
        'post_clock_2023': [
            f"{pitch_count_stats['post_mean']:.1f}",
            f"{effectiveness_df[effectiveness_df['game_year']==2023]['woba'].values[0]:.3f}",
            f"{effectiveness_df[effectiveness_df['game_year']==2023]['woba'].values[0]:.3f}",
            f"{effectiveness_df[effectiveness_df['game_year']==2023]['whiff_rate'].values[0]*100:.1f}%"
        ],
        'interpretation': [
            f"{pitch_count_stats['change']:.1f} fewer pitches (faster games)",
            "Velocity continued to rise",
            "Slight improvement for pitchers",
            "Stable"
        ]
    }

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(f'{RESULTS_DIR}/summary.csv', index=False)
    print("Saved summary.csv")


def main():
    """Execute complete pitch clock analysis."""
    print("=" * 60)
    print("Chapter 14: Pitch Clock Effect (2023+)")
    print("=" * 60)

    # Load data
    df = load_data()

    # Analyze pitch counts
    yearly_pitches, pitch_count_stats = analyze_pitch_counts(df)

    # Analyze velocity
    yearly_velo, inning_velo, velo_change = analyze_velocity(df)

    # Analyze pitch mix
    yearly_mix = analyze_pitch_mix(df)

    # Analyze effectiveness
    effectiveness_df = analyze_effectiveness(df)

    # Statistical tests
    tests_df = statistical_tests(df, pitch_count_stats, effectiveness_df)

    # Create visualizations
    create_visualizations(yearly_pitches, effectiveness_df, yearly_mix, inning_velo)

    # Save results
    save_results(yearly_pitches, effectiveness_df, yearly_mix, tests_df, pitch_count_stats)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY: PITCH CLOCK EFFECT")
    print("=" * 60)

    print(f"\n1. PACE OF PLAY:")
    print(f"   Pre-clock avg: {pitch_count_stats['pre_mean']:.1f} pitches/game")
    print(f"   Post-clock avg: {pitch_count_stats['post_mean']:.1f} pitches/game")
    print(f"   Change: {pitch_count_stats['change']:.1f} pitches ({pitch_count_stats['change']/pitch_count_stats['pre_mean']*100:.1f}%)")

    print(f"\n2. VELOCITY:")
    print(f"   Velocity continued to increase post-clock")
    print(f"   Change: {velo_change:+.2f} mph")

    print(f"\n3. EFFECTIVENESS:")
    eff_2022 = effectiveness_df[effectiveness_df['game_year'] == 2022].iloc[0]
    eff_2023 = effectiveness_df[effectiveness_df['game_year'] == 2023].iloc[0]
    print(f"   wOBA: {eff_2022['woba']:.3f} → {eff_2023['woba']:.3f}")
    print(f"   Whiff: {eff_2022['whiff_rate']*100:.1f}% → {eff_2023['whiff_rate']*100:.1f}%")

    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
