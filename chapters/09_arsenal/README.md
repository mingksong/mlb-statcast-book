# Chapter 9: Pitcher Arsenal Diversity (2015-2025)

## Research Question

**How has pitcher arsenal diversity evolved, and what pitch types have gained or lost popularity?**

---

## Key Findings

### 1. Arsenal Size Increased Slightly

| Year | Avg Arsenal | 4+ Pitches |
|------|-------------|------------|
| 2015 | 3.98 types | 64.8% |
| 2025 | 4.25 types | 71.7% |
| Change | +0.27 | +6.9% |

### 2. Pitch Type Popularity Shifts

| Pitch | 2015 | 2025 | Change |
|-------|------|------|--------|
| Sweeper (ST) | ~0% | **37.8%** | **New pitch** |
| Cutter (FC) | 25.9% | 39.5% | +13.6% |
| Splitter (FS) | 6.9% | 17.0% | +10.1% |
| Curveball (CU) | 50.9% | 39.5% | -11.4% |
| Changeup (CH) | 68.4% | 58.4% | -10.0% |

### 3. Arsenal Distribution

| Size | % of Pitchers |
|------|---------------|
| 2 types | 9.4% |
| 3 types | 27.5% |
| 4 types | 32.7% |
| 5 types | 23.5% |
| 6+ types | 6.9% |

---

## Statistical Validation

| Test | Value | Interpretation |
|------|-------|----------------|
| Trend slope | +0.021 types/year | Modest increase |
| R² | 0.155 | Weak fit |
| p-value | 0.231 | Not significant |

The trend is positive but not statistically significant at p<0.05.

---

## Files

```
chapters/09_arsenal/
├── README.md
├── analysis.py
├── figures/
│   ├── fig01_arsenal_trend.png
│   ├── fig02_arsenal_distribution.png
│   ├── fig03_multipitch_trend.png
│   └── fig04_pitch_popularity.png
└── results/
    ├── arsenal_by_year.csv
    ├── pitcher_arsenals.csv
    ├── pitch_type_popularity.csv
    ├── statistical_tests.csv
    └── summary.csv
```

---

*Analysis completed: 2025-01-12*
*Pitcher-seasons analyzed: 6,663*
