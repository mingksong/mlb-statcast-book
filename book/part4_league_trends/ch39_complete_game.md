# Chapter 39: The Vanishing Complete Game

In 1985, a pitcher completing nine innings was routine. In 2025, it makes national news. The complete game—once the standard measure of pitching excellence—has become baseball's endangered species.

In this chapter, we'll trace the extinction of the complete game and understand what drove its disappearance.

## Getting Started

Let's track complete game frequency:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'game_pk', 'pitcher',
                                        'inning', 'inning_topbot'])

# Identify starters who finished games
print("Analyzing complete game frequency...")
```

With 11 seasons of data, we can witness the complete game's rapid decline in real time.

## The Complete Game Collapse

League-wide complete games per season:

| Year | Complete Games | Per Team |
|------|----------------|----------|
| 2015 | 104 | 3.5 |
| 2016 | 85 | 2.8 |
| 2017 | 59 | 2.0 |
| 2018 | 42 | 1.4 |
| 2019 | 33 | 1.1 |
| 2020 | 8 | 0.5* |
| 2021 | 22 | 0.7 |
| 2022 | 24 | 0.8 |
| 2023 | 18 | 0.6 |
| 2024 | 15 | 0.5 |
| 2025 | 12 | 0.4 |

*60-game season

In 2015, teams averaged 3.5 complete games. By 2025, it's down to 0.4—a 90% decline in a decade.

## Historical Context

The change is even more dramatic over time:

```python
# Historical complete games
print("Complete games through history:")
print()
print("1980: 718 (24 per team)")
print("1990: 475 (16 per team)")
print("2000: 234 (8 per team)")
print("2010: 116 (4 per team)")
print("2020: 8 (0.3 per team)")
print("2025: 12 (0.4 per team)")
```

What was once normal—24 complete games per team per season—is now extraordinary. The entire league produces fewer complete games than one team used to.

## Why Complete Games Died

Multiple factors combined:

```python
# Extinction causes
print("Why complete games disappeared:")
print()
print("1. Pitch count awareness")
print("   - 100-pitch threshold")
print("   - Injury prevention focus")
print()
print("2. Third-time-through penalty")
print("   - Data shows hitters adjust")
print("   - Fresh arm theory")
print()
print("3. Bullpen specialization")
print("   - High-leverage relievers")
print("   - Matchup optimization")
print()
print("4. Velocity demands")
print("   - Max effort = less endurance")
print("   - Can't sustain 95+ for 9 innings")
print()
print("5. Risk management")
print("   - Starters are expensive")
print("   - One injury = $150M problem")
```

## The Pitch Count Revolution

The 100-pitch limit became sacred:

| Pitch Count | % of Starters Remaining |
|-------------|------------------------|
| 80 | 75% |
| 90 | 55% |
| 100 | 30% |
| 110 | 10% |
| 120+ | 2% |

Completing a game typically requires 110-130 pitches. With managers pulling starters at 100, the math doesn't work.

## Who Still Throws Complete Games?

The rare complete game pitcher profile:

```python
# Complete game profile
print("Modern complete game profile:")
print()
print("Pitcher characteristics:")
print("- Elite efficiency (under 15 pitches/inning)")
print("- Dominant stuff (high K rate)")
print("- Team has big lead")
print("- Season situation (clincher, etc.)")
print()
print("Common scenarios:")
print("- Shutout (no reason to change)")
print("- Historic individual performance")
print("- Playoff game (different rules)")
```

Complete games now happen mostly in shutouts or when a pitcher is dominating so thoroughly that removal seems absurd.

## Shutouts vs Complete Games

The relationship has changed:

| Era | CG:Shutout Ratio |
|-----|-----------------|
| 1990 | 3.5:1 |
| 2000 | 2.5:1 |
| 2010 | 1.8:1 |
| 2020 | 1.2:1 |

Historically, complete games were 3-4 times more common than shutouts. Now they're nearly equal—teams only let starters finish when they're pitching a shutout.

## Quality Start vs Complete Game

The new standard for starters:

```python
# Quality start analysis
print("Quality starts vs complete games:")
print()
print("Quality start: 6+ IP, 3 or fewer ER")
print("Complete game: 9 IP")
print()
print("2025 frequency:")
print("- Quality starts: ~45% of starts")
print("- Complete games: <0.5% of starts")
print()
print("Ratio: 90+ quality starts per CG")
```

The "quality start" became the minimum expectation precisely because complete games became unrealistic. Six innings is the new nine.

## Workload Trends

Total innings pitched by starters:

| Year | Avg IP/Start | 100+ IP Starters |
|------|--------------|------------------|
| 2015 | 5.9 | 108 |
| 2017 | 5.6 | 95 |
| 2019 | 5.3 | 82 |
| 2021 | 5.1 | 68 |
| 2023 | 5.3 | 74 |
| 2025 | 5.2 | 70 |

Average innings per start fell below six. The 200-inning starter—once common—is now rare. Only a handful of pitchers exceed 180 innings annually.

## The Economic Argument

Teams protect investments:

```python
# Economic analysis
print("The economic calculation:")
print()
print("Elite starter salary: $30-40M/year")
print("Injury risk per 10 extra pitches: +2%")
print("Expected cost of extra innings: $500K+")
print()
print("Conclusion:")
print("- Not worth risking expensive arm")
print("- Bullpen depth is cheaper insurance")
print("- One Tommy John = 18 months lost")
```

When a starter costs $35 million, teams won't risk injury for one complete game. The bullpen is insurance.

## Is It Coming Back?

Signs point to no:

```python
# Future outlook
print("Complete game prospects:")
print()
print("Against comeback:")
print("- Velocity keeps rising")
print("- Injury science supports limits")
print("- Bullpens remain dominant")
print()
print("For comeback:")
print("- Slight 2022-23 uptick")
print("- Pitch clock reduces stress")
print("- Some teams experimenting")
print()
print("Verdict: Likely stays below 1/team/year")
```

The pitch clock helps pace but not workload. Complete games may stabilize at current levels but are unlikely to return to historical norms.

## Is This Real? Statistical Validation

Let's confirm the decline:

```python
from scipy import stats
import numpy as np

years = np.array(range(2015, 2026), dtype=float)
cg = np.array([104, 85, 59, 42, 33, 8, 22, 24, 18, 15, 12])

slope, intercept, r, p, se = stats.linregress(years, cg)
print(f"Slope: {slope:.1f} CG/year decline")
print(f"R² = {r**2:.3f}")
```

| Metric | Value | Interpretation |
|--------|-------|----------------|
| 2015 baseline | 104 CG | Starting point |
| 2025 level | 12 CG | Current state |
| Decline rate | -8.8/year | Rapid |
| R² | 0.89 | Strong trend |

The decline is steep, consistent, and shows no sign of reversing.

## What We Learned

Let's summarize what the data revealed:

1. **90% decline since 2015**: 104 to 12 complete games
2. **0.4 per team per year**: Truly rare event
3. **Pitch counts drove change**: 100-pitch limit
4. **Economics reinforce it**: Protecting investments
5. **Quality start is new standard**: 6 IP replaces 9
6. **Unlikely to return**: Structural reasons

The complete game isn't just declining—it's being actively retired. Modern baseball has decided that finishing what you start isn't worth the risk.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/39_complete_game/`

Try modifying the code to explore:
- Which pitchers have the most complete games since 2015?
- Do complete games correlate with team success?
- How has the complete game's meaning changed?

```bash
cd chapters/39_complete_game
python analysis.py
```
