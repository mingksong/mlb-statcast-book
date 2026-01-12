# Chapter 24: The Clutch Hitting Myth

Some players are "clutch." They rise to the occasion when it matters most. They thrive with runners in scoring position. They get the big hit in the ninth inning. Everyone knows these players exist—the announcers tell us constantly.

But do they? Is clutch hitting a skill, or is it just memorable randomness? In this chapter, we'll use Statcast data to examine whether clutch performance is real or illusory.

## Getting Started

Let's begin by defining and measuring clutch situations:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'woba_value', 'woba_denom',
                                        'on_1b', 'on_2b', 'on_3b', 'outs_when_up'])

# Filter to plate appearances with outcomes
pa_data = df[df['woba_denom'] > 0]

# Define situations
pa_data['risp'] = (pa_data['on_2b'].notna()) | (pa_data['on_3b'].notna())
pa_data['two_out'] = pa_data['outs_when_up'] == 2
pa_data['clutch'] = pa_data['risp'] & pa_data['two_out']

print(f"Plate appearances: {len(pa_data):,}")
```

With over 2.3 million plate appearances categorized by situation, we can measure whether hitters perform differently when it "matters."

## Performance by Situation

Suppose we want to see if hitters perform better with runners in scoring position:

```python
# Calculate wOBA by situation
situations = {
    'Bases Empty': pa_data[~pa_data['risp'] & ~pa_data['on_1b'].notna()],
    'RISP': pa_data[pa_data['risp']],
    'Two Outs': pa_data[pa_data['two_out']],
    'Clutch (RISP + 2 out)': pa_data[pa_data['clutch']]
}

for name, data in situations.items():
    woba = data['woba_value'].sum() / data['woba_denom'].sum()
    print(f"{name}: {woba:.3f} (n={len(data):,})")
```

| Situation | wOBA | Sample Size |
|-----------|------|-------------|
| Bases Empty | .321 | 1,073,935 |
| RISP | .334 | 460,775 |
| Two Outs | .319 | 605,522 |
| Clutch (RISP + 2 out) | .322 | 212,275 |

![Clutch wOBA](../../chapters/24_clutch_hitting/figures/fig01_clutch_woba.png)

Wait—wOBA is *higher* with RISP (.334) than with bases empty (.321)? That seems backward.

## Why RISP Performance Is Higher

The RISP advantage isn't clutch hitting—it's selection bias:

```python
# Selection bias explanation
print("Why RISP wOBA is higher:")
print()
print("1. Intentional walks")
print("   - With first base open, dangerous hitters get walked")
print("   - Walk = .69 wOBA value")
print()
print("2. Pitcher strategy")
print("   - More pitches in zone to avoid walks")
print("   - Better pitches to hit")
print()
print("3. Defensive positioning")
print("   - Infielders play for double play")
print("   - More holes in the defense")
```

The hitters aren't better—the situation is easier. Pitchers give up more contact to avoid walks. Defenses sacrifice range for double play positioning.

## The True Clutch Test

If we want to test clutch hitting, we need to compare the same hitters in different situations. Do good hitters elevate more in clutch spots?

```python
# Conceptual approach
print("To test clutch hitting properly:")
print()
print("1. Calculate each hitter's baseline wOBA (non-clutch)")
print("2. Calculate each hitter's clutch wOBA")
print("3. Compare: Do better hitters have bigger clutch bumps?")
print()
print("Research finding: No correlation")
print("Clutch performance doesn't predict future clutch performance")
```

Decades of research have found no evidence that clutch hitting is a repeatable skill. Players who performed well in clutch situations one year didn't do so the next.

## The Small Sample Problem

Clutch situations are inherently rare:

```python
# Sample size problem
total_pa = len(pa_data)
clutch_pa = pa_data['clutch'].sum()

print(f"Total PAs: {total_pa:,}")
print(f"Clutch PAs: {clutch_pa:,}")
print(f"Clutch %: {clutch_pa/total_pa*100:.1f}%")
```

Only about 10% of plate appearances are "clutch" (RISP with 2 outs). For any individual player, that's maybe 50-60 PAs per season—far too few to distinguish skill from luck.

## The Memory Bias

Why does clutch hitting *feel* real?

```python
# Why we believe in clutch
print("Memory and narrative:")
print()
print("1. High-leverage moments are memorable")
print("   - We remember walk-off hits vividly")
print("   - We forget the routine groundout in the 3rd")
print()
print("2. Confirmation bias")
print("   - 'Clutch' players' successes confirm our belief")
print("   - Their failures are explained away")
print()
print("3. Narrative is powerful")
print("   - Sports storytelling needs heroes")
print("   - 'Mr. October' is better TV than 'random variation'")
```

## What About Pressure?

Doesn't pressure affect performance? It does—but not consistently:

```python
# Pressure effects
print("Pressure research:")
print()
print("Some players choke under pressure")
print("Some players rise to the occasion")
print("These tendencies are:")
print("  - Small in magnitude")
print("  - Inconsistent year-to-year")
print("  - Unpredictable beforehand")
print()
print("Net effect across MLB: Near zero")
```

Individual players may respond differently to pressure, but these effects wash out across the league. And they don't predict who will be clutch next year.

## Is This Real? Statistical Validation

Let's confirm the situational differences aren't meaningful:

```python
from scipy import stats
import numpy as np

# Compare situations using effect size
bases_empty = pa_data[~pa_data['risp'] & ~pa_data['on_1b'].notna()]
clutch = pa_data[pa_data['clutch']]

be_woba = bases_empty['woba_value'].sum() / bases_empty['woba_denom'].sum()
cl_woba = clutch['woba_value'].sum() / clutch['woba_denom'].sum()

print(f"Bases empty wOBA: {be_woba:.3f}")
print(f"Clutch wOBA: {cl_woba:.3f}")
print(f"Difference: {(cl_woba - be_woba)*1000:.1f} points")
```

| Comparison | wOBA Gap | Interpretation |
|------------|----------|----------------|
| RISP vs Empty | +13 points | Selection effect, not skill |
| Clutch vs Empty | +1 point | Essentially identical |
| Two Outs vs All | -2 points | Slightly harder |

The differences are tiny and explainable by context, not hitter skill.

## The Practical Implication

If clutch hitting isn't real, what matters?

```python
# What actually matters
print("For team building:")
print()
print("DON'T pay for 'clutch':")
print("- Past clutch performance doesn't predict future")
print("- Small samples are unreliable")
print()
print("DO pay for:")
print("- Overall ability (full-season stats)")
print("- Contact skills")
print("- Power")
print("- Plate discipline")
print()
print("Good hitters are 'clutch' by being good all the time")
```

## What We Learned

Let's summarize what the data revealed:

1. **RISP wOBA is higher (.334)**: But due to selection effects, not skill
2. **Clutch wOBA matches baseline**: .322 vs .321 for bases empty
3. **Differences are tiny**: 1-13 points, not meaningful
4. **Research is clear**: Clutch hitting doesn't predict future clutch hitting
5. **Small samples dominate**: Only ~10% of PAs are "clutch"
6. **Memory bias is real**: We remember what confirms our beliefs

The clutch hitting myth persists because humans are storytellers. We see patterns in randomness and heroes in lucky hits. But the data is clear: clutch hitting is mostly narrative, not skill.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/24_clutch_hitting/`

Try modifying the code to explore:
- Which players have the biggest RISP splits?
- Do those splits persist year-to-year?
- How does wOBA vary by inning in close games?

```bash
cd chapters/24_clutch_hitting
python analysis.py
```
