# Report Converter

Converts content plan and extracted code into final ABDWR-style markdown report.

## Trigger

Use after content organization and code extraction to generate the final report.

Keywords: convert report, generate markdown, write chapter, final report

## Purpose

This skill combines:
- Content plan (structure and narrative flow)
- Extracted code blocks (executable, cleaned)
- Actual results data (from CSV files)

Into a publication-ready markdown chapter in ABDWR style.

## Input Requirements

1. **Content plan** from Content Organizer
2. **Extracted code blocks** from Code Extractor
3. **Results CSV files** with actual data values
4. **Generated figures** (paths verified)

## ABDWR Style Specification

### Core Principles

1. **Conversational Exploration**: Write as if discovering with the reader
2. **Code-Narrative Integration**: Code blocks flow within the story
3. **Show Results Inline**: Tables appear after code that generates them
4. **Explain After Showing**: Code first, interpretation second

### Writing Patterns

**Opening Hook Pattern**:
```markdown
# Chapter Title

[2-3 sentence hook that poses a question or surprising fact]

In this chapter, we'll [verb: explore/analyze/examine] [topic] and [discovery goal].
```

**Getting Started Pattern**:
```markdown
## Getting Started

Let's [action verb] [what we're doing]:

```python
[data loading code block]
```

With [N million/thousand] [records/pitches/etc.], we can [analysis capability].
```

**Analysis Section Pattern**:
```markdown
## [Analysis Topic]

[Transition sentence connecting to previous section]

```python
[calculation code block]
```

| Column1 | Column2 | Column3 |
|---------|---------|---------|
| data    | data    | data    |

[Interpretation of results - 1-2 paragraphs]
```

**Visualization Pattern**:
```markdown
## [Figure Topic]

[Setup sentence explaining what we'll visualize]

![Description](../../chapters/XX_topic/figures/fig01_xxx.png)

[Caption explaining key takeaways - what does this show?]
```

**Statistical Validation Pattern**:
```markdown
## Is This Real? Statistical Validation

Let's confirm the [finding] with proper statistical tests:

```python
[statistical test code block]
```

| Test | Value | Interpretation |
|------|-------|----------------|
| Metric | X.XX | [meaning] |

[Interpretation paragraph - what do these tests tell us?]
```

**Summary Pattern**:
```markdown
## What We Learned

Let's summarize what the data revealed:

1. **[Finding 1 headline]**: [one-line summary]
2. **[Finding 2 headline]**: [one-line summary]
3. **[Finding 3 headline]**: [one-line summary]
4. **[Finding 4 headline]**: [one-line summary]
5. **[Finding 5 headline]**: [one-line summary]
6. **[Finding 6 headline]**: [one-line summary]

[Closing paragraph with broader implications]
```

**Try It Yourself Pattern**:
```markdown
## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/XX_topic/`

Try modifying the code to explore:
- [Exploration idea 1]
- [Exploration idea 2]
- [Exploration idea 3]

```bash
cd chapters/XX_topic
python analysis.py
```
```

## Conversion Process

### Step 1: Read Actual Results

```python
# Load results from CSV files
import pandas as pd

summary = pd.read_csv('chapters/XX_topic/results/summary.csv')
stats = pd.read_csv('chapters/XX_topic/results/statistical_tests.csv')
```

**Extract actual values** for use in narrative:
- Key metrics (means, percentages)
- Year-over-year changes
- Statistical test results
- Sample sizes

### Step 2: Generate Tables from Data

Convert CSV data to markdown tables:

```python
# From CSV
# year,avg_velocity,std
# 2015,92.8,4.2
# 2025,94.8,4.1

# To Markdown
| Year | Avg Velocity | Std Dev |
|------|--------------|---------|
| 2015 | 92.8 mph     | 4.2     |
| 2025 | 94.8 mph     | 4.1     |
```

### Step 3: Insert Code Blocks

Place extracted code at designated content plan locations:

```markdown
## Getting Started

Let's analyze fastball velocity trends:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=[
    'game_year', 'pitch_type', 'release_speed'
])

fastballs = df[df['pitch_type'] == 'FF']
print(f"Fastball pitches analyzed: {len(fastballs):,}")
```

With over 2.5 million fastballs tracked, we can trace velocity evolution precisely.
```

### Step 4: Write Narrative Connectors

**Transition phrases** (use sparingly):
- "Suppose we want to see..."
- "Let's examine..."
- "The data reveals..."
- "Looking at the breakdown..."
- "What drives this change?"

**Avoid**:
- "As you can see..."
- "Obviously..."
- "It's clear that..."
- "Now let's move on to..."

### Step 5: Format Statistical Results

Convert statistical test output to interpretation:

```python
# From statistical_tests.csv
# metric,value
# slope,0.18
# r_squared,0.94
# p_value,0.00001
# cohens_d,1.35

# To narrative
The trend is statistically robust:

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Slope | +0.18 mph/year | Consistent annual increase |
| R² | 0.94 | Explains 94% of variance |
| p-value | <0.001 | Highly significant |
| Cohen's d | 1.35 | Very large effect size |

The R² of 0.94 indicates an almost perfectly linear trend. The effect size (d=1.35) is very large, confirming that the velocity increase is not just statistically significant but practically meaningful.
```

## Output Format

### File Location

```
book/partX_category/chXX_topic.md
```

### Required Sections

1. **Title** (# Chapter N: Title)
2. **Opening Hook** (2-3 paragraphs, no code)
3. **Getting Started** (data loading code + context)
4. **Main Analysis** (2-4 sections with code and tables)
5. **Visualization** (figures with captions)
6. **Statistical Validation** (tests with interpretation)
7. **What We Learned** (6 bullet points)
8. **Try It Yourself** (execution instructions)

### Image Path Format

**CRITICAL**: Book chapters are in `book/partX/` so images need TWO parent traversals:

```markdown
![Figure](../../chapters/XX_topic/figures/fig01_xxx.png)
```

NOT `../chapters/` (wrong - only one level up)

## Quality Checks

Before finalizing:

- [ ] All numeric values come from actual results files
- [ ] No placeholder text (e.g., "[X]" or "TBD")
- [ ] All code blocks are syntactically valid
- [ ] Image paths use `../../chapters/` format
- [ ] Tables have consistent column alignment
- [ ] Statistical interpretations match values
- [ ] No orphaned references to non-existent sections
- [ ] Summary bullets match actual findings
- [ ] Execution instructions are accurate

## Example Conversion

### Input

**Content Plan Section**:
```yaml
section: main_analysis_1
purpose: "Show velocity by year"
code_block_id: analysis_calc
data_source: results/velocity_by_year.csv
figure: fig01_velocity_trend.png
```

**Extracted Code**:
```python
# Group by year and calculate mean velocity
yearly_velocity = fastballs.groupby('game_year')['release_speed'].mean()
print(yearly_velocity.round(2))
```

**Results Data** (velocity_by_year.csv):
```
game_year,avg_velocity
2015,92.8
2020,94.1
2025,94.8
```

### Output

```markdown
## Velocity by Year

Let's calculate the average fastball velocity for each season:

```python
# Group by year and calculate mean velocity
yearly_velocity = fastballs.groupby('game_year')['release_speed'].mean()
print(yearly_velocity.round(2))
```

| Year | Avg Velocity |
|------|--------------|
| 2015 | 92.8 mph |
| 2020 | 94.1 mph |
| 2025 | 94.8 mph |

![Velocity Trend](../../chapters/02_velocity_trend/figures/fig01_velocity_trend.png)

The progression is unmistakable. Average fastball velocity climbed from 92.8 mph in 2015 to 94.8 mph in 2025—a 2.0 mph increase over a decade. This represents the most significant velocity shift in baseball history.
```

## Final Validation

Run these checks before completing:

1. **Read the report as a reader would** - does it flow?
2. **Execute all code blocks** - do they work?
3. **Verify all figures exist** at referenced paths
4. **Cross-check all numbers** against source CSVs
5. **Check markdown rendering** - tables, code blocks, images
