# Chapter 16: The Launch Angle Revolution

Average launch angle increased from 11.7° in 2015 to 17.8° in 2025—a 6.1 degree shift that fundamentally changed baseball offense. Ground ball rate dropped from 48.1% to 38.1%, while fly ball rate rose from 22.8% to 26.3%. This strategic transformation—not harder contact—explains the power surge of the late 2010s. This chapter examines how hitters learned to lift the ball and the trade-offs that came with elevation.

## Getting the Data

We begin by loading batted ball data with launch angle measurements.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['launch_angle', 'launch_speed', 'events', 'bb_type'])

    # Filter to batted balls with launch angle data
    batted = df[df['launch_angle'].notna()]

    # Classify batted ball types
    gb = (batted['launch_angle'] < 10).mean() * 100
    ld = ((batted['launch_angle'] >= 10) & (batted['launch_angle'] < 25)).mean() * 100
    fb = ((batted['launch_angle'] >= 25) & (batted['launch_angle'] < 50)).mean() * 100
    pu = (batted['launch_angle'] >= 50).mean() * 100

    # Sweet spot rate (8-32 degrees)
    sweet_spot = ((batted['launch_angle'] >= 8) & (batted['launch_angle'] <= 32)).mean() * 100

    results.append({
        'year': year,
        'mean_la': batted['launch_angle'].mean(),
        'median_la': batted['launch_angle'].median(),
        'gb_rate': gb,
        'ld_rate': ld,
        'fb_rate': fb,
        'popup_rate': pu,
        'sweet_spot': sweet_spot,
        'n_batted': len(batted),
    })

la_df = pd.DataFrame(results)
```

The dataset contains over 2.1 million batted balls with launch angle data.

## Launch Angle by Year

We calculate average launch angle for each season.

```python
la_df[['year', 'mean_la', 'median_la']]
```

|year|Mean LA|Median LA|
|----|-------|---------|
|2015|11.7°|12°|
|2016|16.2°|17°|
|2017|16.5°|18°|
|2019|16.6°|18°|
|2021|16.8°|20°|
|2023|16.8°|19°|
|2025|17.8°|20°|

Average launch angle increased by 6.1 degrees over the decade. The jump from 2015 to 2016 alone was 4.5 degrees—a combination of Statcast calibration changes and genuine strategic shift.

## Visualizing Launch Angle

We plot the launch angle trend in Figure 16.1.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(la_df['year'], la_df['mean_la'], 'o-', linewidth=2, markersize=8, color='#1f77b4')

slope, intercept, r, p, se = stats.linregress(la_df['year'], la_df['mean_la'])
ax.plot(la_df['year'], intercept + slope * la_df['year'], '--',
        color='red', linewidth=2, label=f'Trend: +{slope:.2f}°/year')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Average Launch Angle (degrees)', fontsize=12)
ax.set_title('Launch Angle (2015-2025)', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig01_la_trend.png', dpi=150)
```

![Launch angle increased from 11.7° to 17.8° over the decade](../../chapters/16_launch_angle/figures/fig01_la_trend.png)

The upward trend is clear: hitters have systematically elevated their batted balls across the Statcast era.

## Batted Ball Type Distribution

We examine how the shift affected batted ball types.

```python
la_df[['year', 'gb_rate', 'ld_rate', 'fb_rate', 'popup_rate']]
```

|year|Ground Ball|Line Drive|Fly Ball|Pop Up|
|----|-----------|----------|--------|------|
|2015|48.1%|21.1%|22.8%|7.9%|
|2017|41.2%|20.2%|26.5%|12.0%|
|2019|39.8%|21.1%|27.2%|11.9%|
|2022|39.1%|18.3%|26.4%|16.2%|
|2025|38.1%|18.5%|26.3%|17.1%|

Ground balls dropped by 10 percentage points (48.1% to 38.1%), while pop-ups more than doubled (7.9% to 17.1%). The fly ball revolution came with a cost.

## Visualizing Batted Ball Types

We plot batted ball type distribution in Figure 16.2.

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(la_df['year'], la_df['gb_rate'], 'o-', linewidth=2,
        markersize=8, color='#1f77b4', label='Ground Ball')
ax.plot(la_df['year'], la_df['fb_rate'], 's-', linewidth=2,
        markersize=8, color='#ff7f0e', label='Fly Ball')
ax.plot(la_df['year'], la_df['ld_rate'], '^-', linewidth=2,
        markersize=8, color='#2ca02c', label='Line Drive')
ax.plot(la_df['year'], la_df['popup_rate'], 'd-', linewidth=2,
        markersize=8, color='#d62728', label='Pop Up')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Percentage', fontsize=12)
ax.set_title('Batted Ball Type Distribution (2015-2025)', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig02_bb_types.png', dpi=150)
```

![Ground balls declined while pop-ups increased dramatically](../../chapters/16_launch_angle/figures/fig02_bb_types.png)

The cross-over pattern illustrates the trade-off: hitters elevated out of ground balls but often over-elevated into pop-ups.

## The Trade-Off: More Pop-Ups

We quantify the pop-up cost of elevation.

```python
popup_2015 = la_df[la_df['year'] == 2015]['popup_rate'].values[0]
popup_2025 = la_df[la_df['year'] == 2025]['popup_rate'].values[0]
popup_change = popup_2025 - popup_2015
```

|Metric|2015|2025|Change|
|------|----|----|------|
|Pop-up Rate|7.9%|17.1%|**+9.2%**|
|Ground Ball Rate|48.1%|38.1%|-10.0%|
|Net|—|—|Trade-off|

Pop-ups—essentially automatic outs—increased by 9.2 percentage points. The same swing mechanics that produce fly balls also produce pop-ups when mistimed.

## Sweet Spot Analysis

We examine "sweet spot" rate—batted balls in the 8-32° range that produce optimal outcomes.

```python
la_df[['year', 'sweet_spot']]
```

|year|Sweet Spot Rate|
|----|---------------|
|2015|33.9%|
|2017|34.0%|
|2019|34.2%|
|2022|30.1%|
|2025|30.4%|

Sweet spot rate has actually declined from 33.9% to 30.4%. The revolution was not about hitting more balls in the optimal zone—it was about avoiding ground balls at all costs.

## Statistical Validation

We validate the launch angle change by comparing early (2016-2018) and late (2023-2025) periods.

```python
# Aggregate batted balls for both periods
early_la, late_la = [], []

for year in [2016, 2017, 2018]:
    df = load_season(year, columns=['launch_angle'])
    batted = df[df['launch_angle'].notna()]
    early_la.extend(batted['launch_angle'].tolist())

for year in [2023, 2024, 2025]:
    df = load_season(year, columns=['launch_angle'])
    batted = df[df['launch_angle'].notna()]
    late_la.extend(batted['launch_angle'].tolist())

early = np.array(early_la)
late = np.array(late_la)

# T-test
t_stat, p_val = stats.ttest_ind(early, late)

# Cohen's d
pooled_std = np.sqrt((early.var() + late.var()) / 2)
cohens_d = (late.mean() - early.mean()) / pooled_std
```

|Test|Early Mean|Late Mean|Change|Cohen's d|Effect|
|----|----------|---------|------|---------|------|
|Launch Angle|15.43°|17.24°|+1.81°|0.059|negligible|

The effect size is negligible due to the enormous variance in launch angle (std ~30°). A 1.8° change in means is meaningful strategically but small relative to the spread from -80° ground balls to +90° pop-ups. The batted ball type percentages better capture the practical significance.

## The Strategic Logic

The elevation strategy makes sense for power hitters despite the pop-up cost. Ground balls almost never become home runs. Fly balls with sufficient exit velocity do. For hitters with power, accepting more pop-ups is worth it for the additional home runs.

```python
# Approximate run values by batted ball type
run_values = {
    'Ground Ball': -0.05,
    'Line Drive': +0.45,
    'Fly Ball': +0.12,
    'Pop Up': -0.90
}

# The calculation favors elevation for power hitters:
# - Losing 10% GB saves: 10 × 0.05 = 0.5 runs/100 BB
# - Gaining 3.5% FB adds: 3.5 × 0.12 = 0.4 runs/100 BB
# - But FB with high EV become HR: +1.4 runs each
```

## Summary

The launch angle revolution transformed baseball offense from 2015 to 2025:

1. **Average launch angle increased 6.1°** from 11.7° to 17.8°
2. **Ground balls dropped 10%** from 48.1% to 38.1%
3. **Pop-ups more than doubled** from 7.9% to 17.1%
4. **Fly balls rose modestly** from 22.8% to 26.3%
5. **Sweet spot rate declined** from 33.9% to 30.4%
6. **Effect size negligible** (Cohen's d = 0.06) due to high variance

The revolution explains what exit velocity stability could not. Hitters did not hit the ball harder—they hit it at better angles for power. Combined with the juiced ball era (which amplified fly ball distance), this produced the home run surge of the late 2010s. The trade-off—more strikeouts and pop-ups—was deemed acceptable for the power gains.

## Further Reading

- Sullivan, J. (2016). "The Fly Ball Revolution." *FanGraphs*.
- Arthur, R. (2017). "How Hitters Changed the Game." *FiveThirtyEight*.

## Exercises

1. Identify hitters who changed their launch angle most dramatically between 2015 and 2020. Did their power numbers improve?

2. Calculate the home run probability by exit velocity AND launch angle. What is the optimal combination?

3. Compare launch angle strategies for different hitter types (power vs contact). Do all hitters benefit equally from elevation?

```bash
cd chapters/16_launch_angle
python analysis.py
```
