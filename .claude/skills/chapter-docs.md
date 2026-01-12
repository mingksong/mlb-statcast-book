# Chapter Documentation Writer

Creates documentation for MLB Statcast book chapters in two formats: GitHub README and Book Chapter.

## Trigger

Use when writing or updating chapter documentation.

Keywords: documentation, readme, chapter markdown, write docs, book chapter

## Two-Tier Documentation System

Each chapter requires TWO documents:

### Tier 1: GitHub README (`chapters/XX_topic/README.md`)

**Purpose**: Technical reference for developers who want to understand and run the code.

**Length**: 1-2 pages

**Template**:

```markdown
# Chapter XX: [Title]

## Summary

[2-3 sentence description of what this chapter analyzes]

## Key Findings

1. **[Finding 1 headline]**
   - [Supporting detail]
   - [Supporting detail]

2. **[Finding 2 headline]**
   - [Supporting detail]
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

## Methodology

1. [Step 1 description]
2. [Step 2 description]
3. [Step 3 description]
4. [Step 4 description]

## Output

### Figures

- `fig01_xxx.png`: [Description]
- `fig02_xxx.png`: [Description]
- `fig03_xxx.png`: [Description]

### Results

- `results.csv`: [Description of columns]
- `summary.csv`: [Description]
```

---

### Tier 2: Book Chapter (`book/partX_category/chXX_topic.md`)

**Purpose**: Narrative content for readers, suitable for PDF publication.

**Length**: 5-10 pages

**Template**:

```markdown
# [Chapter Title]

## Key Findings

- **[Headline 1]**: [One-line summary]
- **[Headline 2]**: [One-line summary]
- **[Headline 3]**: [One-line summary]

---

## The Story

[Opening paragraph that hooks the reader. Ask a question or present an interesting observation.]

[Historical context paragraph. How did things used to be?]

[The change paragraph. What shifted and when?]

[The impact paragraph. Why does this matter for baseball?]

---

## The Analysis

### Data Overview

We analyzed [X million] pitches from [YYYY] to [YYYY], focusing on [specific aspect].

### Methodology

[Explain the approach in plain language]

```python
# Key code snippet (simplified for book)
# Show the essential logic, not boilerplate
df = load_season(2024)
fastballs = df[df['pitch_type'] == 'FF']
avg_velocity = fastballs['release_speed'].mean()
```

### Results

[Explain what the analysis revealed]

---

## Visualizations

### [Figure 1 Title]

![Figure 1](../../chapters/XX_topic/figures/fig01_xxx.png)

[Caption explaining what the figure shows and key takeaways]

### [Figure 2 Title]

![Figure 2](../../chapters/XX_topic/figures/fig02_xxx.png)

[Caption]

---

## Discussion

### What This Means

[Interpretation for baseball context]

### Limitations

[Acknowledge any caveats]

### Future Questions

[What else could be explored]

---

## Try It Yourself

Full analysis code available at:
```
github.com/mingksong/mlb-statcast-book/chapters/XX_topic/
```

Run it:
```bash
cd chapters/XX_topic
python analysis.py
```
```

## Writing Style Guidelines

### For GitHub README

- Technical and concise
- Focus on reproducibility
- Include all commands needed
- List exact file dependencies
- Use bullet points and tables

### For Book Chapter

- Conversational but authoritative
- Tell a story, don't just report facts
- Explain WHY findings matter
- Use analogies for complex concepts
- Include historical context
- Keep code snippets short (5-15 lines)
- Explain code in surrounding text

## Key Phrases to Use

### Opening hooks

- "In 2015, the average fastball was [X]. Today, it's [Y]."
- "What separates elite pitchers from the rest?"
- "The data reveals a surprising trend..."
- "Every baseball fan has noticed that..."

### Transitions

- "To understand this change, we need to look at..."
- "The data tells a clear story..."
- "This finding has significant implications..."
- "Looking deeper into the numbers..."

### Conclusions

- "These findings suggest that..."
- "For teams looking to..."
- "The trajectory is clear: ..."
- "As the game continues to evolve..."

## Chapter-Specific Content

Each chapter should address:

1. **What?** - The specific metric or trend being analyzed
2. **When?** - Time period and key inflection points
3. **How much?** - Quantified changes (percentages, raw numbers)
4. **Why?** - Possible explanations (training, strategy, technology)
5. **So what?** - Implications for players, teams, fans
