# Chapter 15: Exit Velocity Revolution (2015-2025)

## Research Question

**How has exit velocity evolved over the Statcast era?**

---

## Key Findings

### 1. Exit Velocity Declined (with caveats)

| Year | Mean EV | Hard Hit Rate |
|------|---------|---------------|
| 2015 | 87.1 mph | 31.8% |
| 2025 | 83.1 mph | 25.5% |

### 2. Data Quality Note

The 2015 data shows significantly higher values than subsequent years. This is likely due to **Statcast calibration changes** rather than a real decline in hitting power. From 2016 onward, values are more consistent (82-84 mph range).

### 3. Statistical Summary

| Test | Value | Interpretation |
|------|-------|----------------|
| Trend slope | -0.26 mph/year | Slight decline |
| R² | 0.367 | Moderate fit |
| p-value | 0.048 | Marginally significant |
| Cohen's d | -0.093 | Negligible effect |

---

## Interpretation

1. **2015 data anomaly**: First year of Statcast likely had different calibration
2. **Stable since 2016**: Exit velocity has been remarkably consistent (82-84 mph)
3. **Hard hit rate stable**: ~24-26% of batted balls hit 95+ mph
4. **No "power revolution" in EV**: The launch angle shift (Ch 16) drove HR increases, not harder contact

---

## Files

```
chapters/15_exit_velocity/
├── README.md
├── analysis.py
├── figures/
│   ├── fig01_ev_trend.png
│   ├── fig02_hard_hit_rate.png
│   ├── fig03_ev_distribution.png
│   └── fig04_ev_percentiles.png
└── results/
    ├── exit_velocity_by_year.csv
    ├── hard_hit_rate_by_year.csv
    ├── elite_ev_by_year.csv
    ├── statistical_tests.csv
    └── summary.csv
```

---

*Analysis completed: 2025-01-12*
*Batted balls analyzed: 2,198,577*
