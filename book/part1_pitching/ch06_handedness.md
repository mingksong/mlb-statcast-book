# Chapter 6: Left vs Right Pitcher Differences

Right-handed pitchers throw 1.39 mph harder than left-handers on four-seam fastballs—94.01 mph versus 92.62 mph. This is a medium effect size (Cohen's d = 0.53), not trivial noise. Yet left-handers have maintained a stable 27% share of all pitches throughout the Statcast era. This chapter investigates the fundamental differences between handedness groups and discovers how southpaws compete despite a measurable velocity disadvantage.

## Getting the Data

We begin by loading Statcast pitch data and separating by pitcher handedness.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['pitch_type', 'release_speed', 'p_throws',
                                     'release_spin_rate', 'pfx_x', 'pfx_z'])

    # Separate by handedness
    lhp = df[df['p_throws'] == 'L']
    rhp = df[df['p_throws'] == 'R']

    # Calculate LHP percentage
    lhp_pct = len(lhp) / len(df) * 100

    # Calculate 4-seam velocity by handedness
    lhp_ff = lhp[(lhp['pitch_type'] == 'FF') & (lhp['release_speed'].notna())]
    rhp_ff = rhp[(rhp['pitch_type'] == 'FF') & (rhp['release_speed'].notna())]

    results.append({
        'year': year,
        'lhp_pct': lhp_pct,
        'lhp_velocity': lhp_ff['release_speed'].mean(),
        'rhp_velocity': rhp_ff['release_speed'].mean(),
        'velocity_gap': rhp_ff['release_speed'].mean() - lhp_ff['release_speed'].mean(),
        'lhp_count': len(lhp),
        'rhp_count': len(rhp),
    })

hand_df = pd.DataFrame(results)
```

The data contains over 2.5 million pitches—679,151 from left-handers and 1,854,916 from right-handers.

## The Velocity Gap

We compare four-seam fastball velocity between handedness groups.

```python
# Aggregate velocity across all years
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['pitch_type', 'release_speed', 'p_throws'])

    lhp_ff = df[(df['p_throws'] == 'L') & (df['pitch_type'] == 'FF')]['release_speed']
    rhp_ff = df[(df['p_throws'] == 'R') & (df['pitch_type'] == 'FF')]['release_speed']
```

|Handedness|4-Seam Velocity|Sample Size|
|----------|---------------|-----------|
|Right-handed|94.01 mph|1,854,916|
|Left-handed|92.62 mph|679,151|
|**Difference**|**+1.39 mph**||

The velocity gap is consistent across years and pitch types. Right-handers throw harder.

## Velocity Gap Over Time

We examine whether the gap has widened or narrowed.

```python
hand_df[['year', 'lhp_velocity', 'rhp_velocity', 'velocity_gap']]
```

|year|LHP Velocity|RHP Velocity|Gap|
|----|------------|------------|---|
|2015|92.15 mph|93.45 mph|+1.30 mph|
|2017|92.46 mph|93.49 mph|+1.03 mph|
|2019|92.10 mph|93.85 mph|+1.75 mph|
|2021|92.68 mph|94.12 mph|+1.44 mph|
|2023|93.12 mph|94.55 mph|+1.42 mph|
|2025|93.09 mph|95.01 mph|+1.92 mph|

Both groups are participating in the velocity revolution—average velocity increased for both left- and right-handers. However, the gap has widened slightly from +1.30 mph in 2015 to +1.92 mph in 2025.

## Left-Hander Representation

We track the percentage of pitches thrown by left-handers over time in Figure 6.2.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(hand_df['year'], hand_df['lhp_pct'], 'o-', linewidth=2, markersize=8, color='#1f77b4')
ax.axhline(y=hand_df['lhp_pct'].mean(), color='red', linestyle='--',
           label=f'Mean: {hand_df["lhp_pct"].mean():.1f}%')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Left-Handed Pitcher Percentage', fontsize=12)
ax.set_title('LHP Representation Over Time (2015-2025)', fontsize=14)
ax.set_ylim(20, 35)
ax.legend()
plt.tight_layout()
plt.savefig('figures/fig02_lhp_percentage_trend.png', dpi=150)
```

![Left-hander representation has remained stable at approximately 27% throughout the decade](../../chapters/06_handedness/figures/fig02_lhp_percentage_trend.png)

|year|LHP %|
|----|-----|
|2015|27.0%|
|2017|25.7%|
|2019|27.8%|
|2021|29.6%|
|2023|26.5%|
|2025|27.2%|

Despite velocity disadvantages, left-handers have maintained their ~27% share throughout the decade. The representation shows no significant trend (p = 0.639).

## Statistical Validation

We validate the velocity difference using a t-test and effect size calculation.

```python
# Aggregate all LHP and RHP fastball velocity
lhp_all, rhp_all = [], []

for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['pitch_type', 'release_speed', 'p_throws'])
    lhp_ff = df[(df['p_throws'] == 'L') & (df['pitch_type'] == 'FF')]['release_speed'].dropna()
    rhp_ff = df[(df['p_throws'] == 'R') & (df['pitch_type'] == 'FF')]['release_speed'].dropna()
    lhp_all.extend(lhp_ff.tolist())
    rhp_all.extend(rhp_ff.tolist())

lhp_arr = np.array(lhp_all)
rhp_arr = np.array(rhp_all)

t_stat, p_value = stats.ttest_ind(lhp_arr, rhp_arr)
pooled_std = np.sqrt((lhp_arr.std()**2 + rhp_arr.std()**2) / 2)
cohens_d = (rhp_arr.mean() - lhp_arr.mean()) / pooled_std
```

|Test|Metric|Value|
|----|------|-----|
|Velocity Comparison|LHP Mean|92.62 mph|
||RHP Mean|94.01 mph|
||Difference|+1.39 mph|
||t-statistic|-375.10|
||p-value|<0.001|
||Cohen's d|0.532|
||Effect Size|medium|
|LHP Trend|Slope|+0.05%/year|
||R²|0.026|
||p-value|0.639|
||Trend|not significant|

The velocity gap is highly significant (p < 0.001) with a medium effect size (Cohen's d = 0.53). The left-hander representation shows no significant trend.

## Spin Rate Comparison

We also compare spin rates between handedness groups.

```python
# Aggregate spin rate by handedness
lhp_spin = df[(df['p_throws'] == 'L') & (df['pitch_type'] == 'FF')]['release_spin_rate']
rhp_spin = df[(df['p_throws'] == 'R') & (df['pitch_type'] == 'FF')]['release_spin_rate']
```

|Metric|LHP|RHP|Difference|
|------|---|---|----------|
|Mean Spin Rate|2,247 rpm|2,289 rpm|+42 rpm|
|Cohen's d|0.237||small|

Right-handers also have a small spin rate advantage (+42 rpm), though the effect size is smaller than for velocity.

## How Lefties Compete

The data raises an obvious question: if right-handers throw harder and spin the ball more, why haven't left-handers been squeezed out?

Several factors explain left-handers' continued value:

1. **Scarcity creates advantage**: Only ~10% of the population is left-handed. This natural rarity means left-handed batters see fewer same-side matchups
2. **Platoon advantage**: Left-handers face left-handed batters with advantageous angles
3. **Different look**: After seeing 73% right-handed pitching, batters face fundamentally different release points from lefties
4. **Natural selection**: Only left-handers who can compete despite lower velocity make MLB—survivors are especially skilled

## Summary

Left-handed and right-handed pitchers show measurable differences:

1. **Right-handers throw 1.39 mph harder** (94.01 vs 92.62 mph, Cohen's d = 0.53)
2. **The velocity gap is widening** from +1.30 mph (2015) to +1.92 mph (2025)
3. **Right-handers spin the ball more** (+42 rpm, Cohen's d = 0.24)
4. **Left-hander representation is stable** at ~27% (no significant trend)
5. **Left-handers survive through scarcity** and platoon advantages

The persistence of left-handers despite measurable disadvantages demonstrates that raw velocity is not the only path to success in baseball. Scarcity, deception, and strategic matchup advantages create value that compensates for lower velocity.

## Further Reading

- Petti, B. (2018). "The Platoon Advantage by Handedness." *FanGraphs*.
- Petriello, M. (2020). "Why Left-Handed Pitchers Still Matter." *MLB.com*.

## Exercises

1. Calculate the platoon splits (performance vs same-handed batters vs opposite-handed batters) for left- and right-handed pitchers. Which group shows a larger platoon advantage?

2. Identify the 10 fastest-throwing left-handed pitchers each year. Has their velocity increased at the same rate as right-handers?

3. Compare pitch mix (fastball/breaking/offspeed ratio) between handedness groups. Do left-handers compensate with different arsenals?

```bash
cd chapters/06_handedness
python analysis.py
```
