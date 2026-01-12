# Chapter 5: Movement Analysis

## Key Findings

- **Pitch movement has remained remarkably stable** from 2015 to 2025
- **4-seam fastball horizontal break**: -0.23 in (2015) to -0.28 in (2025), a negligible -0.05 in change
- **Vertical break (IVB)**: +1.33 in (2015) to +1.32 in (2025), essentially unchanged
- **Key insight**: While velocity increased 1.4 mph over the decade, movement stayed flat

---

## The Story

Here's a puzzle: if pitchers are throwing 1.4 mph harder than a decade ago, shouldn't their pitches move differently? The physics would suggest harder-thrown balls might have less movement due to reduced air time, yet our analysis reveals something unexpected.

### The Stability Paradox

After analyzing 7.4 million pitches across 11 seasons, we found pitch movement has barely budged. The 4-seam fastball—baseball's most common pitch—shows nearly identical movement profiles in 2015 and 2025.

This stability extends across pitch types. Sliders break the same. Curveballs drop the same. Changeups fade the same. Despite all the talk of "spin rate revolutions" and "pitch design," the fundamental movement characteristics of MLB pitches haven't changed.

### What This Means

The stability tells us something important: **the velocity arms race and pitch design are largely independent phenomena**.

Pitchers aren't gaining velocity by sacrificing movement. Instead, they're optimizing one variable (velocity) while maintaining another (movement). This is likely due to:

1. **Biomechanical constraints**: Movement comes from spin axis and release mechanics that don't change with velocity
2. **Natural selection**: Pitchers who lose movement when throwing harder don't make it to MLB
3. **Focused optimization**: Teams prioritize velocity because it's the clearer path to "stuff" gains

---

## The Analysis

### Measuring Movement

Statcast tracks two key movement metrics:

```python
# pfx_x: Horizontal movement (inches)
#   Positive = arm-side break (inside to RHH for RHP)
#   Negative = glove-side break

# pfx_z: Vertical movement (inches)
#   Also called "Induced Vertical Break" (IVB)
#   Measures rise above what gravity alone would produce
```

### Loading 11 Seasons

```python
from statcast_analysis import load_season, AVAILABLE_SEASONS

for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['pitch_type', 'pfx_x', 'pfx_z'])

    # Filter to 4-seam fastballs
    ff = df[df['pitch_type'] == 'FF']

    print(f"{year}: H-Break={ff['pfx_x'].mean():.2f}in, V-Break={ff['pfx_z'].mean():.2f}in")
```

### Results: 4-Seam Fastball Movement

| Year | Horizontal Break | Vertical Break (IVB) |
|------|------------------|---------------------|
| 2015 | -0.23 in | +1.33 in |
| 2016 | -0.20 in | +1.32 in |
| 2017 | -0.33 in | +1.43 in |
| 2018 | -0.27 in | +1.31 in |
| 2019 | -0.29 in | +1.30 in |
| 2020 | -0.27 in | +1.33 in |
| 2021 | -0.24 in | +1.34 in |
| 2022 | -0.27 in | +1.35 in |
| 2023 | -0.28 in | +1.31 in |
| 2024 | -0.27 in | +1.31 in |
| 2025 | -0.28 in | +1.32 in |

---

## Statistical Validation

| Test | Horizontal Break | Vertical Break |
|------|------------------|----------------|
| Trend slope | -0.003 in/year | -0.003 in/year |
| R-squared | 0.094 (weak) | 0.065 (weak) |
| p-value | 0.358 (not significant) | 0.450 (not significant) |
| Cohen's d | -0.036 (negligible) | -0.153 (negligible) |

**Interpretation**: Neither horizontal nor vertical break shows a statistically significant trend. The effect sizes are negligible, meaning any observed differences have no practical significance.

---

## Visualizations

### Figure 1: Fastball Movement Trend

![Fastball Movement Trend](../chapters/05_movement/figures/fig01_fastball_movement_trend.png)

The flat regression lines confirm the lack of trend. Year-to-year variation exists, but no directional change emerges.

### Figure 2: Pitch Movement Profile

![Pitch Movement Profile](../chapters/05_movement/figures/fig02_pitch_movement_profile.png)

Each pitch type occupies a distinct region of the movement space, and these regions haven't shifted over the decade.

### Figure 3: Distribution Comparison (2015 vs 2025)

![Distribution Comparison](../chapters/05_movement/figures/fig04_distribution_comparison.png)

The 2015 and 2025 distributions nearly perfectly overlap—statistical proof of stability.

---

## The Bigger Picture

This finding has important implications:

1. **"Stuff" evolution**: When analysts say stuff is improving, they primarily mean velocity—not movement
2. **Pitch design limits**: There may be physical ceilings on how much movement optimization is possible
3. **The complete picture**: To understand modern pitching, you need both velocity trends (Chapter 2) and movement stability (this chapter)

---

## Try It Yourself

Full analysis code available at:
```
github.com/mingksong/mlb-statcast-book/chapters/05_movement/
```

Run it:
```bash
cd chapters/05_movement
python analysis.py
```
