#!/usr/bin/env python3
"""Chapter 23: Strikeout Rate Trends (2015-2025)"""

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
    print("Chapter 23: Strikeout Rate Trends")
    print("=" * 60)

    df = load_seasons(2015, 2025, columns=['game_year', 'game_pk', 'at_bat_number', 'events'])
    pa_end = df[df['events'].notna()].drop_duplicates(subset=['game_pk', 'at_bat_number'])
    print(f"Plate appearances: {len(pa_end):,}")

    # K rate by year
    yearly = pa_end.groupby('game_year').agg({
        'events': 'count'
    })
    yearly['strikeouts'] = pa_end[pa_end['events'] == 'strikeout'].groupby('game_year').size()
    yearly['k_rate'] = yearly['strikeouts'] / yearly['events'] * 100

    print("\nStrikeout Rate by Year:")
    print(yearly.round(2))

    years = np.array(yearly.index.values, dtype=float)
    rates = np.array(yearly['k_rate'].values, dtype=float)
    slope, _, r, p, _ = stats.linregress(years, rates)
    print(f"\nTrend: {slope:.3f}%/year, R²={r**2:.3f}, p={p:.4f}")

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, rates, 'o-', color='#e74c3c', linewidth=2, markersize=8)
    z = np.polyfit(years, rates, 1)
    p_line = np.poly1d(z)
    ax.plot(years, p_line(years), '--', color='gray')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Strikeout Rate (%)', fontsize=12)
    ax.set_title('MLB Strikeout Rate Trend', fontsize=14)
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_k_rate_trend.png', dpi=150)
    plt.close()

    yearly.to_csv(f'{RESULTS_DIR}/k_rate_by_year.csv')
    pd.DataFrame({'metric': ['K Rate 2015', 'K Rate 2025', 'Change'],
                  'value': [f"{yearly.loc[2015, 'k_rate']:.1f}%", f"{yearly.loc[2025, 'k_rate']:.1f}%",
                           f"{yearly.loc[2025, 'k_rate'] - yearly.loc[2015, 'k_rate']:+.1f}%"]}).to_csv(f'{RESULTS_DIR}/summary.csv', index=False)

    print(f"\nK Rate: {yearly.loc[2015, 'k_rate']:.1f}% → {yearly.loc[2025, 'k_rate']:.1f}%")

if __name__ == '__main__':
    main()
