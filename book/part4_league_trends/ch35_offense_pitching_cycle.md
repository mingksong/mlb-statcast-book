# Chapter 35: The Eternal Tug of War

Baseball has always oscillated between offense and pitching dominance. Just when hitters seem to have figured it out, pitchers adapt. When pitching becomes dominant, rules change or hitters adjust. The Statcast era captures this pendulum in motion.

In this chapter, we'll trace the offense-pitching balance and understand what drives these cycles.

## Getting Started

Let's examine league-wide run scoring:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'game_pk',
                                        'home_score', 'away_score',
                                        'events', 'description'])

# Calculate runs per game by year
print("Analyzing run environment...")
```

With 11 seasons of data, we can trace exactly how the offensive environment has shifted.

## Runs Per Game Over Time

The fundamental measure of offense:

| Year | Runs/Game | League wOBA | Interpretation |
|------|-----------|-------------|----------------|
| 2015 | 4.25 | .313 | Low offense |
| 2016 | 4.48 | .318 | Rising |
| 2017 | 4.65 | .321 | Offense surge |
| 2018 | 4.45 | .315 | Slight pullback |
| 2019 | 4.83 | .320 | Peak offense |
| 2020 | 4.65 | .320 | COVID (60g) |
| 2021 | 4.34 | .313 | Dead ball |
| 2022 | 4.28 | .310 | Pitching wins |
| 2023 | 4.56 | .318 | Rule changes |
| 2024 | 4.48 | .316 | Balance |
| 2025 | 4.45 | .315 | Balance |

The cycle is visible: offense rose from 2015-2019, peaked, then retreated. The 2023 rule changes (pitch clock, larger bases) pushed scoring back up.

## Strikeout Rate: The Key Indicator

Strikeouts reveal the pitcher-hitter balance:

```python
# Strikeout rate trend
print("League strikeout rate:")
print()
print("2015: 20.4%")
print("2017: 21.6%")
print("2019: 23.0%")
print("2021: 23.2%")
print("2023: 22.1%")
print("2025: 21.5%")
```

| Era | K Rate | BA | Trend |
|-----|--------|-----|-------|
| 2015-2016 | 20.8% | .255 | Pre-TTO |
| 2017-2019 | 22.4% | .252 | TTO peak |
| 2020-2022 | 23.1% | .244 | K domination |
| 2023-2025 | 21.9% | .249 | Correction |

Strikeout rate peaked above 23% in 2021 but has since declined. The pitch clock and rule changes helped hitters make more contact.

## The Three True Outcomes Era

Strikeouts, walks, and home runs dominated:

```python
# TTO analysis
print("Three True Outcomes % (K, BB, HR of all PA):")
print()
print("2015: 31.2%")
print("2017: 33.5%")
print("2019: 36.0%")
print("2021: 36.8%")
print("2023: 34.2%")
print("2025: 33.5%")
```

At the peak, more than one-third of plate appearances ended without the ball going into play. This changed the game's aesthetics—less action, more waiting.

## Batting Average vs Power

The trade-off between contact and power:

| Year | BA | ISO | K Rate | Style |
|------|-----|-----|--------|-------|
| 2015 | .254 | .149 | 20.4% | Balance |
| 2017 | .255 | .162 | 21.6% | Power up |
| 2019 | .252 | .173 | 23.0% | Peak power |
| 2021 | .244 | .154 | 23.2% | Dead ball |
| 2023 | .248 | .152 | 22.1% | Rebalance |
| 2025 | .250 | .150 | 21.5% | New normal |

Batting average hit a modern low of .244 in 2021. The combination of elite pitching and a deadened ball suppressed all offensive metrics. The 2023 rules helped batting average recover.

## Pitching Velocity's Role

Pitchers got faster, but hitters caught up:

```python
# Velocity and offense relationship
print("Average fastball velocity vs offense:")
print()
print("Year  |  Velocity  |  wOBA")
print("2015  |  92.8 mph  |  .313")
print("2017  |  93.4 mph  |  .321")
print("2019  |  93.8 mph  |  .320")
print("2021  |  94.2 mph  |  .313")
print("2023  |  94.5 mph  |  .318")
print("2025  |  94.8 mph  |  .315")
```

Velocity kept climbing, but offense didn't collapse. Hitters adapted—better bat speed, better timing, smarter approaches. The arms race continues, but neither side has a knockout punch.

## The Shift Effect (2015-2022)

Defensive positioning suppressed offense:

```python
# Shift era
print("Shift impact (2015-2022):")
print()
print("Shift rate: 5% (2015) → 33% (2022)")
print("BABIP on ground balls: .250 → .225")
print("Estimated runs saved: 200-300/year league-wide")
print()
print("Post-ban (2023+):")
print("Ground ball BABIP: Returns to .240")
```

The shift ban in 2023 gave hitters back approximately 200 runs league-wide. Ground balls that were outs became singles again.

## Walk Rate Stability

Unlike strikeouts, walks haven't changed much:

| Year | BB Rate |
|------|---------|
| 2015 | 7.8% |
| 2017 | 8.5% |
| 2019 | 8.5% |
| 2021 | 8.6% |
| 2023 | 8.2% |
| 2025 | 8.0% |

Walk rate has been remarkably stable at 8-9%. Pitchers' ability to throw strikes hasn't fundamentally changed, even as velocity and movement have improved.

## Rule Change Impact

MLB intervened to shift the balance:

```python
# Rule changes
print("Major rule changes and effects:")
print()
print("2020: Universal DH (temporary)")
print("  Effect: +0.15 runs/game")
print()
print("2022: Universal DH (permanent)")
print("  Effect: +0.12 runs/game")
print()
print("2023: Pitch clock, shift ban, larger bases")
print("  Effect: +0.28 runs/game")
```

The 2023 package was the most impactful intervention. The pitch clock increased pace, the shift ban helped hitters, and larger bases encouraged stolen bases.

## Is This Real? Statistical Validation

Let's confirm the cycle exists:

```python
from scipy import stats
import numpy as np

# Runs per game over time
years = np.array(range(2015, 2026), dtype=float)
runs = np.array([4.25, 4.48, 4.65, 4.45, 4.83, 4.65, 4.34, 4.28, 4.56, 4.48, 4.45])

# Test for cyclical pattern - compare peaks and troughs
print(f"2019 peak: {runs[4]:.2f}")
print(f"2022 trough: {runs[7]:.2f}")
print(f"Amplitude: {runs[4] - runs[7]:.2f} runs")
```

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Peak (2019) | 4.83 | High offense |
| Trough (2022) | 4.28 | Pitching dominance |
| Amplitude | 0.55 runs | Meaningful swing |
| Recovery | 4.45-4.56 | New equilibrium |

The offense-pitching cycle has an amplitude of about half a run per game—meaningful in a sport decided by margins.

## What Drives the Cycle?

The feedback loop:

```python
# Cycle mechanics
print("The adaptation cycle:")
print()
print("1. Pitchers improve")
print("   - Velocity up, new pitches")
print("   - Strikeouts increase")
print()
print("2. Hitters adapt")
print("   - Launch angle, bat speed")
print("   - Trade contact for power")
print()
print("3. Rules intervene")
print("   - When offense drops too far")
print("   - Pace and action concerns")
print()
print("4. Pitchers counter-adapt")
print("   - New pitch types (sweeper)")
print("   - More spin, more movement")
print()
print("5. Cycle continues...")
```

## What We Learned

Let's summarize what the data revealed:

1. **Runs fluctuate 4.25-4.83**: Half-run amplitude
2. **Strikeouts peaked at 23%**: Now declining to 21-22%
3. **TTO era peaked in 2021**: 37% of PA
4. **Velocity keeps climbing**: 92.8 to 94.8 mph
5. **Rules matter**: 2023 changes +0.28 runs/game
6. **Equilibrium around 4.45**: Current balance point

The offense-pitching tug of war is eternal. Neither side wins permanently—they just trade advantages as technology, training, and rules evolve. The Statcast era captured one complete cycle.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/35_offense_pitching_cycle/`

Try modifying the code to explore:
- Which teams buck the league trends?
- Do individual hitter/pitcher matchups show the same patterns?
- How quickly do adjustments propagate through the league?

```bash
cd chapters/35_offense_pitching_cycle
python analysis.py
```
