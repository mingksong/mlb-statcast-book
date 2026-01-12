"""
Constants for Statcast Analysis

Pitch types, team codes, and other reference data.
"""

# Pitch type codes and names
PITCH_TYPES = {
    'FF': '4-Seam Fastball',
    'SI': 'Sinker',
    'FC': 'Cutter',
    'SL': 'Slider',
    'ST': 'Sweeper',
    'CU': 'Curveball',
    'KC': 'Knuckle Curve',
    'CH': 'Changeup',
    'FS': 'Splitter',
    'KN': 'Knuckleball',
    'CS': 'Slow Curve',
    'SV': 'Slurve',
    'FA': 'Fastball (generic)',
    'EP': 'Eephus',
    'SC': 'Screwball',
    'PO': 'Pitchout',
    'IN': 'Intentional Ball',
    'AB': 'Automatic Ball',
}

# Pitch groupings for analysis
PITCH_GROUPS = {
    'fastball': ['FF', 'SI', 'FC', 'FA'],
    'breaking': ['SL', 'ST', 'CU', 'KC', 'CS', 'SV'],
    'offspeed': ['CH', 'FS'],
    'other': ['KN', 'EP', 'SC', 'PO', 'IN', 'AB'],
}

# MLB team codes
MLB_TEAMS = {
    'AZ': 'Arizona Diamondbacks',
    'ATL': 'Atlanta Braves',
    'BAL': 'Baltimore Orioles',
    'BOS': 'Boston Red Sox',
    'CHC': 'Chicago Cubs',
    'CWS': 'Chicago White Sox',
    'CIN': 'Cincinnati Reds',
    'CLE': 'Cleveland Guardians',
    'COL': 'Colorado Rockies',
    'DET': 'Detroit Tigers',
    'HOU': 'Houston Astros',
    'KC': 'Kansas City Royals',
    'LAA': 'Los Angeles Angels',
    'LAD': 'Los Angeles Dodgers',
    'MIA': 'Miami Marlins',
    'MIL': 'Milwaukee Brewers',
    'MIN': 'Minnesota Twins',
    'NYM': 'New York Mets',
    'NYY': 'New York Yankees',
    'OAK': 'Oakland Athletics',
    'PHI': 'Philadelphia Phillies',
    'PIT': 'Pittsburgh Pirates',
    'SD': 'San Diego Padres',
    'SF': 'San Francisco Giants',
    'SEA': 'Seattle Mariners',
    'STL': 'St. Louis Cardinals',
    'TB': 'Tampa Bay Rays',
    'TEX': 'Texas Rangers',
    'TOR': 'Toronto Blue Jays',
    'WSH': 'Washington Nationals',
}

# Outcome descriptions
SWING_OUTCOMES = [
    'swinging_strike',
    'swinging_strike_blocked',
    'foul',
    'foul_tip',
    'hit_into_play',
]

WHIFF_OUTCOMES = [
    'swinging_strike',
    'swinging_strike_blocked',
]

# Zone definitions
# Zones 1-9: Strike zone (3x3 grid)
# Zones 11-14: Outside the zone
IN_ZONE = list(range(1, 10))
OUT_ZONE = [11, 12, 13, 14]
