#!/usr/bin/env python3
"""
Chapter 8: Velocity/Spin Decay by Inning (2015-2025)

Research Question: How do velocity and spin rate change as pitchers
progress through a game, and has this fatigue pattern evolved?

Hypotheses:
- H0: No significant velocity/spin decay by inning
- H1: Significant decline in velocity/spin as innings increase

Key Analyses:
1. Velocity by inning (innings 1-9)
2. Spin rate by inning
3. Starter vs reliever patterns
4. Evolution of fatigue tolerance over time

Usage:
    python analysis.py
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from statcast_analysis import load_season, AVAILABLE_SEASONS

FIGURES_DIR = Path(__file__).parent / "figures"
RESULTS_DIR = Path(__file__).parent / "results"
FIGURES_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


def load_inning_data():
    """Load pitch data with inning information."""
    print("=" * 60)
    print("  Chapter 8: Velocity/Spin Decay by Inning (2015-2025)")
    print("=" * 60)
    print("\n[1] Loading pitch data with inning information...")

    all_data = []

    for year in AVAILABLE_SEASONS:
        try:
            df = load_season(year, columns=[
                'pitch_type', 'release_speed', 'release_spin_rate',
                'inning', 'pitcher'
            ])
            df['game_year'] = year

            # Ensure numeric
            df['release_speed'] = pd.to_numeric(df['release_speed'], errors='coerce')
            df['release_spin_rate'] = pd.to_numeric(df['release_spin_rate'], errors='coerce')
            df['inning'] = pd.to_numeric(df['inning'], errors='coerce')

            # Filter to valid innings (1-9 regular, 10+ extra)
            df = df.dropna(subset=['pitch_type', 'inning', 'release_speed'])
            df = df[(df['inning'] >= 1) & (df['inning'] <= 12)]

            # Filter to 4-seam fastballs for consistency
            df = df[df['pitch_type'] == 'FF']

            all_data.append(df)
            print(f"  {year}: {len(df):,} 4-seam fastballs")

        except FileNotFoundError:
            print(f"  {year}: data not found, skipping")
            continue

    combined = pd.concat(all_data, ignore_index=True)
    print(f"\n  Total 4-seam fastballs: {len(combined):,}")

    return combined


def analyze_velocity_by_inning(df: pd.DataFrame):
    """Analyze velocity patterns by inning."""
    print("\n[2] Analyzing velocity by inning...")

    results = []

    for inning in range(1, 10):  # Focus on innings 1-9
        inning_data = df[df['inning'] == inning]['release_speed'].dropna()

        if len(inning_data) < 1000:
            continue

        n = len(inning_data)
        mean = inning_data.mean()
        std = inning_data.std()
        se = std / np.sqrt(n)

        results.append({
            'inning': inning,
            'n': n,
            'mean': mean,
            'std': std,
            'se': se,
            'ci_lower': mean - 1.96 * se,
            'ci_upper': mean + 1.96 * se,
        })

    results_df = pd.DataFrame(results)

    # Print summary
    print("\n  4-Seam Fastball Velocity by Inning:")
    for _, row in results_df.iterrows():
        print(f"    Inning {int(row['inning'])}: {row['mean']:.2f} mph "
              f"(95% CI: [{row['ci_lower']:.2f}, {row['ci_upper']:.2f}], n={int(row['n']):,})")

    # Calculate decay
    first_inning = results_df[results_df['inning'] == 1]['mean'].values[0]
    last_inning = results_df[results_df['inning'] == 9]['mean'].values[0]
    total_decay = last_inning - first_inning

    print(f"\n  Total Decay (Inning 1 → 9): {total_decay:.2f} mph")

    return results_df


def analyze_spin_by_inning(df: pd.DataFrame):
    """Analyze spin rate patterns by inning."""
    print("\n[3] Analyzing spin rate by inning...")

    results = []

    for inning in range(1, 10):
        inning_data = df[df['inning'] == inning]['release_spin_rate'].dropna()
        inning_data = inning_data[(inning_data > 1000) & (inning_data < 3500)]

        if len(inning_data) < 1000:
            continue

        n = len(inning_data)
        mean = inning_data.mean()
        std = inning_data.std()
        se = std / np.sqrt(n)

        results.append({
            'inning': inning,
            'n': n,
            'mean': mean,
            'std': std,
            'se': se,
            'ci_lower': mean - 1.96 * se,
            'ci_upper': mean + 1.96 * se,
        })

    results_df = pd.DataFrame(results)

    print("\n  4-Seam Fastball Spin Rate by Inning:")
    for _, row in results_df.iterrows():
        print(f"    Inning {int(row['inning'])}: {row['mean']:.0f} rpm "
              f"(n={int(row['n']):,})")

    # Calculate decay
    first_inning = results_df[results_df['inning'] == 1]['mean'].values[0]
    last_inning = results_df[results_df['inning'] == 9]['mean'].values[0]
    total_decay = last_inning - first_inning

    print(f"\n  Total Spin Change (Inning 1 → 9): {total_decay:+.0f} rpm")

    return results_df


def perform_trend_analysis(velocity_df: pd.DataFrame, spin_df: pd.DataFrame):
    """Perform linear regression on inning-based decay."""
    print("\n[4] Trend Analysis (Linear Regression)...")

    results = {}

    # Velocity trend
    innings = velocity_df['inning'].values
    velocity = velocity_df['mean'].values

    slope, intercept, r_value, p_value, std_err = stats.linregress(innings, velocity)

    results['velocity'] = {
        'slope': slope,
        'slope_ci_lower': slope - 1.96 * std_err,
        'slope_ci_upper': slope + 1.96 * std_err,
        'intercept': intercept,
        'r_squared': r_value**2,
        'p_value': p_value,
    }

    print(f"\n  Velocity Decay:")
    print(f"    Slope: {slope:.4f} mph/inning")
    print(f"    95% CI: [{slope - 1.96*std_err:.4f}, {slope + 1.96*std_err:.4f}]")
    print(f"    R²: {results['velocity']['r_squared']:.4f}")
    print(f"    p-value: {p_value:.2e}")

    # Spin trend
    innings = spin_df['inning'].values
    spin = spin_df['mean'].values

    slope, intercept, r_value, p_value, std_err = stats.linregress(innings, spin)

    results['spin'] = {
        'slope': slope,
        'slope_ci_lower': slope - 1.96 * std_err,
        'slope_ci_upper': slope + 1.96 * std_err,
        'intercept': intercept,
        'r_squared': r_value**2,
        'p_value': p_value,
    }

    print(f"\n  Spin Rate Change:")
    print(f"    Slope: {slope:.2f} rpm/inning")
    print(f"    R²: {results['spin']['r_squared']:.4f}")
    print(f"    p-value: {p_value:.2e}")

    return results


def analyze_early_vs_late_innings(df: pd.DataFrame):
    """Compare early innings (1-3) vs late innings (7-9)."""
    print("\n[5] Early vs Late Innings Comparison...")

    early = df[df['inning'].isin([1, 2, 3])]['release_speed'].dropna().astype(float)
    late = df[df['inning'].isin([7, 8, 9])]['release_speed'].dropna().astype(float)

    # t-test
    t_stat, p_value = stats.ttest_ind(early, late)

    # Cohen's d
    pooled_std = np.sqrt(((len(early)-1)*early.std()**2 +
                          (len(late)-1)*late.std()**2) /
                         (len(early) + len(late) - 2))
    cohens_d = (late.mean() - early.mean()) / pooled_std

    # Confidence interval
    se_diff = np.sqrt(early.var()/len(early) + late.var()/len(late))
    diff = late.mean() - early.mean()

    comparison = {
        'early_mean': early.mean(),
        'early_std': early.std(),
        'early_n': len(early),
        'late_mean': late.mean(),
        'late_std': late.std(),
        'late_n': len(late),
        'difference': diff,
        'diff_ci_lower': diff - 1.96 * se_diff,
        'diff_ci_upper': diff + 1.96 * se_diff,
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
    }

    print(f"\n  Early Innings (1-3): {early.mean():.2f} mph (n={len(early):,})")
    print(f"  Late Innings (7-9): {late.mean():.2f} mph (n={len(late):,})")
    print(f"  Difference: {diff:.2f} mph")
    print(f"  Cohen's d: {cohens_d:.3f}")
    print(f"  p-value: {p_value:.2e}")

    return comparison


def analyze_yearly_fatigue_patterns(df: pd.DataFrame):
    """Analyze how fatigue patterns have changed over time."""
    print("\n[6] Yearly Fatigue Pattern Evolution...")

    results = []

    for year in sorted(df['game_year'].unique()):
        year_data = df[df['game_year'] == year]

        # Calculate velocity in inning 1 vs inning 6
        inning1 = year_data[year_data['inning'] == 1]['release_speed'].mean()
        inning6 = year_data[year_data['inning'] == 6]['release_speed'].mean()

        if pd.notna(inning1) and pd.notna(inning6):
            decay = inning6 - inning1
            results.append({
                'year': year,
                'inning1_velo': inning1,
                'inning6_velo': inning6,
                'decay_1_to_6': decay,
            })

    results_df = pd.DataFrame(results)

    print("\n  Velocity Decay (Inning 1 → 6) by Year:")
    for _, row in results_df.iterrows():
        print(f"    {int(row['year'])}: {row['inning1_velo']:.2f} → {row['inning6_velo']:.2f} "
              f"({row['decay_1_to_6']:+.2f} mph)")

    return results_df


def create_visualizations(velocity_df: pd.DataFrame, spin_df: pd.DataFrame,
                          trend_results: dict, yearly_df: pd.DataFrame):
    """Generate visualizations."""
    print("\n[7] Creating visualizations...")

    # Figure 1: Velocity by inning
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.errorbar(velocity_df['inning'], velocity_df['mean'],
                yerr=1.96*velocity_df['se'], fmt='o-',
                linewidth=2, markersize=10, capsize=5, color='#1f77b4')

    # Add regression line
    innings = velocity_df['inning'].values
    slope = trend_results['velocity']['slope']
    intercept = trend_results['velocity']['intercept']
    ax.plot(innings, intercept + slope * innings, '--', color='red',
            linewidth=2, label=f'Trend: {slope:.3f} mph/inning')

    ax.set_xlabel('Inning', fontsize=12)
    ax.set_ylabel('4-Seam Fastball Velocity (mph)', fontsize=12)
    ax.set_title('Velocity Decay by Inning', fontsize=14)
    ax.set_xticks(range(1, 10))
    ax.legend()

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig01_velocity_by_inning.png', dpi=150)
    plt.close()
    print("  Saved: fig01_velocity_by_inning.png")

    # Figure 2: Spin rate by inning
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.errorbar(spin_df['inning'], spin_df['mean'],
                yerr=1.96*spin_df['se'], fmt='s-',
                linewidth=2, markersize=10, capsize=5, color='#ff7f0e')

    # Add regression line
    innings = spin_df['inning'].values
    slope = trend_results['spin']['slope']
    intercept = trend_results['spin']['intercept']
    ax.plot(innings, intercept + slope * innings, '--', color='red',
            linewidth=2, label=f'Trend: {slope:.1f} rpm/inning')

    ax.set_xlabel('Inning', fontsize=12)
    ax.set_ylabel('4-Seam Fastball Spin Rate (rpm)', fontsize=12)
    ax.set_title('Spin Rate by Inning', fontsize=14)
    ax.set_xticks(range(1, 10))
    ax.legend()

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig02_spin_by_inning.png', dpi=150)
    plt.close()
    print("  Saved: fig02_spin_by_inning.png")

    # Figure 3: Combined velocity and spin (dual axis)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color1 = '#1f77b4'
    ax1.set_xlabel('Inning', fontsize=12)
    ax1.set_ylabel('Velocity (mph)', color=color1, fontsize=12)
    ax1.plot(velocity_df['inning'], velocity_df['mean'], 'o-',
             color=color1, linewidth=2, markersize=8, label='Velocity')
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = '#ff7f0e'
    ax2.set_ylabel('Spin Rate (rpm)', color=color2, fontsize=12)
    ax2.plot(spin_df['inning'], spin_df['mean'], 's-',
             color=color2, linewidth=2, markersize=8, label='Spin Rate')
    ax2.tick_params(axis='y', labelcolor=color2)

    ax1.set_title('Velocity and Spin Rate Progression Through Game', fontsize=14)
    ax1.set_xticks(range(1, 10))

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig03_velocity_spin_combined.png', dpi=150)
    plt.close()
    print("  Saved: fig03_velocity_spin_combined.png")

    # Figure 4: Yearly fatigue pattern evolution
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(yearly_df['year'], yearly_df['decay_1_to_6'],
           color=['#d62728' if x < 0 else '#2ca02c' for x in yearly_df['decay_1_to_6']],
           edgecolor='black', linewidth=0.5)

    ax.axhline(y=0, color='black', linewidth=1)
    ax.axhline(y=yearly_df['decay_1_to_6'].mean(), color='red', linestyle='--',
               label=f"Average: {yearly_df['decay_1_to_6'].mean():.2f} mph")

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Velocity Change: Inning 1 → 6 (mph)', fontsize=12)
    ax.set_title('Fatigue Pattern by Year', fontsize=14)
    ax.legend()

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig04_yearly_fatigue.png', dpi=150)
    plt.close()
    print("  Saved: fig04_yearly_fatigue.png")


def save_results(velocity_df: pd.DataFrame, spin_df: pd.DataFrame,
                 trend_results: dict, comparison: dict, yearly_df: pd.DataFrame):
    """Save results to CSV."""
    print("\n[8] Saving results...")

    velocity_df.to_csv(RESULTS_DIR / 'velocity_by_inning.csv', index=False)
    print("  Saved: velocity_by_inning.csv")

    spin_df.to_csv(RESULTS_DIR / 'spin_by_inning.csv', index=False)
    print("  Saved: spin_by_inning.csv")

    yearly_df.to_csv(RESULTS_DIR / 'yearly_fatigue.csv', index=False)
    print("  Saved: yearly_fatigue.csv")

    # Statistical tests
    stat_tests = [
        {'test': 'Velocity Decay', 'metric': 'Slope', 'value': f"{trend_results['velocity']['slope']:.4f}", 'unit': 'mph/inning'},
        {'test': 'Velocity Decay', 'metric': 'R-squared', 'value': f"{trend_results['velocity']['r_squared']:.4f}", 'unit': ''},
        {'test': 'Velocity Decay', 'metric': 'p-value', 'value': f"{trend_results['velocity']['p_value']:.2e}", 'unit': ''},
        {'test': 'Spin Change', 'metric': 'Slope', 'value': f"{trend_results['spin']['slope']:.2f}", 'unit': 'rpm/inning'},
        {'test': 'Spin Change', 'metric': 'R-squared', 'value': f"{trend_results['spin']['r_squared']:.4f}", 'unit': ''},
        {'test': 'Early vs Late', 'metric': 'Early Mean (Inn 1-3)', 'value': f"{comparison['early_mean']:.2f}", 'unit': 'mph'},
        {'test': 'Early vs Late', 'metric': 'Late Mean (Inn 7-9)', 'value': f"{comparison['late_mean']:.2f}", 'unit': 'mph'},
        {'test': 'Early vs Late', 'metric': 'Difference', 'value': f"{comparison['difference']:.2f}", 'unit': 'mph'},
        {'test': 'Early vs Late', 'metric': "Cohen's d", 'value': f"{comparison['cohens_d']:.3f}", 'unit': ''},
        {'test': 'Early vs Late', 'metric': 'p-value', 'value': f"{comparison['p_value']:.2e}", 'unit': ''},
    ]
    pd.DataFrame(stat_tests).to_csv(RESULTS_DIR / 'statistical_tests.csv', index=False)
    print("  Saved: statistical_tests.csv")

    # Summary
    summary = {
        'metric': [
            'Inning 1 Velocity',
            'Inning 9 Velocity',
            'Total Velocity Decay (1→9)',
            'Velocity Decay per Inning',
            'Inning 1 Spin Rate',
            'Inning 9 Spin Rate',
            'Early vs Late Cohen\'s d',
        ],
        'value': [
            f"{velocity_df.iloc[0]['mean']:.2f} mph",
            f"{velocity_df.iloc[-1]['mean']:.2f} mph",
            f"{velocity_df.iloc[-1]['mean'] - velocity_df.iloc[0]['mean']:.2f} mph",
            f"{trend_results['velocity']['slope']:.3f} mph/inning",
            f"{spin_df.iloc[0]['mean']:.0f} rpm",
            f"{spin_df.iloc[-1]['mean']:.0f} rpm",
            f"{comparison['cohens_d']:.3f}",
        ]
    }
    pd.DataFrame(summary).to_csv(RESULTS_DIR / 'summary.csv', index=False)
    print("  Saved: summary.csv")


def print_summary(velocity_df: pd.DataFrame, trend_results: dict, comparison: dict):
    """Print analysis summary."""
    print("\n" + "=" * 60)
    print("  Summary: Velocity/Spin Decay by Inning")
    print("=" * 60)

    total_decay = velocity_df.iloc[-1]['mean'] - velocity_df.iloc[0]['mean']

    print(f"""
KEY FINDINGS:

1. Velocity Decay Pattern:
   - Inning 1: {velocity_df.iloc[0]['mean']:.2f} mph
   - Inning 9: {velocity_df.iloc[-1]['mean']:.2f} mph
   - Total Decay: {total_decay:.2f} mph
   - Rate: {trend_results['velocity']['slope']:.3f} mph/inning
   - R²: {trend_results['velocity']['r_squared']:.4f}

2. Early vs Late Innings:
   - Early (1-3): {comparison['early_mean']:.2f} mph
   - Late (7-9): {comparison['late_mean']:.2f} mph
   - Difference: {comparison['difference']:.2f} mph
   - Cohen's d: {comparison['cohens_d']:.3f}
   - p-value: {comparison['p_value']:.2e}

3. Spin Rate:
   - Slope: {trend_results['spin']['slope']:.2f} rpm/inning
   - R²: {trend_results['spin']['r_squared']:.4f}

INTERPRETATION: Pitchers show measurable velocity decline as games progress,
losing approximately {abs(trend_results['velocity']['slope']):.2f} mph per inning on average.
""")


def main():
    df = load_inning_data()

    if len(df) == 0:
        print("\n[ERROR] No data found.")
        return

    velocity_df = analyze_velocity_by_inning(df)
    spin_df = analyze_spin_by_inning(df)
    trend_results = perform_trend_analysis(velocity_df, spin_df)
    comparison = analyze_early_vs_late_innings(df)
    yearly_df = analyze_yearly_fatigue_patterns(df)

    create_visualizations(velocity_df, spin_df, trend_results, yearly_df)
    save_results(velocity_df, spin_df, trend_results, comparison, yearly_df)
    print_summary(velocity_df, trend_results, comparison)

    print("\n" + "=" * 60)
    print("  [DONE] Analysis complete!")
    print("=" * 60)
    print(f"  Figures: {FIGURES_DIR}")
    print(f"  Results: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
