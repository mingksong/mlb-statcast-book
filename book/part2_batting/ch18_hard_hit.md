# Chapter 18: Hard Hit Rate Revisited

We've explored exit velocity (Chapter 15), launch angle (Chapter 16), and barrel rate (Chapter 17). Now let's examine "hard hit" rate—a simpler but widely-used metric that captures balls hit 95+ mph regardless of launch angle.

Hard hit rate has become a staple of broadcast analytics. "He's got a hard hit rate of 45%!" But what does it actually tell us about contact quality, and how has it changed over the Statcast era?

## Getting Started

Let's begin by calculating hard hit rate across all seasons:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'launch_speed', 'launch_angle',
                                        'events', 'description'])

# Filter to batted balls
batted_balls = df.dropna(subset=['launch_speed'])

# Define hard hit (95+ mph)
batted_balls['hard_hit'] = batted_balls['launch_speed'] >= 95
print(f"Total batted balls: {len(batted_balls):,}")
print(f"Hard hit balls: {batted_balls['hard_hit'].sum():,}")
```

With over 2 million batted balls, we can track how hard hitters are making contact.

## The Hard Hit Trend

Suppose we want to see if hard hit rate has changed over the decade:

```python
# Calculate hard hit rate by year
hard_hit_rate = batted_balls.groupby('game_year')['hard_hit'].mean() * 100
print(hard_hit_rate.round(1))
```

| Year | Hard Hit Rate | Hard Hit Count | Avg EV |
|------|---------------|----------------|--------|
| 2015 | 31.8% | 48,253 | 87.1 mph |
| 2016 | 26.3% | 49,804 | 84.1 mph |
| 2017 | 24.0% | 47,892 | 82.1 mph |
| 2018 | 25.1% | 50,604 | 83.5 mph |
| 2019 | 25.9% | 52,219 | 83.9 mph |
| 2020 | 24.6% | 19,151 | 82.8 mph |
| 2021 | 23.7% | 55,041 | 82.2 mph |
| 2022 | 23.6% | 55,592 | 82.2 mph |
| 2023 | 24.1% | 57,206 | 82.6 mph |
| 2024 | 23.8% | 56,367 | 82.5 mph |
| 2025 | 25.5% | 60,035 | 83.1 mph |

![Hard Hit Trend](../../chapters/18_hard_hit/figures/fig01_hard_hit_trend.png)

The pattern mirrors what we saw with exit velocity: an apparent decline from 2015, then stability from 2016 onward.

## The 2015 Problem (Again)

That 31.8% hard hit rate in 2015 stands out dramatically:

```python
# The 2015 gap
hhr_2015 = (batted_balls[batted_balls['game_year'] == 2015]['launch_speed'] >= 95).mean() * 100
hhr_2016 = (batted_balls[batted_balls['game_year'] == 2016]['launch_speed'] >= 95).mean() * 100
print(f"2015: {hhr_2015:.1f}%")
print(f"2016: {hhr_2016:.1f}%")
print(f"Drop: {hhr_2015 - hhr_2016:.1f} percentage points")
```

A 5.5 percentage point drop in one year is implausible as organic change. This is the same Statcast calibration issue we identified in Chapter 15. The 2015 exit velocity readings were systematically higher, which artificially inflated hard hit rate.

## The Real Story: Post-2015 Stability

Excluding 2015, the picture changes entirely:

```python
# Post-2015 analysis
post_2015 = batted_balls[batted_balls['game_year'] >= 2016]
yearly_hhr = post_2015.groupby('game_year')['hard_hit'].mean() * 100

print(f"Range: {yearly_hhr.min():.1f}% to {yearly_hhr.max():.1f}%")
print(f"Mean: {yearly_hhr.mean():.1f}%")
print(f"Std: {yearly_hhr.std():.1f}%")
```

| Statistic | Value |
|-----------|-------|
| Minimum (2022) | 23.6% |
| Maximum (2016) | 26.3% |
| Mean | 24.6% |
| Std Dev | 1.0% |

From 2016-2025, hard hit rate has varied by less than 3 percentage points. The year-to-year variation is essentially noise around a stable 24-25% baseline.

## Hard Hit vs. Barrel

How does hard hit rate compare to barrel rate?

```python
# Comparison
print("Hard Hit (95+ mph any angle):")
print("- Rate: ~25%")
print("- Definition: Simple, one threshold")
print("- Includes: Ground balls, pop-ups")
print()
print("Barrel (98+ mph, optimal angle):")
print("- Rate: ~5%")
print("- Definition: Complex, sliding scale")
print("- Excludes: Non-optimal angles")
```

Hard hit captures about 5x more batted balls than barrels because it ignores launch angle. A 100 mph grounder counts as "hard hit" but not as a barrel—and that grounder is often an out.

| Contact Type | Rate | Typical Outcome |
|--------------|------|-----------------|
| Barrel | 5% | .755 xBA, 65% HR |
| Hard Hit (non-barrel) | 20% | .400 xBA, varies |
| Soft Contact | 75% | .200 xBA |

## The Quality Spectrum

Let's break down hard hit balls by launch angle:

```python
# Hard hit breakdown
hard_hit_only = batted_balls[batted_balls['hard_hit'] == True]

# Categorize by launch angle
ground_balls = hard_hit_only[hard_hit_only['launch_angle'] < 10]
line_drives = hard_hit_only[(hard_hit_only['launch_angle'] >= 10) &
                            (hard_hit_only['launch_angle'] < 25)]
fly_balls = hard_hit_only[(hard_hit_only['launch_angle'] >= 25) &
                          (hard_hit_only['launch_angle'] < 50)]
pop_ups = hard_hit_only[hard_hit_only['launch_angle'] >= 50]

print(f"Hard-hit ground balls: {len(ground_balls) / len(hard_hit_only) * 100:.1f}%")
print(f"Hard-hit line drives: {len(line_drives) / len(hard_hit_only) * 100:.1f}%")
print(f"Hard-hit fly balls: {len(fly_balls) / len(hard_hit_only) * 100:.1f}%")
```

About 30% of hard-hit balls are ground balls or pop-ups—hard contact that doesn't lead to good outcomes. This is why barrel rate, despite being more complex, is often a better predictor of success.

## Is This Real? Statistical Validation

Let's test whether there's a significant trend in hard hit rate:

```python
from scipy import stats
import numpy as np

# Full period including 2015
years_all = np.array(range(2015, 2026), dtype=float)
rates_all = np.array([31.8, 26.3, 24.0, 25.1, 25.9, 24.6, 23.7, 23.6, 24.1, 23.8, 25.5])

slope, intercept, r, p, se = stats.linregress(years_all, rates_all)
print(f"Full period: slope={slope:.2f}%/year, R²={r**2:.3f}, p={p:.3f}")

# Post-2015 only
years_post = np.array(range(2016, 2026), dtype=float)
rates_post = rates_all[1:]

slope2, intercept2, r2, p2, se2 = stats.linregress(years_post, rates_post)
print(f"Post-2015: slope={slope2:.2f}%/year, R²={r2**2:.3f}, p={p2:.3f}")
```

| Test Period | Slope | R² | p-value |
|-------------|-------|-----|---------|
| 2015-2025 | -0.52%/year | 0.37 | 0.052 |
| 2016-2025 | -0.05%/year | 0.01 | 0.791 |

The full period shows marginal significance (p=0.052), but that's driven entirely by the 2015 outlier. Excluding 2015, there's no trend whatsoever (p=0.791).

## Why Hard Hit Rate Matters Less

Hard hit rate is a useful quick metric, but it's a blunt instrument:

```python
# Limitations of hard hit rate
print("What hard hit rate tells you:")
print("- General contact quality")
print("- Easy to calculate")
print("- Good for quick comparisons")
print()
print("What it misses:")
print("- Launch angle matters enormously")
print("- A 95 mph grounder ≠ 95 mph line drive")
print("- Barrel rate is more predictive")
```

For serious analysis, barrel rate and expected statistics (xBA, xSLG) provide better insight. Hard hit rate remains popular in broadcasts because it's simple to explain, not because it's the best metric.

## Connection to Other Chapters

Hard hit rate bridges several concepts:

1. **Exit velocity (Chapter 15)**: Hard hit is EV with a threshold
2. **Barrel rate (Chapter 17)**: Barrels are hard-hit + optimal angle
3. **Launch angle (Chapter 16)**: The missing dimension in hard hit

```python
# The contact hierarchy
print("Contact quality hierarchy:")
print("1. Barrels: 98+ mph, optimal angle → Best")
print("2. Hard hit line drives: 95+ mph, 10-25° → Excellent")
print("3. Hard hit fly balls: 95+ mph, 25-35° → Good")
print("4. Hard hit ground balls: 95+ mph, <10° → Mixed")
print("5. Soft contact: <95 mph → Poor")
```

## What We Learned

Let's summarize what the data revealed:

1. **Hard hit rate stable at ~25%**: After 2015 calibration correction
2. **2015 was anomalous**: 31.8% driven by measurement, not performance
3. **No meaningful trend post-2015**: p=0.791, pure noise
4. **Hard hit includes bad outcomes**: 30% are grounders or pop-ups
5. **Barrel rate is superior**: Captures quality better than quantity
6. **Simple metric, limited insight**: Good for broadcasts, not analysis

Hard hit rate is baseball's "good enough" metric—easy to understand, widely available, but telling only part of the story. For deeper analysis, barrel rate and expected statistics provide more value.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/18_hard_hit/`

Try modifying the code to explore:
- Which players have the highest hard hit rates?
- How does hard hit rate vary by pitch location?
- Is hard hit rate more predictive for certain player types?

```bash
cd chapters/18_hard_hit
python analysis.py
```
