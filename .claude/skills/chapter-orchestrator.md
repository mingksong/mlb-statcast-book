# Research Orchestrator 2.0

Advanced research orchestrator for MLB Statcast Analytics Book with statistical validation.

## Trigger

**Command**: `start chapter N research` (e.g., "start chapter 3 research")

Also triggers on: create chapter, new chapter, research topic, analyze chapter

## Pre-Execution Requirements

1. **Read RESEARCH_PLAN.md** to identify:
   - Chapter title and topic
   - Required data columns
   - Research status (GO/PARTIAL/DONE)
   - Part assignment (Pitching/Batting/etc.)

2. **Verify data availability**:
   ```bash
   ls data/raw/statcast_*.parquet
   ```

---

## Research Pipeline (6 Phases)

### Phase 1: Research Design (PLAN)

**Goal**: Define research questions and methodology

1. **Read research plan**:
   ```
   RESEARCH_PLAN.md → Find chapter N details
   ```

2. **Define research questions**:
   - Primary question (main finding)
   - Secondary questions (2-3 supporting analyses)
   - Null hypothesis for statistical tests

3. **Identify required data**:
   - List all Statcast columns needed
   - Estimate data coverage (%)
   - Plan filtering criteria

4. **Create chapter structure**:
   ```
   chapters/XX_topic_name/
   ├── README.md
   ├── analysis.py
   ├── figures/
   └── results/
   ```

**Output**: Research design documented in analysis.py docstring

---

### Phase 2: Data Extraction (EXTRACT)

**Goal**: Load and prepare data for analysis

1. **Load data with column filtering**:
   ```python
   from statcast_analysis import load_season, load_seasons, AVAILABLE_SEASONS

   columns = ['pitch_type', 'release_speed', 'game_year', ...]
   df = load_seasons(AVAILABLE_SEASONS, columns=columns)
   ```

2. **Apply filters**:
   ```python
   # Example: Filter to 4-seam fastballs only
   df = df[df['pitch_type'] == 'FF']
   df = df.dropna(subset=['release_speed'])
   ```

3. **Data quality report**:
   ```python
   print(f"Total records: {len(df):,}")
   print(f"Date range: {df['game_date'].min()} to {df['game_date'].max()}")
   print(f"Missing values:\n{df.isnull().sum()}")
   ```

**Output**: Clean DataFrame ready for analysis

---

### Phase 3: Descriptive Statistics (DESCRIBE)

**Goal**: Understand data distribution and basic patterns

**Required calculations**:

```python
def descriptive_stats(series, name="metric"):
    """Calculate comprehensive descriptive statistics."""
    stats = {
        'n': len(series),
        'mean': series.mean(),
        'std': series.std(),
        'median': series.median(),
        'min': series.min(),
        'max': series.max(),
        'p10': series.quantile(0.10),
        'p25': series.quantile(0.25),
        'p75': series.quantile(0.75),
        'p90': series.quantile(0.90),
        'skew': series.skew(),
        'kurtosis': series.kurtosis(),
    }
    return stats
```

**Year-by-year breakdown**:
```python
yearly_stats = df.groupby('game_year').agg({
    'metric': ['count', 'mean', 'std', 'median']
}).round(2)
```

**Output**: Descriptive statistics table in results/

---

### Phase 4: Statistical Analysis (ANALYZE)

**Goal**: Perform rigorous statistical tests

#### 4.1 Trend Analysis

```python
from scipy import stats
import numpy as np

# Linear regression for trend
years = yearly_stats.index.values
values = yearly_stats[('metric', 'mean')].values

slope, intercept, r_value, p_value, std_err = stats.linregress(years, values)

print(f"Trend Analysis:")
print(f"  Slope: {slope:.4f} per year")
print(f"  R²: {r_value**2:.4f}")
print(f"  p-value: {p_value:.4e}")
print(f"  95% CI for slope: [{slope - 1.96*std_err:.4f}, {slope + 1.96*std_err:.4f}]")
```

#### 4.2 Period Comparison (Before/After)

```python
def compare_periods(df, metric, period1_years, period2_years):
    """Compare two time periods with t-test and effect size."""

    group1 = df[df['game_year'].isin(period1_years)][metric].dropna()
    group2 = df[df['game_year'].isin(period2_years)][metric].dropna()

    # Two-sample t-test
    t_stat, p_value = stats.ttest_ind(group1, group2)

    # Effect size (Cohen's d)
    pooled_std = np.sqrt(((len(group1)-1)*group1.std()**2 +
                          (len(group2)-1)*group2.std()**2) /
                         (len(group1) + len(group2) - 2))
    cohens_d = (group2.mean() - group1.mean()) / pooled_std

    # Confidence interval for difference
    se_diff = np.sqrt(group1.var()/len(group1) + group2.var()/len(group2))
    diff = group2.mean() - group1.mean()
    ci_lower = diff - 1.96 * se_diff
    ci_upper = diff + 1.96 * se_diff

    return {
        'period1_mean': group1.mean(),
        'period2_mean': group2.mean(),
        'difference': diff,
        'ci_95': (ci_lower, ci_upper),
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'effect_interpretation': interpret_cohens_d(cohens_d)
    }

def interpret_cohens_d(d):
    """Interpret Cohen's d effect size."""
    d = abs(d)
    if d < 0.2:
        return "negligible"
    elif d < 0.5:
        return "small"
    elif d < 0.8:
        return "medium"
    else:
        return "large"
```

#### 4.3 Correlation Analysis

```python
def correlation_analysis(df, x_col, y_col):
    """Calculate correlation with confidence interval."""

    x = df[x_col].dropna()
    y = df[y_col].dropna()

    # Align on common indices
    common = x.index.intersection(y.index)
    x, y = x[common], y[common]

    # Pearson correlation
    r, p = stats.pearsonr(x, y)

    # Fisher z-transformation for CI
    z = np.arctanh(r)
    se = 1 / np.sqrt(len(x) - 3)
    ci_lower = np.tanh(z - 1.96 * se)
    ci_upper = np.tanh(z + 1.96 * se)

    return {
        'r': r,
        'r_squared': r**2,
        'p_value': p,
        'ci_95': (ci_lower, ci_upper),
        'n': len(x)
    }
```

**Output**: Statistical test results with interpretations

---

### Phase 5: Visualization (VISUALIZE)

**Goal**: Create publication-ready figures

**Required figures**:
1. **Trend figure**: Year-over-year with confidence bands
2. **Distribution figure**: Before/after comparison
3. **Summary figure**: Key finding visualization

**Standard figure template**:
```python
def create_trend_figure(df, metric_col, title, ylabel, filename):
    """Create standardized trend figure with confidence intervals."""

    yearly = df.groupby('game_year')[metric_col].agg(['mean', 'std', 'count'])
    yearly['se'] = yearly['std'] / np.sqrt(yearly['count'])
    yearly['ci_lower'] = yearly['mean'] - 1.96 * yearly['se']
    yearly['ci_upper'] = yearly['mean'] + 1.96 * yearly['se']

    fig, ax = plt.subplots(figsize=(10, 6))

    # Main line
    ax.plot(yearly.index, yearly['mean'], 'o-', linewidth=2,
            markersize=8, color='#1f77b4', label='Mean')

    # 95% CI band
    ax.fill_between(yearly.index, yearly['ci_lower'], yearly['ci_upper'],
                    alpha=0.2, color='#1f77b4', label='95% CI')

    # Regression line
    slope, intercept, r, p, se = stats.linregress(yearly.index, yearly['mean'])
    ax.plot(yearly.index, intercept + slope * yearly.index,
            '--', color='red', linewidth=1.5,
            label=f'Trend (R²={r**2:.3f}, p={p:.3e})')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(loc='best')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename, dpi=150)
    plt.close()
```

**Output**: 3-5 figures in figures/ directory

---

### Phase 6: Documentation & Validation (DOCUMENT)

**Goal**: Complete documentation and verify reproducibility

#### 6.1 Create README.md

Include:
- Research question
- Methodology summary
- Key findings with statistics
- File listing
- Reproducibility instructions

#### 6.2 Create Book Chapter

Location: `book/partX_category/chXX_topic.md`

Structure:
```markdown
# [Chapter Title]

## Key Findings
- [Finding 1 with statistic]
- [Finding 2 with statistic]
- [Finding 3 with statistic]

## The Story
[Narrative explanation for general audience]

## The Analysis
[Code snippets with explanations]

## Statistical Validation
| Test | Result | Interpretation |
|------|--------|----------------|
| Trend slope | +X.XX/year | Significant increase |
| Cohen's d | X.XX | [Effect size] effect |
| p-value | <0.001 | Highly significant |

## Visualizations
[Embedded figures with captions]

## Try It Yourself
github.com/mingksong/mlb-statcast-book/chapters/XX_topic/
```

#### 6.3 Reproducibility Check

```bash
# Run analysis twice, verify identical outputs
python chapters/XX_topic/analysis.py
md5sum chapters/XX_topic/results/*.csv > /tmp/run1.md5
python chapters/XX_topic/analysis.py
md5sum chapters/XX_topic/results/*.csv > /tmp/run2.md5
diff /tmp/run1.md5 /tmp/run2.md5  # Should be empty
```

---

## Statistical Validation Checklist

Before marking chapter complete:

### Data Quality
- [ ] Sample size adequate (n > 1000 per year minimum)
- [ ] Missing values documented and handled
- [ ] Outliers identified (>3 SD flagged)
- [ ] Data range verified (no impossible values)

### Statistical Rigor
- [ ] Descriptive statistics complete
- [ ] Trend analysis with R² and p-value
- [ ] Effect size (Cohen's d) calculated
- [ ] 95% confidence intervals provided
- [ ] Statistical significance interpreted correctly

### Reproducibility
- [ ] Analysis runs without errors
- [ ] Results identical on re-run
- [ ] All figures generated
- [ ] Code documented in English

### Documentation
- [ ] README.md complete
- [ ] Book chapter complete
- [ ] Statistics table included
- [ ] Figures captioned

---

## Example Execution

**User**: "start chapter 3 research"

**Orchestrator Response**:

1. **Read RESEARCH_PLAN.md**:
   ```
   Chapter 03: Pitch Type Evolution
   Status: GO
   Key columns: pitch_type, game_year
   ```

2. **Execute 6-phase pipeline**:
   - PLAN: Define sweeper emergence research question
   - EXTRACT: Load pitch_type data 2015-2025
   - DESCRIBE: Calculate pitch mix percentages by year
   - ANALYZE: Test significance of sweeper adoption
   - VISUALIZE: Create stacked bar chart + sweeper trend
   - DOCUMENT: Write README + book chapter

3. **Output**:
   ```
   chapters/03_pitch_type/
   ├── README.md
   ├── analysis.py
   ├── figures/
   │   ├── fig01_pitch_mix_trend.png
   │   ├── fig02_sweeper_emergence.png
   │   └── fig03_pitch_distribution.png
   └── results/
       ├── pitch_mix_by_year.csv
       ├── statistical_tests.csv
       └── summary.csv
   ```

---

## Statistical Interpretation Guidelines

### P-value Interpretation
- p < 0.001: "highly significant"
- p < 0.01: "very significant"
- p < 0.05: "significant"
- p >= 0.05: "not statistically significant"

### Effect Size Interpretation (Cohen's d)
- |d| < 0.2: negligible
- 0.2 ≤ |d| < 0.5: small
- 0.5 ≤ |d| < 0.8: medium
- |d| ≥ 0.8: large

### R² Interpretation
- R² < 0.1: weak
- 0.1 ≤ R² < 0.3: moderate
- 0.3 ≤ R² < 0.5: substantial
- R² ≥ 0.5: strong

---

*Research Orchestrator 2.0 - Statistical rigor meets baseball analytics*
