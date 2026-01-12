"""
Statcast Metrics Module

Functions for calculating common Statcast-based metrics.
"""
import pandas as pd
import numpy as np
from typing import Union

from .constants import SWING_OUTCOMES, WHIFF_OUTCOMES, IN_ZONE, OUT_ZONE


def calculate_barrel(
    exit_velocity: Union[pd.Series, float],
    launch_angle: Union[pd.Series, float]
) -> Union[pd.Series, bool]:
    """
    Determine if a batted ball is a barrel based on exit velocity and launch angle.

    A barrel is defined by MLB as a batted ball with optimal exit velocity
    and launch angle combination for extra-base hits.

    Args:
        exit_velocity: Exit velocity in mph
        launch_angle: Launch angle in degrees

    Returns:
        Boolean (Series or scalar) indicating barrel

    Reference:
        https://www.mlb.com/glossary/statcast/barrel
    """
    ev = exit_velocity
    la = launch_angle

    # Barrel definition:
    # - Exit velocity >= 98 mph
    # - Launch angle in "sweet spot" that expands with higher EV
    is_barrel = (
        (ev >= 98) &
        (la >= 26 - (ev - 98)) &
        (la <= 30 + (ev - 98)) &
        (la >= 8) &
        (la <= 50)
    )

    return is_barrel


def whiff_rate(df: pd.DataFrame) -> float:
    """
    Calculate whiff rate (swinging strikes / swings).

    Args:
        df: DataFrame with 'description' column

    Returns:
        Whiff rate as decimal (0-1)
    """
    swings = df['description'].isin(SWING_OUTCOMES)
    whiffs = df['description'].isin(WHIFF_OUTCOMES)

    swing_count = swings.sum()
    whiff_count = whiffs.sum()

    return whiff_count / swing_count if swing_count > 0 else 0.0


def chase_rate(df: pd.DataFrame) -> float:
    """
    Calculate chase rate (swings at pitches outside zone / pitches outside zone).

    Args:
        df: DataFrame with 'zone' and 'description' columns

    Returns:
        Chase rate as decimal (0-1)
    """
    outside_zone = df['zone'].isin(OUT_ZONE)
    swings = df['description'].isin(SWING_OUTCOMES)

    outside_count = outside_zone.sum()
    chase_count = (outside_zone & swings).sum()

    return chase_count / outside_count if outside_count > 0 else 0.0


def zone_rate(df: pd.DataFrame) -> float:
    """
    Calculate zone rate (pitches in strike zone / total pitches).

    Args:
        df: DataFrame with 'zone' column

    Returns:
        Zone rate as decimal (0-1)
    """
    in_zone = df['zone'].isin(IN_ZONE)
    total = df['zone'].notna()

    return in_zone.sum() / total.sum() if total.sum() > 0 else 0.0


def hard_hit_rate(df: pd.DataFrame, threshold: float = 95.0) -> float:
    """
    Calculate hard hit rate (batted balls >= threshold EV).

    Args:
        df: DataFrame with 'launch_speed' column
        threshold: Exit velocity threshold (default 95 mph)

    Returns:
        Hard hit rate as decimal (0-1)
    """
    batted = df['launch_speed'].notna()
    hard_hit = df['launch_speed'] >= threshold

    batted_count = batted.sum()
    hard_count = hard_hit.sum()

    return hard_count / batted_count if batted_count > 0 else 0.0


def sweet_spot_rate(df: pd.DataFrame, min_angle: float = 8.0, max_angle: float = 32.0) -> float:
    """
    Calculate sweet spot rate (batted balls with optimal launch angle).

    Args:
        df: DataFrame with 'launch_angle' column
        min_angle: Minimum launch angle (default 8 degrees)
        max_angle: Maximum launch angle (default 32 degrees)

    Returns:
        Sweet spot rate as decimal (0-1)
    """
    batted = df['launch_angle'].notna()
    sweet_spot = (df['launch_angle'] >= min_angle) & (df['launch_angle'] <= max_angle)

    batted_count = batted.sum()
    sweet_count = sweet_spot.sum()

    return sweet_count / batted_count if batted_count > 0 else 0.0


def aggregate_pa_results(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate pitch-level data to plate appearance level.

    Uses game_pk + at_bat_number as unique PA identifier.

    Args:
        df: Pitch-level DataFrame

    Returns:
        PA-level DataFrame with final results
    """
    # Create unique PA key
    df = df.copy()
    df['pa_key'] = df['game_pk'].astype(str) + '_' + df['at_bat_number'].astype(str)

    # Aggregate to PA level
    pa_df = df.groupby('pa_key').agg({
        'events': 'last',
        'pitch_number': 'max',
        'batter': 'first',
        'pitcher': 'first',
        'game_pk': 'first',
        'game_year': 'first',
        'home_team': 'first',
        'away_team': 'first',
    }).reset_index()

    # Filter to completed PAs
    pa_df = pa_df[pa_df['events'].notna()]

    return pa_df


def calculate_rate_stats(pa_df: pd.DataFrame) -> dict:
    """
    Calculate K%, BB%, HR% from PA-level data.

    Args:
        pa_df: PA-level DataFrame with 'events' column

    Returns:
        Dictionary with rate statistics
    """
    total_pa = len(pa_df)
    if total_pa == 0:
        return {'k_pct': 0, 'bb_pct': 0, 'hr_pct': 0}

    strikeouts = pa_df['events'].str.contains('strikeout', case=False, na=False).sum()
    walks = pa_df['events'].isin(['walk', 'intent_walk']).sum()
    home_runs = (pa_df['events'] == 'home_run').sum()

    return {
        'k_pct': strikeouts / total_pa * 100,
        'bb_pct': walks / total_pa * 100,
        'hr_pct': home_runs / total_pa * 100,
    }
