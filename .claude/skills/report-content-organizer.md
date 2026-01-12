# Report Content Organizer

Structures report content by analyzing actual results and defining narrative flow with code insertion points.

## Trigger

Use when planning the structure of a chapter report before writing.

Keywords: organize content, plan report, structure chapter, content outline

## Purpose

This skill creates a structured content plan based on ACTUAL analysis results, not placeholder data. It defines:
- Section headings and narrative flow
- Where executable code should be inserted
- What figures/tables to include
- Statistical validation requirements

## Input Requirements

Before using this skill, you MUST have:

1. **Completed analysis.py** in `chapters/XX_topic/`
2. **Generated results** in `chapters/XX_topic/results/`
3. **Generated figures** in `chapters/XX_topic/figures/`

## Output: Content Plan Document

Create a structured plan in this format:

```yaml
# content_plan.yaml (conceptual - output as structured text)

chapter: XX
title: "Chapter Title"
topic: "brief topic description"

sections:
  - id: hook
    type: narrative
    purpose: "Opening hook - present the question/mystery"
    data_reference: null
    code_insertion: false

  - id: getting_started
    type: code_showcase
    purpose: "Show data loading and initial exploration"
    data_reference: "analysis.py lines 10-25"
    code_insertion: true
    code_type: "data_loading"

  - id: main_analysis_1
    type: analysis
    purpose: "Primary finding presentation"
    data_reference: "results/summary.csv"
    code_insertion: true
    code_type: "calculation"
    figure: "fig01_xxx.png"
    table_data: true

  - id: statistical_validation
    type: validation
    purpose: "Confirm findings are statistically significant"
    data_reference: "results/statistical_tests.csv"
    code_insertion: true
    code_type: "statistical_test"
    required_tests:
      - t_test
      - effect_size
      - confidence_interval

  - id: what_we_learned
    type: summary
    purpose: "Key takeaways in numbered list"
    code_insertion: false
    bullet_points: 6

  - id: try_it_yourself
    type: exercise
    purpose: "Reader engagement"
    code_insertion: true
    code_type: "execution_command"
```

## Process

### Step 1: Inventory Available Assets

```python
# Check what exists
chapters/XX_topic/
├── analysis.py          # Source of executable code
├── results/
│   ├── summary.csv      # Main findings
│   ├── yearly_data.csv  # Time series data
│   └── statistical_tests.csv  # Validation results
└── figures/
    ├── fig01_xxx.png    # Primary visualization
    └── fig02_xxx.png    # Secondary visualization
```

### Step 2: Read Results Files

Extract actual values from CSV files:
- Key metrics and their values
- Year-over-year changes
- Statistical test results (p-values, effect sizes)

### Step 3: Define Section Structure

Map content to ABDWR flow:

| Section | Content Type | Code Needed |
|---------|--------------|-------------|
| Opening | Narrative hook | None |
| Getting Started | Data loading demo | data_load block |
| Primary Analysis | Results + narrative | calculation block |
| Visualization | Figure + interpretation | plotting block |
| Statistical Validation | Tests + interpretation | stats block |
| Summary | Key findings | None |
| Try It Yourself | Execution guide | run commands |

### Step 4: Identify Code Blocks Needed

For each code insertion point, specify:

```yaml
code_block:
  section: "getting_started"
  purpose: "Load Statcast data"
  source_file: "analysis.py"
  source_lines: "15-28"
  must_include:
    - load_seasons function call
    - column specification
  must_exclude:
    - print statements (except final result)
    - debugging code
    - timing code
  expected_output: "DataFrame shape display"
```

## Content Flow Rules

### ABDWR Style Requirements

1. **Hook First**: Start with an interesting question or observation
2. **Show Don't Tell**: Code demonstrates before text explains
3. **Exploration Flow**: Present discovery journey, not just results
4. **Statistical Rigor**: Always validate with proper tests
5. **Practical Ending**: Show readers how to run it themselves

### Code Insertion Guidelines

| Code Type | Location | Purpose |
|-----------|----------|---------|
| data_loading | Early | Show how to access data |
| exploration | After loading | Initial data inspection |
| calculation | Main analysis | Core metric computation |
| visualization | With figures | How figure was created |
| statistical_test | Validation section | Significance testing |
| run_command | End | How to execute full analysis |

## Example Content Plan Output

```markdown
## Content Plan: Chapter 03 - Pitch Type Evolution

### Available Assets
- analysis.py: 145 lines
- results/pitch_type_by_year.csv: 11 years × 8 pitch types
- results/statistical_tests.csv: trend tests
- figures/fig01_pitch_mix.png: stacked area chart
- figures/fig02_sweeper_rise.png: sweeper emergence

### Section Breakdown

1. **Opening Hook** (no code)
   - Question: "What happened to the fastball?"
   - Use: 2015 vs 2025 fastball % comparison

2. **Getting Started** (code: lines 12-22)
   - Data loading example
   - Filter to pitch_type column
   - Show sample counts

3. **Pitch Mix Analysis** (code: lines 35-52)
   - Group by year and pitch_type
   - Calculate percentages
   - Include fig01_pitch_mix.png
   - Table: pitch_type_by_year.csv summary

4. **The Sweeper Emergence** (code: lines 65-78)
   - Filter ST/SL pitch types
   - Year-over-year change
   - Include fig02_sweeper_rise.png

5. **Statistical Validation** (code: lines 95-115)
   - Linear regression on fastball decline
   - t-test: 2015-2017 vs 2022-2024
   - Effect size interpretation

6. **What We Learned** (no code)
   - 6 bullet points from findings

7. **Try It Yourself** (run commands only)
   - cd chapters/03_pitch_type
   - python analysis.py
```

## Validation Checklist

Before passing to Code Extractor:

- [ ] All results files read and values extracted
- [ ] All figures identified and captioned
- [ ] Code insertion points mapped to analysis.py lines
- [ ] Statistical tests identified for validation section
- [ ] No placeholder data used - all values from actual results
- [ ] ABDWR flow maintained (hook → explore → analyze → validate → summarize)
