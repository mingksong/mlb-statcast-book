# Analysis Writer

Creates analysis.py scripts for MLB Statcast book chapters.

## Trigger

Use when creating or modifying analysis scripts for a chapter.

Keywords: analysis script, write analysis, create analysis.py, python script

## Requirements

All analysis scripts must:

1. **Follow the standard template** (see below)
2. **Use the shared library** (`from statcast_analysis import ...`)
3. **Generate reproducible results** (no random seeds without setting them)
4. **Include progress output** (print statements showing progress)
5. **Save all outputs** (figures to `figures/`, data to `results/`)

## Standard Template

```python
#!/usr/bin/env python3
"""
Chapter XX: [Title]

[Brief description of what this analysis does]

Usage:
    python analysis.py
"""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from statcast_analysis import load_season, load_seasons, AVAILABLE_SEASONS
from statcast_analysis.metrics import whiff_rate, chase_rate, calculate_barrel
from statcast_analysis.constants import PITCH_TYPES, PITCH_GROUPS

# Output directories
FIGURES_DIR = Path(__file__).parent / "figures"
RESULTS_DIR = Path(__file__).parent / "results"
FIGURES_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# Plot configuration
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['font.size'] = 11


def load_data():
    """Load and prepare data for analysis."""
    print("\n[1] Loading data...")
    # Implementation here
    pass


def analyze_[metric](df: pd.DataFrame) -> pd.DataFrame:
    """Calculate [metric] statistics."""
    print("\n[2] Analyzing [metric]...")
    # Implementation here
    pass


def create_visualizations(df: pd.DataFrame):
    """Generate all chapter visualizations."""
    print("\n[3] Creating visualizations...")

    # Figure 1: [Description]
    fig, ax = plt.subplots(figsize=(10, 6))
    # ... plotting code ...
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'fig01_[name].png')
    plt.close()
    print("  Saved: fig01_[name].png")

    # Figure 2: [Description]
    # ... etc ...


def save_results(df: pd.DataFrame):
    """Save analysis results to CSV."""
    print("\n[4] Saving results...")
    df.to_csv(RESULTS_DIR / '[name].csv', index=False)
    print("  Saved: [name].csv")


def print_summary(df: pd.DataFrame):
    """Print analysis summary."""
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)
    print(f"""
Key Findings:

1. [Finding 1]
2. [Finding 2]
3. [Finding 3]
""")


def main():
    print("=" * 60)
    print("  Chapter XX: [Title]")
    print("=" * 60)

    # Run analysis pipeline
    df = load_data()
    results = analyze_[metric](df)
    create_visualizations(results)
    save_results(results)
    print_summary(results)

    print("\n[DONE] Analysis complete!")
    print(f"  Figures: {FIGURES_DIR}")
    print(f"  Results: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
```

## Code Standards

### Data Loading

```python
# Single season
df = load_season(2024, columns=['pitch_type', 'release_speed'])

# Multiple seasons
df = load_seasons(range(2020, 2026), columns=['pitch_type', 'release_speed'])

# All available seasons
df = load_seasons(AVAILABLE_SEASONS, columns=['pitch_type', 'release_speed'])
```

### Filtering Pitch Types

```python
from statcast_analysis.constants import PITCH_TYPES, PITCH_GROUPS

# Single pitch type
ff = df[df['pitch_type'] == 'FF']

# Pitch group
fastballs = df[df['pitch_type'].isin(PITCH_GROUPS['fastball'])]
```

### Metric Calculations

```python
from statcast_analysis.metrics import (
    whiff_rate,
    chase_rate,
    zone_rate,
    hard_hit_rate,
    calculate_barrel,
    aggregate_pa_results,
    calculate_rate_stats,
)

# Pitch-level metrics
whiff = whiff_rate(pitch_df)
chase = chase_rate(pitch_df)

# Batted ball metrics
df['is_barrel'] = calculate_barrel(df['launch_speed'], df['launch_angle'])

# PA-level aggregation
pa_df = aggregate_pa_results(pitch_df)
rates = calculate_rate_stats(pa_df)  # Returns K%, BB%, HR%
```

### Visualization Standards

- Figure size: `(10, 6)` for standard, `(12, 8)` for complex
- DPI: 150 for saved figures
- Always include: title, axis labels, legend (if multiple series)
- Use `plt.tight_layout()` before saving
- Close figures after saving: `plt.close()`

### File Naming

- Figures: `fig01_description.png`, `fig02_description.png`
- Results: `descriptive_name.csv`
- Use lowercase with underscores

## Common Patterns

### Year-over-year trend analysis

```python
results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['pitch_type', 'release_speed'])
    ff = df[df['pitch_type'] == 'FF']['release_speed'].dropna()
    results.append({
        'year': year,
        'count': len(ff),
        'mean': ff.mean(),
        'median': ff.median(),
    })
trend_df = pd.DataFrame(results)
```

### Pitcher/Batter aggregation

```python
# Group by pitcher
pitcher_stats = df.groupby('pitcher').agg({
    'release_speed': 'mean',
    'release_spin_rate': 'mean',
    'pitch_type': 'count'
}).rename(columns={'pitch_type': 'pitch_count'})

# Filter to qualified pitchers (min 500 pitches)
qualified = pitcher_stats[pitcher_stats['pitch_count'] >= 500]
```
