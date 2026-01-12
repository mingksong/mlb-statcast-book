#!/usr/bin/env python3
"""
Chapter 10: First Pitch Strategy (2015-2025)

Research Question: How do pitchers approach the first pitch of each
plate appearance, and have these strategies evolved?

Key Analyses:
1. First pitch type preferences
2. First pitch strike rate
3. First pitch velocity vs overall
4. First pitch outcomes (ball, strike, in-play)
5. Evolution of first pitch strategy

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

# Pitch categories
FASTBALLS = ['FF', 'SI', 'FC']
BREAKING = ['SL', 'CU', 'ST', 'KC', 'CS']
OFFSPEED = ['CH', 'FS']

# Strike descriptions
STRIKES = ['called_strike', 'swinging_strike', 'foul', 'foul_tip',
           'swinging_strike_blocked', 'foul_bunt', 'missed_bunt']
BALLS = ['ball', 'blocked_ball', 'hit_by_pitch']


def load_first_pitch_data():
    """Load first pitch data for all seasons."""
    print("=" * 60)
    print("  Chapter 10: First Pitch Strategy (2015-2025)")
    print("=" * 60)
    print("\n[1] Loading first pitch data...")

    all_data = []

    for year in AVAILABLE_SEASONS:
        try:
            df = load_season(year, columns=[
                'pitch_type', 'release_speed', 'pitch_number',
                'description', 'zone'
            ])
            df['game_year'] = year

            # Ensure numeric
            df['release_speed'] = pd.to_numeric(df['release_speed'], errors='coerce')
            df['pitch_number'] = pd.to_numeric(df['pitch_number'], errors='coerce')

            # Filter to first pitches (pitch_number == 1)
            first_pitch = df[df['pitch_number'] == 1].copy()
            first_pitch = first_pitch.dropna(subset=['pitch_type'])

            all_data.append(first_pitch)
            print(f"  {year}: {len(first_pitch):,} first pitches")

        except FileNotFoundError:
            print(f"  {year}: data not found, skipping")
            continue

    combined = pd.concat(all_data, ignore_index=True)
    print(f"\n  Total first pitches: {len(combined):,}")

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


def analyze_first_pitch_type(df: pd.DataFrame):
    """Analyze pitch type selection on first pitch."""
    print("\n[2] Analyzing first pitch type selection...")

    df['pitch_category'] = df['pitch_type'].apply(categorize_pitch)

    results = []

    for year in sorted(df['game_year'].unique()):
        year_data = df[df['game_year'] == year]
        total = len(year_data)

        # Category percentages
        fastball_pct = (year_data['pitch_category'] == 'Fastball').mean() * 100
        breaking_pct = (year_data['pitch_category'] == 'Breaking').mean() * 100
        offspeed_pct = (year_data['pitch_category'] == 'Offspeed').mean() * 100

        # Top pitch types
        ff_pct = (year_data['pitch_type'] == 'FF').mean() * 100
        si_pct = (year_data['pitch_type'] == 'SI').mean() * 100
        sl_pct = (year_data['pitch_type'] == 'SL').mean() * 100

        results.append({
            'year': year,
            'total': total,
            'fastball_pct': fastball_pct,
            'breaking_pct': breaking_pct,
            'offspeed_pct': offspeed_pct,
            'ff_pct': ff_pct,
            'si_pct': si_pct,
            'sl_pct': sl_pct,
        })

    results_df = pd.DataFrame(results)

    print("\n  First Pitch Type Distribution:")
    for _, row in results_df.iterrows():
        print(f"    {int(row['year'])}: FB={row['fastball_pct']:.1f}%, "
              f"BR={row['breaking_pct']:.1f}%, OS={row['offspeed_pct']:.1f}%")

    return results_df


def analyze_first_pitch_strike_rate(df: pd.DataFrame):
    """Analyze first pitch strike rate over time."""
    print("\n[3] Analyzing first pitch strike rate...")

    results = []

    for year in sorted(df['game_year'].unique()):
        year_data = df[df['game_year'] == year]

        # Calculate strike rate
        year_data['is_strike'] = year_data['description'].isin(STRIKES) | \
                                  year_data['description'].str.contains('in_play', na=False)

        strike_rate = year_data['is_strike'].mean() * 100

        # In-zone rate (zone 1-9 is in the zone)
        zone_data = year_data['zone'].dropna()
        in_zone_rate = ((zone_data >= 1) & (zone_data <= 9)).mean() * 100

        results.append({
            'year': year,
            'strike_rate': strike_rate,
            'in_zone_rate': in_zone_rate,
            'n': len(year_data),
        })

    results_df = pd.DataFrame(results)

    print("\n  First Pitch Strike Rate:")
    for _, row in results_df.iterrows():
        print(f"    {int(row['year'])}: Strike={row['strike_rate']:.1f}%, "
              f"In-Zone={row['in_zone_rate']:.1f}%")

    return results_df


def analyze_first_pitch_velocity(df: pd.DataFrame):
    """Compare first pitch velocity to overall."""
    print("\n[4] Analyzing first pitch velocity...")

    # Filter to 4-seam fastballs
    ff_data = df[df['pitch_type'] == 'FF'].copy()

    results = []

    for year in sorted(ff_data['game_year'].unique()):
        year_data = ff_data[ff_data['game_year'] == year]
        velo = year_data['release_speed'].dropna()

        if len(velo) < 100:
            continue

        results.append({
            'year': year,
            'mean_velo': velo.mean(),
            'std_velo': velo.std(),
            'n': len(velo),
        })

    results_df = pd.DataFrame(results)

    print("\n  First Pitch 4-Seam Velocity:")
    for _, row in results_df.iterrows():
        print(f"    {int(row['year'])}: {row['mean_velo']:.2f} mph (n={int(row['n']):,})")

    return results_df


def analyze_first_pitch_outcomes(df: pd.DataFrame):
    """Analyze first pitch outcomes distribution."""
    print("\n[5] Analyzing first pitch outcomes...")

    results = []

    for year in sorted(df['game_year'].unique()):
        year_data = df[df['game_year'] == year]

        # Categorize outcomes
        called_strike = (year_data['description'] == 'called_strike').mean() * 100
        swinging_strike = year_data['description'].str.contains('swinging', na=False).mean() * 100
        foul = year_data['description'].str.contains('foul', na=False).mean() * 100
        ball = year_data['description'].isin(BALLS).mean() * 100
        in_play = year_data['description'].str.contains('in_play', na=False).mean() * 100

        results.append({
            'year': year,
            'called_strike': called_strike,
            'swinging_strike': swinging_strike,
            'foul': foul,
            'ball': ball,
            'in_play': in_play,
        })

    results_df = pd.DataFrame(results)

    print("\n  2025 First Pitch Outcomes:")
    latest = results_df[results_df['year'] == 2025].iloc[0]
    print(f"    Called Strike: {latest['called_strike']:.1f}%")
    print(f"    Swinging Strike: {latest['swinging_strike']:.1f}%")
    print(f"    Foul: {latest['foul']:.1f}%")
    print(f"    Ball: {latest['ball']:.1f}%")
    print(f"    In Play: {latest['in_play']:.1f}%")

    return results_df


def perform_trend_analysis(type_df: pd.DataFrame, strike_df: pd.DataFrame):
    """Perform trend analysis on key metrics."""
    print("\n[6] Trend Analysis...")

    results = {}

    # Fastball trend
    years = type_df['year'].values
    fastball = type_df['fastball_pct'].values

    slope, intercept, r_value, p_value, std_err = stats.linregress(years, fastball)
    results['fastball_trend'] = {
        'slope': slope,
        'r_squared': r_value**2,
        'p_value': p_value,
    }

    print(f"\n  First Pitch Fastball% Trend:")
    print(f"    Slope: {slope:.3f}%/year")
    print(f"    R²: {results['fastball_trend']['r_squared']:.4f}")
    print(f"    p-value: {p_value:.2e}")

    # Strike rate trend
    years = strike_df['year'].values
    strike_rate = strike_df['strike_rate'].values

    slope, intercept, r_value, p_value, std_err = stats.linregress(years, strike_rate)
    results['strike_trend'] = {
        'slope': slope,
        'r_squared': r_value**2,
        'p_value': p_value,
    }

    print(f"\n  First Pitch Strike% Trend:")
    print(f"    Slope: {slope:.3f}%/year")
    print(f"    R²: {results['strike_trend']['r_squared']:.4f}")
    print(f"    p-value: {p_value:.2e}")

    return results


def create_visualizations(type_df: pd.DataFrame, strike_df: pd.DataFrame,
                          velocity_df: pd.DataFrame, outcome_df: pd.DataFrame):
    """Generate visualizations."""
    print("\n[7] Creating visualizations...")

    # Figure 1: First pitch type trend
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(type_df['year'], type_df['fastball_pct'], 'o-',
            linewidth=2, markersize=8, label='Fastball', color='#1f77b4')
    ax.plot(type_df['year'], type_df['breaking_pct'], 's-',
            linewidth=2, markersize=8, label='Breaking', color='#ff7f0e')
    ax.plot(type_df['year'], type_df['offspeed_pct'], '^-',
            linewidth=2, markersize=8, label='Offspeed', color='#2ca02c')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('First Pitch Usage (%)', fontsize=12)
    ax.set_title('First Pitch Type Selection Over Time', fontsize=14)
    ax.legend()

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig01_first_pitch_type.png', dpi=150)
    plt.close()
    print("  Saved: fig01_first_pitch_type.png")

    # Figure 2: Strike rate trend
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(strike_df['year'], strike_df['strike_rate'], 'o-',
            linewidth=2, markersize=10, color='#d62728')
    ax.fill_between(strike_df['year'], 50, strike_df['strike_rate'],
                    alpha=0.3, color='#d62728')

    ax.axhline(y=60, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('First Pitch Strike Rate (%)', fontsize=12)
    ax.set_title('First Pitch Strike Rate Over Time', fontsize=14)
    ax.set_ylim(50, 70)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig02_strike_rate.png', dpi=150)
    plt.close()
    print("  Saved: fig02_strike_rate.png")

    # Figure 3: Velocity comparison
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(velocity_df['year'], velocity_df['mean_velo'], 'o-',
            linewidth=2, markersize=10, color='#9467bd')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('First Pitch 4-Seam Velocity (mph)', fontsize=12)
    ax.set_title('First Pitch Fastball Velocity', fontsize=14)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig03_first_pitch_velocity.png', dpi=150)
    plt.close()
    print("  Saved: fig03_first_pitch_velocity.png")

    # Figure 4: Outcome distribution (2015 vs 2025)
    fig, ax = plt.subplots(figsize=(10, 6))

    categories = ['Called Strike', 'Swinging Strike', 'Foul', 'Ball', 'In Play']
    cols = ['called_strike', 'swinging_strike', 'foul', 'ball', 'in_play']

    early = outcome_df[outcome_df['year'] == 2015].iloc[0]
    late = outcome_df[outcome_df['year'] == 2025].iloc[0]

    x = np.arange(len(categories))
    width = 0.35

    ax.bar(x - width/2, [early[c] for c in cols], width, label='2015', color='#1f77b4')
    ax.bar(x + width/2, [late[c] for c in cols], width, label='2025', color='#ff7f0e')

    ax.set_xlabel('Outcome', fontsize=12)
    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.set_title('First Pitch Outcomes: 2015 vs 2025', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=15)
    ax.legend()

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig04_outcomes.png', dpi=150)
    plt.close()
    print("  Saved: fig04_outcomes.png")


def save_results(type_df: pd.DataFrame, strike_df: pd.DataFrame,
                 velocity_df: pd.DataFrame, outcome_df: pd.DataFrame,
                 trend_results: dict):
    """Save results to CSV."""
    print("\n[8] Saving results...")

    type_df.to_csv(RESULTS_DIR / 'first_pitch_types.csv', index=False)
    print("  Saved: first_pitch_types.csv")

    strike_df.to_csv(RESULTS_DIR / 'first_pitch_strikes.csv', index=False)
    print("  Saved: first_pitch_strikes.csv")

    velocity_df.to_csv(RESULTS_DIR / 'first_pitch_velocity.csv', index=False)
    print("  Saved: first_pitch_velocity.csv")

    outcome_df.to_csv(RESULTS_DIR / 'first_pitch_outcomes.csv', index=False)
    print("  Saved: first_pitch_outcomes.csv")

    # Statistical tests
    stat_tests = [
        {'test': 'Fastball Trend', 'metric': 'Slope', 'value': f"{trend_results['fastball_trend']['slope']:.3f}", 'unit': '%/year'},
        {'test': 'Fastball Trend', 'metric': 'R-squared', 'value': f"{trend_results['fastball_trend']['r_squared']:.4f}", 'unit': ''},
        {'test': 'Fastball Trend', 'metric': 'p-value', 'value': f"{trend_results['fastball_trend']['p_value']:.2e}", 'unit': ''},
        {'test': 'Strike Rate Trend', 'metric': 'Slope', 'value': f"{trend_results['strike_trend']['slope']:.3f}", 'unit': '%/year'},
        {'test': 'Strike Rate Trend', 'metric': 'R-squared', 'value': f"{trend_results['strike_trend']['r_squared']:.4f}", 'unit': ''},
        {'test': 'Strike Rate Trend', 'metric': 'p-value', 'value': f"{trend_results['strike_trend']['p_value']:.2e}", 'unit': ''},
    ]
    pd.DataFrame(stat_tests).to_csv(RESULTS_DIR / 'statistical_tests.csv', index=False)
    print("  Saved: statistical_tests.csv")

    # Summary
    summary = {
        'metric': [
            'First Pitch FB% (2015)',
            'First Pitch FB% (2025)',
            'FB% Change',
            'First Pitch Strike% (2015)',
            'First Pitch Strike% (2025)',
            'Strike% Change',
            'First Pitch 4-Seam Velo (2025)',
        ],
        'value': [
            f"{type_df.iloc[0]['fastball_pct']:.1f}%",
            f"{type_df.iloc[-1]['fastball_pct']:.1f}%",
            f"{type_df.iloc[-1]['fastball_pct'] - type_df.iloc[0]['fastball_pct']:+.1f}%",
            f"{strike_df.iloc[0]['strike_rate']:.1f}%",
            f"{strike_df.iloc[-1]['strike_rate']:.1f}%",
            f"{strike_df.iloc[-1]['strike_rate'] - strike_df.iloc[0]['strike_rate']:+.1f}%",
            f"{velocity_df.iloc[-1]['mean_velo']:.2f} mph",
        ]
    }
    pd.DataFrame(summary).to_csv(RESULTS_DIR / 'summary.csv', index=False)
    print("  Saved: summary.csv")


def print_summary(type_df: pd.DataFrame, strike_df: pd.DataFrame,
                  trend_results: dict):
    """Print analysis summary."""
    print("\n" + "=" * 60)
    print("  Summary: First Pitch Strategy")
    print("=" * 60)

    fb_change = type_df.iloc[-1]['fastball_pct'] - type_df.iloc[0]['fastball_pct']
    strike_change = strike_df.iloc[-1]['strike_rate'] - strike_df.iloc[0]['strike_rate']

    print(f"""
KEY FINDINGS:

1. First Pitch Type Selection:
   - 2015 Fastball%: {type_df.iloc[0]['fastball_pct']:.1f}%
   - 2025 Fastball%: {type_df.iloc[-1]['fastball_pct']:.1f}%
   - Change: {fb_change:+.1f}%
   - Trend: {trend_results['fastball_trend']['slope']:.3f}%/year (p={trend_results['fastball_trend']['p_value']:.2e})

2. First Pitch Strike Rate:
   - 2015: {strike_df.iloc[0]['strike_rate']:.1f}%
   - 2025: {strike_df.iloc[-1]['strike_rate']:.1f}%
   - Change: {strike_change:+.1f}%
   - Trend: {trend_results['strike_trend']['slope']:.3f}%/year (p={trend_results['strike_trend']['p_value']:.2e})

3. 2025 Breaking Ball on First Pitch: {type_df.iloc[-1]['breaking_pct']:.1f}%

INTERPRETATION: Pitchers are throwing fewer fastballs on the first pitch,
becoming more aggressive with breaking balls to start plate appearances.
""")


def main():
    df = load_first_pitch_data()

    if len(df) == 0:
        print("\n[ERROR] No data found.")
        return

    type_df = analyze_first_pitch_type(df)
    strike_df = analyze_first_pitch_strike_rate(df)
    velocity_df = analyze_first_pitch_velocity(df)
    outcome_df = analyze_first_pitch_outcomes(df)
    trend_results = perform_trend_analysis(type_df, strike_df)

    create_visualizations(type_df, strike_df, velocity_df, outcome_df)
    save_results(type_df, strike_df, velocity_df, outcome_df, trend_results)
    print_summary(type_df, strike_df, trend_results)

    print("\n" + "=" * 60)
    print("  [DONE] Analysis complete!")
    print("=" * 60)
    print(f"  Figures: {FIGURES_DIR}")
    print(f"  Results: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
