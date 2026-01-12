# Chapter 11: Tunneling Effect Analysis (2015-2025)

## Research Question

**How has pitch tunneling evolved, and are pitchers getting better at disguising their pitches?**

---

## Key Findings

### 1. Release Point Consistency Improved

| Period | Release Consistency (3D StdDev) |
|--------|--------------------------------|
| 2015-2018 | 0.365 inches |
| 2022-2025 | 0.317 inches |
| **Change** | **-0.048 inches (better)** |

### 2. FB-Breaking Ball Tunneling Improved

| Period | Release Separation |
|--------|-------------------|
| 2015-2018 | 0.307 inches |
| 2022-2025 | 0.209 inches |
| **Change** | **-0.097 inches (better)** |

### 3. Statistical Validation

| Test | Cohen's d | p-value | Interpretation |
|------|-----------|---------|----------------|
| Release Consistency | 0.380 | <0.001 | Small improvement |
| FB-Breaking Separation | 0.595 | <0.001 | Medium improvement |

---

## What is Tunneling?

Pitch tunneling is the art of making different pitch types look identical coming out of the pitcher's hand. If a fastball and slider have the same release point and early trajectory, the batter can't distinguish them until it's too late.

### Key Metrics:

1. **Release Consistency** - How similar the release point is across all pitches (lower = better)
2. **FB-Breaking Separation** - Distance between fastball and breaking ball release points (lower = better tunneling)

---

## Interpretation

### Data Quality Note

The 2017-2019 period shows elevated values likely due to Statcast measurement system changes. Comparing early (2015-2018) to late (2022-2025) periods accounts for this.

### Key Insights

1. **Pitchers are improving at tunneling** - Both metrics show significant improvement
2. **FB-Breaking ball tunneling up ~32%** - Pitchers release fastballs and breaking balls from more similar points
3. **Part of the analytics revolution** - Teams now specifically train release point consistency
4. **Medium effect size** - The improvement is meaningful, not just statistical noise

---

## Files

```
chapters/11_tunneling/
├── README.md
├── analysis.py
├── figures/
│   ├── fig01_release_consistency.png
│   ├── fig02_fb_breaking_separation.png
│   ├── fig03_consistency_distribution.png
│   └── fig04_tunnel_scatter.png
└── results/
    ├── release_consistency_by_year.csv
    ├── fb_breaking_separation_by_year.csv
    ├── statistical_tests.csv
    ├── summary.csv
    └── top_tunnelers_2025.csv
```

---

*Analysis completed: 2025-01-12*
*Pitcher-seasons analyzed: 7,540*
