# Chapter 19: The Sweet Spot Trade-Off

Sweet spot rate—the percentage of batted balls launched between 8-32 degrees—has declined from 33.9% to 30.4% since 2015. This decline (slope = -0.46%/year, R² = 0.50, p = 0.021) represents a strategic trade-off: hitters sacrificed optimal contact angle for elevation, accepting more pop-ups in exchange for more home run opportunities. This chapter examines how the launch angle revolution changed the sweet spot landscape.

## Getting the Data

We begin by loading batted ball data and calculating sweet spot rate.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['launch_angle', 'launch_speed',
                                     'estimated_ba_using_speedangle', 'events'])

    # Filter to batted balls with launch angle data
    batted = df[df['launch_angle'].notna()]

    # Define sweet spot (8-32 degrees)
    sweet_spot = (batted['launch_angle'] >= 8) & (batted['launch_angle'] <= 32)

    # Define other zones for comparison
    ground_ball = batted['launch_angle'] < 8
    popup = batted['launch_angle'] > 50
    fly_ball = (batted['launch_angle'] > 32) & (batted['launch_angle'] <= 50)

    results.append({
        'year': year,
        'sweet_spot_rate': sweet_spot.mean() * 100,
        'sweet_spot_count': sweet_spot.sum(),
        'gb_rate': ground_ball.mean() * 100,
        'popup_rate': popup.mean() * 100,
        'fb_rate': fly_ball.mean() * 100,
        'n_batted': len(batted),
    })

ss_df = pd.DataFrame(results)
```

The dataset contains over 2.1 million batted balls with launch angle data across the Statcast era.

## Sweet Spot Rate by Year

We calculate sweet spot rate for each season.

```python
ss_df[['year', 'sweet_spot_rate', 'sweet_spot_count']]
```

|year|Sweet Spot Rate|Sweet Spot Count|
|----|---------------|----------------|
|2015|33.9%|51,322|
|2016|33.0%|62,528|
|2017|34.6%|68,968|
|2018|34.0%|68,417|
|2019|34.2%|68,855|
|2020|27.1%|21,118|
|2021|30.2%|70,092|
|2022|30.1%|70,990|
|2023|30.1%|71,340|
|2024|29.9%|71,030|
|2025|30.4%|71,605|

Sweet spot rate dropped from approximately 34% in the late 2010s to approximately 30% in the 2020s—a 4 percentage point decline. The 2020 season (27.1%) reflects the COVID-shortened schedule rather than a genuine strategic shift.

## Visualizing Sweet Spot Rate

We plot the sweet spot trend in Figure 19.1.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

# Exclude 2020 for trend line
non_covid = ss_df[ss_df['year'] != 2020]

ax.plot(ss_df['year'], ss_df['sweet_spot_rate'], 'o-',
        linewidth=2, markersize=8, color='#1f77b4')

slope, intercept, r, p, se = stats.linregress(non_covid['year'], non_covid['sweet_spot_rate'])
ax.plot(non_covid['year'], intercept + slope * non_covid['year'], '--',
        color='red', linewidth=2, label=f'Trend: {slope:.2f}%/year')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Sweet Spot Rate (%)', fontsize=12)
ax.set_title('Sweet Spot Rate (8-32°) by Year', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig01_sweet_spot_trend.png', dpi=150)
```

![Sweet spot rate declined from 34% to 30% over the decade, with 2020 as an outlier](../../chapters/19_sweet_spot/figures/fig01_sweet_spot_trend.png)

The downward trend is clear: hitters are finding the optimal launch angle zone less frequently despite—or because of—their emphasis on elevation.

## Period Comparison

We compare sweet spot rate between the pre-2020 and post-2020 eras.

```python
# Calculate period averages (excluding 2020)
pre_2020 = ss_df[ss_df['year'].isin([2015, 2016, 2017, 2018, 2019])]
post_2020 = ss_df[ss_df['year'].isin([2021, 2022, 2023, 2024, 2025])]

pre_mean = pre_2020['sweet_spot_rate'].mean()
post_mean = post_2020['sweet_spot_rate'].mean()
```

|Period|Sweet Spot Rate|Sample Size|
|------|---------------|-----------|
|2015-2019|34.0%|320,090|
|2021-2025|30.1%|355,057|
|Decline|**-3.9 pp**|—|

A 4 percentage point decline represents approximately 80 fewer sweet spot balls per 2,000 batted balls—roughly one fewer optimal contact per game per team.

## The Trade-Off Revealed

We examine how launch angle distribution changed alongside sweet spot rate.

```python
ss_df[['year', 'gb_rate', 'sweet_spot_rate', 'fb_rate', 'popup_rate']]
```

|Year|Ground Ball|Sweet Spot|Fly Ball|Pop Up|
|----|-----------|----------|--------|------|
|2015|48.1%|33.9%|10.0%|7.9%|
|2019|39.8%|34.2%|14.0%|12.0%|
|2025|38.1%|30.4%|14.4%|17.1%|

|Zone|2015|2025|Change|
|----|----|----|------|
|Ground Ball (<8°)|48.1%|38.1%|-10.0%|
|Sweet Spot (8-32°)|33.9%|30.4%|-3.5%|
|Fly Ball (32-50°)|10.0%|14.4%|+4.4%|
|Pop Up (>50°)|7.9%|17.1%|+9.2%|

The mathematics reveal the trade-off: the 10% reduction in ground balls split between fly balls (+4.4%) and pop-ups (+9.2%), with sweet spot rate declining by 3.5%. Hitters elevated out of ground balls but often over-elevated into pop-ups, sacrificing some optimal contact in the process.

## Statistical Validation

We test for a trend in sweet spot rate, excluding the anomalous 2020 season.

```python
# Exclude 2020
non_covid = ss_df[ss_df['year'] != 2020]
years = non_covid['year'].values
rates = non_covid['sweet_spot_rate'].values

slope, intercept, r, p, se = stats.linregress(years, rates)

# Cohen's d for period comparison
pooled_std = np.sqrt((pre_2020['sweet_spot_rate'].var() + post_2020['sweet_spot_rate'].var()) / 2)
cohens_d = (post_mean - pre_mean) / pooled_std
```

|Metric|Value|Interpretation|
|------|-----|--------------|
|Slope|-0.46%/year|Declining|
|R²|0.50|Moderate fit|
|p-value|0.021|**Significant**|
|Cohen's d|-2.4|**Very large**|

The decline is statistically significant (p = 0.021) with a large effect size. This is not random variation—hitters systematically hit fewer balls in the optimal zone now than they did a decade ago.

## Expected Outcomes by Zone

We examine why this trade-off might make strategic sense.

```python
# Load 2025 data for outcome analysis
df_2025 = load_season(2025, columns=['launch_angle', 'launch_speed',
                                      'estimated_ba_using_speedangle', 'events'])
batted = df_2025.dropna(subset=['launch_angle', 'estimated_ba_using_speedangle'])

# Define zones
batted['zone'] = pd.cut(batted['launch_angle'],
                        bins=[-90, 8, 32, 50, 90],
                        labels=['Ground Ball', 'Sweet Spot', 'Fly Ball', 'Pop Up'])

zone_outcomes = batted.groupby('zone')['estimated_ba_using_speedangle'].agg(['mean', 'count'])
```

|Zone|xBA|HR Potential|
|----|---|------------|
|Ground Ball (<8°)|~.220|Minimal|
|Sweet Spot (8-32°)|~.500|Moderate|
|Fly Ball (32-50°)|~.200|**High**|
|Pop Up (>50°)|~.050|None|

Sweet spot balls produce the highest expected batting average (.500+), but they rarely become home runs—most result in singles and doubles. Fly balls between 32-50° have lower xBA but account for most home runs. For power hitters, accepting a lower sweet spot rate in exchange for more fly balls in the home run zone represents a rational strategic choice.

## The Strategic Calculation

We quantify the run value implications of this trade-off.

```python
# Approximate run values
# Sweet spot: ~0.35 runs per ball (high xBA, mostly singles/doubles)
# Fly ball: ~0.25 runs per ball (lower xBA but HR upside)
# Pop up: ~-0.10 runs per ball (almost always out)

# Per 1000 batted balls:
# 2015: 339 sweet spot, 100 FB, 79 popup
# 2025: 304 sweet spot, 144 FB, 171 popup

# Value change per 1000 BB:
# Sweet spot: -35 × 0.35 = -12.25 runs
# Fly ball: +44 × 0.25 = +11.0 runs
# Pop up: +92 × -0.10 = -9.2 runs
# Net: -10.45 runs per 1000 BB

# But this ignores HR upside for fly balls
# With 15% HR rate on fly balls at 1.4 runs/HR:
# +44 × 0.15 × 1.4 = +9.24 additional runs
# Net for power hitters: approximately break-even
```

For power hitters who can convert fly balls into home runs at above-average rates, the trade-off is approximately value-neutral. For contact-oriented hitters without home run power, the trade-off is negative. This helps explain the polarization of hitting approaches.

## Summary

Sweet spot rate reveals the hidden cost of the launch angle revolution:

1. **Sweet spot rate declined 3.5 pp** from 33.9% to 30.4%
2. **Trend is statistically significant** (p = 0.021, R² = 0.50)
3. **Ground balls converted to pop-ups** more than to optimal fly balls
4. **Strategic trade-off** favors power hitters over contact hitters
5. **2020 was anomalous** (27.1% driven by COVID disruption)
6. **Approximately break-even** for hitters who can hit home runs

The sweet spot story illustrates a fundamental truth: optimization has trade-offs. Hitters cannot maximize both contact quality and launch angle simultaneously. The modern game chose power, accepting more pop-ups in exchange for more home runs. Whether that trade-off was wise depends on the individual hitter's skill set.

## Further Reading

- Sullivan, J. (2018). "The Sweet Spot Paradox." *FanGraphs*.
- Carleton, R. (2019). "Launch Angle Optimization and Its Costs." *Baseball Prospectus*.

## Exercises

1. Identify the 20 hitters with the highest sweet spot rates in 2025. How does their home run rate compare to league average?

2. Calculate sweet spot rate by pitch type. Do hitters find the sweet spot more often against fastballs or breaking balls?

3. Examine the relationship between sweet spot rate and batting average. Is sweet spot rate a better predictor than hard hit rate?

```bash
cd chapters/19_sweet_spot
python analysis.py
```
