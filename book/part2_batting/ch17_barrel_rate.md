# Chapter 17: The Barrel Rate Plateau

When MLB introduced Statcast, "barrel" became the new power metric. A barrel represents the perfect combination of exit velocity and launch angle—contact so pure it almost guarantees extra-base hits. The definition is precise: 98+ mph exit velocity at an optimal launch angle (the exact angle threshold varies by exit velocity).

Given the focus on launch angle optimization, you might expect barrel rate to climb. Hitters are trying to elevate, trying to hit the ball hard. But the data reveals something surprising: barrel rate hasn't changed at all.

## Getting Started

Let's begin by understanding what makes a barrel:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'launch_speed', 'launch_angle',
                                        'events', 'estimated_ba_using_speedangle'])

# Filter to batted balls
batted_balls = df.dropna(subset=['launch_speed', 'launch_angle'])

# Define barrels (simplified: 98+ mph, 25-30° optimal zone)
# Note: MLB's actual barrel definition is more complex with sliding scale
def is_barrel(row):
    ev = row['launch_speed']
    la = row['launch_angle']
    if ev >= 98:
        # Higher EV allows wider launch angle range
        optimal_min = 26 - (ev - 98)
        optimal_max = 30 + (ev - 98)
        return optimal_min <= la <= optimal_max
    return False

batted_balls['barrel'] = batted_balls.apply(is_barrel, axis=1)
print(f"Total batted balls: {len(batted_balls):,}")
print(f"Total barrels: {batted_balls['barrel'].sum():,}")
```

With over 2 million batted balls, we can track the most elite contact in baseball.

## The Flat Line

Suppose we want to see if hitters are barreling more balls over time:

```python
# Calculate barrel rate by year
barrel_rate = batted_balls.groupby('game_year')['barrel'].mean() * 100
print(barrel_rate.round(2))
```

| Year | Barrel Rate | Total Barrels |
|------|-------------|---------------|
| 2015 | 5.15% | 7,807 |
| 2016 | 4.81% | 9,116 |
| 2017 | 4.58% | 9,148 |
| 2018 | 4.80% | 9,667 |
| 2019 | 5.27% | 10,608 |
| 2020 | 4.81% | 3,746 |
| 2021 | 4.79% | 11,129 |
| 2022 | 4.57% | 10,773 |
| 2023 | 4.94% | 11,700 |
| 2024 | 4.71% | 11,182 |
| 2025 | 5.29% | 12,457 |

![Barrel Rate Trend](../../chapters/17_barrel_rate/figures/fig01_barrel_trend.png)

The barrel rate hasn't moved. It fluctuates between 4.6% and 5.3%—essentially random variation around a stable mean of about 4.9%.

## What This Tells Us

This flat line is revealing. Despite the launch angle revolution (Chapter 16), hitters aren't making better contact—they're just changing where mediocre contact lands.

```python
# The barrel paradox
print("What the launch angle revolution did:")
print("- Reduced ground balls → fewer easy outs")
print("- Increased fly balls → more potential home runs")
print("- Maintained barrel rate → same quality of peak contact")
print()
print("What it DIDN'T do:")
print("- Create more barrels")
print("- Improve contact quality")
print("- Generate more elite exit velocity")
```

The revolution was about converting non-barrel ground balls into non-barrel fly balls—not about creating more elite contact.

## Year-to-Year Variation

Let's examine the small variations we do see:

```python
# Peak years
print(f"Best year: 2025 at {5.29:.2f}%")
print(f"Worst year: 2022 at {4.57:.2f}%")
print(f"Range: {5.29 - 4.57:.2f} percentage points")
```

The difference between the best and worst years is less than 1 percentage point. And there's no pattern—2022 was low, 2019 was high, then it went down again. This is noise, not trend.

## Why Can't Hitters Barrel More?

The stability of barrel rate suggests a fundamental ceiling. Barrels require:

1. **Elite exit velocity (98+ mph)**: Achieved only with perfect timing and bat-to-ball contact
2. **Optimal launch angle (25-30°)**: A narrow window that shrinks with lower exit velocity
3. **Perfect sweet spot contact**: The bat's optimal hitting zone is small

```python
# The physics of barrels
print("Why barrels are hard:")
print("- Sweet spot on bat: ~2 inches wide")
print("- Optimal contact point: 1/8 inch tolerance")
print("- Timing window: ~7 milliseconds")
print("- Ball travels: 60.5 feet in 400ms")
print()
print("Even MLB's best hitters barrel ~10-12% of batted balls")
print("League average: ~5%")
```

No amount of swing optimization can change these physical constraints. The bat's sweet spot doesn't get bigger, the timing window doesn't expand, and the ball doesn't slow down.

## The Elite Barrels

Let's see what happens when batters do barrel the ball:

```python
# Outcomes on barrels vs non-barrels
barrels_only = batted_balls[batted_balls['barrel'] == True]
non_barrels = batted_balls[batted_balls['barrel'] == False]

barrel_avg = barrels_only['estimated_ba_using_speedangle'].mean()
non_barrel_avg = non_barrels['estimated_ba_using_speedangle'].mean()

print(f"Barrels xBA: {barrel_avg:.3f}")
print(f"Non-barrels xBA: {non_barrel_avg:.3f}")
```

| Contact Type | xBA | xSLG | HR Rate |
|--------------|-----|------|---------|
| Barrels | .755 | 1.427 | ~65% |
| Non-Barrels | .251 | .355 | ~4% |

Barrels produce a .755 expected batting average and roughly 65% become home runs. They're the most valuable contact in baseball—which is exactly why the flat rate matters.

## Is This Real? Statistical Validation

Let's confirm there's no meaningful trend:

```python
from scipy import stats
import numpy as np

years = np.array(range(2015, 2026), dtype=float)
rates = np.array([5.15, 4.81, 4.58, 4.80, 5.27, 4.81, 4.79, 4.57, 4.94, 4.71, 5.29])

slope, intercept, r, p, se = stats.linregress(years, rates)
print(f"Trend: {slope:.4f}%/year")
print(f"R² = {r**2:.3f}")
print(f"p-value = {p:.3f}")
```

| Test | Value | Interpretation |
|------|-------|----------------|
| Slope | +0.004%/year | Essentially zero |
| R² | 0.004 | No relationship |
| p-value | 0.878 | Not significant |

With a p-value of 0.878 and R² of 0.004, there's no evidence of any trend whatsoever. The year-to-year variation is pure randomness.

## Connection to Other Metrics

Barrel rate's stability helps explain several patterns we've seen:

1. **Exit velocity stable (Chapter 15)**: Barrels require high EV, and both are flat
2. **Launch angle increased (Chapter 16)**: But not in the barrel zone specifically
3. **Home runs fluctuated**: Driven by ball composition, not barrel rate

```python
# The power equation
print("Home runs are driven by:")
print("1. Barrel rate (stable at ~5%)")
print("2. Ball composition (variable)")
print("3. Total batted balls (variable)")
print()
print("When HRs surged 2017-2019, it wasn't because of more barrels.")
print("The same barrels were just traveling farther.")
```

## What We Learned

Let's summarize what the data revealed:

1. **Barrel rate flat at ~5%**: No change from 2015 to 2025
2. **Year-to-year variation is noise**: R² = 0.004, p = 0.878
3. **Physical ceiling exists**: Bat physics limit barrel potential
4. **Elite contact unchanged**: Best hitters still barrel ~10-12%
5. **Launch angle revolution was different**: About non-barrel contact distribution
6. **Barrels still dominant**: .755 xBA, ~65% HR rate when achieved

The barrel rate story reinforces a theme: hitting a baseball remains one of the hardest tasks in sports. Despite analytics, technology, and training advances, the fundamental challenge of putting the bat's sweet spot on a 95+ mph pitch in a 7-millisecond window hasn't changed.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/17_barrel_rate/`

Try modifying the code to explore:
- Which players have the highest barrel rates?
- How does barrel rate vary by pitch type?
- What's the correlation between barrel rate and home runs?

```bash
cd chapters/17_barrel_rate
python analysis.py
```
