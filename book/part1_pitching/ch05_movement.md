# Chapter 5: Pitch Movement Analysis

Here's a puzzle: if pitchers are throwing 1.4 mph harder than a decade ago, shouldn't their pitches move differently? Physics would suggest that harder-thrown balls spend less time in the air, potentially reducing movement. Yet our analysis reveals something unexpected—pitch movement has barely changed at all.

In this chapter, we'll investigate whether the velocity revolution has affected how pitches actually move through the strike zone, and discover why the answer matters for understanding modern pitching.

## Getting Started

Let's begin by loading our pitch data and examining the two key movement metrics that Statcast tracks:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'pitch_type', 'pfx_x', 'pfx_z'])

# pfx_x: Horizontal movement (inches)
#   Positive = arm-side break (inside to RHH for RHP)
#   Negative = glove-side break

# pfx_z: Vertical movement (inches)
#   Also called "Induced Vertical Break" (IVB)
#   Measures rise above what gravity alone would produce

# Filter to 4-seam fastballs
ff = df[df['pitch_type'] == 'FF']
print(f"Total fastballs analyzed: {len(ff):,}")
```

With over 2.4 million four-seam fastballs in our dataset, we can track exactly how pitch movement has—or hasn't—evolved.

## The Stability Paradox

Suppose we want to see how fastball movement changed year by year. We can calculate the mean horizontal and vertical break:

```python
yearly_movement = ff.groupby('game_year').agg({
    'pfx_x': ['mean', 'std'],
    'pfx_z': ['mean', 'std']
}).round(2)
print(yearly_movement)
```

The results reveal a remarkably flat picture:

| Year | Horizontal Break | Vertical Break (IVB) |
|------|------------------|---------------------|
| 2015 | -0.23 in | +1.33 in |
| 2017 | -0.33 in | +1.43 in |
| 2019 | -0.29 in | +1.30 in |
| 2020 | -0.27 in | +1.33 in |
| 2021 | -0.24 in | +1.34 in |
| 2023 | -0.28 in | +1.31 in |
| 2025 | -0.28 in | +1.32 in |

![Fastball Movement Trend](../../chapters/05_movement/figures/fig01_fastball_movement_trend.png)

Look at those numbers—over 11 seasons, horizontal break changed by just 0.05 inches and vertical break by essentially zero. Meanwhile, velocity increased by 1.4 mph. How is this possible?

## Understanding the Physics

The stability tells us something important about pitching physics. Movement comes primarily from:

1. **Spin rate**: How fast the ball rotates
2. **Spin axis**: The orientation of that rotation
3. **Seam orientation**: How the stitches interact with air

```python
# Let's look at average movement across all pitch types
pitch_types = ['FF', 'SL', 'CU', 'CH', 'SI']
for pt in pitch_types:
    subset = df[df['pitch_type'] == pt]
    early = subset[subset['game_year'].isin([2015, 2016, 2017])]
    late = subset[subset['game_year'].isin([2023, 2024, 2025])]

    print(f"{pt}: H-break changed from {early['pfx_x'].mean():.2f} to {late['pfx_x'].mean():.2f}")
```

The stability extends across pitch types:

| Pitch Type | 2015-17 H-Break | 2023-25 H-Break | Change |
|------------|-----------------|-----------------|--------|
| 4-Seam (FF) | -0.27 in | -0.28 in | -0.01 in |
| Slider (SL) | +0.25 in | +0.20 in | -0.05 in |
| Curveball (CU) | +0.47 in | +0.35 in | -0.12 in |
| Changeup (CH) | -0.29 in | -0.37 in | -0.08 in |
| Sinker (SI) | -0.50 in | -0.52 in | -0.02 in |

![Pitch Movement Profile](../../chapters/05_movement/figures/fig02_pitch_movement_profile.png)

Each pitch type occupies a distinct region of the movement space, and these regions haven't shifted meaningfully over the decade.

## Why Hasn't Movement Changed?

This raises an interesting question: with all the talk of "spin rate revolutions" and "pitch design," why hasn't movement actually changed?

Several factors explain this stability:

1. **Biomechanical constraints**: Movement comes from spin axis and release mechanics that don't change much with velocity increases

2. **Natural selection**: Pitchers who lose movement when throwing harder don't make it to MLB

3. **Focused optimization**: Teams prioritize velocity because it's the clearer path to "stuff" gains

4. **Efficiency limits**: There may be physical ceilings on how much spin axis can be optimized

```python
# Compare distributions between 2015 and 2025
import numpy as np

ff_2015 = ff[ff['game_year'] == 2015]
ff_2025 = ff[ff['game_year'] == 2025]

print("Horizontal Break Distribution:")
print(f"2015: mean={ff_2015['pfx_x'].mean():.2f}, std={ff_2015['pfx_x'].std():.2f}")
print(f"2025: mean={ff_2025['pfx_x'].mean():.2f}, std={ff_2025['pfx_x'].std():.2f}")
```

![Distribution Comparison](../../chapters/05_movement/figures/fig04_distribution_comparison.png)

The 2015 and 2025 distributions nearly perfectly overlap—visual proof of the stability.

## Is This Real? Statistical Validation

Before drawing conclusions, we should ask: Is this stability statistically significant, or might there be hidden trends we're missing?

```python
from scipy import stats
import numpy as np

# Trend analysis for horizontal break
yearly = ff.groupby('game_year')['pfx_x'].mean()
years = np.array(yearly.index, dtype=float)
h_break = np.array(yearly.values, dtype=float)

slope, intercept, r, p, se = stats.linregress(years, h_break)
print(f"Horizontal Break Trend:")
print(f"  Slope: {slope:.4f} in/year")
print(f"  R² = {r**2:.3f}")
print(f"  p-value = {p:.3f}")
```

The results confirm the lack of trend:

| Metric | Horizontal Break | Vertical Break |
|--------|------------------|----------------|
| Trend slope | -0.003 in/year | -0.003 in/year |
| R² | 0.094 (weak) | 0.065 (weak) |
| p-value | 0.358 (not significant) | 0.450 (not significant) |
| Cohen's d | -0.036 (negligible) | -0.153 (negligible) |

With R² values below 0.1 and p-values well above 0.05, there is no statistically significant trend in either direction. And with Cohen's d values under 0.2, any observed differences have no practical significance.

## What About Different Pitch Types?

Let's see if any specific pitch type shows meaningful movement changes:

```python
# Movement trends by pitch type
for pitch_type in ['FF', 'SL', 'CU', 'CH', 'SI']:
    subset = df[df['pitch_type'] == pitch_type]
    yearly = subset.groupby('game_year')['pfx_x'].mean()

    slope, _, r, p, _ = stats.linregress(
        np.array(yearly.index, dtype=float),
        np.array(yearly.values, dtype=float)
    )

    print(f"{pitch_type}: slope={slope:.4f} in/yr, R²={r**2:.3f}, p={p:.3f}")
```

| Pitch Type | Trend (in/year) | R² | Significant? |
|------------|-----------------|-----|--------------|
| 4-Seam | -0.003 | 0.094 | No |
| Slider | -0.006 | 0.142 | No |
| Curveball | -0.014 | 0.320 | No |
| Changeup | -0.012 | 0.361 | No |
| Sinker | -0.009 | 0.269 | No |

![Movement by Pitch Type](../../chapters/05_movement/figures/fig03_movement_by_pitch_type.png)

No pitch type shows a statistically significant trend in horizontal break. The game's movement profile has remained stable across the board.

## The Bigger Picture

This finding has important implications for understanding modern pitching:

1. **"Stuff" evolution is about velocity**: When analysts say stuff is improving, they primarily mean velocity—not movement

2. **Velocity and movement are independent**: Pitchers aren't trading movement for velocity; they're gaining one while maintaining the other

3. **Pitch design has limits**: Despite all the technology, there may be physical ceilings on movement optimization

4. **The complete picture**: To understand modern pitching, you need both velocity trends (Chapter 2) and movement stability (this chapter)

## What We Learned

Let's summarize what the data revealed:

1. **Fastball movement hasn't changed**: Horizontal break moved -0.05 in, vertical break -0.01 in over the decade
2. **No significant trend exists**: R² < 0.1, p > 0.35 for both metrics
3. **Effect sizes are negligible**: Cohen's d of -0.036 (horizontal) and -0.153 (vertical)
4. **All pitch types are stable**: Sliders, curves, changeups, and sinkers show similar stability
5. **Velocity and movement are independent**: Throwing harder doesn't sacrifice movement

The stability paradox reveals that baseball's velocity revolution has been remarkably selective—pitchers found ways to throw harder without losing the movement that makes their pitches effective.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/05_movement/`

Try modifying the code to explore:
- How does movement correlate with spin rate for individual pitchers?
- Are there specific pitchers who gained velocity while losing movement?
- How does release point affect movement profiles?

```bash
cd chapters/05_movement
python analysis.py
```
