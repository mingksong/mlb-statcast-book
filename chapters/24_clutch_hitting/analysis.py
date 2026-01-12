#!/usr/bin/env python3
"""Chapter 24: Clutch Hitting Analysis (2015-2025)"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/Users/mksong/Documents/mlb-statcast-book')
from src.statcast_analysis import load_seasons

FIGURES_DIR = '/Users/mksong/Documents/mlb-statcast-book/chapters/24_clutch_hitting/figures'
RESULTS_DIR = '/Users/mksong/Documents/mlb-statcast-book/chapters/24_clutch_hitting/results'

def main():
    print("=" * 60)
    print("Chapter 24: Clutch Hitting Analysis")
    print("=" * 60)

    df = load_seasons(2015, 2025, columns=['game_year', 'on_1b', 'on_2b', 'on_3b', 'outs_when_up',
                                            'events', 'woba_value', 'woba_denom'])
    pa_end = df[df['woba_denom'] > 0]
    print(f"PA-ending pitches: {len(pa_end):,}")

    # Define situations
    pa_end['risp'] = pa_end['on_2b'].notna() | pa_end['on_3b'].notna()
    pa_end['bases_empty'] = pa_end['on_1b'].isna() & pa_end['on_2b'].isna() & pa_end['on_3b'].isna()
    pa_end['two_outs'] = pa_end['outs_when_up'] == 2
    pa_end['clutch'] = pa_end['risp'] & pa_end['two_outs']

    # wOBA by situation
    situations = {
        'Bases Empty': pa_end[pa_end['bases_empty']],
        'RISP': pa_end[pa_end['risp']],
        'Two Outs': pa_end[pa_end['two_outs']],
        'Clutch (RISP + 2 out)': pa_end[pa_end['clutch']]
    }

    results = []
    for name, data in situations.items():
        woba = data['woba_value'].sum() / data['woba_denom'].sum()
        results.append({'situation': name, 'woba': woba, 'n': len(data)})
        print(f"{name}: wOBA = {woba:.3f} (n={len(data):,})")

    results_df = pd.DataFrame(results)

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(results_df['situation'], results_df['woba'], color=['#3498db', '#e74c3c', '#f39c12', '#9b59b6'])
    ax.axhline(y=0.320, color='gray', linestyle='--')
    ax.set_ylabel('wOBA', fontsize=12)
    ax.set_title('Batting Performance by Situation', fontsize=14)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_clutch_woba.png', dpi=150)
    plt.close()

    results_df.to_csv(f'{RESULTS_DIR}/woba_by_situation.csv', index=False)

if __name__ == '__main__':
    main()
