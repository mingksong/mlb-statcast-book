#!/usr/bin/env python3
"""Chapter 18: Hard Hit Rate Analysis (2015-2025)"""

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
    print("=" * 60)
    print("Chapter 18: Hard Hit Rate Analysis")
    print("=" * 60)

    df = load_seasons(2015, 2025, columns=['game_year', 'batter', 'launch_speed', 'events'])
    df = df.dropna(subset=['launch_speed'])
    print(f"Batted balls: {len(df):,}")

    # Hard hit = 95+ mph
    df['hard_hit'] = df['launch_speed'] >= 95

    # By year
    yearly = df.groupby('game_year').agg({
        'hard_hit': ['sum', 'mean'],
        'launch_speed': ['mean', 'count']
    })
    yearly.columns = ['n_hard_hit', 'hard_hit_rate', 'avg_ev', 'n_batted_balls']
    yearly['hard_hit_rate'] *= 100

    print("\nHard Hit Rate by Year:")
    print(yearly.round(2))

    # Trend
    years = np.array(yearly.index.values, dtype=float)
    rates = np.array(yearly['hard_hit_rate'].values, dtype=float)
    slope, _, r, p, _ = stats.linregress(years, rates)
    print(f"\nTrend: {slope:.3f}%/year, R²={r**2:.3f}, p={p:.4f}")

    # Visualization
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, rates, 'o-', color='#e74c3c', linewidth=2, markersize=8)
    ax.axhline(y=rates.mean(), color='gray', linestyle='--', label=f'Avg: {rates.mean():.1f}%')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Hard Hit Rate (%)', fontsize=12)
    ax.set_title('Hard Hit Rate (95+ mph) Trend', fontsize=14)
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_hard_hit_trend.png', dpi=150)
    plt.close()

    # Save
    yearly.to_csv(f'{RESULTS_DIR}/hard_hit_by_year.csv')
    pd.DataFrame({'metric': ['Hard Hit Rate'], 'value_2015': [f"{yearly.loc[2015, 'hard_hit_rate']:.1f}%"],
                  'value_2025': [f"{yearly.loc[2025, 'hard_hit_rate']:.1f}%"]}).to_csv(f'{RESULTS_DIR}/summary.csv', index=False)

    print(f"\nHard Hit Rate: {yearly.loc[2015, 'hard_hit_rate']:.1f}% → {yearly.loc[2025, 'hard_hit_rate']:.1f}%")

if __name__ == '__main__':
    main()
