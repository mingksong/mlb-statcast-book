# Chapter Documentation Writer

Orchestrates the report generation pipeline using three specialized sub-skills.

## Trigger

Use when writing or updating chapter documentation.

Keywords: documentation, readme, chapter markdown, write docs, book chapter

## Report Generation Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                REPORT GENERATION PIPELINE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PREREQUISITE: Analysis must be complete                        │
│  ├── analysis.py executed successfully                          │
│  ├── results/*.csv files generated                              │
│  └── figures/*.png files generated                              │
│                                                                  │
│  PHASE 1: CONTENT ORGANIZER                                     │
│  ├── Read results files to extract actual values                │
│  ├── Inventory available figures                                │
│  ├── Define section structure and flow                          │
│  ├── Mark code insertion points                                 │
│  └── Output: Content plan with data references                  │
│                                                                  │
│  PHASE 2: CODE EXTRACTOR                                        │
│  ├── Parse analysis.py to identify code blocks                  │
│  ├── Match blocks to content plan sections                      │
│  ├── Clean code (remove debug, add comments)                    │
│  └── Output: Executable code blocks for each section            │
│                                                                  │
│  PHASE 3: REPORT CONVERTER                                      │
│  ├── Merge content plan + extracted code                        │
│  ├── Insert actual values from results                          │
│  ├── Generate markdown tables from CSV                          │
│  ├── Apply ABDWR style formatting                               │
│  └── Output: Final markdown report                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Sub-Skills Reference

| Skill | File | Purpose |
|-------|------|---------|
| Content Organizer | `report-content-organizer.md` | Structure report, define sections |
| Code Extractor | `report-code-extractor.md` | Extract clean, executable code |
| Report Converter | `report-converter.md` | Generate final ABDWR markdown |

## Two-Tier Documentation System

Each chapter requires TWO documents:

### Tier 1: GitHub README (`chapters/XX_topic/README.md`)

**Purpose**: Technical reference for developers

**Process**: Standard template (see below)

### Tier 2: Book Chapter (`book/partX_category/chXX_topic.md`)

**Purpose**: ABDWR-style narrative for readers

**Process**: Use 3-phase pipeline above

---

## Tier 1: README Template

```markdown
# Chapter XX: [Title]

## Summary

[2-3 sentence description of what this chapter analyzes]

## Key Findings

1. **[Finding 1 headline]**
   - [Supporting detail]

2. **[Finding 2 headline]**
   - [Supporting detail]

3. **[Finding 3 headline]**
   - [Supporting detail]

## Files

| File | Description |
|------|-------------|
| `analysis.py` | Main analysis script |
| `figures/` | Generated visualizations |
| `results/` | Output CSV files |

## Running the Analysis

```bash
cd chapters/XX_topic
python analysis.py
```

## Data Requirements

- Requires: `data/raw/statcast_YYYY.parquet` (specify years)
- Collect with: `python collector/collect_statcast.py --range YYYY YYYY`

## Output

### Figures
- `fig01_xxx.png`: [Description]

### Results
- `results.csv`: [Description of columns]
```

---

## Tier 2: Book Chapter Pipeline

### Phase 1: Content Organization

**Input**: Completed analysis (results + figures)

**Actions**:
1. Read `results/summary.csv` - extract key metrics
2. Read `results/statistical_tests.csv` - extract validation data
3. List `figures/*.png` - identify visualizations
4. Define section structure:
   - Opening hook (no code)
   - Getting Started (data loading code)
   - Main analysis sections (calculation code + tables)
   - Visualization (figures)
   - Statistical validation (tests code)
   - Summary (no code)
   - Try it yourself (run commands)

**Output**: Section plan with actual values and code line references

### Phase 2: Code Extraction

**Input**: Content plan + analysis.py

**Actions**:
1. Parse analysis.py structure
2. For each code insertion point:
   - Extract relevant lines
   - Remove debug statements (`print("Loading...")`)
   - Remove timing code
   - Keep imports used in block
   - Keep one meaningful output per block
3. Add explanatory comments

**Output**: Clean code blocks keyed to sections

**Code Cleaning Rules**:

| Remove | Keep |
|--------|------|
| `print("Processing...")` | `print(f"Total: {n:,}")` (final result) |
| `.head()` for debugging | Actual calculations |
| `time.time()` timing | Statistical functions |
| `# TODO` comments | Explanatory `#` comments |
| Exception suppression | Core logic |

### Phase 3: Report Conversion

**Input**: Content plan + code blocks + results data

**Actions**:
1. Write opening hook using actual values
2. Insert code blocks at designated points
3. Convert CSV data to markdown tables
4. Reference figures with correct paths (`../../chapters/`)
5. Write interpretive narrative between code
6. Format statistical results with interpretation
7. Generate summary bullets from findings

**Output**: Complete ABDWR-style markdown

---

## Image Path Format

> **CRITICAL**: Book chapters are in `book/partX_category/`
> Images are in `chapters/XX_topic/figures/`
>
> Path requires TWO parent traversals:
> ```markdown
> ![Figure](../../chapters/XX_topic/figures/fig01_xxx.png)
> ```

---

## ABDWR Writing Style

### Structure Pattern

```markdown
# Chapter Title

[Opening hook - question or surprising fact]

In this chapter, we'll [explore/analyze] [topic].

## Getting Started

Let's [action]:

```python
[data loading code]
```

With [N] [records], we can [capability].

## [Analysis Section]

[Transition]

```python
[calculation code]
```

| Col1 | Col2 |
|------|------|
| data | data |

[Interpretation]

## Is This Real? Statistical Validation

```python
[statistics code]
```

| Test | Value | Meaning |
|------|-------|---------|

[Interpretation]

## What We Learned

1. **Finding 1**: Summary
2. **Finding 2**: Summary
...

## Try It Yourself

```bash
cd chapters/XX_topic
python analysis.py
```
```

### Voice Guidelines

| Do | Don't |
|----|-------|
| "Let's examine..." | "As you can see..." |
| "The data reveals..." | "Obviously..." |
| "Suppose we want to..." | "Now we will..." |
| State findings directly | Use hedging language |

---

## Execution Checklist

Before writing documentation:

- [ ] `analysis.py` runs without errors
- [ ] `results/*.csv` files exist with data
- [ ] `figures/*.png` files exist and are readable
- [ ] Statistical tests completed (p-values, effect sizes)

During Phase 1 (Content):
- [ ] Read all results files
- [ ] Extract actual numeric values
- [ ] Map sections to analysis.py line numbers
- [ ] Identify required code blocks

During Phase 2 (Code):
- [ ] Extract each required code block
- [ ] Remove all debug output
- [ ] Verify code is syntactically valid
- [ ] Add helpful comments

During Phase 3 (Report):
- [ ] Use actual values (no placeholders)
- [ ] Verify image paths (`../../chapters/`)
- [ ] Tables render correctly
- [ ] Narrative flows naturally
- [ ] Summary matches findings

---

## Quick Reference

### Part Assignments

| Part | Chapters | Directory |
|------|----------|-----------|
| II: Pitching | 02-14 | `book/part1_pitching/` |
| III: Batting | 15-25 | `book/part2_batting/` |
| IV: Game Mgmt | 26-33 | `book/part3_game_management/` |
| V: League Trends | 34-40 | `book/part4_league_trends/` |

### File Naming

- README: `chapters/XX_topic/README.md`
- Book chapter: `book/partN_category/chXX_topic.md`
- Figures: `chapters/XX_topic/figures/fig01_descriptor.png`
- Results: `chapters/XX_topic/results/summary.csv`
