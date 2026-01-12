# MLB Statcast Analytics Book

## Project Overview

A data-driven book about MLB baseball using Statcast data (2015-2025).

- **Repository**: https://github.com/mingksong/mlb-statcast-book
- **Language**: English (all code, comments, and documentation)
- **Target**: Amazon PDF publication

## Data Access

```python
# Load from parquet files
from statcast_analysis import load_season, load_seasons, AVAILABLE_SEASONS

# Single season
df = load_season(2024, columns=['pitch_type', 'release_speed'])

# Multiple seasons
df = load_seasons(range(2020, 2026))

# Available: 2015-2025 (11 seasons, 7.4M+ pitches)
```

**Data location**: `data/raw/statcast_YYYY.parquet`

## Key Modules

| Module | Purpose |
|--------|---------|
| `src/statcast_analysis/` | Shared analysis library |
| `collector/` | Data collection via pybaseball |
| `chapters/` | Individual chapter analyses |
| `book/` | Final book content (markdown) |
| `scripts/` | Build and validation tools |

## Chapter Workflow

```
1. Create chapter: chapters/XX_topic/
2. Write analysis.py (use template)
3. Run analysis, generate figures
4. Write README.md (GitHub)
5. Write book chapter (book/partX/chXX.md)
6. Validate: python scripts/validate_code.py
```

## Available Skills

| Skill | Purpose |
|-------|---------|
| `chapter-orchestrator` | Full chapter creation pipeline |
| `analysis-writer` | Create analysis.py scripts |
| `figure-generator` | Create visualizations |
| `chapter-docs` | Write documentation |
| `code-validator` | Test code reproducibility |

## Code Standards

- All comments and docstrings in English
- Use `statcast_analysis` library for data loading
- Save figures to `figures/` at 150 DPI
- Save results to `results/` as CSV
- Follow the analysis.py template structure

## Common Statcast Columns

**Pitch data**: pitch_type, release_speed, release_spin_rate, spin_axis
**Movement**: pfx_x, pfx_z (horizontal/vertical break)
**Location**: plate_x, plate_z, zone
**Batted ball**: launch_speed, launch_angle, hit_distance_sc
**Identifiers**: pitcher, batter, game_pk, at_bat_number, game_year

## Pitch Type Codes

| Code | Type |
|------|------|
| FF | 4-Seam Fastball |
| SI | Sinker |
| FC | Cutter |
| SL | Slider |
| ST | Sweeper |
| CU | Curveball |
| CH | Changeup |
| FS | Splitter |

---

*Last updated: 2025-01-12*
