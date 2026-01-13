# Chapter 4: Spin Rate Trends

In 2015, the average four-seam fastball spun at 2,239 rpm. By 2025, that number had climbed to 2,323 rpm—an increase of 84 rpm over the decade. But the spin rate story is not a simple upward march. It includes a controversial peak in 2020, a dramatic enforcement-driven crash in 2021, and a remarkable recovery through legitimate innovation.

This chapter traces the evolution of pitch spin rates from 2015 to 2025, examining how technology, foreign substances, and rule enforcement shaped one of baseball's most scrutinized metrics.

## Getting the Data

We begin by loading Statcast pitch data and filtering to four-seam fastballs with valid spin rates.

```python
import pandas as pd
import numpy as np
from scipy import stats
from statcast_analysis import load_season, AVAILABLE_SEASONS

results = []
for year in AVAILABLE_SEASONS:
    df = load_season(year, columns=['pitch_type', 'release_spin_rate'])

    # Filter to 4-seam fastballs with valid spin data
    ff = df[(df['pitch_type'] == 'FF') &
            (df['release_spin_rate'].notna()) &
            (df['release_spin_rate'] > 0) &
            (df['release_spin_rate'] < 4000)]['release_spin_rate']

    n = len(ff)
    mean = ff.mean()
    std = ff.std()
    se = std / np.sqrt(n)

    results.append({
        'year': year,
        'count': n,
        'mean': mean,
        'std': std,
        'ci_lower': mean - 1.96 * se,
        'ci_upper': mean + 1.96 * se,
        'pct_2500plus': (ff >= 2500).mean() * 100,
    })

spin_df = pd.DataFrame(results)
```

The data contains over 2.5 million four-seam fastballs across 11 seasons.

## Spin Rate by Year

We calculate the average spin rate for each season.

```python
spin_df[['year', 'mean', 'std', 'count', 'pct_2500plus']]
```

|year|mean|std|count|pct_2500plus|
|----|----|----|-----|------------|
|2015|2239|200|242,490|6.1%|
|2016|2267|179|252,139|8.3%|
|2017|2260|171|248,888|7.6%|
|2018|2266|169|252,958|8.2%|
|2019|2289|175|263,358|11.2%|
|2020|2304|218|91,412|15.0%|
|2021|2274|182|251,219|10.0%|
|2022|2275|169|234,754|7.8%|
|2023|2283|166|229,208|9.3%|
|2024|2298|167|224,541|10.9%|
|2025|2323|162|225,485|13.2%|

The data reveals a complex pattern. Spin rates increased steadily from 2015-2020, peaked dramatically in 2020 (2,304 rpm), dropped sharply in 2021 (2,274 rpm), and then resumed climbing to reach 2,323 rpm by 2025.

## Visualizing the Trend

We plot the spin rate trend with 95% confidence intervals in Figure 4.1.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(spin_df['year'], spin_df['mean'], 'o-', linewidth=2, markersize=8,
        color='#1f77b4', label='Mean spin rate')
ax.fill_between(spin_df['year'], spin_df['ci_lower'], spin_df['ci_upper'],
                alpha=0.3, color='#1f77b4', label='95% CI')

# Add regression line
slope, intercept, r, p, se = stats.linregress(spin_df['year'], spin_df['mean'])
ax.plot(spin_df['year'], intercept + slope * spin_df['year'], '--',
        color='red', linewidth=2, label=f'Trend (R²={r**2:.3f})')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Average 4-Seam Fastball Spin Rate (rpm)', fontsize=12)
ax.set_title('Spin Rate Trends: 4-Seam Fastball (2015-2025)', fontsize=14)
ax.legend(loc='best')
plt.tight_layout()
plt.savefig('figures/fig01_spin_rate_trend.png', dpi=150)
```

![Average four-seam fastball spin rate increased from 2239 rpm (2015) to 2323 rpm (2025), with a notable peak in 2020](../../chapters/04_spin_rate/figures/fig01_spin_rate_trend.png)

The 2020 peak and 2021 drop are clearly visible. This pattern corresponds to MLB's enforcement of foreign substance rules in June 2021—the so-called "sticky stuff" crackdown.

## The Rise of High-Spin Fastballs

We examine the percentage of fastballs exceeding 2,500 rpm in Figure 4.2.

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(spin_df['year'], spin_df['pct_2500plus'], color='#ff7f0e',
       edgecolor='black', linewidth=0.5)

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Percentage of 4-Seamers at 2500+ rpm', fontsize=12)
ax.set_title('High Spin Fastballs: 2500+ rpm', fontsize=14)

for _, row in spin_df.iterrows():
    ax.text(row['year'], row['pct_2500plus'] + 0.5, f"{row['pct_2500plus']:.0f}%",
            ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('figures/fig02_2500plus_percentage.png', dpi=150)
```

![The percentage of high-spin fastballs peaked at 15% in 2020, dropped to 7.8% in 2022, then recovered to 13.2% by 2025](../../chapters/04_spin_rate/figures/fig02_2500plus_percentage.png)

In 2015, only 6.1% of fastballs exceeded 2,500 rpm. By 2020, that share had surged to 15.0%—more than doubling. After the crackdown, the percentage fell to 7.8% in 2022 before recovering to 13.2% by 2025.

## The Sticky Substance Era

The 2020 peak warrants closer examination. The COVID-shortened season coincided with widespread use of grip-enhancing substances—spider tack, sunscreen-rosin mixtures, and other foreign substances that could add 200+ rpm to a pitch.

```python
# Calculate the 2020-2021 drop
spin_2020 = spin_df[spin_df['year'] == 2020]['mean'].values[0]
spin_2021 = spin_df[spin_df['year'] == 2021]['mean'].values[0]
drop = spin_2020 - spin_2021
```

|Metric|Value|
|------|-----|
|2020 Mean|2,304 rpm|
|2021 Mean|2,274 rpm|
|Drop|30 rpm|

The 30 rpm drop from 2020 to 2021 represents the immediate impact of enforcement. Pitchers who had relied on sticky substances had to adapt quickly.

## Distribution Shift

We compare the full spin rate distributions between 2015 and 2025 in Figure 4.4.

```python
df_2015 = load_season(2015, columns=['pitch_type', 'release_spin_rate'])
df_2025 = load_season(2025, columns=['pitch_type', 'release_spin_rate'])

spin_2015 = df_2015[(df_2015['pitch_type'] == 'FF') &
                    (df_2015['release_spin_rate'] > 0) &
                    (df_2015['release_spin_rate'] < 4000)]['release_spin_rate']
spin_2025 = df_2025[(df_2025['pitch_type'] == 'FF') &
                    (df_2025['release_spin_rate'] > 0) &
                    (df_2025['release_spin_rate'] < 4000)]['release_spin_rate']

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(spin_2015, bins=50, alpha=0.6, label='2015', density=True, color='#1f77b4')
ax.hist(spin_2025, bins=50, alpha=0.6, label='2025', density=True, color='#ff7f0e')
ax.axvline(spin_2015.mean(), color='#1f77b4', linestyle='--', linewidth=2)
ax.axvline(spin_2025.mean(), color='#ff7f0e', linestyle='--', linewidth=2)
ax.set_xlabel('Spin Rate (rpm)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Spin Rate Distribution Shift: 2015 vs 2025', fontsize=14)
ax.legend()
plt.tight_layout()
plt.savefig('figures/fig04_distribution_comparison.png', dpi=150)
```

![The entire spin rate distribution shifted rightward from 2015 to 2025](../../chapters/04_spin_rate/figures/fig04_distribution_comparison.png)

|Percentile|2015|2025|Change|
|----------|----|----|------|
|10th|2,023 rpm|2,120 rpm|+97 rpm|
|25th|2,132 rpm|2,219 rpm|+87 rpm|
|Median|2,253 rpm|2,324 rpm|+71 rpm|
|75th|2,366 rpm|2,428 rpm|+62 rpm|
|90th|2,459 rpm|2,527 rpm|+68 rpm|

The entire distribution shifted rightward. Even low-spin pitchers (10th percentile) gained nearly 100 rpm. This suggests league-wide improvements in pitch design and training, not just individual outliers.

## Statistical Validation

We validate the trend using linear regression.

```python
years = spin_df['year'].values
means = spin_df['mean'].values

slope, intercept, r_value, p_value, std_err = stats.linregress(years, means)
r_squared = r_value ** 2
slope_ci_lower = slope - 1.96 * std_err
slope_ci_upper = slope + 1.96 * std_err
```

|Metric|Value|Interpretation|
|------|-----|--------------|
|Slope|+5.58 rpm/year|Consistent annual increase|
|Slope 95% CI|[2.84, 8.32]|Robust estimate|
|R²|0.639|Strong fit|
|p-value|0.003|Very significant|

The R² of 0.639 indicates that year explains nearly two-thirds of the variance in average spin rate. The trend is highly significant (p = 0.003).

## Period Comparison

We compare the early period (2015-2017) to the late period (2023-2025) using a two-sample t-test.

```python
early_data, late_data = [], []

for year in [2015, 2016, 2017]:
    df = load_season(year, columns=['pitch_type', 'release_spin_rate'])
    spin = df[(df['pitch_type'] == 'FF') &
              (df['release_spin_rate'] > 0) &
              (df['release_spin_rate'] < 4000)]['release_spin_rate']
    early_data.extend(spin.tolist())

for year in [2023, 2024, 2025]:
    df = load_season(year, columns=['pitch_type', 'release_spin_rate'])
    spin = df[(df['pitch_type'] == 'FF') &
              (df['release_spin_rate'] > 0) &
              (df['release_spin_rate'] < 4000)]['release_spin_rate']
    late_data.extend(spin.tolist())

early = np.array(early_data)
late = np.array(late_data)

t_stat, p_value = stats.ttest_ind(early, late)
pooled_std = np.sqrt(((len(early)-1)*early.std()**2 + (len(late)-1)*late.std()**2) /
                      (len(early) + len(late) - 2))
cohens_d = (late.mean() - early.mean()) / pooled_std
```

|Metric|Value|
|------|-----|
|Early Period Mean (2015-17)|2,255 rpm|
|Late Period Mean (2023-25)|2,301 rpm|
|Difference|+46 rpm|
|95% CI for Difference|[45, 46] rpm|
|t-statistic|-154.66|
|p-value|<0.001|
|Cohen's d|0.260|

The effect size (Cohen's d = 0.26) falls in the "small" range. However, in baseball terms, 46 additional rpm creates measurably different pitch movement—more rise on fastballs, more break on breaking balls.

## Summary

The spin rate evolution from 2015 to 2025 reveals a complex story:

1. **Average spin increased 84 rpm** from 2,239 (2015) to 2,323 (2025)
2. **High-spin fastballs more than doubled** from 6.1% to 13.2% at 2500+ rpm
3. **The sticky substance era peaked in 2020** with 15.0% of fastballs exceeding 2,500 rpm
4. **The crackdown caused a 30 rpm drop** from 2020 to 2021
5. **Legal innovation drove recovery** with spin rates exceeding pre-crackdown levels by 2025
6. **The trend is statistically significant** (R² = 0.639, p = 0.003)

What enabled the recovery without foreign substances? Pitch design technology, legal grip products, weighted ball training programs, and a focus on spin efficiency in player development all contributed. The game adapted and found legitimate paths to higher spin.

## Further Reading

- Boddy, K. (2020). "Spin Rate and Pitch Movement." *Driveline Baseball Research*.
- Nathan, A. M. (2019). "The Physics of Spin Rate." *Baseball Research Journal*.

## Exercises

1. Analyze spin rate trends for breaking balls (slider, curveball). Did they show the same 2020 peak and 2021 drop pattern as fastballs?

2. Identify individual pitchers who showed the largest spin rate drops from 2020 to 2021. What happened to their performance?

3. Calculate the correlation between spin rate and swinging strike rate. Is higher spin actually more effective?

```bash
cd chapters/04_spin_rate
python analysis.py
```
