# Chapter 12: Pitch Effectiveness by Type (2015-2025)

## Research Question

**Which pitch types are most effective, and how has effectiveness evolved over the decade?**

---

## Key Findings

### 1. Most Effective Pitches in 2025

| Pitch | wOBA Against | Whiff Rate |
|-------|--------------|------------|
| Splitter (FS) | 0.267 | 32.6% |
| Sweeper (ST) | 0.283 | 30.0% |
| Knuckle Curve (KC) | 0.288 | 35.0% |

### 2. Category Effectiveness (wOBA Against)

| Category | 2015 | 2025 | Change |
|----------|------|------|--------|
| Fastball | .350 | .348 | -0.003 |
| Breaking | .267 | .294 | +0.027 |
| Offspeed | .297 | .283 | -0.015 |

### 3. Whiff Rate Trends

| Category | 2015 | 2025 | Change |
|----------|------|------|--------|
| Fastball | 15.0% | 17.0% | +2.0% |
| Breaking | 31.8% | 30.9% | -1.0% |
| Offspeed | 29.8% | 30.1% | +0.3% |

---

## Interpretation

1. **Breaking balls remain most effective** - Lowest wOBA despite slight decline
2. **Fastball whiff rate improved** - Up 2% over the decade
3. **Splitter emerged as elite** - Lowest wOBA of any pitch type
4. **Sweeper is highly effective** - New pitch already among the best
5. **Changes are modest** - Effect sizes are negligible; pitching effectiveness stable

---

## Statistical Validation

| Category | wOBA Change | Cohen's d | Interpretation |
|----------|-------------|-----------|----------------|
| Fastball | -0.008 | -0.055 | Negligible |
| Breaking | +0.015 | +0.097 | Negligible |
| Offspeed | -0.014 | -0.096 | Negligible |

Despite changes being statistically detectable with 7M+ pitches, the practical effect is minimal.

---

## Files

```
chapters/12_pitch_effectiveness/
├── README.md
├── analysis.py
├── figures/
│   ├── fig01_woba_by_category.png
│   ├── fig02_whiff_by_category.png
│   ├── fig03_woba_by_pitch_type.png
│   └── fig04_whiff_by_pitch_type.png
└── results/
    ├── effectiveness_by_pitch_year.csv
    ├── effectiveness_by_category.csv
    ├── pitch_type_trends.csv
    ├── statistical_tests.csv
    └── summary.csv
```

---

*Analysis completed: 2025-01-12*
*Total pitches analyzed: 7,340,458*
