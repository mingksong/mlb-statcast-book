# Chapter 7: Count-Based Pitch Selection (2015-2025)

## Research Question

**How does pitch selection change based on the count, and have these strategies evolved over time?**

---

## Key Findings

### 1. Massive Fastball Shift by Count Type

| Count Type | Fastball % | Breaking % | Difference |
|------------|-----------|------------|------------|
| Pitcher's Counts (0-1, 0-2, 1-2) | 50.4% | 34.3% | Baseline |
| Hitter's Counts (1-0, 2-0, 3-0, 3-1) | 67.4% | 19.5% | **+17% FB** |

### 2. Extreme Counts Show Extreme Strategies

| Count | Fastball % | Context |
|-------|-----------|---------|
| 3-0 | **93.0%** | Almost exclusively fastballs |
| 0-2 | **48.2%** | More breaking balls than fastballs |
| 2-0 | 74.4% | Strong fastball bias |

### 3. Two-Strike Strategy

- Breaking ball usage **increases by 7.6%** with two strikes
- Two-strike breaking%: 33.6% vs 26.0% in other counts

### 4. Evolution Over Time

| Metric | 2015 | 2025 | Change |
|--------|------|------|--------|
| First Pitch (0-0) FB% | 67.5% | 60.3% | **-7.2%** |
| 3-0 Count FB% | 85.1% | 93.6% | **+8.5%** |
| Two-Strike Breaking% | 31.1% | 35.2% | +4.1% |

---

## Statistical Validation

| Test | Statistic | Value | Interpretation |
|------|-----------|-------|----------------|
| Count Type Comparison | Chi-square | 109,187 | Highly significant |
| Count Type Comparison | p-value | <0.001 | Reject H0 |
| Count Type Comparison | Cramer's V | 0.170 | Small-medium effect |
| First Pitch Trend | Slope | -0.77%/year | Significant decline |
| First Pitch Trend | R² | 0.863 | Strong fit |

---

## Files

```
chapters/07_count_strategy/
├── README.md
├── analysis.py
├── figures/
│   ├── fig01_fastball_by_count.png
│   ├── fig02_pitcher_vs_hitter_counts.png
│   ├── fig03_two_strike_strategy.png
│   ├── fig04_yearly_trends.png
│   └── fig05_count_ranking.png
└── results/
    ├── pitch_mix_by_count.csv
    ├── yearly_trends.csv
    ├── statistical_tests.csv
    └── summary.csv
```

---

## Reproducibility

```bash
python chapters/07_count_strategy/analysis.py
```

---

*Analysis completed: 2025-01-12*
*Total pitches analyzed: 7,396,806*
