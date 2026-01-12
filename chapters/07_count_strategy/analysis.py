#!/usr/bin/env python3
"""
Chapter 7: Count-Based Pitch Selection (2015-2025)

Research Question: How does pitch selection change based on the count,
and have these strategies evolved over time?

Hypotheses:
- H0: Pitch selection is independent of count
- H1: Pitchers adjust pitch mix based on count situation

Key Analyses:
1. Fastball% by count (pitcher's counts vs hitter's counts)
2. Breaking ball usage in two-strike counts
3. First pitch strategies (0-0 count)
4. Full count (3-2) pitch selection
5. Evolution of count-based strategy over time

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

# Count classifications
PITCHER_COUNTS = [(0, 1), (0, 2), (1, 2)]  # Ahead in count
HITTER_COUNTS = [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1)]  # Behind in count
EVEN_COUNTS = [(0, 0), (1, 1), (2, 2), (3, 2)]  # Even/neutral

# Pitch categories
FASTBALLS = ['FF', 'SI', 'FC']
BREAKING = ['SL', 'CU', 'ST', 'KC', 'CS']
OFFSPEED = ['CH', 'FS']


def load_count_data():
    """Load pitch data with count information."""
    print("=" * 60)
    print("  Chapter 7: Count-Based Pitch Selection (2015-2025)")
    print("=" * 60)
    print("\n[1] Loading pitch data with count information...")

    all_data = []

    for year in AVAILABLE_SEASONS:
        try:
            df = load_season(year, columns=[
                'pitch_type', 'balls', 'strikes', 'release_speed'
            ])
            df['game_year'] = year

            # Ensure numeric
            df['balls'] = pd.to_numeric(df['balls'], errors='coerce')
            df['strikes'] = pd.to_numeric(df['strikes'], errors='coerce')

            # Filter valid data
            df = df.dropna(subset=['pitch_type', 'balls', 'strikes'])
            df = df[(df['balls'] >= 0) & (df['balls'] <= 3)]
            df = df[(df['strikes'] >= 0) & (df['strikes'] <= 2)]

            all_data.append(df)
            print(f"  {year}: {len(df):,} pitches")

        except FileNotFoundError:
            print(f"  {year}: data not found, skipping")
            continue

    combined = pd.concat(all_data, ignore_index=True)
    print(f"\n  Total pitches: {len(combined):,}")

    return combined


def categorize_pitch(pitch_type):
    """Categorize pitch into Fastball, Breaking, or Offspeed."""
    if pitch_type in FASTBALLS:
        return 'Fastball'
    elif pitch_type in BREAKING:
        return 'Breaking'
    elif pitch_type in OFFSPEED:
        return 'Offspeed'
    else:
        return 'Other'


def analyze_pitch_mix_by_count(df: pd.DataFrame):
    """Analyze pitch selection patterns by count."""
    print("\n[2] Analyzing pitch mix by count...")

    df['pitch_category'] = df['pitch_type'].apply(categorize_pitch)
    df['count'] = df['balls'].astype(int).astype(str) + '-' + df['strikes'].astype(int).astype(str)

    results = []

    # All counts
    all_counts = [(b, s) for b in range(4) for s in range(3)]

    for balls, strikes in all_counts:
        count_data = df[(df['balls'] == balls) & (df['strikes'] == strikes)]
        total = len(count_data)

        if total < 1000:
            continue

        fastball_pct = (count_data['pitch_category'] == 'Fastball').mean() * 100
        breaking_pct = (count_data['pitch_category'] == 'Breaking').mean() * 100
        offspeed_pct = (count_data['pitch_category'] == 'Offspeed').mean() * 100

        # Classify count type
        if (balls, strikes) in PITCHER_COUNTS:
            count_type = 'Pitcher'
        elif (balls, strikes) in HITTER_COUNTS:
            count_type = 'Hitter'
        else:
            count_type = 'Even'

        results.append({
            'balls': balls,
            'strikes': strikes,
            'count': f"{balls}-{strikes}",
            'count_type': count_type,
            'total': total,
            'fastball_pct': fastball_pct,
            'breaking_pct': breaking_pct,
            'offspeed_pct': offspeed_pct,
        })

    results_df = pd.DataFrame(results)

    # Print summary
    print("\n  Pitch Mix by Count:")
    print("  " + "-" * 50)
    for _, row in results_df.sort_values(['balls', 'strikes']).iterrows():
        print(f"    {row['count']} ({row['count_type']:7}): FB={row['fastball_pct']:.1f}%, "
              f"BR={row['breaking_pct']:.1f}%, OS={row['offspeed_pct']:.1f}%")

    return results_df


def analyze_count_type_comparison(df: pd.DataFrame):
    """Compare pitch selection between pitcher's and hitter's counts."""
    print("\n[3] Comparing pitcher's vs hitter's counts...")

    df['pitch_category'] = df['pitch_type'].apply(categorize_pitch)

    # Pitcher's counts
    pitcher_mask = df.apply(lambda x: (int(x['balls']), int(x['strikes'])) in PITCHER_COUNTS, axis=1)
    pitcher_data = df[pitcher_mask]

    # Hitter's counts
    hitter_mask = df.apply(lambda x: (int(x['balls']), int(x['strikes'])) in HITTER_COUNTS, axis=1)
    hitter_data = df[hitter_mask]

    comparison = {
        'pitcher_count': {
            'n': len(pitcher_data),
            'fastball_pct': (pitcher_data['pitch_category'] == 'Fastball').mean() * 100,
            'breaking_pct': (pitcher_data['pitch_category'] == 'Breaking').mean() * 100,
            'offspeed_pct': (pitcher_data['pitch_category'] == 'Offspeed').mean() * 100,
        },
        'hitter_count': {
            'n': len(hitter_data),
            'fastball_pct': (hitter_data['pitch_category'] == 'Fastball').mean() * 100,
            'breaking_pct': (hitter_data['pitch_category'] == 'Breaking').mean() * 100,
            'offspeed_pct': (hitter_data['pitch_category'] == 'Offspeed').mean() * 100,
        }
    }

    # Chi-square test for independence
    pitcher_fb = (pitcher_data['pitch_category'] == 'Fastball').sum()
    pitcher_other = len(pitcher_data) - pitcher_fb
    hitter_fb = (hitter_data['pitch_category'] == 'Fastball').sum()
    hitter_other = len(hitter_data) - hitter_fb

    contingency = [[pitcher_fb, pitcher_other], [hitter_fb, hitter_other]]
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

    # Effect size (Cramer's V)
    n = pitcher_fb + pitcher_other + hitter_fb + hitter_other
    cramers_v = np.sqrt(chi2 / n)

    comparison['chi2_test'] = {
        'chi2': chi2,
        'p_value': p_value,
        'cramers_v': cramers_v,
    }

    print(f"\n  Pitcher's Counts (0-1, 0-2, 1-2):")
    print(f"    Fastball: {comparison['pitcher_count']['fastball_pct']:.1f}%")
    print(f"    Breaking: {comparison['pitcher_count']['breaking_pct']:.1f}%")
    print(f"    n = {comparison['pitcher_count']['n']:,}")

    print(f"\n  Hitter's Counts (1-0, 2-0, 2-1, 3-0, 3-1):")
    print(f"    Fastball: {comparison['hitter_count']['fastball_pct']:.1f}%")
    print(f"    Breaking: {comparison['hitter_count']['breaking_pct']:.1f}%")
    print(f"    n = {comparison['hitter_count']['n']:,}")

    fb_diff = comparison['hitter_count']['fastball_pct'] - comparison['pitcher_count']['fastball_pct']
    print(f"\n  Fastball Difference: {fb_diff:+.1f}% (hitter - pitcher counts)")
    print(f"  Chi-square: {chi2:.2f}, p-value: {p_value:.2e}")
    print(f"  Cramer's V: {cramers_v:.4f}")

    return comparison


def analyze_two_strike_strategy(df: pd.DataFrame):
    """Analyze pitch selection with two strikes."""
    print("\n[4] Analyzing two-strike strategy...")

    df['pitch_category'] = df['pitch_type'].apply(categorize_pitch)

    two_strike = df[df['strikes'] == 2]
    other = df[df['strikes'] < 2]

    results = {
        'two_strike': {
            'n': len(two_strike),
            'fastball_pct': (two_strike['pitch_category'] == 'Fastball').mean() * 100,
            'breaking_pct': (two_strike['pitch_category'] == 'Breaking').mean() * 100,
            'offspeed_pct': (two_strike['pitch_category'] == 'Offspeed').mean() * 100,
        },
        'other': {
            'n': len(other),
            'fastball_pct': (other['pitch_category'] == 'Fastball').mean() * 100,
            'breaking_pct': (other['pitch_category'] == 'Breaking').mean() * 100,
            'offspeed_pct': (other['pitch_category'] == 'Offspeed').mean() * 100,
        }
    }

    print(f"\n  Two-Strike Counts (X-2):")
    print(f"    Fastball: {results['two_strike']['fastball_pct']:.1f}%")
    print(f"    Breaking: {results['two_strike']['breaking_pct']:.1f}%")
    print(f"    Offspeed: {results['two_strike']['offspeed_pct']:.1f}%")

    print(f"\n  Other Counts (X-0, X-1):")
    print(f"    Fastball: {results['other']['fastball_pct']:.1f}%")
    print(f"    Breaking: {results['other']['breaking_pct']:.1f}%")

    breaking_increase = results['two_strike']['breaking_pct'] - results['other']['breaking_pct']
    print(f"\n  Breaking Ball Increase with 2 Strikes: {breaking_increase:+.1f}%")

    return results


def analyze_yearly_trends(df: pd.DataFrame):
    """Analyze how count-based strategy has evolved."""
    print("\n[5] Analyzing yearly trends...")

    df['pitch_category'] = df['pitch_type'].apply(categorize_pitch)

    # 0-0 count (first pitch) fastball rate by year
    first_pitch = df[(df['balls'] == 0) & (df['strikes'] == 0)]
    yearly_first_pitch = first_pitch.groupby('game_year').apply(
        lambda x: (x['pitch_category'] == 'Fastball').mean() * 100
    ).reset_index(name='first_pitch_fb_pct')

    # Two-strike breaking ball rate by year
    two_strike = df[df['strikes'] == 2]
    yearly_two_strike = two_strike.groupby('game_year').apply(
        lambda x: (x['pitch_category'] == 'Breaking').mean() * 100
    ).reset_index(name='two_strike_breaking_pct')

    # 3-0 fastball rate
    three_oh = df[(df['balls'] == 3) & (df['strikes'] == 0)]
    yearly_three_oh = three_oh.groupby('game_year').apply(
        lambda x: (x['pitch_category'] == 'Fastball').mean() * 100
    ).reset_index(name='three_oh_fb_pct')

    trends = yearly_first_pitch.merge(yearly_two_strike, on='game_year')
    trends = trends.merge(yearly_three_oh, on='game_year')

    # Trend analysis for first pitch FB%
    years = trends['game_year'].values
    fp_fb = trends['first_pitch_fb_pct'].values

    slope, intercept, r_value, p_value, std_err = stats.linregress(years, fp_fb)

    trends_results = {
        'data': trends,
        'first_pitch_trend': {
            'slope': slope,
            'r_squared': r_value**2,
            'p_value': p_value,
        }
    }

    print("\n  First Pitch (0-0) Fastball %:")
    print(f"    2015: {trends.iloc[0]['first_pitch_fb_pct']:.1f}%")
    print(f"    2025: {trends.iloc[-1]['first_pitch_fb_pct']:.1f}%")
    print(f"    Trend: {slope:.2f}%/year (R²={r_value**2:.3f}, p={p_value:.3f})")

    print("\n  Two-Strike Breaking Ball %:")
    print(f"    2015: {trends.iloc[0]['two_strike_breaking_pct']:.1f}%")
    print(f"    2025: {trends.iloc[-1]['two_strike_breaking_pct']:.1f}%")

    print("\n  3-0 Count Fastball %:")
    print(f"    2015: {trends.iloc[0]['three_oh_fb_pct']:.1f}%")
    print(f"    2025: {trends.iloc[-1]['three_oh_fb_pct']:.1f}%")

    return trends_results


def create_visualizations(count_df: pd.DataFrame, comparison: dict,
                          two_strike: dict, trends: dict):
    """Generate visualizations."""
    print("\n[6] Creating visualizations...")

    # Figure 1: Pitch mix heatmap by count
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create pivot for fastball %
    pivot = count_df.pivot(index='strikes', columns='balls', values='fastball_pct')

    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlBu_r', ax=ax,
                cbar_kws={'label': 'Fastball %'}, vmin=45, vmax=75)
    ax.set_xlabel('Balls', fontsize=12)
    ax.set_ylabel('Strikes', fontsize=12)
    ax.set_title('Fastball Usage by Count', fontsize=14)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig01_fastball_by_count.png', dpi=150)
    plt.close()
    print("  Saved: fig01_fastball_by_count.png")

    # Figure 2: Pitcher's vs Hitter's counts comparison
    fig, ax = plt.subplots(figsize=(10, 6))

    categories = ['Fastball', 'Breaking', 'Offspeed']
    pitcher_vals = [comparison['pitcher_count']['fastball_pct'],
                    comparison['pitcher_count']['breaking_pct'],
                    comparison['pitcher_count']['offspeed_pct']]
    hitter_vals = [comparison['hitter_count']['fastball_pct'],
                   comparison['hitter_count']['breaking_pct'],
                   comparison['hitter_count']['offspeed_pct']]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax.bar(x - width/2, pitcher_vals, width, label="Pitcher's Count", color='#1f77b4')
    bars2 = ax.bar(x + width/2, hitter_vals, width, label="Hitter's Count", color='#ff7f0e')

    ax.set_ylabel('Usage (%)', fontsize=12)
    ax.set_title("Pitch Selection: Pitcher's vs Hitter's Counts", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()

    # Add value labels
    for bar in bars1 + bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig02_pitcher_vs_hitter_counts.png', dpi=150)
    plt.close()
    print("  Saved: fig02_pitcher_vs_hitter_counts.png")

    # Figure 3: Two-strike strategy
    fig, ax = plt.subplots(figsize=(10, 6))

    categories = ['Fastball', 'Breaking', 'Offspeed']
    two_strike_vals = [two_strike['two_strike']['fastball_pct'],
                       two_strike['two_strike']['breaking_pct'],
                       two_strike['two_strike']['offspeed_pct']]
    other_vals = [two_strike['other']['fastball_pct'],
                  two_strike['other']['breaking_pct'],
                  two_strike['other']['offspeed_pct']]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax.bar(x - width/2, other_vals, width, label='0-1 Strikes', color='#2ca02c')
    bars2 = ax.bar(x + width/2, two_strike_vals, width, label='2 Strikes', color='#d62728')

    ax.set_ylabel('Usage (%)', fontsize=12)
    ax.set_title('Two-Strike Pitch Selection Change', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()

    for bar in bars1 + bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig03_two_strike_strategy.png', dpi=150)
    plt.close()
    print("  Saved: fig03_two_strike_strategy.png")

    # Figure 4: Yearly trends
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    trend_data = trends['data']

    # First pitch FB%
    ax1 = axes[0]
    ax1.plot(trend_data['game_year'], trend_data['first_pitch_fb_pct'], 'o-',
             linewidth=2, markersize=8, color='#1f77b4')
    ax1.set_xlabel('Year', fontsize=11)
    ax1.set_ylabel('Fastball %', fontsize=11)
    ax1.set_title('First Pitch (0-0) Fastball %', fontsize=12)

    # Two-strike breaking%
    ax2 = axes[1]
    ax2.plot(trend_data['game_year'], trend_data['two_strike_breaking_pct'], 'o-',
             linewidth=2, markersize=8, color='#ff7f0e')
    ax2.set_xlabel('Year', fontsize=11)
    ax2.set_ylabel('Breaking Ball %', fontsize=11)
    ax2.set_title('Two-Strike Breaking Ball %', fontsize=12)

    # 3-0 FB%
    ax3 = axes[2]
    ax3.plot(trend_data['game_year'], trend_data['three_oh_fb_pct'], 'o-',
             linewidth=2, markersize=8, color='#2ca02c')
    ax3.set_xlabel('Year', fontsize=11)
    ax3.set_ylabel('Fastball %', fontsize=11)
    ax3.set_title('3-0 Count Fastball %', fontsize=12)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig04_yearly_trends.png', dpi=150)
    plt.close()
    print("  Saved: fig04_yearly_trends.png")

    # Figure 5: Count progression visualization
    fig, ax = plt.subplots(figsize=(12, 8))

    # Sort by count type and then by fastball%
    sorted_df = count_df.sort_values('fastball_pct', ascending=True)

    colors = {'Pitcher': '#1f77b4', 'Hitter': '#ff7f0e', 'Even': '#2ca02c'}
    bar_colors = [colors[ct] for ct in sorted_df['count_type']]

    bars = ax.barh(sorted_df['count'], sorted_df['fastball_pct'], color=bar_colors)

    ax.set_xlabel('Fastball %', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Fastball Usage Ranked by Count', fontsize=14)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=colors['Pitcher'], label="Pitcher's Count"),
                       Patch(facecolor=colors['Hitter'], label="Hitter's Count"),
                       Patch(facecolor=colors['Even'], label='Even Count')]
    ax.legend(handles=legend_elements, loc='lower right')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig05_count_ranking.png', dpi=150)
    plt.close()
    print("  Saved: fig05_count_ranking.png")


def save_results(count_df: pd.DataFrame, comparison: dict,
                 two_strike: dict, trends: dict):
    """Save results to CSV."""
    print("\n[7] Saving results...")

    # Count-by-count results
    count_df.to_csv(RESULTS_DIR / 'pitch_mix_by_count.csv', index=False)
    print("  Saved: pitch_mix_by_count.csv")

    # Yearly trends
    trends['data'].to_csv(RESULTS_DIR / 'yearly_trends.csv', index=False)
    print("  Saved: yearly_trends.csv")

    # Statistical tests
    stat_tests = [
        {'test': 'Pitcher vs Hitter Count', 'metric': 'Pitcher FB%',
         'value': f"{comparison['pitcher_count']['fastball_pct']:.1f}", 'unit': '%'},
        {'test': 'Pitcher vs Hitter Count', 'metric': 'Hitter FB%',
         'value': f"{comparison['hitter_count']['fastball_pct']:.1f}", 'unit': '%'},
        {'test': 'Pitcher vs Hitter Count', 'metric': 'Difference',
         'value': f"{comparison['hitter_count']['fastball_pct'] - comparison['pitcher_count']['fastball_pct']:+.1f}", 'unit': '%'},
        {'test': 'Pitcher vs Hitter Count', 'metric': 'Chi-square',
         'value': f"{comparison['chi2_test']['chi2']:.2f}", 'unit': ''},
        {'test': 'Pitcher vs Hitter Count', 'metric': 'p-value',
         'value': f"{comparison['chi2_test']['p_value']:.2e}", 'unit': ''},
        {'test': 'Pitcher vs Hitter Count', 'metric': "Cramer's V",
         'value': f"{comparison['chi2_test']['cramers_v']:.4f}", 'unit': ''},
        {'test': 'Two-Strike Strategy', 'metric': 'Breaking% (2 strikes)',
         'value': f"{two_strike['two_strike']['breaking_pct']:.1f}", 'unit': '%'},
        {'test': 'Two-Strike Strategy', 'metric': 'Breaking% (0-1 strikes)',
         'value': f"{two_strike['other']['breaking_pct']:.1f}", 'unit': '%'},
        {'test': 'Two-Strike Strategy', 'metric': 'Breaking% Increase',
         'value': f"{two_strike['two_strike']['breaking_pct'] - two_strike['other']['breaking_pct']:+.1f}", 'unit': '%'},
        {'test': 'First Pitch Trend', 'metric': 'Slope',
         'value': f"{trends['first_pitch_trend']['slope']:.3f}", 'unit': '%/year'},
        {'test': 'First Pitch Trend', 'metric': 'R-squared',
         'value': f"{trends['first_pitch_trend']['r_squared']:.4f}", 'unit': ''},
    ]
    pd.DataFrame(stat_tests).to_csv(RESULTS_DIR / 'statistical_tests.csv', index=False)
    print("  Saved: statistical_tests.csv")

    # Summary
    trend_data = trends['data']
    summary = {
        'metric': [
            "Pitcher's Count FB%",
            "Hitter's Count FB%",
            'FB% Difference (Hitter - Pitcher)',
            'Two-Strike Breaking Ball %',
            'First Pitch FB% (2015)',
            'First Pitch FB% (2025)',
            '3-0 Count FB% (2015)',
            '3-0 Count FB% (2025)',
        ],
        'value': [
            f"{comparison['pitcher_count']['fastball_pct']:.1f}%",
            f"{comparison['hitter_count']['fastball_pct']:.1f}%",
            f"{comparison['hitter_count']['fastball_pct'] - comparison['pitcher_count']['fastball_pct']:+.1f}%",
            f"{two_strike['two_strike']['breaking_pct']:.1f}%",
            f"{trend_data.iloc[0]['first_pitch_fb_pct']:.1f}%",
            f"{trend_data.iloc[-1]['first_pitch_fb_pct']:.1f}%",
            f"{trend_data.iloc[0]['three_oh_fb_pct']:.1f}%",
            f"{trend_data.iloc[-1]['three_oh_fb_pct']:.1f}%",
        ]
    }
    pd.DataFrame(summary).to_csv(RESULTS_DIR / 'summary.csv', index=False)
    print("  Saved: summary.csv")


def print_summary(comparison: dict, two_strike: dict, trends: dict):
    """Print analysis summary."""
    print("\n" + "=" * 60)
    print("  Summary: Count-Based Pitch Selection")
    print("=" * 60)

    fb_diff = comparison['hitter_count']['fastball_pct'] - comparison['pitcher_count']['fastball_pct']
    breaking_inc = two_strike['two_strike']['breaking_pct'] - two_strike['other']['breaking_pct']
    trend_data = trends['data']

    print(f"""
KEY FINDINGS:

1. Pitcher's vs Hitter's Counts:
   - Pitcher's counts (0-1, 0-2, 1-2): {comparison['pitcher_count']['fastball_pct']:.1f}% fastballs
   - Hitter's counts (1-0, 2-0, 3-0, etc.): {comparison['hitter_count']['fastball_pct']:.1f}% fastballs
   - Difference: {fb_diff:+.1f}% more fastballs in hitter's counts
   - Chi-square p-value: {comparison['chi2_test']['p_value']:.2e} (highly significant)

2. Two-Strike Strategy:
   - Breaking ball usage increases by {breaking_inc:+.1f}% with 2 strikes
   - Two-strike breaking%: {two_strike['two_strike']['breaking_pct']:.1f}%
   - Other counts breaking%: {two_strike['other']['breaking_pct']:.1f}%

3. First Pitch (0-0) Trends:
   - 2015: {trend_data.iloc[0]['first_pitch_fb_pct']:.1f}% fastballs
   - 2025: {trend_data.iloc[-1]['first_pitch_fb_pct']:.1f}% fastballs

4. 3-0 Count Strategy:
   - 2015: {trend_data.iloc[0]['three_oh_fb_pct']:.1f}% fastballs
   - 2025: {trend_data.iloc[-1]['three_oh_fb_pct']:.1f}% fastballs

INTERPRETATION: Pitchers heavily adjust pitch selection based on count.
In hitter's counts, they throw more fastballs to avoid walks.
With two strikes, they increase breaking ball usage to induce swings and misses.
""")


def main():
    df = load_count_data()

    if len(df) == 0:
        print("\n[ERROR] No data found.")
        return

    count_df = analyze_pitch_mix_by_count(df)
    comparison = analyze_count_type_comparison(df)
    two_strike = analyze_two_strike_strategy(df)
    trends = analyze_yearly_trends(df)

    create_visualizations(count_df, comparison, two_strike, trends)
    save_results(count_df, comparison, two_strike, trends)
    print_summary(comparison, two_strike, trends)

    print("\n" + "=" * 60)
    print("  [DONE] Analysis complete!")
    print("=" * 60)
    print(f"  Figures: {FIGURES_DIR}")
    print(f"  Results: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
