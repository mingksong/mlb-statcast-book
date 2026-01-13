# Chapter 18: Hard Hit Rate Revisited

Hard hit rate—the percentage of batted balls with exit velocity of 95+ mph—has remained stable at approximately 24-26% since 2016. The apparent 2015 outlier (31.8%) reflects Statcast calibration issues, not exceptional contact quality. Excluding 2015, the data shows no meaningful trend (slope = -0.05%/year, R² = 0.01, p = 0.791). This chapter examines hard hit rate as a contact quality metric and its relationship to the more sophisticated barrel rate.

## Getting the Data

We begin by loading batted ball data and calculating hard hit rate.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['launch_speed', 'launch_angle', 'events'])

    # Filter to batted balls
    batted = df[df['launch_speed'].notna()]

    # Define hard hit (95+ mph)
    hard_hit = (batted['launch_speed'] >= 95)

    results.append({
        'year': year,
        'hard_hit_rate': hard_hit.mean() * 100,
        'hard_hit_count': hard_hit.sum(),
        'mean_ev': batted['launch_speed'].mean(),
        'n_batted': len(batted),
    })

hhr_df = pd.DataFrame(results)
```

The dataset contains over 2 million batted balls across 11 seasons.

## Hard Hit Rate by Year

We calculate the hard hit rate for each season.

```python
hhr_df[['year', 'hard_hit_rate', 'mean_ev']]
```

|year|Hard Hit Rate|Avg EV|
|----|-------------|------|
|2015|31.8%|87.1 mph|
|2016|26.3%|84.1 mph|
|2017|24.0%|82.1 mph|
|2019|25.9%|83.9 mph|
|2021|23.7%|82.2 mph|
|2023|24.1%|82.6 mph|
|2025|25.5%|83.1 mph|

The 2015 hard hit rate (31.8%) stands apart from all subsequent years. This mirrors the exit velocity anomaly identified in Chapter 15—Statcast's first-year calibration systematically inflated readings.

## Visualizing Hard Hit Rate

We plot the hard hit rate trend in Figure 18.1.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(hhr_df['year'], hhr_df['hard_hit_rate'], 'o-',
        linewidth=2, markersize=8, color='#1f77b4')
ax.axhline(y=hhr_df[hhr_df['year'] >= 2016]['hard_hit_rate'].mean(),
           color='red', linestyle='--',
           label=f'Mean (2016+): {hhr_df[hhr_df["year"] >= 2016]["hard_hit_rate"].mean():.1f}%')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Hard Hit Rate (%)', fontsize=12)
ax.set_title('Hard Hit Rate (95+ mph) by Year', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig01_hard_hit_trend.png', dpi=150)
```

![Hard hit rate dropped after 2015 and has remained stable around 24-25%](../../chapters/18_hard_hit/figures/fig01_hard_hit_trend.png)

The 2015 outlier dominates the visual. From 2016 onward, hard hit rate has fluctuated within a narrow band.

## Post-2015 Analysis

We examine the trend excluding the anomalous 2015 season.

```python
post_2015 = hhr_df[hhr_df['year'] >= 2016]

mean_hhr = post_2015['hard_hit_rate'].mean()
std_hhr = post_2015['hard_hit_rate'].std()
min_hhr = post_2015['hard_hit_rate'].min()
max_hhr = post_2015['hard_hit_rate'].max()
```

|Statistic|Value|
|---------|-----|
|Mean (2016-2025)|24.6%|
|Std Dev|1.0%|
|Minimum (2022)|23.6%|
|Maximum (2016)|26.3%|

From 2016-2025, hard hit rate has varied by less than 3 percentage points—essentially noise around a stable baseline.

## Statistical Validation

We test for trends in both the full dataset and post-2015 only.

```python
# Full period
years_all = hhr_df['year'].values
rates_all = hhr_df['hard_hit_rate'].values
slope_all, int_all, r_all, p_all, se_all = stats.linregress(years_all, rates_all)

# Post-2015 only
years_post = hhr_df[hhr_df['year'] >= 2016]['year'].values
rates_post = hhr_df[hhr_df['year'] >= 2016]['hard_hit_rate'].values
slope_post, int_post, r_post, p_post, se_post = stats.linregress(years_post, rates_post)
```

|Period|Slope|R²|p-value|Interpretation|
|------|-----|--|-------|--------------|
|2015-2025|-0.52%/year|0.37|0.052|Marginally significant|
|2016-2025|-0.05%/year|0.01|0.791|**No trend**|

The full period shows marginal significance (p = 0.052), but this is driven entirely by the 2015 outlier. Excluding 2015, there is no trend whatsoever.

## Hard Hit vs. Barrel

We compare hard hit rate to barrel rate to understand the relationship.

```python
# Hard hit includes all launch angles
# Barrels require optimal launch angle
# This creates a 5:1 ratio difference

hard_hit_rate = 25  # %
barrel_rate = 5     # %
ratio = hard_hit_rate / barrel_rate  # 5x more hard-hit than barrels
```

|Metric|Definition|Rate|Typical Outcome|
|------|----------|----|----|
|Hard Hit|95+ mph, any angle|~25%|Mixed|
|Barrel|98+ mph, optimal angle|~5%|.755 xBA, 65% HR|

Hard hit captures approximately 5x more batted balls than barrels because it ignores launch angle. A 100 mph grounder counts as "hard hit" but not as a barrel—and that grounder is typically an out.

## Hard Hit Breakdown by Launch Angle

We analyze what happens to hard-hit balls at different angles.

```python
# Load 2025 data for breakdown
df_2025 = load_season(2025, columns=['launch_speed', 'launch_angle'])
batted = df_2025.dropna(subset=['launch_speed', 'launch_angle'])
hard_hit = batted[batted['launch_speed'] >= 95]

gb = (hard_hit['launch_angle'] < 10).mean() * 100
ld = ((hard_hit['launch_angle'] >= 10) & (hard_hit['launch_angle'] < 25)).mean() * 100
fb = ((hard_hit['launch_angle'] >= 25) & (hard_hit['launch_angle'] < 50)).mean() * 100
pu = (hard_hit['launch_angle'] >= 50).mean() * 100
```

|Launch Angle Category|% of Hard Hit Balls|Typical Outcome|
|---------------------|-------------------|---------------|
|Ground Ball (<10°)|~30%|Often outs|
|Line Drive (10-25°)|~35%|Excellent|
|Fly Ball (25-50°)|~30%|Good to excellent|
|Pop Up (50°+)|~5%|Almost always out|

Approximately 35% of hard-hit balls are ground balls or pop-ups—hard contact that does not lead to good outcomes. This is why barrel rate, despite being more complex, is often a better predictor of success.

## Practical Limitations

Hard hit rate has become a staple of broadcast analytics due to its simplicity, but it has meaningful limitations:

1. **Ignores launch angle**: A 95 mph grounder is not equivalent to a 95 mph line drive
2. **Single threshold**: 94.9 mph counts as soft, 95.0 mph counts as hard
3. **No outcome weighting**: Does not distinguish between home runs and double plays

For serious analysis, barrel rate and expected statistics (xBA, xSLG) provide superior predictive value.

## Summary

Hard hit rate reveals the stability of contact quality:

1. **Post-2015 rate stable at ~25%** with minimal variation
2. **2015 was anomalous** (31.8% driven by calibration issues)
3. **No meaningful trend** (p = 0.791 post-2015)
4. **30-35% are poor outcomes** (hard-hit grounders and pop-ups)
5. **Barrel rate is superior** (captures quality better than quantity)
6. **Simple metric, limited insight** (good for broadcasts, not deep analysis)

Hard hit rate serves as baseball's "good enough" metric—easy to understand and widely available, but telling only part of the contact quality story.

## Further Reading

- Sullivan, J. (2018). "Hard Hit vs. Barrel: What Matters More?" *FanGraphs*.
- Petriello, M. (2019). "Understanding Contact Quality Metrics." *MLB.com*.

## Exercises

1. Identify the 20 hitters with the highest hard hit rates in 2025. What percentage of their hard-hit balls were barrels?

2. Calculate hard hit rate by pitch location. Do hitters make harder contact on pitches in certain zones?

3. Compare hard hit rate to barrel rate as predictors of home runs. Which metric shows stronger correlation?

```bash
cd chapters/18_hard_hit
python analysis.py
```
