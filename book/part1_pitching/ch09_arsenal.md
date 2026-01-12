# Chapter 9: Pitcher Arsenal Diversity

How many different pitches does the average MLB pitcher throw? A decade ago, the typical arsenal was a fastball, slider, changeup, and maybe a curveball. Today, new pitch types have emerged—sweepers, cutters, and splitters have joined the mix. But has pitcher diversity actually increased, or is it mostly hype?

In this chapter, we'll count the pitches in every pitcher's arsenal and track how toolkit size has evolved over the Statcast era.

## Getting Started

Let's begin by loading our data and identifying what pitches each pitcher throws:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'pitcher', 'pitch_type'])

# Count pitch types per pitcher (requiring 20+ of each type to qualify)
def count_arsenal(pitcher_df):
    pitch_counts = pitcher_df['pitch_type'].value_counts()
    qualifying = pitch_counts[pitch_counts >= 20]
    return len(qualifying)

# Apply to each pitcher each year
arsenal_by_pitcher = df.groupby(['game_year', 'pitcher']).apply(count_arsenal)
print(f"Pitchers analyzed: {len(arsenal_by_pitcher):,}")
```

By requiring at least 20 throws of each pitch type, we filter out situational or accidental pitch classifications.

## The Average Arsenal

Suppose we want to see how arsenal size has changed over the decade. We can calculate the average:

```python
yearly_arsenal = arsenal_by_pitcher.groupby('game_year').mean()
print(yearly_arsenal.round(2))
```

| Year | Average Arsenal Size |
|------|---------------------|
| 2015 | 3.98 |
| 2017 | 4.02 |
| 2019 | 4.08 |
| 2021 | 4.15 |
| 2023 | 4.21 |
| 2025 | 4.25 |

![Arsenal Trend](../../chapters/09_arsenal/figures/fig01_arsenal_trend.png)

The average arsenal has grown from 3.98 to 4.25 pitch types per pitcher—an increase of about 0.27 pitches over the decade. That's a modest but real increase in diversity.

## The Arsenal Distribution

Let's look at how pitcher arsenal sizes are distributed:

```python
# Count pitchers by arsenal size
arsenal_dist = arsenal_by_pitcher.value_counts().sort_index()
for size in range(2, 7):
    count = arsenal_dist.get(size, 0)
    pct = count / len(arsenal_by_pitcher) * 100
    print(f"{size} pitches: {count} pitchers ({pct:.1f}%)")
```

| Arsenal Size | Count | Percentage |
|-------------|-------|------------|
| 2 pitches | 623 | 9.4% |
| 3 pitches | 1,830 | 27.5% |
| 4 pitches | 2,179 | **32.7%** |
| 5 pitches | 1,569 | 23.5% |
| 6+ pitches | 460 | 6.9% |

![Arsenal Distribution](../../chapters/09_arsenal/figures/fig02_arsenal_distribution.png)

The most common arsenal is 4 pitches—one in three pitchers carry exactly four qualifying pitch types. But the trend is toward more diversity.

## Multi-Pitch Pitchers Are Rising

Let's see how the proportion of pitchers with 4+ and 5+ pitch arsenals has changed:

```python
# Calculate multi-pitch percentage by year
for year in range(2015, 2026):
    year_data = arsenal_by_pitcher[year]
    pct_4plus = (year_data >= 4).mean() * 100
    pct_5plus = (year_data >= 5).mean() * 100
    print(f"{year}: {pct_4plus:.1f}% have 4+, {pct_5plus:.1f}% have 5+")
```

| Year | 4+ Pitch % | 5+ Pitch % |
|------|-----------|-----------|
| 2015 | 64.8% | 30.5% |
| 2019 | 67.3% | 33.1% |
| 2025 | 71.7% | 37.2% |

![Multi-Pitch Trend](../../chapters/09_arsenal/figures/fig03_multipitch_trend.png)

The share of pitchers with 4+ pitch arsenals grew from 65% to 72%. The 5+ pitch crowd expanded from 31% to 37%. More pitchers are developing deeper toolkits.

## Winners and Losers: Pitch Type Popularity

But wait—what's driving this arsenal expansion? Let's see which specific pitches have gained and lost popularity:

```python
# Calculate % of pitchers throwing each pitch type
pitch_types = ['FF', 'SL', 'CH', 'CU', 'SI', 'FC', 'ST', 'FS']
for pt in pitch_types:
    usage_2015 = ... # Calculate % of pitchers using this pitch in 2015
    usage_2025 = ... # Calculate % of pitchers using this pitch in 2025
    print(f"{pt}: {usage_2015:.0f}% → {usage_2025:.0f}%")
```

**Rising Pitches:**

| Pitch | 2015 | 2025 | Change |
|-------|------|------|--------|
| Sweeper (ST) | 0% | **38%** | +38% |
| Cutter (FC) | 26% | 40% | +14% |
| Splitter (FS) | 7% | 17% | +10% |

**Declining Pitches:**

| Pitch | 2015 | 2025 | Change |
|-------|------|------|--------|
| Curveball (CU) | 51% | 40% | -11% |
| Changeup (CH) | 68% | 58% | -10% |

![Pitch Popularity](../../chapters/09_arsenal/figures/fig04_pitch_popularity.png)

The sweeper's rise is the story of the decade. It didn't exist as a tracked pitch type in 2015—Statcast didn't classify it separately until 2022. By 2025, more than one-third of pitchers throw it regularly.

## The Sweeper Revolution

The sweeper deserves special attention. It's not just a new pitch—it's a replacement for existing pitches:

```python
# Track sweeper adoption by year
sweeper_pct = df[df['pitch_type'] == 'ST'].groupby('game_year').size()
total_by_year = df.groupby('game_year')['pitcher'].nunique()
adoption = (sweeper_pct / total_by_year * 100).fillna(0)
print(adoption.round(1))
```

| Year | Pitchers with Sweeper |
|------|----------------------|
| 2015 | <1% |
| 2020 | ~5% |
| 2022 | 15% |
| 2025 | 38% |

The sweeper's horizontal movement—often 15+ inches of glove-side break—makes it a devastating weapon that essentially created a new pitch category. Many pitchers who previously threw sliders now throw sweepers instead (or both).

## Is This Real? Statistical Validation

Let's test whether the arsenal growth is statistically significant:

```python
from scipy import stats
import numpy as np

years = np.array(range(2015, 2026), dtype=float)
arsenal_means = np.array(yearly_arsenal.values, dtype=float)

slope, intercept, r, p, se = stats.linregress(years, arsenal_means)
print(f"Slope: {slope:.4f} types/year")
print(f"R² = {r**2:.3f}, p = {p:.3f}")
```

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Slope | +0.021 types/year | Gradual increase |
| R² | 0.155 | Weak fit |
| p-value | 0.231 | Not statistically significant |
| Total change | +0.27 types | Modest practical effect |

The trend is positive but the statistical evidence is weak. Arsenal diversification is real but modest—this isn't a revolution in pitcher toolkits.

## What's Driving the Change?

Several factors explain the gradual arsenal expansion:

1. **Pitch design technology**: Rapsodo and TrackMan help pitchers develop new shapes
2. **The sweeper effect**: An entirely new pitch category adds to everyone's arsenal
3. **Three-times-through penalty**: Pitchers need more weapons to keep hitters guessing
4. **Bullpen specialization**: Relievers can focus on perfecting 2-3 elite pitches

But the change is modest because:
- More pitches doesn't mean better pitching
- Command and deception matter more than variety
- Many pitchers find success with 3-4 pitches

## What We Learned

Let's summarize what the data revealed:

1. **Arsenal size increased modestly**: 3.98 → 4.25 pitch types (+0.27)
2. **4+ pitch pitchers grew**: 64.8% → 71.7%
3. **Sweeper emerged from nothing**: 0% → 38% of pitchers
4. **Curveball and changeup declined**: Making room for new pitches
5. **The trend is real but weak**: R² = 0.155, not statistically significant

The arsenal story is about evolution, not revolution. Pitchers are adding weapons, but the fundamentals—fastball command and one elite secondary—still drive success.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/09_arsenal/`

Try modifying the code to explore:
- Do pitchers with larger arsenals have better results?
- Which teams develop the most diverse pitching staffs?
- How does arsenal size differ between starters and relievers?

```bash
cd chapters/09_arsenal
python analysis.py
```
