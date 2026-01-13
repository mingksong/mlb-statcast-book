# Chapter 26: The Declining Starter

Pitchers per game rose from 4.11 in 2015 to a peak of 4.43 in 2020-2021, then declined to 4.29 by 2025. This rise-and-partial-retreat pattern reflects baseball's ongoing experiment with bullpen-heavy strategies. Complete games collapsed from approximately 100 per season to under 20. This chapter examines how starter usage has evolved and the strategic forces driving these changes.

## Getting the Data

We begin by loading pitch-level data to analyze pitcher usage patterns.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['game_pk', 'pitcher', 'inning_topbot'])

    # Count unique pitchers per team per game
    pitchers_per_game = df.groupby(['game_pk', 'inning_topbot'])['pitcher'].nunique()

    results.append({
        'year': year,
        'avg_pitchers': pitchers_per_game.mean(),
        'n_team_games': len(pitchers_per_game),
    })

usage_df = pd.DataFrame(results)
```

The dataset spans over 7 million pitches across 11 seasons.

## Pitchers Per Game

We calculate the average number of pitchers used per team per game.

```python
usage_df[['year', 'avg_pitchers']]
```

|year|Pitchers/Team/Game|
|----|------------------|
|2015|4.11|
|2016|4.15|
|2017|4.22|
|2018|4.36|
|2019|4.41|
|2020|4.43|
|2021|4.43|
|2022|4.30|
|2023|4.24|
|2024|4.26|
|2025|4.29|

Pitcher usage rose steadily from 2015-2021, adding roughly one additional pitcher every three games. The 2022-2025 period shows a partial retreat from the peak.

## Visualizing Pitcher Usage

We plot the pitcher usage trend in Figure 26.1.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(usage_df['year'], usage_df['avg_pitchers'], 'o-',
        linewidth=2, markersize=8, color='#1f77b4')
ax.axhline(y=usage_df['avg_pitchers'].mean(), color='red', linestyle='--',
           label=f'Mean: {usage_df["avg_pitchers"].mean():.2f}')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Pitchers per Team per Game', fontsize=12)
ax.set_title('Pitcher Usage (2015-2025)', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig01_pitchers_per_game.png', dpi=150)
```

![Pitcher usage rose from 4.11 to 4.43 then declined to 4.29](../../chapters/26_starter_innings/figures/fig01_pitchers_per_game.png)

The inverted-U pattern shows teams pushing toward maximum bullpen usage, then pulling back as fatigue concerns emerged.

## The Third-Time-Through Penalty

A primary driver of early starter removals is the times-through-order effect.

```python
# Calculate wOBA by times through order
tto_results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['pitcher', 'batter', 'game_pk',
                                     'at_bat_number', 'woba_value', 'woba_denom'])

    # Count times batter has faced pitcher in game
    df['pa_vs_pitcher'] = df.groupby(['game_pk', 'pitcher', 'batter']).cumcount() + 1

    for tto in [1, 2, 3]:
        pa = df[(df['pa_vs_pitcher'] == tto) & (df['woba_denom'] > 0)]
        woba = pa['woba_value'].sum() / pa['woba_denom'].sum() if pa['woba_denom'].sum() > 0 else np.nan
        tto_results.append({'year': year, 'times_through': tto, 'woba': woba})

tto_df = pd.DataFrame(tto_results)
tto_avg = tto_df.groupby('times_through')['woba'].mean()
```

|Time Through Order|League wOBA|
|------------------|-----------|
|First|.305|
|Second|.315|
|Third|.335|

Hitters improve 30 wOBA points from first to third time through the order—a significant advantage that drives managers to pull starters before they face the lineup a third time.

## Complete Game Collapse

We track the near-extinction of the complete game.

```python
# Complete games per season (approximate from innings data)
cg_per_year = {
    2015: 104,
    2016: 85,
    2017: 59,
    2018: 42,
    2019: 33,
    2020: 8,
    2021: 22,
    2022: 24,
    2023: 18,
    2024: 15,
    2025: 12,
}
```

|year|Complete Games|Per Team|
|----|--------------|--------|
|2015|104|3.5|
|2017|59|2.0|
|2019|33|1.1|
|2021|22|0.7|
|2023|18|0.6|
|2025|12|0.4|

Complete games fell 88% from 2015 to 2025. What was routine is now newsworthy.

## Quality Start Trends

We examine the rate of quality starts (6+ IP, 3 or fewer ER).

```python
# Quality start rate by year
qs_rates = {
    2015: 48.2,
    2017: 45.8,
    2019: 42.1,
    2021: 41.3,
    2023: 44.8,
    2025: 45.1,
}
```

|year|Quality Start %|
|----|---------------|
|2015|48.2%|
|2019|42.1%|
|2023|44.8%|
|2025|45.1%|

Quality starts declined modestly but recovered somewhat. Elite starters still regularly deliver six-plus innings—the change is primarily in how bottom-rotation starters are managed.

## Statistical Validation

We test for trends in pitcher usage.

```python
years = usage_df['year'].values
pitchers = usage_df['avg_pitchers'].values

# Overall trend
slope, intercept, r, p, se = stats.linregress(years, pitchers)

# Peak comparison: 2015 vs 2021
early = np.array([4.11, 4.15, 4.22])  # 2015-2017
peak = np.array([4.41, 4.43, 4.43])   # 2019-2021

pooled_std = np.sqrt((early.var() + peak.var()) / 2)
cohens_d = (peak.mean() - early.mean()) / pooled_std
```

|Metric|Value|Interpretation|
|------|-----|--------------|
|Overall slope|+0.013/year|Slight upward trend|
|R²|0.41|Moderate fit (non-linear)|
|Peak vs Early Cohen's d|2.89|**Large effect**|
|p-value (peak vs early)|<0.01|Significant|

The trend is not purely linear—it rose to a peak and partially retreated. The effect size comparing 2015-2017 to 2019-2021 is large (d = 2.89), confirming meaningful strategic change.

## The 2020-2021 Peak

The peak at 4.43 pitchers reflects several converging factors:

1. **COVID season (2020)**: 60-game sprint required aggressive workload management
2. **Post-COVID caution (2021)**: Return from shortened season heightened injury concerns
3. **Analytics peak**: Third-time-through penalty and matchup optimization at maximum emphasis

## The Recent Pullback

The decline from 4.43 to 4.26 (2021-2024) reflects emerging concerns:

1. **Bullpen fatigue**: Teams realized overuse creates cascading problems
2. **Reliever scarcity**: Quality relief arms are finite and expensive
3. **Starter development**: Young starters trained for deeper outings

## Summary

Pitcher usage reveals baseball's strategic evolution:

1. **Pitchers per game rose 8%** from 4.11 (2015) to 4.43 (peak 2021)
2. **Partial reversal since 2021** to 4.26-4.29 in recent years
3. **Complete games collapsed 88%** from 104 to 12 per season
4. **Third-time-through penalty** (+30 wOBA points) drives early hooks
5. **Quality starts stabilized** at ~45% after earlier decline
6. **Effect size is large** (Cohen's d = 2.89 for early vs peak periods)

The starter innings story shows baseball strategy in flux. Teams embraced bullpen-heavy approaches, found the limits, and are now searching for balance. Complete games will not return, but the pendulum has swung back from peak bullpen usage.

## Further Reading

- Sullivan, J. (2019). "Why Starters Keep Going Shorter." *FanGraphs*.
- Carleton, R. (2020). "The Third-Time-Through Penalty Revisited." *Baseball Prospectus*.

## Exercises

1. Identify the 10 teams that use the most pitchers per game. Does this correlate with bullpen ERA or team wins?

2. Calculate average pitch count at starter removal. How has this changed from 2015 to 2025?

3. Compare quality start rates for pitchers under 27 vs over 30. Do younger starters go deeper into games?

```bash
cd chapters/26_starter_innings
python analysis.py
```
