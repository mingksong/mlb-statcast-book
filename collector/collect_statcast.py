#!/usr/bin/env python3
"""
MLB Statcast Data Collector

Collects pitch-by-pitch Statcast data from Baseball Savant using pybaseball.

Usage:
    python collect_statcast.py --year 2024
    python collect_statcast.py --year 2024 --month 4
    python collect_statcast.py --range 2015 2025
    python collect_statcast.py --list

Data is saved as Parquet files in data/raw/
"""
import argparse
import sys
import warnings
from datetime import datetime
from pathlib import Path

# Suppress FutureWarnings from pybaseball internals
warnings.filterwarnings('ignore', category=FutureWarning)

import pandas as pd
from pybaseball import statcast, cache

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_RAW.mkdir(parents=True, exist_ok=True)

# Enable pybaseball caching
cache.enable()

# Season date ranges (Opening Day to end of regular season)
SEASON_DATES = {
    2025: ('2025-03-27', '2025-09-28'),
    2024: ('2024-03-28', '2024-09-29'),
    2023: ('2023-03-30', '2023-10-01'),
    2022: ('2022-04-07', '2022-10-05'),
    2021: ('2021-04-01', '2021-10-03'),
    2020: ('2020-07-23', '2020-09-27'),  # COVID-shortened season
    2019: ('2019-03-28', '2019-09-29'),
    2018: ('2018-03-29', '2018-10-01'),
    2017: ('2017-04-02', '2017-10-01'),
    2016: ('2016-04-03', '2016-10-02'),
    2015: ('2015-04-05', '2015-10-04'),
}


def collect_season(year: int) -> Path:
    """Collect full season Statcast data."""
    if year not in SEASON_DATES:
        print(f"[ERROR] Unsupported season: {year}")
        print(f"        Supported seasons: {sorted(SEASON_DATES.keys())}")
        sys.exit(1)

    start_dt, end_dt = SEASON_DATES[year]
    filepath = DATA_RAW / f"statcast_{year}.parquet"

    # Check if file already exists
    if filepath.exists():
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"[INFO] File already exists: {filepath} ({size_mb:.1f} MB)")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("[SKIP] Skipping.")
            return filepath

    print(f"\n{'='*60}")
    print(f"  Collecting {year} Season Statcast Data")
    print(f"  Period: {start_dt} to {end_dt}")
    print(f"{'='*60}\n")

    print("[COLLECT] Fetching data... (this may take several minutes)")
    start_time = datetime.now()

    data = statcast(start_dt, end_dt)

    elapsed = (datetime.now() - start_time).total_seconds()

    print(f"\n[DONE] Collection complete!")
    print(f"       - Pitches: {len(data):,}")
    print(f"       - Time: {elapsed:.1f} seconds")

    # Save to parquet
    data.to_parquet(filepath)
    size_mb = filepath.stat().st_size / (1024 * 1024)
    print(f"       - Saved: {filepath.name} ({size_mb:.1f} MB)")

    return filepath


def collect_month(year: int, month: int) -> Path:
    """Collect a specific month of Statcast data."""
    import calendar

    last_day = calendar.monthrange(year, month)[1]
    start_dt = f"{year}-{month:02d}-01"
    end_dt = f"{year}-{month:02d}-{last_day}"

    filepath = DATA_RAW / f"statcast_{year}_{month:02d}.parquet"

    if filepath.exists():
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"[INFO] File already exists: {filepath} ({size_mb:.1f} MB)")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("[SKIP] Skipping.")
            return filepath

    print(f"\n{'='*60}")
    print(f"  Collecting {year}-{month:02d} Statcast Data")
    print(f"  Period: {start_dt} to {end_dt}")
    print(f"{'='*60}\n")

    print("[COLLECT] Fetching data...")
    start_time = datetime.now()

    data = statcast(start_dt, end_dt)

    elapsed = (datetime.now() - start_time).total_seconds()

    print(f"\n[DONE] Collection complete!")
    print(f"       - Pitches: {len(data):,}")
    print(f"       - Time: {elapsed:.1f} seconds")

    data.to_parquet(filepath)
    size_mb = filepath.stat().st_size / (1024 * 1024)
    print(f"       - Saved: {filepath.name} ({size_mb:.1f} MB)")

    return filepath


def collect_range(start_year: int, end_year: int):
    """Collect multiple seasons consecutively."""
    print(f"\n{'='*60}")
    print(f"  Multi-Season Collection: {start_year} to {end_year}")
    print(f"{'='*60}\n")

    total_pitches = 0
    total_size = 0

    for year in range(start_year, end_year + 1):
        if year not in SEASON_DATES:
            print(f"[SKIP] {year} is not supported.")
            continue

        filepath = collect_season(year)

        if filepath.exists():
            df = pd.read_parquet(filepath)
            total_pitches += len(df)
            total_size += filepath.stat().st_size

        print()

    print(f"\n{'='*60}")
    print(f"  Collection Complete!")
    print(f"  - Total pitches: {total_pitches:,}")
    print(f"  - Total size: {total_size / (1024**3):.2f} GB")
    print(f"{'='*60}")


def list_data():
    """List all collected data files."""
    print(f"\n{'='*60}")
    print(f"  Collected Statcast Data")
    print(f"  Location: {DATA_RAW}")
    print(f"{'='*60}\n")

    files = sorted(DATA_RAW.glob("statcast_*.parquet"))

    if not files:
        print("[INFO] No data collected yet.")
        print(f"\n       To collect: python collect_statcast.py --year 2024")
        return

    total_size = 0
    total_pitches = 0

    print(f"{'Filename':<35} {'Pitches':>12} {'Size':>10}")
    print("-" * 60)

    for f in files:
        size_mb = f.stat().st_size / (1024 * 1024)
        total_size += f.stat().st_size

        try:
            df = pd.read_parquet(f)
            pitches = len(df)
            total_pitches += pitches
            print(f"{f.name:<35} {pitches:>12,} {size_mb:>8.1f} MB")
        except Exception as e:
            print(f"{f.name:<35} {'ERROR':>12} {size_mb:>8.1f} MB")

    print("-" * 60)
    print(f"{'TOTAL':<35} {total_pitches:>12,} {total_size/(1024**2):>8.1f} MB")


def main():
    parser = argparse.ArgumentParser(
        description="MLB Statcast Data Collector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python collect_statcast.py --year 2024              # Single season
  python collect_statcast.py --year 2024 --month 4    # Single month
  python collect_statcast.py --range 2020 2024        # Multiple seasons
  python collect_statcast.py --list                   # Show collected data

Supported seasons: 2015-2025
Data saved to: data/raw/
        """
    )

    parser.add_argument("--year", type=int, help="Season year to collect")
    parser.add_argument("--month", type=int, help="Specific month (1-12)")
    parser.add_argument("--range", type=int, nargs=2, metavar=("START", "END"),
                       help="Range of seasons to collect")
    parser.add_argument("--list", action="store_true", help="List collected data")

    args = parser.parse_args()

    if args.list:
        list_data()
    elif args.range:
        collect_range(args.range[0], args.range[1])
    elif args.year and args.month:
        collect_month(args.year, args.month)
    elif args.year:
        collect_season(args.year)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
