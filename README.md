# MLB Statcast Analytics Book

A data-driven exploration of Major League Baseball using Statcast data (2015-2025).

## Overview

This repository contains the complete code and analysis for the book **"MLB Statcast Analytics: A Data-Driven Journey Through Baseball"**. All analyses are fully reproducible using publicly available data from Baseball Savant.

## Data Coverage

- **Period**: 2015-2025 (11 seasons)
- **Pitches**: 7.4+ million
- **Source**: [Baseball Savant](https://baseballsavant.mlb.com) via pybaseball

## Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone https://github.com/mingksong/mlb-statcast-book.git
cd mlb-statcast-book

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Collect Data

```bash
# Collect a single season
python collector/collect_statcast.py --year 2024

# Collect multiple seasons
python collector/collect_statcast.py --range 2015 2025

# List collected data
python collector/collect_statcast.py --list
```

### 3. Run Analysis

Each chapter has its own analysis script:

```bash
cd chapters/01_velocity_trend
python analysis.py
```

## Book Structure

```
Part I: Getting Started
  - Setting Up Your Environment
  - Understanding Statcast Data

Part II: Pitching Analysis (13 chapters)
  - The Velocity Arms Race
  - Pitch Type Evolution
  - Spin Rate Trends
  ...

Part III: Batting Analysis (11 chapters)
  - Exit Velocity Revolution
  - Launch Angle Transformation
  ...

Part IV: Game Strategy (8 chapters)

Part V: League Trends (7 chapters)
```

## Repository Structure

```
mlb-statcast-book/
├── README.md
├── requirements.txt
├── collector/           # Data collection scripts
├── src/                 # Analysis library
│   └── statcast_analysis/
├── chapters/            # Individual chapter analyses
├── book/                # Book content (markdown)
└── scripts/             # Build utilities
```

## Requirements

- Python 3.9+
- pandas, pybaseball, matplotlib, seaborn

## License

MIT License

## Author

[Your Name]

---

*Data source: MLB Statcast via Baseball Savant*
