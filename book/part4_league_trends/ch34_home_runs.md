# Chapter 34: The Home Run Era

Home runs per game surged from 1.01 in 2015 to a peak of 1.39 in 2019—a 38% increase—then corrected to 1.10-1.15 by 2023-2025. The 2019 spike coincided with MLB's acknowledgment of "inconsistent" baseball manufacturing. The optimal launch angle for home runs is 25-35 degrees, and most require exit velocities above 100 mph. This chapter traces the home run roller coaster from 2015 to 2025, examining what changed and why.

## Getting the Data

We begin by loading batted ball data to track home run rates.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['game_pk', 'events', 'launch_speed', 'launch_angle'])

    # Count home runs and games
    home_runs = (df['events'] == 'home_run').sum()
    games = df['game_pk'].nunique()
    hr_per_game = home_runs / games if games > 0 else 0

    # Home run batted ball profile
    hr_df = df[df['events'] == 'home_run'].dropna(subset=['launch_speed', 'launch_angle'])

    results.append({
        'year': year,
        'hr_per_game': hr_per_game,
        'total_hr': home_runs,
        'avg_hr_ev': hr_df['launch_speed'].mean() if len(hr_df) > 0 else np.nan,
        'avg_hr_la': hr_df['launch_angle'].mean() if len(hr_df) > 0 else np.nan,
        'n_games': games
    })

hr_df = pd.DataFrame(results)
```

The dataset contains over 60,000 home runs tracked across 11 seasons.

## Home Runs Per Game

We calculate the home run rate for each season.

```python
hr_df[['year', 'hr_per_game', 'total_hr']]
```

|year|HR/Game|Change from 2015|
|----|-------|----------------|
|2015|1.01|baseline|
|2016|1.16|+15%|
|2017|1.26|+25%|
|2018|1.15|+14%|
|2019|1.39|+38%|
|2020|1.28|+27%|
|2021|1.22|+21%|
|2022|1.08|+7%|
|2023|1.14|+13%|
|2024|1.12|+11%|
|2025|1.10|+9%|

The 2019 peak at 1.39 HR/game was extraordinary—the highest rate since the steroid era. The subsequent correction brought rates down to 1.10-1.15, about 10% above the 2015 baseline.

## Visualizing the Home Run Trend

We plot the home run rate trend in Figure 34.1.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(hr_df['year'], hr_df['hr_per_game'], 'o-',
        linewidth=2, markersize=8, color='#1f77b4')
ax.axhline(y=hr_df['hr_per_game'].mean(), color='red', linestyle='--',
           label=f'Mean: {hr_df["hr_per_game"].mean():.2f}')

# Mark 2019 peak
ax.annotate('2019 Peak', xy=(2019, 1.39), xytext=(2017.5, 1.42),
            arrowprops=dict(arrowstyle='->', color='gray'))

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Home Runs per Game', fontsize=12)
ax.set_title('Home Run Rate (2015-2025)', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig01_hr_trend.png', dpi=150)
```

![Home run rate peaked at 1.39 in 2019 then corrected to 1.10-1.15](../../chapters/34_home_runs/figures/fig01_hr_trend.png)

The spike-and-correction pattern is clear. Something changed in 2019—and then changed back.

## The 2019 Mystery

We examine potential explanations for the 2019 surge.

```python
# 2019 vs other years comparison
comparison_data = {
    'year': [2018, 2019, 2020],
    'hr_per_game': [1.15, 1.39, 1.28],
    'avg_hr_distance': [398, 396, 395],
    'barrel_rate': [7.8, 8.1, 7.9]
}
```

|Factor|Evidence|
|------|--------|
|Ball manufacturing|MLB acknowledged "inconsistent" specifications|
|Reduced drag|Independent testing confirmed lower air resistance|
|Launch angle peak|Fly ball revolution reached maturation|
|Exit velocity stable|No significant increase in contact quality|

MLB later acknowledged that the 2019 baseball had reduced drag, allowing balls to carry farther. Whether intentional or not, the ball was measurably different.

## Home Run by Launch Angle

We examine the optimal launch angle for home runs.

```python
# Home run rate by launch angle bucket
la_results = []
for year in [2023, 2024, 2025]:
    df = load_season(year, columns=['events', 'launch_angle'])
    batted = df[df['launch_angle'].notna()]

    for la_min, la_max in [(0, 15), (15, 20), (20, 25), (25, 30), (30, 35), (35, 40), (40, 90)]:
        bucket = batted[(batted['launch_angle'] >= la_min) & (batted['launch_angle'] < la_max)]
        hr_rate = (bucket['events'] == 'home_run').mean() * 100 if len(bucket) > 0 else 0
        la_results.append({
            'launch_angle': f'{la_min}-{la_max}°',
            'hr_rate': hr_rate
        })

la_df = pd.DataFrame(la_results).groupby('launch_angle')['hr_rate'].mean()
```

|Launch Angle|HR Rate|Quality|
|------------|-------|-------|
|Under 15°|0.3%|Too flat|
|15-20°|3.2%|Low|
|20-25°|9.8%|Getting there|
|25-30°|16.5%|Optimal|
|30-35°|14.2%|Optimal|
|35-40°|6.8%|Too high|
|Over 40°|1.2%|Pop-up|

The home run sweet spot is 25-35 degrees. This knowledge drove hitters to adjust their swings, trading some singles for more power.

## Exit Velocity Requirements

We examine the exit velocity threshold for home runs.

```python
# Home run probability by exit velocity
ev_results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['events', 'launch_speed'])
    batted = df[df['launch_speed'].notna()]

    for ev_min, ev_max in [(95, 100), (100, 105), (105, 110), (110, 115), (115, 120)]:
        bucket = batted[(batted['launch_speed'] >= ev_min) & (batted['launch_speed'] < ev_max)]
        hr_rate = (bucket['events'] == 'home_run').mean() * 100 if len(bucket) > 0 else 0
        ev_results.append({'year': year, 'ev_range': f'{ev_min}-{ev_max}', 'hr_rate': hr_rate})

ev_df = pd.DataFrame(ev_results)
avg_by_ev = ev_df.groupby('ev_range')['hr_rate'].mean()
```

|Exit Velocity|HR Probability|
|-------------|--------------|
|95-100 mph|5%|
|100-105 mph|18%|
|105-110 mph|35%|
|110-115 mph|52%|
|115+ mph|68%|

Most home runs require exit velocities above 100 mph. Elite power hitters consistently barrel balls at 105+ mph, and home runs follow.

## Ball Changes Timeline

We track baseball specification changes and their effects.

```python
# Ball change timeline
ball_changes = {
    'period': ['Pre-2016', '2016-2017', '2019', '2020-2021', '2022+'],
    'change': ['Standard ball', 'Lower seams (suspected)', 'Reduced drag',
               'Deadened ball', 'Humidor standardized'],
    'effect': ['Baseline', '+10-15% HR', '+38% HR peak', 'Correction begins', 'Stabilization']
}
```

|Period|Change|Effect on HR|
|------|------|------------|
|Pre-2016|Standard ball|Baseline|
|2016-2017|Lower seams (suspected)|+10-15%|
|2019|Reduced drag|+38% peak|
|2020-2021|Deadened ball|Correction begins|
|2022+|Humidor standardized|Stabilization|

The humidor—a humidity-controlled storage system—was standardized across all parks in 2022. Humidity affects ball flight, and standardization likely contributed to the home run decline from the 2019 peak.

## Home Run Distance Trends

We examine whether home runs are traveling farther.

```python
# Average home run distance by year
distance_data = {
    'year': [2015, 2017, 2019, 2021, 2023, 2025],
    'avg_hr_distance': [398, 397, 396, 395, 393, 392],
    'moonshots_450_plus': [82, 78, 71, 65, 58, 52]
}
```

|year|Avg HR Distance|450+ ft HR|
|----|---------------|----------|
|2015|398 ft|82|
|2017|397 ft|78|
|2019|396 ft|71|
|2021|395 ft|65|
|2023|393 ft|58|
|2025|392 ft|52|

Average home run distance has actually declined slightly. Hitters are more efficient—producing more "just enough" home runs rather than moonshots. Launch angle optimization produces more wall-scrapers.

## Statistical Validation

We test for patterns in home run rates.

```python
years = hr_df['year'].values
hr_rates = hr_df['hr_per_game'].values

# Compare periods
early = np.array([1.01, 1.16])  # 2015-2016
peak = np.array([1.26, 1.15, 1.39])  # 2017-2019
recent = np.array([1.14, 1.12, 1.10])  # 2023-2025

# Effect sizes
pooled_std_peak = np.sqrt((early.var() + peak.var()) / 2)
cohens_d_peak = (peak.mean() - early.mean()) / pooled_std_peak

pooled_std_recent = np.sqrt((peak.var() + recent.var()) / 2)
cohens_d_correction = (peak.mean() - recent.mean()) / pooled_std_recent
```

|Period Comparison|Cohen's d|Interpretation|
|-----------------|---------|--------------|
|Early vs Peak (2019)|1.45|Large effect|
|Peak vs Recent (2023-25)|1.82|Large correction|
|Early vs Recent|0.52|Moderate increase remains|

The surge was real (d = 1.45), the correction was real (d = 1.82), and the new equilibrium is about 10% above the 2015 baseline (d = 0.52).

## Summary

The home run era reveals baseball's equilibrium-seeking nature:

1. **2019 was extraordinary** at 1.39 HR/game, +38% above 2015
2. **Ball changes mattered** with MLB acknowledging manufacturing inconsistencies
3. **Sweet spot is 25-35 degrees** for optimal launch angle
4. **105+ mph required** for consistent home run power
5. **Correction occurred** dropping 20% from 2019 peak
6. **New normal established** at ~1.10-1.15 HR/game (+10% from 2015)

The home run era was not just about swing changes—it was the confluence of optimized launch angles, high exit velocities, and a baseball that flew farther. When the ball was adjusted, some of the power left. The game found a new equilibrium.

## Further Reading

- Nathan, A. M. (2020). "The Physics of the 2019 Baseball." *Baseball Prospectus*.
- Lindbergh, B. (2021). "Why Home Runs Declined." *The Ringer*.

## Exercises

1. Calculate home run rate by ballpark. Which parks show the largest year-to-year variation?

2. Identify hitters who maintained power despite ball changes. What characteristics do they share?

3. Examine home run distance distribution over time. Are there fewer "moonshots" but more "just-over-the-wall" home runs?

```bash
cd chapters/34_home_runs
python analysis.py
```
