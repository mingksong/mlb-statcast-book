# Chapter 10: First Pitch Strategy

The first pitch of every plate appearance sets the tone for everything that follows. Get ahead 0-1, and the advantage shifts dramatically to the pitcher. Fall behind 1-0, and hitters gain the upper hand. For decades, the conventional wisdom was simple: throw a fastball for a strike. But that wisdom is changing.

In this chapter, we'll explore how first pitch strategy has evolved and what it means for the chess match between pitchers and hitters.

## Getting Started

Let's begin by loading first-pitch data across all seasons:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'pitch_type', 'pitch_number',
                                        'type', 'release_speed'])

# Filter to first pitch of each plate appearance
first_pitch = df[df['pitch_number'] == 1]

# Categorize pitch types
fastballs = ['FF', 'SI', 'FC']
breaking = ['SL', 'CU', 'ST', 'KC']

first_pitch['category'] = first_pitch['pitch_type'].apply(
    lambda x: 'Fastball' if x in fastballs
    else 'Breaking' if x in breaking
    else 'Offspeed'
)
print(f"First pitches analyzed: {len(first_pitch):,}")
```

With nearly 2 million first pitches in our dataset, we can track exactly how strategy has shifted over the decade.

## The Decline of the First-Pitch Fastball

Suppose we want to see how first pitch selection has changed. We can calculate the percentage of fastballs year by year:

```python
# Calculate fastball percentage on first pitch by year
yearly_fb = first_pitch.groupby('game_year').apply(
    lambda x: (x['category'] == 'Fastball').mean() * 100
)
print(yearly_fb.round(1))
```

The results show a clear trend:

| Year | Fastball | Breaking | Offspeed |
|------|----------|----------|----------|
| 2015 | 67.5% | 22.8% | 8.7% |
| 2017 | 65.6% | 25.9% | 7.8% |
| 2019 | 62.5% | 28.9% | 8.1% |
| 2021 | 61.8% | 29.3% | 8.4% |
| 2023 | 60.1% | 30.8% | 8.3% |
| 2025 | 60.3% | 30.4% | 8.3% |

![First Pitch Type](../../chapters/10_first_pitch/figures/fig01_first_pitch_type.png)

First pitch fastball percentage has dropped from 67.5% to 60.3%—a **7.2 percentage point decline**. Meanwhile, breaking balls on the first pitch have jumped from 22.8% to 30.4%. Nearly one-third of plate appearances now start with a slider, curveball, or sweeper.

## Why the Change?

This raises an interesting question: why would pitchers abandon the tried-and-true first-pitch fastball?

```python
# Let's check what happened to first-pitch strike rates
first_pitch['strike'] = first_pitch['type'].isin(['S', 'C', 'F', 'X'])
yearly_strike = first_pitch.groupby('game_year')['strike'].mean() * 100
print(f"2015 strike rate: {yearly_strike[2015]:.1f}%")
print(f"2025 strike rate: {yearly_strike[2025]:.1f}%")
```

| Year | Strike Rate |
|------|-------------|
| 2015 | 49.5% |
| 2019 | 50.0% |
| 2025 | 50.5% |

![Strike Rate](../../chapters/10_first_pitch/figures/fig02_strike_rate.png)

Despite throwing fewer fastballs, pitchers are actually getting *slightly more* first-pitch strikes. The strike rate improved by 1 percentage point over the decade. This tells us that breaking balls aren't just for show—they're effective strike-getters.

## The Breaking Ball Revolution on 0-0

Let's look specifically at how breaking ball usage on first pitch has evolved:

```python
# Breaking ball percentage by year
yearly_brk = first_pitch.groupby('game_year').apply(
    lambda x: (x['category'] == 'Breaking').mean() * 100
)

for year in [2015, 2018, 2021, 2025]:
    print(f"{year}: {yearly_brk[year]:.1f}% breaking balls")
```

| Year | Breaking Ball % | Change from 2015 |
|------|----------------|------------------|
| 2015 | 22.8% | — |
| 2018 | 26.5% | +3.7% |
| 2021 | 29.3% | +6.5% |
| 2025 | 30.4% | **+7.6%** |

Breaking balls on the first pitch have increased by 7.6 percentage points—a 33% relative increase. The sweeper's emergence (Chapter 3) plays a role here, as pitchers now have a breaking ball that's both nasty and controllable.

## What About Hitter Response?

The shift in first-pitch strategy isn't happening in a vacuum. Let's see how hitters have responded:

```python
# First pitch swing rate by year
first_pitch['swing'] = first_pitch['type'].isin(['S', 'F', 'X'])
yearly_swing = first_pitch.groupby('game_year')['swing'].mean() * 100
print(yearly_swing.round(1))
```

Hitters have adjusted too—first-pitch swing rates have fluctuated but remain in the 28-32% range. The cat-and-mouse game continues, with neither side gaining a decisive edge.

## Is This Real? Statistical Validation

Let's confirm the first-pitch fastball decline is statistically significant:

```python
from scipy import stats
import numpy as np

years = np.array(range(2015, 2026), dtype=float)
fb_rates = np.array(yearly_fb.values, dtype=float)

slope, intercept, r, p, se = stats.linregress(years, fb_rates)
print(f"Fastball trend: {slope:.3f}%/year")
print(f"R² = {r**2:.3f}, p = {p:.2e}")
```

| Test | Metric | Value | Interpretation |
|------|--------|-------|----------------|
| Fastball Trend | Slope | -0.77%/year | Significant decline |
| | R² | 0.863 | **Strong fit** |
| | p-value | < 0.001 | Highly significant |
| Strike Rate Trend | Slope | +0.13%/year | Slight improvement |
| | R² | 0.725 | Strong fit |
| | p-value | < 0.001 | Significant |

With R² of 0.86 and p < 0.001, the first-pitch fastball decline is one of the most statistically robust trends in our entire analysis. This is a genuine strategic shift, not random variation.

## The Bigger Picture

The first-pitch strategy shift connects to broader themes we've explored:

1. **Better breaking balls** (Chapter 4): Higher spin rates make sliders more reliable
2. **Pitch type evolution** (Chapter 3): Sweepers give pitchers a new 0-0 weapon
3. **Arsenal diversity** (Chapter 9): More pitches means more first-pitch options

```python
# The strategic logic
print("Old approach (2015):")
print("  - Throw fastball for strike one")
print("  - Then expand zone with breaking balls")
print()
print("New approach (2025):")
print("  - Mix in breaking balls from pitch one")
print("  - Keep hitters off-balance from the start")
print("  - Use sweeper as reliable strike pitch")
```

## What We Learned

Let's summarize what the data revealed:

1. **First pitch fastballs dropped 7.2%**: From 67.5% (2015) to 60.3% (2025)
2. **Breaking balls on 0-0 up 7.6%**: From 22.8% to 30.4%
3. **Strike rate slightly improved**: 49.5% → 50.5% despite fewer fastballs
4. **The trend is highly significant**: R² = 0.863, p < 0.001
5. **Modern breaking balls work on 0-0**: Sweepers and sliders get strikes

The old rule—"throw fastball strike one"—is no longer the default. Pitchers have learned they can start plate appearances with breaking balls and still get ahead. It's another piece of the breaking ball revolution.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/10_first_pitch/`

Try modifying the code to explore:
- How does first pitch strategy differ for starters vs relievers?
- Which pitchers have the most aggressive first-pitch breaking ball rates?
- How does first pitch outcome correlate with overall at-bat result?

```bash
cd chapters/10_first_pitch
python analysis.py
```
