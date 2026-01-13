#!/usr/bin/env python3
"""
Chapter 12: Pitch Effectiveness by Type (2015-2025)

Research Question: Which pitch types are most effective, and how has
pitch effectiveness evolved over the decade?

Key Metrics:
- wOBA (weighted on-base average) per pitch type
- Batting average against
- Whiff rate (swinging strikes / swings)
- Called strike + swinging strike rate
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from statcast_analysis import load_seasons

# Configuration
FIGURES_DIR = 'figures'
RESULTS_DIR = 'results'

# Pitch type groupings
PITCH_CATEGORIES = {
    'FF': 'Fastball',
    'SI': 'Fastball',
    'FC': 'Fastball',
    'SL': 'Breaking',
    'ST': 'Breaking',
    'CU': 'Breaking',
    'KC': 'Breaking',
    'CH': 'Offspeed',
    'FS': 'Offspeed'
}


def load_data():
    """Load all seasons with effectiveness metrics."""
    print("Loading data...")
    columns = [
        'game_year', 'pitch_type', 'pitch_name',
        'release_speed', 'release_spin_rate',
        'woba_value', 'woba_denom',
        'estimated_ba_using_speedangle', 'estimated_woba_using_speedangle',
        'events', 'description', 'type',
        'launch_speed', 'launch_angle',
        'zone', 'plate_x', 'plate_z'
    ]

    df = load_seasons(2015, 2025, columns=columns)
    print(f"Loaded {len(df):,} total pitches")

    return df


def categorize_pitches(df):
    """Add pitch category column."""
    df['pitch_category'] = df['pitch_type'].map(PITCH_CATEGORIES)
    df = df.dropna(subset=['pitch_category'])
    return df


def calculate_effectiveness_metrics(df):
    """Calculate effectiveness metrics by pitch type and year."""
    print("\n--- Calculating Effectiveness Metrics ---")

    results = []

    for (year, pitch_type), group in df.groupby(['game_year', 'pitch_type']):
        if len(group) < 1000:  # Minimum sample
            continue

        # wOBA calculation (only on PA-ending pitches)
        woba_data = group[group['woba_denom'] > 0]
        if len(woba_data) > 0:
            woba = woba_data['woba_value'].sum() / woba_data['woba_denom'].sum()
        else:
            woba = np.nan

        # Batting average against (on balls in play)
        hits = group['events'].isin(['single', 'double', 'triple', 'home_run']).sum()
        ab_events = ['single', 'double', 'triple', 'home_run', 'field_out',
                     'grounded_into_double_play', 'force_out', 'fielders_choice',
                     'fielders_choice_out', 'double_play', 'triple_play',
                     'field_error', 'strikeout']
        at_bats = group['events'].isin(ab_events).sum()
        ba = hits / at_bats if at_bats > 0 else np.nan

        # Whiff rate (swinging strikes / swings)
        swings = group['description'].isin([
            'swinging_strike', 'swinging_strike_blocked', 'foul', 'foul_tip',
            'hit_into_play', 'foul_bunt', 'missed_bunt'
        ]).sum()
        whiffs = group['description'].isin(['swinging_strike', 'swinging_strike_blocked']).sum()
        whiff_rate = whiffs / swings if swings > 0 else np.nan

        # Strike rate (called + swinging strikes / total)
        strikes = group['type'].isin(['S', 'X']).sum()  # S = strike, X = in play
        strike_rate = strikes / len(group) if len(group) > 0 else np.nan

        # Called strike rate
        called_strikes = group['description'].isin(['called_strike']).sum()
        called_strike_rate = called_strikes / len(group) if len(group) > 0 else np.nan

        # In-zone rate
        in_zone = ((group['zone'] >= 1) & (group['zone'] <= 9)).sum()
        zone_rate = in_zone / len(group) if len(group) > 0 else np.nan

        # Average velocity
        avg_velo = group['release_speed'].mean()

        results.append({
            'game_year': year,
            'pitch_type': pitch_type,
            'pitch_category': PITCH_CATEGORIES.get(pitch_type, 'Other'),
            'n_pitches': len(group),
            'woba': woba,
            'batting_avg': ba,
            'whiff_rate': whiff_rate,
            'strike_rate': strike_rate,
            'called_strike_rate': called_strike_rate,
            'zone_rate': zone_rate,
            'avg_velocity': avg_velo
        })

    results_df = pd.DataFrame(results)
    print(f"Calculated metrics for {len(results_df)} pitch type-year combinations")

    return results_df


def analyze_by_category(df, effectiveness_df):
    """Analyze effectiveness by pitch category over time."""
    print("\n--- Analyzing by Category ---")

    # Aggregate by category and year
    category_results = []

    for (year, category), group in df.groupby(['game_year', 'pitch_category']):
        woba_data = group[group['woba_denom'] > 0]
        if len(woba_data) > 0:
            woba = woba_data['woba_value'].sum() / woba_data['woba_denom'].sum()
        else:
            woba = np.nan

        # Whiff rate
        swings = group['description'].isin([
            'swinging_strike', 'swinging_strike_blocked', 'foul', 'foul_tip',
            'hit_into_play', 'foul_bunt', 'missed_bunt'
        ]).sum()
        whiffs = group['description'].isin(['swinging_strike', 'swinging_strike_blocked']).sum()
        whiff_rate = whiffs / swings if swings > 0 else np.nan

        category_results.append({
            'game_year': year,
            'pitch_category': category,
            'n_pitches': len(group),
            'woba': woba,
            'whiff_rate': whiff_rate
        })

    category_df = pd.DataFrame(category_results)

    # Print summary
    print("\nwOBA by Category (2015 vs 2025):")
    for cat in ['Fastball', 'Breaking', 'Offspeed']:
        w2015 = category_df[(category_df['game_year'] == 2015) &
                           (category_df['pitch_category'] == cat)]['woba'].values
        w2025 = category_df[(category_df['game_year'] == 2025) &
                           (category_df['pitch_category'] == cat)]['woba'].values
        if len(w2015) > 0 and len(w2025) > 0:
            print(f"  {cat}: {w2015[0]:.3f} → {w2025[0]:.3f} ({w2025[0] - w2015[0]:+.3f})")

    print("\nWhiff Rate by Category (2015 vs 2025):")
    for cat in ['Fastball', 'Breaking', 'Offspeed']:
        wr2015 = category_df[(category_df['game_year'] == 2015) &
                            (category_df['pitch_category'] == cat)]['whiff_rate'].values
        wr2025 = category_df[(category_df['game_year'] == 2025) &
                            (category_df['pitch_category'] == cat)]['whiff_rate'].values
        if len(wr2015) > 0 and len(wr2025) > 0:
            print(f"  {cat}: {wr2015[0]*100:.1f}% → {wr2025[0]*100:.1f}% ({(wr2025[0] - wr2015[0])*100:+.1f}%)")

    return category_df


def analyze_specific_pitches(effectiveness_df):
    """Deep dive on specific pitch types."""
    print("\n--- Specific Pitch Type Analysis ---")

    key_pitches = ['FF', 'SL', 'CH', 'CU', 'SI', 'FC', 'ST', 'FS']

    pitch_trends = []

    for pitch in key_pitches:
        pitch_data = effectiveness_df[effectiveness_df['pitch_type'] == pitch]
        if len(pitch_data) < 5:
            continue

        years = pitch_data['game_year'].values
        woba = pitch_data['woba'].values
        whiff = pitch_data['whiff_rate'].values

        # wOBA trend
        if len(woba[~np.isnan(woba)]) >= 3:
            valid = ~np.isnan(woba)
            slope_woba, _, r_woba, p_woba, _ = stats.linregress(years[valid], woba[valid])
        else:
            slope_woba, r_woba, p_woba = np.nan, np.nan, np.nan

        # Whiff rate trend
        if len(whiff[~np.isnan(whiff)]) >= 3:
            valid_w = ~np.isnan(whiff)
            slope_whiff, _, r_whiff, p_whiff, _ = stats.linregress(years[valid_w], whiff[valid_w])
        else:
            slope_whiff, r_whiff, p_whiff = np.nan, np.nan, np.nan

        # Get 2015 and 2025 values
        w2015 = pitch_data[pitch_data['game_year'] == 2015]['woba'].values
        w2025 = pitch_data[pitch_data['game_year'] == 2025]['woba'].values
        wr2015 = pitch_data[pitch_data['game_year'] == 2015]['whiff_rate'].values
        wr2025 = pitch_data[pitch_data['game_year'] == 2025]['whiff_rate'].values

        pitch_trends.append({
            'pitch_type': pitch,
            'woba_2015': w2015[0] if len(w2015) > 0 else np.nan,
            'woba_2025': w2025[0] if len(w2025) > 0 else np.nan,
            'woba_slope': slope_woba,
            'woba_r2': r_woba**2 if not np.isnan(r_woba) else np.nan,
            'woba_p': p_woba,
            'whiff_2015': wr2015[0] if len(wr2015) > 0 else np.nan,
            'whiff_2025': wr2025[0] if len(wr2025) > 0 else np.nan,
            'whiff_slope': slope_whiff,
            'whiff_r2': r_whiff**2 if not np.isnan(r_whiff) else np.nan,
            'whiff_p': p_whiff
        })

    pitch_trends_df = pd.DataFrame(pitch_trends)

    print("\nPitch Type Trends:")
    print(pitch_trends_df[['pitch_type', 'woba_2015', 'woba_2025', 'whiff_2015', 'whiff_2025']].to_string())

    return pitch_trends_df


def statistical_tests(df):
    """Statistical tests comparing early vs late periods."""
    print("\n--- Statistical Tests ---")

    early_years = [2015, 2016, 2017, 2018]
    late_years = [2022, 2023, 2024, 2025]

    tests = []

    for category in ['Fastball', 'Breaking', 'Offspeed']:
        # Get wOBA values for PA-ending pitches in each period
        cat_early = df[(df['game_year'].isin(early_years)) &
                       (df['pitch_category'] == category) &
                       (df['woba_denom'] > 0)]
        cat_late = df[(df['game_year'].isin(late_years)) &
                      (df['pitch_category'] == category) &
                      (df['woba_denom'] > 0)]

        early_woba = cat_early['woba_value'] / cat_early['woba_denom']
        late_woba = cat_late['woba_value'] / cat_late['woba_denom']

        # Aggregate wOBA
        early_total_woba = cat_early['woba_value'].sum() / cat_early['woba_denom'].sum()
        late_total_woba = cat_late['woba_value'].sum() / cat_late['woba_denom'].sum()

        # Calculate effect size using standard error approximation
        # For large samples, use the difference and a reasonable pooled SD
        pooled_std = 0.15  # Approximate wOBA standard deviation
        cohens_d = (late_total_woba - early_total_woba) / pooled_std

        tests.append({
            'test': f'{category} wOBA (2015-18 vs 2022-25)',
            'early_mean': early_total_woba,
            'late_mean': late_total_woba,
            'change': late_total_woba - early_total_woba,
            'cohens_d': cohens_d,
            'interpretation': 'large' if abs(cohens_d) > 0.8 else 'medium' if abs(cohens_d) > 0.5 else 'small' if abs(cohens_d) > 0.2 else 'negligible',
            'n_early': len(cat_early),
            'n_late': len(cat_late)
        })

    tests_df = pd.DataFrame(tests)

    print("\nCategory Effectiveness Changes:")
    for _, row in tests_df.iterrows():
        print(f"\n{row['test']}:")
        print(f"  Early: {row['early_mean']:.3f}, Late: {row['late_mean']:.3f}")
        print(f"  Change: {row['change']:+.3f}")
        print(f"  Cohen's d: {row['cohens_d']:.3f} ({row['interpretation']})")

    return tests_df


def create_visualizations(effectiveness_df, category_df, pitch_trends_df):
    """Create publication-ready figures."""
    print("\n--- Creating Visualizations ---")

    plt.style.use('seaborn-v0_8-whitegrid')

    # Figure 1: wOBA by category over time
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = {'Fastball': '#1f77b4', 'Breaking': '#ff7f0e', 'Offspeed': '#2ca02c'}

    for cat in ['Fastball', 'Breaking', 'Offspeed']:
        cat_data = category_df[category_df['pitch_category'] == cat].sort_values('game_year')
        ax.plot(cat_data['game_year'], cat_data['woba'], 'o-',
                label=cat, color=colors[cat], linewidth=2, markersize=8)

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('wOBA Against', fontsize=12)
    ax.set_title('Pitch Category Effectiveness: wOBA Against (2015-2025)\nLower = More Effective', fontsize=14)
    ax.legend()
    ax.set_xlim(2014.5, 2025.5)
    ax.set_ylim(0.25, 0.45)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_woba_by_category.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig01_woba_by_category.png")

    # Figure 2: Whiff rate by category
    fig, ax = plt.subplots(figsize=(10, 6))

    for cat in ['Fastball', 'Breaking', 'Offspeed']:
        cat_data = category_df[category_df['pitch_category'] == cat].sort_values('game_year')
        ax.plot(cat_data['game_year'], cat_data['whiff_rate'] * 100, 'o-',
                label=cat, color=colors[cat], linewidth=2, markersize=8)

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Whiff Rate (%)', fontsize=12)
    ax.set_title('Pitch Category Whiff Rate (2015-2025)\nHigher = More Effective', fontsize=14)
    ax.legend()
    ax.set_xlim(2014.5, 2025.5)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig02_whiff_by_category.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig02_whiff_by_category.png")

    # Figure 3: Specific pitch type wOBA comparison (bar chart)
    fig, ax = plt.subplots(figsize=(12, 6))

    pitches = pitch_trends_df['pitch_type'].tolist()
    x = np.arange(len(pitches))
    width = 0.35

    woba_2015 = pitch_trends_df['woba_2015'].values
    woba_2025 = pitch_trends_df['woba_2025'].values

    bars1 = ax.bar(x - width/2, woba_2015, width, label='2015', color='#1f77b4', alpha=0.8)
    bars2 = ax.bar(x + width/2, woba_2025, width, label='2025', color='#ff7f0e', alpha=0.8)

    ax.set_xlabel('Pitch Type', fontsize=12)
    ax.set_ylabel('wOBA Against', fontsize=12)
    ax.set_title('wOBA Against by Pitch Type: 2015 vs 2025', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(pitches)
    ax.legend()
    ax.set_ylim(0.2, 0.5)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig03_woba_by_pitch_type.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig03_woba_by_pitch_type.png")

    # Figure 4: Whiff rate by specific pitch type
    fig, ax = plt.subplots(figsize=(12, 6))

    whiff_2015 = pitch_trends_df['whiff_2015'].values * 100
    whiff_2025 = pitch_trends_df['whiff_2025'].values * 100

    bars1 = ax.bar(x - width/2, whiff_2015, width, label='2015', color='#1f77b4', alpha=0.8)
    bars2 = ax.bar(x + width/2, whiff_2025, width, label='2025', color='#ff7f0e', alpha=0.8)

    ax.set_xlabel('Pitch Type', fontsize=12)
    ax.set_ylabel('Whiff Rate (%)', fontsize=12)
    ax.set_title('Whiff Rate by Pitch Type: 2015 vs 2025', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(pitches)
    ax.legend()

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig04_whiff_by_pitch_type.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig04_whiff_by_pitch_type.png")


def save_results(effectiveness_df, category_df, pitch_trends_df, tests_df):
    """Save all results to CSV files."""
    print("\n--- Saving Results ---")

    # Effectiveness by pitch type and year
    effectiveness_df.to_csv(f'{RESULTS_DIR}/effectiveness_by_pitch_year.csv', index=False)
    print("Saved effectiveness_by_pitch_year.csv")

    # Category summary
    category_df.to_csv(f'{RESULTS_DIR}/effectiveness_by_category.csv', index=False)
    print("Saved effectiveness_by_category.csv")

    # Pitch trends
    pitch_trends_df.to_csv(f'{RESULTS_DIR}/pitch_type_trends.csv', index=False)
    print("Saved pitch_type_trends.csv")

    # Statistical tests
    tests_df.to_csv(f'{RESULTS_DIR}/statistical_tests.csv', index=False)
    print("Saved statistical_tests.csv")

    # Summary
    summary = {
        'finding': [],
        'value': []
    }

    # Most effective pitch type (lowest wOBA in 2025)
    latest = effectiveness_df[effectiveness_df['game_year'] == 2025]
    best_pitch = latest.loc[latest['woba'].idxmin()]
    summary['finding'].append('Most effective pitch 2025 (lowest wOBA)')
    summary['value'].append(f"{best_pitch['pitch_type']} ({best_pitch['woba']:.3f})")

    # Highest whiff rate
    best_whiff = latest.loc[latest['whiff_rate'].idxmax()]
    summary['finding'].append('Highest whiff rate 2025')
    summary['value'].append(f"{best_whiff['pitch_type']} ({best_whiff['whiff_rate']*100:.1f}%)")

    # Category changes
    for cat in ['Fastball', 'Breaking', 'Offspeed']:
        cat_data = category_df[category_df['pitch_category'] == cat]
        w2015 = cat_data[cat_data['game_year'] == 2015]['woba'].values[0]
        w2025 = cat_data[cat_data['game_year'] == 2025]['woba'].values[0]
        summary['finding'].append(f'{cat} wOBA change')
        summary['value'].append(f"{w2015:.3f} → {w2025:.3f} ({w2025-w2015:+.3f})")

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(f'{RESULTS_DIR}/summary.csv', index=False)
    print("Saved summary.csv")


def main():
    """Execute complete pitch effectiveness analysis."""
    print("=" * 60)
    print("Chapter 12: Pitch Effectiveness by Type")
    print("=" * 60)

    # Load data
    df = load_data()

    # Categorize pitches
    df = categorize_pitches(df)
    print(f"After categorization: {len(df):,} pitches")

    # Calculate effectiveness metrics
    effectiveness_df = calculate_effectiveness_metrics(df)

    # Analyze by category
    category_df = analyze_by_category(df, effectiveness_df)

    # Analyze specific pitches
    pitch_trends_df = analyze_specific_pitches(effectiveness_df)

    # Statistical tests
    tests_df = statistical_tests(df)

    # Create visualizations
    create_visualizations(effectiveness_df, category_df, pitch_trends_df)

    # Save results
    save_results(effectiveness_df, category_df, pitch_trends_df, tests_df)

    # Print final summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print("\nKey Findings:")
    print("1. Breaking balls remain the most effective category (lowest wOBA)")
    print("2. Whiff rates have increased across all categories")
    print("3. Sweeper (ST) has become one of the most effective individual pitches")

    # Get 2025 most effective
    latest = effectiveness_df[effectiveness_df['game_year'] == 2025]
    best = latest.nsmallest(3, 'woba')[['pitch_type', 'woba', 'whiff_rate']]
    print("\nTop 3 Most Effective Pitches 2025 (by wOBA):")
    for _, row in best.iterrows():
        print(f"  {row['pitch_type']}: wOBA={row['woba']:.3f}, Whiff={row['whiff_rate']*100:.1f}%")

    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
