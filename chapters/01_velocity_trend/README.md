# Chapter 2: The Velocity Arms Race (2015-2025)

## Research Question

**Has MLB fastball velocity significantly increased over the past decade, and if so, what is the magnitude of this change?**

### Hypotheses
- **H0**: No significant change in average fastball velocity (slope = 0)
- **H1**: Significant increase in average fastball velocity (slope > 0)

---

## Key Findings

### 1. Velocity Trend
- **2015**: 93.12 mph (95% CI: [93.11, 93.13])
- **2025**: 94.49 mph (95% CI: [94.48, 94.51])
- **10-Year Change**: +1.37 mph

### 2. Elite Velocity (95+ mph)
- **2015**: 26.1% of 4-seamers
- **2025**: 43.1% of 4-seamers
- **Change**: +17.1 percentage points

### 3. Trend Acceleration
- **2015-2020**: Gradual increase (+0.24 mph over 5 years)
- **2021-2025**: Rapid increase (+0.79 mph over 4 years)
- **Inflection point**: 2021 season

---

## Statistical Validation

| Test | Metric | Value | Interpretation |
|------|--------|-------|----------------|
| Trend Analysis | Slope | 0.144 mph/year | Significant upward trend |
| Trend Analysis | Slope 95% CI | [0.113, 0.174] | Excludes zero |
| Trend Analysis | R² | 0.905 | Strong fit |
| Trend Analysis | p-value | 6.92e-06 | Highly significant |
| Period Comparison | Difference | 1.12 mph | Early vs Late |
| Period Comparison | 95% CI | [1.12, 1.13] | Excludes zero |
| Period Comparison | Cohen's d | 0.422 | Small effect |
| Period Comparison | p-value | <0.001 | Highly significant |

### Interpretation
- The velocity increase is **statistically significant** (p < 0.001)
- The **R² of 0.905** indicates the linear trend explains 90.5% of year-to-year variance
- **Cohen's d = 0.422** represents a small-to-medium practical effect
- The **positive slope (0.144 mph/year)** confirms sustained velocity increase

---

## Methodology

1. **Data**: All 4-seam fastballs (pitch_type == 'FF') from 2015-2025
2. **Sample size**: 2,534,067 pitches across 11 seasons
3. **Trend analysis**: Linear regression on yearly means
4. **Period comparison**: Two-sample t-test comparing 2015-2017 vs 2023-2025
5. **Effect size**: Cohen's d for practical significance

### Period Definitions
- **Early period**: 2015, 2016, 2017 (n = 756,871)
- **Late period**: 2023, 2024, 2025 (n = 681,779)

---

## Files

| File | Description |
|------|-------------|
| `analysis.py` | Main analysis script with statistical tests |
| `figures/fig01_velocity_trend.png` | Trend with 95% CI and regression line |
| `figures/fig02_95plus_percentage.png` | Elite velocity growth |
| `figures/fig03_distribution_comparison.png` | 2015 vs 2025 distribution |
| `results/velocity_by_year.csv` | Yearly statistics with CI |
| `results/statistical_tests.csv` | All statistical test results |
| `results/summary.csv` | Key findings summary |

---

## Running the Analysis

```bash
cd chapters/01_velocity_trend
python analysis.py
```

### Requirements
- Data: `data/raw/statcast_2015.parquet` through `statcast_2025.parquet`
- Dependencies: pandas, numpy, scipy, matplotlib, seaborn

---

## Reproducibility

The analysis is fully reproducible:
```bash
python analysis.py  # Run 1
md5sum results/*.csv > /tmp/run1.md5
python analysis.py  # Run 2
md5sum results/*.csv > /tmp/run2.md5
diff /tmp/run1.md5 /tmp/run2.md5  # Should be empty
```

---

*Research Orchestrator 2.0 - Statistical rigor meets baseball analytics*
