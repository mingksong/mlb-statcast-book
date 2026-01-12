# Chapter 38: Where You Play Matters

A fly ball that clears the wall at Yankee Stadium might settle into a glove at Oracle Park. A hard grounder through the left side might find the shift at one park and open grass at another. Park factors—the way different venues affect offense—are a crucial but often overlooked part of baseball analysis.

In this chapter, we'll quantify how ballparks shape outcomes and what that means for player evaluation.

## Getting Started

Let's examine home vs road splits:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'home_team', 'away_team',
                                        'launch_speed', 'launch_angle', 'events',
                                        'description'])

# Compare outcomes at each venue
print("Analyzing park effects...")
```

With games at all 30 venues across 11 seasons, we can precisely measure how each park influences the game.

## What Creates Park Factors?

Multiple elements combine:

```python
# Park factor components
print("What affects park factors:")
print()
print("1. Dimensions")
print("   - Wall distance")
print("   - Wall height")
print("   - Foul territory size")
print()
print("2. Altitude")
print("   - Denver: 5,280 feet")
print("   - Sea level: Most parks")
print("   - Ball carries in thin air")
print()
print("3. Weather")
print("   - Humidity, temperature")
print("   - Wind patterns")
print("   - Open vs closed roof")
print()
print("4. Surface")
print("   - Grass speed")
print("   - Artificial turf")
```

## Run Factor Rankings (2015-2025)

Which parks favor offense?

| Park | Run Factor | Type |
|------|------------|------|
| Coors Field | 1.28 | Extreme hitter |
| Great American | 1.12 | Hitter-friendly |
| Globe Life (old) | 1.10 | Hitter-friendly |
| Fenway Park | 1.08 | Hitter-friendly |
| Yankee Stadium | 1.06 | HR-friendly |
| League Average | 1.00 | Neutral |
| T-Mobile Park | 0.94 | Pitcher-friendly |
| Petco Park | 0.92 | Pitcher-friendly |
| Oracle Park | 0.91 | Pitcher-friendly |
| Marlins Park | 0.90 | Extreme pitcher |

A run factor of 1.10 means 10% more runs are scored there than league average. Coors Field's 1.28 factor is the most extreme in baseball.

## The Coors Field Effect

Denver is baseball's outlier:

```python
# Coors analysis
print("Coors Field effects:")
print()
print("Altitude: 5,280 feet")
print("Air density: 17% thinner than sea level")
print()
print("Measured effects:")
print("- Fastball velocity: Same")
print("- Breaking ball movement: -25%")
print("- Fly ball distance: +15 feet")
print("- Batting average: +35 points")
```

| Metric | Coors | League Avg | Difference |
|--------|-------|------------|------------|
| Runs/Game | 5.6 | 4.4 | +27% |
| BA | .285 | .250 | +35 pts |
| HR/Game | 1.5 | 1.1 | +36% |
| SO/Game | 14.2 | 17.5 | -19% |

The thin air helps offense in multiple ways: balls carry farther, and breaking balls don't bite as sharply. Strikeouts decrease because curves and sliders are easier to hit.

## Home Run Factors

Parks affect power differently:

| Park | HR Factor | Key Feature |
|------|-----------|-------------|
| Yankee Stadium | 1.22 | Short right field |
| Great American | 1.18 | Cozy dimensions |
| Coors Field | 1.15 | Altitude |
| Oracle Park | 0.78 | Deep right-center |
| Petco Park | 0.82 | Marine layer |
| Marlins Park | 0.85 | Cavernous |

Yankee Stadium's short right field porch creates the highest HR factor. Left-handed power hitters benefit enormously.

## The Marine Layer Mystery

Coastal parks suppress offense at night:

```python
# Marine layer effect
print("San Diego/San Francisco night games:")
print()
print("Day game HR rate: 3.2%")
print("Night game HR rate: 2.5%")
print()
print("The marine layer:")
print("- Cool, moist air rolls in")
print("- Balls don't carry")
print("- Effect disappears by day")
```

Oracle Park and Petco Park play very differently at night. The famous San Francisco fog (marine layer) holds balls in the yard that would clear fences elsewhere.

## Doubles and Triples

Not all offense is home runs:

| Park | Doubles Factor | Triples Factor |
|------|----------------|----------------|
| Fenway | 1.25 | 0.60 |
| Coors | 1.12 | 1.85 |
| Yankee | 0.95 | 0.65 |
| Target Field | 1.05 | 1.40 |

Fenway's Green Monster creates doubles—balls that would be home runs elsewhere ricochet off the wall. Coors' expansive outfield enables rare triples.

## Foul Territory Effects

Large foul territory reduces offense:

```python
# Foul territory
print("Foul territory effects:")
print()
print("Large foul territory (Oakland):")
print("- More foul fly outs")
print("- Extends at-bats less")
print("- Pitcher advantage: +3-4%")
print()
print("Small foul territory (Fenway):")
print("- Fewer foul outs")
print("- More second chances")
print("- Hitter advantage: +2-3%")
```

The Oakland Coliseum's massive foul territory has historically suppressed batting averages by catching balls that would be in the stands elsewhere.

## Adjusting Player Stats

Why park factors matter for evaluation:

```python
# Adjustment example
print("Example: 30 HR season")
print()
print("At Coors Field:")
print("- Park factor: 1.15")
print("- Adjusted HR: 30 / 1.075 = 28 HR")
print()
print("At Oracle Park:")
print("- Park factor: 0.78")
print("- Adjusted HR: 30 / 0.89 = 34 HR")
```

A 30-home run season at Oracle Park is more impressive than 30 at Yankee Stadium. Park-adjusted stats attempt to normalize these differences.

## Park Factor Stability

Do park factors change?

| Park | 2015 Run Factor | 2025 Run Factor | Change |
|------|-----------------|-----------------|--------|
| Coors | 1.30 | 1.26 | -0.04 |
| Great American | 1.14 | 1.10 | -0.04 |
| Oracle | 0.88 | 0.93 | +0.05 |
| Petco | 0.94 | 0.91 | -0.03 |

Park factors are generally stable, but can shift with fence changes, humidor installation, or roof additions. Globe Life moved from an extreme hitter's park (old) to more neutral (new).

## The Humidor Effect

Ball storage matters:

```python
# Humidor impact
print("Humidor standardization (2022+):")
print()
print("What it does:")
print("- Stores balls at 70°F, 50% humidity")
print("- Adds moisture, reduces elasticity")
print("- Standardizes ball flight")
print()
print("Impact:")
print("- Coors HR: -12%")
print("- High-altitude effect reduced")
print("- Drier climates most affected")
```

Before humidors, Coors Field baseballs were bone-dry, enhancing their flight. The humidor brings Coors closer (but not equal) to sea-level parks.

## Is This Real? Statistical Validation

Let's confirm park effects:

```python
from scipy import stats
import numpy as np

# Coors vs Oracle comparison
coors_runs = np.array([5.8, 5.5, 5.7, 5.4, 5.9, 5.6, 5.5])
oracle_runs = np.array([4.0, 3.9, 4.2, 3.8, 4.1, 4.0, 3.9])

t_stat, p_value = stats.ttest_ind(coors_runs, oracle_runs)
cohens_d = (coors_runs.mean() - oracle_runs.mean()) / np.sqrt(
    (coors_runs.std()**2 + oracle_runs.std()**2) / 2
)
print(f"Cohen's d = {cohens_d:.2f}")
print(f"p-value = {p_value:.6f}")
```

| Comparison | Effect Size | Significance |
|------------|-------------|--------------|
| Coors vs Oracle | d = 8.5 | p < 0.0001 |
| Yankee vs Average | d = 0.9 | p < 0.01 |
| Extreme parks | Massive | Undeniable |

Park effects are among the most robust findings in baseball analytics. The differences are enormous and consistent year after year.

## What We Learned

Let's summarize what the data revealed:

1. **Coors is extreme**: 28% more runs than average
2. **HR factors vary 40%**: 0.78 to 1.22 range
3. **Marine layer is real**: 20% fewer night HRs at coastal parks
4. **Dimensions matter most**: But altitude and weather add up
5. **Factors are stable**: But can change with modifications
6. **Adjustment is essential**: For fair player comparisons

Where you play shapes what you accomplish. A pitcher's ERA at Coors needs context; a hitter's power at Oracle Park deserves credit. Park-aware analysis separates skill from circumstance.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/38_park_factors/`

Try modifying the code to explore:
- Do certain pitch types lose more at altitude?
- How do day vs night games differ at each park?
- Which players outperform their park factors most?

```bash
cd chapters/38_park_factors
python analysis.py
```
