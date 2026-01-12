# Chapter 10: First Pitch Strategy

## Key Findings

- **First pitch fastballs dropped 7%**: 67.5% (2015) → 60.3% (2025)
- **Breaking balls on first pitch up 8%**: 22.8% → 30.4%
- **Strike rate slightly improved**: 49.5% → 50.5%
- **Velocity increased**: 92.8 → 94.2 mph (same as overall trend)

---

## The Story

The first pitch sets the tone for every plate appearance. Get ahead 0-1, and the advantage shifts to the pitcher. Fall behind 1-0, and hitters gain the upper hand.

For decades, the conventional wisdom was simple: throw a fastball for a strike.

### The Old Approach

In 2015, pitchers threw fastballs 67.5% of the time on the first pitch. The logic was straightforward:
- Fastballs are easier to command
- Get strike one, then expand the zone
- Breaking balls on 0-0 risk falling behind

### The New Reality

By 2025, first pitch strategy had fundamentally changed:
- Fastballs dropped to 60.3%
- Breaking balls rose to 30.4%
- Nearly one-third of plate appearances start with a breaking ball

### Why the Change?

The shift reflects broader trends:
1. **Better breaking balls**: Sweepers and sliders are more reliable strike-getters
2. **Hitter aggression**: Hitters swing more on first pitches, making breaking balls effective
3. **Unpredictability value**: Less predictable first pitches keep hitters off-balance

---

## The Analysis

### 1.9 Million First Pitches

```python
# Filter to first pitch of each plate appearance
first_pitch = df[df['pitch_number'] == 1]

# Calculate pitch type distribution by year
for year in range(2015, 2026):
    year_data = first_pitch[first_pitch['game_year'] == year]
    fb_pct = (year_data['pitch_category'] == 'Fastball').mean() * 100
    print(f"{year}: {fb_pct:.1f}% fastballs")
```

### Year-by-Year Breakdown

| Year | Fastball | Breaking | Offspeed |
|------|----------|----------|----------|
| 2015 | 67.5% | 22.8% | 8.7% |
| 2016 | 66.0% | 24.6% | 8.2% |
| 2017 | 65.6% | 25.9% | 7.8% |
| 2018 | 65.4% | 26.5% | 7.7% |
| 2019 | 62.5% | 28.9% | 8.1% |
| 2020 | 61.5% | 29.4% | 8.7% |
| 2021 | 61.8% | 29.3% | 8.4% |
| 2022 | 59.8% | 31.4% | 8.0% |
| 2023 | 60.1% | 30.8% | 8.3% |
| 2024 | 60.9% | 30.0% | 8.2% |
| 2025 | 60.3% | 30.4% | 8.3% |

---

## Statistical Validation

| Test | Metric | Value |
|------|--------|-------|
| Fastball Trend | Slope | -0.77%/year |
| Fastball Trend | R² | 0.863 (strong) |
| Fastball Trend | p-value | <0.001 |
| Strike Rate Trend | Slope | +0.13%/year |
| Strike Rate Trend | R² | 0.725 (strong) |

---

## Visualizations

### Figure 1: First Pitch Type Trend

![First Pitch Type](../../chapters/10_first_pitch/figures/fig01_first_pitch_type.png)

Fastballs declining, breaking balls rising - the lines are crossing.

### Figure 2: Strike Rate

![Strike Rate](../../chapters/10_first_pitch/figures/fig02_strike_rate.png)

Despite fewer fastballs, pitchers are getting slightly more first-pitch strikes.

---

## What It Means

1. **Old rules are changing**: "Throw fastball strike one" is no longer the default
2. **Breaking balls work**: Pitchers can start PAs with sliders and still get ahead
3. **The element of surprise**: Hitters can't sit fastball on 0-0 anymore
4. **Connected to pitch mix**: Part of the broader breaking ball revolution (Chapter 3)

---

## Try It Yourself

```bash
cd chapters/10_first_pitch
python analysis.py
```
