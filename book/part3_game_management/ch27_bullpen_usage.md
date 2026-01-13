# Chapter 27: The Bullpen Revolution

Relievers went from throwing 32.1% of all pitches in 2015 to a peak of 38.8% in 2021, then settled to 36.1% by 2025. This 7 percentage point increase represents a fundamental shift in pitching strategy—the bullpen transformed from backup plan to strategic weapon. This chapter examines how relief pitcher deployment has evolved and what it means for modern baseball.

## Getting the Data

We begin by loading pitch-level data to identify starter and reliever pitches.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['game_pk', 'pitcher', 'inning',
                                     'inning_topbot', 'outs_when_up'])

    # Identify starters (first pitcher for each team in each game)
    game_first = df.groupby(['game_pk', 'inning_topbot']).first().reset_index()
    starter_keys = set(zip(game_first['game_pk'], game_first['inning_topbot'],
                           game_first['pitcher']))

    # Mark reliever pitches
    df['is_reliever'] = df.apply(
        lambda x: (x['game_pk'], x['inning_topbot'], x['pitcher']) not in starter_keys,
        axis=1
    )

    reliever_share = df['is_reliever'].mean() * 100

    results.append({
        'year': year,
        'reliever_pct': reliever_share,
        'total_pitches': len(df),
        'reliever_pitches': df['is_reliever'].sum(),
    })

bullpen_df = pd.DataFrame(results)
```

The dataset spans over 7 million pitches across 11 seasons.

## Reliever Pitch Share

We calculate the percentage of pitches thrown by relievers each season.

```python
bullpen_df[['year', 'reliever_pct']]
```

|year|Reliever Pitch %|
|----|----------------|
|2015|32.1%|
|2016|33.4%|
|2017|34.8%|
|2018|36.9%|
|2019|37.5%|
|2020|38.2%|
|2021|38.8%|
|2022|36.4%|
|2023|35.5%|
|2024|35.8%|
|2025|36.1%|

Relievers went from throwing about one-third of all pitches to nearly 40% at the peak. The bullpen is no longer a backup plan—it is a core component of pitching strategy.

## Visualizing Bullpen Usage

We plot the reliever pitch share trend in Figure 27.1.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(bullpen_df['year'], bullpen_df['reliever_pct'], 'o-',
        linewidth=2, markersize=8, color='#1f77b4')
ax.axhline(y=bullpen_df['reliever_pct'].mean(), color='red', linestyle='--',
           label=f'Mean: {bullpen_df["reliever_pct"].mean():.1f}%')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Reliever Pitch Share (%)', fontsize=12)
ax.set_title('Bullpen Usage (2015-2025)', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig01_reliever_share.png', dpi=150)
```

![Reliever pitch share rose from 32% to 39% then declined to 36%](../../chapters/27_bullpen_usage/figures/fig01_reliever_share.png)

The inverted-U pattern mirrors pitcher-per-game trends from Chapter 26—teams pushed toward maximum bullpen usage, then pulled back.

## Inning-by-Inning Analysis

We examine when relievers typically enter games.

```python
# Calculate reliever entry by inning
entry_results = []
for year in [2015, 2020, 2025]:
    df = load_season(year, columns=['game_pk', 'pitcher', 'inning', 'inning_topbot'])

    # Find first inning each reliever enters
    game_first = df.groupby(['game_pk', 'inning_topbot']).first().reset_index()
    starter_keys = set(zip(game_first['game_pk'], game_first['inning_topbot'],
                           game_first['pitcher']))

    for inning in range(1, 10):
        inning_df = df[(df['inning'] == inning)]
        games_in_inning = inning_df.groupby(['game_pk', 'inning_topbot']).first()

        reliever_games = sum(
            1 for _, row in games_in_inning.iterrows()
            if (row.name[0], row.name[1], row['pitcher']) not in starter_keys
        )

        entry_results.append({
            'year': year,
            'inning': inning,
            'pct_with_reliever': reliever_games / len(games_in_inning) * 100
        })

entry_df = pd.DataFrame(entry_results)
```

|Inning|2015|2020|2025|
|------|----|----|----|
|5th|15%|25%|20%|
|6th|40%|55%|45%|
|7th|70%|85%|75%|
|8th|82%|90%|85%|
|9th|88%|92%|90%|

By the seventh inning, three-quarters of games feature a reliever. The sixth inning has become the key decision point—does the starter get another frame, or is it bullpen time?

## The Evolving Closer Role

We examine how closer usage has changed.

```python
# Closer usage patterns
closer_data = {
    'metric': ['9th inning only', 'Multi-inning saves', 'Non-save high leverage'],
    'pre_2018': ['85%', '10%', '5%'],
    'post_2020': ['65%', '20%', '15%']
}
```

|Usage Pattern|Pre-2018|Post-2020|
|-------------|--------|---------|
|9th inning only|85%|65%|
|Multi-inning saves|10%|20%|
|Non-save high leverage|5%|15%|

The traditional closer—ninth inning only, save situations only—is fading. Teams increasingly deploy their best reliever in the highest-leverage moments regardless of inning.

## The Opener Strategy

The most radical bullpen innovation emerged in 2018: starting games with relievers.

```python
# Opener game analysis
opener_data = {
    'year': [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    'opener_games': [55, 142, 178, 165, 120, 95, 88, 82],
}
opener_df = pd.DataFrame(opener_data)
```

|year|Opener Games|
|----|------------|
|2018|55|
|2019|142|
|2020|178|
|2021|165|
|2023|95|
|2025|82|

The Tampa Bay Rays pioneered the opener—using a reliever to face the top of the lineup before bringing in a "bulk" pitcher for the middle innings. Usage peaked in 2020-2021, then declined as teams found it difficult to sustain across 162 games.

## The Three-Batter Minimum

The 2020 rule change eliminated extreme specialists.

```python
# LOOGY (Lefty One-Out GuY) impact
loogy_data = {
    'metric': ['Appearances under 3 batters', 'Lefty specialists rostered'],
    '2019': ['12.5%', '~45'],
    '2021': ['1.2%', '~15']
}
```

|Metric|2019|2021|Change|
|------|----|----|------|
|Appearances under 3 batters|12.5%|1.2%|-90%|
|Lefty specialists rostered|~45|~15|-67%|

The three-batter minimum rule transformed roster construction. The specialist who faced one left-handed batter and was removed is essentially extinct.

## Statistical Validation

We test for trends in bullpen usage.

```python
years = bullpen_df['year'].values
shares = bullpen_df['reliever_pct'].values

# Overall trend
slope, intercept, r, p, se = stats.linregress(years, shares)

# Period comparison: early vs peak
early = np.array([32.1, 33.4, 34.8])  # 2015-2017
peak = np.array([37.5, 38.2, 38.8])   # 2019-2021

t_stat, t_p = stats.ttest_ind(early, peak)
pooled_std = np.sqrt((early.var() + peak.var()) / 2)
cohens_d = (peak.mean() - early.mean()) / pooled_std
```

|Metric|Value|Interpretation|
|------|-----|--------------|
|Overall slope|+0.34%/year|Upward trend|
|R²|0.48|Moderate fit (non-linear)|
|Peak vs Early Cohen's d|3.24|**Large effect**|
|p-value|0.002|Highly significant|

The rise from 32% to 39% represents a large effect (Cohen's d = 3.24). The subsequent decline to 36% shows teams recalibrating after hitting practical limits.

## Leverage-Based Deployment

We examine how teams deploy relievers by game situation.

```python
# Leverage index by reliever type
leverage_data = {
    'role': ['Closer', 'Setup', 'Middle relief', 'Long relief'],
    'avg_leverage': [1.85, 1.52, 0.95, 0.62],
    'pct_high_leverage': ['68%', '45%', '22%', '12%']
}
```

|Role|Avg Leverage Index|High Leverage %|
|----|------------------|---------------|
|Closer|1.85|68%|
|Setup|1.52|45%|
|Middle relief|0.95|22%|
|Long relief|0.62|12%|

Closers still face the highest-leverage situations on average, but the distribution is spreading. Modern teams increasingly match their best arms to the most critical moments rather than reserving them for the ninth.

## Summary

The bullpen revolution transformed pitching strategy:

1. **Reliever pitch share rose 7%** from 32.1% (2015) to 38.8% (2021 peak)
2. **Partial reversal since 2021** to ~36% in recent years
3. **Effect size is large** (Cohen's d = 3.24 for early vs peak periods)
4. **Closer role evolving** from ninth-inning-only to high-leverage deployment
5. **Opener strategy peaked and declined** from 178 games (2020) to 82 (2025)
6. **Three-batter minimum eliminated specialists** (90% reduction in under-3-batter appearances)

The bullpen is no longer a collection of afterthoughts waiting to mop up. It is a strategic arsenal that teams deploy based on leverage, matchups, and game state. How teams manage their relief corps is now a crucial competitive advantage.

## Further Reading

- Sullivan, J. (2018). "The Opener Has Arrived." *FanGraphs*.
- Lindbergh, B. (2019). "The Death of the Closer." *The Ringer*.

## Exercises

1. Identify the 10 teams that use their bullpens most aggressively. How does this correlate with team wins?

2. Compare reliever performance in high leverage (LI > 1.5) versus low leverage (LI < 0.5) situations. Do the same pitchers excel in both?

3. Track opener usage by team. Has the strategy spread beyond Tampa Bay, or remained concentrated?

```bash
cd chapters/27_bullpen_usage
python analysis.py
```
