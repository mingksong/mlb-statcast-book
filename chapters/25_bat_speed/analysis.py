#!/usr/bin/env python3
"""Chapter 25: Bat Speed Analysis (2023+ only)"""

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
    print("Chapter 25: Bat Speed Analysis (2023+)")
    print("=" * 60)

    # Bat speed only available 2023+
    df = load_seasons(2023, 2025, columns=['game_year', 'batter', 'bat_speed', 'swing_length',
                                            'launch_speed', 'events'])

    # Check if bat_speed column exists and has data
    if 'bat_speed' not in df.columns:
        print("WARNING: bat_speed column not found in data")
        # Create placeholder results
        pd.DataFrame({'note': ['Bat speed data not available in dataset']}).to_csv(f'{RESULTS_DIR}/summary.csv', index=False)
        return

    df_bat = df.dropna(subset=['bat_speed'])
    print(f"Swings with bat speed data: {len(df_bat):,}")

    if len(df_bat) < 1000:
        print("Insufficient bat speed data for analysis")
        pd.DataFrame({'note': ['Insufficient bat speed data']}).to_csv(f'{RESULTS_DIR}/summary.csv', index=False)
        return

    yearly = df_bat.groupby('game_year')['bat_speed'].agg(['mean', 'std', 'count'])
    print("\nBat Speed by Year:")
    print(yearly.round(2))

    # Correlation with exit velo
    df_both = df_bat.dropna(subset=['launch_speed'])
    if len(df_both) > 0:
        corr = df_both['bat_speed'].corr(df_both['launch_speed'])
        print(f"\nBat Speed - Exit Velo correlation: {corr:.3f}")

    plt.style.use('seaborn-v0_8-whitegrid')
    if len(yearly) > 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(yearly.index, yearly['mean'], color='#9b59b6')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Avg Bat Speed (mph)', fontsize=12)
        ax.set_title('Average Bat Speed (2023+)', fontsize=14)
        plt.tight_layout()
        plt.savefig(f'{FIGURES_DIR}/fig01_bat_speed.png', dpi=150)
        plt.close()

    yearly.to_csv(f'{RESULTS_DIR}/bat_speed_by_year.csv')
    pd.DataFrame({'metric': ['Avg Bat Speed'], 'value': [f"{yearly['mean'].mean():.1f} mph"]}).to_csv(f'{RESULTS_DIR}/summary.csv', index=False)

if __name__ == '__main__':
    main()
