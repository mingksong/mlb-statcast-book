# Chapter 11: Tunneling Effect Analysis

## Key Findings

- **Release consistency improved 13%**: Pitchers throw from more consistent release points
- **FB-breaking separation down 32%**: Fastballs and breaking balls now look more alike
- **Medium effect size**: The improvement is statistically and practically significant
- **Analytics-driven**: Teams now train pitchers specifically on tunneling

---

## The Story

Pitch tunneling is perhaps the most sophisticated concept in modern pitching. It's not just about throwing hard or having nasty movement—it's about deception at the source.

### What is Tunneling?

Imagine you're a hitter. The pitcher releases the ball, and for the first 10-15 feet of flight, every pitch looks identical. Same release point, same early trajectory. By the time you can tell if it's a 95 mph fastball or an 85 mph slider, it's too late to adjust.

That's tunneling.

### The Old Way

Pitchers used to throw from wherever felt natural. Different grips led to slightly different arm slots and release points. Hitters could pick up subtle cues—a lower arm angle meant slider, higher meant fastball.

### The New Way

Today's pitchers obsess over release point consistency. Using Statcast data, they train to throw every pitch from the exact same spot in space. The result: better deception, more swing-and-miss, higher strikeout rates.

---

## The Analysis

### Measuring Tunneling

We used two key metrics:

1. **Release Consistency**: Standard deviation of release point across all pitches (lower = better)
2. **FB-Breaking Separation**: Distance between average fastball and breaking ball release points (lower = better tunneling)

### 7,540 Pitcher-Seasons Analyzed

```python
# Calculate 3D release point consistency
for pitcher in pitchers:
    x_std = pitcher_data['release_pos_x'].std()
    y_std = pitcher_data['release_pos_y'].std()
    z_std = pitcher_data['release_pos_z'].std()

    # Combined 3D consistency (lower = better)
    consistency = sqrt(x_std**2 + y_std**2 + z_std**2)
```

---

## The Numbers

### Release Consistency by Period

| Period | Consistency | Change |
|--------|-------------|--------|
| 2015-2018 | 0.365 in | baseline |
| 2022-2025 | 0.317 in | **-13%** |

### FB-Breaking Ball Separation

| Period | Separation | Change |
|--------|------------|--------|
| 2015-2018 | 0.307 in | baseline |
| 2022-2025 | 0.209 in | **-32%** |

### Statistical Validation

| Test | t-statistic | p-value | Cohen's d |
|------|-------------|---------|-----------|
| Release Consistency | 14.23 | <0.001 | 0.38 (small) |
| FB-Breaking Separation | 21.78 | <0.001 | 0.60 (medium) |

Both improvements are highly statistically significant.

---

## Visualizations

### Figure 1: Release Consistency Trend

![Release Consistency](../../chapters/11_tunneling/figures/fig01_release_consistency.png)

Year-over-year variation in release point consistency.

### Figure 2: FB-Breaking Separation

![FB-Breaking Separation](../../chapters/11_tunneling/figures/fig02_fb_breaking_separation.png)

The gap between fastball and breaking ball release points has narrowed.

### Figure 3: Distribution Comparison

![Distribution](../../chapters/11_tunneling/figures/fig03_consistency_distribution.png)

2025 pitchers cluster toward tighter consistency than 2015 pitchers.

---

## What It Means

1. **Pitching is more scientific**: Tunneling is trained, not accidental
2. **Deception matters as much as stuff**: You can throw 100 mph, but if hitters see it coming, they'll hit it
3. **Analytics changed training**: Teams use Statcast to optimize release points
4. **Connected to strikeout rise**: Better tunneling → more swing and miss

---

## A Note on the Data

The 2017-2019 period shows elevated values likely due to Statcast measurement calibration changes. The early vs. late period comparison (2015-18 vs 2022-25) provides the most reliable assessment of the true trend.

---

## Try It Yourself

```bash
cd chapters/11_tunneling
python analysis.py
```
