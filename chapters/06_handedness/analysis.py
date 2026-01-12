#!/usr/bin/env python3
"""
Chapter 6: L/R Pitcher Differences (2015-2025)

Research Question: How do left-handed and right-handed pitchers differ
in pitch characteristics, and have these differences changed over time?

Hypotheses:
- H0: No significant difference between LHP and RHP pitch characteristics
- H1: Significant differences exist in velocity, movement, or pitch mix

Key Analyses:
1. LHP vs RHP velocity comparison
2. Movement profile differences by handedness
3. Pitch type usage by handedness
4. Trend in LHP/RHP ratio over time

Usage:
    python analysis.py
"""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from statcast_analysis import load_season, AVAILABLE_SEASONS

# Output directories
FIGURES_DIR = Path(__file__).parent / "figures"
RESULTS_DIR = Path(__file__).parent / "results"
FIGURES_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# Plot style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Analysis periods for comparison
EARLY_PERIOD = [2015, 2016, 2017]
LATE_PERIOD = [2023, 2024, 2025]

# Primary pitch types for analysis
PRIMARY_PITCHES = {
    'FF': '4-Seam Fastball',
    'SI': 'Sinker',
    'SL': 'Slider',
    'CU': 'Curveball',
    'CH': 'Changeup',
}


def interpret_cohens_d(d):
    """Interpret Cohen's d effect size."""
    d = abs(d)
    if d < 0.2:
        return "negligible"
    elif d < 0.5:
        return "small"
    elif d < 0.8:
        return "medium"
    else:
        return "large"


def interpret_r_squared(r2):
    """Interpret R-squared value."""
    if r2 < 0.1:
        return "weak"
    elif r2 < 0.3:
        return "moderate"
    elif r2 < 0.5:
        return "substantial"
    else:
        return "strong"


def interpret_p_value(p):
    """Interpret p-value for significance."""
    if p < 0.001:
        return "highly significant"
    elif p < 0.01:
        return "very significant"
    elif p < 0.05:
        return "significant"
    else:
        return "not significant"


def load_handedness_data():
    """Load pitch data with handedness information."""
    print("=" * 60)
    print("  Chapter 6: L/R Pitcher Differences (2015-2025)")
    print("=" * 60)
    print("\n[1] Loading pitch data with handedness...")

    all_data = []

    for year in AVAILABLE_SEASONS:
        try:
            df = load_season(year, columns=[
                'pitch_type', 'release_speed', 'release_spin_rate',
                'pfx_x', 'pfx_z', 'p_throws', 'pitcher'
            ])
            df['game_year'] = year

            # Ensure numeric types
            df['release_speed'] = pd.to_numeric(df['release_speed'], errors='coerce')
            df['release_spin_rate'] = pd.to_numeric(df['release_spin_rate'], errors='coerce')
            df['pfx_x'] = pd.to_numeric(df['pfx_x'], errors='coerce')
            df['pfx_z'] = pd.to_numeric(df['pfx_z'], errors='coerce')

            # Filter to valid data with handedness
            df = df.dropna(subset=['p_throws', 'pitch_type'])

            all_data.append(df)

            # Count by handedness
            lhp = (df['p_throws'] == 'L').sum()
            rhp = (df['p_throws'] == 'R').sum()
            print(f"  {year}: LHP={lhp:,} ({lhp/(lhp+rhp)*100:.1f}%), RHP={rhp:,} ({rhp/(lhp+rhp)*100:.1f}%)")

        except FileNotFoundError:
            print(f"  {year}: data not found, skipping")
            continue

    combined = pd.concat(all_data, ignore_index=True)
    print(f"\n  Total pitches: {len(combined):,}")

    return combined


def analyze_handedness_by_year(df: pd.DataFrame):
    """Calculate yearly statistics by handedness."""
    print("\n[2] Calculating yearly statistics by handedness...")

    results = []

    for year in df['game_year'].unique():
        year_data = df[df['game_year'] == year]

        for hand in ['L', 'R']:
            hand_data = year_data[year_data['p_throws'] == hand]

            # Overall stats
            n_pitches = len(hand_data)
            n_pitchers = hand_data['pitcher'].nunique()

            # 4-seam fastball stats
            ff_data = hand_data[hand_data['pitch_type'] == 'FF']
            ff_velo = ff_data['release_speed'].dropna()
            ff_spin = ff_data['release_spin_rate'].dropna()

            results.append({
                'year': year,
                'hand': hand,
                'n_pitches': n_pitches,
                'n_pitchers': n_pitchers,
                'pct_of_total': n_pitches / len(year_data) * 100,
                'ff_velo_mean': ff_velo.mean() if len(ff_velo) > 0 else np.nan,
                'ff_velo_std': ff_velo.std() if len(ff_velo) > 0 else np.nan,
                'ff_spin_mean': ff_spin.mean() if len(ff_spin) > 0 else np.nan,
                'ff_spin_std': ff_spin.std() if len(ff_spin) > 0 else np.nan,
                'ff_count': len(ff_velo),
            })

    results_df = pd.DataFrame(results)

    # Print summary
    print("\n  Yearly LHP vs RHP 4-Seam Fastball Velocity:")
    for year in sorted(results_df['year'].unique()):
        lhp = results_df[(results_df['year'] == year) & (results_df['hand'] == 'L')].iloc[0]
        rhp = results_df[(results_df['year'] == year) & (results_df['hand'] == 'R')].iloc[0]
        diff = rhp['ff_velo_mean'] - lhp['ff_velo_mean']
        print(f"    {int(year)}: LHP={lhp['ff_velo_mean']:.2f}, RHP={rhp['ff_velo_mean']:.2f}, Diff={diff:+.2f} mph")

    return results_df


def analyze_pitch_mix_by_handedness(df: pd.DataFrame):
    """Analyze pitch type usage differences by handedness."""
    print("\n[3] Analyzing pitch mix by handedness...")

    pitch_mix_results = []

    for year in df['game_year'].unique():
        year_data = df[df['game_year'] == year]

        for hand in ['L', 'R']:
            hand_data = year_data[year_data['p_throws'] == hand]
            total = len(hand_data)

            for pitch_code in PRIMARY_PITCHES.keys():
                pitch_count = (hand_data['pitch_type'] == pitch_code).sum()
                pitch_mix_results.append({
                    'year': year,
                    'hand': hand,
                    'pitch_type': pitch_code,
                    'count': pitch_count,
                    'pct': pitch_count / total * 100 if total > 0 else 0,
                })

    pitch_mix_df = pd.DataFrame(pitch_mix_results)

    # Print summary for 2025
    print("\n  2025 Pitch Mix by Handedness:")
    recent = pitch_mix_df[pitch_mix_df['year'] == 2025]
    for pitch_code, pitch_name in PRIMARY_PITCHES.items():
        lhp_pct = recent[(recent['hand'] == 'L') & (recent['pitch_type'] == pitch_code)]['pct'].values
        rhp_pct = recent[(recent['hand'] == 'R') & (recent['pitch_type'] == pitch_code)]['pct'].values
        if len(lhp_pct) > 0 and len(rhp_pct) > 0:
            print(f"    {pitch_name}: LHP={lhp_pct[0]:.1f}%, RHP={rhp_pct[0]:.1f}%")

    return pitch_mix_df


def analyze_movement_by_handedness(df: pd.DataFrame):
    """Analyze pitch movement differences by handedness."""
    print("\n[4] Analyzing movement by handedness...")

    movement_results = []

    # Focus on 4-seam fastballs
    ff_data = df[df['pitch_type'] == 'FF'].copy()

    for year in ff_data['game_year'].unique():
        year_data = ff_data[ff_data['game_year'] == year]

        for hand in ['L', 'R']:
            hand_data = year_data[year_data['p_throws'] == hand]

            pfx_x = hand_data['pfx_x'].dropna()
            pfx_z = hand_data['pfx_z'].dropna()

            if len(pfx_x) > 0:
                movement_results.append({
                    'year': year,
                    'hand': hand,
                    'pfx_x_mean': pfx_x.mean(),
                    'pfx_x_std': pfx_x.std(),
                    'pfx_z_mean': pfx_z.mean(),
                    'pfx_z_std': pfx_z.std(),
                    'count': len(pfx_x),
                })

    movement_df = pd.DataFrame(movement_results)

    # Print 2025 comparison
    print("\n  2025 4-Seam Fastball Movement by Handedness:")
    recent = movement_df[movement_df['year'] == 2025]
    for hand in ['L', 'R']:
        data = recent[recent['hand'] == hand].iloc[0]
        label = "Left-handed" if hand == 'L' else "Right-handed"
        print(f"    {label}: H-Break={data['pfx_x_mean']:+.2f}in, V-Break={data['pfx_z_mean']:+.2f}in")

    return movement_df


def perform_statistical_comparison(df: pd.DataFrame):
    """Perform statistical tests comparing LHP vs RHP."""
    print("\n[5] Statistical Comparison (LHP vs RHP)...")

    # Filter to 4-seam fastballs with valid data
    ff_data = df[(df['pitch_type'] == 'FF')].copy()

    lhp = ff_data[ff_data['p_throws'] == 'L']
    rhp = ff_data[ff_data['p_throws'] == 'R']

    comparison_results = {}

    # Velocity comparison
    lhp_velo = lhp['release_speed'].dropna().astype(float)
    rhp_velo = rhp['release_speed'].dropna().astype(float)

    t_stat, p_value = stats.ttest_ind(lhp_velo, rhp_velo)
    pooled_std = np.sqrt(((len(lhp_velo)-1)*lhp_velo.std()**2 +
                          (len(rhp_velo)-1)*rhp_velo.std()**2) /
                         (len(lhp_velo) + len(rhp_velo) - 2))
    cohens_d = (rhp_velo.mean() - lhp_velo.mean()) / pooled_std

    comparison_results['velocity'] = {
        'lhp_mean': lhp_velo.mean(),
        'lhp_std': lhp_velo.std(),
        'lhp_n': len(lhp_velo),
        'rhp_mean': rhp_velo.mean(),
        'rhp_std': rhp_velo.std(),
        'rhp_n': len(rhp_velo),
        'difference': rhp_velo.mean() - lhp_velo.mean(),
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'effect_interpretation': interpret_cohens_d(cohens_d),
    }

    print(f"\n  4-Seam Fastball Velocity:")
    print(f"    LHP: {lhp_velo.mean():.2f} mph (SD={lhp_velo.std():.2f}, n={len(lhp_velo):,})")
    print(f"    RHP: {rhp_velo.mean():.2f} mph (SD={rhp_velo.std():.2f}, n={len(rhp_velo):,})")
    print(f"    Difference: {rhp_velo.mean() - lhp_velo.mean():+.2f} mph")
    print(f"    Cohen's d: {cohens_d:.3f} ({interpret_cohens_d(cohens_d)} effect)")
    print(f"    p-value: {p_value:.2e} ({interpret_p_value(p_value)})")

    # Spin rate comparison
    lhp_spin = lhp['release_spin_rate'].dropna().astype(float)
    rhp_spin = rhp['release_spin_rate'].dropna().astype(float)

    t_stat, p_value = stats.ttest_ind(lhp_spin, rhp_spin)
    pooled_std = np.sqrt(((len(lhp_spin)-1)*lhp_spin.std()**2 +
                          (len(rhp_spin)-1)*rhp_spin.std()**2) /
                         (len(lhp_spin) + len(rhp_spin) - 2))
    cohens_d = (rhp_spin.mean() - lhp_spin.mean()) / pooled_std

    comparison_results['spin_rate'] = {
        'lhp_mean': lhp_spin.mean(),
        'lhp_std': lhp_spin.std(),
        'lhp_n': len(lhp_spin),
        'rhp_mean': rhp_spin.mean(),
        'rhp_std': rhp_spin.std(),
        'rhp_n': len(rhp_spin),
        'difference': rhp_spin.mean() - lhp_spin.mean(),
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'effect_interpretation': interpret_cohens_d(cohens_d),
    }

    print(f"\n  4-Seam Fastball Spin Rate:")
    print(f"    LHP: {lhp_spin.mean():.0f} rpm (SD={lhp_spin.std():.0f}, n={len(lhp_spin):,})")
    print(f"    RHP: {rhp_spin.mean():.0f} rpm (SD={rhp_spin.std():.0f}, n={len(rhp_spin):,})")
    print(f"    Difference: {rhp_spin.mean() - lhp_spin.mean():+.0f} rpm")
    print(f"    Cohen's d: {cohens_d:.3f} ({interpret_cohens_d(cohens_d)} effect)")

    # Horizontal movement comparison (note: LHP and RHP have opposite natural movement)
    lhp_pfx_x = lhp['pfx_x'].dropna().astype(float)
    rhp_pfx_x = rhp['pfx_x'].dropna().astype(float)

    # For comparison, use absolute values to compare magnitude
    lhp_pfx_x_abs = lhp_pfx_x.abs()
    rhp_pfx_x_abs = rhp_pfx_x.abs()

    t_stat, p_value = stats.ttest_ind(lhp_pfx_x_abs, rhp_pfx_x_abs)
    pooled_std = np.sqrt(((len(lhp_pfx_x_abs)-1)*lhp_pfx_x_abs.std()**2 +
                          (len(rhp_pfx_x_abs)-1)*rhp_pfx_x_abs.std()**2) /
                         (len(lhp_pfx_x_abs) + len(rhp_pfx_x_abs) - 2))
    cohens_d = (rhp_pfx_x_abs.mean() - lhp_pfx_x_abs.mean()) / pooled_std

    comparison_results['h_break_magnitude'] = {
        'lhp_mean': lhp_pfx_x.mean(),
        'lhp_abs_mean': lhp_pfx_x_abs.mean(),
        'rhp_mean': rhp_pfx_x.mean(),
        'rhp_abs_mean': rhp_pfx_x_abs.mean(),
        'difference': rhp_pfx_x_abs.mean() - lhp_pfx_x_abs.mean(),
        'cohens_d': cohens_d,
        'effect_interpretation': interpret_cohens_d(cohens_d),
    }

    print(f"\n  Horizontal Movement:")
    print(f"    LHP: {lhp_pfx_x.mean():+.2f}in (magnitude={lhp_pfx_x_abs.mean():.2f}in)")
    print(f"    RHP: {rhp_pfx_x.mean():+.2f}in (magnitude={rhp_pfx_x_abs.mean():.2f}in)")
    print(f"    Note: LHP/RHP have mirrored movement directions")

    return comparison_results


def analyze_lhp_ratio_trend(results_df: pd.DataFrame):
    """Analyze trend in LHP ratio over time."""
    print("\n[6] LHP Ratio Trend Analysis...")

    lhp_data = results_df[results_df['hand'] == 'L'].sort_values('year')
    years = lhp_data['year'].values
    lhp_pct = lhp_data['pct_of_total'].values

    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(years, lhp_pct)
    r_squared = r_value ** 2

    trend_results = {
        'slope': slope,
        'slope_ci_lower': slope - 1.96 * std_err,
        'slope_ci_upper': slope + 1.96 * std_err,
        'intercept': intercept,
        'r_squared': r_squared,
        'p_value': p_value,
        'r_squared_interpretation': interpret_r_squared(r_squared),
        'p_value_interpretation': interpret_p_value(p_value),
    }

    print(f"  LHP Percentage Trend:")
    print(f"    2015: {lhp_pct[0]:.1f}%")
    print(f"    2025: {lhp_pct[-1]:.1f}%")
    print(f"    Slope: {slope:.3f}%/year (95% CI: [{slope - 1.96*std_err:.3f}, {slope + 1.96*std_err:.3f}])")
    print(f"    R²: {r_squared:.4f} ({interpret_r_squared(r_squared)})")
    print(f"    p-value: {p_value:.2e} ({interpret_p_value(p_value)})")

    return trend_results


def create_visualizations(results_df: pd.DataFrame, pitch_mix_df: pd.DataFrame,
                          movement_df: pd.DataFrame, comparison_results: dict):
    """Generate chapter visualizations."""
    print("\n[7] Creating visualizations...")

    # Figure 1: LHP vs RHP Velocity Trend
    fig, ax = plt.subplots(figsize=(10, 6))

    for hand, color, label in [('L', '#1f77b4', 'Left-handed'), ('R', '#ff7f0e', 'Right-handed')]:
        data = results_df[results_df['hand'] == hand].sort_values('year')
        ax.plot(data['year'], data['ff_velo_mean'], 'o-', color=color,
                linewidth=2, markersize=8, label=label)

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('4-Seam Fastball Velocity (mph)', fontsize=12)
    ax.set_title('Fastball Velocity by Handedness (2015-2025)', fontsize=14)
    ax.legend(loc='lower right', fontsize=11)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig01_velocity_by_handedness.png', dpi=150)
    plt.close()
    print("  Saved: fig01_velocity_by_handedness.png")

    # Figure 2: LHP Percentage Trend
    fig, ax = plt.subplots(figsize=(10, 6))

    lhp_data = results_df[results_df['hand'] == 'L'].sort_values('year')
    ax.bar(lhp_data['year'], lhp_data['pct_of_total'], color='#1f77b4',
           edgecolor='black', linewidth=0.5)

    ax.axhline(y=lhp_data['pct_of_total'].mean(), color='red', linestyle='--',
               linewidth=2, label=f"Average: {lhp_data['pct_of_total'].mean():.1f}%")

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('LHP Percentage of Pitches (%)', fontsize=12)
    ax.set_title('Left-Handed Pitcher Usage Over Time', fontsize=14)
    ax.set_ylim(0, 35)
    ax.legend(loc='upper right')

    for i, row in lhp_data.iterrows():
        ax.text(row['year'], row['pct_of_total'] + 0.5, f"{row['pct_of_total']:.1f}%",
                ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig02_lhp_percentage_trend.png', dpi=150)
    plt.close()
    print("  Saved: fig02_lhp_percentage_trend.png")

    # Figure 3: Pitch Mix Comparison (2025)
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    recent = pitch_mix_df[pitch_mix_df['year'] == 2025]

    for idx, (hand, title) in enumerate([('L', 'Left-Handed Pitchers'), ('R', 'Right-Handed Pitchers')]):
        ax = axes[idx]
        data = recent[recent['hand'] == hand].sort_values('pct', ascending=True)

        colors = plt.cm.Set2(np.linspace(0, 1, len(data)))
        bars = ax.barh(data['pitch_type'].map(PRIMARY_PITCHES), data['pct'], color=colors)

        ax.set_xlabel('Usage (%)', fontsize=11)
        ax.set_title(title, fontsize=12)

        for bar, pct in zip(bars, data['pct']):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                    f'{pct:.1f}%', va='center', fontsize=10)

        ax.set_xlim(0, 45)

    plt.suptitle('Pitch Mix by Handedness (2025)', fontsize=14)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig03_pitch_mix_comparison.png', dpi=150)
    plt.close()
    print("  Saved: fig03_pitch_mix_comparison.png")

    # Figure 4: Movement Profile by Handedness
    fig, ax = plt.subplots(figsize=(10, 8))

    recent_movement = movement_df[movement_df['year'] == 2025]

    for hand, color, marker in [('L', '#1f77b4', 'o'), ('R', '#ff7f0e', 's')]:
        data = recent_movement[recent_movement['hand'] == hand]
        if len(data) > 0:
            label = 'Left-handed' if hand == 'L' else 'Right-handed'
            ax.scatter(data['pfx_x_mean'], data['pfx_z_mean'],
                       s=200, c=color, marker=marker, label=label, edgecolors='black')

    # Show all years as smaller points
    for hand, color, marker in [('L', '#1f77b4', 'o'), ('R', '#ff7f0e', 's')]:
        data = movement_df[movement_df['hand'] == hand].sort_values('year')
        ax.scatter(data['pfx_x_mean'], data['pfx_z_mean'],
                   s=50, c=color, marker=marker, alpha=0.3)
        ax.plot(data['pfx_x_mean'], data['pfx_z_mean'], '-', color=color, alpha=0.3)

    ax.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
    ax.axvline(x=0, color='gray', linestyle=':', alpha=0.5)
    ax.set_xlabel('Horizontal Break (inches)', fontsize=12)
    ax.set_ylabel('Vertical Break (inches)', fontsize=12)
    ax.set_title('4-Seam Fastball Movement by Handedness', fontsize=14)
    ax.legend(loc='best', fontsize=11)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig04_movement_by_handedness.png', dpi=150)
    plt.close()
    print("  Saved: fig04_movement_by_handedness.png")

    # Figure 5: Velocity Distribution Comparison
    fig, ax = plt.subplots(figsize=(10, 6))

    # Use comparison results for distribution
    lhp_mean = comparison_results['velocity']['lhp_mean']
    lhp_std = comparison_results['velocity']['lhp_std']
    rhp_mean = comparison_results['velocity']['rhp_mean']
    rhp_std = comparison_results['velocity']['rhp_std']

    x = np.linspace(80, 105, 200)
    lhp_dist = stats.norm.pdf(x, lhp_mean, lhp_std)
    rhp_dist = stats.norm.pdf(x, rhp_mean, rhp_std)

    ax.fill_between(x, lhp_dist, alpha=0.5, color='#1f77b4', label='Left-handed')
    ax.fill_between(x, rhp_dist, alpha=0.5, color='#ff7f0e', label='Right-handed')
    ax.axvline(lhp_mean, color='#1f77b4', linestyle='--', linewidth=2)
    ax.axvline(rhp_mean, color='#ff7f0e', linestyle='--', linewidth=2)

    ax.set_xlabel('4-Seam Fastball Velocity (mph)', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title('Velocity Distribution: LHP vs RHP', fontsize=14)
    ax.legend(fontsize=11)

    # Add annotation
    diff = rhp_mean - lhp_mean
    ax.annotate(f'Difference: {diff:+.2f} mph',
                xy=(0.5, 0.95), xycoords='axes fraction',
                ha='center', fontsize=12,
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray'))

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig05_velocity_distribution.png', dpi=150)
    plt.close()
    print("  Saved: fig05_velocity_distribution.png")


def save_results(results_df: pd.DataFrame, pitch_mix_df: pd.DataFrame,
                 comparison_results: dict, trend_results: dict):
    """Save analysis results to CSV."""
    print("\n[8] Saving results...")

    # Main results - yearly statistics by handedness
    results_df.to_csv(RESULTS_DIR / 'stats_by_handedness.csv', index=False)
    print(f"  Saved: stats_by_handedness.csv")

    # Pitch mix results
    pitch_mix_df.to_csv(RESULTS_DIR / 'pitch_mix_by_handedness.csv', index=False)
    print(f"  Saved: pitch_mix_by_handedness.csv")

    # Statistical tests
    stat_tests = []

    # Velocity comparison
    velo = comparison_results['velocity']
    stat_tests.extend([
        {'test': 'Velocity Comparison', 'metric': 'LHP Mean', 'value': f"{velo['lhp_mean']:.2f}", 'unit': 'mph'},
        {'test': 'Velocity Comparison', 'metric': 'RHP Mean', 'value': f"{velo['rhp_mean']:.2f}", 'unit': 'mph'},
        {'test': 'Velocity Comparison', 'metric': 'Difference (RHP-LHP)', 'value': f"{velo['difference']:+.2f}", 'unit': 'mph'},
        {'test': 'Velocity Comparison', 'metric': 't-statistic', 'value': f"{velo['t_statistic']:.2f}", 'unit': ''},
        {'test': 'Velocity Comparison', 'metric': 'p-value', 'value': f"{velo['p_value']:.2e}", 'unit': ''},
        {'test': 'Velocity Comparison', 'metric': "Cohen's d", 'value': f"{velo['cohens_d']:.3f}", 'unit': ''},
        {'test': 'Velocity Comparison', 'metric': 'Effect Interpretation', 'value': velo['effect_interpretation'], 'unit': ''},
    ])

    # Spin rate comparison
    spin = comparison_results['spin_rate']
    stat_tests.extend([
        {'test': 'Spin Rate Comparison', 'metric': 'LHP Mean', 'value': f"{spin['lhp_mean']:.0f}", 'unit': 'rpm'},
        {'test': 'Spin Rate Comparison', 'metric': 'RHP Mean', 'value': f"{spin['rhp_mean']:.0f}", 'unit': 'rpm'},
        {'test': 'Spin Rate Comparison', 'metric': 'Difference (RHP-LHP)', 'value': f"{spin['difference']:+.0f}", 'unit': 'rpm'},
        {'test': 'Spin Rate Comparison', 'metric': "Cohen's d", 'value': f"{spin['cohens_d']:.3f}", 'unit': ''},
        {'test': 'Spin Rate Comparison', 'metric': 'Effect Interpretation', 'value': spin['effect_interpretation'], 'unit': ''},
    ])

    # LHP ratio trend
    stat_tests.extend([
        {'test': 'LHP Ratio Trend', 'metric': 'Slope', 'value': f"{trend_results['slope']:.4f}", 'unit': '%/year'},
        {'test': 'LHP Ratio Trend', 'metric': 'R-squared', 'value': f"{trend_results['r_squared']:.4f}", 'unit': ''},
        {'test': 'LHP Ratio Trend', 'metric': 'R² Interpretation', 'value': trend_results['r_squared_interpretation'], 'unit': ''},
        {'test': 'LHP Ratio Trend', 'metric': 'p-value', 'value': f"{trend_results['p_value']:.2e}", 'unit': ''},
    ])

    pd.DataFrame(stat_tests).to_csv(RESULTS_DIR / 'statistical_tests.csv', index=False)
    print(f"  Saved: statistical_tests.csv")

    # Summary
    lhp_2015 = results_df[(results_df['year'] == 2015) & (results_df['hand'] == 'L')].iloc[0]
    lhp_2025 = results_df[(results_df['year'] == 2025) & (results_df['hand'] == 'L')].iloc[0]
    rhp_2015 = results_df[(results_df['year'] == 2015) & (results_df['hand'] == 'R')].iloc[0]
    rhp_2025 = results_df[(results_df['year'] == 2025) & (results_df['hand'] == 'R')].iloc[0]

    summary = {
        'metric': [
            'LHP Pitch Percentage (2015)',
            'LHP Pitch Percentage (2025)',
            'LHP Percentage Change',
            'LHP 4-Seam Velocity (All Years)',
            'RHP 4-Seam Velocity (All Years)',
            'Velocity Difference (RHP-LHP)',
            "Velocity Cohen's d",
            'Total LHP Pitches',
            'Total RHP Pitches',
        ],
        'value': [
            f"{lhp_2015['pct_of_total']:.1f}%",
            f"{lhp_2025['pct_of_total']:.1f}%",
            f"{lhp_2025['pct_of_total'] - lhp_2015['pct_of_total']:+.1f}%",
            f"{comparison_results['velocity']['lhp_mean']:.2f} mph",
            f"{comparison_results['velocity']['rhp_mean']:.2f} mph",
            f"{comparison_results['velocity']['difference']:+.2f} mph",
            f"{comparison_results['velocity']['cohens_d']:.3f} ({comparison_results['velocity']['effect_interpretation']})",
            f"{int(comparison_results['velocity']['lhp_n']):,}",
            f"{int(comparison_results['velocity']['rhp_n']):,}",
        ]
    }
    pd.DataFrame(summary).to_csv(RESULTS_DIR / 'summary.csv', index=False)
    print(f"  Saved: summary.csv")


def print_summary(results_df: pd.DataFrame, comparison_results: dict, trend_results: dict):
    """Print analysis summary."""
    print("\n" + "=" * 60)
    print("  Summary: L/R Pitcher Differences")
    print("=" * 60)

    lhp_2015 = results_df[(results_df['year'] == 2015) & (results_df['hand'] == 'L')].iloc[0]
    lhp_2025 = results_df[(results_df['year'] == 2025) & (results_df['hand'] == 'L')].iloc[0]

    velo = comparison_results['velocity']
    spin = comparison_results['spin_rate']

    print(f"""
KEY FINDINGS:

1. LHP vs RHP Representation:
   - 2015: LHP = {lhp_2015['pct_of_total']:.1f}% of pitches
   - 2025: LHP = {lhp_2025['pct_of_total']:.1f}% of pitches
   - Trend: {trend_results['slope']:+.3f}%/year (R²={trend_results['r_squared']:.4f})

2. 4-Seam Fastball Velocity (All Years):
   - LHP: {velo['lhp_mean']:.2f} mph (SD={velo['lhp_std']:.2f})
   - RHP: {velo['rhp_mean']:.2f} mph (SD={velo['rhp_std']:.2f})
   - Difference: {velo['difference']:+.2f} mph
   - Cohen's d: {velo['cohens_d']:.3f} ({velo['effect_interpretation']} effect)

3. 4-Seam Fastball Spin Rate:
   - LHP: {spin['lhp_mean']:.0f} rpm
   - RHP: {spin['rhp_mean']:.0f} rpm
   - Difference: {spin['difference']:+.0f} rpm
   - Cohen's d: {spin['cohens_d']:.3f} ({spin['effect_interpretation']} effect)

4. Sample Sizes:
   - LHP 4-Seamers: {velo['lhp_n']:,}
   - RHP 4-Seamers: {velo['rhp_n']:,}

INTERPRETATION: Right-handed pitchers throw slightly harder than left-handed
pitchers, but the difference is {velo['effect_interpretation']} in practical terms.
""")


def main():
    # Phase 1 & 2: Load data
    df = load_handedness_data()

    if len(df) == 0:
        print("\n[ERROR] No data found.")
        return

    # Phase 3: Calculate yearly statistics by handedness
    results_df = analyze_handedness_by_year(df)

    # Phase 4: Analyze pitch mix
    pitch_mix_df = analyze_pitch_mix_by_handedness(df)

    # Phase 5: Analyze movement
    movement_df = analyze_movement_by_handedness(df)

    # Phase 6: Statistical comparisons
    comparison_results = perform_statistical_comparison(df)

    # Phase 7: LHP ratio trend
    trend_results = analyze_lhp_ratio_trend(results_df)

    # Phase 8: Visualizations
    create_visualizations(results_df, pitch_mix_df, movement_df, comparison_results)

    # Phase 9: Save results
    save_results(results_df, pitch_mix_df, comparison_results, trend_results)

    # Print summary
    print_summary(results_df, comparison_results, trend_results)

    print("\n" + "=" * 60)
    print("  [DONE] Analysis complete!")
    print("=" * 60)
    print(f"  Figures: {FIGURES_DIR}")
    print(f"  Results: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
