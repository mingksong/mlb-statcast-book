# Chapter 25: The New Frontier of Bat Speed

In 2023, MLB introduced a new metric: bat speed. For the first time, we can measure how fast the bat moves through the zone—information that was previously invisible to tracking systems. This opens an entirely new dimension of hitting analysis.

In this chapter, we'll explore what bat speed reveals about hitting and how it connects to the metrics we've already examined.

## Getting Started

Bat speed tracking began in 2023, giving us limited but fascinating data:

```python
from statcast_analysis import load_seasons

df = load_seasons([2023, 2024, 2025], columns=['game_year', 'bat_speed', 'launch_speed',
                                                'launch_angle', 'events'])

# Filter to swings with bat speed data
swings = df.dropna(subset=['bat_speed'])
print(f"Swings with bat speed: {len(swings):,}")
```

With nearly 800,000 swings tracked across three seasons, we can begin to understand this new dimension.

## What Is Bat Speed?

Bat speed measures how fast the bat is moving at contact (or swing completion):

```python
# Understanding bat speed
print("Bat speed basics:")
print()
print("- Measured at bat-ball contact point")
print("- Units: miles per hour")
print("- Avg MLB bat speed: ~70 mph")
print("- Elite bat speed: 75+ mph")
print()
print("Related to but distinct from:")
print("- Exit velocity (result)")
print("- Swing mechanics (input)")
```

## League-Wide Bat Speed

Let's examine the distribution:

```python
# Calculate yearly averages
yearly_bat_speed = swings.groupby('game_year').agg({
    'bat_speed': ['mean', 'std', 'count']
})
print(yearly_bat_speed.round(1))
```

| Year | Mean Bat Speed | Std Dev | Swings |
|------|----------------|---------|--------|
| 2023 | 69.6 mph | 8.5 | 145,911 |
| 2024 | 69.5 mph | 8.9 | 316,353 |
| 2025 | 69.7 mph | 9.2 | 329,145 |

![Bat Speed Distribution](../../chapters/25_bat_speed/figures/fig01_bat_speed.png)

Average bat speed has been remarkably stable at about 69.5 mph across all three seasons. The standard deviation (~9 mph) tells us there's significant variation between swings and players.

## Bat Speed and Exit Velocity

The most important question: how does bat speed relate to exit velocity?

```python
from scipy.stats import pearsonr

# Filter to batted balls
batted = swings.dropna(subset=['launch_speed'])

correlation, p_value = pearsonr(batted['bat_speed'], batted['launch_speed'])
print(f"Correlation: r = {correlation:.3f}")
print(f"p-value: {p_value:.2e}")
```

| Relationship | Correlation | Interpretation |
|--------------|-------------|----------------|
| Bat Speed → Exit Velocity | r = 0.356 | Moderate positive |

The correlation is positive and meaningful (r = 0.356), but not as strong as you might expect. Bat speed explains only about 13% of exit velocity variance—other factors matter too.

## Why Isn't the Correlation Higher?

Bat speed isn't everything:

```python
# Factors affecting exit velocity
print("Exit velocity depends on:")
print()
print("1. Bat speed (measured)")
print("   - Faster bat = potential for harder contact")
print()
print("2. Contact quality (not fully captured)")
print("   - Sweet spot vs. edge")
print("   - Attack angle")
print()
print("3. Pitch factors")
print("   - Incoming velocity")
print("   - Ball-bat collision physics")
print()
print("4. Timing")
print("   - Early contact = pulled, harder")
print("   - Late contact = opposite field, softer")
```

You can swing hard and miss the sweet spot, producing soft contact. You can swing slower but time it perfectly, producing hard contact. Bat speed is necessary but not sufficient.

## The Distribution Shape

Let's look at the bat speed distribution:

```python
# Distribution analysis
percentiles = swings['bat_speed'].quantile([0.10, 0.25, 0.50, 0.75, 0.90])
print(percentiles.round(1))
```

| Percentile | Bat Speed |
|------------|-----------|
| 10th | 59.0 mph |
| 25th | 64.0 mph |
| 50th (median) | 70.0 mph |
| 75th | 75.5 mph |
| 90th | 80.0 mph |

The distribution is roughly normal with a slight left tail. Elite bat speed (75+ mph) is achieved by roughly the top quarter of swings.

## Swing Type Matters

Not all swings are created equal:

```python
# Context for bat speed
print("Swing context:")
print()
print("Protective swings (2 strikes)")
print("- Lower bat speed")
print("- Contact-focused")
print()
print("Aggressive swings (hitter's count)")
print("- Higher bat speed")
print("- Damage-focused")
print()
print("Pitch type matters too:")
print("- Fastball swings: Higher bat speed")
print("- Breaking ball swings: More varied")
```

Comparing bat speeds without context is misleading. A 65 mph protective swing with two strikes isn't worse than a 75 mph hack—it's a different goal.

## What We're Still Learning

Bat speed tracking is new, so many questions remain:

```python
# Open questions
print("Future research questions:")
print()
print("1. How does bat speed develop?")
print("   - Can players increase it?")
print("   - At what cost (injury, consistency)?")
print()
print("2. Is there a speed/contact trade-off?")
print("   - Do faster swings miss more?")
print("   - Optimal speed for different players?")
print()
print("3. How does bat speed vary by pitch?")
print("   - Fastball vs slider?")
print("   - Location effects?")
```

With only three years of data, we're just beginning to understand bat speed's role.

## Connection to Other Metrics

Bat speed fills a gap in our hitting framework:

```python
# Metric connections
print("The hitting equation:")
print()
print("Bat Speed (input)")
print("    ↓")
print("Contact Quality (process)")
print("    ↓")
print("Exit Velocity + Launch Angle (output)")
print("    ↓")
print("xBA, xSLG (expected outcome)")
print("    ↓")
print("Actual Results")
```

Before bat speed tracking, we could only see outputs (EV, LA) and outcomes (hits, home runs). Now we can see one key input.

## What We Learned

Let's summarize what the data revealed:

1. **Average bat speed is ~70 mph**: Stable across 2023-2025
2. **Moderate correlation with EV**: r = 0.356, meaningful but not dominant
3. **Contact quality matters too**: Bat speed is necessary but not sufficient
4. **Elite threshold ~75+ mph**: Top quartile of swings
5. **Context matters**: Swing intent varies by count and pitch
6. **New frontier**: Only 3 years of data, much to learn

Bat speed adds a new dimension to hitting analysis. It's not the whole story—contact quality and timing still matter enormously—but it gives us our first look at the input side of the hitting equation.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/25_bat_speed/`

Try modifying the code to explore:
- Which players have the highest average bat speed?
- How does bat speed vary by count?
- Is there a relationship between bat speed and strikeout rate?

```bash
cd chapters/25_bat_speed
python analysis.py
```
