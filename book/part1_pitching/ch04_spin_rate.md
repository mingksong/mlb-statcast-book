# Chapter 4: Spin Rate Trends

## Key Findings

- **Spin rate increased 84 rpm** from 2,239 (2015) to 2,323 (2025)
- **High-spin fastballs doubled**: 6.1% → 13.2% at 2500+ rpm
- **2020 peak** marked the height of the "sticky substance" era
- **2021 crackdown** caused immediate 30 rpm drop, followed by gradual recovery

---

## The Story

The spin rate story is really two stories: the rise of an obsession, and baseball's response to its dark side.

### The Spin Revolution

In 2015, spin rate was a curiosity—interesting to analysts, ignored by most. By 2020, it had become the most talked-about metric in pitching development.

The numbers tell the tale:

| Year | Avg Spin (rpm) | 2500+ rpm % |
|------|----------------|-------------|
| 2015 | 2,239 | 6.1% |
| 2019 | 2,289 | 11.2% |
| 2020 | **2,304** | **15.0%** |
| 2021 | 2,274 | 10.0% |
| 2025 | 2,323 | 13.2% |

The spike to 2020 wasn't just improvement—it was an industry-wide embrace of "sticky stuff."

### The Crackdown

In June 2021, MLB began enforcing foreign substance rules. The effect was immediate and measurable: a 30 rpm drop almost overnight. Pitchers who had relied on spider tack and other grip enhancers suddenly had to adapt.

### The Recovery

But here's the remarkable part: by 2025, spin rates had not only recovered—they exceeded pre-crackdown levels. How?

- **Pitch design software**: Understanding how seam orientation affects movement
- **Legal grip products**: Approved substances for moisture control
- **Training methods**: Weighted ball programs and spin-efficiency drills
- **Player selection**: Teams prioritizing high-spin pitchers in development

The game found legal paths to the same destination.

---

## The Analysis

### Measuring 2.5 Million Fastballs

```python
from statcast_analysis import load_season, AVAILABLE_SEASONS

for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['pitch_type', 'release_spin_rate'])

    # Filter to 4-seam fastballs
    ff = df[(df['pitch_type'] == 'FF') &
            (df['release_spin_rate'] > 0) &
            (df['release_spin_rate'] < 4000)]

    spin = ff['release_spin_rate']
    high_spin_pct = (spin >= 2500).mean() * 100

    print(f"{year}: {spin.mean():.0f} rpm, {high_spin_pct:.1f}% at 2500+")
```

### Results by Year

| Year | Mean | SD | 2500+ % | n |
|------|------|-----|---------|---|
| 2015 | 2,239 | 166 | 6.1% | 242,490 |
| 2016 | 2,267 | 166 | 8.3% | 252,139 |
| 2017 | 2,260 | 165 | 7.6% | 248,888 |
| 2018 | 2,266 | 166 | 8.2% | 252,958 |
| 2019 | 2,289 | 168 | 11.2% | 263,358 |
| 2020 | 2,304 | 168 | 15.0% | 91,412 |
| 2021 | 2,274 | 171 | 10.0% | 251,219 |
| 2022 | 2,275 | 173 | 7.8% | 234,754 |
| 2023 | 2,283 | 175 | 9.3% | 229,208 |
| 2024 | 2,298 | 176 | 10.9% | 224,541 |
| 2025 | 2,323 | 178 | 13.2% | 225,485 |

---

## Statistical Validation

| Test | Metric | Value | Interpretation |
|------|--------|-------|----------------|
| Trend Slope | rpm/year | +5.58 | Significant increase |
| Trend 95% CI | | [2.84, 8.32] | Excludes zero |
| Trend R² | | 0.639 | Strong fit |
| Trend p-value | | 0.003 | Very significant |
| Cohen's d | (Early vs Late) | 0.260 | Small effect |

---

## Visualizations

### Figure 1: The Spin Rate Timeline

![Spin Rate Trend](../chapters/04_spin_rate/figures/fig01_spin_rate_trend.png)

Notice the 2020 peak and 2021 drop—the signature of the sticky substance saga.

### Figure 2: High-Spin Revolution

![2500+ Percentage](../chapters/04_spin_rate/figures/fig02_2500plus_percentage.png)

The proportion of elite-spin fastballs has more than doubled.

### Figure 3: Spin Across Pitch Types

![Spin by Pitch Type](../chapters/04_spin_rate/figures/fig03_spin_by_pitch_type.png)

All pitch types show upward spin trends.

### Figure 4: Distribution Shift

![Distribution Comparison](../chapters/04_spin_rate/figures/fig04_distribution_comparison.png)

The entire curve has shifted right over the decade.

---

## The Sticky Substance Timeline

| Period | Events |
|--------|--------|
| 2015-2018 | Baseline spin rates (~2,260 rpm) |
| 2019-2020 | "Sticky stuff" becomes widespread |
| June 2021 | MLB announces enforcement |
| 2021-2022 | Immediate drop, adjustment period |
| 2023-2025 | Recovery through legal innovation |

---

## What It Means

1. **Technology wins eventually**: Despite the crackdown, spin rates are now higher than ever through legal means
2. **The genie is out**: Pitchers learned what's possible and found legitimate paths
3. **Small effect, big impact**: Cohen's d of 0.26 seems modest, but 84 rpm creates noticeable pitch movement differences
4. **Development prioritization**: Teams now specifically seek high-spin arms

---

## Try It Yourself

Full analysis code:
```
github.com/mingksong/mlb-statcast-book/chapters/04_spin_rate/
```

Run it:
```bash
cd chapters/04_spin_rate
python analysis.py
```
