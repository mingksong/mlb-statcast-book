"""
Statcast Analysis Library

A collection of utilities for analyzing MLB Statcast data.
"""
from .data_loader import (
    load_season,
    load_seasons,
    load_all,
    AVAILABLE_SEASONS,
)

from .constants import (
    PITCH_TYPES,
    PITCH_GROUPS,
    MLB_TEAMS,
)

from .metrics import (
    calculate_barrel,
    whiff_rate,
    chase_rate,
    zone_rate,
    hard_hit_rate,
    sweet_spot_rate,
)

__all__ = [
    # Data loading
    'load_season', 'load_seasons', 'load_all', 'AVAILABLE_SEASONS',
    # Constants
    'PITCH_TYPES', 'PITCH_GROUPS', 'MLB_TEAMS',
    # Metrics
    'calculate_barrel', 'whiff_rate', 'chase_rate', 'zone_rate',
    'hard_hit_rate', 'sweet_spot_rate',
]
