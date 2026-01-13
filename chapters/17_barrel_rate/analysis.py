#!/usr/bin/env python3
"""Chapter 17: Barrel Rate Analysis (2015-2025)"""

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

def is_barrel(ev, la):
    """Define barrel based on Statcast criteria (simplified)."""
    if pd.isna(ev) or pd.isna(la):
        return False
    if ev < 98:
        return False
    # Sweet spot expands with higher EV
    if ev >= 98 and ev < 99:
        return 26 <= la <= 30
    elif ev >= 99 and ev < 100:
        return 25 <= la <= 31
    elif ev >= 100 and ev < 101:
        return 24 <= la <= 33
    elif ev >= 101 and ev < 102:
        return 23 <= la <= 34
    elif ev >= 102 and ev < 103:
        return 22 <= la <= 35
    elif ev >= 103 and ev < 104:
        return 21 <= la <= 36
    elif ev >= 104 and ev < 105:
        return 20 <= la <= 37
    elif ev >= 105 and ev < 106:
        return 19 <= la <= 38
    elif ev >= 106 and ev < 107:
        return 18 <= la <= 39
    elif ev >= 107 and ev < 108:
        return 17 <= la <= 40
    elif ev >= 108:
        return 8 <= la <= 50
    return False

def main():
    print("=" * 60)
    print("Chapter 17: Barrel Rate Analysis")
    print("=" * 60)

    # Load data
    print("Loading data...")
    df = load_seasons(2015, 2025, columns=['game_year', 'batter', 'launch_speed', 'launch_angle', 'events'])
    df = df.dropna(subset=['launch_speed', 'launch_angle'])
    print(f"Batted balls: {len(df):,}")

    # Calculate barrels
    print("\nCalculating barrels...")
    df['is_barrel'] = df.apply(lambda x: is_barrel(x['launch_speed'], x['launch_angle']), axis=1)

    # Yearly barrel rate
    yearly = df.groupby('game_year').agg({
        'is_barrel': ['sum', 'mean'],
        'launch_speed': 'count'
    })
    yearly.columns = ['n_barrels', 'barrel_rate', 'n_batted_balls']
    yearly['barrel_rate'] = yearly['barrel_rate'] * 100

    print("\nBarrel Rate by Year:")
    print(yearly.round(2))

    # Trend analysis
    years = np.array(yearly.index.values, dtype=float)
    rates = np.array(yearly['barrel_rate'].values, dtype=float)
    slope, intercept, r_value, p_value, std_err = stats.linregress(years, rates)
    print(f"\nTrend: {slope:.3f}%/year, R²={r_value**2:.3f}, p={p_value:.4f}")

    # Statistical test
    early = df[df['game_year'].isin([2015, 2016, 2017, 2018])]['is_barrel'].mean() * 100
    late = df[df['game_year'].isin([2022, 2023, 2024, 2025])]['is_barrel'].mean() * 100
    print(f"\nEarly (2015-18): {early:.2f}%")
    print(f"Late (2022-25): {late:.2f}%")
    print(f"Change: {late - early:+.2f}%")

    # Visualizations
    print("\n--- Creating Visualizations ---")
    plt.style.use('seaborn-v0_8-whitegrid')

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, rates, 'o-', color='#e74c3c', linewidth=2, markersize=8)
    z = np.polyfit(years, rates, 1)
    p = np.poly1d(z)
    ax.plot(years, p(years), '--', color='gray', linewidth=2)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Barrel Rate (%)', fontsize=12)
    ax.set_title('Barrel Rate Trend (2015-2025)', fontsize=14)
    ax.set_xlim(2014.5, 2025.5)
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_barrel_trend.png', dpi=150)
    plt.close()

    # Save results
    yearly.to_csv(f'{RESULTS_DIR}/barrel_rate_by_year.csv')
    pd.DataFrame({
        'metric': ['Barrel Rate'],
        'value_2015': [f"{yearly.loc[2015, 'barrel_rate']:.2f}%"],
        'value_2025': [f"{yearly.loc[2025, 'barrel_rate']:.2f}%"],
        'trend': [f"{slope:+.3f}%/year"]
    }).to_csv(f'{RESULTS_DIR}/summary.csv', index=False)

    print("\n" + "=" * 60)
    print(f"Barrel Rate: {yearly.loc[2015, 'barrel_rate']:.1f}% → {yearly.loc[2025, 'barrel_rate']:.1f}%")
    print("=" * 60)

if __name__ == '__main__':
    main()
