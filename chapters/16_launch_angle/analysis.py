#!/usr/bin/env python3
"""
Chapter 16: Launch Angle Transformation (2015-2025)

Research Question: How has launch angle evolved, and how did it drive
the fly ball revolution?

Key Metrics:
- Average launch angle
- Fly ball rate (LA > 25°)
- Ground ball rate (LA < 10°)
- Optimal launch angle rate (10-30°)
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/Users/mksong/Documents/mlb-statcast-book')

from src.statcast_analysis import load_seasons

FIGURES_DIR = '/Users/mksong/Documents/mlb-statcast-book/chapters/16_launch_angle/figures'
RESULTS_DIR = '/Users/mksong/Documents/mlb-statcast-book/chapters/16_launch_angle/results'


def load_data():
    print("Loading data...")
    columns = ['game_year', 'batter', 'launch_angle', 'launch_speed', 'events',
               'estimated_ba_using_speedangle']
    df = load_seasons(2015, 2025, columns=columns)
    print(f"Loaded {len(df):,} total pitches")
    df = df.dropna(subset=['launch_angle'])
    print(f"Batted balls with launch angle: {len(df):,}")
    return df


def analyze_launch_angle_trends(df):
    print("\n--- Launch Angle Trends ---")

    yearly = df.groupby('game_year')['launch_angle'].agg(['count', 'mean', 'std', 'median'])
    yearly.columns = ['n_batted_balls', 'mean_la', 'std_la', 'median_la']

    print("\nLaunch Angle by Year:")
    print(yearly.round(2))

    years = np.array(yearly.index.values, dtype=float)
    means = np.array(yearly['mean_la'].values, dtype=float)
    slope, intercept, r_value, p_value, std_err = stats.linregress(years, means)

    print(f"\nTrend: {slope:.3f}°/year, R²={r_value**2:.3f}, p={p_value:.4f}")

    return yearly, {'slope': slope, 'r_squared': r_value**2, 'p_value': p_value}


def analyze_batted_ball_types(df):
    print("\n--- Batted Ball Type Distribution ---")

    df['bb_type'] = pd.cut(df['launch_angle'],
                           bins=[-90, 10, 25, 50, 90],
                           labels=['Ground Ball', 'Line Drive', 'Fly Ball', 'Pop Up'])

    yearly_types = df.groupby('game_year')['bb_type'].value_counts(normalize=True).unstack() * 100

    print("\nBatted Ball Distribution by Year:")
    print(yearly_types.round(1))

    # Ground ball trend
    years = np.array(yearly_types.index.values, dtype=float)
    gb_rates = np.array(yearly_types['Ground Ball'].values, dtype=float)
    fb_rates = np.array(yearly_types['Fly Ball'].values, dtype=float)

    gb_slope, _, gb_r, gb_p, _ = stats.linregress(years, gb_rates)
    fb_slope, _, fb_r, fb_p, _ = stats.linregress(years, fb_rates)

    print(f"\nGround Ball Trend: {gb_slope:.3f}%/year, R²={gb_r**2:.3f}")
    print(f"Fly Ball Trend: {fb_slope:.3f}%/year, R²={fb_r**2:.3f}")

    return yearly_types, {'gb_slope': gb_slope, 'fb_slope': fb_slope}


def analyze_sweet_spot(df):
    print("\n--- Sweet Spot Analysis (8-32°) ---")

    df['sweet_spot'] = (df['launch_angle'] >= 8) & (df['launch_angle'] <= 32)
    yearly_ss = df.groupby('game_year')['sweet_spot'].mean() * 100

    print("\nSweet Spot Rate by Year:")
    for year, rate in yearly_ss.items():
        print(f"  {year}: {rate:.1f}%")

    return yearly_ss


def statistical_tests(df):
    print("\n--- Statistical Tests ---")

    early = df[df['game_year'].isin([2015, 2016, 2017, 2018])]['launch_angle']
    late = df[df['game_year'].isin([2022, 2023, 2024, 2025])]['launch_angle']

    sample_size = min(500000, len(early), len(late))
    early_sample = early.sample(n=sample_size, random_state=42)
    late_sample = late.sample(n=sample_size, random_state=42)

    t_stat, p_val = stats.ttest_ind(early_sample.astype(float), late_sample.astype(float))
    pooled_std = np.sqrt((early.std()**2 + late.std()**2) / 2)
    cohens_d = (late.mean() - early.mean()) / pooled_std

    interp = 'large' if abs(cohens_d) > 0.8 else 'medium' if abs(cohens_d) > 0.5 else 'small' if abs(cohens_d) > 0.2 else 'negligible'

    print(f"\nLaunch Angle Change:")
    print(f"  Early (2015-18): {early.mean():.2f}°")
    print(f"  Late (2022-25): {late.mean():.2f}°")
    print(f"  Change: {late.mean() - early.mean():+.2f}°")
    print(f"  Cohen's d: {cohens_d:.3f} ({interp})")

    return pd.DataFrame([{
        'test': 'Launch Angle (2015-18 vs 2022-25)',
        'early_mean': early.mean(),
        'late_mean': late.mean(),
        'change': late.mean() - early.mean(),
        'cohens_d': cohens_d,
        'interpretation': interp
    }])


def create_visualizations(df, yearly, yearly_types, yearly_ss):
    print("\n--- Creating Visualizations ---")
    plt.style.use('seaborn-v0_8-whitegrid')

    # Figure 1: Launch angle trend
    fig, ax = plt.subplots(figsize=(10, 6))
    years = np.array(yearly.index.values, dtype=float)
    means = np.array(yearly['mean_la'].values, dtype=float)

    ax.plot(years, means, 'o-', color='#1f77b4', linewidth=2, markersize=8)
    z = np.polyfit(years, means, 1)
    p = np.poly1d(z)
    ax.plot(years, p(years), '--', color='red', linewidth=2, label=f'Trend: {z[0]:+.2f}°/year')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Average Launch Angle (°)', fontsize=12)
    ax.set_title('Average Launch Angle Trend (2015-2025)', fontsize=14)
    ax.legend()
    ax.set_xlim(2014.5, 2025.5)
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_la_trend.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig01_la_trend.png")

    # Figure 2: Batted ball type distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    years_bb = np.array(yearly_types.index.values, dtype=float)

    for col in ['Ground Ball', 'Line Drive', 'Fly Ball']:
        vals = np.array(yearly_types[col].values, dtype=float)
        ax.plot(years_bb, vals, 'o-', label=col, linewidth=2, markersize=6)

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Rate (%)', fontsize=12)
    ax.set_title('Batted Ball Type Distribution', fontsize=14)
    ax.legend()
    ax.set_xlim(2014.5, 2025.5)
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig02_bb_types.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig02_bb_types.png")

    # Figure 3: Distribution comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    la_2015 = df[df['game_year'] == 2015]['launch_angle']
    la_2025 = df[df['game_year'] == 2025]['launch_angle']

    ax.hist(la_2015, bins=50, alpha=0.5, label=f'2015 (mean: {la_2015.mean():.1f}°)',
            color='#1f77b4', density=True, range=(-50, 70))
    ax.hist(la_2025, bins=50, alpha=0.5, label=f'2025 (mean: {la_2025.mean():.1f}°)',
            color='#ff7f0e', density=True, range=(-50, 70))
    ax.axvspan(8, 32, alpha=0.2, color='green', label='Sweet Spot (8-32°)')

    ax.set_xlabel('Launch Angle (°)', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title('Launch Angle Distribution: 2015 vs 2025', fontsize=14)
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig03_la_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig03_la_distribution.png")

    # Figure 4: Sweet spot rate
    fig, ax = plt.subplots(figsize=(10, 6))
    ss_years = np.array(yearly_ss.index.values, dtype=float)
    ss_vals = np.array(yearly_ss.values, dtype=float)

    ax.plot(ss_years, ss_vals, 'o-', color='#2ca02c', linewidth=2, markersize=8)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Sweet Spot Rate (%)', fontsize=12)
    ax.set_title('Sweet Spot Rate (8-32° Launch Angle)', fontsize=14)
    ax.set_xlim(2014.5, 2025.5)
    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig04_sweet_spot.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig04_sweet_spot.png")


def save_results(yearly, yearly_types, yearly_ss, tests_df, trend):
    print("\n--- Saving Results ---")
    yearly.to_csv(f'{RESULTS_DIR}/launch_angle_by_year.csv')
    yearly_types.to_csv(f'{RESULTS_DIR}/batted_ball_types.csv')
    yearly_ss.to_frame('sweet_spot_rate').to_csv(f'{RESULTS_DIR}/sweet_spot_rate.csv')
    tests_df.to_csv(f'{RESULTS_DIR}/statistical_tests.csv', index=False)

    summary = pd.DataFrame({
        'metric': ['Average Launch Angle', 'Ground Ball Rate', 'Fly Ball Rate', 'Sweet Spot Rate'],
        'value_2015': [f"{yearly.loc[2015, 'mean_la']:.1f}°",
                       f"{yearly_types.loc[2015, 'Ground Ball']:.1f}%",
                       f"{yearly_types.loc[2015, 'Fly Ball']:.1f}%",
                       f"{yearly_ss.loc[2015]:.1f}%"],
        'value_2025': [f"{yearly.loc[2025, 'mean_la']:.1f}°",
                       f"{yearly_types.loc[2025, 'Ground Ball']:.1f}%",
                       f"{yearly_types.loc[2025, 'Fly Ball']:.1f}%",
                       f"{yearly_ss.loc[2025]:.1f}%"],
        'trend': [f"{trend['slope']:+.2f}°/year", "Declining", "Rising", "Stable"]
    })
    summary.to_csv(f'{RESULTS_DIR}/summary.csv', index=False)
    print("Saved all results")


def main():
    print("=" * 60)
    print("Chapter 16: Launch Angle Transformation")
    print("=" * 60)

    df = load_data()
    yearly, trend = analyze_launch_angle_trends(df)
    yearly_types, bb_trends = analyze_batted_ball_types(df)
    yearly_ss = analyze_sweet_spot(df)
    tests_df = statistical_tests(df)
    create_visualizations(df, yearly, yearly_types, yearly_ss)
    save_results(yearly, yearly_types, yearly_ss, tests_df, trend)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nLaunch Angle: {yearly.loc[2015, 'mean_la']:.1f}° → {yearly.loc[2025, 'mean_la']:.1f}°")
    print(f"Ground Balls: {yearly_types.loc[2015, 'Ground Ball']:.1f}% → {yearly_types.loc[2025, 'Ground Ball']:.1f}%")
    print(f"Fly Balls: {yearly_types.loc[2015, 'Fly Ball']:.1f}% → {yearly_types.loc[2025, 'Fly Ball']:.1f}%")
    print("=" * 60)


if __name__ == '__main__':
    main()
