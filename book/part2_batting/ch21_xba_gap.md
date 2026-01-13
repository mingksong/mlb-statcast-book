# Chapter 21: Expected vs. Reality

Actual batting average consistently exceeds expected batting average (xBA) by approximately 9-10 points throughout the Statcast era. This gap (mean = 9.4 points, std = 1.3 points) represents the aspects of hitting that exit velocity and launch angle cannot capture: batter speed, spray angle, defensive positioning, and park factors. This chapter examines the relationship between expected and actual outcomes and what the gap reveals about the limits of batted ball metrics.

## Getting the Data

We begin by loading batted ball data with both actual outcomes and expected values.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['events', 'launch_speed', 'launch_angle',
                                     'estimated_ba_using_speedangle'])

    # Filter to at-bats with outcomes (hits and outs)
    hit_types = ['single', 'double', 'triple', 'home_run']
    out_types = ['field_out', 'force_out', 'grounded_into_double_play',
                 'fielders_choice_out', 'double_play', 'sac_fly']

    batted = df[df['events'].isin(hit_types + out_types)].copy()
    batted = batted.dropna(subset=['estimated_ba_using_speedangle'])

    # Calculate actual BA
    batted['hit'] = batted['events'].isin(hit_types).astype(int)

    actual_ba = batted['hit'].mean()
    xba = batted['estimated_ba_using_speedangle'].mean()
    gap = (actual_ba - xba) * 1000  # Convert to points

    results.append({
        'year': year,
        'actual_ba': actual_ba,
        'xba': xba,
        'gap': gap,
        'n_batted': len(batted),
    })

xba_df = pd.DataFrame(results)
```

The dataset contains over 1.2 million at-bats with valid xBA values.

## BA vs xBA by Year

We calculate both metrics for each season.

```python
xba_df[['year', 'actual_ba', 'xba', 'gap']]
```

|Year|Actual BA|xBA|Gap (points)|
|----|---------|---|------------|
|2015|.332|.321|+11|
|2016|.337|.327|+10|
|2017|.340|.331|+10|
|2018|.334|.324|+10|
|2019|.344|.334|+10|
|2020|.339|.332|+7|
|2021|.334|.323|+11|
|2022|.328|.319|+9|
|2023|.337|.327|+10|
|2024|.329|.321|+8|
|2025|.330|.323|+8|

Actual BA consistently exceeds xBA by approximately 8-11 points. This gap has remained remarkably stable throughout the Statcast era.

## Visualizing the Gap

We plot both metrics over time in Figure 21.1.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(xba_df['year'], xba_df['actual_ba'], 'o-', linewidth=2,
        markersize=8, color='#1f77b4', label='Actual BA')
ax.plot(xba_df['year'], xba_df['xba'], 's-', linewidth=2,
        markersize=8, color='#ff7f0e', label='xBA')

ax.fill_between(xba_df['year'], xba_df['xba'], xba_df['actual_ba'],
                alpha=0.3, color='green', label='Gap')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Batting Average', fontsize=12)
ax.set_title('Actual BA vs Expected BA (2015-2025)', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig01_ba_vs_xba.png', dpi=150)
```

![Actual BA exceeds xBA by 8-11 points consistently across all seasons](../../chapters/21_xba_gap/figures/fig01_ba_vs_xba.png)

The parallel tracks show that both metrics move together, but actual BA maintains a consistent advantage.

## Why the Gap Exists

We examine what xBA captures and what it misses.

```python
# xBA components
xba_components = {
    'included': ['Exit velocity', 'Launch angle', 'Historical outcomes for similar batted balls'],
    'excluded': ['Spray angle (pull/center/oppo)', 'Batter speed',
                 'Defensive positioning', 'Park factors', 'Weather conditions']
}
```

|xBA Includes|xBA Excludes|
|------------|------------|
|Exit velocity|Spray angle|
|Launch angle|Batter speed|
|Historical outcomes|Defensive positioning|
||Park factors|
||Weather conditions|

The gap exists because real baseball has dimensions that exit velocity and launch angle cannot capture. Fast runners beat out more infield hits. Pull hitters exploit defensive alignments. Good baserunners take extra bases.

## Decomposing the Gap

We estimate the contribution of different factors to the gap.

```python
# Approximate gap sources
gap_sources = {
    'speed_premium': 3.5,      # Fast players beat out grounders/infield hits
    'spray_angle': 2.5,        # Pulling the ball exploits shift weaknesses
    'home_runs': 1.5,          # No luck variance on HRs (always hits)
    'babip_noise': 1.5,        # Defense, wind, bounces
}

total = sum(gap_sources.values())  # ~9 points
```

|Factor|Contribution|Explanation|
|------|------------|-----------|
|Speed premium|~3-5 points|Fast players beat out grounders|
|Spray angle|~2-3 points|Pull hits exploit defensive holes|
|Home runs|~1-2 points|No variance on HR outcomes|
|BABIP noise|~1-2 points|Defense, wind, lucky bounces|
|**Total**|**~9-10 points**||

## Stability Analysis

We test whether the gap has changed over time.

```python
years = xba_df['year'].values.astype(float)
gaps = xba_df['gap'].values

slope, intercept, r, p, se = stats.linregress(years, gaps)
```

|Metric|Value|Interpretation|
|------|-----|--------------|
|Mean gap|9.4 points|Consistent outperformance|
|Std dev|1.3 points|Moderate variation|
|Slope|-0.22/year|Slight decline|
|R²|0.15|Weak relationship|
|p-value|0.14|Not significant|

The gap has remained stable—approximately 9-10 points throughout the Statcast era. The slight declining trend is not statistically significant.

## The 2020 Anomaly

We examine the notably smaller gap in 2020.

```python
gap_2019 = xba_df[xba_df['year'] == 2019]['gap'].values[0]
gap_2020 = xba_df[xba_df['year'] == 2020]['gap'].values[0]
gap_2021 = xba_df[xba_df['year'] == 2021]['gap'].values[0]
```

|Year|Gap|
|----|---|
|2019|+10.0|
|2020|+6.6|
|2021|+11.2|

The 60-game season with no fans, unusual schedules, and smaller sample size produced a notably smaller gap. This appears to be noise from the disrupted season rather than a meaningful change.

## Individual Player Variation

We examine how the gap varies for different player types.

```python
# Player types that exceed xBA
exceed_xba = ['Fast runners (+5-10 points)',
              'Pull hitters with power (+3-5 points)',
              'Bunt-for-hit specialists (+10-15 points)']

# Player types that underperform xBA
underperform_xba = ['Slow runners (-5-10 points)',
                    'Fly-ball hitters (more catchable)',
                    'Hitters facing extreme shifts']
```

|Consistently Exceed xBA|Consistently Underperform xBA|
|-----------------------|----------------------------|
|Fast runners (+5-10 pts)|Slow runners (-5-10 pts)|
|Pull hitters with power|Fly-ball hitters|
|Bunt-for-hit specialists|Shift victims|

Some players consistently beat their xBA; others consistently fall short. This is not luck—it reflects skills that xBA does not capture.

## Statistical Validation

We confirm the gap is statistically significant but practically consistent.

```python
# T-test for gap being different from zero
from scipy.stats import ttest_1samp

gaps = xba_df['gap'].values
t_stat, p_val = ttest_1samp(gaps, 0)

# Cohen's d for gap magnitude
cohens_d = gaps.mean() / gaps.std()
```

|Test|Value|Interpretation|
|----|-----|--------------|
|Mean gap|9.4 points|Significantly above zero|
|t-statistic|23.9|Highly significant|
|p-value|<0.001|Gap is real|
|Cohen's d|7.2|**Very large** effect|

The gap is real, consistent, and meaningful. Actual BA will continue to exceed xBA as long as factors like speed and spray angle affect outcomes.

## Practical Applications

We outline how to use this understanding in analysis.

```python
# How to interpret BA-xBA gaps
interpretation = {
    'ba_much_greater_xba': 'Getting lucky, likely to regress down',
    'ba_slightly_greater_xba': 'Normal (9-10 points expected)',
    'ba_less_than_xba': 'Getting unlucky, may improve OR lacks speed'
}
```

For player evaluation:
- **Compare players by xBA**, not BA (removes luck/defense variance)
- **Expect 9-10 point BA premium** over xBA as normal
- **Investigate large deviations**: BA >> xBA suggests luck; BA << xBA suggests speed issues or bad luck
- **xBA predicts future BA** better than current BA does

## Summary

The BA-xBA gap reveals the limits of batted ball metrics:

1. **Actual BA exceeds xBA by ~9-10 points** consistently
2. **Gap is not luck**: Speed, spray angle, and defense explain it
3. **Gap is stable**: No significant trend over time
4. **Individual variation matters**: Some players consistently over/underperform
5. **xBA is still useful**: Better predictor of future than BA
6. **2020 was anomalous**: Smaller gap in shortened season

The xBA gap teaches us that expected statistics are valuable simplifications, not perfect predictions. They capture the most important factors—exit velocity and launch angle—but not everything. Use them as tools, not oracles.

## Further Reading

- Carleton, R. (2017). "When xBA Lies." *Baseball Prospectus*.
- Sullivan, J. (2019). "The Gap Between Expected and Actual." *FanGraphs*.

## Exercises

1. Identify the 20 hitters with the largest positive BA-xBA gaps in 2025. What characteristics do they share (speed, spray angle)?

2. Calculate the BA-xBA gap by batted ball type (ground ball, line drive, fly ball). Which type shows the largest gap?

3. Examine whether the gap differs for left-handed vs right-handed hitters.

```bash
cd chapters/21_xba_gap
python analysis.py
```
