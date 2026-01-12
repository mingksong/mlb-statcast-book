# MLB Statcast Analytics Book

## Project Overview

A data-driven book about MLB baseball using Statcast data (2015-2025).

- **Repository**: https://github.com/mingksong/mlb-statcast-book
- **Language**: English (all code, comments, and documentation)
- **Target**: Amazon PDF publication
- **Chapters**: 40 research topics across 5 parts

---

## Quick Start: Research Command

**To start a chapter research**:
```
start chapter N research
```

Example: `start chapter 3 research` → Executes Pitch Type Evolution analysis

This triggers **Research Orchestrator 2.0** which executes:
1. PLAN → Research design
2. EXTRACT → Data loading
3. DESCRIBE → Descriptive statistics
4. ANALYZE → Statistical tests (t-test, effect size, CI)
5. VISUALIZE → Publication-ready figures
6. DOCUMENT → README + book chapter

---

## Research Plan

**Reference**: `RESEARCH_PLAN.md` contains all chapter topics with:
- Chapter number and title
- Status (DONE/GO/PARTIAL)
- Required data columns
- Part assignment

### Chapter Status

| Part | Chapters | Status |
|------|----------|--------|
| II: Pitching | 02-14 | 02 DONE, rest GO |
| III: Batting | 15-25 | All GO (25 PARTIAL) |
| IV: Game Mgmt | 26-33 | All GO |
| V: League Trends | 34-40 | All GO |

---

## Data Access

```python
from statcast_analysis import load_season, load_seasons, AVAILABLE_SEASONS

# Single season
df = load_season(2024, columns=['pitch_type', 'release_speed'])

# Multiple seasons
df = load_seasons(range(2020, 2026))

# All seasons (2015-2025, 7.4M+ pitches)
df = load_seasons(AVAILABLE_SEASONS)
```

**Data location**: `data/raw/statcast_YYYY.parquet`

**PA-level aggregation**: `PA_KEY = game_pk + at_bat_number`

---

## Available Skills

### Research Pipeline

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `chapter-orchestrator` | "start chapter N research" | **Research Orchestrator 2.0** - Full 6-phase pipeline |
| `analysis-writer` | "create analysis script" | analysis.py templates |
| `figure-generator` | "create figure" | Visualization standards |
| `code-validator` | "validate code" | Reproducibility testing |

### Report Generation Pipeline

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `chapter-docs` | "write documentation" | Orchestrates report pipeline |
| `report-content-organizer` | Phase 1 | Structure report, extract actual values |
| `report-code-extractor` | Phase 2 | Extract clean, executable code blocks |
| `report-converter` | Phase 3 | Generate final ABDWR markdown |

### Report Pipeline Flow

```
PREREQUISITE: analysis.py executed, results + figures generated

Phase 1: CONTENT ORGANIZER
├── Read results/*.csv for actual values
├── Inventory figures/*.png
├── Define section structure
└── Mark code insertion points

Phase 2: CODE EXTRACTOR
├── Parse analysis.py
├── Extract relevant code blocks
├── Remove debug (print statements)
└── Add explanatory comments

Phase 3: REPORT CONVERTER
├── Merge content + code
├── Insert actual values
├── Generate markdown tables
└── Apply ABDWR style
```

---

## Project Structure

```
mlb-statcast-book/
├── RESEARCH_PLAN.md        # Chapter topics & status
├── chapters/               # Individual analyses
│   ├── 02_velocity_trend/  # [DONE]
│   ├── 03_pitch_type/      # [PENDING]
│   └── ...
├── book/                   # Book content (markdown)
├── src/statcast_analysis/  # Shared library
├── collector/              # Data collection
└── scripts/                # Build & validation
```

---

## Statistical Requirements

Each chapter must include:

1. **Descriptive stats**: n, mean, std, median, percentiles
2. **Trend analysis**: Linear regression with R², p-value
3. **Effect size**: Cohen's d with interpretation
4. **Confidence intervals**: 95% CI for key metrics
5. **Significance tests**: t-test for period comparisons

### Interpretation Guidelines

| Metric | Weak | Moderate | Strong |
|--------|------|----------|--------|
| R² | <0.1 | 0.1-0.3 | >0.3 |
| Cohen's d | <0.2 | 0.2-0.8 | >0.8 |
| p-value | >0.05 | 0.01-0.05 | <0.01 |

---

## Common Statcast Columns

| Category | Columns |
|----------|---------|
| Pitch | pitch_type, release_speed, release_spin_rate |
| Movement | pfx_x, pfx_z |
| Location | plate_x, plate_z, zone |
| Batted ball | launch_speed, launch_angle |
| Identifiers | pitcher, batter, game_pk, at_bat_number |
| Game context | game_year, inning, balls, strikes, outs_when_up |

---

## Pitch Type Codes

| Code | Type | Group |
|------|------|-------|
| FF | 4-Seam Fastball | Fastball |
| SI | Sinker | Fastball |
| FC | Cutter | Fastball |
| SL | Slider | Breaking |
| ST | Sweeper | Breaking |
| CU | Curveball | Breaking |
| CH | Changeup | Offspeed |
| FS | Splitter | Offspeed |

---

*Research Orchestrator 2.0 - Statistical rigor meets baseball analytics*
*Last updated: 2025-01-12*
