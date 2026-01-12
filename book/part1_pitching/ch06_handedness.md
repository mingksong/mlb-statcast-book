# Chapter 6: L/R Pitcher Differences

## Key Findings

- **Right-handers throw 1.4 mph harder** than left-handers (94.0 vs 92.6 mph)
- **Left-handers throw more changeups**: 13.1% vs 9.2% usage
- **LHP representation is stable** at ~27% of all pitches (no significant trend)
- **Movement patterns are perfectly mirrored** between handedness

---

## The Story

Walk into any big league clubhouse, and you'll notice something immediately: right-handers dominate. For every southpaw, you'll find roughly three right-handed pitchers. This ratio has held steady for a decade.

But here's the puzzle: if right-handers throw harder, why do teams still value lefties so highly?

### The Velocity Gap

Our analysis of 7.4 million pitches reveals a consistent velocity difference:

| Handedness | 4-Seam Velocity | Sample Size |
|------------|-----------------|-------------|
| Right-handed | 94.01 mph | 1.85M pitches |
| Left-handed | 92.62 mph | 0.68M pitches |
| **Difference** | **+1.39 mph** | |

This isn't a small effect. With a Cohen's d of 0.53, this is a "medium" effect size—statistically meaningful and practically significant.

### Why Lefties Survive

Despite the velocity disadvantage, left-handers have thrived. The answer lies in scarcity and strategy.

**Scarcity creates value**: Only about 10% of the population is left-handed. This natural rarity means left-handed batters see fewer same-side matchups, giving lefty pitchers a platoon advantage.

**Strategic adaptations**: Our data shows left-handers have evolved a distinct pitch mix:

| Pitch Type | LHP | RHP |
|------------|-----|-----|
| Changeup | **13.1%** | 9.2% |
| Curveball | 7.7% | 6.7% |
| Sinker | 16.4% | 15.2% |

Left-handers throw nearly 50% more changeups than right-handers. This off-speed emphasis compensates for lower velocity.

### Mirror Images

One of the most elegant findings: movement patterns are perfectly mirrored.

```
LHP 4-Seam: H-Break = +0.68 inches (arm-side)
RHP 4-Seam: H-Break = -0.64 inches (glove-side)
```

The vertical break is identical (+1.32 inches). The difference is purely directional—like looking at your reflection.

---

## The Analysis

### Loading Handedness Data

```python
from statcast_analysis import load_season, AVAILABLE_SEASONS

for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['pitch_type', 'release_speed', 'p_throws'])

    lhp = df[df['p_throws'] == 'L']
    rhp = df[df['p_throws'] == 'R']

    lhp_velo = lhp[lhp['pitch_type'] == 'FF']['release_speed'].mean()
    rhp_velo = rhp[rhp['pitch_type'] == 'FF']['release_speed'].mean()

    print(f"{year}: LHP={lhp_velo:.2f}, RHP={rhp_velo:.2f}, Diff={rhp_velo-lhp_velo:+.2f}")
```

### Year-by-Year Velocity

| Year | LHP Velocity | RHP Velocity | Gap |
|------|-------------|-------------|-----|
| 2015 | 92.15 | 93.45 | +1.30 |
| 2016 | 92.47 | 93.48 | +1.01 |
| 2017 | 92.46 | 93.49 | +1.03 |
| 2018 | 92.16 | 93.50 | +1.34 |
| 2019 | 92.10 | 93.85 | +1.75 |
| 2020 | 92.00 | 93.87 | +1.86 |
| 2021 | 92.68 | 94.12 | +1.44 |
| 2022 | 93.01 | 94.27 | +1.27 |
| 2023 | 93.12 | 94.55 | +1.42 |
| 2024 | 93.27 | 94.68 | +1.42 |
| 2025 | 93.09 | 95.01 | +1.92 |

Both groups are getting faster, but the gap persists.

---

## Statistical Validation

| Test | Result | Interpretation |
|------|--------|----------------|
| Velocity t-test | p < 0.001 | Highly significant |
| Velocity Cohen's d | 0.532 | Medium effect |
| LHP ratio trend | p = 0.639 | Not significant |
| LHP ratio R² | 0.026 | Weak (stable) |

---

## Visualizations

### Figure 1: The Persistent Gap

![Velocity by Handedness](../chapters/06_handedness/figures/fig01_velocity_by_handedness.png)

Both curves rise together—the velocity arms race affects both handedness groups equally.

### Figure 2: Stable Representation

![LHP Percentage](../chapters/06_handedness/figures/fig02_lhp_percentage_trend.png)

Despite the velocity disadvantage, left-handers maintain their ~27% share.

### Figure 3: The Changeup Advantage

![Pitch Mix](../chapters/06_handedness/figures/fig03_pitch_mix_comparison.png)

Left-handers compensate for lower velocity with more off-speed pitches.

---

## What It Means

1. **Velocity isn't everything**: Left-handers prove that pitch mix and platoon advantages matter
2. **Natural selection at work**: Only lefties who can compete despite lower velocity make it to MLB
3. **Strategic evolution**: Heavy changeup usage shows adaptation to physical constraints
4. **The ratio holds**: Despite analytics revolution, LHP representation hasn't changed

---

## Try It Yourself

Full analysis code:
```
github.com/mingksong/mlb-statcast-book/chapters/06_handedness/
```

Run it:
```bash
cd chapters/06_handedness
python analysis.py
```
