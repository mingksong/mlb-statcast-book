# Chapter 20: The Count Advantage

Every plate appearance is a battle of counts. Get ahead early, and the batter gains an enormous advantage. Fall behind, and the pitcher takes control. This fundamental truth hasn't changed in a century—but now we can quantify exactly how much each count matters.

In this chapter, we'll explore how batting success varies by count and discover why getting ahead is more important than ever.

## Getting Started

Let's begin by loading plate appearance data with count information:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'balls', 'strikes',
                                        'woba_value', 'woba_denom', 'events'])

# Create count column
df['count'] = df['balls'].astype(str) + '-' + df['strikes'].astype(str)

# Filter to plate appearances with outcomes
pa_data = df[df['woba_denom'] > 0]
print(f"Plate appearances analyzed: {len(pa_data):,}")
```

With over 1.9 million plate appearances, we can measure exactly how batting performance varies across all 12 standard counts.

## The wOBA Hierarchy

Suppose we want to see how effective hitters are in each count:

```python
# Calculate wOBA by count
count_woba = pa_data.groupby('count').apply(
    lambda x: x['woba_value'].sum() / x['woba_denom'].sum()
)
count_woba = count_woba.sort_values(ascending=False)
print(count_woba.round(3))
```

| Count | wOBA | Events | Advantage |
|-------|------|--------|-----------|
| 3-0 | .777 | 28,697 | Extreme hitter |
| 3-1 | .583 | 81,446 | Strong hitter |
| 2-0 | .435 | 42,557 | Hitter |
| 0-0 | .417 | 205,576 | Neutral |
| 1-0 | .415 | 116,414 | Neutral |
| 2-1 | .406 | 87,558 | Slight hitter |
| 1-1 | .393 | 150,560 | Neutral |
| 3-2 | .386 | 262,183 | Neutral |
| 0-1 | .378 | 164,287 | Slight pitcher |
| 2-2 | .208 | 272,802 | Pitcher |
| 1-2 | .189 | 287,688 | Strong pitcher |
| 0-2 | .177 | 177,268 | Extreme pitcher |

![wOBA by Count](../../chapters/20_count_batting/figures/fig01_woba_by_count.png)

The hierarchy is dramatic. At 3-0, hitters produce a .777 wOBA—equivalent to an all-time great season. At 0-2, they manage just .177 wOBA—worse than most pitchers batting.

## The 3-0 Kingdom

Let's examine the extreme case:

```python
# 3-0 analysis
count_30 = pa_data[pa_data['count'] == '3-0']
woba_30 = count_30['woba_value'].sum() / count_30['woba_denom'].sum()

print(f"3-0 count wOBA: {woba_30:.3f}")
print(f"Events at 3-0: {len(count_30):,}")
print(f"For context: League avg wOBA is ~.320")
```

A .777 wOBA at 3-0 is off the charts. Why?

1. **Pitcher must throw a strike**: Walking is nearly guaranteed otherwise
2. **Hitter knows what's coming**: Fastball over the plate
3. **Hitter can sit on a pitch**: No need to protect the zone
4. **High-leverage swings**: Hitters often let 3-0 pass, but when they swing, they're ready

## The 0-2 Nightmare

The opposite extreme tells an equally clear story:

```python
# 0-2 analysis
count_02 = pa_data[pa_data['count'] == '0-2']
woba_02 = count_02['woba_value'].sum() / count_02['woba_denom'].sum()

print(f"0-2 count wOBA: {woba_02:.3f}")
print(f"Events at 0-2: {len(count_02):,}")
```

A .177 wOBA at 0-2 represents complete pitcher dominance:

1. **Pitcher can waste pitches**: Chase zone becomes effective
2. **Hitter must protect**: Any strike could be strike three
3. **Defensive swings**: Contact more important than damage
4. **Breaking balls dominate**: 0-2 is prime slider/curveball territory

## The Gap: Hitter's vs Pitcher's Counts

Let's quantify the advantage more broadly:

```python
# Define count types
hitter_counts = ['3-0', '3-1', '2-0', '1-0', '2-1']
pitcher_counts = ['0-2', '1-2', '2-2', '0-1']
neutral_counts = ['0-0', '1-1', '3-2']

def calculate_woba(counts):
    filtered = pa_data[pa_data['count'].isin(counts)]
    return filtered['woba_value'].sum() / filtered['woba_denom'].sum()

print(f"Hitter's counts wOBA: {calculate_woba(hitter_counts):.3f}")
print(f"Neutral counts wOBA: {calculate_woba(neutral_counts):.3f}")
print(f"Pitcher's counts wOBA: {calculate_woba(pitcher_counts):.3f}")
```

| Count Type | wOBA | Gap from Average |
|------------|------|------------------|
| Hitter's counts | .448 | +.128 |
| Neutral counts | .394 | +.074 |
| Pitcher's counts | .235 | -.085 |

The difference between hitter's counts (.448) and pitcher's counts (.235) is 213 points of wOBA—nearly the difference between an MVP and a replacement-level player.

## Why Count Matters So Much

The count fundamentally changes the strategic environment:

```python
# The count effect
print("In hitter's counts:")
print("- Pitcher throws more strikes")
print("- Fastball frequency increases")
print("- Pitch location more predictable")
print("- Hitter can be selective")
print()
print("In pitcher's counts:")
print("- Pitcher can waste pitches")
print("- Breaking ball frequency increases")
print("- Chase zone becomes effective")
print("- Hitter must protect")
```

The count doesn't just affect outcomes—it changes which pitches are thrown, where they're thrown, and how aggressively hitters can swing.

## The Full Count Special Case

The 3-2 count is unique—full pressure on both sides:

```python
# Full count analysis
count_32 = pa_data[pa_data['count'] == '3-2']
woba_32 = count_32['woba_value'].sum() / count_32['woba_denom'].sum()

print(f"Full count wOBA: {woba_32:.3f}")
print(f"Full count events: {len(count_32):,}")
```

At .386 wOBA, the full count is nearly neutral—slightly favoring hitters but not dramatically. Both player types are under maximum pressure, creating a balanced situation.

## First Pitch Importance

Given these gaps, the first pitch becomes crucial:

```python
# First pitch outcomes
first_pitch = pa_data[pa_data['count'] == '0-0']
woba_00 = first_pitch['woba_value'].sum() / first_pitch['woba_denom'].sum()

# What happens after 0-1 vs 1-0?
after_01 = pa_data[pa_data['count'] == '0-1']
after_10 = pa_data[pa_data['count'] == '1-0']

print(f"After 0-0 ends: .417 wOBA")
print(f"If pitcher gets ahead (0-1): .378 wOBA")
print(f"If hitter gets ahead (1-0): .415 wOBA")
```

This connects to Chapter 10 (First Pitch Strategy)—the first pitch sets the trajectory for the entire plate appearance.

## Is This Stable? Historical Comparison

Let's check if the count advantage has changed over time:

```python
# Early vs late comparison
early = pa_data[pa_data['game_year'].isin([2015, 2016, 2017, 2018])]
late = pa_data[pa_data['game_year'].isin([2022, 2023, 2024, 2025])]

for count in ['3-0', '0-0', '0-2']:
    early_woba = early[early['count'] == count]['woba_value'].sum() / \
                 early[early['count'] == count]['woba_denom'].sum()
    late_woba = late[late['count'] == count]['woba_value'].sum() / \
                late[late['count'] == count]['woba_denom'].sum()
    print(f"{count}: {early_woba:.3f} → {late_woba:.3f}")
```

| Count | 2015-2018 | 2022-2025 | Change |
|-------|-----------|-----------|--------|
| 3-0 | .780 | .772 | -.008 |
| 0-0 | .420 | .415 | -.005 |
| 0-2 | .180 | .175 | -.005 |

The count hierarchy has remained remarkably stable. The gap between hitter's counts and pitcher's counts is a fundamental feature of baseball, not something that changes with trends.

## Strategic Implications

What does this mean for the game?

```python
# Strategic implications
print("For hitters:")
print("- Get ahead: wOBA jumps 100+ points")
print("- Avoid 0-2: Most dangerous count")
print("- Patience pays: Working the count creates opportunities")
print()
print("For pitchers:")
print("- First strike is critical")
print("- 0-2 is the goal: Expand zone confidently")
print("- Avoid 3-0: Near-guaranteed damage if attacked")
```

## What We Learned

Let's summarize what the data revealed:

1. **3-0 is dominant**: .777 wOBA, equivalent to best-ever season
2. **0-2 is crushing**: .177 wOBA, worse than most pitchers batting
3. **The gap is 213 points**: Hitter's counts (.448) vs pitcher's (.235)
4. **Full count is neutral**: .386 wOBA balances pressure
5. **First pitch matters**: Sets trajectory for entire PA
6. **Stable over time**: Count advantage is fundamental

The count story reminds us that baseball isn't just about raw talent—it's about strategic positioning. Every ball and strike changes the probabilities dramatically, making count management one of the game's most important skills.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/20_count_batting/`

Try modifying the code to explore:
- How does count affect pitch type selection?
- Which players are best at avoiding pitcher's counts?
- Does count matter more for power hitters or contact hitters?

```bash
cd chapters/20_count_batting
python analysis.py
```
