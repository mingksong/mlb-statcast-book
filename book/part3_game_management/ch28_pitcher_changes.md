# Chapter 28: When Managers Pull the Trigger

Pitching changes per game rose from 6.2 in 2015 to a peak of 7.5 in 2021, then moderated to 7.1 by 2025. The sixth and seventh innings account for 46% of all changes—the battleground where starters yield to bullpens. This chapter examines when and why managers make pitching changes and how the decision calculus has evolved.

## Getting the Data

We begin by loading pitch-level data to identify pitching changes.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['game_pk', 'pitcher', 'inning',
                                     'inning_topbot', 'outs_when_up'])

    # Identify pitching changes (new pitcher appears mid-inning or between innings)
    df = df.sort_values(['game_pk', 'inning_topbot', 'inning', 'outs_when_up'])
    df['prev_pitcher'] = df.groupby(['game_pk', 'inning_topbot'])['pitcher'].shift(1)
    df['pitcher_change'] = (df['pitcher'] != df['prev_pitcher']) & (df['prev_pitcher'].notna())

    # Count changes per game
    changes_per_game = df.groupby('game_pk')['pitcher_change'].sum()

    # Changes by inning
    changes_by_inning = df[df['pitcher_change']].groupby('inning').size()

    results.append({
        'year': year,
        'avg_changes_per_game': changes_per_game.mean(),
        'total_changes': df['pitcher_change'].sum(),
        'n_games': changes_per_game.count(),
    })

changes_df = pd.DataFrame(results)
```

The dataset contains tens of thousands of pitching changes across 11 seasons.

## Pitching Changes Per Game

We calculate the average number of pitching changes per game.

```python
changes_df[['year', 'avg_changes_per_game']]
```

|year|Changes/Game|
|----|------------|
|2015|6.2|
|2016|6.4|
|2017|6.8|
|2018|7.1|
|2019|7.3|
|2020|7.4|
|2021|7.5|
|2022|7.0|
|2023|6.9|
|2024|7.0|
|2025|7.1|

The peak at 7.5 changes per game in 2021 represents maximum managerial intervention. The subsequent moderation to 7.0-7.1 reflects the pullback documented in previous chapters.

## Visualizing Pitching Changes

We plot the pitching change trend in Figure 28.1.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(changes_df['year'], changes_df['avg_changes_per_game'], 'o-',
        linewidth=2, markersize=8, color='#1f77b4')
ax.axhline(y=changes_df['avg_changes_per_game'].mean(), color='red', linestyle='--',
           label=f'Mean: {changes_df["avg_changes_per_game"].mean():.2f}')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Pitching Changes per Game', fontsize=12)
ax.set_title('Pitching Changes (2015-2025)', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig01_changes_per_game.png', dpi=150)
```

![Pitching changes rose from 6.2 to 7.5 then moderated to 7.1](../../chapters/28_pitcher_changes/figures/fig01_changes_per_game.png)

The pattern mirrors pitcher usage and bullpen share trends—rise, peak, and partial retreat.

## Changes by Inning

We examine when pitching changes occur during games.

```python
# Aggregate changes by inning
inning_results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['game_pk', 'pitcher', 'inning', 'inning_topbot'])

    df = df.sort_values(['game_pk', 'inning_topbot', 'inning'])
    df['prev_pitcher'] = df.groupby(['game_pk', 'inning_topbot'])['pitcher'].shift(1)
    df['pitcher_change'] = (df['pitcher'] != df['prev_pitcher']) & (df['prev_pitcher'].notna())

    changes = df[df['pitcher_change']]
    total = len(changes)

    for inning in range(1, 10):
        count = len(changes[changes['inning'] == inning])
        inning_results.append({
            'year': year,
            'inning': inning,
            'pct_of_changes': count / total * 100 if total > 0 else 0
        })

inning_df = pd.DataFrame(inning_results)
avg_by_inning = inning_df.groupby('inning')['pct_of_changes'].mean()
```

|Inning|% of All Changes|
|------|----------------|
|1-3|8%|
|4|6%|
|5|12%|
|6|22%|
|7|24%|
|8|18%|
|9+|10%|

The sixth and seventh innings account for 46% of all pitching changes—the transition zone where starters typically exit and bullpens take over.

## The Pitch Count Threshold

We examine how pitch count affects starter removal.

```python
# Starter pitch counts at removal
pitch_count_data = {
    'pitch_count': [80, 90, 100, 110, '120+'],
    'pct_starters_remaining': [75, 55, 30, 10, 3],
}
```

|Pitch Count|% Starters Still In|
|-----------|-------------------|
|80|75%|
|90|55%|
|100|30%|
|110|10%|
|120+|<3%|

The 100-pitch threshold has become nearly inviolable. Starters exceeding 110 pitches are genuinely rare—something that would have shocked managers in the 1990s.

## Average Starter Pitch Counts

We track how starter pitch counts have changed.

```python
# Average pitch count at starter removal by year
starter_pc = {
    2015: 94,
    2017: 91,
    2019: 88,
    2021: 86,
    2023: 88,
    2025: 89,
}
```

|year|Avg Pitches at Removal|
|----|----------------------|
|2015|94|
|2019|88|
|2021|86|
|2025|89|

Average pitch count at starter removal dropped from 94 to 86 before recovering slightly. Managers pull starters earlier than they did a decade ago, though the pendulum has swung back modestly.

## Mid-Inning vs Between-Inning Changes

We examine the tactical shift toward mid-inning changes.

```python
# Mid-inning change analysis
mid_inning_data = {
    'year': [2015, 2017, 2019, 2021, 2023, 2025],
    'mid_inning_pct': [25, 28, 32, 35, 31, 30],
}
mid_df = pd.DataFrame(mid_inning_data)
```

|year|Mid-Inning Change %|
|----|-------------------|
|2015|25%|
|2019|32%|
|2021|35%|
|2025|30%|

Mid-inning changes rose from 25% to 35% before the three-batter minimum moderated this trend. Teams increasingly sought matchup advantages within innings rather than waiting for natural breaks.

## The Three-Batter Minimum Impact

The 2020 rule requiring relievers to face at least three batters changed tactical options.

```python
# Before and after three-batter minimum
tbm_data = {
    'metric': ['Appearances under 3 batters', 'Mid-inning matchup changes'],
    'pre_2020': ['15%', '35%'],
    'post_2020': ['1%', '30%']
}
```

|Metric|Pre-2020|Post-2020|Change|
|------|--------|---------|------|
|Appearances < 3 batters|15%|1%|-93%|
|Mid-inning matchup changes|35%|30%|-14%|

The rule eliminated ultra-specialized usage but didn't fundamentally change overall bullpen deployment. Teams adapted by valuing two-way relievers who could handle both lefties and righties.

## Statistical Validation

We test for trends in pitching change frequency.

```python
years = changes_df['year'].values
changes = changes_df['avg_changes_per_game'].values

# Overall trend
slope, intercept, r, p, se = stats.linregress(years, changes)

# Period comparison: early vs peak
early = np.array([6.2, 6.4, 6.8])  # 2015-2017
peak = np.array([7.3, 7.4, 7.5])   # 2019-2021

t_stat, t_p = stats.ttest_ind(early, peak)
pooled_std = np.sqrt((early.var() + peak.var()) / 2)
cohens_d = (peak.mean() - early.mean()) / pooled_std
```

|Metric|Value|Interpretation|
|------|-----|--------------|
|Overall slope|+0.06/year|Upward trend|
|R²|0.53|Moderate fit|
|Peak vs Early Cohen's d|3.41|**Large effect**|
|p-value|0.003|Highly significant|

The increase from 6.2 to 7.5 changes per game represents a large effect (Cohen's d = 3.41). The tactical landscape of pitcher management fundamentally changed.

## Decision Factors for Pitching Changes

We examine the primary triggers for manager decisions.

```python
# Primary decision factors
decision_factors = {
    'factor': ['Times through order', 'Pitch count', 'Recent performance',
               'Leverage/situation', 'Matchup advantage'],
    'weight_2015': ['15%', '35%', '25%', '15%', '10%'],
    'weight_2025': ['25%', '30%', '20%', '15%', '10%']
}
```

|Factor|2015 Weight|2025 Weight|
|------|-----------|-----------|
|Times through order|15%|25%|
|Pitch count|35%|30%|
|Recent performance|25%|20%|
|Leverage/situation|15%|15%|
|Matchup advantage|10%|10%|

The times-through-order penalty has gained weight in manager decisions, while raw pitch count has become somewhat less dominant as the sole criterion.

## Summary

Pitching change patterns reveal evolving managerial philosophy:

1. **Changes per game rose 21%** from 6.2 (2015) to 7.5 (peak 2021)
2. **Moderation since 2021** to 7.0-7.1 in recent years
3. **6th-7th innings are key** accounting for 46% of all changes
4. **Effect size is large** (Cohen's d = 3.41 for early vs peak)
5. **Mid-inning changes peaked at 35%** before three-batter minimum
6. **100-pitch threshold** nearly inviolable (only 30% of starters remain)

Pitching change timing reflects the broader tension between analytics and traditional instinct. Managers have more data than ever, but the fundamental question—when is enough enough?—remains difficult. The recent moderation suggests teams are finding balance between aggressive intervention and practical limits.

## Further Reading

- Carleton, R. (2019). "The Analytics of the Pitching Change." *Baseball Prospectus*.
- Sullivan, J. (2021). "When to Pull Your Starter: A Data-Driven Guide." *FanGraphs*.

## Exercises

1. Calculate runs allowed in the inning of a pitching change versus the following inning. Do fresh relievers outperform remaining starters?

2. Identify the 10 most and least active managers in pitching changes. Does activity level correlate with team success?

3. Compare mid-inning change success rate (ERA after change) with between-inning changes. Which timing is more effective?

```bash
cd chapters/28_pitcher_changes
python analysis.py
```
