#!/usr/bin/env python3
"""
Chapter 11: Tunneling Effect Analysis (2015-2025)

Research Question: How has pitch tunneling evolved, and do pitchers
with tighter tunnels generate better results?

Tunneling = throwing different pitch types through similar release points
and early trajectory paths, making it hard for batters to identify pitch type.

Key Metrics:
- Release point consistency (std dev of release_pos)
- Tunnel tightness (separation at ~25 ft from plate)
- Comparison across pitch type combinations
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/Users/mksong/Documents/mlb-statcast-book')

from src.statcast_analysis import load_seasons

# Configuration
FIGURES_DIR = '/Users/mksong/Documents/mlb-statcast-book/chapters/11_tunneling/figures'
RESULTS_DIR = '/Users/mksong/Documents/mlb-statcast-book/chapters/11_tunneling/results'
MIN_PITCHES_PER_PITCHER = 100  # Minimum sample for inclusion


def load_data():
    """Load all seasons with release point and location data."""
    print("Loading data...")
    columns = [
        'game_year', 'pitcher', 'pitch_type', 'pitch_name',
        'release_pos_x', 'release_pos_y', 'release_pos_z',
        'plate_x', 'plate_z',
        'release_speed', 'release_spin_rate',
        'pfx_x', 'pfx_z',
        'events', 'description', 'type'
    ]

    df = load_seasons(2015, 2025, columns=columns)
    print(f"Loaded {len(df):,} total pitches")

    # Clean data - need valid release position and plate location
    df = df.dropna(subset=['release_pos_x', 'release_pos_y', 'release_pos_z',
                           'plate_x', 'plate_z'])
    print(f"After cleaning: {len(df):,} pitches")

    return df


def calculate_release_consistency(df):
    """
    Calculate release point consistency for each pitcher-year.
    Lower std dev = more consistent release = better tunneling potential.
    """
    print("\n--- Calculating Release Point Consistency ---")

    # Group by pitcher and year
    results = []

    for (year, pitcher), group in df.groupby(['game_year', 'pitcher']):
        if len(group) < MIN_PITCHES_PER_PITCHER:
            continue

        # Calculate standard deviation of release points
        x_std = group['release_pos_x'].std()
        y_std = group['release_pos_y'].std()
        z_std = group['release_pos_z'].std()

        # Combined 3D release consistency (lower = better)
        release_consistency = np.sqrt(x_std**2 + y_std**2 + z_std**2)

        # Mean release position
        x_mean = group['release_pos_x'].mean()
        y_mean = group['release_pos_y'].mean()
        z_mean = group['release_pos_z'].mean()

        results.append({
            'game_year': year,
            'pitcher': pitcher,
            'n_pitches': len(group),
            'release_x_mean': x_mean,
            'release_y_mean': y_mean,
            'release_z_mean': z_mean,
            'release_x_std': x_std,
            'release_y_std': y_std,
            'release_z_std': z_std,
            'release_consistency': release_consistency
        })

    release_df = pd.DataFrame(results)
    print(f"Analyzed {len(release_df):,} pitcher-seasons")

    return release_df


def calculate_pitch_type_tunnel(df):
    """
    Calculate tunneling metrics between pitch type pairs.
    Compare release points and early trajectory for FB vs breaking ball.
    """
    print("\n--- Calculating Pitch Type Tunneling ---")

    # Categorize pitches
    fastballs = ['FF', 'SI', 'FC']
    breaking = ['SL', 'CU', 'ST', 'KC']
    offspeed = ['CH', 'FS']

    results = []

    for (year, pitcher), group in df.groupby(['game_year', 'pitcher']):
        if len(group) < MIN_PITCHES_PER_PITCHER:
            continue

        fb_data = group[group['pitch_type'].isin(fastballs)]
        br_data = group[group['pitch_type'].isin(breaking)]

        if len(fb_data) < 20 or len(br_data) < 20:
            continue

        # Release point separation between FB and breaking balls
        fb_release = fb_data[['release_pos_x', 'release_pos_y', 'release_pos_z']].mean()
        br_release = br_data[['release_pos_x', 'release_pos_y', 'release_pos_z']].mean()

        release_separation = np.sqrt(
            (fb_release['release_pos_x'] - br_release['release_pos_x'])**2 +
            (fb_release['release_pos_y'] - br_release['release_pos_y'])**2 +
            (fb_release['release_pos_z'] - br_release['release_pos_z'])**2
        )

        # Plate location separation (final separation)
        fb_plate = fb_data[['plate_x', 'plate_z']].mean()
        br_plate = br_data[['plate_x', 'plate_z']].mean()

        plate_separation = np.sqrt(
            (fb_plate['plate_x'] - br_plate['plate_x'])**2 +
            (fb_plate['plate_z'] - br_plate['plate_z'])**2
        )

        results.append({
            'game_year': year,
            'pitcher': pitcher,
            'n_fb': len(fb_data),
            'n_br': len(br_data),
            'release_separation': release_separation,  # Lower = better tunnel
            'plate_separation': plate_separation,      # Higher = more deception
        })

    tunnel_df = pd.DataFrame(results)
    print(f"Analyzed {len(tunnel_df):,} pitcher-seasons with FB-breaking combos")

    return tunnel_df


def analyze_trends(release_df, tunnel_df):
    """Analyze year-over-year trends in tunneling metrics."""
    print("\n--- Analyzing Trends ---")

    results = {}

    # 1. Release consistency trend
    yearly_consistency = release_df.groupby('game_year')['release_consistency'].agg(['mean', 'median', 'std'])
    print("\nRelease Consistency by Year (lower = better tunneling):")
    print(yearly_consistency.round(4))

    # Linear regression for release consistency
    years = yearly_consistency.index.values
    means = yearly_consistency['mean'].values
    slope, intercept, r_value, p_value, std_err = stats.linregress(years, means)

    results['release_consistency'] = {
        'slope': slope,
        'r_squared': r_value**2,
        'p_value': p_value,
        'start_value': yearly_consistency.loc[2015, 'mean'] if 2015 in yearly_consistency.index else means[0],
        'end_value': yearly_consistency.loc[2025, 'mean'] if 2025 in yearly_consistency.index else means[-1]
    }

    print(f"\nRelease Consistency Trend: slope={slope:.5f} inches/year, R²={r_value**2:.3f}, p={p_value:.4f}")

    # 2. FB-Breaking release separation trend
    yearly_separation = tunnel_df.groupby('game_year')['release_separation'].agg(['mean', 'median', 'std'])
    print("\nFB-Breaking Release Separation by Year (lower = better tunnel):")
    print(yearly_separation.round(4))

    years2 = yearly_separation.index.values
    means2 = yearly_separation['mean'].values
    slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(years2, means2)

    results['release_separation'] = {
        'slope': slope2,
        'r_squared': r_value2**2,
        'p_value': p_value2,
        'start_value': yearly_separation.loc[2015, 'mean'] if 2015 in yearly_separation.index else means2[0],
        'end_value': yearly_separation.loc[2025, 'mean'] if 2025 in yearly_separation.index else means2[-1]
    }

    print(f"\nRelease Separation Trend: slope={slope2:.5f} inches/year, R²={r_value2**2:.3f}, p={p_value2:.4f}")

    return results, yearly_consistency, yearly_separation


def statistical_tests(release_df, tunnel_df):
    """Run statistical tests comparing early vs late period."""
    print("\n--- Statistical Tests ---")

    early_years = [2015, 2016, 2017, 2018]
    late_years = [2022, 2023, 2024, 2025]

    tests = []

    # Test 1: Release consistency improvement
    early_consistency = release_df[release_df['game_year'].isin(early_years)]['release_consistency']
    late_consistency = release_df[release_df['game_year'].isin(late_years)]['release_consistency']

    t_stat, p_val = stats.ttest_ind(early_consistency.astype(float), late_consistency.astype(float))
    cohens_d = (early_consistency.mean() - late_consistency.mean()) / np.sqrt(
        (early_consistency.std()**2 + late_consistency.std()**2) / 2
    )

    tests.append({
        'test': 'Release Consistency (2015-18 vs 2022-25)',
        'early_mean': early_consistency.mean(),
        'late_mean': late_consistency.mean(),
        'change': late_consistency.mean() - early_consistency.mean(),
        't_statistic': t_stat,
        'p_value': p_val,
        'cohens_d': cohens_d,
        'interpretation': 'large' if abs(cohens_d) > 0.8 else 'medium' if abs(cohens_d) > 0.5 else 'small' if abs(cohens_d) > 0.2 else 'negligible'
    })

    # Test 2: FB-Breaking separation
    early_sep = tunnel_df[tunnel_df['game_year'].isin(early_years)]['release_separation']
    late_sep = tunnel_df[tunnel_df['game_year'].isin(late_years)]['release_separation']

    t_stat2, p_val2 = stats.ttest_ind(early_sep.astype(float), late_sep.astype(float))
    cohens_d2 = (early_sep.mean() - late_sep.mean()) / np.sqrt(
        (early_sep.std()**2 + late_sep.std()**2) / 2
    )

    tests.append({
        'test': 'FB-Breaking Release Separation (2015-18 vs 2022-25)',
        'early_mean': early_sep.mean(),
        'late_mean': late_sep.mean(),
        'change': late_sep.mean() - early_sep.mean(),
        't_statistic': t_stat2,
        'p_value': p_val2,
        'cohens_d': cohens_d2,
        'interpretation': 'large' if abs(cohens_d2) > 0.8 else 'medium' if abs(cohens_d2) > 0.5 else 'small' if abs(cohens_d2) > 0.2 else 'negligible'
    })

    for test in tests:
        print(f"\n{test['test']}:")
        print(f"  Early: {test['early_mean']:.4f}, Late: {test['late_mean']:.4f}")
        print(f"  Change: {test['change']:.4f}")
        print(f"  t={test['t_statistic']:.2f}, p={test['p_value']:.4f}")
        print(f"  Cohen's d: {test['cohens_d']:.3f} ({test['interpretation']})")

    return pd.DataFrame(tests)


def create_visualizations(release_df, tunnel_df, yearly_consistency, yearly_separation):
    """Create publication-ready figures."""
    print("\n--- Creating Visualizations ---")

    plt.style.use('seaborn-v0_8-whitegrid')

    # Figure 1: Release consistency trend
    fig, ax = plt.subplots(figsize=(10, 6))

    years = yearly_consistency.index.values
    means = yearly_consistency['mean'].values
    stds = yearly_consistency['std'].values

    ax.plot(years, means, 'o-', color='#1f77b4', linewidth=2, markersize=8, label='Mean')
    ax.fill_between(years, means - stds, means + stds, alpha=0.2, color='#1f77b4')

    # Trend line
    z = np.polyfit(years, means, 1)
    p = np.poly1d(z)
    ax.plot(years, p(years), '--', color='red', linewidth=2, label=f'Trend (slope: {z[0]:.4f})')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Release Consistency (3D Std Dev, inches)', fontsize=12)
    ax.set_title('Pitcher Release Point Consistency (2015-2025)\nLower = More Consistent', fontsize=14)
    ax.legend()
    ax.set_xlim(2014.5, 2025.5)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_release_consistency.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig01_release_consistency.png")

    # Figure 2: FB-Breaking release separation
    fig, ax = plt.subplots(figsize=(10, 6))

    years2 = yearly_separation.index.values
    means2 = yearly_separation['mean'].values
    stds2 = yearly_separation['std'].values

    ax.plot(years2, means2, 'o-', color='#2ca02c', linewidth=2, markersize=8, label='Mean')
    ax.fill_between(years2, means2 - stds2, means2 + stds2, alpha=0.2, color='#2ca02c')

    # Trend line
    z2 = np.polyfit(years2, means2, 1)
    p2 = np.poly1d(z2)
    ax.plot(years2, p2(years2), '--', color='red', linewidth=2, label=f'Trend (slope: {z2[0]:.4f})')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('FB-Breaking Release Separation (inches)', fontsize=12)
    ax.set_title('Fastball vs Breaking Ball Release Point Separation\nLower = Better Tunneling', fontsize=14)
    ax.legend()
    ax.set_xlim(2014.5, 2025.5)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig02_fb_breaking_separation.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig02_fb_breaking_separation.png")

    # Figure 3: Release consistency distribution comparison (2015 vs 2025)
    fig, ax = plt.subplots(figsize=(10, 6))

    cons_2015 = release_df[release_df['game_year'] == 2015]['release_consistency']
    cons_2025 = release_df[release_df['game_year'] == 2025]['release_consistency']

    ax.hist(cons_2015, bins=40, alpha=0.5, label=f'2015 (mean: {cons_2015.mean():.3f})', color='#1f77b4')
    ax.hist(cons_2025, bins=40, alpha=0.5, label=f'2025 (mean: {cons_2025.mean():.3f})', color='#ff7f0e')

    ax.set_xlabel('Release Consistency (3D Std Dev, inches)', fontsize=12)
    ax.set_ylabel('Number of Pitchers', fontsize=12)
    ax.set_title('Release Consistency Distribution: 2015 vs 2025', fontsize=14)
    ax.legend()

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig03_consistency_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig03_consistency_distribution.png")

    # Figure 4: Heatmap of release point (sample pitcher)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Get a sample pitcher with good data from 2025
    sample_year = 2025
    sample_data = release_df[release_df['game_year'] == sample_year].nlargest(1, 'n_pitches')

    ax1 = axes[0]
    ax1.scatter(release_df['release_x_std'], release_df['release_z_std'],
                alpha=0.3, s=10, c=release_df['game_year'], cmap='viridis')
    ax1.set_xlabel('Horizontal Release Std Dev (inches)', fontsize=12)
    ax1.set_ylabel('Vertical Release Std Dev (inches)', fontsize=12)
    ax1.set_title('Release Point Consistency (All Pitchers)', fontsize=14)

    ax2 = axes[1]
    scatter = ax2.scatter(tunnel_df['release_separation'], tunnel_df['plate_separation'],
                          alpha=0.3, s=10, c=tunnel_df['game_year'], cmap='viridis')
    ax2.set_xlabel('Release Point Separation (inches)', fontsize=12)
    ax2.set_ylabel('Plate Location Separation (feet)', fontsize=12)
    ax2.set_title('FB-Breaking Ball: Release vs Plate Separation', fontsize=14)
    plt.colorbar(scatter, ax=ax2, label='Year')

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig04_tunnel_scatter.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig04_tunnel_scatter.png")


def save_results(release_df, tunnel_df, tests_df, trend_results, yearly_consistency, yearly_separation):
    """Save all results to CSV files."""
    print("\n--- Saving Results ---")

    # Yearly release consistency
    yearly_consistency.to_csv(f'{RESULTS_DIR}/release_consistency_by_year.csv')
    print("Saved release_consistency_by_year.csv")

    # Yearly FB-breaking separation
    yearly_separation.to_csv(f'{RESULTS_DIR}/fb_breaking_separation_by_year.csv')
    print("Saved fb_breaking_separation_by_year.csv")

    # Statistical tests
    tests_df.to_csv(f'{RESULTS_DIR}/statistical_tests.csv', index=False)
    print("Saved statistical_tests.csv")

    # Summary
    summary = {
        'metric': [],
        'value_2015': [],
        'value_2025': [],
        'change': [],
        'trend_slope': [],
        'r_squared': [],
        'p_value': [],
        'interpretation': []
    }

    # Release consistency
    rc = trend_results['release_consistency']
    summary['metric'].append('Release Consistency (3D StdDev)')
    summary['value_2015'].append(f"{rc['start_value']:.4f}")
    summary['value_2025'].append(f"{rc['end_value']:.4f}")
    summary['change'].append(f"{rc['end_value'] - rc['start_value']:.4f}")
    summary['trend_slope'].append(f"{rc['slope']:.5f}/year")
    summary['r_squared'].append(f"{rc['r_squared']:.3f}")
    summary['p_value'].append(f"{rc['p_value']:.4f}")

    # Interpret trend
    if rc['p_value'] < 0.05:
        if rc['slope'] < 0:
            interp = "Significant improvement (more consistent)"
        else:
            interp = "Significant decline (less consistent)"
    else:
        interp = "No significant trend"
    summary['interpretation'].append(interp)

    # FB-Breaking separation
    rs = trend_results['release_separation']
    summary['metric'].append('FB-Breaking Release Separation')
    summary['value_2015'].append(f"{rs['start_value']:.4f}")
    summary['value_2025'].append(f"{rs['end_value']:.4f}")
    summary['change'].append(f"{rs['end_value'] - rs['start_value']:.4f}")
    summary['trend_slope'].append(f"{rs['slope']:.5f}/year")
    summary['r_squared'].append(f"{rs['r_squared']:.3f}")
    summary['p_value'].append(f"{rs['p_value']:.4f}")

    if rs['p_value'] < 0.05:
        if rs['slope'] < 0:
            interp = "Significant improvement (better tunneling)"
        else:
            interp = "Significant decline (worse tunneling)"
    else:
        interp = "No significant trend"
    summary['interpretation'].append(interp)

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(f'{RESULTS_DIR}/summary.csv', index=False)
    print("Saved summary.csv")

    # Top tunnelers sample (2025)
    top_tunnelers = release_df[release_df['game_year'] == 2025].nsmallest(20, 'release_consistency')[
        ['pitcher', 'n_pitches', 'release_consistency', 'release_x_std', 'release_z_std']
    ]
    top_tunnelers.to_csv(f'{RESULTS_DIR}/top_tunnelers_2025.csv', index=False)
    print("Saved top_tunnelers_2025.csv")


def main():
    """Execute complete tunneling analysis."""
    print("=" * 60)
    print("Chapter 11: Tunneling Effect Analysis")
    print("=" * 60)

    # Load data
    df = load_data()

    # Calculate metrics
    release_df = calculate_release_consistency(df)
    tunnel_df = calculate_pitch_type_tunnel(df)

    # Analyze trends
    trend_results, yearly_consistency, yearly_separation = analyze_trends(release_df, tunnel_df)

    # Statistical tests
    tests_df = statistical_tests(release_df, tunnel_df)

    # Create visualizations
    create_visualizations(release_df, tunnel_df, yearly_consistency, yearly_separation)

    # Save results
    save_results(release_df, tunnel_df, tests_df, trend_results, yearly_consistency, yearly_separation)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nTotal pitcher-seasons analyzed: {len(release_df):,}")
    print(f"Pitcher-seasons with FB-breaking combos: {len(tunnel_df):,}")

    rc = trend_results['release_consistency']
    rs = trend_results['release_separation']

    print(f"\nRelease Consistency:")
    print(f"  2015: {rc['start_value']:.4f} inches")
    print(f"  2025: {rc['end_value']:.4f} inches")
    print(f"  Trend: {rc['slope']:.5f}/year (R²={rc['r_squared']:.3f}, p={rc['p_value']:.4f})")

    print(f"\nFB-Breaking Release Separation:")
    print(f"  2015: {rs['start_value']:.4f} inches")
    print(f"  2025: {rs['end_value']:.4f} inches")
    print(f"  Trend: {rs['slope']:.5f}/year (R²={rs['r_squared']:.3f}, p={rs['p_value']:.4f})")

    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
