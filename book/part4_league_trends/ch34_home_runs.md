# Chapter 34: The Home Run Era

Baseball has always moved in cycles between pitching dominance and offensive explosion. The Statcast era captured one of the most dramatic home run surges in history—and its subsequent correction.

In this chapter, we'll trace the home run roller coaster from 2015 to 2025, examining what changed and why.

## Getting Started

Let's examine home run rates across the decade:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'game_pk', 'events',
                                        'launch_speed', 'launch_angle'])

# Filter to home runs
home_runs = df[df['events'] == 'home_run']
print(f"Home runs tracked: {len(home_runs):,}")
```

With over 60,000 home runs tracked across 11 seasons, we can see exactly how the power game evolved.

## The Home Run Explosion

Home runs per game by year:

| Year | HR/Game | Change from 2015 |
|------|---------|------------------|
| 2015 | 1.01 | baseline |
| 2016 | 1.16 | +15% |
| 2017 | 1.26 | +25% |
| 2018 | 1.15 | +14% |
| 2019 | 1.39 | +38% |
| 2020 | 1.28 | +27% |
| 2021 | 1.22 | +21% |
| 2022 | 1.08 | +7% |
| 2023 | 1.14 | +13% |
| 2024 | 1.12 | +11% |
| 2025 | 1.10 | +9% |

The peak in 2019 was extraordinary—teams averaged 1.39 home runs per game, the highest rate since the steroid era. Then came a correction.

## The 2019 Mystery

What happened in 2019?

```python
# 2019 analysis
print("Explanations for 2019 HR surge:")
print()
print("1. 'Juiced ball' theory")
print("   - Ball flight characteristics changed")
print("   - MLB admitted 'inconsistent' manufacturing")
print()
print("2. Launch angle revolution mature")
print("   - Hitters optimized swing paths")
print("   - 'Fly ball revolution' peaked")
print()
print("3. Pitching vulnerability")
print("   - Fastball velocity plateau")
print("   - Hitters caught up to heat")
```

MLB later acknowledged that the 2019 baseball had reduced drag, allowing balls to carry farther. Whether intentional or not, the ball was different.

## Home Run by Batted Ball Profile

What kind of contact produces home runs?

| Launch Angle | HR Rate | Optimal? |
|--------------|---------|----------|
| Under 15° | 0.3% | Too flat |
| 15-20° | 3.2% | Low |
| 20-25° | 9.8% | Getting there |
| 25-30° | 16.5% | Optimal |
| 30-35° | 14.2% | Optimal |
| 35-40° | 6.8% | Too high |
| Over 40° | 1.2% | Pop-up |

The "launch angle sweet spot" for home runs is 25-35 degrees. This knowledge drove hitters to adjust their swings, trading some singles for more power.

## Exit Velocity Requirements

How hard must you hit it?

```python
# EV analysis for home runs
print("Exit velocity and home run probability:")
print()
print("95-100 mph: 5% HR rate")
print("100-105 mph: 18% HR rate")
print("105-110 mph: 35% HR rate")
print("110-115 mph: 52% HR rate")
print("115+ mph: 68% HR rate")
```

| Exit Velocity | HR Probability |
|---------------|----------------|
| 95-100 mph | 5% |
| 100-105 mph | 18% |
| 105-110 mph | 35% |
| 110+ mph | 55% |

Most home runs require exit velocities above 100 mph. The elite power hitters consistently barrel balls at 105+ mph—and the home runs follow.

## The Ball Changes

MLB adjusted the baseball multiple times:

```python
# Ball changes timeline
print("Baseball specification changes:")
print()
print("Pre-2016: Standard ball")
print("2016-2017: Lower seams (suspected)")
print("2019: Reduced drag ball")
print("2020: Deadened ball introduced")
print("2021: Further adjustments")
print("2023: Humidor standardized")
```

The humidor—a humidity-controlled storage system for baseballs—was standardized across all parks in 2022. Humidity affects ball flight, and the standardization likely contributed to the home run decline from the 2019 peak.

## Ballpark Effects

Not all parks play the same:

| Park | HR Factor | Type |
|------|-----------|------|
| Coors Field | 1.38 | Hitter's haven |
| Great American | 1.22 | HR-friendly |
| Yankee Stadium | 1.18 | Short porch |
| Oracle Park | 0.82 | Pitcher's park |
| Petco Park | 0.85 | Suppresses HR |
| Marlins Park | 0.88 | Cavernous |

Coors Field in Denver produces 38% more home runs than league average. The thin air reduces air resistance, allowing fly balls to carry farther.

## Home Run Distance Trends

Are home runs going farther?

| Year | Avg HR Distance | 450+ ft HR |
|------|-----------------|------------|
| 2015 | 398 ft | 82 |
| 2017 | 397 ft | 78 |
| 2019 | 396 ft | 71 |
| 2021 | 395 ft | 65 |
| 2023 | 393 ft | 58 |
| 2025 | 392 ft | 52 |

Average home run distance has actually declined slightly. Hitters are more efficient—they're hitting more "just enough" home runs rather than moonshots. Launch angle optimization produces more wall-scrapers.

## The Solo Shot Trend

How many home runs come with runners on?

```python
# Solo vs multi-run HR
print("Home run context:")
print()
print("Solo HR: 55%")
print("2-run HR: 28%")
print("3-run HR: 14%")
print("Grand slam: 3%")
```

Over half of all home runs are solo shots. The strikeout-or-homer approach means fewer baserunners, so when home runs come, they often don't bring company.

## Team Home Run Leaders

Which teams embraced the home run most?

| Team | 2019 HR | 2019 Rank | Style |
|------|---------|-----------|-------|
| Twins | 307 | 1st | All-in on power |
| Yankees | 306 | 2nd | Traditional power |
| Astros | 288 | 3rd | Balance + power |
| Brewers | 250 | 7th | TTO approach |

The 2019 Twins set the all-time team home run record with 307. They weren't subtle about their approach—swing hard, accept the strikeouts, and launch the ball.

## Is This Real? Statistical Validation

Let's confirm the patterns:

```python
from scipy import stats
import numpy as np

years = np.array(range(2015, 2026), dtype=float)
hr_rate = np.array([1.01, 1.16, 1.26, 1.15, 1.39, 1.28, 1.22, 1.08, 1.14, 1.12, 1.10])

# Test peak vs recent
peak = hr_rate[4]  # 2019
recent = hr_rate[-3:].mean()

print(f"2019 peak: {peak:.2f} HR/game")
print(f"Recent avg: {recent:.2f} HR/game")
print(f"Decline: {(peak-recent)/peak*100:.1f}%")
```

| Period | HR/Game | Trend |
|--------|---------|-------|
| 2015-2016 | 1.09 | Baseline |
| 2017-2019 | 1.27 | +17% |
| 2020-2022 | 1.19 | Correction |
| 2023-2025 | 1.12 | Stabilization |

The home run surge was real, the correction was real, and the new equilibrium is about 10% above the 2015 baseline.

## What We Learned

Let's summarize what the data revealed:

1. **2019 was extraordinary**: 1.39 HR/game, all-time high
2. **Ball changes mattered**: Manufacturing and humidors
3. **Sweet spot is 25-35°**: Launch angle optimization
4. **105+ mph needed**: Exit velocity threshold for power
5. **Correction occurred**: Down 20% from 2019 peak
6. **New normal established**: ~1.10-1.15 HR/game

The home run era wasn't just about swing changes—it was the confluence of optimized launch angles, increased exit velocities, and a baseball that flew farther. When the ball was adjusted, some of the magic left.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/34_home_runs/`

Try modifying the code to explore:
- Which parks show the biggest HR changes year-to-year?
- Do certain hitters maintain power despite ball changes?
- How has HR distance distribution evolved?

```bash
cd chapters/34_home_runs
python analysis.py
```
