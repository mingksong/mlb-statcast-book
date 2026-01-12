#!/usr/bin/env python3
"""Chapter 20: Count-Based Batting Success (2015-2025)"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/Users/mksong/Documents/mlb-statcast-book')
from src.statcast_analysis import load_seasons

FIGURES_DIR = '/Users/mksong/Documents/mlb-statcast-book/chapters/20_count_batting/figures'
RESULTS_DIR = '/Users/mksong/Documents/mlb-statcast-book/chapters/20_count_batting/results'

def main():
    print("=" * 60)
    print("Chapter 20: Count-Based Batting Success")
    print("=" * 60)

    df = load_seasons(2015, 2025, columns=['game_year', 'balls', 'strikes', 'events',
                                            'launch_speed', 'woba_value', 'woba_denom'])
    df = df.dropna(subset=['balls', 'strikes'])
    df['count'] = df['balls'].astype(int).astype(str) + '-' + df['strikes'].astype(int).astype(str)
    print(f"Pitches: {len(df):,}")

    # Batting outcomes by count (PA-ending only)
    pa_end = df[df['events'].notna()]

    count_stats = pa_end.groupby('count').agg({
        'events': 'count',
        'woba_value': 'sum',
        'woba_denom': 'sum'
    })
    count_stats['woba'] = count_stats['woba_value'] / count_stats['woba_denom']
    count_stats = count_stats.sort_values('woba', ascending=False)

    print("\nwOBA by Count:")
    print(count_stats[['events', 'woba']].round(3))

    # Hitter vs Pitcher counts
    hitter_counts = ['3-0', '3-1', '2-0', '3-2', '2-1']
    pitcher_counts = ['0-2', '1-2', '0-1']

    hitter_woba = pa_end[pa_end['count'].isin(hitter_counts)]
    pitcher_woba = pa_end[pa_end['count'].isin(pitcher_counts)]

    h_woba = hitter_woba['woba_value'].sum() / hitter_woba['woba_denom'].sum()
    p_woba = pitcher_woba['woba_value'].sum() / pitcher_woba['woba_denom'].sum()

    print(f"\nHitter's counts wOBA: {h_woba:.3f}")
    print(f"Pitcher's counts wOBA: {p_woba:.3f}")
    print(f"Advantage: {(h_woba - p_woba):.3f} wOBA")

    # Visualization
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 6))

    counts = count_stats.index.tolist()
    wobas = count_stats['woba'].values
    colors = ['#27ae60' if c in hitter_counts else '#e74c3c' if c in pitcher_counts else '#3498db' for c in counts]

    ax.bar(range(len(counts)), wobas, color=colors)
    ax.set_xticks(range(len(counts)))
    ax.set_xticklabels(counts, rotation=45)
    ax.set_xlabel('Count', fontsize=12)
    ax.set_ylabel('wOBA', fontsize=12)
    ax.set_title('Batting Success (wOBA) by Count', fontsize=14)
    ax.axhline(y=0.320, color='gray', linestyle='--', label='League Avg (~.320)')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_woba_by_count.png', dpi=150)
    plt.close()

    count_stats.to_csv(f'{RESULTS_DIR}/woba_by_count.csv')
    pd.DataFrame({'metric': ['Hitter Count wOBA', 'Pitcher Count wOBA', 'Difference'],
                  'value': [f"{h_woba:.3f}", f"{p_woba:.3f}", f"{h_woba-p_woba:.3f}"]}).to_csv(f'{RESULTS_DIR}/summary.csv', index=False)

    print(f"\nKey: Hitter's counts have {(h_woba/p_woba - 1)*100:.0f}% higher wOBA than pitcher's counts")

if __name__ == '__main__':
    main()
