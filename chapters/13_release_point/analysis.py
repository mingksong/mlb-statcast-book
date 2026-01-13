#!/usr/bin/env python3
"""
Chapter 13: Release Point Consistency (2015-2025)

Research Question: How consistent are MLB pitchers with their release points,
and has release point consistency improved over the decade?

Key Metrics:
- Release point coordinates (x, y, z)
- Arm angle (derived from release point)
- Consistency (standard deviation within pitcher-season)
- Relationship between consistency and effectiveness
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from statcast_analysis import load_seasons

# Configuration
FIGURES_DIR = 'figures'
RESULTS_DIR = 'results'
MIN_PITCHES = 200  # Minimum sample size


def load_data():
    """Load all seasons with release point data."""
    print("Loading data...")
    columns = [
        'game_year', 'pitcher', 'p_throws',
        'release_pos_x', 'release_pos_y', 'release_pos_z',
        'release_speed', 'pitch_type',
        'woba_value', 'woba_denom',
        'description', 'type'
    ]

    df = load_seasons(2015, 2025, columns=columns)
    print(f"Loaded {len(df):,} total pitches")

    # Clean data
    df = df.dropna(subset=['release_pos_x', 'release_pos_y', 'release_pos_z'])
    print(f"After cleaning: {len(df):,} pitches")

    return df


def calculate_pitcher_metrics(df):
    """Calculate release point metrics for each pitcher-season."""
    print("\n--- Calculating Pitcher Metrics ---")

    results = []

    for (year, pitcher), group in df.groupby(['game_year', 'pitcher']):
        if len(group) < MIN_PITCHES:
            continue

        # Release point statistics
        x_mean = group['release_pos_x'].mean()
        y_mean = group['release_pos_y'].mean()
        z_mean = group['release_pos_z'].mean()

        x_std = group['release_pos_x'].std()
        y_std = group['release_pos_y'].std()
        z_std = group['release_pos_z'].std()

        # 3D consistency (lower = better)
        consistency_3d = np.sqrt(x_std**2 + y_std**2 + z_std**2)

        # Horizontal consistency only (what hitters see)
        horizontal_std = np.sqrt(x_std**2 + z_std**2)

        # Arm angle approximation (using release height and horizontal position)
        # This is a simplified estimate
        arm_angle = np.degrees(np.arctan2(z_mean - 5.0, abs(x_mean)))  # relative to ~5ft shoulder height

        # Handedness
        throws = group['p_throws'].mode()
        throws = throws.iloc[0] if len(throws) > 0 else 'Unknown'

        # Effectiveness (wOBA allowed)
        woba_data = group[group['woba_denom'] > 0]
        if len(woba_data) > 0:
            woba = woba_data['woba_value'].sum() / woba_data['woba_denom'].sum()
        else:
            woba = np.nan

        # Average velocity
        avg_velo = group['release_speed'].mean()

        # Whiff rate
        swings = group['description'].isin([
            'swinging_strike', 'swinging_strike_blocked', 'foul', 'foul_tip',
            'hit_into_play', 'foul_bunt', 'missed_bunt'
        ]).sum()
        whiffs = group['description'].isin(['swinging_strike', 'swinging_strike_blocked']).sum()
        whiff_rate = whiffs / swings if swings > 0 else np.nan

        results.append({
            'game_year': year,
            'pitcher': pitcher,
            'p_throws': throws,
            'n_pitches': len(group),
            'release_x_mean': x_mean,
            'release_y_mean': y_mean,
            'release_z_mean': z_mean,
            'release_x_std': x_std,
            'release_y_std': y_std,
            'release_z_std': z_std,
            'consistency_3d': consistency_3d,
            'horizontal_std': horizontal_std,
            'arm_angle_est': arm_angle,
            'avg_velocity': avg_velo,
            'woba_allowed': woba,
            'whiff_rate': whiff_rate
        })

    pitcher_df = pd.DataFrame(results)
    print(f"Analyzed {len(pitcher_df):,} pitcher-seasons")

    return pitcher_df


def analyze_trends(pitcher_df):
    """Analyze year-over-year trends in release point metrics."""
    print("\n--- Analyzing Trends ---")

    # Aggregate by year
    yearly = pitcher_df.groupby('game_year').agg({
        'consistency_3d': ['mean', 'median', 'std'],
        'horizontal_std': ['mean', 'median'],
        'release_x_mean': ['mean', 'std'],
        'release_y_mean': ['mean', 'std'],
        'release_z_mean': ['mean', 'std'],
        'arm_angle_est': ['mean', 'std'],
        'avg_velocity': 'mean',
        'pitcher': 'count'
    })

    # Flatten column names
    yearly.columns = ['_'.join(col).strip() for col in yearly.columns.values]
    yearly = yearly.rename(columns={'pitcher_count': 'n_pitchers'})

    print("\nRelease Point Metrics by Year:")
    print(yearly[['consistency_3d_mean', 'horizontal_std_mean', 'release_z_mean_mean']].round(4))

    # Linear regression for consistency trend
    years = yearly.index.values
    consistency = yearly['consistency_3d_mean'].values

    slope, intercept, r_value, p_value, std_err = stats.linregress(years, consistency)

    trend_results = {
        'consistency_3d': {
            'slope': slope,
            'r_squared': r_value**2,
            'p_value': p_value,
            'start_value': yearly.loc[2015, 'consistency_3d_mean'],
            'end_value': yearly.loc[2025, 'consistency_3d_mean']
        }
    }

    print(f"\n3D Consistency Trend: slope={slope:.5f}/year, R²={r_value**2:.3f}, p={p_value:.4f}")

    # Release height trend
    heights = yearly['release_z_mean_mean'].values
    slope_h, _, r_h, p_h, _ = stats.linregress(years, heights)

    trend_results['release_height'] = {
        'slope': slope_h,
        'r_squared': r_h**2,
        'p_value': p_h,
        'start_value': yearly.loc[2015, 'release_z_mean_mean'],
        'end_value': yearly.loc[2025, 'release_z_mean_mean']
    }

    print(f"Release Height Trend: slope={slope_h:.5f} ft/year, R²={r_h**2:.3f}, p={p_h:.4f}")

    return yearly, trend_results


def analyze_consistency_effectiveness(pitcher_df):
    """Analyze relationship between consistency and effectiveness."""
    print("\n--- Consistency vs Effectiveness Analysis ---")

    # Use latest year for most reliable data
    recent = pitcher_df[pitcher_df['game_year'].isin([2023, 2024, 2025])].copy()
    recent = recent.dropna(subset=['consistency_3d', 'woba_allowed'])

    # Correlation between consistency and wOBA
    corr_woba, p_woba = stats.pearsonr(recent['consistency_3d'], recent['woba_allowed'])
    print(f"\nConsistency vs wOBA: r={corr_woba:.3f}, p={p_woba:.4f}")

    # Correlation between consistency and whiff rate
    recent_whiff = recent.dropna(subset=['whiff_rate'])
    corr_whiff, p_whiff = stats.pearsonr(recent_whiff['consistency_3d'], recent_whiff['whiff_rate'])
    print(f"Consistency vs Whiff Rate: r={corr_whiff:.3f}, p={p_whiff:.4f}")

    # Group into quartiles of consistency
    recent['consistency_quartile'] = pd.qcut(recent['consistency_3d'], 4, labels=['Best', 'Good', 'Fair', 'Worst'])

    quartile_stats = recent.groupby('consistency_quartile', observed=True).agg({
        'woba_allowed': 'mean',
        'whiff_rate': 'mean',
        'consistency_3d': 'mean',
        'pitcher': 'count'
    }).round(4)

    print("\nEffectiveness by Consistency Quartile:")
    print(quartile_stats)

    correlation_results = {
        'consistency_vs_woba': {'r': corr_woba, 'p': p_woba},
        'consistency_vs_whiff': {'r': corr_whiff, 'p': p_whiff}
    }

    return correlation_results, quartile_stats


def analyze_by_handedness(pitcher_df):
    """Compare release points by handedness."""
    print("\n--- Handedness Analysis ---")

    for hand in ['R', 'L']:
        hand_data = pitcher_df[pitcher_df['p_throws'] == hand]
        print(f"\n{hand}HP Pitchers ({len(hand_data):,} pitcher-seasons):")
        print(f"  Avg Release X: {hand_data['release_x_mean'].mean():.2f} ft")
        print(f"  Avg Release Z: {hand_data['release_z_mean'].mean():.2f} ft")
        print(f"  Avg Consistency: {hand_data['consistency_3d'].mean():.4f} in")
        print(f"  Arm Angle (est): {hand_data['arm_angle_est'].mean():.1f}°")

    # Compare consistency by handedness over time
    hand_yearly = pitcher_df.groupby(['game_year', 'p_throws'])['consistency_3d'].mean().unstack()
    print("\nConsistency by Handedness over Time:")
    print(hand_yearly.round(4))

    return hand_yearly


def statistical_tests(pitcher_df):
    """Run statistical tests comparing periods."""
    print("\n--- Statistical Tests ---")

    early_years = [2015, 2016, 2017, 2018]
    late_years = [2022, 2023, 2024, 2025]

    tests = []

    # Test 1: 3D Consistency improvement
    early = pitcher_df[pitcher_df['game_year'].isin(early_years)]['consistency_3d']
    late = pitcher_df[pitcher_df['game_year'].isin(late_years)]['consistency_3d']

    t_stat, p_val = stats.ttest_ind(early.astype(float), late.astype(float))
    cohens_d = (early.mean() - late.mean()) / np.sqrt(
        (early.std()**2 + late.std()**2) / 2
    )

    tests.append({
        'test': '3D Consistency (2015-18 vs 2022-25)',
        'early_mean': early.mean(),
        'late_mean': late.mean(),
        'change': late.mean() - early.mean(),
        't_statistic': t_stat,
        'p_value': p_val,
        'cohens_d': cohens_d,
        'interpretation': 'large' if abs(cohens_d) > 0.8 else 'medium' if abs(cohens_d) > 0.5 else 'small' if abs(cohens_d) > 0.2 else 'negligible'
    })

    # Test 2: Release height change
    early_z = pitcher_df[pitcher_df['game_year'].isin(early_years)]['release_z_mean']
    late_z = pitcher_df[pitcher_df['game_year'].isin(late_years)]['release_z_mean']

    t_stat2, p_val2 = stats.ttest_ind(early_z.astype(float), late_z.astype(float))
    cohens_d2 = (late_z.mean() - early_z.mean()) / np.sqrt(
        (early_z.std()**2 + late_z.std()**2) / 2
    )

    tests.append({
        'test': 'Release Height (2015-18 vs 2022-25)',
        'early_mean': early_z.mean(),
        'late_mean': late_z.mean(),
        'change': late_z.mean() - early_z.mean(),
        't_statistic': t_stat2,
        'p_value': p_val2,
        'cohens_d': cohens_d2,
        'interpretation': 'large' if abs(cohens_d2) > 0.8 else 'medium' if abs(cohens_d2) > 0.5 else 'small' if abs(cohens_d2) > 0.2 else 'negligible'
    })

    tests_df = pd.DataFrame(tests)

    for test in tests:
        print(f"\n{test['test']}:")
        print(f"  Early: {test['early_mean']:.4f}, Late: {test['late_mean']:.4f}")
        print(f"  Change: {test['change']:.4f}")
        print(f"  t={test['t_statistic']:.2f}, p={test['p_value']:.4f}")
        print(f"  Cohen's d: {test['cohens_d']:.3f} ({test['interpretation']})")

    return tests_df


def create_visualizations(pitcher_df, yearly, hand_yearly, quartile_stats):
    """Create publication-ready figures."""
    print("\n--- Creating Visualizations ---")

    plt.style.use('seaborn-v0_8-whitegrid')

    # Figure 1: 3D Consistency trend
    fig, ax = plt.subplots(figsize=(10, 6))

    years = yearly.index.values
    consistency = yearly['consistency_3d_mean'].values
    consistency_std = yearly['consistency_3d_std'].values

    ax.plot(years, consistency, 'o-', color='#1f77b4', linewidth=2, markersize=8)
    ax.fill_between(years, consistency - consistency_std, consistency + consistency_std,
                    alpha=0.2, color='#1f77b4')

    # Trend line
    z = np.polyfit(years, consistency, 1)
    p = np.poly1d(z)
    ax.plot(years, p(years), '--', color='red', linewidth=2, label=f'Trend: {z[0]:.4f}/year')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('3D Release Consistency (Std Dev, inches)', fontsize=12)
    ax.set_title('Pitcher Release Point Consistency (2015-2025)\nLower = More Consistent', fontsize=14)
    ax.legend()
    ax.set_xlim(2014.5, 2025.5)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_consistency_trend.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig01_consistency_trend.png")

    # Figure 2: Release height trend
    fig, ax = plt.subplots(figsize=(10, 6))

    heights = yearly['release_z_mean_mean'].values

    ax.plot(years, heights, 'o-', color='#2ca02c', linewidth=2, markersize=8)

    z2 = np.polyfit(years, heights, 1)
    p2 = np.poly1d(z2)
    ax.plot(years, p2(years), '--', color='red', linewidth=2, label=f'Trend: {z2[0]:.4f} ft/year')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Average Release Height (feet)', fontsize=12)
    ax.set_title('Average Pitcher Release Height (2015-2025)', fontsize=14)
    ax.legend()
    ax.set_xlim(2014.5, 2025.5)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig02_release_height.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig02_release_height.png")

    # Figure 3: Consistency by handedness
    fig, ax = plt.subplots(figsize=(10, 6))

    if 'R' in hand_yearly.columns:
        ax.plot(hand_yearly.index, hand_yearly['R'], 'o-', label='RHP', color='#1f77b4', linewidth=2, markersize=8)
    if 'L' in hand_yearly.columns:
        ax.plot(hand_yearly.index, hand_yearly['L'], 's-', label='LHP', color='#ff7f0e', linewidth=2, markersize=8)

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('3D Consistency (Std Dev, inches)', fontsize=12)
    ax.set_title('Release Point Consistency by Handedness', fontsize=14)
    ax.legend()
    ax.set_xlim(2014.5, 2025.5)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig03_consistency_by_hand.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig03_consistency_by_hand.png")

    # Figure 4: Consistency quartiles vs effectiveness
    fig, ax = plt.subplots(figsize=(10, 6))

    quartiles = quartile_stats.index.tolist()
    woba = quartile_stats['woba_allowed'].values

    colors = ['#2ca02c', '#98df8a', '#ffbb78', '#ff7f0e']
    bars = ax.bar(quartiles, woba, color=colors, edgecolor='black')

    ax.set_xlabel('Consistency Quartile', fontsize=12)
    ax.set_ylabel('wOBA Allowed', fontsize=12)
    ax.set_title('Pitcher Effectiveness by Release Consistency (2023-2025)\nLower wOBA = Better', fontsize=14)
    ax.set_ylim(0.30, 0.36)

    # Add value labels
    for bar, val in zip(bars, woba):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
                f'{val:.3f}', ha='center', va='bottom', fontsize=11)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig04_consistency_vs_woba.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig04_consistency_vs_woba.png")


def save_results(pitcher_df, yearly, tests_df, trend_results, correlation_results, quartile_stats):
    """Save all results to CSV files."""
    print("\n--- Saving Results ---")

    # Yearly summary
    yearly.to_csv(f'{RESULTS_DIR}/release_point_by_year.csv')
    print("Saved release_point_by_year.csv")

    # Statistical tests
    tests_df.to_csv(f'{RESULTS_DIR}/statistical_tests.csv', index=False)
    print("Saved statistical_tests.csv")

    # Quartile stats
    quartile_stats.to_csv(f'{RESULTS_DIR}/effectiveness_by_consistency.csv')
    print("Saved effectiveness_by_consistency.csv")

    # Top consistent pitchers (2025)
    top_consistent = pitcher_df[pitcher_df['game_year'] == 2025].nsmallest(20, 'consistency_3d')[
        ['pitcher', 'n_pitches', 'consistency_3d', 'woba_allowed', 'avg_velocity']
    ]
    top_consistent.to_csv(f'{RESULTS_DIR}/most_consistent_2025.csv', index=False)
    print("Saved most_consistent_2025.csv")

    # Summary
    summary = {
        'metric': [],
        'value_2015': [],
        'value_2025': [],
        'change': [],
        'interpretation': []
    }

    # 3D Consistency
    summary['metric'].append('3D Release Consistency (StdDev)')
    summary['value_2015'].append(f"{trend_results['consistency_3d']['start_value']:.4f}")
    summary['value_2025'].append(f"{trend_results['consistency_3d']['end_value']:.4f}")
    change = trend_results['consistency_3d']['end_value'] - trend_results['consistency_3d']['start_value']
    summary['change'].append(f"{change:.4f}")
    summary['interpretation'].append('Improved (lower)' if change < 0 else 'Declined (higher)')

    # Release height
    summary['metric'].append('Average Release Height (ft)')
    summary['value_2015'].append(f"{trend_results['release_height']['start_value']:.3f}")
    summary['value_2025'].append(f"{trend_results['release_height']['end_value']:.3f}")
    change_h = trend_results['release_height']['end_value'] - trend_results['release_height']['start_value']
    summary['change'].append(f"{change_h:.3f}")
    summary['interpretation'].append('Higher release point' if change_h > 0 else 'Lower release point')

    # Correlation
    summary['metric'].append('Consistency-wOBA Correlation')
    summary['value_2015'].append('N/A')
    summary['value_2025'].append(f"r={correlation_results['consistency_vs_woba']['r']:.3f}")
    summary['change'].append('N/A')

    if correlation_results['consistency_vs_woba']['r'] > 0:
        summary['interpretation'].append('More consistent = lower wOBA')
    else:
        summary['interpretation'].append('Less consistent = lower wOBA')

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(f'{RESULTS_DIR}/summary.csv', index=False)
    print("Saved summary.csv")


def main():
    """Execute complete release point analysis."""
    print("=" * 60)
    print("Chapter 13: Release Point Consistency")
    print("=" * 60)

    # Load data
    df = load_data()

    # Calculate pitcher metrics
    pitcher_df = calculate_pitcher_metrics(df)

    # Analyze trends
    yearly, trend_results = analyze_trends(pitcher_df)

    # Consistency vs effectiveness
    correlation_results, quartile_stats = analyze_consistency_effectiveness(pitcher_df)

    # Handedness analysis
    hand_yearly = analyze_by_handedness(pitcher_df)

    # Statistical tests
    tests_df = statistical_tests(pitcher_df)

    # Create visualizations
    create_visualizations(pitcher_df, yearly, hand_yearly, quartile_stats)

    # Save results
    save_results(pitcher_df, yearly, tests_df, trend_results, correlation_results, quartile_stats)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"\nTotal pitcher-seasons analyzed: {len(pitcher_df):,}")

    rc = trend_results['consistency_3d']
    rh = trend_results['release_height']

    print(f"\n3D Release Consistency:")
    print(f"  2015: {rc['start_value']:.4f} inches")
    print(f"  2025: {rc['end_value']:.4f} inches")
    print(f"  Trend: {rc['slope']:.5f}/year (R²={rc['r_squared']:.3f})")

    print(f"\nRelease Height:")
    print(f"  2015: {rh['start_value']:.3f} feet")
    print(f"  2025: {rh['end_value']:.3f} feet")
    print(f"  Trend: {rh['slope']:.4f} ft/year")

    print(f"\nConsistency-Effectiveness Correlation: r={correlation_results['consistency_vs_woba']['r']:.3f}")

    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
