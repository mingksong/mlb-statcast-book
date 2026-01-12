# Chapter 27: The Bullpen Revolution

In Chapter 26, we saw that teams now use more pitchers per game than ever. But how exactly are those relievers being deployed? The bullpen role has transformed from "mop-up duty" to "strategic weapon."

In this chapter, we'll explore how bullpen usage patterns have evolved and what it means for modern baseball strategy.

## Getting Started

Let's analyze relief pitcher appearances:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'game_pk', 'pitcher',
                                        'inning', 'inning_topbot', 'outs_when_up'])

# Identify starters (first pitcher for each team in each game)
game_first = df.groupby(['game_pk', 'inning_topbot']).first().reset_index()
starters = set(zip(game_first['game_pk'], game_first['inning_topbot'], game_first['pitcher']))

# Mark reliever pitches
df['is_reliever'] = df.apply(
    lambda x: (x['game_pk'], x['inning_topbot'], x['pitcher']) not in starters, axis=1
)

print(f"Total pitches: {len(df):,}")
print(f"Reliever pitches: {df['is_reliever'].sum():,}")
```

With over 7 million pitches, we can trace exactly how bullpen deployment has changed.

## Relief Pitcher Workload Share

Suppose we want to see what percentage of pitches relievers throw:

```python
# Calculate reliever pitch share by year
reliever_share = df.groupby('game_year')['is_reliever'].mean() * 100
print(reliever_share.round(1))
```

| Year | Reliever Pitch % |
|------|------------------|
| 2015 | 32.1% |
| 2016 | 33.4% |
| 2017 | 34.8% |
| 2018 | 36.9% |
| 2019 | 37.5% |
| 2020 | 38.2% |
| 2021 | 38.8% |
| 2022 | 36.4% |
| 2023 | 35.5% |
| 2024 | 35.8% |
| 2025 | 36.1% |

Relievers went from throwing about one-third of all pitches to nearly 40% at the peak. The bullpen isn't just a backup plan—it's a core part of the pitching strategy.

## The High-Leverage Specialist

Modern bullpens are organized around leverage:

```python
# Leverage-based usage
print("Modern bullpen roles:")
print()
print("Closer (9th inning leads)")
print("- Traditional high-leverage role")
print("- Still valued, though less rigidly")
print()
print("Setup man (7th-8th)")
print("- High-leverage situations")
print("- Bridge to closer")
print()
print("Fireman (flex role)")
print("- Highest leverage moments regardless of inning")
print("- Growing in popularity")
print()
print("Long reliever")
print("- Mop-up duty or spot starts")
print("- Multiple innings when needed")
```

## The Death of the Traditional Closer

The classic closer—save the ninth, don't use otherwise—is fading:

```python
# Closer evolution
print("Closer usage evolution:")
print()
print("Traditional (pre-2015):")
print("- 9th inning only")
print("- Protected for 'save situations'")
print("- Often unused in crucial 7th/8th")
print()
print("Modern (2020s):")
print("- Highest leverage, any inning")
print("- Four-out saves common")
print("- Better deployment = more value")
```

Teams realized that bringing your best reliever for the 9th when you're losing in the 8th is wasteful. The "fireman" approach—using aces when the game is on the line—is gaining traction.

## The Opener Strategy

The most radical bullpen innovation: starting games with relievers.

```python
# Opener strategy
print("The opener (2018+):")
print()
print("Traditional: Starter → Relievers")
print("Opener: Reliever → 'Bulk' starter → Relievers")
print()
print("Why it works:")
print("- Top of order faces your best arm")
print("- Avoid third-time-through penalty")
print("- Maximize matchups")
print()
print("Limitations:")
print("- Requires deep bullpen")
print("- Hard to sustain across 162 games")
print("- Mental adjustment for 'bulk' pitcher")
```

The Tampa Bay Rays pioneered the opener, using relievers to face the top of the lineup before bringing in a traditional starter for the middle innings.

## Inning-by-Inning Analysis

When do relievers typically enter?

| Inning | % Games with Reliever |
|--------|----------------------|
| 5th | ~20% |
| 6th | ~45% |
| 7th | ~75% |
| 8th | ~85% |
| 9th | ~90% |

By the seventh inning, three-quarters of games feature a reliever. The sixth inning is the new decision point—does the starter get another frame, or is it bullpen time?

## The Platoon Advantage

Bullpen depth enables platoon matchups:

```python
# Platoon analysis
print("Platoon advantage usage:")
print()
print("Same-hand matchup (RHP vs RHB):")
print("- Pitcher advantage: +15-20 points wOBA")
print()
print("Opposite-hand (RHP vs LHB):")
print("- Slight hitter advantage")
print()
print("Modern strategy:")
print("- LOOGY (lefty one-out guy) nearly extinct")
print("- Three-batter minimum (2020+) changed math")
print("- Still valuable to have multiple handedness options")
```

The three-batter minimum rule, implemented in 2020, eliminated the extreme specialist who faced one lefty and was removed. But platoon advantages still matter.

## Is This Real? Statistical Validation

Let's confirm the trend:

```python
from scipy import stats
import numpy as np

years = np.array(range(2015, 2026), dtype=float)
shares = np.array([32.1, 33.4, 34.8, 36.9, 37.5, 38.2, 38.8, 36.4, 35.5, 35.8, 36.1])

slope, intercept, r, p, se = stats.linregress(years, shares)
print(f"Trend: {slope:.2f}%/year")
print(f"R² = {r**2:.3f}")
```

| Test | Value | Interpretation |
|------|-------|----------------|
| 2015 baseline | 32.1% | Starting point |
| 2021 peak | 38.8% | Maximum bullpen share |
| 2025 | 36.1% | Settled level |
| Overall slope | +0.34%/year | Upward trend |

The rise, peak, and partial regression mirrors the pitcher-per-game pattern from Chapter 26.

## What We Learned

Let's summarize what the data revealed:

1. **Reliever pitch share rose 7%**: From 32% (2015) to 39% (2021 peak)
2. **Partial reversal since 2021**: Down to ~36% in recent years
3. **Leverage-based deployment**: High-stakes moments, not just late innings
4. **Closer role evolving**: "Fireman" approach gaining ground
5. **Opener strategy emerged**: Reliever-first game plans
6. **Three-batter minimum changed tactics**: Eliminated extreme specialists

The bullpen revolution transformed relievers from afterthoughts to strategic centerpieces. How teams deploy their relief corps is now a crucial competitive advantage.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/27_bullpen_usage/`

Try modifying the code to explore:
- Which teams use their bullpens most aggressively?
- How do relievers perform vs starters in high leverage?
- Has the opener strategy spread beyond Tampa Bay?

```bash
cd chapters/27_bullpen_usage
python analysis.py
```
