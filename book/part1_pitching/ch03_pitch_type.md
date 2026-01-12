# Chapter 3: Pitch Type Evolution

## Key Findings

- **Four-seam fastball usage declined** from 35.6% (2015) to 31.9% (2025)
- **Sweeper emerged from obscurity** to 7.0% usage (fastest-growing pitch)
- **Sinker saw the largest decline**: -5.8 percentage points over the decade
- **Breaking balls gained**: 21.9% (2015) → 28.8% (2025) of all pitches

---

## The Story

If you watched baseball in 2015 and then jumped forward to 2025, the most noticeable change wouldn't be velocity or spin rate—it would be *what* pitchers throw.

### The Fastball Fade

For generations, the four-seam fastball was the alpha pitch. Throw hard, challenge hitters. In 2015, it comprised over 35% of all pitches. By 2025, that number had dropped below 32%.

The sinker's decline was even more dramatic. Once the pitch of choice for ground-ball specialists, sinker usage cratered from 21.3% to 15.5%—nearly a 6 percentage point drop.

### The Sweeper Revolution

No pitch better captures baseball's analytical transformation than the sweeper. In 2015, it barely existed in the data—less than 0.1% of pitches. Today, it's thrown more than 7% of the time.

| Year | Sweeper Usage |
|------|---------------|
| 2015 | 0.1% |
| 2018 | 0.7% |
| 2021 | 2.0% |
| 2025 | **7.0%** |

The sweeper combines slider-like horizontal movement with a flatter trajectory, creating a pitch that tunnels with fastballs while moving dramatically away from batters.

### The New Balance

The overall shift tells a clear story:

| Category | 2015 | 2025 | Change |
|----------|------|------|--------|
| Fastball | 62.6% | 55.0% | -7.6% |
| Breaking | 21.9% | 28.8% | +6.9% |
| Offspeed | 12.1% | 13.6% | +1.5% |

Breaking balls gained almost exactly what fastballs lost.

---

## The Analysis

### Tracking 7.4 Million Pitches

```python
from statcast_analysis import load_seasons, AVAILABLE_SEASONS

# Load all pitch data
df = load_seasons(AVAILABLE_SEASONS, columns=['pitch_type', 'game_year'])

# Calculate yearly pitch mix
pitch_mix = df.groupby(['game_year', 'pitch_type']).size()
pitch_mix = pitch_mix.unstack(fill_value=0)
pitch_mix = pitch_mix.div(pitch_mix.sum(axis=1), axis=0) * 100
```

### Winners and Losers

**Increasing (Statistically Significant)**:
| Pitch | Trend | R² | p-value |
|-------|-------|-----|---------|
| Sweeper | +0.77%/year | 0.87 | <0.001 |
| Cutter | +0.29%/year | 0.89 | <0.001 |
| Splitter | +0.16%/year | 0.67 | 0.004 |

**Decreasing (Statistically Significant)**:
| Pitch | Trend | R² | p-value |
|-------|-------|-----|---------|
| Sinker | -0.65%/year | 0.74 | <0.001 |
| 4-Seam | -0.44%/year | 0.72 | <0.001 |
| Curveball | -0.15%/year | 0.51 | 0.014 |

---

## Statistical Validation

| Test | Pitch | Result | Interpretation |
|------|-------|--------|----------------|
| Trend R² | 4-Seam | 0.718 | Strong decline |
| Trend R² | Sinker | 0.739 | Strong decline |
| Trend R² | Sweeper | 0.936 | Very strong growth |
| Effect Size | Sweeper (2015 vs 2025) | h=0.41 | Small-medium |

---

## Visualizations

### Figure 1: The Shifting Landscape

![Pitch Type Evolution](../chapters/03_pitch_type/figures/fig01_pitch_type_evolution.png)

A decade of change captured in stacked area form.

### Figure 2: Sweeper's Meteoric Rise

![Sweeper Emergence](../chapters/03_pitch_type/figures/fig02_sweeper_emergence.png)

From nothing to 7% in ten years—the fastest pitch adoption in modern history.

### Figure 3: Fastball Decline

![Fastball Decline](../chapters/03_pitch_type/figures/fig03_fastball_decline.png)

The steady erosion of the traditional workhorse pitch.

### Figure 4: Category Balance

![Pitch Categories](../chapters/03_pitch_type/figures/fig04_pitch_categories.png)

Fastballs down, breaking balls up—the macro trend is unmistakable.

---

## What It Means

1. **Pitch design wins**: The sweeper's rise shows how analytical pitch development creates new weapons
2. **Movement over velocity**: Pitchers are trading pure speed for horizontal break
3. **Sinker death**: Ground-ball pitching has given way to strikeout-chasing approaches
4. **The cutter's rise**: A hybrid pitch that combines velocity with late movement

---

## Try It Yourself

Full analysis code:
```
github.com/mingksong/mlb-statcast-book/chapters/03_pitch_type/
```

Run it:
```bash
cd chapters/03_pitch_type
python analysis.py
```
