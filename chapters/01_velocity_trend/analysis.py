#!/usr/bin/env python3
"""
Chapter 1: The Velocity Arms Race (2015-2025)

Analysis of 10-year velocity trends in MLB fastballs.

Usage:
    python analysis.py
"""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from statcast_analysis import load_season, AVAILABLE_SEASONS

# Output directories
FIGURES_DIR = Path(__file__).parent / "figures"
RESULTS_DIR = Path(__file__).parent / "results"
FIGURES_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# Plot style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


def analyze_velocity_by_year():
    """Calculate yearly velocity statistics."""
    print("=" * 60)
    print("  Chapter 1: The Velocity Arms Race (2015-2025)")
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

            results.append({
                'year': year,
                'count': len(ff),
                'mean': ff.mean(),
                'median': ff.median(),
                'std': ff.std(),
                'pct_95plus': (ff >= 95).mean() * 100,
                'pct_100plus': (ff >= 100).mean() * 100,
                'max': ff.max(),
            })

            print(f"  {year}: {ff.mean():.1f} mph (n={len(ff):,})")

        except FileNotFoundError:
            print(f"  {year}: data not found, skipping")
            continue

    return pd.DataFrame(results)


def create_visualizations(df: pd.DataFrame):
    """Generate chapter visualizations."""
    print("\n[2] Creating visualizations...")

    # Figure 1: Velocity trend over time
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['year'], df['mean'], 'o-', linewidth=2, markersize=8, color='#1f77b4')
    ax.fill_between(df['year'], df['mean'] - df['std'], df['mean'] + df['std'], alpha=0.2)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Average 4-Seam Fastball Velocity (mph)', fontsize=12)
    ax.set_title('The Velocity Arms Race: 4-Seam Fastball Velocity (2015-2025)', fontsize=14)
    ax.set_xlim(2014.5, 2025.5)
    ax.set_ylim(92.5, 95.5)

    # Add annotations for key years
    ax.annotate(f"{df.iloc[0]['mean']:.1f}", (df.iloc[0]['year'], df.iloc[0]['mean']),
                textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)
    ax.annotate(f"{df.iloc[-1]['mean']:.1f}", (df.iloc[-1]['year'], df.iloc[-1]['mean']),
                textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)

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


def save_results(df: pd.DataFrame):
    """Save analysis results to CSV."""
    print("\n[4] Saving results...")

    # Main results
    df.to_csv(RESULTS_DIR / 'velocity_by_year.csv', index=False)
    print(f"  Saved: velocity_by_year.csv")

    # Summary statistics
    summary = {
        'metric': [
            '2015 Average Velocity',
            '2025 Average Velocity',
            '10-Year Change',
            '2015 95+ Percentage',
            '2025 95+ Percentage',
        ],
        'value': [
            f"{df.iloc[0]['mean']:.1f} mph",
            f"{df.iloc[-1]['mean']:.1f} mph",
            f"+{df.iloc[-1]['mean'] - df.iloc[0]['mean']:.1f} mph",
            f"{df.iloc[0]['pct_95plus']:.1f}%",
            f"{df.iloc[-1]['pct_95plus']:.1f}%",
        ]
    }
    pd.DataFrame(summary).to_csv(RESULTS_DIR / 'summary.csv', index=False)
    print(f"  Saved: summary.csv")


def print_summary(df: pd.DataFrame):
    """Print analysis summary."""
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)

    change = df.iloc[-1]['mean'] - df.iloc[0]['mean']
    pct_change = df.iloc[-1]['pct_95plus'] - df.iloc[0]['pct_95plus']

    print(f"""
Key Findings:

1. Average 4-seam fastball velocity:
   - 2015: {df.iloc[0]['mean']:.1f} mph
   - 2025: {df.iloc[-1]['mean']:.1f} mph
   - Change: +{change:.1f} mph

2. Percentage of 95+ mph fastballs:
   - 2015: {df.iloc[0]['pct_95plus']:.1f}%
   - 2025: {df.iloc[-1]['pct_95plus']:.1f}%
   - Change: +{pct_change:.1f} percentage points

3. Total pitches analyzed: {df['count'].sum():,}
""")


def main():
    # Run analysis
    velocity_df = analyze_velocity_by_year()

    if len(velocity_df) == 0:
        print("\n[ERROR] No data found. Please collect data first:")
        print("  python collector/collect_statcast.py --range 2015 2025")
        return

    # Create visualizations
    create_visualizations(velocity_df)

    # Save results
    save_results(velocity_df)

    # Print summary
    print_summary(velocity_df)

    print("\n[DONE] Analysis complete!")
    print(f"  Figures: {FIGURES_DIR}")
    print(f"  Results: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
