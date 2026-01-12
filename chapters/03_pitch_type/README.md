# Chapter 3: Pitch Type Evolution (2015-2025)

## Summary

This chapter analyzes the 10-year evolution of pitch type usage in MLB, documenting the dramatic shift from fastball-dominant pitching to a more diverse, breaking-ball-heavy approach. The emergence of the sweeper as a distinct pitch category represents one of the most significant developments in modern pitching.

## Key Findings

### 1. Four-Seam Fastball Decline

The traditional workhorse pitch has seen **statistically significant decline**:

| Metric | Value |
|--------|-------|
| 2015 usage | 35.6% |
| 2025 usage | 31.9% |
| Change | **-3.7 percentage points** |
| Trend | -0.44%/year |
| R² | 0.718 (strong) |
| p-value | <0.001 (highly significant) |

### 2. Sweeper Emergence

The sweeper (ST) has emerged as a **revolutionary new pitch category**:

| Year | Usage | Growth |
|------|-------|--------|
| 2015 | 0.1% | - |
| 2018 | 0.7% | First meaningful adoption |
| 2021 | 2.0% | Rapid acceleration begins |
| 2025 | **7.0%** | Now 7th most common pitch |

- **Growth rate**: +1.07%/year since emergence (R²=0.936)
- **Effect size**: Cohen's h = 0.41 (small-medium effect)
- Fastest-growing pitch type in Statcast era

### 3. Sinker Decline

The sinker has seen the **largest absolute decline**:

| Metric | Value |
|--------|-------|
| 2015 usage | 21.3% |
| 2025 usage | 15.5% |
| Change | **-5.8 percentage points** |
| Trend | -0.65%/year |
| R² | 0.739 (strong) |

### 4. Category Shift: Fastball vs Breaking

| Category | 2015 | 2025 | Change |
|----------|------|------|--------|
| Fastball | 62.6% | 55.0% | -7.6% |
| Breaking | 21.9% | 28.8% | +6.9% |
| Offspeed | 12.1% | 13.6% | +1.5% |

### 5. Winners and Losers

**Increasing (Statistically Significant)**:
| Pitch | Trend | p-value |
|-------|-------|---------|
| Sweeper | +0.77%/year | <0.001 |
| Cutter | +0.29%/year | <0.001 |
| Splitter | +0.16%/year | 0.004 |

**Decreasing (Statistically Significant)**:
| Pitch | Trend | p-value |
|-------|-------|---------|
| Sinker | -0.65%/year | <0.001 |
| 4-Seam | -0.44%/year | <0.001 |
| Curveball | -0.15%/year | 0.014 |

## Statistical Validation

### Trend Analysis (Linear Regression)

All major findings pass statistical validation:

| Pitch Type | Slope | 95% CI | R² | Interpretation |
|------------|-------|--------|----|----|
| 4-Seam Fastball | -0.44%/year | [-0.62, -0.26] | 0.72 | Strong decline |
| Sinker | -0.65%/year | [-0.91, -0.40] | 0.74 | Strong decline |
| Sweeper | +0.77%/year | [+0.58, +0.96] | 0.87 | Strong growth |
| Cutter | +0.29%/year | [+0.22, +0.35] | 0.89 | Strong growth |

### Period Comparison (2015-17 vs 2023-25)

Effect sizes calculated using Cohen's h for proportion differences:

| Pitch Type | Early | Late | Effect Size |
|------------|-------|------|-------------|
| Sweeper | 0.3% | 6.6% | h=0.41 (small) |
| Sinker | 20.8% | 15.6% | h=-0.14 (negligible) |
| 4-Seam | 35.5% | 31.9% | h=-0.07 (negligible) |

## Methodology

1. Loaded pitch-level data for all 11 seasons (2015-2025)
2. Calculated yearly pitch type distributions (n=7,396,832 pitches)
3. Grouped pitches into categories: Fastball, Breaking, Offspeed
4. Performed linear regression for trend analysis
5. Compared early (2015-17) vs late (2023-25) periods
6. Calculated effect sizes using Cohen's h for proportions

## Files

| File | Description |
|------|-------------|
| `analysis.py` | Main analysis script |
| `figures/fig01_pitch_type_evolution.png` | Stacked area chart of all pitch types |
| `figures/fig02_sweeper_emergence.png` | Sweeper adoption timeline |
| `figures/fig03_fastball_decline.png` | 4-seam fastball trend |
| `figures/fig04_pitch_categories.png` | Category balance over time |
| `figures/fig05_period_comparison.png` | Early vs late era comparison |
| `results/pitch_type_by_year.csv` | Raw pitch type counts by year |
| `results/trend_analysis.csv` | Linear regression results |
| `results/period_comparison.csv` | Period comparison statistics |

## Running the Analysis

```bash
cd chapters/03_pitch_type
python analysis.py
```

## Data Requirements

- Requires: `data/raw/statcast_2015.parquet` through `statcast_2025.parquet`
- Key column: `pitch_type`
- Total pitches analyzed: 7,396,832

## Interpretation

The data reveals a fundamental shift in pitching philosophy:

1. **Decline of "pure" fastballs**: Both 4-seam fastballs and sinkers have declined significantly as pitchers move toward more movement-focused approaches.

2. **Rise of hybrid pitches**: The cutter (+2.4%) and sweeper (+6.3%) represent the modern preference for pitches that combine velocity with significant horizontal movement.

3. **Sweeper revolution**: The sweeper's emergence from obscurity (<0.1% in 2015) to mainstream (7.0% in 2025) mirrors the success pitchers have had using horizontal movement to induce weak contact.

4. **Breaking ball dominance**: Breaking balls now comprise nearly 29% of all pitches, up from 22% in 2015, reflecting improved pitch design and analytical understanding.
