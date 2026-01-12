#!/usr/bin/env python3
"""Chapter 21: xBA vs Actual BA Gap (2015-2025)"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/Users/mksong/Documents/mlb-statcast-book')
from src.statcast_analysis import load_seasons

FIGURES_DIR = '/Users/mksong/Documents/mlb-statcast-book/chapters/21_xba_gap/figures'
RESULTS_DIR = '/Users/mksong/Documents/mlb-statcast-book/chapters/21_xba_gap/results'

def main():
    print("=" * 60)
    print("Chapter 21: xBA vs Actual BA Gap")
    print("=" * 60)

    df = load_seasons(2015, 2025, columns=['game_year', 'events', 'estimated_ba_using_speedangle'])
    df = df.dropna(subset=['estimated_ba_using_speedangle', 'events'])
    print(f"Batted balls with xBA: {len(df):,}")

    # Calculate actual BA
    hits = ['single', 'double', 'triple', 'home_run']
    ab_events = hits + ['field_out', 'strikeout', 'grounded_into_double_play',
                        'force_out', 'fielders_choice', 'double_play']

    df['is_hit'] = df['events'].isin(hits)
    df['is_ab'] = df['events'].isin(ab_events)
    df_ab = df[df['is_ab']]

    yearly = df_ab.groupby('game_year').agg({
        'is_hit': 'mean',
        'estimated_ba_using_speedangle': 'mean',
        'events': 'count'
    })
    yearly.columns = ['actual_ba', 'xba', 'n_ab']
    yearly['gap'] = yearly['actual_ba'] - yearly['xba']

    print("\nBA vs xBA by Year:")
    print(yearly.round(3))

    years = np.array(yearly.index.values, dtype=float)
    gaps = np.array(yearly['gap'].values, dtype=float)
    slope, _, r, p, _ = stats.linregress(years, gaps)
    print(f"\nGap Trend: {slope:.5f}/year, R²={r**2:.3f}")

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, yearly['actual_ba'], 'o-', label='Actual BA', linewidth=2)
    ax.plot(years, yearly['xba'], 's-', label='xBA', linewidth=2)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Batting Average', fontsize=12)
    ax.set_title('Actual BA vs Expected BA (xBA)', fontsize=14)
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_ba_vs_xba.png', dpi=150)
    plt.close()

    yearly.to_csv(f'{RESULTS_DIR}/ba_xba_by_year.csv')
    pd.DataFrame({'metric': ['Avg Gap (BA - xBA)'], 'value': [f"{yearly['gap'].mean():.4f}"]}).to_csv(f'{RESULTS_DIR}/summary.csv', index=False)

    print(f"\nAverage Gap: {yearly['gap'].mean():.4f}")

if __name__ == '__main__':
    main()
