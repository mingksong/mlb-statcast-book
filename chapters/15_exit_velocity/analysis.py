#!/usr/bin/env python3
"""
Chapter 15: Exit Velocity Revolution (2015-2025)

Research Question: How has exit velocity evolved, and what does it
tell us about the modern power game?

Key Metrics:
- Average exit velocity (launch_speed)
- Max exit velocity
- Exit velocity distribution
- Year-over-year trends
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


def load_data():
    """Load all seasons with batted ball data."""
    print("Loading data...")
    columns = [
        'game_year', 'batter', 'pitcher',
        'launch_speed', 'launch_angle',
        'events', 'description',
        'estimated_ba_using_speedangle',
        'estimated_woba_using_speedangle',
        'pitch_type', 'release_speed'
    ]

    df = load_seasons(2015, 2025, columns=columns)
    print(f"Loaded {len(df):,} total pitches")

    # Filter to batted balls only (have exit velocity)
    df = df.dropna(subset=['launch_speed'])
    print(f"Batted balls with exit velocity: {len(df):,}")

    return df


def analyze_yearly_trends(df):
    """Analyze exit velocity trends by year."""
    print("\n--- Yearly Exit Velocity Trends ---")

    yearly = df.groupby('game_year')['launch_speed'].agg([
        'count', 'mean', 'std', 'median',
        lambda x: x.quantile(0.90),
        lambda x: x.quantile(0.95),
        'max'
    ])
    yearly.columns = ['n_batted_balls', 'mean_ev', 'std_ev', 'median_ev',
                      'p90_ev', 'p95_ev', 'max_ev']

    print("\nExit Velocity by Year:")
    print(yearly.round(2))

    # Linear regression for trend
    years = np.array(yearly.index.values, dtype=float)
    means = np.array(yearly['mean_ev'].values, dtype=float)

    slope, intercept, r_value, p_value, std_err = stats.linregress(years, means)

    trend_results = {
        'slope': slope,
        'r_squared': r_value**2,
        'p_value': p_value,
        'start_value': yearly.loc[2015, 'mean_ev'],
        'end_value': yearly.loc[2025, 'mean_ev']
    }

    print(f"\nTrend Analysis:")
    print(f"  Slope: {slope:.3f} mph/year")
    print(f"  R²: {r_value**2:.3f}")
    print(f"  p-value: {p_value:.4f}")
    print(f"  Change: {yearly.loc[2015, 'mean_ev']:.1f} → {yearly.loc[2025, 'mean_ev']:.1f} mph")

    return yearly, trend_results


def analyze_hard_hit_evolution(df):
    """Analyze hard hit rate (95+ mph) evolution."""
    print("\n--- Hard Hit Rate Evolution ---")

    df['hard_hit'] = df['launch_speed'] >= 95

    yearly_hh = df.groupby('game_year').agg({
        'hard_hit': 'mean',
        'launch_speed': 'count'
    })
    yearly_hh.columns = ['hard_hit_rate', 'n_batted_balls']
    yearly_hh['hard_hit_rate'] = yearly_hh['hard_hit_rate'] * 100

    print("\nHard Hit Rate (95+ mph) by Year:")
    print(yearly_hh.round(2))

    # Trend
    years = np.array(yearly_hh.index.values, dtype=float)
    rates = np.array(yearly_hh['hard_hit_rate'].values, dtype=float)
    slope, intercept, r_value, p_value, std_err = stats.linregress(years, rates)

    print(f"\nHard Hit Rate Trend:")
    print(f"  Slope: {slope:.3f}%/year")
    print(f"  R²: {r_value**2:.3f}")
    print(f"  p-value: {p_value:.4f}")

    return yearly_hh, {'slope': slope, 'r_squared': r_value**2, 'p_value': p_value}


def analyze_elite_contact(df):
    """Analyze elite exit velocity (100+ mph) trends."""
    print("\n--- Elite Contact (100+ mph) ---")

    df['elite_ev'] = df['launch_speed'] >= 100

    yearly_elite = df.groupby('game_year')['elite_ev'].mean() * 100

    print("\nElite Exit Velocity Rate (100+ mph):")
    for year, rate in yearly_elite.items():
        print(f"  {year}: {rate:.2f}%")

    return yearly_elite


def statistical_tests(df, yearly):
    """Run statistical tests comparing periods."""
    print("\n--- Statistical Tests ---")

    early_years = [2015, 2016, 2017, 2018]
    late_years = [2022, 2023, 2024, 2025]

    early_ev = df[df['game_year'].isin(early_years)]['launch_speed']
    late_ev = df[df['game_year'].isin(late_years)]['launch_speed']

    # Sample for t-test (full data is too large)
    sample_size = min(500000, len(early_ev), len(late_ev))
    early_sample = early_ev.sample(n=sample_size, random_state=42)
    late_sample = late_ev.sample(n=sample_size, random_state=42)

    t_stat, p_val = stats.ttest_ind(early_sample.astype(float), late_sample.astype(float))

    # Cohen's d
    pooled_std = np.sqrt((early_ev.std()**2 + late_ev.std()**2) / 2)
    cohens_d = (late_ev.mean() - early_ev.mean()) / pooled_std

    tests = [{
        'test': 'Exit Velocity (2015-18 vs 2022-25)',
        'early_mean': early_ev.mean(),
        'late_mean': late_ev.mean(),
        'change': late_ev.mean() - early_ev.mean(),
        't_statistic': t_stat,
        'p_value': p_val,
        'cohens_d': cohens_d,
        'interpretation': 'large' if abs(cohens_d) > 0.8 else 'medium' if abs(cohens_d) > 0.5 else 'small' if abs(cohens_d) > 0.2 else 'negligible'
    }]

    tests_df = pd.DataFrame(tests)

    print(f"\nExit Velocity Change:")
    print(f"  Early (2015-18): {early_ev.mean():.2f} mph")
    print(f"  Late (2022-25): {late_ev.mean():.2f} mph")
    print(f"  Change: {late_ev.mean() - early_ev.mean():+.2f} mph")
    print(f"  t={t_stat:.2f}, p={p_val:.4f}")
    print(f"  Cohen's d: {cohens_d:.3f} ({tests[0]['interpretation']})")

    return tests_df


def create_visualizations(df, yearly, yearly_hh, yearly_elite):
    """Create publication-ready figures."""
    print("\n--- Creating Visualizations ---")

    plt.style.use('seaborn-v0_8-whitegrid')

    # Figure 1: Exit velocity trend
    fig, ax = plt.subplots(figsize=(10, 6))

    years = np.array(yearly.index.values, dtype=float)
    means = np.array(yearly['mean_ev'].values, dtype=float)
    stds = np.array(yearly['std_ev'].values, dtype=float)

    ax.plot(years, means, 'o-', color='#1f77b4', linewidth=2, markersize=8, label='Mean EV')
    ax.fill_between(years, means - stds, means + stds, alpha=0.2, color='#1f77b4')

    # Trend line
    z = np.polyfit(years, means, 1)
    p = np.poly1d(z)
    ax.plot(years, p(years), '--', color='red', linewidth=2, label=f'Trend: {z[0]:+.2f} mph/year')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Exit Velocity (mph)', fontsize=12)
    ax.set_title('Average Exit Velocity Trend (2015-2025)', fontsize=14)
    ax.legend()
    ax.set_xlim(2014.5, 2025.5)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig01_ev_trend.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig01_ev_trend.png")

    # Figure 2: Hard hit rate trend
    fig, ax = plt.subplots(figsize=(10, 6))

    hh_years = np.array(yearly_hh.index.values, dtype=float)
    hh_rates = np.array(yearly_hh['hard_hit_rate'].values, dtype=float)

    ax.plot(hh_years, hh_rates, 'o-', color='#ff7f0e',
            linewidth=2, markersize=8)

    z2 = np.polyfit(hh_years, hh_rates, 1)
    p2 = np.poly1d(z2)
    ax.plot(hh_years, p2(hh_years), '--', color='red', linewidth=2,
            label=f'Trend: {z2[0]:+.2f}%/year')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Hard Hit Rate (%)', fontsize=12)
    ax.set_title('Hard Hit Rate (95+ mph) Trend', fontsize=14)
    ax.legend()
    ax.set_xlim(2014.5, 2025.5)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig02_hard_hit_rate.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig02_hard_hit_rate.png")

    # Figure 3: Distribution comparison 2015 vs 2025
    fig, ax = plt.subplots(figsize=(10, 6))

    ev_2015 = df[df['game_year'] == 2015]['launch_speed']
    ev_2025 = df[df['game_year'] == 2025]['launch_speed']

    ax.hist(ev_2015, bins=50, alpha=0.5, label=f'2015 (mean: {ev_2015.mean():.1f})',
            color='#1f77b4', density=True)
    ax.hist(ev_2025, bins=50, alpha=0.5, label=f'2025 (mean: {ev_2025.mean():.1f})',
            color='#ff7f0e', density=True)

    ax.axvline(x=95, color='red', linestyle='--', linewidth=2, label='Hard Hit (95 mph)')

    ax.set_xlabel('Exit Velocity (mph)', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title('Exit Velocity Distribution: 2015 vs 2025', fontsize=14)
    ax.legend()

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig03_ev_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig03_ev_distribution.png")

    # Figure 4: Percentile trends
    fig, ax = plt.subplots(figsize=(10, 6))

    median_ev = np.array(yearly['median_ev'].values, dtype=float)
    p90_ev = np.array(yearly['p90_ev'].values, dtype=float)
    p95_ev = np.array(yearly['p95_ev'].values, dtype=float)

    ax.plot(years, median_ev, 'o-', label='Median (50th)', linewidth=2)
    ax.plot(years, p90_ev, 's-', label='90th Percentile', linewidth=2)
    ax.plot(years, p95_ev, '^-', label='95th Percentile', linewidth=2)

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Exit Velocity (mph)', fontsize=12)
    ax.set_title('Exit Velocity Percentiles Over Time', fontsize=14)
    ax.legend()
    ax.set_xlim(2014.5, 2025.5)

    plt.tight_layout()
    plt.savefig(f'{FIGURES_DIR}/fig04_ev_percentiles.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved fig04_ev_percentiles.png")


def save_results(yearly, yearly_hh, yearly_elite, tests_df, trend_results, hh_trend):
    """Save all results to CSV files."""
    print("\n--- Saving Results ---")

    yearly.to_csv(f'{RESULTS_DIR}/exit_velocity_by_year.csv')
    print("Saved exit_velocity_by_year.csv")

    yearly_hh.to_csv(f'{RESULTS_DIR}/hard_hit_rate_by_year.csv')
    print("Saved hard_hit_rate_by_year.csv")

    yearly_elite.to_frame('elite_rate').to_csv(f'{RESULTS_DIR}/elite_ev_by_year.csv')
    print("Saved elite_ev_by_year.csv")

    tests_df.to_csv(f'{RESULTS_DIR}/statistical_tests.csv', index=False)
    print("Saved statistical_tests.csv")

    # Summary
    summary = pd.DataFrame({
        'metric': ['Average Exit Velocity', 'Hard Hit Rate', 'Elite EV Rate'],
        'value_2015': [
            f"{yearly.loc[2015, 'mean_ev']:.1f} mph",
            f"{yearly_hh.loc[2015, 'hard_hit_rate']:.1f}%",
            f"{yearly_elite.loc[2015]:.1f}%"
        ],
        'value_2025': [
            f"{yearly.loc[2025, 'mean_ev']:.1f} mph",
            f"{yearly_hh.loc[2025, 'hard_hit_rate']:.1f}%",
            f"{yearly_elite.loc[2025]:.1f}%"
        ],
        'trend': [
            f"{trend_results['slope']:+.2f} mph/year",
            f"{hh_trend['slope']:+.2f}%/year",
            "Increasing"
        ],
        'r_squared': [
            f"{trend_results['r_squared']:.3f}",
            f"{hh_trend['r_squared']:.3f}",
            "N/A"
        ]
    })
    summary.to_csv(f'{RESULTS_DIR}/summary.csv', index=False)
    print("Saved summary.csv")


def main():
    """Execute complete exit velocity analysis."""
    print("=" * 60)
    print("Chapter 15: Exit Velocity Revolution")
    print("=" * 60)

    # Load data
    df = load_data()

    # Analyze trends
    yearly, trend_results = analyze_yearly_trends(df)
    yearly_hh, hh_trend = analyze_hard_hit_evolution(df)
    yearly_elite = analyze_elite_contact(df)

    # Statistical tests
    tests_df = statistical_tests(df, yearly)

    # Create visualizations
    create_visualizations(df, yearly, yearly_hh, yearly_elite)

    # Save results
    save_results(yearly, yearly_hh, yearly_elite, tests_df, trend_results, hh_trend)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nTotal batted balls analyzed: {len(df):,}")
    print(f"\nExit Velocity: {yearly.loc[2015, 'mean_ev']:.1f} → {yearly.loc[2025, 'mean_ev']:.1f} mph")
    print(f"Hard Hit Rate: {yearly_hh.loc[2015, 'hard_hit_rate']:.1f}% → {yearly_hh.loc[2025, 'hard_hit_rate']:.1f}%")
    print(f"Elite EV Rate: {yearly_elite.loc[2015]:.1f}% → {yearly_elite.loc[2025]:.1f}%")

    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
