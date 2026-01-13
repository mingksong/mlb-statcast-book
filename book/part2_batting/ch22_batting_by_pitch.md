# Chapter 22: Batting Against the Arsenal

Batting performance varies dramatically by pitch type. Sinkers produce the highest wOBA against (.363), while splitters produce the lowest (.266)—a 97-point gap that represents the difference between a league-average hitter and an elite one. Fastballs generate the hardest contact (90+ mph exit velocity), while breaking balls suppress exit velocity by 4-5 mph. This chapter examines how hitters perform against different pitch types and why pitch selection remains the pitcher's primary weapon.

## Getting the Data

We begin by loading outcome data categorized by pitch type.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['pitch_type', 'woba_value', 'woba_denom',
                                     'launch_speed', 'events'])

    # Filter to plate appearances with outcomes
    pa_data = df[(df['woba_denom'] > 0) & (df['pitch_type'].notna())].copy()

    # Calculate by pitch type
    for pitch in ['FF', 'SI', 'FC', 'CH', 'SL', 'CU', 'KC', 'ST', 'FS']:
        pitch_data = pa_data[pa_data['pitch_type'] == pitch]
        if len(pitch_data) > 100:
            woba = pitch_data['woba_value'].sum() / pitch_data['woba_denom'].sum()

            # Calculate average exit velocity on contact
            batted = pitch_data[pitch_data['launch_speed'].notna()]
            avg_ev = batted['launch_speed'].mean() if len(batted) > 0 else np.nan

            results.append({
                'year': year,
                'pitch_type': pitch,
                'woba': woba,
                'avg_ev': avg_ev,
                'n_events': len(pitch_data),
            })

pitch_df = pd.DataFrame(results)
```

The dataset contains nearly 2 million plate appearances categorized by pitch type.

## wOBA by Pitch Type

We calculate average wOBA for each pitch type.

```python
pitch_woba = pitch_df.groupby('pitch_type').agg({
    'woba': 'mean',
    'avg_ev': 'mean',
    'n_events': 'sum'
}).sort_values('woba', ascending=False)
```

|Pitch Type|wOBA|Avg EV|Category|
|----------|-----|------|--------|
|Sinker (SI)|.363|89.2 mph|Fastball|
|4-Seam (FF)|.355|90.3 mph|Fastball|
|Cutter (FC)|.335|87.3 mph|Fastball|
|Changeup (CH)|.302|85.9 mph|Offspeed|
|Slider (SL)|.287|86.8 mph|Breaking|
|Curveball (CU)|.282|86.8 mph|Breaking|
|Knuckle Curve (KC)|.273|88.0 mph|Breaking|
|Sweeper (ST)|.273|85.3 mph|Breaking|
|Splitter (FS)|.266|86.6 mph|Offspeed|

The hierarchy is clear: fastballs are most hittable, breaking balls are toughest, with offspeed pitches in between.

## Visualizing Pitch Hittability

We plot wOBA by pitch type in Figure 22.1.

```python
import matplotlib.pyplot as plt

# Group by pitch category
fastballs = ['SI', 'FF', 'FC']
breaking = ['SL', 'CU', 'KC', 'ST']
offspeed = ['CH', 'FS']

avg_woba = pitch_df.groupby('pitch_type')['woba'].mean()

fig, ax = plt.subplots(figsize=(10, 6))

colors = {'SI': '#1f77b4', 'FF': '#1f77b4', 'FC': '#1f77b4',
          'SL': '#ff7f0e', 'CU': '#ff7f0e', 'KC': '#ff7f0e', 'ST': '#ff7f0e',
          'CH': '#2ca02c', 'FS': '#2ca02c'}

pitch_order = ['SI', 'FF', 'FC', 'CH', 'SL', 'CU', 'KC', 'ST', 'FS']
woba_values = [avg_woba[p] for p in pitch_order if p in avg_woba]

ax.bar(range(len(pitch_order)), woba_values,
       color=[colors.get(p, 'gray') for p in pitch_order])

ax.set_xticks(range(len(pitch_order)))
ax.set_xticklabels(pitch_order)
ax.axhline(y=0.320, color='red', linestyle='--', label='League avg wOBA')
ax.set_xlabel('Pitch Type', fontsize=12)
ax.set_ylabel('wOBA Against', fontsize=12)
ax.set_title('Batting Performance by Pitch Type', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig('figures/fig01_woba_by_pitch.png', dpi=150)
```

![Fastballs (blue) produce highest wOBA, breaking balls (orange) lowest, offspeed (green) in between](../../chapters/22_batting_by_pitch/figures/fig01_woba_by_pitch.png)

The pattern is unmistakable: fastballs in blue cluster at the top, breaking balls in orange at the bottom, with offspeed pitches in between.

## Fastball Hittability

We examine why fastballs are the most productive pitches for hitters.

```python
# Fastball category analysis
fb_data = pitch_df[pitch_df['pitch_type'].isin(['FF', 'SI', 'FC'])]
fb_woba = fb_data['woba'].mean()
fb_ev = fb_data['avg_ev'].mean()
```

|Metric|Value|
|------|-----|
|Fastball category wOBA|.351|
|Fastball avg exit velocity|88.9 mph|

Fastballs produce higher wOBA (.345-.365) because:

1. **Predictable velocity**: Hitters know roughly when to swing
2. **Less movement**: Straighter paths are easier to track
3. **Higher exit velocity**: Ball coming in faster means ball goes out faster
4. **Count leverage**: Often thrown when hitter is ahead

## The Sinker Paradox

We examine why the sinker (.363 wOBA) is the most hittable pitch despite its intended purpose.

```python
# Sinker vs 4-Seam comparison
sinker = pitch_df[pitch_df['pitch_type'] == 'SI']
four_seam = pitch_df[pitch_df['pitch_type'] == 'FF']

sinker_woba = sinker['woba'].mean()
four_seam_woba = four_seam['woba'].mean()
```

|Pitch|wOBA|Intended Outcome|
|-----|-----|----------------|
|Sinker|.363|Weak ground balls|
|4-Seam|.355|Swings and misses|

The sinker paradox has several explanations:

1. **Sinkers are often belt-high**: The movement profile puts them in hittable zones
2. **Selection effects**: Sinkers thrown when pitcher needs a strike
3. **Grounders find holes**: Even weak ground balls sometimes become hits
4. **Exit velocity remains high**: Hard grounders still produce base hits

## Splitter Dominance

We examine why the splitter (.266 wOBA) is the hardest pitch to hit.

```python
# Splitter analysis
splitter = pitch_df[pitch_df['pitch_type'] == 'FS']
splitter_woba = splitter['woba'].mean()
splitter_ev = splitter['avg_ev'].mean()
```

|Metric|Value|
|------|-----|
|Splitter wOBA|.266|
|Splitter avg EV|86.6 mph|

The splitter dominates because:

1. **Deception**: Looks like fastball, drops at last moment
2. **Chase rate**: Generates swings out of zone
3. **Weak contact**: Even when hit, contact is often poor
4. **Late movement**: Hardest to adjust to

## Exit Velocity by Pitch Type

We examine how contact quality varies by pitch.

```python
ev_by_pitch = pitch_df.groupby('pitch_type')['avg_ev'].mean().sort_values(ascending=False)
```

|Pitch|Avg Exit Velocity|
|-----|-----------------|
|4-Seam (FF)|90.3 mph|
|Sinker (SI)|89.2 mph|
|Knuckle Curve (KC)|88.0 mph|
|Cutter (FC)|87.3 mph|
|Slider (SL)|86.8 mph|
|Curveball (CU)|86.8 mph|
|Splitter (FS)|86.6 mph|
|Changeup (CH)|85.9 mph|
|Sweeper (ST)|85.3 mph|

Fastballs generate the hardest contact (90+ mph). Offspeed and breaking balls produce weaker contact (85-87 mph). This 4-5 mph gap translates to significant outcome differences.

## Category Analysis

We aggregate pitch types into fastball, breaking, and offspeed categories.

```python
# Category wOBA
def category_woba(pitches, df):
    cat_data = df[df['pitch_type'].isin(pitches)]
    return cat_data['woba'].mean()

fb_woba = category_woba(['FF', 'SI', 'FC'], pitch_df)
brk_woba = category_woba(['SL', 'CU', 'ST', 'KC'], pitch_df)
off_woba = category_woba(['CH', 'FS'], pitch_df)
```

|Category|wOBA|Gap from Average|
|--------|-----|----------------|
|Fastball|.351|+.031|
|Breaking|.279|-.041|
|Offspeed|.284|-.036|

The 72-point gap between fastballs (.351) and breaking balls (.279) explains why the breaking ball revolution (Chapter 3) has been so impactful.

## Statistical Validation

We test the stability of pitch effectiveness rankings.

```python
# Test stability by comparing early vs late periods
early = pitch_df[pitch_df['year'].isin([2015, 2016, 2017, 2018])]
late = pitch_df[pitch_df['year'].isin([2022, 2023, 2024, 2025])]

for pitch in ['FF', 'SI', 'SL', 'FS']:
    early_woba = early[early['pitch_type'] == pitch]['woba'].mean()
    late_woba = late[late['pitch_type'] == pitch]['woba'].mean()
```

|Pitch|2015-2018|2022-2025|Change|
|-----|---------|---------|------|
|4-Seam|.358|.352|-.006|
|Sinker|.368|.359|-.009|
|Slider|.292|.281|-.011|
|Splitter|.275|.260|-.015|

The rankings have remained stable, though all pitches have become slightly less hittable as velocity and movement have increased.

## Strategic Implications

We outline the connection between pitch effectiveness and sequencing strategy.

```python
# Sequencing logic
sequence_strategy = {
    'establish_fastball': 'Get hitter timing fastball',
    'change_plane': 'Use breaking ball off fastball look',
    'put_away': 'Splitter/changeup for strikeout'
}
```

The pitch effectiveness hierarchy explains pitching strategy:
- **Start with fastball**: Establish timing that hitter must respect
- **Use breaking ball off fastball**: Change plane to disrupt timing
- **Splitter/changeup to put away**: Late movement for swing-and-miss

This connects to Chapter 12 (Pitch Effectiveness): pitch effectiveness is the mirror of batting effectiveness.

## Summary

Batting performance by pitch type reveals predictable patterns:

1. **Sinker most hittable**: .363 wOBA despite "pitch to contact" intent
2. **Splitter hardest to hit**: .266 wOBA, best put-away pitch
3. **Fastballs produce highest EV**: 90+ mph exit velocity
4. **Breaking balls cluster**: All in .273-.287 wOBA range
5. **4-5 mph EV gap**: Between fastball and offspeed contact
6. **Rankings are stable**: Patterns consistent over time

The batting-by-pitch analysis shows that hitting is fundamentally reactive. Hitters must respond to what pitchers throw, and some pitches simply give hitters less chance to succeed. This asymmetry drives the entire cat-and-mouse game of baseball.

## Further Reading

- Sullivan, J. (2018). "The Hittability Hierarchy." *FanGraphs*.
- Nathan, A. M. (2019). "Physics of Pitch Effectiveness." *Baseball Prospectus*.

## Exercises

1. Calculate how wOBA against the splitter has changed as usage has increased. Is the splitter becoming more or less effective?

2. Identify hitters who excel against breaking balls. What characteristics do they share (approach, swing mechanics)?

3. Examine whether pitch hittability varies by count. Do breaking balls become less effective in hitter's counts?

```bash
cd chapters/22_batting_by_pitch
python analysis.py
```
