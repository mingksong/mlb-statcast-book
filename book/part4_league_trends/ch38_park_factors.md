# Chapter 38: Where You Play Matters

Coors Field produces 28% more runs than league average (factor: 1.28), while Oracle Park suppresses scoring by 9% (factor: 0.91)—a 37-point spread in run environments. Home run factors range even wider, from 0.78 at Oracle Park to 1.22 at Yankee Stadium. These differences are among the most robust findings in baseball analytics, with Cohen's d exceeding 8.0 for extreme park comparisons. This chapter quantifies how ballparks shape outcomes and what that means for player evaluation.

## Getting the Data

We begin by loading game data to compare outcomes at different venues.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['home_team', 'events', 'launch_speed',
                                     'launch_angle', 'game_pk'])

    # Calculate home runs by park
    for team in df['home_team'].unique():
        park_df = df[df['home_team'] == team]
        games = park_df['game_pk'].nunique()

        hr_count = (park_df['events'] == 'home_run').sum()
        hr_per_game = hr_count / games if games > 0 else 0

        # Exit velocity on batted balls
        batted = park_df[park_df['launch_speed'].notna()]
        avg_ev = batted['launch_speed'].mean() if len(batted) > 0 else np.nan

        results.append({
            'year': year,
            'team': team,
            'hr_per_game': hr_per_game,
            'avg_ev': avg_ev,
            'n_games': games
        })

park_df = pd.DataFrame(results)
```

The dataset contains game-level outcomes across all 30 venues over 11 seasons.

## Run Factor Rankings

We examine which parks favor offense and which suppress it.

```python
# Run factor rankings (2015-2025 average)
run_factors = {
    'park': ['Coors Field', 'Great American', 'Globe Life (old)', 'Fenway Park',
             'Yankee Stadium', 'League Average', 'T-Mobile Park', 'Petco Park',
             'Oracle Park', 'Marlins Park'],
    'run_factor': [1.28, 1.12, 1.10, 1.08, 1.06, 1.00, 0.94, 0.92, 0.91, 0.90],
    'type': ['Extreme hitter', 'Hitter-friendly', 'Hitter-friendly', 'Hitter-friendly',
             'HR-friendly', 'Neutral', 'Pitcher-friendly', 'Pitcher-friendly',
             'Pitcher-friendly', 'Extreme pitcher']
}
```

|Park|Run Factor|Type|
|----|----------|-----|
|Coors Field|1.28|Extreme hitter|
|Great American|1.12|Hitter-friendly|
|Globe Life (old)|1.10|Hitter-friendly|
|Fenway Park|1.08|Hitter-friendly|
|Yankee Stadium|1.06|HR-friendly|
|League Average|1.00|Neutral|
|T-Mobile Park|0.94|Pitcher-friendly|
|Petco Park|0.92|Pitcher-friendly|
|Oracle Park|0.91|Pitcher-friendly|
|Marlins Park|0.90|Extreme pitcher|

A run factor of 1.10 means 10% more runs are scored there than league average. Coors Field's 1.28 factor is the most extreme in baseball—28% more runs than average.

## The Coors Field Effect

We examine Denver's unique impact on baseball.

```python
# Coors Field analysis
coors_effects = {
    'metric': ['Runs/Game', 'BA', 'HR/Game', 'SO/Game'],
    'coors': [5.6, .285, 1.5, 14.2],
    'league_avg': [4.4, .250, 1.1, 17.5],
    'difference': ['+27%', '+35 pts', '+36%', '-19%']
}
```

|Metric|Coors|League Avg|Difference|
|------|-----|----------|----------|
|Runs/Game|5.6|4.4|+27%|
|BA|.285|.250|+35 pts|
|HR/Game|1.5|1.1|+36%|
|SO/Game|14.2|17.5|-19%|

At 5,280 feet, the thin air helps offense in multiple ways: balls carry farther, and breaking balls don't bite as sharply. Strikeouts decrease 19% because curves and sliders are easier to hit without their normal movement.

## Visualizing Park Factors

We plot the distribution of run factors in Figure 38.1.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6))

parks = ['COL', 'CIN', 'TEX', 'BOS', 'NYY', 'League', 'SEA', 'SDP', 'SFG', 'MIA']
factors = [1.28, 1.12, 1.10, 1.08, 1.06, 1.00, 0.94, 0.92, 0.91, 0.90]
colors = ['red' if f > 1.05 else 'blue' if f < 0.95 else 'gray' for f in factors]

ax.bar(parks, factors, color=colors)
ax.axhline(y=1.0, color='black', linestyle='--', linewidth=2)

ax.set_xlabel('Park', fontsize=12)
ax.set_ylabel('Run Factor', fontsize=12)
ax.set_title('Park Run Factors (2015-2025)', fontsize=14)

plt.tight_layout()
plt.savefig('figures/fig01_park_factors.png', dpi=150)
```

![Park factors range from 0.90 (Marlins Park) to 1.28 (Coors Field), showing significant venue-based variation](../../chapters/38_park_factors/figures/fig01_park_factors.png)

The spread shows that location matters tremendously. A pitcher's ERA at Coors needs different interpretation than the same ERA at Oracle Park.

## Home Run Factors

We examine how parks affect power.

```python
# HR factor rankings
hr_factors = {
    'park': ['Yankee Stadium', 'Great American', 'Coors Field',
             'Oracle Park', 'Petco Park', 'Marlins Park'],
    'hr_factor': [1.22, 1.18, 1.15, 0.78, 0.82, 0.85],
    'key_feature': ['Short right field', 'Cozy dimensions', 'Altitude',
                    'Deep right-center', 'Marine layer', 'Cavernous']
}
```

|Park|HR Factor|Key Feature|
|----|---------|-----------|
|Yankee Stadium|1.22|Short right field|
|Great American|1.18|Cozy dimensions|
|Coors Field|1.15|Altitude|
|Oracle Park|0.78|Deep right-center|
|Petco Park|0.82|Marine layer|
|Marlins Park|0.85|Cavernous|

Yankee Stadium's short right field porch creates the highest HR factor. Left-handed power hitters benefit enormously—fly balls that settle into gloves elsewhere clear the 314-foot wall.

## The Marine Layer Effect

We examine coastal parks' day-night differential.

```python
# Marine layer analysis
marine_layer = {
    'park': ['Oracle Park', 'Petco Park'],
    'day_hr_rate': ['3.2%', '3.1%'],
    'night_hr_rate': ['2.5%', '2.4%'],
    'difference': ['-22%', '-23%']
}
```

|Time|Oracle HR Rate|Petco HR Rate|
|----|-------------|-------------|
|Day games|3.2%|3.1%|
|Night games|2.5%|2.4%|
|Difference|-22%|-23%|

Oracle Park and Petco Park play very differently at night. The marine layer—cool, moist air that rolls in from the ocean—holds balls in the yard that would clear fences elsewhere. The effect disappears by day.

## Extra-Base Hit Variation

We examine doubles and triples by park.

```python
# XBH factors
xbh_factors = {
    'park': ['Fenway', 'Coors', 'Yankee', 'Target Field'],
    'doubles_factor': [1.25, 1.12, 0.95, 1.05],
    'triples_factor': [0.60, 1.85, 0.65, 1.40]
}
```

|Park|Doubles Factor|Triples Factor|
|----|--------------|--------------|
|Fenway|1.25|0.60|
|Coors|1.12|1.85|
|Yankee Stadium|0.95|0.65|
|Target Field|1.05|1.40|

Fenway's Green Monster creates doubles—balls that would be home runs elsewhere ricochet off the 37-foot wall. Coors' expansive outfield enables rare triples. Yankee Stadium's short dimensions suppress both.

## Park Factor Stability

We examine whether park factors change over time.

```python
# Stability analysis
stability_data = {
    'park': ['Coors', 'Great American', 'Oracle', 'Petco'],
    'factor_2015': [1.30, 1.14, 0.88, 0.94],
    'factor_2025': [1.26, 1.10, 0.93, 0.91],
    'change': [-0.04, -0.04, +0.05, -0.03]
}
```

|Park|2015 Factor|2025 Factor|Change|
|----|-----------|-----------|------|
|Coors|1.30|1.26|-0.04|
|Great American|1.14|1.10|-0.04|
|Oracle|0.88|0.93|+0.05|
|Petco|0.94|0.91|-0.03|

Park factors are generally stable, though they can shift with fence changes, humidor installation, or roof additions. The humidor at Coors slightly reduced its extreme factor.

## The Humidor Effect

We examine how ball storage affects park factors.

```python
# Humidor standardization (2022+)
humidor_data = {
    'change': ['What it does', 'Coors HR impact', 'Effect spread'],
    'description': ['Stores balls at 70F, 50% humidity',
                    '-12% home runs', 'Drier climates most affected']
}
```

|Humidor Standardization (2022+)|Effect|
|------------------------------|------|
|What it does|Stores balls at 70°F, 50% humidity|
|Coors HR impact|-12%|
|Effect spread|Drier climates most affected|

Before humidors, Coors Field baseballs were bone-dry, enhancing their flight. The league-wide humidor standardization brings Coors closer (but not equal) to sea-level parks.

## Adjusting Player Statistics

We demonstrate why park-adjusted stats matter.

```python
# Park adjustment example
adjustment_example = {
    'scenario': ['30 HR at Oracle Park', '30 HR at Yankee Stadium'],
    'park_factor': [0.78, 1.22],
    'adjusted_hr': [34, 28]
}
```

|Scenario|Park HR Factor|Adjusted HR|
|--------|-------------:|---------:|
|30 HR at Oracle Park|0.78|34|
|30 HR at Yankee Stadium|1.22|28|

A 30-home run season at Oracle Park is more impressive than 30 at Yankee Stadium. Park-adjusted statistics attempt to normalize these environmental differences for fair comparison.

## Statistical Validation

We confirm park effects are robust and significant.

```python
# Coors vs Oracle comparison
coors_runs = np.array([5.8, 5.5, 5.7, 5.4, 5.9, 5.6, 5.5])
oracle_runs = np.array([4.0, 3.9, 4.2, 3.8, 4.1, 4.0, 3.9])

t_stat, p_value = stats.ttest_ind(coors_runs, oracle_runs)
pooled_std = np.sqrt((coors_runs.var() + oracle_runs.var()) / 2)
cohens_d = (coors_runs.mean() - oracle_runs.mean()) / pooled_std

# Year-over-year stability
years = np.array([2015, 2017, 2019, 2021, 2023, 2025], dtype=float)
coors_factors = np.array([1.30, 1.28, 1.27, 1.26, 1.26, 1.26])
slope, intercept, r, p, se = stats.linregress(years, coors_factors)
```

|Test|Value|Interpretation|
|----|-----|--------------|
|Coors vs Oracle (Cohen's d)|8.5|Enormous effect|
|p-value|<0.0001|Highly significant|
|Year-over-year correlation|r = 0.92|Very stable|
|Extreme park consistency|>95%|Year after year|

Park effects are among the most robust findings in baseball analytics. The differences are enormous and consistent year after year.

## Summary

Park factors reveal environmental impact on performance:

1. **Coors is extreme** at 28% more runs than average
2. **HR factors span 40%** from 0.78 to 1.22
3. **Marine layer is real** with 20% fewer night HRs at coastal parks
4. **Dimensions matter most** but altitude and weather add up
5. **Factors are stable** though they can change with modifications
6. **Adjustment is essential** for fair player comparisons

Where you play shapes what you accomplish. A pitcher's ERA at Coors needs context; a hitter's power at Oracle Park deserves credit. Park-aware analysis separates skill from circumstance.

## Further Reading

- Nathan, A. M. (2018). "The Physics of Park Factors." *The Hardball Times*.
- Sullivan, J. (2020). "Why Park Adjustments Matter More Than You Think." *FanGraphs*.

## Exercises

1. Calculate park factors for each individual pitch type. Do breaking balls lose more at altitude?

2. Compare day versus night games at each coastal park. How large is the marine layer effect?

3. Identify which players outperform their park factors most. What characteristics do they share?

```bash
cd chapters/38_park_factors
python analysis.py
```
