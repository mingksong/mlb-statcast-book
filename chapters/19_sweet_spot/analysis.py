#!/usr/bin/env python3
"""Chapter 19: Sweet Spot Rate Trends (2015-2025)"""

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
    print("Chapter 19: Sweet Spot Rate Trends")
    print("=" * 60)

    df = load_seasons(2015, 2025, columns=['game_year', 'batter', 'launch_angle', 'launch_speed', 'events'])
    df = df.dropna(subset=['launch_angle'])
    print(f"Batted balls: {len(df):,}")

    # Sweet spot = 8-32° launch angle
    df['sweet_spot'] = (df['launch_angle'] >= 8) & (df['launch_angle'] <= 32)

    yearly = df.groupby('game_year')['sweet_spot'].agg(['sum', 'mean', 'count'])
    yearly.columns = ['n_sweet_spot', 'sweet_spot_rate', 'n_batted_balls']
    yearly['sweet_spot_rate'] *= 100

    print("\nSweet Spot Rate by Year:")
    print(yearly.round(2))

    years = np.array(yearly.index.values, dtype=float)
    rates = np.array(yearly['sweet_spot_rate'].values, dtype=float)
    slope, _, r, p, _ = stats.linregress(years, rates)
    print(f"\nTrend: {slope:.3f}%/year, R²={r**2:.3f}, p={p:.4f}")

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, rates, 'o-', color='#27ae60', linewidth=2, markersize=8)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Sweet Spot Rate (%)', fontsize=12)
    ax.set_title('Sweet Spot Rate (8-32° LA) Trend', fontsize=14)
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_sweet_spot_trend.png', dpi=150)
    plt.close()

    yearly.to_csv(f'{RESULTS_DIR}/sweet_spot_by_year.csv')
    pd.DataFrame({'metric': ['Sweet Spot Rate'], 'value_2015': [f"{yearly.loc[2015, 'sweet_spot_rate']:.1f}%"],
                  'value_2025': [f"{yearly.loc[2025, 'sweet_spot_rate']:.1f}%"]}).to_csv(f'{RESULTS_DIR}/summary.csv', index=False)

    print(f"\nSweet Spot Rate: {yearly.loc[2015, 'sweet_spot_rate']:.1f}% → {yearly.loc[2025, 'sweet_spot_rate']:.1f}%")

if __name__ == '__main__':
    main()
