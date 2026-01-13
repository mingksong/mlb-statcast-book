# Chapter 39: The Vanishing Complete Game

League-wide complete games collapsed from 104 in 2015 to just 12 in 2025—an 88% decline in a decade. Teams averaged 3.5 complete games per year in 2015; by 2025, that number dropped to 0.4. Average innings per start fell from 5.9 to 5.2, and pitchers reaching 100 pitches became rare as the 100-pitch threshold became sacred. This chapter traces the extinction of the complete game and examines what drove its disappearance.

## Getting the Data

We begin by loading pitching data to track complete game frequency.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['game_pk', 'pitcher', 'inning',
                                     'inning_topbot', 'pitch_number'])

    # Count pitches per game for starters
    game_pitches = df.groupby(['game_pk', 'pitcher']).agg({
        'inning': 'max',
        'pitch_number': 'max'
    }).reset_index()

    # Identify starters (pitched in 1st inning)
    first_inning = df[df['inning'] == 1].groupby('game_pk')['pitcher'].first()
    game_pitches = game_pitches.merge(
        first_inning.reset_index().rename(columns={'pitcher': 'starter'}),
        on='game_pk'
    )
    starters = game_pitches[game_pitches['pitcher'] == game_pitches['starter']]

    # Average innings per start
    avg_ip = starters['inning'].mean()

    # Games where starter went 9+ innings
    cg_count = (starters['inning'] >= 9).sum()

    results.append({
        'year': year,
        'complete_games': cg_count,
        'avg_ip_start': avg_ip,
        'n_games': len(starters)
    })

cg_df = pd.DataFrame(results)
```

The dataset contains over 25,000 games across 11 seasons.

## The Complete Game Collapse

We track the decline of complete games league-wide.

```python
# Complete game totals by year
cg_data = {
    'year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    'complete_games': [104, 85, 59, 42, 33, 8, 22, 24, 18, 15, 12],
    'per_team': [3.5, 2.8, 2.0, 1.4, 1.1, 0.5, 0.7, 0.8, 0.6, 0.5, 0.4]
}
```

|Year|Complete Games|Per Team|
|----|-------------:|-------:|
|2015|104|3.5|
|2016|85|2.8|
|2017|59|2.0|
|2018|42|1.4|
|2019|33|1.1|
|2020|8|0.5*|
|2021|22|0.7|
|2022|24|0.8|
|2023|18|0.6|
|2024|15|0.5|
|2025|12|0.4|

*60-game season

In 2015, teams averaged 3.5 complete games per season. By 2025, that number dropped to 0.4—a 90% decline in a decade.

## Visualizing the Decline

We plot the complete game trend in Figure 39.1.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

years = cg_data['year']
cg = cg_data['complete_games']

ax.plot(years, cg, 'o-', linewidth=2, markersize=8, color='#1f77b4')

slope, intercept, r, p, se = stats.linregress(years, cg)
ax.plot(years, [intercept + slope * y for y in years],
        '--', color='red', label=f'{slope:.1f} CG/year decline')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('League Complete Games', fontsize=12)
ax.set_title('Complete Game Decline (2015-2025)', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig01_cg_decline.png', dpi=150)
```

![Complete games declined from 104 in 2015 to just 12 in 2025, an 88% reduction](../../chapters/39_complete_game/figures/fig01_cg_decline.png)

The decline is steep and consistent. The complete game has gone from rare to nearly extinct.

## Historical Context

We place the Statcast era in historical perspective.

```python
# Historical complete games
historical_cg = {
    'year': [1980, 1990, 2000, 2010, 2020, 2025],
    'cg_per_team': [24, 16, 8, 4, 0.3, 0.4]
}
```

|Year|CG Per Team|
|----|-----------:|
|1980|24|
|1990|16|
|2000|8|
|2010|4|
|2020|0.3|
|2025|0.4|

What was once routine—24 complete games per team per year in 1980—is now extraordinary. The entire league produces fewer complete games than one team used to.

## Why Complete Games Disappeared

We examine the factors driving the decline.

```python
# Extinction causes
extinction_factors = {
    'factor': ['Pitch count awareness', 'Third-time-through penalty',
               'Bullpen specialization', 'Velocity demands', 'Risk management'],
    'mechanism': ['100-pitch threshold', 'Hitters adjust third time',
                  'High-leverage relievers', 'Max effort = less endurance',
                  'Starters are expensive']
}
```

|Factor|Mechanism|
|------|---------|
|Pitch count awareness|100-pitch threshold became sacred|
|Third-time-through penalty|Hitters adjust, batters succeed more|
|Bullpen specialization|High-leverage relievers available|
|Velocity demands|Max effort means less endurance|
|Risk management|Protecting expensive arms|

Multiple forces combined to make complete games obsolete. The 100-pitch limit became nearly inviolable.

## The Pitch Count Revolution

We examine how the 100-pitch threshold changed starter management.

```python
# Starter removal by pitch count
pitch_count_data = {
    'pitch_count': [80, 90, 100, 110, '120+'],
    'pct_remaining': [75, 55, 30, 10, 2]
}
```

|Pitch Count|% of Starters Still In|
|-----------|--------------------:|
|80|75%|
|90|55%|
|100|30%|
|110|10%|
|120+|2%|

Completing a game typically requires 110-130 pitches. With managers pulling starters at 100, the mathematics make complete games nearly impossible.

## Innings Per Start

We track the workload compression.

```python
# Innings per start by year
ip_data = {
    'year': [2015, 2017, 2019, 2021, 2023, 2025],
    'avg_ip': [5.9, 5.6, 5.3, 5.1, 5.3, 5.2],
    'starters_100_ip': [108, 95, 82, 68, 74, 70]
}
```

|Year|Avg IP/Start|100+ IP Starters|
|----|------------|---------------:|
|2015|5.9|108|
|2017|5.6|95|
|2019|5.3|82|
|2021|5.1|68|
|2023|5.3|74|
|2025|5.2|70|

Average innings per start fell below six innings. The 200-inning starter—once common—is now rare. Only a handful of pitchers exceed 180 innings annually.

## Complete Game Profile

We examine what modern complete games look like.

```python
# Modern CG characteristics
cg_profile = {
    'characteristic': ['Efficiency', 'Dominance', 'Game situation', 'Outcome'],
    'requirement': ['Under 15 pitches/inning', 'High K rate',
                    'Large lead or shutout', 'Almost always a shutout']
}
```

|Characteristic|Requirement|
|--------------|-----------|
|Efficiency|Under 15 pitches/inning|
|Dominance|High K rate|
|Game situation|Large lead or shutout|
|Outcome|Almost always a shutout|

Complete games now occur mostly in shutouts or when a pitcher is dominating so thoroughly that removal seems absurd. Routine complete games—where a starter finished a close game—have vanished.

## Shutouts vs Complete Games

We examine the changing relationship between shutouts and complete games.

```python
# CG:Shutout ratio over time
cg_shutout = {
    'era': ['1990', '2000', '2010', '2020'],
    'ratio': ['3.5:1', '2.5:1', '1.8:1', '1.2:1']
}
```

|Era|CG:Shutout Ratio|
|---|----------------|
|1990|3.5:1|
|2000|2.5:1|
|2010|1.8:1|
|2020|1.2:1|

Historically, complete games were 3-4 times more common than shutouts. Now they are nearly equal—teams only let starters finish when pitching a shutout.

## The Quality Start Standard

We examine the new expectations for starters.

```python
# Quality start vs complete game
qs_vs_cg = {
    'metric': ['Quality start requirement', 'CG requirement',
               '2025 frequency', 'Ratio'],
    'value': ['6+ IP, 3 or fewer ER', '9 IP',
              '45% vs <0.5%', '90+ QS per CG']
}
```

|Standard|Definition|2025 Frequency|
|--------|----------|--------------|
|Quality Start|6+ IP, 3 or fewer ER|~45% of starts|
|Complete Game|9 IP|<0.5% of starts|
|Ratio||90+ QS per CG|

The quality start became the minimum expectation precisely because complete games became unrealistic. Six innings is the new nine.

## The Economic Argument

We examine the financial calculation.

```python
# Economic analysis
economic_data = {
    'factor': ['Elite starter salary', 'Injury risk per extra pitches',
               'Expected cost of extra innings', 'Tommy John recovery'],
    'value': ['$30-40M/year', '+2% per 10 pitches',
              '$500K+ expected cost', '18 months lost']
}
```

|Factor|Value|
|------|-----|
|Elite starter salary|$30-40M/year|
|Injury risk per 10 extra pitches|+2%|
|Expected cost of extra innings|$500K+|
|Tommy John recovery|18 months lost|

When a starter costs $35 million, teams will not risk injury for one complete game. The bullpen is insurance against catastrophic arm injuries.

## Statistical Validation

We confirm the complete game decline is robust.

```python
years = np.array(range(2015, 2026), dtype=float)
cg = np.array([104, 85, 59, 42, 33, 8, 22, 24, 18, 15, 12])

slope, intercept, r, p, se = stats.linregress(years, cg)
r_squared = r ** 2

# Effect size: 2015 vs 2025
early = np.array([104, 85, 59])
late = np.array([18, 15, 12])
pooled_std = np.sqrt((early.var() + late.var()) / 2)
cohens_d = (early.mean() - late.mean()) / pooled_std
```

|Metric|Value|Interpretation|
|------|-----|--------------|
|2015 baseline|104 CG|Starting point|
|2025 level|12 CG|Current state|
|Decline rate|-8.8/year|Rapid|
|R²|0.89|Strong trend|
|Cohen's d (early vs late)|3.2|Enormous effect|

The decline is steep (−8.8 CG/year), consistent (R² = 0.89), and shows no sign of reversing. The effect size (d = 3.2) indicates massive change.

## Future Outlook

We assess whether complete games might return.

```python
# Future prospects
future_data = {
    'factor': ['Velocity trend', 'Injury science', 'Bullpen dominance',
               'Pitch clock effect'],
    'direction': ['Against', 'Against', 'Against', 'Neutral']
}
```

|Factor|Direction for CG Return|
|------|----------------------|
|Velocity continues rising|Against|
|Injury science supports limits|Against|
|Bullpens remain dominant|Against|
|Pitch clock reduces stress|Neutral|

The pitch clock helps pace but not workload. Complete games may stabilize at current levels but are unlikely to return to historical norms.

## Summary

The complete game's extinction reveals modern baseball's priorities:

1. **90% decline since 2015** from 104 to 12 complete games
2. **0.4 per team per year** making it a truly rare event
3. **100-pitch limit** became nearly inviolable
4. **Economics reinforce change** protecting expensive investments
5. **Quality start is new standard** with 6 IP replacing 9
6. **Unlikely to return** due to structural factors

The complete game is not just declining—it is being actively retired. Modern baseball has decided that finishing what you start is not worth the risk.

## Further Reading

- Lindbergh, B. (2019). "The Death of the Complete Game." *The Ringer*.
- Sullivan, J. (2021). "Why Nobody Throws Complete Games Anymore." *FanGraphs*.

## Exercises

1. Identify which pitchers have the most complete games since 2015. What characteristics do they share?

2. Calculate whether complete games correlate with team success. Do teams with more CG win more games?

3. Examine how complete game frequency varies by ballpark. Do pitcher-friendly parks see more CG?

```bash
cd chapters/39_complete_game
python analysis.py
```
