# Report Converter

Converts content plan and extracted code into final ABDWR-style markdown report.

## Trigger

Use after content organization and code extraction to generate the final report.

Keywords: convert report, generate markdown, write chapter, final report

## Reference Style

Based on: **Analyzing Baseball Data with R, 3rd Edition**
Example: https://beanumber.github.io/abdwr3e/07-framing.html

## ABDWR Style Core Principles

### 1. Code is REAL and EXECUTABLE

Code blocks must be actual working code that produces results, not demonstrations:

```python
# WRONG - placeholder/demonstration style
print("Loading data...")
print(f"We have {n} pitches")

# RIGHT - ABDWR style (executable, produces real output)
sc_2024 = pd.read_parquet("data/statcast_2024.parquet")
called = sc_2024[sc_2024['description'].isin(['called_strike', 'ball'])]
```

### 2. Direct Language (No "Suppose" or "Let's")

```markdown
# WRONG
Suppose we want to examine velocity trends. Let's load the data.

# RIGHT
We examine velocity trends using Statcast data from 2015-2025.
We start by reading the pitch-level data.
```

### 3. Skip Intermediate Output Display

Do NOT show `.head()`, `print(df)`, or intermediate tibble outputs.
Instead, describe findings narratively:

```markdown
# WRONG
```python
print(df.head())
```
   pitch_type  release_speed
0  FF          94.2
1  SL          85.1
...

# RIGHT
The data contains pitch type and velocity for each pitch.
Fastballs average 94.2 mph while sliders average 85.1 mph.
```

### 4. Code Flows Naturally

Multi-step analysis shows each logical step with code, but skips intermediate output:

```python
# Step 1: Load and filter
df = load_seasons(2015, 2025, columns=['game_year', 'pitch_type', 'release_speed'])
fastballs = df[df['pitch_type'] == 'FF']

# Step 2: Calculate yearly averages
yearly_velocity = (
    fastballs
    .groupby('game_year')['release_speed']
    .agg(['mean', 'std', 'count'])
)
yearly_velocity.columns = ['avg_velocity', 'std', 'n_pitches']
```

### 5. Tables Come AFTER Code That Produces Them

Show the code, then show the output (as if executed):

```markdown
We calculate the average velocity by year:

```python
yearly_velocity = fastballs.groupby('game_year')['release_speed'].mean()
```

|game_year|avg_velocity|
|---------|------------|
|2015     |92.8        |
|2020     |94.1        |
|2025     |94.8        |

The progression is clear—average velocity increased 2.0 mph over the decade.
```

### 6. Figures Follow Their Code

```markdown
We visualize this trend in Figure 2.1.

```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(yearly_velocity.index, yearly_velocity.values, 'o-')
ax.set_xlabel('Year')
ax.set_ylabel('Average Velocity (mph)')
ax.set_title('Fastball Velocity Trend')
plt.savefig('figures/fig01_velocity_trend.png', dpi=150)
```

![Fastball velocity has increased steadily from 2015 to 2025](../../chapters/02_velocity_trend/figures/fig01_velocity_trend.png)

Note that velocity increased in nearly every season, with the steepest gains occurring between 2017 and 2019.
```

## Chapter Structure Template

```markdown
# Chapter N: Title

[Opening paragraph - establishes context and importance. NO code here.]

[Second paragraph - what we will explore in this chapter.]

## Getting the Data

We begin by reading the Statcast data for [years].

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=[
    'game_year', 'pitch_type', 'release_speed', 'release_spin_rate'
])
```

We focus on [specific subset], which we obtain by filtering:

```python
fastballs = df[df['pitch_type'] == 'FF']
```

## [Analysis Section Title]

[Brief statement of what we analyze.]

```python
[Analysis code - real, executable]
```

[Table output from the code above]

[Interpretation paragraph - what does this tell us?]

## [Visualization Section]

We plot [description] in Figure N.M.

```python
[Plotting code - real, executable]
```

![Caption](../../chapters/XX_topic/figures/figNN_name.png)

[Post-figure interpretation - what patterns do we observe?]

## Statistical Validation

[Brief setup for statistical tests]

```python
from scipy import stats

slope, intercept, r, p, se = stats.linregress(years, velocities)
```

|Metric|Value|
|------|-----|
|Slope|+0.18 mph/year|
|R²|0.94|
|p-value|<0.001|

The R² of 0.94 indicates [interpretation]. The trend is statistically significant (p < 0.001).

## Summary

[2-3 paragraph summary of findings]

## Further Reading

- [Reference 1]
- [Reference 2]

## Exercises

1. [Exercise question]
2. [Exercise question]
3. [Exercise question]
```

## Code Block Rules

### MUST Include
- Import statements (at first use)
- Variable assignments
- The actual calculation/transformation
- Plot saving commands

### MUST Exclude
- `print("Loading...")` progress messages
- `df.head()` debugging
- `time.time()` timing
- Comments like `# Debug` or `# TODO`
- Try/except with pass

### Format Guidelines
- Use meaningful variable names
- Chain operations with `.pipe()` or multiple lines
- Include comments only for non-obvious operations
- Keep blocks focused (one logical operation per block)

## Table Output Format

Tables appear as if they are output from code execution:

```markdown
|column1|column2|column3|
|-------|-------|-------|
|value1 |value2 |value3 |
|value4 |value5 |value6 |
```

- Left-align text, right-align numbers
- Use actual values from results CSVs
- Include units where appropriate

## Figure Captions

Captions describe what the figure shows:

```markdown
![Fastball velocity increased steadily from 92.8 mph (2015) to 94.8 mph (2025)](path/to/figure.png)
```

## Narrative Voice

| Use | Avoid |
|-----|-------|
| "We examine..." | "Let's examine..." |
| "We start by..." | "Suppose we want to..." |
| "Note that..." | "As you can see..." |
| "The data show..." | "Obviously..." |
| "One criticism is..." | "It's clear that..." |

## Transitions Between Sections

- "Next, we examine..."
- "To prepare these data for modeling, we..."
- "One criticism of this approach is that..."
- "We can extend this analysis by..."

## Quality Checklist

- [ ] All code blocks are executable Python
- [ ] No `print()` statements except for final results
- [ ] No `.head()` or debugging output shown
- [ ] Tables follow immediately after code that generates them
- [ ] Figures follow immediately after plotting code
- [ ] Direct language (no "suppose", "let's")
- [ ] Interpretations follow every code/table/figure
- [ ] Image paths use `../../chapters/` format
