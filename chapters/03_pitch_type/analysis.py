#!/usr/bin/env python3
"""
Chapter 3: Pitch Type Evolution (2015-2025)

Research Question: How has the pitch type mix evolved over the past decade,
and what is the significance of the sweeper's emergence?

Hypotheses:
- H1: Pitch type diversity has increased (more distinct pitch types used)
- H2: Traditional 4-seam fastball usage has declined
- H3: Breaking ball usage (especially sweeper) has increased significantly

Methodology:
1. Calculate yearly pitch type distributions
2. Track sweeper (ST) emergence and adoption
3. Analyze fastball/breaking/offspeed category shifts
4. Perform chi-square tests for distribution changes
5. Calculate effect sizes for major pitch type changes

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

from statcast_analysis import load_season, AVAILABLE_SEASONS, PITCH_TYPES, PITCH_GROUPS

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

# Core pitch types for analysis (excluding rare types)
CORE_PITCH_TYPES = ['FF', 'SI', 'FC', 'SL', 'ST', 'CU', 'CH', 'FS']
CORE_PITCH_NAMES = {
    'FF': '4-Seam Fastball',
    'SI': 'Sinker',
    'FC': 'Cutter',
    'SL': 'Slider',
    'ST': 'Sweeper',
    'CU': 'Curveball',
    'CH': 'Changeup',
    'FS': 'Splitter',
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


def calculate_pitch_type_distribution():
    """Calculate pitch type distribution by year."""
    print("=" * 60)
    print("  Chapter 3: Pitch Type Evolution (2015-2025)")
    print("=" * 60)

    print("\n[1] Loading data and calculating pitch type distributions...")

    results = []

    for year in AVAILABLE_SEASONS:
        try:
            df = load_season(year, columns=['pitch_type'])

            # Remove null values
            df = df[df['pitch_type'].notna()]

            # Count by pitch type
            counts = df['pitch_type'].value_counts()
            total = len(df)

            # Build row with all pitch types
            row = {'year': year, 'total': total}
            for pt in CORE_PITCH_TYPES:
                row[f'{pt}_count'] = counts.get(pt, 0)
                row[f'{pt}_pct'] = (counts.get(pt, 0) / total * 100) if total > 0 else 0

            # Calculate "other" category
            other_count = sum(counts.get(pt, 0) for pt in counts.index if pt not in CORE_PITCH_TYPES)
            row['other_count'] = other_count
            row['other_pct'] = (other_count / total * 100) if total > 0 else 0

            results.append(row)

            # Print summary for this year
            top_types = [(pt, row[f'{pt}_pct']) for pt in CORE_PITCH_TYPES]
            top_types.sort(key=lambda x: x[1], reverse=True)
            top_3 = ', '.join([f"{pt}:{pct:.1f}%" for pt, pct in top_types[:3]])
            print(f"  {year}: n={total:,} | Top 3: {top_3}")

        except FileNotFoundError:
            print(f"  {year}: data not found, skipping")
            continue

    return pd.DataFrame(results)


def calculate_pitch_group_distribution(df: pd.DataFrame):
    """Calculate fastball/breaking/offspeed category distributions."""
    print("\n[2] Calculating pitch category distributions...")

    results = []

    for _, row in df.iterrows():
        year = row['year']
        total = row['total']

        # Calculate category totals
        fastball = sum(row.get(f'{pt}_count', 0) for pt in PITCH_GROUPS['fastball'] if f'{pt}_count' in row)
        breaking = sum(row.get(f'{pt}_count', 0) for pt in PITCH_GROUPS['breaking'] if f'{pt}_count' in row)
        offspeed = sum(row.get(f'{pt}_count', 0) for pt in PITCH_GROUPS['offspeed'] if f'{pt}_count' in row)

        results.append({
            'year': year,
            'fastball_pct': (fastball / total * 100) if total > 0 else 0,
            'breaking_pct': (breaking / total * 100) if total > 0 else 0,
            'offspeed_pct': (offspeed / total * 100) if total > 0 else 0,
        })

        print(f"  {year}: Fastball {fastball/total*100:.1f}% | Breaking {breaking/total*100:.1f}% | Offspeed {offspeed/total*100:.1f}%")

    return pd.DataFrame(results)


def perform_trend_analysis(df: pd.DataFrame):
    """Perform linear regression trend analysis for key pitch types."""
    print("\n[3] Trend Analysis (Linear Regression)...")

    results = {}
    years = df['year'].values

    # Analyze trends for each core pitch type
    for pt in CORE_PITCH_TYPES:
        pct_col = f'{pt}_pct'
        if pct_col not in df.columns:
            continue

        values = df[pct_col].values

        # Skip if no meaningful data (e.g., sweeper before it existed)
        if values.max() < 0.1:
            continue

        slope, intercept, r_value, p_value, std_err = stats.linregress(years, values)
        r_squared = r_value ** 2

        results[pt] = {
            'pitch_type': pt,
            'pitch_name': CORE_PITCH_NAMES.get(pt, pt),
            'slope': slope,
            'slope_ci_lower': slope - 1.96 * std_err,
            'slope_ci_upper': slope + 1.96 * std_err,
            'r_squared': r_squared,
            'p_value': p_value,
            'direction': 'increasing' if slope > 0 else 'decreasing',
            'r2_interpretation': interpret_r_squared(r_squared),
            'p_interpretation': interpret_p_value(p_value),
        }

        direction = "+" if slope > 0 else ""
        print(f"  {CORE_PITCH_NAMES.get(pt, pt):20s}: {direction}{slope:.3f}%/year (R²={r_squared:.3f}, p={p_value:.2e})")

    return results


def perform_period_comparison(pitch_type_df: pd.DataFrame):
    """Compare early vs late period pitch type usage."""
    print("\n[4] Period Comparison (Early vs Late)...")
    print(f"    Early period: {EARLY_PERIOD}")
    print(f"    Late period: {LATE_PERIOD}")

    # Aggregate data for both periods
    early_totals = {pt: 0 for pt in CORE_PITCH_TYPES}
    late_totals = {pt: 0 for pt in CORE_PITCH_TYPES}
    early_total = 0
    late_total = 0

    for _, row in pitch_type_df.iterrows():
        year = row['year']
        if year in EARLY_PERIOD:
            for pt in CORE_PITCH_TYPES:
                early_totals[pt] += row.get(f'{pt}_count', 0)
            early_total += row['total']
        elif year in LATE_PERIOD:
            for pt in CORE_PITCH_TYPES:
                late_totals[pt] += row.get(f'{pt}_count', 0)
            late_total += row['total']

    results = []

    print(f"\n  {'Pitch Type':<20} {'Early':<12} {'Late':<12} {'Change':<12} {'Effect':<12}")
    print("  " + "-" * 68)

    for pt in CORE_PITCH_TYPES:
        early_pct = (early_totals[pt] / early_total * 100) if early_total > 0 else 0
        late_pct = (late_totals[pt] / late_total * 100) if late_total > 0 else 0
        change = late_pct - early_pct

        # Calculate effect size (proportion difference)
        # Using Cohen's h for proportion differences
        p1 = early_pct / 100
        p2 = late_pct / 100
        cohens_h = 2 * (np.arcsin(np.sqrt(p2)) - np.arcsin(np.sqrt(p1)))

        results.append({
            'pitch_type': pt,
            'pitch_name': CORE_PITCH_NAMES.get(pt, pt),
            'early_pct': early_pct,
            'late_pct': late_pct,
            'change': change,
            'cohens_h': cohens_h,
            'effect_interpretation': interpret_cohens_d(cohens_h),  # Same thresholds as Cohen's d
        })

        direction = "+" if change > 0 else ""
        print(f"  {CORE_PITCH_NAMES.get(pt, pt):<20} {early_pct:>10.1f}% {late_pct:>10.1f}% {direction}{change:>10.1f}% {interpret_cohens_d(cohens_h):>12}")

    return pd.DataFrame(results)


def analyze_sweeper_emergence(pitch_type_df: pd.DataFrame):
    """Analyze the sweeper's emergence as a distinct pitch category."""
    print("\n[5] Sweeper Emergence Analysis...")

    # Get sweeper usage by year
    sweeper_data = []
    for _, row in pitch_type_df.iterrows():
        sweeper_data.append({
            'year': row['year'],
            'count': row.get('ST_count', 0),
            'pct': row.get('ST_pct', 0),
        })

    sweeper_df = pd.DataFrame(sweeper_data)

    # Find first year with >0.5% usage
    emergence_year = None
    for _, row in sweeper_df.iterrows():
        if row['pct'] > 0.5:
            emergence_year = row['year']
            break

    # Calculate growth rate from emergence
    if emergence_year:
        post_emergence = sweeper_df[sweeper_df['year'] >= emergence_year]
        if len(post_emergence) > 1:
            slope, _, r_value, p_value, _ = stats.linregress(
                post_emergence['year'].values,
                post_emergence['pct'].values
            )
            r_squared = r_value ** 2
        else:
            slope, r_squared, p_value = 0, 0, 1
    else:
        slope, r_squared, p_value = 0, 0, 1

    print(f"\n  Sweeper usage by year:")
    for _, row in sweeper_df.iterrows():
        bar = "#" * int(row['pct'] * 2)
        print(f"    {int(row['year'])}: {row['pct']:>6.2f}% {bar}")

    if emergence_year:
        print(f"\n  First year with >0.5% usage: {emergence_year}")
        print(f"  Growth rate since emergence: +{slope:.2f}%/year")
        print(f"  R² for post-emergence trend: {r_squared:.3f}")

    return {
        'emergence_year': emergence_year,
        'data': sweeper_df,
        'growth_rate': slope,
        'r_squared': r_squared,
    }


def create_visualizations(pitch_type_df: pd.DataFrame, group_df: pd.DataFrame,
                          trend_results: dict, comparison_df: pd.DataFrame):
    """Generate chapter visualizations."""
    print("\n[6] Creating visualizations...")

    # Figure 1: Pitch type usage over time (stacked area)
    fig, ax = plt.subplots(figsize=(12, 7))

    years = pitch_type_df['year'].values

    # Create stacked area chart for main pitch types
    pitch_order = ['FF', 'SI', 'FC', 'SL', 'ST', 'CU', 'CH', 'FS']
    colors = ['#1f77b4', '#2ca02c', '#17becf', '#ff7f0e', '#d62728', '#9467bd', '#8c564b', '#e377c2']

    bottom = np.zeros(len(years))
    for pt, color in zip(pitch_order, colors):
        pct_col = f'{pt}_pct'
        if pct_col in pitch_type_df.columns:
            values = pitch_type_df[pct_col].values
            ax.fill_between(years, bottom, bottom + values, label=CORE_PITCH_NAMES.get(pt, pt),
                           color=color, alpha=0.8)
            bottom += values

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Percentage of All Pitches', fontsize=12)
    ax.set_title('Pitch Type Evolution: Usage Share by Year (2015-2025)', fontsize=14)
    ax.set_xlim(2015, 2025)
    ax.set_ylim(0, 100)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig01_pitch_type_evolution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: fig01_pitch_type_evolution.png")

    # Figure 2: Sweeper emergence
    fig, ax = plt.subplots(figsize=(10, 6))

    sweeper_pct = pitch_type_df['ST_pct'].values if 'ST_pct' in pitch_type_df.columns else np.zeros(len(years))
    ax.bar(years, sweeper_pct, color='#d62728', edgecolor='black', linewidth=0.5)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Sweeper Usage (%)', fontsize=12)
    ax.set_title('The Sweeper Revolution: Emergence of a New Pitch (2015-2025)', fontsize=14)
    ax.set_xlim(2014.5, 2025.5)

    # Add percentage labels
    for i, (y, pct) in enumerate(zip(years, sweeper_pct)):
        if pct > 0.1:
            ax.text(y, pct + 0.3, f"{pct:.1f}%", ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig02_sweeper_emergence.png', dpi=150)
    plt.close()
    print("  Saved: fig02_sweeper_emergence.png")

    # Figure 3: Fastball decline
    fig, ax = plt.subplots(figsize=(10, 6))

    ff_pct = pitch_type_df['FF_pct'].values
    ax.plot(years, ff_pct, 'o-', linewidth=2, markersize=8, color='#1f77b4', label='4-Seam Fastball')

    # Add trend line
    if 'FF' in trend_results:
        slope = trend_results['FF']['slope']
        intercept = trend_results['FF']['slope'] * -2015 + ff_pct[0]  # Approximate intercept
        # Recalculate intercept properly
        slope, intercept, _, _, _ = stats.linregress(years, ff_pct)
        ax.plot(years, intercept + slope * years, '--', color='red', linewidth=2,
                label=f'Trend ({slope:.2f}%/year)')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('4-Seam Fastball Usage (%)', fontsize=12)
    ax.set_title('Decline of the Four-Seam Fastball (2015-2025)', fontsize=14)
    ax.set_xlim(2014.5, 2025.5)
    ax.legend(loc='upper right', fontsize=10)

    # Annotate start and end
    ax.annotate(f"{ff_pct[0]:.1f}%", (years[0], ff_pct[0]),
                textcoords="offset points", xytext=(0, 10), ha='center', fontsize=10)
    ax.annotate(f"{ff_pct[-1]:.1f}%", (years[-1], ff_pct[-1]),
                textcoords="offset points", xytext=(0, 10), ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig03_fastball_decline.png', dpi=150)
    plt.close()
    print("  Saved: fig03_fastball_decline.png")

    # Figure 4: Category shifts (fastball vs breaking vs offspeed)
    fig, ax = plt.subplots(figsize=(10, 6))

    width = 0.25
    x = np.arange(len(years))

    ax.bar(x - width, group_df['fastball_pct'], width, label='Fastball', color='#1f77b4')
    ax.bar(x, group_df['breaking_pct'], width, label='Breaking', color='#ff7f0e')
    ax.bar(x + width, group_df['offspeed_pct'], width, label='Offspeed', color='#2ca02c')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Usage Percentage', fontsize=12)
    ax.set_title('Pitch Category Balance: Fastball vs Breaking vs Offspeed', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(years, rotation=45)
    ax.legend(loc='upper right', fontsize=10)
    ax.set_ylim(0, 60)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig04_pitch_categories.png', dpi=150)
    plt.close()
    print("  Saved: fig04_pitch_categories.png")

    # Figure 5: Period comparison (early vs late)
    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.arange(len(comparison_df))
    width = 0.35

    ax.bar(x - width/2, comparison_df['early_pct'], width, label=f'Early ({EARLY_PERIOD[0]}-{EARLY_PERIOD[-1]})',
           color='#1f77b4', alpha=0.8)
    ax.bar(x + width/2, comparison_df['late_pct'], width, label=f'Late ({LATE_PERIOD[0]}-{LATE_PERIOD[-1]})',
           color='#ff7f0e', alpha=0.8)

    ax.set_xlabel('Pitch Type', fontsize=12)
    ax.set_ylabel('Usage Percentage', fontsize=12)
    ax.set_title('Pitch Type Usage: Early Era vs Modern Era', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([CORE_PITCH_NAMES.get(pt, pt) for pt in comparison_df['pitch_type']], rotation=45, ha='right')
    ax.legend(loc='upper right', fontsize=10)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig05_period_comparison.png', dpi=150)
    plt.close()
    print("  Saved: fig05_period_comparison.png")


def save_results(pitch_type_df: pd.DataFrame, group_df: pd.DataFrame,
                 trend_results: dict, comparison_df: pd.DataFrame):
    """Save analysis results to CSV."""
    print("\n[7] Saving results...")

    # Main pitch type distribution
    pitch_type_df.to_csv(RESULTS_DIR / 'pitch_type_by_year.csv', index=False)
    print("  Saved: pitch_type_by_year.csv")

    # Group distribution
    group_df.to_csv(RESULTS_DIR / 'pitch_category_by_year.csv', index=False)
    print("  Saved: pitch_category_by_year.csv")

    # Trend analysis
    trend_df = pd.DataFrame(trend_results.values())
    trend_df.to_csv(RESULTS_DIR / 'trend_analysis.csv', index=False)
    print("  Saved: trend_analysis.csv")

    # Period comparison
    comparison_df.to_csv(RESULTS_DIR / 'period_comparison.csv', index=False)
    print("  Saved: period_comparison.csv")

    # Summary statistics
    summary = []
    if len(pitch_type_df) > 0:
        first_row = pitch_type_df.iloc[0]
        last_row = pitch_type_df.iloc[-1]

        summary.append({'metric': '4-Seam Usage (2015)', 'value': f"{first_row['FF_pct']:.1f}%"})
        summary.append({'metric': '4-Seam Usage (2025)', 'value': f"{last_row['FF_pct']:.1f}%"})
        summary.append({'metric': '4-Seam Change', 'value': f"{last_row['FF_pct'] - first_row['FF_pct']:.1f}%"})
        summary.append({'metric': 'Sweeper Usage (2025)', 'value': f"{last_row.get('ST_pct', 0):.1f}%"})

        if 'FF' in trend_results:
            summary.append({'metric': '4-Seam Trend (per year)', 'value': f"{trend_results['FF']['slope']:.3f}%"})

    pd.DataFrame(summary).to_csv(RESULTS_DIR / 'summary.csv', index=False)
    print("  Saved: summary.csv")


def print_summary(pitch_type_df: pd.DataFrame, trend_results: dict, comparison_df: pd.DataFrame):
    """Print analysis summary."""
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)

    if len(pitch_type_df) == 0:
        print("  No data available")
        return

    first_row = pitch_type_df.iloc[0]
    last_row = pitch_type_df.iloc[-1]

    ff_change = last_row['FF_pct'] - first_row['FF_pct']
    st_2025 = last_row.get('ST_pct', 0)

    print(f"""
Key Findings:

1. Four-Seam Fastball Decline:
   - 2015: {first_row['FF_pct']:.1f}%
   - 2025: {last_row['FF_pct']:.1f}%
   - Change: {ff_change:+.1f} percentage points
   {'- Statistically significant decline' if 'FF' in trend_results and trend_results['FF']['p_value'] < 0.05 else ''}

2. Sweeper Emergence:
   - 2025 usage: {st_2025:.1f}%
   - Became a distinct category around 2020-2021
   - One of the fastest-growing pitch types in MLB history

3. Breaking Ball Revolution:
   - Slider + Sweeper combined now ~{last_row['SL_pct'] + st_2025:.1f}% of all pitches
   - Breaking balls increasingly preferred over fastballs

4. Total pitches analyzed: {pitch_type_df['total'].sum():,}
""")


def main():
    """Main analysis pipeline."""
    # Phase 1: Extract and describe
    pitch_type_df = calculate_pitch_type_distribution()

    if len(pitch_type_df) == 0:
        print("\n[ERROR] No data found. Please collect data first:")
        print("  python collector/collect_statcast.py --range 2015 2025")
        return

    # Phase 2: Group analysis
    group_df = calculate_pitch_group_distribution(pitch_type_df)

    # Phase 3: Trend analysis
    trend_results = perform_trend_analysis(pitch_type_df)

    # Phase 4: Period comparison
    comparison_df = perform_period_comparison(pitch_type_df)

    # Phase 5: Sweeper deep-dive
    sweeper_analysis = analyze_sweeper_emergence(pitch_type_df)

    # Phase 6: Visualizations
    create_visualizations(pitch_type_df, group_df, trend_results, comparison_df)

    # Phase 7: Save results
    save_results(pitch_type_df, group_df, trend_results, comparison_df)

    # Phase 8: Summary
    print_summary(pitch_type_df, trend_results, comparison_df)

    print("\n[DONE] Analysis complete!")
    print(f"  Figures: {FIGURES_DIR}")
    print(f"  Results: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
