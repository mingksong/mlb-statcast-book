# Chapter 2: The Velocity Arms Race

In 2015, the average four-seam fastball crossed the plate at 93.1 mph. By 2025, that number had climbed to 94.5 mph. This 1.4 mph increase may seem modest, but it represents one of the most significant shifts in baseball history—a decade-long arms race that has fundamentally changed how the game is played.

In this chapter, we explore this velocity evolution using Statcast data from 2015 to 2025. We examine not just the trend itself, but its magnitude, statistical significance, and implications for the future of pitching.

## Getting the Data

We begin by loading Statcast pitch-level data and filtering to four-seam fastballs.

```python
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['pitch_type', 'release_speed'])
    ff = df[df['pitch_type'] == 'FF']['release_speed'].dropna()

    n = len(ff)
    mean = ff.mean()
    std = ff.std()
    se = std / np.sqrt(n)

    results.append({
        'year': year,
        'count': n,
        'mean': mean,
        'std': std,
        'ci_lower': mean - 1.96 * se,
        'ci_upper': mean + 1.96 * se,
        'pct_95plus': (ff >= 95).mean() * 100
    })

velocity_df = pd.DataFrame(results)
```

The data contains over 2.5 million four-seam fastballs across 11 seasons—sufficient sample size to detect even small changes with high confidence.

## Average Velocity by Year

We calculate the mean velocity for each season:

```python
velocity_df[['year', 'mean', 'std', 'count']]
```

|year|mean|std|count|
|----|-----|-----|------|
|2015|93.12|2.84|249,546|
|2016|93.23|2.79|258,392|
|2017|93.23|2.79|248,933|
|2018|93.14|2.74|252,979|
|2019|93.39|2.63|263,386|
|2020|93.36|2.72|91,684|
|2021|93.70|2.52|251,958|
|2022|93.92|2.54|235,410|
|2023|94.16|2.47|230,247|
|2024|94.29|2.46|225,470|
|2025|94.49|2.53|226,062|

The progression is unmistakable. Average velocity increased from 93.12 mph in 2015 to 94.49 mph in 2025—a gain of 1.37 mph over the decade. Note that 2020's smaller sample reflects the COVID-shortened 60-game season.

## Visualizing the Trend

We plot the velocity trend with 95% confidence intervals in Figure 2.1.

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(velocity_df['year'], velocity_df['mean'], 'o-', linewidth=2, markersize=8,
        color='#1f77b4', label='Mean velocity')
ax.fill_between(velocity_df['year'], velocity_df['ci_lower'], velocity_df['ci_upper'],
                alpha=0.3, color='#1f77b4', label='95% CI')

# Add regression line
slope, intercept, r, p, se = stats.linregress(velocity_df['year'], velocity_df['mean'])
ax.plot(velocity_df['year'], intercept + slope * velocity_df['year'], '--',
        color='red', linewidth=2, label=f'Trend (R²={r**2:.3f})')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Average 4-Seam Fastball Velocity (mph)', fontsize=12)
ax.set_title('The Velocity Arms Race (2015-2025)', fontsize=14)
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig('figures/fig01_velocity_trend.png', dpi=150)
```

![Average four-seam fastball velocity increased from 93.1 mph (2015) to 94.5 mph (2025)](../../chapters/01_velocity_trend/figures/fig01_velocity_trend.png)

The confidence intervals are extremely narrow—barely visible at this scale—reflecting the large sample sizes. The upward trend is clear, though not perfectly linear: velocity stagnated from 2015-2018, then accelerated sharply from 2019 onward.

## The Rise of Elite Velocity

Perhaps more striking than the average is the shift at the top end of the distribution. We examine the percentage of fastballs thrown at 95+ mph:

```python
velocity_df[['year', 'pct_95plus']]
```

|year|pct_95plus|
|----|----------|
|2015|26.1%|
|2016|26.5%|
|2017|27.0%|
|2018|26.3%|
|2019|27.5%|
|2020|28.1%|
|2021|31.2%|
|2022|33.9%|
|2023|37.6%|
|2024|40.1%|
|2025|43.1%|

In 2015, roughly one in four fastballs reached 95 mph. By 2025, it was nearly one in two. This 17-percentage-point increase represents a fundamental shift in what constitutes a "normal" fastball.

We visualize this shift in Figure 2.2.

```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(velocity_df['year'], velocity_df['pct_95plus'],
       color='#ff7f0e', edgecolor='black', linewidth=0.5)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Percentage of 4-Seamers at 95+ mph', fontsize=12)
ax.set_title('Rise of Elite Velocity', fontsize=14)
ax.set_ylim(0, 50)
plt.tight_layout()
plt.savefig('figures/fig02_95plus_percentage.png', dpi=150)
```

![The percentage of fastballs at 95+ mph increased from 26% to 43%](../../chapters/01_velocity_trend/figures/fig02_95plus_percentage.png)

## Statistical Validation

We confirm the trend with linear regression:

```python
years = velocity_df['year'].values
means = velocity_df['mean'].values

slope, intercept, r_value, p_value, std_err = stats.linregress(years, means)
r_squared = r_value ** 2
slope_ci_lower = slope - 1.96 * std_err
slope_ci_upper = slope + 1.96 * std_err
```

|Metric|Value|Interpretation|
|------|-----|--------------|
|Slope|+0.144 mph/year|Consistent annual increase|
|Slope 95% CI|[0.113, 0.174]|Robust estimate|
|R²|0.905|Strong fit|
|p-value|6.92e-06|Highly significant|

The R² of 0.905 indicates that year alone explains over 90% of the variance in average velocity—an exceptionally strong relationship for real-world data. The trend is highly significant (p < 0.001).

## Period Comparison

We compare the early period (2015-2017) to the late period (2023-2025) using a two-sample t-test:

```python
early_data, late_data = [], []

for year in [2015, 2016, 2017]:
    df = load_season(year, columns=['pitch_type', 'release_speed'])
    early_data.extend(df[df['pitch_type'] == 'FF']['release_speed'].dropna())

for year in [2023, 2024, 2025]:
    df = load_season(year, columns=['pitch_type', 'release_speed'])
    late_data.extend(df[df['pitch_type'] == 'FF']['release_speed'].dropna())

early, late = np.array(early_data), np.array(late_data)

t_stat, p_value = stats.ttest_ind(early, late)

pooled_std = np.sqrt(((len(early)-1)*early.std()**2 + (len(late)-1)*late.std()**2) /
                      (len(early) + len(late) - 2))
cohens_d = (late.mean() - early.mean()) / pooled_std
```

|Metric|Value|
|------|-----|
|Early Period Mean (2015-17)|93.19 mph|
|Late Period Mean (2023-25)|94.32 mph|
|Difference|+1.12 mph|
|95% CI for Difference|[1.12, 1.13] mph|
|t-statistic|-252.98|
|p-value|<0.001|
|Cohen's d|0.422|

The effect size (Cohen's d = 0.42) falls in the "small to medium" range. One criticism of effect size measures is that with very large samples, even small practical differences become statistically significant. However, the 1.12 mph difference is meaningful in baseball terms—it reduces batter reaction time by approximately 4 milliseconds.

## Distribution Shift

We compare the full velocity distributions between 2015 and 2025 in Figure 2.3.

```python
df_2015 = load_season(2015, columns=['pitch_type', 'release_speed'])
df_2025 = load_season(2025, columns=['pitch_type', 'release_speed'])

ff_2015 = df_2015[df_2015['pitch_type'] == 'FF']['release_speed'].dropna()
ff_2025 = df_2025[df_2025['pitch_type'] == 'FF']['release_speed'].dropna()

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(ff_2015, bins=50, alpha=0.6, label='2015', density=True, color='#1f77b4')
ax.hist(ff_2025, bins=50, alpha=0.6, label='2025', density=True, color='#ff7f0e')
ax.axvline(ff_2015.mean(), color='#1f77b4', linestyle='--', linewidth=2)
ax.axvline(ff_2025.mean(), color='#ff7f0e', linestyle='--', linewidth=2)
ax.set_xlabel('Velocity (mph)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Velocity Distribution Shift: 2015 vs 2025', fontsize=14)
ax.legend(fontsize=11)
ax.set_xlim(80, 105)
plt.tight_layout()
plt.savefig('figures/fig03_distribution_comparison.png', dpi=150)
```

![The entire velocity distribution shifted rightward from 2015 to 2025](../../chapters/01_velocity_trend/figures/fig03_distribution_comparison.png)

The entire distribution has shifted rightward. This is not simply a case of elite pitchers throwing harder—the increase has occurred across all velocity levels.

## Summary

The velocity arms race is real and substantial:

1. **Average velocity increased 1.37 mph** from 93.12 (2015) to 94.49 (2025)
2. **Elite velocity (95+ mph) nearly doubled** from 26% to 43% of fastballs
3. **The trend is highly significant** (R² = 0.905, p < 0.001)
4. **Effect size is meaningful** (Cohen's d = 0.42)
5. **The entire distribution shifted** not just the top end
6. **Acceleration occurred post-2019** after a plateau from 2015-2018

What drove this change? The answers include advances in biomechanics, training technology, and organizational emphasis on velocity. The consequences—rising strikeouts, pitcher injuries, shortened outings—ripple through every aspect of the modern game.

## Further Reading

- Boddy, K. (2018). *Hacking the Kinetic Chain*. Driveline Baseball.
- Arthur, R. (2016). "The New Science of Building Baseball Superstars." *FiveThirtyEight*.

## Exercises

1. Extend this analysis to sinkers (SI) and cutters (FC). Do they show similar velocity trends?

2. Calculate the 90th percentile velocity by year. Has the gap between average and elite pitchers widened or narrowed?

3. The 2020 season was shortened to 60 games. Remove it from the regression and recalculate R². Does it meaningfully change the results?

```bash
cd chapters/01_velocity_trend
python analysis.py
```
