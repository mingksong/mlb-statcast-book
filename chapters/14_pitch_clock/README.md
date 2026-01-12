# Chapter 14: Pitch Clock Effect (2023+)

## Research Question

**How has the 2023 pitch clock affected pitching metrics?**

---

## Key Findings

### 1. Minimal Impact on Pitch Counts

| Period | Pitches/Game | Change |
|--------|--------------|--------|
| Pre-clock (2019-22) | 296.0 | baseline |
| Post-clock (2023-25) | 294.3 | **-1.8** |

Cohen's d = 0.049 (negligible effect)

### 2. Velocity Continued to Rise

| Year | Avg Velocity |
|------|-------------|
| 2022 | 88.89 mph |
| 2023 | 89.00 mph |
| 2024 | 89.15 mph |
| 2025 | 89.37 mph |

### 3. Effectiveness Stable

| Metric | 2022 | 2023 | Change |
|--------|------|------|--------|
| wOBA | .318 | .329 | +.011 |
| Whiff Rate | 23.4% | 23.6% | +0.2% |
| K Rate | 22.3% | 22.6% | +0.3% |

---

## Interpretation

The pitch clock's primary effect is on **game duration**, not pitch-level metrics:

1. **Same pitches, less waiting** - The clock reduces time between pitches, not the pitches themselves
2. **Velocity unaffected** - No evidence of fatigue from faster pace
3. **Pitch mix unchanged** - Pitchers didn't simplify their approach
4. **Effectiveness stable** - Neither pitchers nor hitters were disadvantaged

---

## Statistical Validation

| Test | Effect Size | p-value | Interpretation |
|------|-------------|---------|----------------|
| Pitches/Game | d=0.049 | 0.003 | Negligible |
| Velocity | d=0.060 | <0.001 | Negligible |

---

## Files

```
chapters/14_pitch_clock/
├── README.md
├── analysis.py
├── figures/
│   ├── fig01_pitches_per_game.png
│   ├── fig02_effectiveness.png
│   ├── fig03_pitch_mix.png
│   └── fig04_velocity_by_inning.png
└── results/
    ├── pitches_per_game.csv
    ├── effectiveness_by_year.csv
    ├── pitch_mix_by_year.csv
    ├── statistical_tests.csv
    └── summary.csv
```

---

*Analysis completed: 2025-01-12*
*Total pitches analyzed: 4,564,405 (2019-2025)*
