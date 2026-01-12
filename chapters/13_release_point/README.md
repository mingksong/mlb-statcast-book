# Chapter 13: Release Point Consistency (2015-2025)

## Research Question

**How consistent are MLB pitchers with their release points, and has this improved over the decade?**

---

## Key Findings

### 1. Release Consistency Improved

| Period | 3D Consistency | Change |
|--------|---------------|--------|
| 2015-2018 | 0.368 inches | baseline |
| 2022-2025 | 0.319 inches | **-13%** |

### 2. Release Height Decreased Significantly

| Year | Release Height |
|------|---------------|
| 2015 | 5.98 ft |
| 2025 | 5.75 ft |
| **Change** | **-2.8 inches** |

### 3. Consistency Has Weak Effect on Effectiveness

| Consistency Quartile | wOBA Allowed |
|---------------------|--------------|
| Best (most consistent) | .327 |
| Good | .324 |
| Fair | .329 |
| Worst (least consistent) | .334 |

---

## Statistical Validation

| Test | Cohen's d | p-value | Interpretation |
|------|-----------|---------|----------------|
| 3D Consistency | 0.380 | <0.001 | Small improvement |
| Release Height | -0.329 | <0.001 | Small decrease |
| Consistency vs wOBA | r=0.059 | 0.010 | Weak positive |

---

## Interpretation

1. **Pitchers are becoming more consistent** - Analytics focus on repeatable mechanics
2. **Release points are dropping** - Part of the "ride" fastball trend (lower release = more perceived rise)
3. **Consistency helps, but marginally** - The best quartile allows .007 less wOBA than worst
4. **Handedness similar** - LHP and RHP have comparable consistency levels

---

## Files

```
chapters/13_release_point/
├── README.md
├── analysis.py
├── figures/
│   ├── fig01_consistency_trend.png
│   ├── fig02_release_height.png
│   ├── fig03_consistency_by_hand.png
│   └── fig04_consistency_vs_woba.png
└── results/
    ├── release_point_by_year.csv
    ├── statistical_tests.csv
    ├── effectiveness_by_consistency.csv
    ├── most_consistent_2025.csv
    └── summary.csv
```

---

*Analysis completed: 2025-01-12*
*Pitcher-seasons analyzed: 6,664*
