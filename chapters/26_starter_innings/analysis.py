"""
Chapter 26: Starter Innings Trend Analysis
Analyzes the decline in innings pitched by starting pitchers.
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from statcast_analysis import load_seasons

FIGURES_DIR = 'figures'
RESULTS_DIR = 'results'

def main():
    print("Loading data...")
    df = load_seasons(2015, 2025, columns=[
        'game_year', 'game_pk', 'pitcher', 'inning', 'inning_topbot'
    ])

    print(f"Total pitches: {len(df):,}")

    # Identify starters (first pitcher in each game for each team)
    game_first = df.groupby(['game_pk', 'inning_topbot']).first().reset_index()
    starters = game_first[['game_pk', 'inning_topbot', 'pitcher', 'game_year']].copy()
    starters.columns = ['game_pk', 'inning_topbot', 'starter_id', 'game_year']

    # For each inning (5, 6, 7, 8, 9), check if starter is still pitching
    results = []

    for year in range(2015, 2026):
        year_data = df[df['game_year'] == year]
        year_starters = starters[starters['game_year'] == year]

        year_results = {'game_year': year}

        # Total game-sides (each team's pitching in a game)
        total_game_sides = len(year_starters)
        year_results['n_games'] = total_game_sides // 2  # Approximate games

        for target_inning in [5, 6, 7, 8, 9]:
            # Get pitches from that inning
            inning_pitches = year_data[year_data['inning'] == target_inning]

            # Merge with starters to see if starter is still pitching
            merged = inning_pitches.merge(
                year_starters[['game_pk', 'inning_topbot', 'starter_id']],
                on=['game_pk', 'inning_topbot']
            )

            # Check if pitcher matches starter
            starter_still_in = merged[merged['pitcher'] == merged['starter_id']]

            # Count unique game-sides where starter pitched in this inning
            games_starter_in_inning = starter_still_in.groupby(['game_pk', 'inning_topbot']).ngroups

            # Rate
            rate = games_starter_in_inning / total_game_sides * 100 if total_game_sides > 0 else 0
            year_results[f'pct_in_{target_inning}'] = rate

        results.append(year_results)

    results_df = pd.DataFrame(results)
    print("\nStarter Still Pitching Rate by Inning:")
    print(results_df.round(1))

    # Save results
    results_df.to_csv('results/starter_by_inning.csv', index=False)

    # Calculate average pitchers per game
    pitchers_per_game = df.groupby(['game_year', 'game_pk', 'inning_topbot'])['pitcher'].nunique()
    avg_pitchers = pitchers_per_game.groupby('game_year').mean()
    pitchers_df = pd.DataFrame({
        'game_year': avg_pitchers.index,
        'avg_pitchers_per_team': avg_pitchers.values
    })
    pitchers_df.to_csv('results/pitchers_per_game.csv', index=False)

    print("\nAverage Pitchers Per Team Per Game:")
    print(pitchers_df.round(2))

    # Statistical tests on 6th inning rate
    years = results_df['game_year'].values.astype(float)
    pct_6 = results_df['pct_in_6'].values.astype(float)

    slope, intercept, r, p, se = stats.linregress(years, pct_6)

    early_mean = results_df[results_df['game_year'].isin([2015, 2016, 2017, 2018])]['pct_in_6'].mean()
    late_mean = results_df[results_df['game_year'].isin([2022, 2023, 2024, 2025])]['pct_in_6'].mean()

    stats_results = pd.DataFrame({
        'metric': ['early_pct_6th', 'late_pct_6th', 'change', 'slope', 'r_squared', 'p_value'],
        'value': [early_mean, late_mean, late_mean - early_mean, slope, r**2, p]
    })
    stats_results.to_csv('results/statistical_tests.csv', index=False)

    print(f"\nStatistical Results (6th inning):")
    print(f"Early period (2015-18): {early_mean:.1f}%")
    print(f"Late period (2022-25): {late_mean:.1f}%")
    print(f"Change: {late_mean - early_mean:.1f}%")
    print(f"Slope: {slope:.2f}%/year")
    print(f"R² = {r**2:.3f}, p = {p:.4f}")

    # Create figure - starter in 6th inning rate
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(results_df['game_year'], results_df['pct_in_6'], 'o-', linewidth=2, markersize=8, label='6th Inning')
    ax.plot(results_df['game_year'], results_df['pct_in_7'], 's--', linewidth=2, markersize=6, label='7th Inning')
    ax.plot(results_df['game_year'], results_df['pct_in_8'], '^:', linewidth=2, markersize=6, label='8th Inning')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('% of Games Starter Still Pitching', fontsize=12)
    ax.set_title('Starter Usage by Inning (2015-2025)', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 100)
    plt.tight_layout()
    plt.savefig('figures/fig01_starter_innings.png', dpi=150)
    plt.close()

    # Create figure - pitchers per game
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(pitchers_df['game_year'], pitchers_df['avg_pitchers_per_team'], 'o-', linewidth=2, markersize=8, color='darkred')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Average Pitchers Per Team', fontsize=12)
    ax.set_title('Pitcher Usage Per Game (2015-2025)', fontsize=14)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/fig02_pitchers_per_game.png', dpi=150)
    plt.close()

    print("\nAnalysis complete!")

if __name__ == '__main__':
    main()
