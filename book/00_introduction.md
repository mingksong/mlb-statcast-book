# Introduction

## About This Book

This book takes you on a data-driven journey through Major League Baseball using Statcast, MLB's revolutionary pitch-tracking technology. Since its full deployment in 2015, Statcast has transformed how we understand baseball, providing unprecedented insight into every pitch, swing, and batted ball.

## What You'll Learn

Over 45 chapters, we'll explore:

- **Pitching Evolution**: How velocity, spin rates, and pitch mix have changed
- **Batting Revolution**: The launch angle and exit velocity transformation
- **Game Strategy**: Modern bullpen usage and in-game decision making
- **League Trends**: The broader patterns shaping today's game

## How to Use This Book

Each chapter stands alone, so you can read them in any order. Every analysis includes:

1. **Key Findings**: The main insights in brief
2. **The Story**: Context and narrative explanation
3. **The Analysis**: Code and methodology
4. **Visualizations**: Charts that illustrate the findings
5. **Try It Yourself**: Links to full code on GitHub

## Reproducibility

All analyses in this book are fully reproducible. The complete code is available at:

```
https://github.com/mingksong/mlb-statcast-book
```

To run the analyses yourself:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Collect data: `python collector/collect_statcast.py --range 2015 2025`
4. Run any chapter: `python chapters/XX_topic/analysis.py`

## Data Source

All data comes from [Baseball Savant](https://baseballsavant.mlb.com), MLB's official Statcast data portal. We use the excellent [pybaseball](https://github.com/jldbc/pybaseball) library for data collection.

## Prerequisites

This book assumes basic familiarity with:
- Baseball terminology
- Python programming (for running the code)
- Basic statistics

No advanced statistics or machine learning knowledge is required.

---

*Let's dive into the data and discover what makes modern baseball tick.*
