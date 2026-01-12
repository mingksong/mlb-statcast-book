#!/usr/bin/env python3
"""
Chapter 5: Movement Analysis (2015-2025)

Research Question: How has pitch movement (horizontal and vertical break)
evolved over the past decade in MLB?

Hypotheses:
- H0: No significant change in average pitch movement (slope = 0)
- H1: Significant change in movement patterns over time (slope ≠ 0)

Key Metrics:
- pfx_x: Horizontal movement (inches) - positive = arm-side, negative = glove-side
- pfx_z: Vertical movement (inches) - induced vertical break (IVB)

Methodology:
1. Load pfx_x and pfx_z for all pitch types
2. Analyze movement by pitch type category (Fastball, Breaking, Offspeed)
3. Calculate yearly movement statistics with confidence intervals
4. Perform linear regression for trend analysis
5. Compare early period (2015-2017) vs late period (2023-2025)
6. Calculate effect size (Cohen's d) for practical significance

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

# Pitch type categories
PITCH_CATEGORIES = {
    'Fastball': ['FF', 'SI', 'FC'],      # 4-seam, sinker, cutter
    'Breaking': ['SL', 'CU', 'ST', 'KC'], # slider, curveball, sweeper, knuckle curve
    'Offspeed': ['CH', 'FS']              # changeup, splitter
}

# Individual pitch types for detailed analysis
PRIMARY_PITCHES = {
    'FF': '4-Seam Fastball',
    'SL': 'Slider',
    'CU': 'Curveball',
    'CH': 'Changeup',
    'SI': 'Sinker'
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


def descriptive_stats(series, name="metric"):
    """Calculate comprehensive descriptive statistics."""
    return {
        'n': len(series),
        'mean': series.mean(),
        'std': series.std(),
        'median': series.median(),
        'min': series.min(),
        'max': series.max(),
        'p10': series.quantile(0.10),
        'p25': series.quantile(0.25),
        'p75': series.quantile(0.75),
        'p90': series.quantile(0.90),
        'skew': series.skew(),
        'kurtosis': series.kurtosis(),
    }


def load_movement_data():
    """Load movement data for all seasons."""
    print("=" * 60)
    print("  Chapter 5: Movement Analysis (2015-2025)")
    print("=" * 60)
    print("\n[1] Loading pitch movement data...")

    all_data = []

    for year in AVAILABLE_SEASONS:
        try:
            df = load_season(year, columns=['pitch_type', 'pfx_x', 'pfx_z', 'p_throws'])
            df['game_year'] = year

            # Ensure numeric types for movement columns
            df['pfx_x'] = pd.to_numeric(df['pfx_x'], errors='coerce')
            df['pfx_z'] = pd.to_numeric(df['pfx_z'], errors='coerce')

            # Filter to valid movement data
            df = df.dropna(subset=['pfx_x', 'pfx_z', 'pitch_type'])

            # Convert movement to inches (already in inches in Statcast)
            # pfx_x and pfx_z are in inches from 2015+

            all_data.append(df)
            print(f"  {year}: {len(df):,} pitches with movement data")

        except FileNotFoundError:
            print(f"  {year}: data not found, skipping")
            continue

    combined = pd.concat(all_data, ignore_index=True)
    print(f"\n  Total pitches: {len(combined):,}")

    return combined


def analyze_movement_by_year(df: pd.DataFrame):
    """Calculate yearly movement statistics by pitch type."""
    print("\n[2] Calculating yearly movement statistics...")

    results = []

    for year in df['game_year'].unique():
        year_data = df[df['game_year'] == year]

        # Overall statistics
        overall_pfx_x = year_data['pfx_x']
        overall_pfx_z = year_data['pfx_z']

        results.append({
            'year': year,
            'pitch_type': 'ALL',
            'count': len(year_data),
            'pfx_x_mean': overall_pfx_x.mean(),
            'pfx_x_std': overall_pfx_x.std(),
            'pfx_x_median': overall_pfx_x.median(),
            'pfx_z_mean': overall_pfx_z.mean(),
            'pfx_z_std': overall_pfx_z.std(),
            'pfx_z_median': overall_pfx_z.median(),
        })

        # By primary pitch types
        for pitch_code, pitch_name in PRIMARY_PITCHES.items():
            pitch_data = year_data[year_data['pitch_type'] == pitch_code]
            if len(pitch_data) < 100:
                continue

            pfx_x = pitch_data['pfx_x']
            pfx_z = pitch_data['pfx_z']
            n = len(pitch_data)

            results.append({
                'year': year,
                'pitch_type': pitch_code,
                'count': n,
                'pfx_x_mean': pfx_x.mean(),
                'pfx_x_std': pfx_x.std(),
                'pfx_x_median': pfx_x.median(),
                'pfx_x_se': pfx_x.std() / np.sqrt(n),
                'pfx_z_mean': pfx_z.mean(),
                'pfx_z_std': pfx_z.std(),
                'pfx_z_median': pfx_z.median(),
                'pfx_z_se': pfx_z.std() / np.sqrt(n),
            })

    results_df = pd.DataFrame(results)

    # Print summary for key pitch types
    print("\n  Yearly averages for 4-Seam Fastball (FF):")
    ff_data = results_df[results_df['pitch_type'] == 'FF'].sort_values('year')
    for _, row in ff_data.iterrows():
        print(f"    {int(row['year'])}: H-Break={row['pfx_x_mean']:+.2f}in, V-Break={row['pfx_z_mean']:+.2f}in (n={int(row['count']):,})")

    return results_df


def perform_trend_analysis(results_df: pd.DataFrame, pitch_type: str = 'FF'):
    """Perform linear regression trend analysis for a pitch type."""
    print(f"\n[3] Trend Analysis for {PRIMARY_PITCHES.get(pitch_type, pitch_type)}...")

    pitch_data = results_df[results_df['pitch_type'] == pitch_type].sort_values('year')
    years = pitch_data['year'].values

    trend_results = {}

    for metric, label in [('pfx_x_mean', 'Horizontal Break'), ('pfx_z_mean', 'Vertical Break')]:
        values = pitch_data[metric].values

        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(years, values)
        r_squared = r_value ** 2

        trend_results[metric] = {
            'slope': slope,
            'slope_ci_lower': slope - 1.96 * std_err,
            'slope_ci_upper': slope + 1.96 * std_err,
            'intercept': intercept,
            'r_squared': r_squared,
            'p_value': p_value,
            'std_err': std_err,
            'r_squared_interpretation': interpret_r_squared(r_squared),
            'p_value_interpretation': interpret_p_value(p_value),
        }

        print(f"\n  {label} ({pitch_type}):")
        print(f"    Slope: {slope:+.4f} in/year (95% CI: [{slope - 1.96*std_err:+.4f}, {slope + 1.96*std_err:+.4f}])")
        print(f"    R²: {r_squared:.4f} ({interpret_r_squared(r_squared)})")
        print(f"    p-value: {p_value:.2e} ({interpret_p_value(p_value)})")
        print(f"    10-year change: {slope * 10:+.2f} inches")

    return trend_results


def perform_period_comparison(df: pd.DataFrame, pitch_type: str = 'FF'):
    """Compare early period vs late period with t-test and effect size."""
    print(f"\n[4] Period Comparison for {PRIMARY_PITCHES.get(pitch_type, pitch_type)}...")
    print(f"    Early period: {EARLY_PERIOD}")
    print(f"    Late period: {LATE_PERIOD}")

    early = df[(df['game_year'].isin(EARLY_PERIOD)) & (df['pitch_type'] == pitch_type)]
    late = df[(df['game_year'].isin(LATE_PERIOD)) & (df['pitch_type'] == pitch_type)]

    comparison_results = {}

    for metric, label in [('pfx_x', 'Horizontal Break'), ('pfx_z', 'Vertical Break')]:
        early_values = early[metric].dropna().astype(float)
        late_values = late[metric].dropna().astype(float)

        # Two-sample t-test
        t_stat, p_value = stats.ttest_ind(early_values, late_values)

        # Effect size (Cohen's d)
        pooled_std = np.sqrt(((len(early_values)-1)*early_values.std()**2 +
                              (len(late_values)-1)*late_values.std()**2) /
                             (len(early_values) + len(late_values) - 2))
        cohens_d = (late_values.mean() - early_values.mean()) / pooled_std

        # Confidence interval for difference
        se_diff = np.sqrt(early_values.var()/len(early_values) + late_values.var()/len(late_values))
        diff = late_values.mean() - early_values.mean()
        ci_lower = diff - 1.96 * se_diff
        ci_upper = diff + 1.96 * se_diff

        comparison_results[metric] = {
            'early_n': len(early_values),
            'early_mean': early_values.mean(),
            'early_std': early_values.std(),
            'late_n': len(late_values),
            'late_mean': late_values.mean(),
            'late_std': late_values.std(),
            'difference': diff,
            'diff_ci_lower': ci_lower,
            'diff_ci_upper': ci_upper,
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'effect_interpretation': interpret_cohens_d(cohens_d),
            'p_value_interpretation': interpret_p_value(p_value),
        }

        print(f"\n  {label}:")
        print(f"    Early: {early_values.mean():+.2f}in (SD: {early_values.std():.2f}, n={len(early_values):,})")
        print(f"    Late:  {late_values.mean():+.2f}in (SD: {late_values.std():.2f}, n={len(late_values):,})")
        print(f"    Difference: {diff:+.2f}in (95% CI: [{ci_lower:+.2f}, {ci_upper:+.2f}])")
        print(f"    Cohen's d: {cohens_d:.3f} ({interpret_cohens_d(cohens_d)} effect)")
        print(f"    p-value: {p_value:.2e} ({interpret_p_value(p_value)})")

    return comparison_results


def create_visualizations(results_df: pd.DataFrame, df: pd.DataFrame, trend_results: dict):
    """Generate chapter visualizations with statistical annotations."""
    print("\n[5] Creating visualizations...")

    # Figure 1: 4-Seam Fastball Movement Trend (dual panel)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    ff_data = results_df[results_df['pitch_type'] == 'FF'].sort_values('year')
    years = ff_data['year'].values

    # Left panel: Horizontal break
    ax1 = axes[0]
    pfx_x_means = ff_data['pfx_x_mean'].values
    pfx_x_se = ff_data['pfx_x_std'].values / np.sqrt(ff_data['count'].values)

    ax1.errorbar(years, pfx_x_means, yerr=1.96*pfx_x_se, fmt='o-',
                 linewidth=2, markersize=8, color='#1f77b4', capsize=4, label='Mean ± 95% CI')

    # Regression line
    slope = trend_results['pfx_x_mean']['slope']
    intercept = trend_results['pfx_x_mean']['intercept']
    r_squared = trend_results['pfx_x_mean']['r_squared']
    ax1.plot(years, intercept + slope * years, '--', color='red', linewidth=2,
             label=f'Trend (R²={r_squared:.3f})')

    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Horizontal Break (inches)', fontsize=12)
    ax1.set_title('4-Seam Fastball: Horizontal Movement', fontsize=14)
    ax1.legend(loc='best')
    ax1.axhline(y=0, color='gray', linestyle=':', alpha=0.5)

    # Right panel: Vertical break
    ax2 = axes[1]
    pfx_z_means = ff_data['pfx_z_mean'].values
    pfx_z_se = ff_data['pfx_z_std'].values / np.sqrt(ff_data['count'].values)

    ax2.errorbar(years, pfx_z_means, yerr=1.96*pfx_z_se, fmt='o-',
                 linewidth=2, markersize=8, color='#ff7f0e', capsize=4, label='Mean ± 95% CI')

    # Regression line
    slope = trend_results['pfx_z_mean']['slope']
    intercept = trend_results['pfx_z_mean']['intercept']
    r_squared = trend_results['pfx_z_mean']['r_squared']
    ax2.plot(years, intercept + slope * years, '--', color='red', linewidth=2,
             label=f'Trend (R²={r_squared:.3f})')

    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Vertical Break (inches)', fontsize=12)
    ax2.set_title('4-Seam Fastball: Vertical Movement (IVB)', fontsize=14)
    ax2.legend(loc='best')
    ax2.axhline(y=0, color='gray', linestyle=':', alpha=0.5)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig01_fastball_movement_trend.png', dpi=150)
    plt.close()
    print("  Saved: fig01_fastball_movement_trend.png")

    # Figure 2: Movement by pitch type comparison
    fig, ax = plt.subplots(figsize=(12, 8))

    colors = {'FF': '#1f77b4', 'SL': '#ff7f0e', 'CU': '#2ca02c', 'CH': '#d62728', 'SI': '#9467bd'}

    for pitch_code in PRIMARY_PITCHES.keys():
        pitch_data = results_df[results_df['pitch_type'] == pitch_code].sort_values('year')
        if len(pitch_data) == 0:
            continue
        ax.scatter(pitch_data['pfx_x_mean'], pitch_data['pfx_z_mean'],
                   c=[colors.get(pitch_code, 'gray')] * len(pitch_data),
                   s=100, alpha=0.7, label=PRIMARY_PITCHES[pitch_code])

        # Connect points with lines for trend visualization
        ax.plot(pitch_data['pfx_x_mean'], pitch_data['pfx_z_mean'],
                '-', alpha=0.3, color=colors.get(pitch_code, 'gray'))

    ax.set_xlabel('Horizontal Break (inches)', fontsize=12)
    ax.set_ylabel('Vertical Break (inches)', fontsize=12)
    ax.set_title('Pitch Movement Profile by Type (2015-2025)', fontsize=14)
    ax.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
    ax.axvline(x=0, color='gray', linestyle=':', alpha=0.5)
    ax.legend(loc='best', fontsize=10)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig02_pitch_movement_profile.png', dpi=150)
    plt.close()
    print("  Saved: fig02_pitch_movement_profile.png")

    # Figure 3: Movement trends for all pitch types
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for idx, (pitch_code, pitch_name) in enumerate(PRIMARY_PITCHES.items()):
        if idx >= 5:
            break
        ax = axes[idx]
        pitch_data = results_df[results_df['pitch_type'] == pitch_code].sort_values('year')

        if len(pitch_data) < 3:
            ax.text(0.5, 0.5, 'Insufficient data', ha='center', va='center', transform=ax.transAxes)
            ax.set_title(pitch_name)
            continue

        years = pitch_data['year'].values

        # Plot both metrics
        ax.plot(years, pitch_data['pfx_x_mean'], 'o-', color='#1f77b4',
                label='Horizontal', markersize=6)
        ax.plot(years, pitch_data['pfx_z_mean'], 's-', color='#ff7f0e',
                label='Vertical', markersize=6)

        ax.set_xlabel('Year', fontsize=10)
        ax.set_ylabel('Movement (inches)', fontsize=10)
        ax.set_title(pitch_name, fontsize=12)
        ax.legend(loc='best', fontsize=8)
        ax.axhline(y=0, color='gray', linestyle=':', alpha=0.5)

    # Remove empty subplot
    axes[5].axis('off')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig03_movement_by_pitch_type.png', dpi=150)
    plt.close()
    print("  Saved: fig03_movement_by_pitch_type.png")

    # Figure 4: 2015 vs 2025 Distribution comparison
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    ff_2015 = df[(df['game_year'] == 2015) & (df['pitch_type'] == 'FF')]
    ff_2025 = df[(df['game_year'] == 2025) & (df['pitch_type'] == 'FF')]

    # Horizontal break distribution
    ax1 = axes[0]
    ax1.hist(ff_2015['pfx_x'], bins=50, alpha=0.6, label='2015', density=True, color='#1f77b4')
    ax1.hist(ff_2025['pfx_x'], bins=50, alpha=0.6, label='2025', density=True, color='#ff7f0e')
    ax1.axvline(ff_2015['pfx_x'].mean(), color='#1f77b4', linestyle='--', linewidth=2)
    ax1.axvline(ff_2025['pfx_x'].mean(), color='#ff7f0e', linestyle='--', linewidth=2)
    ax1.set_xlabel('Horizontal Break (inches)', fontsize=12)
    ax1.set_ylabel('Density', fontsize=12)
    ax1.set_title('4-Seam Fastball: Horizontal Break Distribution', fontsize=14)
    ax1.legend(fontsize=11)

    # Vertical break distribution
    ax2 = axes[1]
    ax2.hist(ff_2015['pfx_z'], bins=50, alpha=0.6, label='2015', density=True, color='#1f77b4')
    ax2.hist(ff_2025['pfx_z'], bins=50, alpha=0.6, label='2025', density=True, color='#ff7f0e')
    ax2.axvline(ff_2015['pfx_z'].mean(), color='#1f77b4', linestyle='--', linewidth=2)
    ax2.axvline(ff_2025['pfx_z'].mean(), color='#ff7f0e', linestyle='--', linewidth=2)
    ax2.set_xlabel('Vertical Break (inches)', fontsize=12)
    ax2.set_ylabel('Density', fontsize=12)
    ax2.set_title('4-Seam Fastball: Vertical Break (IVB) Distribution', fontsize=14)
    ax2.legend(fontsize=11)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig04_distribution_comparison.png', dpi=150)
    plt.close()
    print("  Saved: fig04_distribution_comparison.png")


def save_results(results_df: pd.DataFrame, trend_results: dict, comparison_results: dict):
    """Save analysis results to CSV."""
    print("\n[6] Saving results...")

    # Main results - yearly statistics by pitch type
    results_df.to_csv(RESULTS_DIR / 'movement_by_year.csv', index=False)
    print(f"  Saved: movement_by_year.csv")

    # Statistical tests results
    stat_tests = []

    # Trend analysis results
    for metric, label in [('pfx_x_mean', 'Horizontal Break'), ('pfx_z_mean', 'Vertical Break')]:
        tr = trend_results[metric]
        stat_tests.extend([
            {'test': f'Trend ({label})', 'metric': 'Slope', 'value': f"{tr['slope']:.4f}", 'unit': 'in/year'},
            {'test': f'Trend ({label})', 'metric': 'Slope 95% CI', 'value': f"[{tr['slope_ci_lower']:.4f}, {tr['slope_ci_upper']:.4f}]", 'unit': 'in/year'},
            {'test': f'Trend ({label})', 'metric': 'R-squared', 'value': f"{tr['r_squared']:.4f}", 'unit': ''},
            {'test': f'Trend ({label})', 'metric': 'R² Interpretation', 'value': tr['r_squared_interpretation'], 'unit': ''},
            {'test': f'Trend ({label})', 'metric': 'p-value', 'value': f"{tr['p_value']:.2e}", 'unit': ''},
            {'test': f'Trend ({label})', 'metric': 'p-value Interpretation', 'value': tr['p_value_interpretation'], 'unit': ''},
        ])

    # Period comparison results
    for metric, label in [('pfx_x', 'Horizontal Break'), ('pfx_z', 'Vertical Break')]:
        cr = comparison_results[metric]
        stat_tests.extend([
            {'test': f'Period Comparison ({label})', 'metric': 'Early Period Mean', 'value': f"{cr['early_mean']:.2f}", 'unit': 'in'},
            {'test': f'Period Comparison ({label})', 'metric': 'Late Period Mean', 'value': f"{cr['late_mean']:.2f}", 'unit': 'in'},
            {'test': f'Period Comparison ({label})', 'metric': 'Difference', 'value': f"{cr['difference']:.2f}", 'unit': 'in'},
            {'test': f'Period Comparison ({label})', 'metric': 'Difference 95% CI', 'value': f"[{cr['diff_ci_lower']:.2f}, {cr['diff_ci_upper']:.2f}]", 'unit': 'in'},
            {'test': f'Period Comparison ({label})', 'metric': 't-statistic', 'value': f"{cr['t_statistic']:.2f}", 'unit': ''},
            {'test': f'Period Comparison ({label})', 'metric': 'p-value', 'value': f"{cr['p_value']:.2e}", 'unit': ''},
            {'test': f'Period Comparison ({label})', 'metric': "Cohen's d", 'value': f"{cr['cohens_d']:.3f}", 'unit': ''},
            {'test': f'Period Comparison ({label})', 'metric': 'Effect Interpretation', 'value': cr['effect_interpretation'], 'unit': ''},
        ])

    pd.DataFrame(stat_tests).to_csv(RESULTS_DIR / 'statistical_tests.csv', index=False)
    print(f"  Saved: statistical_tests.csv")

    # Summary statistics
    ff_data = results_df[results_df['pitch_type'] == 'FF'].sort_values('year')
    first_year = ff_data.iloc[0]
    last_year = ff_data.iloc[-1]

    summary = {
        'metric': [
            '2015 Horizontal Break (FF)',
            '2025 Horizontal Break (FF)',
            'Horizontal Break Change',
            '2015 Vertical Break (FF)',
            '2025 Vertical Break (FF)',
            'Vertical Break Change',
            'H-Break Trend Slope',
            'H-Break R-squared',
            'V-Break Trend Slope',
            'V-Break R-squared',
            "Cohen's d (H-Break)",
            "Cohen's d (V-Break)",
            'Total Pitches Analyzed',
        ],
        'value': [
            f"{first_year['pfx_x_mean']:+.2f} in",
            f"{last_year['pfx_x_mean']:+.2f} in",
            f"{last_year['pfx_x_mean'] - first_year['pfx_x_mean']:+.2f} in",
            f"{first_year['pfx_z_mean']:+.2f} in",
            f"{last_year['pfx_z_mean']:+.2f} in",
            f"{last_year['pfx_z_mean'] - first_year['pfx_z_mean']:+.2f} in",
            f"{trend_results['pfx_x_mean']['slope']:.4f} in/year",
            f"{trend_results['pfx_x_mean']['r_squared']:.4f} ({trend_results['pfx_x_mean']['r_squared_interpretation']})",
            f"{trend_results['pfx_z_mean']['slope']:.4f} in/year",
            f"{trend_results['pfx_z_mean']['r_squared']:.4f} ({trend_results['pfx_z_mean']['r_squared_interpretation']})",
            f"{comparison_results['pfx_x']['cohens_d']:.3f} ({comparison_results['pfx_x']['effect_interpretation']})",
            f"{comparison_results['pfx_z']['cohens_d']:.3f} ({comparison_results['pfx_z']['effect_interpretation']})",
            f"{results_df[results_df['pitch_type'] == 'ALL']['count'].sum():,}",
        ]
    }
    pd.DataFrame(summary).to_csv(RESULTS_DIR / 'summary.csv', index=False)
    print(f"  Saved: summary.csv")


def print_summary(results_df: pd.DataFrame, trend_results: dict, comparison_results: dict):
    """Print analysis summary with statistical validation."""
    print("\n" + "=" * 60)
    print("  Summary: Statistical Validation")
    print("=" * 60)

    ff_data = results_df[results_df['pitch_type'] == 'FF'].sort_values('year')
    first_year = ff_data.iloc[0]
    last_year = ff_data.iloc[-1]

    hbreak_change = last_year['pfx_x_mean'] - first_year['pfx_x_mean']
    vbreak_change = last_year['pfx_z_mean'] - first_year['pfx_z_mean']

    print(f"""
KEY FINDINGS (4-Seam Fastball):

1. Horizontal Break Trend (2015-2025):
   - 2015: {first_year['pfx_x_mean']:+.2f} inches
   - 2025: {last_year['pfx_x_mean']:+.2f} inches
   - Change: {hbreak_change:+.2f} inches

2. Vertical Break (IVB) Trend (2015-2025):
   - 2015: {first_year['pfx_z_mean']:+.2f} inches
   - 2025: {last_year['pfx_z_mean']:+.2f} inches
   - Change: {vbreak_change:+.2f} inches

3. Horizontal Break Statistical Validation:
   - Trend slope: {trend_results['pfx_x_mean']['slope']:.4f} in/year
   - R²: {trend_results['pfx_x_mean']['r_squared']:.4f} ({trend_results['pfx_x_mean']['r_squared_interpretation']})
   - p-value: {trend_results['pfx_x_mean']['p_value']:.2e} ({trend_results['pfx_x_mean']['p_value_interpretation']})
   - Cohen's d: {comparison_results['pfx_x']['cohens_d']:.3f} ({comparison_results['pfx_x']['effect_interpretation']})

4. Vertical Break Statistical Validation:
   - Trend slope: {trend_results['pfx_z_mean']['slope']:.4f} in/year
   - R²: {trend_results['pfx_z_mean']['r_squared']:.4f} ({trend_results['pfx_z_mean']['r_squared_interpretation']})
   - p-value: {trend_results['pfx_z_mean']['p_value']:.2e} ({trend_results['pfx_z_mean']['p_value_interpretation']})
   - Cohen's d: {comparison_results['pfx_z']['cohens_d']:.3f} ({comparison_results['pfx_z']['effect_interpretation']})

5. Total pitches analyzed: {results_df[results_df['pitch_type'] == 'ALL']['count'].sum():,}

INTERPRETATION: Movement patterns analyzed across 11 seasons.
""")


def main():
    # Phase 1 & 2: Load data
    df = load_movement_data()

    if len(df) == 0:
        print("\n[ERROR] No data found. Please collect data first:")
        print("  python collector/collect_statcast.py --range 2015 2025")
        return

    # Phase 3: Calculate yearly statistics
    results_df = analyze_movement_by_year(df)

    # Phase 4: Trend analysis (linear regression) for 4-seam fastball
    trend_results = perform_trend_analysis(results_df, 'FF')

    # Phase 5: Period comparison (t-test, Cohen's d)
    comparison_results = perform_period_comparison(df, 'FF')

    # Phase 6: Create visualizations
    create_visualizations(results_df, df, trend_results)

    # Phase 7: Save results
    save_results(results_df, trend_results, comparison_results)

    # Print summary
    print_summary(results_df, trend_results, comparison_results)

    print("\n" + "=" * 60)
    print("  [DONE] Analysis complete!")
    print("=" * 60)
    print(f"  Figures: {FIGURES_DIR}")
    print(f"  Results: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
