# Chapter 15: Exit Velocity Revolution

## Key Findings

- **Average EV stable at ~83 mph**: Not the power driver many expected
- **Hard hit rate consistent**: 24-26% of batted balls hit 95+ mph
- **2015 data anomaly**: Early Statcast calibration inflated initial readings
- **Launch angle, not EV, drove HR surge**: Power revolution is about angle, not speed

---

## The Story

When Statcast launched in 2015, exit velocity became baseball's new obsession. "He hit that 115 mph!" became as common as "He threw 100!" The assumption was clear: hitters were hitting the ball harder than ever.

But the data tells a different story.

### The Surprise

Average exit velocity hasn't increased. It's been remarkably stable at around 83 mph since 2016. The home run surge of the late 2010s wasn't about hitting the ball harder—it was about hitting it at better angles.

### The 2015 Anomaly

Our data shows 2015 with an average EV of 87.1 mph, dropping to 83-84 mph in subsequent years. This isn't because hitters suddenly got weaker. Statcast's first year had different calibration, making direct 2015 comparisons unreliable.

---

## The Analysis

### 2.2 Million Batted Balls

```python
# Filter to batted balls with exit velocity data
df = df.dropna(subset=['launch_speed'])

# Calculate yearly averages
yearly = df.groupby('game_year')['launch_speed'].mean()
```

### Exit Velocity by Year

| Year | Mean EV | Hard Hit % | Elite (100+) % |
|------|---------|------------|----------------|
| 2015 | 87.1 | 31.8% | 17.8% |
| 2016 | 84.1 | 26.3% | 15.2% |
| 2017 | 82.1 | 24.0% | 13.8% |
| 2018 | 83.5 | 25.1% | 14.4% |
| 2019 | 83.9 | 25.9% | 15.2% |
| 2020 | 82.8 | 24.6% | 14.0% |
| 2021 | 82.2 | 23.7% | 13.9% |
| 2022 | 82.3 | 23.6% | 13.6% |
| 2023 | 82.6 | 24.2% | 14.2% |
| 2024 | 82.5 | 23.8% | 13.8% |
| 2025 | 83.1 | 25.5% | 15.4% |

---

## Statistical Validation

| Test | Result | Interpretation |
|------|--------|----------------|
| Trend slope | -0.26 mph/year | Slight decline |
| R² | 0.367 | Moderate fit |
| p-value | 0.048 | Marginally significant |
| Cohen's d | -0.093 | **Negligible effect** |

The negligible Cohen's d tells the real story: any year-to-year changes are not practically meaningful.

---

## Visualizations

### Figure 1: Exit Velocity Trend

![EV Trend](../../chapters/15_exit_velocity/figures/fig01_ev_trend.png)

The 2015 outlier is visible. Post-2015 data shows remarkable stability.

### Figure 2: Hard Hit Rate

![Hard Hit Rate](../../chapters/15_exit_velocity/figures/fig02_hard_hit_rate.png)

Hard hit rate (95+ mph) follows a similar pattern to mean EV.

### Figure 3: Distribution Comparison

![Distribution](../../chapters/15_exit_velocity/figures/fig03_ev_distribution.png)

2015 vs 2025 distributions show the calibration shift.

### Figure 4: Percentile Trends

![Percentiles](../../chapters/15_exit_velocity/figures/fig04_ev_percentiles.png)

Median, 90th, and 95th percentiles over time.

---

## What It Means

### 1. The Power Revolution Wasn't About EV

Home runs surged in the late 2010s, but not because hitters hit the ball harder. They hit it at better angles. Launch angle optimization (Chapter 16) was the real driver.

### 2. Hitters Aren't Getting Stronger

Despite strength training advances, average exit velocity hasn't increased. There may be a physical ceiling to how hard humans can hit a baseball.

### 3. Data Quality Matters

The 2015 anomaly reminds us that measurement systems evolve. Early Statcast data should be used cautiously for historical comparisons.

### 4. Stability Is the Story

From 2016-2025, exit velocity has been remarkably consistent. The variation is noise, not signal.

---

## The Bigger Picture

Exit velocity is the first piece of the batted ball puzzle. Combined with launch angle (Chapter 16), it determines outcomes. But EV alone doesn't explain the changes in baseball's offensive environment.

The real revolution was angles, not speed.

---

## Try It Yourself

```bash
cd chapters/15_exit_velocity
python analysis.py
```
