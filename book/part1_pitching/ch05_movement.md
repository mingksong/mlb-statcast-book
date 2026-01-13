# Chapter 5: Pitch Movement Analysis

In 2015, the average four-seam fastball had -0.23 inches of horizontal break and +1.33 inches of induced vertical break. By 2025, those numbers were -0.28 inches and +1.32 inches—virtually unchanged despite a decade of velocity increases, pitch design technology, and analytical innovation. This stability presents a fascinating puzzle.

This chapter investigates whether the velocity revolution has affected how pitches move through the strike zone, and discovers that pitch movement has remained remarkably constant across the Statcast era.

## Getting the Data

We begin by loading Statcast pitch data with horizontal (pfx_x) and vertical (pfx_z) movement metrics.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

# Movement metrics:
# pfx_x: Horizontal movement (inches), positive = arm-side break
# pfx_z: Vertical movement (inches), induced vertical break above gravity

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['pitch_type', 'pfx_x', 'pfx_z'])

    # Filter to 4-seam fastballs with valid movement data
    ff = df[(df['pitch_type'] == 'FF') &
            (df['pfx_x'].notna()) &
            (df['pfx_z'].notna())]

    n = len(ff)
    results.append({
        'year': year,
        'count': n,
        'pfx_x_mean': ff['pfx_x'].mean(),
        'pfx_x_std': ff['pfx_x'].std(),
        'pfx_z_mean': ff['pfx_z'].mean(),
        'pfx_z_std': ff['pfx_z'].std(),
    })

movement_df = pd.DataFrame(results)
```

The data contains over 2.4 million four-seam fastballs across 11 seasons.

## Fastball Movement by Year

We calculate the average horizontal and vertical movement for each season.

```python
movement_df[['year', 'pfx_x_mean', 'pfx_z_mean', 'count']]
```

|year|pfx_x (H-Break)|pfx_z (V-Break)|count|
|----|---------------|---------------|-----|
|2015|-0.23 in|+1.33 in|249,545|
|2016|-0.20 in|+1.32 in|258,392|
|2017|-0.33 in|+1.43 in|248,927|
|2018|-0.27 in|+1.31 in|252,975|
|2019|-0.29 in|+1.30 in|263,385|
|2020|-0.27 in|+1.33 in|91,684|
|2021|-0.24 in|+1.34 in|251,958|
|2022|-0.27 in|+1.35 in|235,409|
|2023|-0.28 in|+1.31 in|230,247|
|2024|-0.27 in|+1.31 in|225,470|
|2025|-0.28 in|+1.32 in|226,018|

The numbers reveal remarkable stability. Over 11 seasons, horizontal break changed by just 0.05 inches and vertical break by essentially zero. This occurred while average velocity increased by 1.37 mph (Chapter 2).

## Visualizing Movement Trends

We plot the movement trends with 95% confidence intervals in Figure 5.1.

```python
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Horizontal break
ax1.plot(movement_df['year'], movement_df['pfx_x_mean'], 'o-', linewidth=2,
         markersize=8, color='#1f77b4')
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Horizontal Break (inches)', fontsize=12)
ax1.set_title('Fastball Horizontal Movement (2015-2025)', fontsize=14)
ax1.axhline(y=movement_df['pfx_x_mean'].mean(), color='red', linestyle='--',
            label=f'Mean: {movement_df["pfx_x_mean"].mean():.2f} in')
ax1.legend()

# Vertical break
ax2.plot(movement_df['year'], movement_df['pfx_z_mean'], 'o-', linewidth=2,
         markersize=8, color='#ff7f0e')
ax2.set_xlabel('Year', fontsize=12)
ax2.set_ylabel('Vertical Break (inches)', fontsize=12)
ax2.set_title('Fastball Vertical Movement (2015-2025)', fontsize=14)
ax2.axhline(y=movement_df['pfx_z_mean'].mean(), color='red', linestyle='--',
            label=f'Mean: {movement_df["pfx_z_mean"].mean():.2f} in')
ax2.legend()

plt.tight_layout()
plt.savefig('figures/fig01_fastball_movement_trend.png', dpi=150)
```

![Fastball movement has remained stable from 2015 to 2025, with horizontal break around -0.27 inches and vertical break around +1.33 inches](../../chapters/05_movement/figures/fig01_fastball_movement_trend.png)

The flat trendlines confirm what the table shows: pitch movement has not evolved meaningfully despite all other changes in pitching.

## Movement by Pitch Type

We examine whether other pitch types show similar stability.

```python
pitch_types = ['FF', 'SL', 'CU', 'CH', 'SI']
pitch_names = {'FF': '4-Seam', 'SL': 'Slider', 'CU': 'Curve', 'CH': 'Change', 'SI': 'Sinker'}

for pt in pitch_types:
    for year in AVAILABLE_SEASONS:
        df = load_season(year, columns=['pitch_type', 'pfx_x', 'pfx_z'])
        subset = df[df['pitch_type'] == pt]
        # ... aggregate movement data
```

|Pitch Type|2015-17 H-Break|2023-25 H-Break|Change|
|----------|---------------|---------------|------|
|4-Seam Fastball|-0.25 in|-0.28 in|-0.03 in|
|Slider|+0.25 in|+0.20 in|-0.05 in|
|Curveball|+0.47 in|+0.35 in|-0.12 in|
|Changeup|-0.29 in|-0.37 in|-0.08 in|
|Sinker|-0.50 in|-0.52 in|-0.02 in|

Each pitch type occupies a distinct region of movement space, and these regions have not shifted meaningfully. The curveball shows the largest change (-0.12 in), but this still represents less than half an inch over a decade.

## Distribution Comparison

We compare the full movement distributions between 2015 and 2025 in Figure 5.4.

```python
df_2015 = load_season(2015, columns=['pitch_type', 'pfx_x', 'pfx_z'])
df_2025 = load_season(2025, columns=['pitch_type', 'pfx_x', 'pfx_z'])

ff_2015 = df_2015[df_2015['pitch_type'] == 'FF']
ff_2025 = df_2025[df_2025['pitch_type'] == 'FF']

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(ff_2015['pfx_x'], bins=50, alpha=0.6, label='2015', density=True, color='#1f77b4')
ax.hist(ff_2025['pfx_x'], bins=50, alpha=0.6, label='2025', density=True, color='#ff7f0e')
ax.axvline(ff_2015['pfx_x'].mean(), color='#1f77b4', linestyle='--', linewidth=2)
ax.axvline(ff_2025['pfx_x'].mean(), color='#ff7f0e', linestyle='--', linewidth=2)
ax.set_xlabel('Horizontal Break (inches)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Horizontal Movement Distribution: 2015 vs 2025', fontsize=14)
ax.legend()
plt.tight_layout()
plt.savefig('figures/fig04_distribution_comparison.png', dpi=150)
```

![The 2015 and 2025 horizontal break distributions nearly perfectly overlap](../../chapters/05_movement/figures/fig04_distribution_comparison.png)

The distributions almost perfectly overlap. This is not just stable averages—the entire shape of how fastballs move has remained constant.

## Statistical Validation

We validate these observations using linear regression.

```python
years = movement_df['year'].values

# Horizontal break trend
h_means = movement_df['pfx_x_mean'].values
slope_h, intercept_h, r_h, p_h, se_h = stats.linregress(years, h_means)

# Vertical break trend
v_means = movement_df['pfx_z_mean'].values
slope_v, intercept_v, r_v, p_v, se_v = stats.linregress(years, v_means)
```

|Metric|Horizontal Break|Vertical Break|
|------|----------------|--------------|
|Slope|-0.0032 in/year|-0.0027 in/year|
|Slope 95% CI|[-0.01, 0.00]|[-0.01, 0.00]|
|R²|0.094|0.065|
|p-value|0.358|0.450|

Both trends have R² values below 0.1 and p-values well above 0.05. There is no statistically significant trend in either direction. The slopes are essentially zero—less than a third of an inch change per decade.

## Period Comparison

We compare the early period (2015-2017) to the late period (2023-2025).

```python
early_data_h, late_data_h = [], []
early_data_v, late_data_v = [], []

for year in [2015, 2016, 2017]:
    df = load_season(year, columns=['pitch_type', 'pfx_x', 'pfx_z'])
    ff = df[df['pitch_type'] == 'FF']
    early_data_h.extend(ff['pfx_x'].dropna().tolist())
    early_data_v.extend(ff['pfx_z'].dropna().tolist())

for year in [2023, 2024, 2025]:
    df = load_season(year, columns=['pitch_type', 'pfx_x', 'pfx_z'])
    ff = df[df['pitch_type'] == 'FF']
    late_data_h.extend(ff['pfx_x'].dropna().tolist())
    late_data_v.extend(ff['pfx_z'].dropna().tolist())

early_h, late_h = np.array(early_data_h), np.array(late_data_h)
early_v, late_v = np.array(early_data_v), np.array(late_data_v)

# Calculate Cohen's d
pooled_std_h = np.sqrt(((len(early_h)-1)*early_h.std()**2 + (len(late_h)-1)*late_h.std()**2) /
                        (len(early_h) + len(late_h) - 2))
cohens_d_h = (late_h.mean() - early_h.mean()) / pooled_std_h
```

|Metric|Horizontal Break|Vertical Break|
|------|----------------|--------------|
|Early Period Mean|-0.25 in|+1.36 in|
|Late Period Mean|-0.28 in|+1.31 in|
|Difference|-0.02 in|-0.04 in|
|t-statistic|21.35|91.41|
|p-value|<0.001|<0.001|
|Cohen's d|-0.036|-0.153|

The t-tests show statistical significance due to the massive sample sizes (over 700,000 pitches per period). However, the effect sizes are negligible: Cohen's d of -0.036 for horizontal break and -0.153 for vertical break. Statistical significance without practical significance—a classic large-sample phenomenon.

## Why Hasn't Movement Changed?

The stability paradox raises a question: with pitch design technology, spin rate optimization, and analytics-driven development, why hasn't movement evolved?

Several factors explain this:

1. **Biomechanical constraints**: Movement comes from spin axis and release mechanics that don't change much with velocity
2. **Natural selection**: Pitchers who lose movement when throwing harder don't reach MLB
3. **Independent optimization**: Velocity and movement are affected by different physical factors
4. **Efficiency limits**: There may be physical ceilings on how much spin axis can be manipulated

## Summary

Pitch movement has remained remarkably stable from 2015 to 2025:

1. **Horizontal break changed by -0.05 inches** from -0.23 in (2015) to -0.28 in (2025)
2. **Vertical break changed by -0.01 inches** from +1.33 in to +1.32 in
3. **No significant trend exists** (R² < 0.10, p > 0.35)
4. **Effect sizes are negligible** (Cohen's d = -0.036 and -0.153)
5. **All pitch types show similar stability**
6. **Velocity and movement are independent** dimensions of pitch quality

The stability paradox reveals that baseball's velocity revolution has been remarkably selective. Pitchers found ways to throw harder without sacrificing the movement that makes their pitches effective. When analysts say "stuff is improving," they primarily mean velocity—not movement.

## Further Reading

- Nathan, A. M. (2012). "The Effect of Spin on the Flight of a Baseball." *American Journal of Physics*.
- Cross, R. (2011). "Physics of Baseball Pitching." *Physics Today*.

## Exercises

1. Calculate the correlation between release speed and horizontal break for four-seam fastballs. Is there evidence that faster pitches move less?

2. Identify pitchers who significantly increased velocity between 2015 and 2025. Did their movement profiles change?

3. Compare movement stability for starters versus relievers. Do relievers, who throw harder on average, show different patterns?

```bash
cd chapters/05_movement
python analysis.py
```
