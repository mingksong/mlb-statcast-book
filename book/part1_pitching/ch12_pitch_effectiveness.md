# Chapter 12: Pitch Effectiveness by Type

## Key Findings

- **Breaking balls most effective**: Lowest wOBA against of any category
- **Splitter is elite**: 0.267 wOBA against, best of any pitch in 2025
- **Sweeper arrived as a weapon**: 0.283 wOBA with 30% whiff rate
- **Fastball whiffs up 2%**: Velocity gains translate to more swings and misses
- **Overall stability**: Category effectiveness largely unchanged over decade

---

## The Story

Not all pitches are created equal. A 95 mph fastball down the middle is very different from an 85 mph slider on the corner. But which pitches are actually most effective at getting outs?

### The Hierarchy

In 2025, the effectiveness hierarchy by wOBA against (lower = better):

1. **Splitter (FS)**: 0.267 - The most effective pitch in baseball
2. **Sweeper (ST)**: 0.283 - A new pitch that's already elite
3. **Changeup (CH)**: 0.288 - The classic off-speed weapon
4. **Slider (SL)**: 0.300 - Still excellent, but not as dominant as 2015
5. **4-Seam (FF)**: 0.342 - Getting better, but still hittable

### The Surprise

The splitter's dominance is the story of modern pitching. It combines velocity deception (looks like a fastball) with movement deception (drops at the last moment). Japanese imports brought new splitter techniques to MLB, and the pitch has flourished.

---

## The Analysis

### Measuring Effectiveness

We used two primary metrics:

1. **wOBA Against**: Weighted on-base average allowed - the gold standard
2. **Whiff Rate**: Swinging strikes divided by swings - raw swing-and-miss ability

### 7.3 Million Pitches Analyzed

```python
# Calculate wOBA for each pitch type
for pitch_type in pitch_types:
    woba_data = df[df['woba_denom'] > 0]
    woba = woba_data['woba_value'].sum() / woba_data['woba_denom'].sum()
```

---

## The Numbers

### wOBA by Pitch Category

| Category | 2015 | 2025 | Change |
|----------|------|------|--------|
| Breaking | .267 | .294 | +.027 |
| Offspeed | .297 | .283 | -.015 |
| Fastball | .350 | .348 | -.003 |

### Whiff Rate by Category

| Category | 2015 | 2025 | Change |
|----------|------|------|--------|
| Breaking | 31.8% | 30.9% | -1.0% |
| Offspeed | 29.8% | 30.1% | +0.3% |
| Fastball | 15.0% | 17.0% | **+2.0%** |

### Individual Pitch wOBA Trends

| Pitch | 2015 | 2025 | Change |
|-------|------|------|--------|
| FF (4-Seam) | .350 | .342 | -.008 |
| SI (Sinker) | .359 | .353 | -.006 |
| FC (Cutter) | .319 | .358 | +.039 |
| SL (Slider) | .271 | .300 | +.029 |
| CU (Curveball) | .260 | .292 | +.032 |
| CH (Changeup) | .301 | .288 | -.013 |
| FS (Splitter) | .277 | .267 | -.010 |
| ST (Sweeper) | N/A | .283 | (new) |

---

## Visualizations

### Figure 1: wOBA by Category

![wOBA by Category](../chapters/12_pitch_effectiveness/figures/fig01_woba_by_category.png)

Breaking balls consistently allow the lowest wOBA.

### Figure 2: Whiff Rate by Category

![Whiff Rate](../chapters/12_pitch_effectiveness/figures/fig02_whiff_by_category.png)

Fastball whiff rates are climbing as velocity increases.

### Figure 3: wOBA by Pitch Type

![wOBA by Pitch](../chapters/12_pitch_effectiveness/figures/fig03_woba_by_pitch_type.png)

2015 vs 2025 comparison shows splitter's emergence.

---

## What It Means

1. **Breaking balls are still king**: Despite hitters adjusting, off-speed dominates
2. **The splitter revolution**: The most effective pitch wasn't fashionable in 2015
3. **Fastballs improving**: Velocity gains help, but they're still the most hittable
4. **Stability is the story**: Despite all the changes in baseball, pitch effectiveness is remarkably stable
5. **New pitches work**: The sweeper arrived and immediately became elite

---

## The Paradox

Breaking balls became slightly less effective over the decade, yet pitchers throw more of them than ever. Why?

The answer: **pitch mix**. A 30% whiff slider is most effective when paired with a 95 mph fastball. It's not about individual pitch effectiveness—it's about how pitches play off each other. That's why tunneling (Chapter 11) and arsenal diversity (Chapter 9) matter as much as raw pitch quality.

---

## Try It Yourself

```bash
cd chapters/12_pitch_effectiveness
python analysis.py
```
