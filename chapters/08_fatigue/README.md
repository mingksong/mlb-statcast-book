# Chapter 8: Velocity/Spin Decay by Inning (2015-2025)

## Research Question

**How do velocity and spin rate change as games progress, and what patterns emerge?**

---

## Key Findings (Surprising!)

### The Paradox: Velocity INCREASES in Late Innings

| Inning | Velocity | Spin Rate |
|--------|----------|-----------|
| 1 | 93.41 mph | 2,266 rpm |
| 5 | 93.14 mph | 2,265 rpm |
| 9 | **94.83 mph** | **2,317 rpm** |

**Why?** Starters are replaced by hard-throwing relievers in late innings.

### The Real Story: Bullpen Effect

| Innings | Avg Velocity | Who's Pitching |
|---------|-------------|----------------|
| 1-3 | 93.26 mph | Mostly starters |
| 7-9 | 94.37 mph | Mostly relievers |
| **Difference** | **+1.11 mph** | |

### Statistical Validation

| Test | Value | Interpretation |
|------|-------|----------------|
| Velocity trend slope | +0.189 mph/inning | Significant increase |
| Velocity R² | 0.684 | Strong fit |
| Early vs Late Cohen's d | 0.421 | Small-medium effect |
| Spin trend slope | +6.1 rpm/inning | Significant increase |

---

## Interpretation

This analysis reveals the **modern bullpen strategy** rather than pitcher fatigue:

1. **Starters go fewer innings** (see Chapter 26: Starter Innings Trend)
2. **Relievers throw harder** than starters on average
3. **The composite effect**: Late-inning velocity rises despite individual pitcher fatigue

Within a starter's outing, velocity does decline. But at the game level, the substitution of relievers masks this effect.

---

## Files

```
chapters/08_fatigue/
├── README.md
├── analysis.py
├── figures/
│   ├── fig01_velocity_by_inning.png
│   ├── fig02_spin_by_inning.png
│   ├── fig03_velocity_spin_combined.png
│   └── fig04_yearly_fatigue.png
└── results/
    ├── velocity_by_inning.csv
    ├── spin_by_inning.csv
    ├── yearly_fatigue.csv
    ├── statistical_tests.csv
    └── summary.csv
```

---

## Reproducibility

```bash
python chapters/08_fatigue/analysis.py
```

---

*Analysis completed: 2025-01-12*
*Total 4-seam fastballs analyzed: 2,529,644*
