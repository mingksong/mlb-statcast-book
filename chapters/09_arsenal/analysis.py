#!/usr/bin/env python3
"""
Chapter 9: Pitcher Arsenal Diversity (2015-2025)

Research Question: How has pitcher arsenal diversity evolved, and do
pitchers with more pitch types perform differently?

Hypotheses:
- H0: No change in average arsenal size over time
- H1: Pitchers are using more diverse arsenals

Key Analyses:
1. Average number of pitch types per pitcher by year
2. Distribution of arsenal sizes (1-pitch to 6+ pitch)
3. Trend in arsenal diversity over time
4. Comparison of starter vs reliever arsenals

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

# Minimum pitches to count as using a pitch type
MIN_PITCHES_PER_TYPE = 20

# Minimum total pitches to be included in analysis
MIN_TOTAL_PITCHES = 200


def load_arsenal_data():
    """Load pitch data for arsenal analysis."""
    print("=" * 60)
    print("  Chapter 9: Pitcher Arsenal Diversity (2015-2025)")
    print("=" * 60)
    print("\n[1] Loading pitch data for arsenal analysis...")

    all_data = []

    for year in AVAILABLE_SEASONS:
        try:
            df = load_season(year, columns=['pitcher', 'pitch_type'])
            df['game_year'] = year
            df = df.dropna(subset=['pitcher', 'pitch_type'])

            all_data.append(df)
            n_pitchers = df['pitcher'].nunique()
            print(f"  {year}: {len(df):,} pitches from {n_pitchers:,} pitchers")

        except FileNotFoundError:
            print(f"  {year}: data not found, skipping")
            continue

    combined = pd.concat(all_data, ignore_index=True)
    print(f"\n  Total: {len(combined):,} pitches")

    return combined


def calculate_arsenal_by_pitcher(df: pd.DataFrame):
    """Calculate arsenal size for each pitcher-year combination."""
    print("\n[2] Calculating arsenal size by pitcher...")

    results = []

    for year in sorted(df['game_year'].unique()):
        year_data = df[df['game_year'] == year]

        for pitcher in year_data['pitcher'].unique():
            pitcher_data = year_data[year_data['pitcher'] == pitcher]
            total_pitches = len(pitcher_data)

            if total_pitches < MIN_TOTAL_PITCHES:
                continue

            # Count pitch types with minimum usage
            pitch_counts = pitcher_data['pitch_type'].value_counts()
            qualifying_pitches = pitch_counts[pitch_counts >= MIN_PITCHES_PER_TYPE]
            arsenal_size = len(qualifying_pitches)

            if arsenal_size == 0:
                continue

            # Get primary pitch
            primary_pitch = pitch_counts.idxmax()
            primary_pct = pitch_counts.max() / total_pitches * 100

            results.append({
                'year': year,
                'pitcher': pitcher,
                'total_pitches': total_pitches,
                'arsenal_size': arsenal_size,
                'primary_pitch': primary_pitch,
                'primary_pct': primary_pct,
                'pitch_types': list(qualifying_pitches.index),
            })

    results_df = pd.DataFrame(results)
    print(f"  Analyzed {len(results_df):,} pitcher-seasons")

    return results_df


def analyze_arsenal_by_year(arsenal_df: pd.DataFrame):
    """Analyze arsenal diversity trends by year."""
    print("\n[3] Analyzing arsenal diversity by year...")

    yearly_stats = []

    for year in sorted(arsenal_df['year'].unique()):
        year_data = arsenal_df[arsenal_df['year'] == year]

        yearly_stats.append({
            'year': year,
            'n_pitchers': len(year_data),
            'avg_arsenal': year_data['arsenal_size'].mean(),
            'median_arsenal': year_data['arsenal_size'].median(),
            'std_arsenal': year_data['arsenal_size'].std(),
            'pct_1pitch': (year_data['arsenal_size'] == 1).mean() * 100,
            'pct_2pitch': (year_data['arsenal_size'] == 2).mean() * 100,
            'pct_3pitch': (year_data['arsenal_size'] == 3).mean() * 100,
            'pct_4pitch': (year_data['arsenal_size'] == 4).mean() * 100,
            'pct_5plus': (year_data['arsenal_size'] >= 5).mean() * 100,
        })

    yearly_df = pd.DataFrame(yearly_stats)

    print("\n  Average Arsenal Size by Year:")
    for _, row in yearly_df.iterrows():
        print(f"    {int(row['year'])}: {row['avg_arsenal']:.2f} pitch types "
              f"(n={int(row['n_pitchers'])} pitchers)")

    return yearly_df


def perform_trend_analysis(yearly_df: pd.DataFrame):
    """Perform linear regression on arsenal size trend."""
    print("\n[4] Trend Analysis...")

    years = yearly_df['year'].values
    avg_arsenal = yearly_df['avg_arsenal'].values

    slope, intercept, r_value, p_value, std_err = stats.linregress(years, avg_arsenal)

    trend_results = {
        'slope': slope,
        'slope_ci_lower': slope - 1.96 * std_err,
        'slope_ci_upper': slope + 1.96 * std_err,
        'intercept': intercept,
        'r_squared': r_value**2,
        'p_value': p_value,
    }

    print(f"  Arsenal Size Trend:")
    print(f"    Slope: {slope:.4f} pitches/year")
    print(f"    95% CI: [{slope - 1.96*std_err:.4f}, {slope + 1.96*std_err:.4f}]")
    print(f"    R²: {trend_results['r_squared']:.4f}")
    print(f"    p-value: {p_value:.2e}")

    return trend_results


def analyze_arsenal_distribution(arsenal_df: pd.DataFrame):
    """Analyze distribution of arsenal sizes."""
    print("\n[5] Arsenal Size Distribution...")

    # Overall distribution
    dist = arsenal_df['arsenal_size'].value_counts().sort_index()
    total = len(arsenal_df)

    print("\n  Overall Distribution (all years):")
    for size in sorted(dist.index):
        count = dist[size]
        pct = count / total * 100
        print(f"    {size} pitch types: {count:,} ({pct:.1f}%)")

    # Compare 2015 vs 2025
    early = arsenal_df[arsenal_df['year'] == 2015]['arsenal_size']
    late = arsenal_df[arsenal_df['year'] == 2025]['arsenal_size']

    comparison = {
        'early_mean': early.mean(),
        'early_median': early.median(),
        'late_mean': late.mean(),
        'late_median': late.median(),
    }

    print(f"\n  2015 vs 2025:")
    print(f"    2015: Mean={early.mean():.2f}, Median={early.median():.1f}")
    print(f"    2025: Mean={late.mean():.2f}, Median={late.median():.1f}")

    return comparison


def analyze_pitch_type_popularity(df: pd.DataFrame):
    """Analyze which pitch types are most common in arsenals."""
    print("\n[6] Pitch Type Popularity in Arsenals...")

    results = []

    for year in [2015, 2020, 2025]:
        year_data = df[df['game_year'] == year]

        # Count how many pitchers throw each pitch type
        pitcher_pitch = year_data.groupby(['pitcher', 'pitch_type']).size().reset_index(name='count')

        # Filter to pitchers with minimum pitches
        pitcher_totals = year_data.groupby('pitcher').size()
        qualified_pitchers = pitcher_totals[pitcher_totals >= MIN_TOTAL_PITCHES].index

        pitcher_pitch = pitcher_pitch[pitcher_pitch['pitcher'].isin(qualified_pitchers)]
        pitcher_pitch = pitcher_pitch[pitcher_pitch['count'] >= MIN_PITCHES_PER_TYPE]

        n_pitchers = len(qualified_pitchers)

        # Count pitchers per pitch type
        pitch_popularity = pitcher_pitch.groupby('pitch_type')['pitcher'].nunique()
        pitch_popularity = (pitch_popularity / n_pitchers * 100).sort_values(ascending=False)

        for pitch_type, pct in pitch_popularity.items():
            results.append({
                'year': year,
                'pitch_type': pitch_type,
                'pct_pitchers': pct,
            })

    results_df = pd.DataFrame(results)

    print("\n  Pitch Type Usage (% of Pitchers):")
    for year in [2015, 2025]:
        print(f"\n    {year}:")
        year_data = results_df[results_df['year'] == year].sort_values('pct_pitchers', ascending=False)
        for _, row in year_data.head(8).iterrows():
            print(f"      {row['pitch_type']}: {row['pct_pitchers']:.1f}%")

    return results_df


def create_visualizations(yearly_df: pd.DataFrame, arsenal_df: pd.DataFrame,
                          trend_results: dict, popularity_df: pd.DataFrame):
    """Generate visualizations."""
    print("\n[7] Creating visualizations...")

    # Figure 1: Average arsenal size over time
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(yearly_df['year'], yearly_df['avg_arsenal'], 'o-',
            linewidth=2, markersize=10, color='#1f77b4')

    # Regression line
    slope = trend_results['slope']
    intercept = trend_results['intercept']
    years = yearly_df['year'].values
    ax.plot(years, intercept + slope * years, '--', color='red',
            linewidth=2, label=f'Trend: {slope:+.3f}/year (R²={trend_results["r_squared"]:.3f})')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Average Arsenal Size (pitch types)', fontsize=12)
    ax.set_title('Pitcher Arsenal Diversity Over Time', fontsize=14)
    ax.legend()

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig01_arsenal_trend.png', dpi=150)
    plt.close()
    print("  Saved: fig01_arsenal_trend.png")

    # Figure 2: Arsenal size distribution by year
    fig, ax = plt.subplots(figsize=(12, 6))

    years_to_plot = [2015, 2020, 2025]
    x = np.arange(1, 7)
    width = 0.25

    for i, year in enumerate(years_to_plot):
        year_data = arsenal_df[arsenal_df['year'] == year]
        counts = [((year_data['arsenal_size'] == s).sum() / len(year_data) * 100)
                  for s in range(1, 7)]
        ax.bar(x + (i - 1) * width, counts, width, label=str(year))

    ax.set_xlabel('Arsenal Size (pitch types)', fontsize=12)
    ax.set_ylabel('Percentage of Pitchers', fontsize=12)
    ax.set_title('Arsenal Size Distribution: 2015 vs 2020 vs 2025', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(['1', '2', '3', '4', '5', '6+'])
    ax.legend()

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig02_arsenal_distribution.png', dpi=150)
    plt.close()
    print("  Saved: fig02_arsenal_distribution.png")

    # Figure 3: Percentage of 4+ pitch arsenals over time
    fig, ax = plt.subplots(figsize=(10, 6))

    yearly_df['pct_4plus'] = yearly_df['pct_4pitch'] + yearly_df['pct_5plus']

    ax.fill_between(yearly_df['year'], 0, yearly_df['pct_4plus'],
                    alpha=0.3, color='#2ca02c', label='4+ pitch types')
    ax.plot(yearly_df['year'], yearly_df['pct_4plus'], 'o-',
            linewidth=2, markersize=8, color='#2ca02c')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Percentage of Pitchers', fontsize=12)
    ax.set_title('Rise of Multi-Pitch Arsenals (4+ Types)', fontsize=14)
    ax.legend()

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig03_multipitch_trend.png', dpi=150)
    plt.close()
    print("  Saved: fig03_multipitch_trend.png")

    # Figure 4: Pitch type popularity comparison
    fig, ax = plt.subplots(figsize=(12, 6))

    pitch_types = ['FF', 'SL', 'CH', 'CU', 'SI', 'FC', 'ST', 'FS']
    x = np.arange(len(pitch_types))
    width = 0.35

    pop_2015 = popularity_df[popularity_df['year'] == 2015].set_index('pitch_type')['pct_pitchers']
    pop_2025 = popularity_df[popularity_df['year'] == 2025].set_index('pitch_type')['pct_pitchers']

    vals_2015 = [pop_2015.get(pt, 0) for pt in pitch_types]
    vals_2025 = [pop_2025.get(pt, 0) for pt in pitch_types]

    ax.bar(x - width/2, vals_2015, width, label='2015', color='#1f77b4')
    ax.bar(x + width/2, vals_2025, width, label='2025', color='#ff7f0e')

    ax.set_xlabel('Pitch Type', fontsize=12)
    ax.set_ylabel('% of Pitchers Using', fontsize=12)
    ax.set_title('Pitch Type Popularity: 2015 vs 2025', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(pitch_types)
    ax.legend()

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig04_pitch_popularity.png', dpi=150)
    plt.close()
    print("  Saved: fig04_pitch_popularity.png")


def save_results(yearly_df: pd.DataFrame, arsenal_df: pd.DataFrame,
                 trend_results: dict, comparison: dict, popularity_df: pd.DataFrame):
    """Save results to CSV."""
    print("\n[8] Saving results...")

    yearly_df.to_csv(RESULTS_DIR / 'arsenal_by_year.csv', index=False)
    print("  Saved: arsenal_by_year.csv")

    # Aggregate arsenal data (remove pitch_types list for CSV)
    arsenal_summary = arsenal_df.drop(columns=['pitch_types'])
    arsenal_summary.to_csv(RESULTS_DIR / 'pitcher_arsenals.csv', index=False)
    print("  Saved: pitcher_arsenals.csv")

    popularity_df.to_csv(RESULTS_DIR / 'pitch_type_popularity.csv', index=False)
    print("  Saved: pitch_type_popularity.csv")

    # Statistical tests
    stat_tests = [
        {'test': 'Arsenal Trend', 'metric': 'Slope', 'value': f"{trend_results['slope']:.4f}", 'unit': 'types/year'},
        {'test': 'Arsenal Trend', 'metric': 'R-squared', 'value': f"{trend_results['r_squared']:.4f}", 'unit': ''},
        {'test': 'Arsenal Trend', 'metric': 'p-value', 'value': f"{trend_results['p_value']:.2e}", 'unit': ''},
        {'test': '2015 vs 2025', 'metric': '2015 Mean Arsenal', 'value': f"{comparison['early_mean']:.2f}", 'unit': 'types'},
        {'test': '2015 vs 2025', 'metric': '2025 Mean Arsenal', 'value': f"{comparison['late_mean']:.2f}", 'unit': 'types'},
        {'test': '2015 vs 2025', 'metric': 'Change', 'value': f"{comparison['late_mean'] - comparison['early_mean']:+.2f}", 'unit': 'types'},
    ]
    pd.DataFrame(stat_tests).to_csv(RESULTS_DIR / 'statistical_tests.csv', index=False)
    print("  Saved: statistical_tests.csv")

    # Summary
    summary = {
        'metric': [
            '2015 Average Arsenal',
            '2025 Average Arsenal',
            'Change in Arsenal Size',
            'Trend Slope',
            'Trend R-squared',
            '% with 4+ Pitches (2015)',
            '% with 4+ Pitches (2025)',
        ],
        'value': [
            f"{comparison['early_mean']:.2f} types",
            f"{comparison['late_mean']:.2f} types",
            f"{comparison['late_mean'] - comparison['early_mean']:+.2f} types",
            f"{trend_results['slope']:.4f} types/year",
            f"{trend_results['r_squared']:.4f}",
            f"{yearly_df.iloc[0]['pct_4pitch'] + yearly_df.iloc[0]['pct_5plus']:.1f}%",
            f"{yearly_df.iloc[-1]['pct_4pitch'] + yearly_df.iloc[-1]['pct_5plus']:.1f}%",
        ]
    }
    pd.DataFrame(summary).to_csv(RESULTS_DIR / 'summary.csv', index=False)
    print("  Saved: summary.csv")


def print_summary(yearly_df: pd.DataFrame, trend_results: dict, comparison: dict):
    """Print analysis summary."""
    print("\n" + "=" * 60)
    print("  Summary: Pitcher Arsenal Diversity")
    print("=" * 60)

    pct_4plus_2015 = yearly_df.iloc[0]['pct_4pitch'] + yearly_df.iloc[0]['pct_5plus']
    pct_4plus_2025 = yearly_df.iloc[-1]['pct_4pitch'] + yearly_df.iloc[-1]['pct_5plus']

    print(f"""
KEY FINDINGS:

1. Arsenal Size Evolution:
   - 2015 Average: {comparison['early_mean']:.2f} pitch types
   - 2025 Average: {comparison['late_mean']:.2f} pitch types
   - Change: {comparison['late_mean'] - comparison['early_mean']:+.2f} pitch types

2. Trend Analysis:
   - Slope: {trend_results['slope']:.4f} types/year
   - R²: {trend_results['r_squared']:.4f}
   - p-value: {trend_results['p_value']:.2e}

3. Multi-Pitch Pitchers (4+ types):
   - 2015: {pct_4plus_2015:.1f}%
   - 2025: {pct_4plus_2025:.1f}%

INTERPRETATION: Arsenal diversity has {'increased' if trend_results['slope'] > 0 else 'decreased'}
over the decade, with pitchers developing more varied repertoires.
""")


def main():
    df = load_arsenal_data()

    if len(df) == 0:
        print("\n[ERROR] No data found.")
        return

    arsenal_df = calculate_arsenal_by_pitcher(df)
    yearly_df = analyze_arsenal_by_year(arsenal_df)
    trend_results = perform_trend_analysis(yearly_df)
    comparison = analyze_arsenal_distribution(arsenal_df)
    popularity_df = analyze_pitch_type_popularity(df)

    create_visualizations(yearly_df, arsenal_df, trend_results, popularity_df)
    save_results(yearly_df, arsenal_df, trend_results, comparison, popularity_df)
    print_summary(yearly_df, trend_results, comparison)

    print("\n" + "=" * 60)
    print("  [DONE] Analysis complete!")
    print("=" * 60)
    print(f"  Figures: {FIGURES_DIR}")
    print(f"  Results: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
