#!/usr/bin/env python3
"""Chapter 22: Batting Success by Pitch Type (2015-2025)"""

import pandas as pd
import numpy as np
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
    print("Chapter 22: Batting Success by Pitch Type")
    print("=" * 60)

    df = load_seasons(2015, 2025, columns=['game_year', 'pitch_type', 'events', 'woba_value', 'woba_denom', 'launch_speed'])
    df = df[df['woba_denom'] > 0]
    print(f"PA-ending pitches: {len(df):,}")

    # wOBA by pitch type
    pitch_woba = df.groupby('pitch_type').agg({
        'woba_value': 'sum',
        'woba_denom': 'sum',
        'launch_speed': 'mean'
    })
    pitch_woba['woba'] = pitch_woba['woba_value'] / pitch_woba['woba_denom']
    pitch_woba = pitch_woba[pitch_woba['woba_denom'] > 10000].sort_values('woba', ascending=False)

    print("\nwOBA by Pitch Type (hitter perspective - higher = better for hitter):")
    print(pitch_woba[['woba_denom', 'woba']].round(3))

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 6))
    pitches = pitch_woba.index.tolist()
    wobas = pitch_woba['woba'].values
    ax.bar(pitches, wobas, color='#3498db')
    ax.axhline(y=0.320, color='red', linestyle='--', label='League Avg')
    ax.set_xlabel('Pitch Type', fontsize=12)
    ax.set_ylabel('wOBA (Hitter)', fontsize=12)
    ax.set_title('Batting Success by Pitch Type', fontsize=14)
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_woba_by_pitch.png', dpi=150)
    plt.close()

    pitch_woba.to_csv(f'{RESULTS_DIR}/woba_by_pitch_type.csv')

    best = pitch_woba['woba'].idxmax()
    worst = pitch_woba['woba'].idxmin()
    print(f"\nEasiest to hit: {best} (wOBA: {pitch_woba.loc[best, 'woba']:.3f})")
    print(f"Hardest to hit: {worst} (wOBA: {pitch_woba.loc[worst, 'woba']:.3f})")

if __name__ == '__main__':
    main()
