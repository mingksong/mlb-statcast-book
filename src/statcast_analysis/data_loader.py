"""
Data Loader Module

Functions for loading Statcast parquet files.
"""
from pathlib import Path
from typing import List, Optional

import pandas as pd

# Project root (relative to this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"

# Available seasons in the dataset
AVAILABLE_SEASONS = list(range(2015, 2026))


def load_season(
    year: int,
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Load a single season of Statcast data.

    Args:
        year: Season year (2015-2025)
        columns: Optional list of columns to load (for memory efficiency)

    Returns:
        DataFrame with pitch-by-pitch data

    Example:
        >>> df = load_season(2024)
        >>> df = load_season(2024, columns=['pitch_type', 'release_speed'])
    """
    filepath = DATA_RAW / f"statcast_{year}.parquet"

    if not filepath.exists():
        raise FileNotFoundError(
            f"Data file not found: {filepath}\n"
            f"Run: python collector/collect_statcast.py --year {year}"
        )

    if columns:
        return pd.read_parquet(filepath, columns=columns)
    return pd.read_parquet(filepath)


def load_seasons(
    start_year: int,
    end_year: int,
    columns: Optional[List[str]] = None,
    verbose: bool = False
) -> pd.DataFrame:
    """
    Load multiple seasons of Statcast data.

    Args:
        start_year: First season to load
        end_year: Last season to load (inclusive)
        columns: Optional list of columns to load
        verbose: Print progress if True

    Returns:
        DataFrame with combined data from all seasons

    Example:
        >>> df = load_seasons(2020, 2024)
        >>> df = load_seasons(2015, 2025, columns=['pitch_type', 'release_speed'], verbose=True)
    """
    dfs = []

    for year in range(start_year, end_year + 1):
        if verbose:
            print(f"Loading {year}...", end=" ")

        try:
            df = load_season(year, columns=columns)
            dfs.append(df)
            if verbose:
                print(f"{len(df):,} pitches")
        except FileNotFoundError:
            if verbose:
                print("not found, skipping")
            continue

    if not dfs:
        raise FileNotFoundError(
            f"No data found for years {start_year}-{end_year}\n"
            f"Run: python collector/collect_statcast.py --range {start_year} {end_year}"
        )

    combined = pd.concat(dfs, ignore_index=True)

    if verbose:
        print(f"Total: {len(combined):,} pitches")

    return combined


def load_all(
    columns: Optional[List[str]] = None,
    verbose: bool = False
) -> pd.DataFrame:
    """
    Load all available Statcast data.

    Args:
        columns: Optional list of columns to load
        verbose: Print progress if True

    Returns:
        DataFrame with all available data
    """
    return load_seasons(
        min(AVAILABLE_SEASONS),
        max(AVAILABLE_SEASONS),
        columns=columns,
        verbose=verbose
    )
