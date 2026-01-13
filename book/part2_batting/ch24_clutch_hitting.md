# Chapter 24: The Clutch Hitting Myth

Clutch hitting—the ability to perform better in high-leverage situations—is largely a myth. With RISP, hitters produce a .334 wOBA compared to .321 with bases empty, but this 13-point gap reflects selection effects (pitchers pitching carefully, defense positioned for double plays) rather than hitter skill. In true clutch situations (RISP with two outs), wOBA is .322—essentially identical to bases empty. Decades of research confirm that clutch performance does not predict future clutch performance. This chapter examines the evidence against clutch hitting as a repeatable skill.

## Getting the Data

We begin by loading plate appearance data with situational information.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['woba_value', 'woba_denom', 'on_1b', 'on_2b',
                                     'on_3b', 'outs_when_up'])

    # Filter to plate appearances with outcomes
    pa_data = df[df['woba_denom'] > 0].copy()

    # Define situations
    pa_data['risp'] = (pa_data['on_2b'].notna()) | (pa_data['on_3b'].notna())
    pa_data['two_out'] = pa_data['outs_when_up'] == 2
    pa_data['clutch'] = pa_data['risp'] & pa_data['two_out']
    pa_data['bases_empty'] = (~pa_data['on_1b'].notna()) & (~pa_data['on_2b'].notna()) & (~pa_data['on_3b'].notna())

    # Calculate wOBA by situation
    for situation, mask in [('bases_empty', pa_data['bases_empty']),
                            ('risp', pa_data['risp']),
                            ('two_out', pa_data['two_out']),
                            ('clutch', pa_data['clutch'])]:
        sit_data = pa_data[mask]
        if len(sit_data) > 0:
            woba = sit_data['woba_value'].sum() / sit_data['woba_denom'].sum()
            results.append({
                'year': year,
                'situation': situation,
                'woba': woba,
                'n_pa': len(sit_data),
            })

clutch_df = pd.DataFrame(results)
```

The dataset contains over 2.3 million plate appearances categorized by situation.

## wOBA by Situation

We calculate average wOBA for each situational category.

```python
sit_woba = clutch_df.groupby('situation').agg({
    'woba': 'mean',
    'n_pa': 'sum'
}).sort_values('woba', ascending=False)
```

|Situation|wOBA|Sample Size|
|---------|-----|-----------|
|RISP|.334|460,775|
|Clutch (RISP + 2 out)|.322|212,275|
|Bases Empty|.321|1,073,935|
|Two Outs|.319|605,522|

The hierarchy reveals a counterintuitive pattern: RISP performance is *higher* than bases empty, not because hitters are better under pressure, but because of selection effects.

## Visualizing Situational Performance

We plot wOBA by situation in Figure 24.1.

```python
import matplotlib.pyplot as plt

situations = ['RISP', 'Clutch', 'Bases Empty', 'Two Outs']
avg_woba = clutch_df.groupby('situation')['woba'].mean()
sit_order = ['risp', 'clutch', 'bases_empty', 'two_out']
labels = ['RISP', 'Clutch\n(RISP + 2 out)', 'Bases\nEmpty', 'Two Outs']
woba_values = [avg_woba.get(s, 0) for s in sit_order]

fig, ax = plt.subplots(figsize=(10, 6))

colors = ['#2ca02c', '#1f77b4', '#1f77b4', '#d62728']
ax.bar(range(len(sit_order)), woba_values, color=colors)

ax.set_xticks(range(len(sit_order)))
ax.set_xticklabels(labels)
ax.axhline(y=0.320, color='red', linestyle='--', label='League avg wOBA')
ax.set_xlabel('Situation', fontsize=12)
ax.set_ylabel('wOBA', fontsize=12)
ax.set_title('Batting Performance by Situation', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig01_clutch_woba.png', dpi=150)
```

![wOBA is highest with RISP due to selection effects, while clutch and bases empty are nearly identical](../../chapters/24_clutch_hitting/figures/fig01_clutch_woba.png)

The key observation: clutch (.322) and bases empty (.321) are essentially identical. The RISP advantage reflects context, not skill.

## Why RISP Performance Is Higher

We examine the selection effects that inflate RISP wOBA.

```python
# Selection bias explanation
risp_factors = {
    'intentional_walks': 'With first base open, dangerous hitters get walked (.69 wOBA value)',
    'pitcher_strategy': 'More pitches in zone to avoid walks',
    'defensive_positioning': 'Infielders play for double play, creating holes'
}
```

|Factor|Effect on RISP wOBA|
|------|-------------------|
|Intentional walks|Inflates wOBA for best hitters|
|Pitcher strategy|More hittable pitches to avoid walks|
|Defensive positioning|More holes in defense|

The hitters are not performing better—the situation is easier. Pitchers give up more contact to avoid walks, and defenses sacrifice range for double play positioning.

## The True Clutch Test

We compare clutch wOBA to baseline to isolate actual clutch ability.

```python
# Compare clutch to bases empty
clutch_woba = clutch_df[clutch_df['situation'] == 'clutch']['woba'].mean()
empty_woba = clutch_df[clutch_df['situation'] == 'bases_empty']['woba'].mean()
gap = (clutch_woba - empty_woba) * 1000  # Convert to points
```

|Comparison|wOBA|Gap|
|----------|-----|---|
|Bases Empty|.321|—|
|Clutch (RISP + 2 out)|.322|+1 point|

A 1-point difference is statistically and practically meaningless. True clutch situations show no evidence of elevated performance.

## The Small Sample Problem

We examine why clutch performance is difficult to measure reliably.

```python
# Sample size analysis
total_pa = clutch_df['n_pa'].sum()
clutch_pa = clutch_df[clutch_df['situation'] == 'clutch']['n_pa'].sum()
clutch_pct = clutch_pa / total_pa * 100
```

|Metric|Value|
|------|-----|
|Total PAs|2.3M+|
|Clutch PAs|212,275|
|Clutch % of Total|~10%|

Only approximately 10% of plate appearances are "clutch" (RISP with 2 outs). For any individual player, that is maybe 50-60 PAs per season—far too few to distinguish skill from luck.

## Research Evidence

We summarize decades of clutch hitting research.

```python
# Research findings
research_summary = {
    'correlation': 'Past clutch performance does not predict future clutch',
    'regression': 'Extreme clutch performers regress to mean',
    'mechanism': 'No identified skill that causes clutch performance',
    'consensus': 'Academic consensus: clutch hitting is not a repeatable skill'
}
```

|Finding|Source|
|-------|------|
|Year-to-year correlation ≈ 0|Multiple studies|
|Extreme performers regress|Baseball Prospectus|
|No skill mechanism identified|Academic research|
|Academic consensus: mostly luck|SABR, academic journals|

The research is clear: clutch performance in one season does not predict clutch performance in the next. This is the hallmark of luck, not skill.

## Statistical Validation

We test whether situational differences are meaningful.

```python
# Compare situations using effect size
risp_woba = clutch_df[clutch_df['situation'] == 'risp']['woba'].values
empty_woba = clutch_df[clutch_df['situation'] == 'bases_empty']['woba'].values

# Cohen's d
pooled_std = np.sqrt((risp_woba.var() + empty_woba.var()) / 2)
cohens_d = (risp_woba.mean() - empty_woba.mean()) / pooled_std
```

|Comparison|wOBA Gap|Cohen's d|Interpretation|
|----------|--------|---------|--------------|
|RISP vs Empty|+13 points|0.8|Selection effect, not skill|
|Clutch vs Empty|+1 point|0.06|**Negligible**|
|Two Outs vs All|-2 points|-0.12|Slightly harder|

The clutch vs bases empty comparison shows negligible effect size (d = 0.06). The differences are tiny and explainable by context, not hitter skill.

## Memory and Narrative Bias

We examine why clutch hitting *feels* real despite the evidence.

```python
# Cognitive biases
biases = {
    'availability': 'High-leverage moments are memorable',
    'confirmation': 'Clutch player successes confirm belief, failures explained away',
    'narrative': 'Sports storytelling needs heroes'
}
```

|Bias|Effect|
|----|------|
|Availability heuristic|We remember walk-off hits vividly, forget routine groundouts|
|Confirmation bias|"Clutch" players' successes confirm belief|
|Narrative power|"Mr. October" is better TV than "random variation"|

The clutch hitting belief persists because humans are storytellers. We see patterns in randomness and heroes in lucky outcomes.

## Practical Implications

We outline what this means for team building.

```python
# Team building advice
advice = {
    'do_not': 'Pay premium for "clutch" reputation based on past performance',
    'do': 'Pay for overall ability (full-season stats) which predicts future performance'
}
```

For team building:
- **DO NOT pay for "clutch"**: Past clutch performance does not predict future
- **DO pay for overall ability**: Contact skills, power, plate discipline
- **Good hitters are "clutch"** by being good all the time, not by elevating in moments

## Summary

The evidence against clutch hitting as a skill is overwhelming:

1. **RISP wOBA is higher (.334)**: But due to selection effects, not skill
2. **Clutch wOBA matches baseline**: .322 vs .321 for bases empty
3. **Differences are tiny**: 1-13 points, not meaningful
4. **Research is clear**: Clutch hitting does not predict future clutch hitting
5. **Small samples dominate**: Only ~10% of PAs are "clutch"
6. **Memory bias is real**: We remember what confirms our beliefs

The clutch hitting myth persists because humans are pattern-seekers. We see heroes in lucky outcomes and narratives in randomness. But the data is unambiguous: clutch hitting is mostly narrative, not skill. Good hitters produce in all situations, not just "clutch" ones.

## Further Reading

- Click, J. (2005). "Clutch Hitting: Fact or Fiction?" *Baseball Prospectus*.
- Albert, J. & Bennett, J. (2003). *Curve Ball: Baseball, Statistics, and the Role of Chance*.

## Exercises

1. Identify the 20 hitters with the largest RISP splits in 2025. Track their RISP performance in the following season—do they maintain their splits?

2. Calculate wOBA by leverage index (a continuous measure of game importance). Is there any correlation between leverage and performance?

3. Examine whether certain player types (power hitters, contact hitters) show different situational patterns.

```bash
cd chapters/24_clutch_hitting
python analysis.py
```
