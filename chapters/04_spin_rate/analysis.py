#!/usr/bin/env python3
"""
Chapter 4: Spin Rate Trends (2015-2025)

Research Question: How has pitch spin rate evolved over the past decade,
and what patterns emerge across different pitch types?

Hypotheses:
- H0: No significant change in average spin rate (slope = 0)
- H1: Significant increase in average spin rate (slope > 0)

Methodology:
1. Analyze spin rate trends for all pitches and by pitch type
2. Calculate yearly spin rate statistics with confidence intervals
3. Perform linear regression to quantify trend
4. Compare early period (2015-2017) vs late period (2023-2025) with t-test
5. Calculate effect size (Cohen's d) for practical significance
6. Examine pitch type-specific spin rate patterns

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

from statcast_analysis import load_season, AVAILABLE_SEASONS, PITCH_TYPES

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

# Key pitch types for analysis
KEY_PITCH_TYPES = {
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


def analyze_spin_by_year():
    """Calculate yearly spin rate statistics with confidence intervals."""
    print("=" * 60)
    print("  Chapter 4: Spin Rate Trends (2015-2025)")
    print("=" * 60)

    results = []

    print("\n[1] Loading data and calculating spin rate stats...")
    print("    Analyzing 4-seam fastball (FF) spin rates\n")

    for year in AVAILABLE_SEASONS:
        try:
            df = load_season(year, columns=['pitch_type', 'release_spin_rate'])

            # Filter to 4-seam fastballs and valid spin rates
            ff = df[(df['pitch_type'] == 'FF') &
                    (df['release_spin_rate'].notna()) &
                    (df['release_spin_rate'] > 0) &
                    (df['release_spin_rate'] < 4000)]['release_spin_rate']

            if len(ff) == 0:
                continue

            # Calculate statistics
            n = len(ff)
            mean = ff.mean()
            std = ff.std()
            se = std / np.sqrt(n)

            results.append({
                'year': year,
                'count': n,
                'mean': mean,
                'median': ff.median(),
                'std': std,
                'se': se,
                'ci_lower': mean - 1.96 * se,
                'ci_upper': mean + 1.96 * se,
                'pct_2500plus': (ff >= 2500).mean() * 100,
                'pct_2700plus': (ff >= 2700).mean() * 100,
                'max': ff.max(),
                'p10': ff.quantile(0.10),
                'p25': ff.quantile(0.25),
                'p75': ff.quantile(0.75),
                'p90': ff.quantile(0.90),
            })

            print(f"  {year}: {mean:.0f} rpm (95% CI: [{mean - 1.96*se:.0f}, {mean + 1.96*se:.0f}], n={n:,})")

        except FileNotFoundError:
            print(f"  {year}: data not found, skipping")
            continue

    return pd.DataFrame(results)


def analyze_spin_by_pitch_type():
    """Analyze spin rate trends for each pitch type."""
    print("\n[2] Analyzing spin rates by pitch type...")

    pitch_type_results = []

    for pitch_code, pitch_name in KEY_PITCH_TYPES.items():
        yearly_means = []

        for year in AVAILABLE_SEASONS:
            try:
                df = load_season(year, columns=['pitch_type', 'release_spin_rate'])

                spin = df[(df['pitch_type'] == pitch_code) &
                          (df['release_spin_rate'].notna()) &
                          (df['release_spin_rate'] > 0) &
                          (df['release_spin_rate'] < 4000)]['release_spin_rate']

                if len(spin) > 0:
                    yearly_means.append({
                        'year': year,
                        'pitch_type': pitch_code,
                        'pitch_name': pitch_name,
                        'mean': spin.mean(),
                        'count': len(spin),
                    })
            except FileNotFoundError:
                continue

        if yearly_means:
            pitch_type_results.extend(yearly_means)

    return pd.DataFrame(pitch_type_results)


def perform_trend_analysis(df: pd.DataFrame):
    """Perform linear regression trend analysis."""
    print("\n[3] Trend Analysis (Linear Regression)...")

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

    print(f"  Slope: {slope:.2f} rpm/year (95% CI: [{slope_ci_lower:.2f}, {slope_ci_upper:.2f}])")
    print(f"  R²: {r_squared:.4f} ({interpret_r_squared(r_squared)})")
    print(f"  p-value: {p_value:.2e} ({interpret_p_value(p_value)})")
    print(f"  Projected 10-year change: {slope * 10:.0f} rpm")

    return trend_results


def perform_period_comparison():
    """Compare early period vs late period with t-test and effect size."""
    print("\n[4] Period Comparison (Early vs Late)...")
    print(f"    Early period: {EARLY_PERIOD}")
    print(f"    Late period: {LATE_PERIOD}")

    # Load data for both periods
    early_data = []
    late_data = []

    for year in EARLY_PERIOD:
        try:
            df = load_season(year, columns=['pitch_type', 'release_spin_rate'])
            spin = df[(df['pitch_type'] == 'FF') &
                      (df['release_spin_rate'].notna()) &
                      (df['release_spin_rate'] > 0) &
                      (df['release_spin_rate'] < 4000)]['release_spin_rate']
            early_data.extend(spin.tolist())
        except FileNotFoundError:
            continue

    for year in LATE_PERIOD:
        try:
            df = load_season(year, columns=['pitch_type', 'release_spin_rate'])
            spin = df[(df['pitch_type'] == 'FF') &
                      (df['release_spin_rate'].notna()) &
                      (df['release_spin_rate'] > 0) &
                      (df['release_spin_rate'] < 4000)]['release_spin_rate']
            late_data.extend(spin.tolist())
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
    print(f"    Mean: {early.mean():.0f} rpm (SD: {early.std():.0f}, n={len(early):,})")
    print(f"  Late period ({LATE_PERIOD[0]}-{LATE_PERIOD[-1]}):")
    print(f"    Mean: {late.mean():.0f} rpm (SD: {late.std():.0f}, n={len(late):,})")
    print(f"\n  Difference: {diff:.0f} rpm (95% CI: [{ci_lower:.0f}, {ci_upper:.0f}])")
    print(f"  t-statistic: {t_stat:.2f}")
    print(f"  p-value: {p_value:.2e} ({interpret_p_value(p_value)})")
    print(f"  Cohen's d: {cohens_d:.3f} ({interpret_cohens_d(cohens_d)} effect)")

    return comparison_results


def create_visualizations(df: pd.DataFrame, pitch_type_df: pd.DataFrame, trend_results: dict):
    """Generate chapter visualizations with statistical annotations."""
    print("\n[5] Creating visualizations...")

    # Figure 1: Spin rate trend with 95% CI and regression line
    fig, ax = plt.subplots(figsize=(10, 6))

    # Main line with 95% CI
    ax.plot(df['year'], df['mean'], 'o-', linewidth=2, markersize=8,
            color='#1f77b4', label='Mean spin rate')
    ax.fill_between(df['year'], df['ci_lower'], df['ci_upper'],
                    alpha=0.3, color='#1f77b4', label='95% CI')

    # Regression line
    years = df['year'].values
    slope = trend_results['slope']
    intercept = trend_results['intercept']
    r_squared = trend_results['r_squared']
    ax.plot(years, intercept + slope * years, '--', color='red', linewidth=2,
            label=f'Trend (R²={r_squared:.3f})')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Average 4-Seam Fastball Spin Rate (rpm)', fontsize=12)
    ax.set_title('Spin Rate Trends: 4-Seam Fastball (2015-2025)', fontsize=14)
    ax.set_xlim(2014.5, 2025.5)

    # Dynamic y-limits based on data
    y_min = df['ci_lower'].min() - 30
    y_max = df['ci_upper'].max() + 30
    ax.set_ylim(y_min, y_max)

    # Add annotations for start and end years
    ax.annotate(f"{df.iloc[0]['mean']:.0f}", (df.iloc[0]['year'], df.iloc[0]['mean']),
                textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)
    ax.annotate(f"{df.iloc[-1]['mean']:.0f}", (df.iloc[-1]['year'], df.iloc[-1]['mean']),
                textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)

    ax.legend(loc='best', fontsize=10)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig01_spin_rate_trend.png', dpi=150)
    plt.close()
    print("  Saved: fig01_spin_rate_trend.png")

    # Figure 2: 2500+ rpm percentage
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df['year'], df['pct_2500plus'], color='#ff7f0e', edgecolor='black', linewidth=0.5)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Percentage of 4-Seamers at 2500+ rpm', fontsize=12)
    ax.set_title('High Spin Fastballs: 2500+ rpm', fontsize=14)

    # Add percentage labels
    for i, row in df.iterrows():
        ax.text(row['year'], row['pct_2500plus'] + 1, f"{row['pct_2500plus']:.0f}%",
                ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig02_2500plus_percentage.png', dpi=150)
    plt.close()
    print("  Saved: fig02_2500plus_percentage.png")

    # Figure 3: Spin rate by pitch type
    fig, ax = plt.subplots(figsize=(12, 6))

    colors = {'FF': '#1f77b4', 'SI': '#ff7f0e', 'SL': '#2ca02c', 'CU': '#d62728', 'CH': '#9467bd'}

    for pitch_code in KEY_PITCH_TYPES.keys():
        pitch_data = pitch_type_df[pitch_type_df['pitch_type'] == pitch_code]
        if len(pitch_data) > 0:
            ax.plot(pitch_data['year'], pitch_data['mean'], 'o-',
                   label=KEY_PITCH_TYPES[pitch_code], color=colors.get(pitch_code, 'gray'),
                   linewidth=2, markersize=6)

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Average Spin Rate (rpm)', fontsize=12)
    ax.set_title('Spin Rate Trends by Pitch Type (2015-2025)', fontsize=14)
    ax.legend(loc='best', fontsize=10)
    ax.set_xlim(2014.5, 2025.5)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig03_spin_by_pitch_type.png', dpi=150)
    plt.close()
    print("  Saved: fig03_spin_by_pitch_type.png")

    # Figure 4: Distribution comparison (2015 vs 2025)
    print("    Loading full data for distribution comparison...")

    try:
        df_2015 = load_season(2015, columns=['pitch_type', 'release_spin_rate'])
        df_2025 = load_season(2025, columns=['pitch_type', 'release_spin_rate'])

        spin_2015 = df_2015[(df_2015['pitch_type'] == 'FF') &
                           (df_2015['release_spin_rate'].notna()) &
                           (df_2015['release_spin_rate'] > 0) &
                           (df_2015['release_spin_rate'] < 4000)]['release_spin_rate']
        spin_2025 = df_2025[(df_2025['pitch_type'] == 'FF') &
                           (df_2025['release_spin_rate'].notna()) &
                           (df_2025['release_spin_rate'] > 0) &
                           (df_2025['release_spin_rate'] < 4000)]['release_spin_rate']

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(spin_2015, bins=50, alpha=0.6, label='2015', density=True, color='#1f77b4')
        ax.hist(spin_2025, bins=50, alpha=0.6, label='2025', density=True, color='#ff7f0e')
        ax.axvline(spin_2015.mean(), color='#1f77b4', linestyle='--', linewidth=2)
        ax.axvline(spin_2025.mean(), color='#ff7f0e', linestyle='--', linewidth=2)
        ax.set_xlabel('Spin Rate (rpm)', fontsize=12)
        ax.set_ylabel('Density', fontsize=12)
        ax.set_title('Spin Rate Distribution Shift: 2015 vs 2025', fontsize=14)
        ax.legend(fontsize=11)
        ax.set_xlim(1500, 3200)

        plt.tight_layout()
        plt.savefig(FIGURES_DIR / 'fig04_distribution_comparison.png', dpi=150)
        plt.close()
        print("  Saved: fig04_distribution_comparison.png")

    except FileNotFoundError as e:
        print(f"  Warning: Could not create distribution plot - {e}")


def save_results(df: pd.DataFrame, pitch_type_df: pd.DataFrame,
                 trend_results: dict, comparison_results: dict):
    """Save analysis results to CSV."""
    print("\n[6] Saving results...")

    # Main results - yearly statistics
    df.to_csv(RESULTS_DIR / 'spin_rate_by_year.csv', index=False)
    print(f"  Saved: spin_rate_by_year.csv")

    # Pitch type results
    pitch_type_df.to_csv(RESULTS_DIR / 'spin_rate_by_pitch_type.csv', index=False)
    print(f"  Saved: spin_rate_by_pitch_type.csv")

    # Statistical tests results
    stat_tests = pd.DataFrame([
        {'test': 'Trend Analysis', 'metric': 'Slope', 'value': f"{trend_results['slope']:.2f}", 'unit': 'rpm/year'},
        {'test': 'Trend Analysis', 'metric': 'Slope 95% CI Lower', 'value': f"{trend_results['slope_ci_lower']:.2f}", 'unit': 'rpm/year'},
        {'test': 'Trend Analysis', 'metric': 'Slope 95% CI Upper', 'value': f"{trend_results['slope_ci_upper']:.2f}", 'unit': 'rpm/year'},
        {'test': 'Trend Analysis', 'metric': 'R-squared', 'value': f"{trend_results['r_squared']:.4f}", 'unit': ''},
        {'test': 'Trend Analysis', 'metric': 'R-squared Interpretation', 'value': trend_results['r_squared_interpretation'], 'unit': ''},
        {'test': 'Trend Analysis', 'metric': 'p-value', 'value': f"{trend_results['p_value']:.2e}", 'unit': ''},
        {'test': 'Trend Analysis', 'metric': 'p-value Interpretation', 'value': trend_results['p_value_interpretation'], 'unit': ''},
        {'test': 'Period Comparison', 'metric': 'Early Period Mean', 'value': f"{comparison_results['early_mean']:.0f}", 'unit': 'rpm'},
        {'test': 'Period Comparison', 'metric': 'Late Period Mean', 'value': f"{comparison_results['late_mean']:.0f}", 'unit': 'rpm'},
        {'test': 'Period Comparison', 'metric': 'Difference', 'value': f"{comparison_results['difference']:.0f}", 'unit': 'rpm'},
        {'test': 'Period Comparison', 'metric': 'Difference 95% CI', 'value': f"[{comparison_results['diff_ci_lower']:.0f}, {comparison_results['diff_ci_upper']:.0f}]", 'unit': 'rpm'},
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
            '2015 Average Spin Rate',
            '2025 Average Spin Rate',
            '10-Year Change',
            '2015 2500+ Percentage',
            '2025 2500+ Percentage',
            'Trend Slope',
            'Trend R-squared',
            'Trend p-value',
            "Cohen's d (Early vs Late)",
            'Effect Size',
        ],
        'value': [
            f"{df.iloc[0]['mean']:.0f} rpm",
            f"{df.iloc[-1]['mean']:.0f} rpm",
            f"{df.iloc[-1]['mean'] - df.iloc[0]['mean']:+.0f} rpm",
            f"{df.iloc[0]['pct_2500plus']:.1f}%",
            f"{df.iloc[-1]['pct_2500plus']:.1f}%",
            f"{trend_results['slope']:.2f} rpm/year",
            f"{trend_results['r_squared']:.4f} ({trend_results['r_squared_interpretation']})",
            f"{trend_results['p_value']:.2e} ({trend_results['p_value_interpretation']})",
            f"{comparison_results['cohens_d']:.3f}",
            comparison_results['effect_interpretation'],
        ]
    }
    pd.DataFrame(summary).to_csv(RESULTS_DIR / 'summary.csv', index=False)
    print(f"  Saved: summary.csv")


def print_summary(df: pd.DataFrame, comparison_results: dict):
    """Print analysis summary."""
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)

    change = df.iloc[-1]['mean'] - df.iloc[0]['mean']
    pct_change = df.iloc[-1]['pct_2500plus'] - df.iloc[0]['pct_2500plus']

    print(f"""
Key Findings:

1. Average 4-seam fastball spin rate:
   - 2015: {df.iloc[0]['mean']:.0f} rpm
   - 2025: {df.iloc[-1]['mean']:.0f} rpm
   - Change: {change:+.0f} rpm

2. Percentage of 2500+ rpm fastballs:
   - 2015: {df.iloc[0]['pct_2500plus']:.1f}%
   - 2025: {df.iloc[-1]['pct_2500plus']:.1f}%
   - Change: {pct_change:+.1f} percentage points

3. Effect size (Cohen's d): {comparison_results['cohens_d']:.3f} ({comparison_results['effect_interpretation']})

4. Total pitches analyzed: {df['count'].sum():,}
""")


def main():
    # Run analysis
    spin_df = analyze_spin_by_year()

    if len(spin_df) == 0:
        print("\n[ERROR] No data found. Please collect data first:")
        print("  python collector/collect_statcast.py --range 2015 2025")
        return

    # Analyze by pitch type
    pitch_type_df = analyze_spin_by_pitch_type()

    # Trend analysis
    trend_results = perform_trend_analysis(spin_df)

    # Period comparison
    comparison_results = perform_period_comparison()

    # Create visualizations
    create_visualizations(spin_df, pitch_type_df, trend_results)

    # Save results
    save_results(spin_df, pitch_type_df, trend_results, comparison_results)

    # Print summary
    print_summary(spin_df, comparison_results)

    print("\n[DONE] Analysis complete!")
    print(f"  Figures: {FIGURES_DIR}")
    print(f"  Results: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
