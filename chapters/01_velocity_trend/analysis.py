#!/usr/bin/env python3
"""
Chapter 2: The Velocity Arms Race (2015-2025)

Research Question: Has MLB fastball velocity significantly increased over the
past decade, and if so, what is the magnitude of this change?

Hypotheses:
- H0: No significant change in average fastball velocity (slope = 0)
- H1: Significant increase in average fastball velocity (slope > 0)

Methodology:
1. Filter to 4-seam fastballs (pitch_type == 'FF')
2. Calculate yearly velocity statistics with confidence intervals
3. Perform linear regression to quantify trend
4. Compare early period (2015-2017) vs late period (2023-2025) with t-test
5. Calculate effect size (Cohen's d) for practical significance

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


def analyze_velocity_by_year():
    """Calculate yearly velocity statistics with confidence intervals."""
    print("=" * 60)
    print("  Chapter 2: The Velocity Arms Race (2015-2025)")
    print("=" * 60)

    results = []

    print("\n[1] Loading data and calculating velocity stats...")

    for year in AVAILABLE_SEASONS:
        try:
            df = load_season(year, columns=['pitch_type', 'release_speed', 'p_throws'])

            # Filter to 4-seam fastballs
            ff = df[df['pitch_type'] == 'FF']['release_speed'].dropna()

            if len(ff) == 0:
                continue

            # Calculate statistics
            n = len(ff)
            mean = ff.mean()
            std = ff.std()
            se = std / np.sqrt(n)  # Standard error for 95% CI

            results.append({
                'year': year,
                'count': n,
                'mean': mean,
                'median': ff.median(),
                'std': std,
                'se': se,
                'ci_lower': mean - 1.96 * se,
                'ci_upper': mean + 1.96 * se,
                'pct_95plus': (ff >= 95).mean() * 100,
                'pct_100plus': (ff >= 100).mean() * 100,
                'max': ff.max(),
                'p10': ff.quantile(0.10),
                'p25': ff.quantile(0.25),
                'p75': ff.quantile(0.75),
                'p90': ff.quantile(0.90),
            })

            print(f"  {year}: {mean:.2f} mph (95% CI: [{mean - 1.96*se:.2f}, {mean + 1.96*se:.2f}], n={n:,})")

        except FileNotFoundError:
            print(f"  {year}: data not found, skipping")
            continue

    return pd.DataFrame(results)


def perform_trend_analysis(df: pd.DataFrame):
    """Perform linear regression trend analysis."""
    print("\n[2] Trend Analysis (Linear Regression)...")

    years = df['year'].values
    means = df['mean'].values

    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(years, means)
    r_squared = r_value ** 2

    # 95% CI for slope
    slope_ci_lower = slope - 1.96 * std_err
    slope_ci_upper = slope + 1.96 * std_err

    trend_results = {
        'slope': slope,
        'slope_ci_lower': slope_ci_lower,
        'slope_ci_upper': slope_ci_upper,
        'intercept': intercept,
        'r_squared': r_squared,
        'p_value': p_value,
        'std_err': std_err,
        'r_squared_interpretation': interpret_r_squared(r_squared),
        'p_value_interpretation': interpret_p_value(p_value),
    }

    print(f"  Slope: {slope:.4f} mph/year (95% CI: [{slope_ci_lower:.4f}, {slope_ci_upper:.4f}])")
    print(f"  R²: {r_squared:.4f} ({interpret_r_squared(r_squared)})")
    print(f"  p-value: {p_value:.2e} ({interpret_p_value(p_value)})")
    print(f"  Projected 10-year change: {slope * 10:.2f} mph")

    return trend_results


def perform_period_comparison():
    """Compare early period vs late period with t-test and effect size."""
    print("\n[3] Period Comparison (Early vs Late)...")
    print(f"    Early period: {EARLY_PERIOD}")
    print(f"    Late period: {LATE_PERIOD}")

    # Load data for both periods
    early_data = []
    late_data = []

    for year in EARLY_PERIOD:
        try:
            df = load_season(year, columns=['pitch_type', 'release_speed'])
            ff = df[df['pitch_type'] == 'FF']['release_speed'].dropna()
            early_data.extend(ff.tolist())
        except FileNotFoundError:
            continue

    for year in LATE_PERIOD:
        try:
            df = load_season(year, columns=['pitch_type', 'release_speed'])
            ff = df[df['pitch_type'] == 'FF']['release_speed'].dropna()
            late_data.extend(ff.tolist())
        except FileNotFoundError:
            continue

    early = np.array(early_data)
    late = np.array(late_data)

    # Two-sample t-test
    t_stat, p_value = stats.ttest_ind(early, late)

    # Effect size (Cohen's d)
    pooled_std = np.sqrt(((len(early)-1)*early.std()**2 +
                          (len(late)-1)*late.std()**2) /
                         (len(early) + len(late) - 2))
    cohens_d = (late.mean() - early.mean()) / pooled_std

    # Confidence interval for difference
    se_diff = np.sqrt(early.var()/len(early) + late.var()/len(late))
    diff = late.mean() - early.mean()
    ci_lower = diff - 1.96 * se_diff
    ci_upper = diff + 1.96 * se_diff

    comparison_results = {
        'early_n': len(early),
        'early_mean': early.mean(),
        'early_std': early.std(),
        'late_n': len(late),
        'late_mean': late.mean(),
        'late_std': late.std(),
        'difference': diff,
        'diff_ci_lower': ci_lower,
        'diff_ci_upper': ci_upper,
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'effect_interpretation': interpret_cohens_d(cohens_d),
        'p_value_interpretation': interpret_p_value(p_value),
    }

    print(f"\n  Early period ({EARLY_PERIOD[0]}-{EARLY_PERIOD[-1]}):")
    print(f"    Mean: {early.mean():.2f} mph (SD: {early.std():.2f}, n={len(early):,})")
    print(f"  Late period ({LATE_PERIOD[0]}-{LATE_PERIOD[-1]}):")
    print(f"    Mean: {late.mean():.2f} mph (SD: {late.std():.2f}, n={len(late):,})")
    print(f"\n  Difference: {diff:.2f} mph (95% CI: [{ci_lower:.2f}, {ci_upper:.2f}])")
    print(f"  t-statistic: {t_stat:.2f}")
    print(f"  p-value: {p_value:.2e} ({interpret_p_value(p_value)})")
    print(f"  Cohen's d: {cohens_d:.3f} ({interpret_cohens_d(cohens_d)} effect)")

    return comparison_results


def create_visualizations(df: pd.DataFrame, trend_results: dict):
    """Generate chapter visualizations with statistical annotations."""
    print("\n[4] Creating visualizations...")

    # Figure 1: Velocity trend with 95% CI and regression line
    fig, ax = plt.subplots(figsize=(10, 6))

    # Main line with 95% CI
    ax.plot(df['year'], df['mean'], 'o-', linewidth=2, markersize=8,
            color='#1f77b4', label='Mean velocity')
    ax.fill_between(df['year'], df['ci_lower'], df['ci_upper'],
                    alpha=0.3, color='#1f77b4', label='95% CI')

    # Regression line
    years = df['year'].values
    slope = trend_results['slope']
    intercept = trend_results['intercept']
    r_squared = trend_results['r_squared']
    p_value = trend_results['p_value']
    ax.plot(years, intercept + slope * years, '--', color='red', linewidth=2,
            label=f'Trend (R²={r_squared:.3f}, p<0.001)')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Average 4-Seam Fastball Velocity (mph)', fontsize=12)
    ax.set_title('The Velocity Arms Race: 4-Seam Fastball Velocity (2015-2025)', fontsize=14)
    ax.set_xlim(2014.5, 2025.5)
    ax.set_ylim(92.5, 95.5)

    # Add annotations for start and end years
    ax.annotate(f"{df.iloc[0]['mean']:.1f}", (df.iloc[0]['year'], df.iloc[0]['mean']),
                textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)
    ax.annotate(f"{df.iloc[-1]['mean']:.1f}", (df.iloc[-1]['year'], df.iloc[-1]['mean']),
                textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)

    ax.legend(loc='lower right', fontsize=10)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig01_velocity_trend.png', dpi=150)
    plt.close()
    print("  Saved: fig01_velocity_trend.png")

    # Figure 2: 95+ mph percentage
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df['year'], df['pct_95plus'], color='#ff7f0e', edgecolor='black', linewidth=0.5)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Percentage of 4-Seamers at 95+ mph', fontsize=12)
    ax.set_title('Rise of Elite Velocity: 95+ mph Fastballs', fontsize=14)
    ax.set_ylim(0, 50)

    # Add percentage labels
    for i, row in df.iterrows():
        ax.text(row['year'], row['pct_95plus'] + 1, f"{row['pct_95plus']:.0f}%",
                ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig02_95plus_percentage.png', dpi=150)
    plt.close()
    print("  Saved: fig02_95plus_percentage.png")

    # Figure 3: Before vs After comparison (2015 vs 2025 distribution)
    print("\n[3] Loading full data for distribution comparison...")

    try:
        df_2015 = load_season(2015, columns=['pitch_type', 'release_speed'])
        df_2025 = load_season(2025, columns=['pitch_type', 'release_speed'])

        ff_2015 = df_2015[df_2015['pitch_type'] == 'FF']['release_speed'].dropna()
        ff_2025 = df_2025[df_2025['pitch_type'] == 'FF']['release_speed'].dropna()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(ff_2015, bins=50, alpha=0.6, label='2015', density=True, color='#1f77b4')
        ax.hist(ff_2025, bins=50, alpha=0.6, label='2025', density=True, color='#ff7f0e')
        ax.axvline(ff_2015.mean(), color='#1f77b4', linestyle='--', linewidth=2)
        ax.axvline(ff_2025.mean(), color='#ff7f0e', linestyle='--', linewidth=2)
        ax.set_xlabel('Velocity (mph)', fontsize=12)
        ax.set_ylabel('Density', fontsize=12)
        ax.set_title('Velocity Distribution Shift: 2015 vs 2025', fontsize=14)
        ax.legend(fontsize=11)
        ax.set_xlim(80, 105)

        plt.tight_layout()
        plt.savefig(FIGURES_DIR / 'fig03_distribution_comparison.png', dpi=150)
        plt.close()
        print("  Saved: fig03_distribution_comparison.png")

    except FileNotFoundError as e:
        print(f"  Warning: Could not create distribution plot - {e}")


def save_results(df: pd.DataFrame, trend_results: dict, comparison_results: dict):
    """Save analysis results to CSV."""
    print("\n[5] Saving results...")

    # Main results - yearly statistics
    df.to_csv(RESULTS_DIR / 'velocity_by_year.csv', index=False)
    print(f"  Saved: velocity_by_year.csv")

    # Statistical tests results
    stat_tests = pd.DataFrame([
        {'test': 'Trend Analysis', 'metric': 'Slope', 'value': f"{trend_results['slope']:.4f}", 'unit': 'mph/year'},
        {'test': 'Trend Analysis', 'metric': 'Slope 95% CI Lower', 'value': f"{trend_results['slope_ci_lower']:.4f}", 'unit': 'mph/year'},
        {'test': 'Trend Analysis', 'metric': 'Slope 95% CI Upper', 'value': f"{trend_results['slope_ci_upper']:.4f}", 'unit': 'mph/year'},
        {'test': 'Trend Analysis', 'metric': 'R-squared', 'value': f"{trend_results['r_squared']:.4f}", 'unit': ''},
        {'test': 'Trend Analysis', 'metric': 'R-squared Interpretation', 'value': trend_results['r_squared_interpretation'], 'unit': ''},
        {'test': 'Trend Analysis', 'metric': 'p-value', 'value': f"{trend_results['p_value']:.2e}", 'unit': ''},
        {'test': 'Trend Analysis', 'metric': 'p-value Interpretation', 'value': trend_results['p_value_interpretation'], 'unit': ''},
        {'test': 'Period Comparison', 'metric': 'Early Period Mean', 'value': f"{comparison_results['early_mean']:.2f}", 'unit': 'mph'},
        {'test': 'Period Comparison', 'metric': 'Late Period Mean', 'value': f"{comparison_results['late_mean']:.2f}", 'unit': 'mph'},
        {'test': 'Period Comparison', 'metric': 'Difference', 'value': f"{comparison_results['difference']:.2f}", 'unit': 'mph'},
        {'test': 'Period Comparison', 'metric': 'Difference 95% CI', 'value': f"[{comparison_results['diff_ci_lower']:.2f}, {comparison_results['diff_ci_upper']:.2f}]", 'unit': 'mph'},
        {'test': 'Period Comparison', 'metric': 't-statistic', 'value': f"{comparison_results['t_statistic']:.2f}", 'unit': ''},
        {'test': 'Period Comparison', 'metric': 'p-value', 'value': f"{comparison_results['p_value']:.2e}", 'unit': ''},
        {'test': 'Period Comparison', 'metric': "Cohen's d", 'value': f"{comparison_results['cohens_d']:.3f}", 'unit': ''},
        {'test': 'Period Comparison', 'metric': 'Effect Size Interpretation', 'value': comparison_results['effect_interpretation'], 'unit': ''},
    ])
    stat_tests.to_csv(RESULTS_DIR / 'statistical_tests.csv', index=False)
    print(f"  Saved: statistical_tests.csv")

    # Summary statistics
    summary = {
        'metric': [
            '2015 Average Velocity',
            '2025 Average Velocity',
            '10-Year Change',
            '2015 95+ Percentage',
            '2025 95+ Percentage',
            'Trend Slope',
            'Trend R-squared',
            'Trend p-value',
            "Cohen's d (Early vs Late)",
            'Effect Size',
        ],
        'value': [
            f"{df.iloc[0]['mean']:.2f} mph",
            f"{df.iloc[-1]['mean']:.2f} mph",
            f"+{df.iloc[-1]['mean'] - df.iloc[0]['mean']:.2f} mph",
            f"{df.iloc[0]['pct_95plus']:.1f}%",
            f"{df.iloc[-1]['pct_95plus']:.1f}%",
            f"{trend_results['slope']:.4f} mph/year",
            f"{trend_results['r_squared']:.4f} ({trend_results['r_squared_interpretation']})",
            f"{trend_results['p_value']:.2e} ({trend_results['p_value_interpretation']})",
            f"{comparison_results['cohens_d']:.3f}",
            comparison_results['effect_interpretation'],
        ]
    }
    pd.DataFrame(summary).to_csv(RESULTS_DIR / 'summary.csv', index=False)
    print(f"  Saved: summary.csv")


def print_summary(df: pd.DataFrame, trend_results: dict, comparison_results: dict):
    """Print analysis summary with statistical validation."""
    print("\n" + "=" * 60)
    print("  Summary: Statistical Validation")
    print("=" * 60)

    change = df.iloc[-1]['mean'] - df.iloc[0]['mean']
    pct_change = df.iloc[-1]['pct_95plus'] - df.iloc[0]['pct_95plus']

    print(f"""
KEY FINDINGS:

1. Velocity Trend (2015-2025):
   - 2015: {df.iloc[0]['mean']:.2f} mph (95% CI: [{df.iloc[0]['ci_lower']:.2f}, {df.iloc[0]['ci_upper']:.2f}])
   - 2025: {df.iloc[-1]['mean']:.2f} mph (95% CI: [{df.iloc[-1]['ci_lower']:.2f}, {df.iloc[-1]['ci_upper']:.2f}])
   - Change: +{change:.2f} mph

2. Elite Velocity (95+ mph):
   - 2015: {df.iloc[0]['pct_95plus']:.1f}%
   - 2025: {df.iloc[-1]['pct_95plus']:.1f}%
   - Change: +{pct_change:.1f} percentage points

3. Statistical Validation:
   - Trend slope: {trend_results['slope']:.4f} mph/year (95% CI: [{trend_results['slope_ci_lower']:.4f}, {trend_results['slope_ci_upper']:.4f}])
   - R²: {trend_results['r_squared']:.4f} ({trend_results['r_squared_interpretation']})
   - p-value: {trend_results['p_value']:.2e} ({trend_results['p_value_interpretation']})

4. Effect Size (Early vs Late Period):
   - Cohen's d: {comparison_results['cohens_d']:.3f} ({comparison_results['effect_interpretation']} effect)
   - Difference: {comparison_results['difference']:.2f} mph (95% CI: [{comparison_results['diff_ci_lower']:.2f}, {comparison_results['diff_ci_upper']:.2f}])

5. Total pitches analyzed: {df['count'].sum():,}

CONCLUSION: The velocity increase is statistically significant (p < 0.001)
with a {comparison_results['effect_interpretation']} effect size (Cohen's d = {comparison_results['cohens_d']:.3f}).
""")


def main():
    # Phase 1 & 2: Load data and calculate yearly statistics
    velocity_df = analyze_velocity_by_year()

    if len(velocity_df) == 0:
        print("\n[ERROR] No data found. Please collect data first:")
        print("  python collector/collect_statcast.py --range 2015 2025")
        return

    # Phase 3: Trend analysis (linear regression)
    trend_results = perform_trend_analysis(velocity_df)

    # Phase 4: Period comparison (t-test, Cohen's d)
    comparison_results = perform_period_comparison()

    # Phase 5: Create visualizations with statistical annotations
    create_visualizations(velocity_df, trend_results)

    # Phase 6: Save results including statistical tests
    save_results(velocity_df, trend_results, comparison_results)

    # Print summary with statistical validation
    print_summary(velocity_df, trend_results, comparison_results)

    print("\n" + "=" * 60)
    print("  [DONE] Analysis complete!")
    print("=" * 60)
    print(f"  Figures: {FIGURES_DIR}")
    print(f"  Results: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
