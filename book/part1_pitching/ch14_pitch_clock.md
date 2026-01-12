# Chapter 14: The Pitch Clock Effect

## Key Findings

- **Game duration shortened**: But pitch-level metrics largely unchanged
- **Velocity still rising**: +0.5 mph from 2022 to 2025
- **Pitch mix stable**: Fastball/breaking ball ratio unchanged
- **Negligible statistical effect**: Cohen's d = 0.05 for pitches per game

---

## The Story

In 2023, Major League Baseball introduced the pitch clock:
- **15 seconds** with bases empty
- **20 seconds** with runners on

The goal: faster games. The fear: Would pitchers suffer?

### The Results

Three years later, the verdict is clear: the pitch clock changed game *duration*, not game *content*.

---

## The Analysis

### What We Measured

1. **Pitches per game** - Are games shorter because of fewer pitches?
2. **Velocity** - Does the clock cause fatigue?
3. **Pitch mix** - Do pitchers simplify under time pressure?
4. **Effectiveness** - Is either side disadvantaged?

### 4.5 Million Pitches (2019-2025)

We compared the pre-clock era (2019-2022) to the clock era (2023-2025), excluding 2020 due to the shortened COVID season.

---

## The Numbers

### Pitches Per Game

| Period | Avg Pitches/Game |
|--------|------------------|
| 2019 | 302.6 |
| 2021 | 293.3 |
| 2022 | 292.3 |
| 2023 | 296.6 |
| 2024 | 293.0 |
| 2025 | 293.2 |

**Finding**: Essentially unchanged. The clock doesn't reduce pitch counts—it reduces the time between them.

### Velocity by Year

| Year | Avg Velocity |
|------|-------------|
| 2022 | 88.89 mph |
| 2023 | 89.00 mph |
| 2024 | 89.15 mph |
| 2025 | 89.37 mph |

**Finding**: Velocity continued its decade-long rise. No fatigue effect.

### Velocity by Inning

| Inning | 2022 | 2024 |
|--------|------|------|
| 1 | 89.37 | 89.63 |
| 5 | 89.52 | 89.87 |
| 9 | 89.93 | 90.52 |

**Finding**: Late-inning velocity actually increased post-clock.

### Pitch Mix

| Category | 2022 | 2023 | Change |
|----------|------|------|--------|
| Fastball | 55.8% | 55.3% | -0.5% |
| Breaking | 30.4% | 30.5% | +0.1% |
| Offspeed | 12.8% | 13.0% | +0.2% |

**Finding**: No simplification. Pitchers maintained their full arsenals.

---

## Visualizations

### Figure 1: Pitches Per Game

![Pitches Per Game](../chapters/14_pitch_clock/figures/fig01_pitches_per_game.png)

The red line marks when the clock was introduced. No meaningful change.

### Figure 2: Effectiveness Metrics

![Effectiveness](../chapters/14_pitch_clock/figures/fig02_effectiveness.png)

wOBA and whiff rate remained stable across the transition.

### Figure 3: Pitch Mix

![Pitch Mix](../chapters/14_pitch_clock/figures/fig03_pitch_mix.png)

The breaking ball revolution continued uninterrupted.

### Figure 4: Velocity by Inning

![Velocity by Inning](../chapters/14_pitch_clock/figures/fig04_velocity_by_inning.png)

Pre and post-clock velocity curves are nearly identical.

---

## What It Means

### 1. The Clock Worked (For Pace)

Average game times dropped from over 3 hours to under 2:40. MLB achieved its goal.

### 2. Pitchers Adapted

Fears of clock-induced fatigue or rushed execution were unfounded. Professional athletes adjusted.

### 3. The Game Itself Didn't Change

The *content* of baseball—the pitches, the strategies, the outcomes—remained the same. Only the *tempo* changed.

### 4. Statistical Non-Effect

With Cohen's d = 0.05, the pitch clock's effect on pitch-level metrics is negligible. Whatever happened to game quality, it didn't show up in the data.

---

## The Bigger Picture

The pitch clock is a perfect case study in baseball analysis: sometimes the most talked-about changes have the least measurable impact on actual performance.

Game duration? Transformed.
Game content? Unchanged.

---

## Try It Yourself

```bash
cd chapters/14_pitch_clock
python analysis.py
```
