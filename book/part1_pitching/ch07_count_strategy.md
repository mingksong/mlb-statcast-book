# Chapter 7: Count-Based Pitch Selection

What does a pitcher throw on 3-0? If you guessed "fastball," you're right—93% of the time. But why? And how does pitch selection change as the count evolves through an at-bat?

In this chapter, we'll decode the strategic calculus behind count-based pitching, revealing how pitchers balance the risk of walks against the need for deception.

## Getting Started

Let's begin by loading our pitch data with count information:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'pitch_type', 'balls', 'strikes'])

# Categorize pitch types
fastballs = ['FF', 'SI', 'FC']
breaking = ['SL', 'CU', 'ST', 'KC']
offspeed = ['CH', 'FS']

df['category'] = df['pitch_type'].apply(
    lambda x: 'Fastball' if x in fastballs
    else 'Breaking' if x in breaking
    else 'Offspeed'
)
print(f"Total pitches with count data: {len(df):,}")
```

With millions of pitches, we can map exactly how strategy shifts from 0-0 to 3-2.

## The Count Matrix

Suppose we want to see how fastball percentage changes across all 12 possible counts. We can create a complete pitch selection matrix:

```python
# Create count matrix
for balls in range(4):
    for strikes in range(3):
        count_data = df[(df['balls'] == balls) & (df['strikes'] == strikes)]
        fb_pct = (count_data['category'] == 'Fastball').mean() * 100
        print(f"{balls}-{strikes}: {fb_pct:.1f}%")
```

The results reveal a clear pattern:

| Count | Fastball % | Breaking % | Offspeed % |
|-------|-----------|------------|------------|
| 0-0 | 63.0% | 28.1% | 8.2% |
| 0-1 | 53.6% | 30.6% | 15.1% |
| 0-2 | 48.2% | 37.8% | 13.1% |
| 1-0 | 62.2% | 22.9% | 14.0% |
| 1-1 | 53.6% | 28.9% | 16.8% |
| 1-2 | 47.6% | 36.8% | 14.8% |
| 2-0 | 74.4% | 14.4% | 10.0% |
| 2-1 | 62.2% | 22.7% | 14.6% |
| 2-2 | 51.6% | 32.5% | 15.3% |
| 3-0 | **93.0%** | 2.8% | 1.8% |
| 3-1 | 80.0% | 12.0% | 7.5% |
| 3-2 | 64.6% | 23.5% | 11.4% |

![Fastball by Count](../../chapters/07_count_strategy/figures/fig01_fastball_by_count.png)

Look at the pattern: as balls increase, fastball percentage jumps dramatically. The count is the single biggest factor determining what pitch comes next.

## The 3-0 Extreme

The 3-0 count deserves special attention. At 93% fastballs, it's essentially a one-pitch count:

```python
# Focus on 3-0 count
count_30 = df[(df['balls'] == 3) & (df['strikes'] == 0)]
fb_30 = (count_30['category'] == 'Fastball').mean() * 100
print(f"3-0 fastball percentage: {fb_30:.1f}%")

# Compare to 0-2 count
count_02 = df[(df['balls'] == 0) & (df['strikes'] == 2)]
fb_02 = (count_02['category'] == 'Fastball').mean() * 100
print(f"0-2 fastball percentage: {fb_02:.1f}%")
print(f"Difference: {fb_30 - fb_02:.1f} percentage points")
```

The gap is staggering: 93% fastballs on 3-0 versus 48% on 0-2. That's a **45 percentage point swing** based purely on count.

Why such extreme predictability? The math is simple:
- Ball four = guaranteed baserunner
- Breaking ball = higher risk of missing the zone
- Fastball = most controllable pitch

On 3-0, pitchers are telling hitters: "Here's a fastball. Try to hit it." The risk of walking is so high that deception isn't worth attempting.

## Hitter's Counts vs Pitcher's Counts

Let's formalize this by comparing hitter-favorable counts to pitcher-favorable counts:

```python
# Define count types
hitter_counts = [(1,0), (2,0), (2,1), (3,0), (3,1)]  # More balls
pitcher_counts = [(0,1), (0,2), (1,2)]  # More strikes

hitter_fb = df[df.apply(lambda x: (x['balls'], x['strikes']) in hitter_counts, axis=1)]
pitcher_fb = df[df.apply(lambda x: (x['balls'], x['strikes']) in pitcher_counts, axis=1)]

print(f"Hitter's counts: {(hitter_fb['category'] == 'Fastball').mean()*100:.1f}% fastballs")
print(f"Pitcher's counts: {(pitcher_fb['category'] == 'Fastball').mean()*100:.1f}% fastballs")
```

| Count Type | Fastball % | Breaking % |
|------------|-----------|------------|
| Hitter's counts | 67.4% | 18.8% |
| Pitcher's counts | 50.4% | 34.9% |
| **Difference** | **+17.0%** | **-16.1%** |

![Pitcher vs Hitter Counts](../../chapters/07_count_strategy/figures/fig02_pitcher_vs_hitter_counts.png)

A 17 percentage point swing in fastball usage between count types. When hitters have the advantage, they know fastballs are coming—and yet pitchers still throw them because the alternative (walking) is worse.

## Two-Strike Strategy

With two strikes, the calculus flips completely. Now pitchers can afford to throw chase pitches—balls that look like strikes but break out of the zone:

```python
# Compare breaking ball usage by strike count
zero_one_strikes = df[df['strikes'].isin([0, 1])]
two_strikes = df[df['strikes'] == 2]

brk_01 = (zero_one_strikes['category'] == 'Breaking').mean() * 100
brk_2 = (two_strikes['category'] == 'Breaking').mean() * 100
print(f"Breaking ball% (0-1 strikes): {brk_01:.1f}%")
print(f"Breaking ball% (2 strikes): {brk_2:.1f}%")
print(f"Increase: +{brk_2 - brk_01:.1f}%")
```

| Strike Count | Breaking Ball % |
|--------------|----------------|
| 0-1 strikes | 26.0% |
| 2 strikes | 33.6% |
| **Increase** | **+7.6%** |

![Two-Strike Strategy](../../chapters/07_count_strategy/figures/fig03_two_strike_strategy.png)

That 7.6% increase represents millions of sliders and curveballs designed to get hitters swinging at air. With two strikes, a strikeout is one pitch away, and pitchers save their best chase pitches for exactly this moment.

## How Has Strategy Evolved?

Let's see if count strategy has changed over the decade:

```python
from scipy import stats
import numpy as np

# First pitch fastball trend
first_pitch = df[(df['balls'] == 0) & (df['strikes'] == 0)]
yearly_fp = first_pitch.groupby('game_year').apply(
    lambda x: (x['category'] == 'Fastball').mean() * 100
)

years = np.array(yearly_fp.index, dtype=float)
values = np.array(yearly_fp.values, dtype=float)
slope, intercept, r, p, se = stats.linregress(years, values)
print(f"First pitch FB trend: {slope:.2f}%/year (R²={r**2:.3f})")
```

| Trend | Metric | Value |
|-------|--------|-------|
| First pitch fastball | Slope | -0.77%/year |
| | R² | 0.863 |
| | Change (2015→2025) | -7.2% |

![Yearly Trends](../../chapters/07_count_strategy/figures/fig04_yearly_trends.png)

First pitch fastball percentage has dropped by 7.2% over the decade. Pitchers are becoming more aggressive early, throwing more breaking balls on the first pitch to steal strikes.

Meanwhile, 3-0 fastball percentage has actually increased—from 85% to 93%. The extremes are becoming more extreme.

## Is This Real? Statistical Validation

Let's confirm the hitter vs pitcher count difference:

```python
from scipy.stats import chi2_contingency
import pandas as pd

# Chi-square test for count type vs pitch category
contingency = pd.crosstab(
    df['count_type'],  # hitter vs pitcher
    df['category']     # fastball vs breaking vs offspeed
)
chi2, p, dof, expected = chi2_contingency(contingency)
cramers_v = np.sqrt(chi2 / (len(df) * (min(contingency.shape) - 1)))
print(f"Chi-square = {chi2:.2f}, p = {p:.2e}")
print(f"Cramer's V = {cramers_v:.3f}")
```

| Test | Value | Interpretation |
|------|-------|----------------|
| Chi-square | 109,187 | |
| p-value | < 0.001 | Highly significant |
| Cramer's V | 0.170 | Moderate association |

With a p-value effectively at zero and Cramer's V of 0.17, the count-pitch relationship is both statistically significant and practically meaningful.

## What We Learned

Let's summarize what the data revealed:

1. **Count determines strategy**: 17% more fastballs in hitter's counts vs pitcher's counts
2. **3-0 is essentially one pitch**: 93% fastballs—pitchers prioritize strikes over deception
3. **Two strikes enable aggression**: Breaking ball usage jumps 7.6% with two strikes
4. **First pitch is evolving**: 7.2% fewer fastballs on 0-0 compared to 2015
5. **Extremes are intensifying**: 3-0 counts more predictable, early counts more aggressive

The count is the invisible hand guiding every pitch selection. Understanding this pattern reveals the strategic chess match happening within each at-bat.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/07_count_strategy/`

Try modifying the code to explore:
- How does count strategy differ for starters vs relievers?
- Which pitchers deviate most from the typical count patterns?
- How does count strategy change in high-leverage situations?

```bash
cd chapters/07_count_strategy
python analysis.py
```
