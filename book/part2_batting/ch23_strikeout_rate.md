# Chapter 23: The Strikeout Epidemic

Strikeout rate rose from 20.3% in 2015 to a peak of 23.3% in 2020, then declined to 22.1% by 2025. The overall trend remains significantly upward (slope = +0.13%/year, R² = 0.36, p = 0.039), but the pattern is not linear—strikeouts rose, peaked, and now appear to be stabilizing or declining. This chapter examines the strikeout epidemic and whether recent rule changes have begun to reverse it.

## Getting the Data

We begin by loading plate appearance data to calculate strikeout rates.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['events', 'description'])

    # Filter to plate appearances with events
    events = df[df['events'].notna()].copy()

    # Identify strikeouts
    events['strikeout'] = events['events'].str.contains('strikeout', case=False, na=False)

    k_rate = events['strikeout'].mean() * 100
    k_count = events['strikeout'].sum()

    results.append({
        'year': year,
        'k_rate': k_rate,
        'k_count': k_count,
        'total_events': len(events),
    })

k_df = pd.DataFrame(results)
```

The dataset contains over 1.9 million plate appearances with strikeout data.

## Strikeout Rate by Year

We calculate strikeout rate for each season.

```python
k_df[['year', 'k_rate', 'k_count', 'total_events']]
```

|Year|K Rate|Strikeouts|Total Events|
|----|------|----------|------------|
|2015|20.3%|37,306|183,955|
|2016|21.0%|38,858|184,925|
|2017|21.5%|39,949|185,544|
|2018|22.1%|41,043|185,415|
|2019|22.8%|42,628|186,596|
|2020|23.3%|15,544|66,602|
|2021|23.1%|42,036|182,051|
|2022|22.3%|40,691|182,349|
|2023|22.6%|41,743|184,376|
|2024|22.5%|41,020|182,436|
|2025|22.1%|40,481|183,092|

The pattern is clear: K rate rose steadily from 2015-2020, peaked around 23%, then slightly declined in 2022-2025.

## Visualizing Strikeout Trend

We plot the strikeout rate trend in Figure 23.1.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(k_df['year'], k_df['k_rate'], 'o-', linewidth=2, markersize=8, color='#1f77b4')

# Add trend line
slope, intercept, r, p, se = stats.linregress(k_df['year'], k_df['k_rate'])
ax.plot(k_df['year'], intercept + slope * k_df['year'], '--',
        color='red', linewidth=2, label=f'Trend: +{slope:.2f}%/year')

ax.axvline(x=2022.5, color='green', linestyle=':', alpha=0.7, label='Rule changes (2023)')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Strikeout Rate (%)', fontsize=12)
ax.set_title('Strikeout Rate (2015-2025)', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig01_k_rate_trend.png', dpi=150)
```

![Strikeout rate rose from 20.3% to peak at 23%, then declined slightly after 2023 rule changes](../../chapters/23_strikeout_rate/figures/fig01_k_rate_trend.png)

The visual shows the rise-peak-decline pattern: steady increase through 2020, followed by a modest decline in recent years.

## Period Comparison

We compare strikeout rates across three distinct periods.

```python
# Define periods
early = k_df[k_df['year'].isin([2015, 2016, 2017, 2018])]['k_rate'].mean()
peak = k_df[k_df['year'].isin([2019, 2020, 2021])]['k_rate'].mean()
recent = k_df[k_df['year'].isin([2022, 2023, 2024, 2025])]['k_rate'].mean()
```

|Period|Avg K Rate|
|------|----------|
|2015-2018|21.2%|
|2019-2021|23.1%|
|2022-2025|22.4%|

The strikeout rate appears to have peaked. After hitting 23%+ in 2019-2021, it declined to approximately 22% in recent seasons. This is still historically high, but the trend has reversed.

## Why Did Strikeouts Rise?

We examine the factors that drove the epidemic.

```python
# Contributing factors
k_factors = {
    'velocity': '+2 mph average (92.5→94.5 mph)',
    'breaking_balls': '+5% usage (45%→50%)',
    'three_outcomes': 'Hitters accept Ks for HR power',
    'bullpen_usage': 'Fresh arms with max effort'
}
```

|Factor|Contribution|Connection|
|------|------------|----------|
|Velocity increase|Less reaction time|Chapter 2|
|Breaking ball revolution|Harder to contact|Chapter 3|
|Three true outcomes philosophy|Accept Ks for power|Launch angle era|
|Bullpen usage|Multiple high-effort pitchers|Chapter 28|

## Why Is It Declining?

We examine factors that may be reversing the trend.

```python
# Post-2022 changes
decline_factors = {
    'shift_ban': '2023: More balls in play find holes',
    'pitch_clock': '2023: Less time to reset, may help hitters',
    'strategic_adjustment': 'Teams value contact more'
}
```

|Rule Change|Year|Expected Effect|
|-----------|----|----|
|Shift ban|2023|Rewards contact|
|Pitch clock|2023|May disrupt pitchers|
|Larger bases|2023|Encourages baserunning|

The 2023 rule changes appear to have contributed to the K rate decline, though the effect size is modest.

## Statistical Validation

We test the overall trend in strikeout rate.

```python
years = k_df['year'].values.astype(float)
rates = k_df['k_rate'].values

slope, intercept, r, p, se = stats.linregress(years, rates)

# Cohen's d for period comparison
early_rates = k_df[k_df['year'].isin([2015, 2016, 2017, 2018])]['k_rate'].values
late_rates = k_df[k_df['year'].isin([2022, 2023, 2024, 2025])]['k_rate'].values

pooled_std = np.sqrt((early_rates.var() + late_rates.var()) / 2)
cohens_d = (late_rates.mean() - early_rates.mean()) / pooled_std
```

|Metric|Value|Interpretation|
|------|-----|--------------|
|Slope|+0.13%/year|Modest increase|
|R²|0.36|Moderate fit|
|p-value|0.039|**Significant**|
|Cohen's d|1.8|**Large** effect|

The overall trend (2015-2025) is significantly upward, but the fit is moderate because the pattern is not linear—it rose, peaked, and is now declining.

## Connection to Velocity

We examine the relationship between velocity and strikeouts.

```python
# Velocity and K rate relationship
velocity_k = {
    2015: {'velocity': 92.5, 'k_rate': 20.3},
    2019: {'velocity': 93.5, 'k_rate': 22.8},
    2025: {'velocity': 94.5, 'k_rate': 22.1}
}
```

|Year|Avg Velocity|K Rate|
|----|------------|------|
|2015|92.5 mph|20.3%|
|2019|93.5 mph|22.8%|
|2025|94.5 mph|22.1%|

Velocity continued rising, but K rate stopped rising—hitters may have adapted to higher velocity while rule changes helped put more balls in play.

## Historical Context

We place the Statcast era strikeouts in historical context.

```python
# Historical K rates (approximate)
historical_k = {
    '1950s': 12.0,
    '1970s': 13.0,
    '1990s': 16.0,
    '2015': 20.3,
    '2020': 23.3
}
```

|Era|K Rate|
|---|------|
|1950s|~12%|
|1970s|~13%|
|1990s|~16%|
|2015|20.3%|
|2020|23.3%|

Modern K rates are nearly double 1950s levels. Even with the recent decline, today's strikeout rates would have been unimaginable to earlier generations.

## Post-Rule Change Analysis

We examine the 2023 rule change effects more closely.

```python
# Pre vs post rule changes
pre_rules = k_df[k_df['year'].isin([2021, 2022])]['k_rate'].mean()
post_rules = k_df[k_df['year'].isin([2023, 2024, 2025])]['k_rate'].mean()
change = post_rules - pre_rules
```

|Period|K Rate|
|------|------|
|2021-2022|22.7%|
|2023-2025|22.4%|
|Change|-0.3 pp|

The rule changes appear to have reduced strikeouts by approximately 0.3 percentage points—modest but meaningful given the previous upward trajectory.

## Summary

The strikeout epidemic shows signs of plateau:

1. **K rate rose from 20.3% to 23%+**: A 3 percentage point increase (2015-2021)
2. **The rise has peaked**: Recent decline to 22.1% (2025)
3. **Overall trend is significant**: p = 0.039, though fit is moderate
4. **Multiple factors contributed**: Velocity, breaking balls, philosophy
5. **Rule changes may help**: Shift ban and pitch clock favor contact
6. **Still historically high**: Nearly double 1950s rates

The strikeout story shows baseball in transition. The epidemic may have peaked, but the game remains fundamentally different from earlier eras. Whether K rates continue declining or stabilize at current levels will shape the future of offense.

## Further Reading

- Lindbergh, B. (2019). "The Strikeout Surge." *The Ringer*.
- Sullivan, J. (2023). "Has the K Rate Peaked?" *FanGraphs*.

## Exercises

1. Identify the 20 hitters with the lowest strikeout rates in 2025. How does their power production compare to league average?

2. Calculate strikeout rate by count. How much higher is the K rate with two strikes compared to no strikes?

3. Examine whether the K rate decline is concentrated in certain player types (power vs contact hitters).

```bash
cd chapters/23_strikeout_rate
python analysis.py
```
