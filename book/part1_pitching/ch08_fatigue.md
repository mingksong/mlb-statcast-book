# Chapter 8: Velocity and Spin by Inning

Do pitchers tire as games progress? You'd expect velocity to decline by the sixth or seventh inning—less zip on the fastball, lower spin rates, diminishing stuff. But when we look at the data, we find something surprising: late-inning pitches are actually thrown *harder* than early-inning pitches.

In this chapter, we'll unravel this paradox and discover what it reveals about modern bullpen strategy.

## Getting Started

Let's begin by loading our fastball data with inning information:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'pitch_type', 'release_speed',
                                        'release_spin_rate', 'inning'])

# Filter to 4-seam fastballs
ff = df[df['pitch_type'] == 'FF'].dropna(subset=['release_speed', 'inning'])
ff = ff[ff['inning'] <= 9]  # Focus on regulation innings
print(f"Total fastballs analyzed: {len(ff):,}")
```

With over 2.5 million four-seam fastballs across all nine innings, we can track exactly how pitch characteristics change as games progress.

## The Counterintuitive Pattern

Suppose we want to see how velocity changes from the first inning to the ninth. Let's calculate the average:

```python
# Calculate velocity by inning
velo_by_inning = ff.groupby('inning')['release_speed'].mean()
for inning in range(1, 10):
    print(f"Inning {inning}: {velo_by_inning[inning]:.2f} mph")
```

The results are surprising:

| Inning | Velocity | Spin Rate | Sample Size |
|--------|----------|-----------|-------------|
| 1 | 93.41 mph | 2,266 rpm | 332,153 |
| 2 | 93.23 mph | 2,266 rpm | 290,921 |
| 3 | 93.12 mph | 2,264 rpm | 272,505 |
| 4 | 93.08 mph | 2,262 rpm | 259,797 |
| 5 | 93.14 mph | 2,265 rpm | 261,072 |
| 6 | 93.54 mph | 2,276 rpm | 268,196 |
| 7 | 94.03 mph | 2,289 rpm | 283,932 |
| 8 | 94.35 mph | 2,300 rpm | 292,083 |
| 9 | **94.83 mph** | **2,317 rpm** | 232,935 |

![Velocity by Inning](../../chapters/08_fatigue/figures/fig01_velocity_by_inning.png)

Wait—velocity *increases* by 1.4 mph from the first inning to the ninth? That doesn't match our intuition about fatigue at all.

## The Bullpen Paradox

But wait—let's think about what's actually happening in each inning. Who's throwing those pitches?

```python
# Think about who's pitching in each inning
print("Inning 1-3: Mostly starters (fresh)")
print("Inning 4-5: Starters (showing some fatigue)")
print("Inning 6-7: Mix of starters and relievers")
print("Inning 8-9: Mostly relievers (fresh arms)")
```

The pattern becomes clear: this isn't about fatigue disappearing. It's about **roster composition**.

Modern baseball has evolved to a simple principle: when starters tire, bring in fresh arms that throw harder. The ninth inning isn't comparing tired starters to fresh starters—it's comparing closers to starting pitchers.

```python
# Compare early vs late innings
early = ff[ff['inning'].isin([1, 2, 3])]['release_speed'].mean()
late = ff[ff['inning'].isin([7, 8, 9])]['release_speed'].mean()
print(f"Early innings (1-3): {early:.2f} mph")
print(f"Late innings (7-9): {late:.2f} mph")
print(f"Difference: +{late - early:.2f} mph")
```

| Period | Velocity |
|--------|----------|
| Early innings (1-3) | 93.26 mph |
| Late innings (7-9) | 94.37 mph |
| **Difference** | **+1.11 mph** |

That 1.1 mph jump reflects the compositional shift from starters to relievers—not any change in individual pitcher performance.

## Does Starter Fatigue Still Exist?

This raises a question: do individual starters still show fatigue, or has modern pitcher management eliminated it?

```python
# Track velocity from inning 1 to 6 (when most starters are still pitching)
for inning in [1, 3, 6]:
    velo = ff[ff['inning'] == inning]['release_speed'].mean()
    print(f"Inning {inning}: {velo:.2f} mph")
```

| Period | Inning 1 | Inning 6 | Change |
|--------|----------|----------|--------|
| 2015 | 92.76 | 92.95 | +0.19 |
| 2020 | 93.29 | 93.34 | +0.05 |
| 2025 | 94.38 | 94.36 | -0.01 |

The changes are minimal. Modern pitcher management pulls starters before significant fatigue shows in the data. This is intentional—teams monitor velocity in real-time and often remove starters at the first sign of decline.

## Spin Rate Follows the Same Pattern

Let's see if spin rate shows the same inning-by-inning increase:

```python
# Calculate spin by inning
spin_by_inning = ff.groupby('inning')['release_spin_rate'].mean()
for inning in range(1, 10):
    print(f"Inning {inning}: {spin_by_inning[inning]:.0f} rpm")
```

![Spin by Inning](../../chapters/08_fatigue/figures/fig02_spin_by_inning.png)

Spin rate increases by about 50 rpm from the first to ninth inning—the same bullpen composition effect we saw with velocity. Relievers spin the ball harder, too.

## Is This Real? Statistical Validation

Let's confirm these patterns statistically:

```python
from scipy import stats
import numpy as np

# Velocity trend across innings
innings = np.array(range(1, 10), dtype=float)
velocities = np.array([velo_by_inning[i] for i in range(1, 10)], dtype=float)

slope, intercept, r, p, se = stats.linregress(innings, velocities)
print(f"Velocity trend: +{slope:.3f} mph per inning")
print(f"R² = {r**2:.3f}, p = {p:.4f}")
```

| Test | Metric | Value | Interpretation |
|------|--------|-------|----------------|
| Velocity Trend | Slope | +0.189 mph/inning | Significant increase |
| | R² | 0.684 | Strong fit |
| | p-value | 0.006 | Very significant |
| Spin Trend | Slope | +6.1 rpm/inning | |
| | R² | 0.748 | Strong fit |
| Early vs Late | Difference | +1.11 mph | |
| | Cohen's d | 0.421 | **Small-to-medium effect** |
| | p-value | < 0.001 | Highly significant |

![Combined View](../../chapters/08_fatigue/figures/fig03_velocity_spin_combined.png)

With R² values above 0.68 and p-values well below 0.05, these trends are statistically robust. The late-inning velocity increase is real—just not caused by what you might think.

## What This Reveals About Modern Baseball

The inning-by-inning velocity pattern is a window into how the game has evolved:

1. **Bullpen specialization**: Teams now carry 13+ pitchers specifically to deploy fresh, hard-throwing arms in late innings

2. **Starter workload management**: Starters rarely face the lineup a third time, not because of fatigue rules but because performance drops

3. **High-leverage optimization**: The hardest throwers are saved for the most important situations (close games, late innings)

4. **Analytics-driven decisions**: Real-time velocity monitoring triggers pitching changes before visible decline

```python
# The modern bullpen philosophy in numbers
print("Modern game strategy:")
print("- Starters: 5-6 innings, velocity ~93 mph")
print("- Setup men: 7th-8th inning, velocity ~95 mph")
print("- Closers: 9th inning, velocity ~96+ mph")
```

## What We Learned

Let's summarize what the data revealed:

1. **Late-inning velocity is higher**: 94.8 mph in the 9th vs 93.4 mph in the 1st (+1.4 mph)
2. **The paradox is compositional**: Relievers replacing starters mask individual fatigue
3. **Spin rate follows the same pattern**: +50 rpm from inning 1 to inning 9
4. **Starter fatigue still exists**: But teams pull starters before it shows significantly
5. **Modern roster construction drives this**: The bullpen era is visible in the data

The "fatigue paradox" reveals something fundamental: baseball has evolved to never let tired pitchers throw important pitches. Fresh arms are always waiting.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/08_fatigue/`

Try modifying the code to explore:
- How does inning-by-inning velocity differ for playoff games vs regular season?
- Do starters who go deep into games show more fatigue than those who don't?
- Has the starter-to-reliever velocity gap widened over the decade?

```bash
cd chapters/08_fatigue
python analysis.py
```
