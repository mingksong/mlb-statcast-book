# Report Code Extractor

Extracts executable, relevant code blocks from analysis.py that match the content plan.

## Trigger

Use after content organization to extract code blocks for report insertion.

Keywords: extract code, get code blocks, match code, executable code

## Reference Style

Based on: **Analyzing Baseball Data with R, 3rd Edition**
Example: https://beanumber.github.io/abdwr3e/07-framing.html

## Purpose

This skill parses analysis.py and extracts ONLY code that:
- Is REAL and EXECUTABLE (not placeholder demonstrations)
- Produces actual results (data transformations, calculations, figures)
- Follows ABDWR style (no print debugging, no intermediate output)

## Input Requirements

1. **Content plan** from Content Organizer (section → code mapping)
2. **analysis.py** source file

## Code Block Types

### Type 1: Data Loading

**Purpose**: Show readers how to load and prepare data

**Extract**:
```python
# GOOD - Extract this
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=[
    'game_year', 'pitch_type', 'release_speed'
])
fastballs = df[df['pitch_type'] == 'FF']
```

**Exclude**:
```python
# BAD - Don't extract
print("Loading data...")  # Debug output
import time
start = time.time()  # Timing code
```

### Type 2: Calculation/Analysis

**Purpose**: Show core analysis logic

**Extract**:
```python
# GOOD - Extract this
yearly_avg = df.groupby('game_year')['release_speed'].agg(['mean', 'std', 'count'])
yearly_avg.columns = ['avg_velocity', 'std_velocity', 'n_pitches']
```

**Exclude**:
```python
# BAD - Don't extract
print(f"Processing year {year}...")  # Loop progress
print(yearly_avg.head())  # Debug inspection
yearly_avg.to_csv('results/temp.csv')  # Intermediate file
```

### Type 3: Visualization

**Purpose**: Show how figures were created

**Extract**:
```python
# GOOD - Extract this
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(years, velocities, 'o-', linewidth=2, markersize=8)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Average Velocity (mph)', fontsize=12)
ax.set_title('Fastball Velocity Trend (2015-2025)', fontsize=14)
plt.tight_layout()
plt.savefig('figures/fig01_velocity_trend.png', dpi=150)
```

**Exclude**:
```python
# BAD - Don't extract
plt.show()  # Interactive display
print("Figure saved!")  # Confirmation
# Debug: check if file exists
import os
print(os.path.exists('figures/fig01.png'))
```

### Type 4: Statistical Tests

**Purpose**: Show validation methodology

**Extract**:
```python
# GOOD - Extract this
from scipy import stats
import numpy as np

# Linear regression for trend
slope, intercept, r, p, se = stats.linregress(years, velocities)

# Effect size (Cohen's d)
early = df[df['game_year'] <= 2017]['release_speed']
late = df[df['game_year'] >= 2023]['release_speed']
cohens_d = (late.mean() - early.mean()) / np.sqrt(
    (early.std()**2 + late.std()**2) / 2
)
```

**Exclude**:
```python
# BAD - Don't extract
print(f"Slope: {slope}")  # Use table instead
print(f"p-value: {p}")
if p < 0.05:
    print("Significant!")
```

## Extraction Process

### Step 1: Parse analysis.py Structure

Identify function boundaries and logical blocks:

```python
# analysis.py structure
def main():
    # Block 1: Data loading (lines 15-28)
    df = load_seasons(...)

    # Block 2: Data preparation (lines 30-45)
    filtered = df[...]

    # Block 3: Main analysis (lines 47-75)
    results = df.groupby(...)

    # Block 4: Statistical tests (lines 77-105)
    slope, intercept, r, p, se = stats.linregress(...)

    # Block 5: Visualization (lines 107-135)
    fig, ax = plt.subplots(...)
```

### Step 2: Match Content Plan to Code

For each code insertion point in content plan:

```yaml
content_section: "getting_started"
required_code_type: "data_loading"
analysis_py_lines: "15-28"
```

### Step 3: Extract and Clean

```python
# Original (lines 15-28)
print("Loading Statcast data...")
df = load_seasons(2015, 2025, columns=[
    'game_year', 'pitch_type', 'release_speed', 'release_spin_rate'
])
print(f"Loaded {len(df):,} pitches")
print(df.head())  # Debug

# After extraction (cleaned)
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=[
    'game_year', 'pitch_type', 'release_speed', 'release_spin_rate'
])

print(f"Total pitches: {len(df):,}")
```

### Step 4: Add Context Comments

Add brief comments that explain what the code does:

```python
# Load 11 seasons of Statcast data
df = load_seasons(2015, 2025, columns=[
    'game_year', 'pitch_type', 'release_speed'
])

# Filter to fastballs only
fastballs = df[df['pitch_type'] == 'FF']

# Calculate yearly averages
yearly_avg = fastballs.groupby('game_year')['release_speed'].mean()
```

## Extraction Rules

### ALWAYS Include

- Import statements for used libraries
- Variable assignments that are referenced
- Function calls that produce results
- One meaningful output per block (final result)

### ALWAYS Exclude

| Pattern | Reason |
|---------|--------|
| `print("Loading...")` | Progress messages |
| `print(df.head())` | Debug inspection |
| `time.time()` | Timing code |
| `# TODO:` comments | Development notes |
| `.to_csv('temp.csv')` | Intermediate saves |
| `try/except` with pass | Error suppression |
| Commented-out code | Dead code |

### Transform These

| Original | Transformed |
|----------|-------------|
| `print(f"Result: {x}")` | `print(f"Average velocity: {x:.1f} mph")` |
| `df.head()` | Remove or use in markdown table |
| Multiple print statements | Single summary output |

## Output Format

For each content section, produce:

```yaml
section_id: "getting_started"
code_block: |
  from statcast_analysis import load_seasons

  df = load_seasons(2015, 2025, columns=[
      'game_year', 'pitch_type', 'release_speed'
  ])

  print(f"Total pitches: {len(df):,}")
output_description: "Displays total pitch count"
execution_note: "Requires statcast_analysis package and data files"
```

## Example Extraction

### Input: analysis.py (excerpt)

```python
def main():
    print("=== Velocity Trend Analysis ===")
    print("Loading data...")

    df = load_seasons(2015, 2025, columns=[
        'game_year', 'pitch_type', 'release_speed'
    ])
    print(f"Loaded {len(df):,} rows")
    print(df.head())

    # Filter to fastballs
    ff = df[df['pitch_type'] == 'FF']
    print(f"Fastballs: {len(ff):,}")

    # Calculate yearly average
    yearly = ff.groupby('game_year')['release_speed'].mean()
    print("Yearly averages:")
    print(yearly)

    # Save results
    yearly.to_csv('results/velocity_by_year.csv')
    print("Saved to CSV")
```

### Output: Extracted Code Blocks

**Block 1: Data Loading**
```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=[
    'game_year', 'pitch_type', 'release_speed'
])

print(f"Total pitches: {len(df):,}")
```

**Block 2: Analysis**
```python
# Filter to four-seam fastballs
fastballs = df[df['pitch_type'] == 'FF']

# Calculate yearly average velocity
yearly_velocity = fastballs.groupby('game_year')['release_speed'].mean()
print(yearly_velocity.round(2))
```

## Validation Checklist

Before passing to Report Converter:

- [ ] All code blocks are syntactically valid Python
- [ ] Required imports are included
- [ ] Variables used are defined in the block or prior blocks
- [ ] No debug print statements remain
- [ ] Each block has a clear, single purpose
- [ ] Output statements produce meaningful results
- [ ] Comments explain non-obvious operations
