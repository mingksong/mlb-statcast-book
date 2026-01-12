# Chapter Orchestrator

Orchestrates the complete chapter creation pipeline for the MLB Statcast Analytics Book.

## Trigger

Use this skill when the user wants to create a new chapter or complete an existing chapter analysis.

Keywords: create chapter, new chapter, research topic, analyze, chapter pipeline

## Workflow

Execute the following steps in order:

### Step 1: Topic Analysis & Data Assessment

1. Identify the research topic and chapter number
2. Determine required Statcast columns using `src/statcast_analysis/constants.py`
3. Verify data availability by checking `data/raw/` parquet files
4. Create the chapter directory structure:
   ```
   chapters/XX_topic_name/
   ├── README.md
   ├── analysis.py
   ├── figures/
   └── results/
   ```

### Step 2: Analysis Script Creation

Create `analysis.py` following this structure:

```python
#!/usr/bin/env python3
"""
Chapter XX: [Title]

[Description of the analysis]

Usage:
    python analysis.py
"""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from statcast_analysis import load_season, AVAILABLE_SEASONS

# Output directories
FIGURES_DIR = Path(__file__).parent / "figures"
RESULTS_DIR = Path(__file__).parent / "results"
FIGURES_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# Plot style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


def main():
    print("=" * 60)
    print(f"  Chapter XX: [Title]")
    print("=" * 60)

    # Step 1: Load and process data
    # Step 2: Calculate metrics
    # Step 3: Create visualizations
    # Step 4: Save results
    # Step 5: Print summary

    print("\n[DONE] Analysis complete!")


if __name__ == "__main__":
    main()
```

### Step 3: Run Analysis & Validate

1. Execute: `python chapters/XX_topic/analysis.py`
2. Verify all figures are generated in `figures/`
3. Verify all results are saved in `results/`
4. Check for any errors or warnings

### Step 4: Documentation

Create two documents:

**A. GitHub README.md** (`chapters/XX_topic/README.md`):
- Summary of findings
- Methodology explanation
- File listing
- Running instructions
- Data requirements

**B. Book Chapter** (`book/partX_category/chXX_topic.md`):
- Key Findings (bullet points)
- The Story (narrative for general audience)
- The Analysis (code snippets with explanations)
- Visualizations (embedded figures)
- Try It Yourself (link to GitHub)

### Step 5: Final Validation

1. Run `python chapters/XX_topic/analysis.py` again to confirm reproducibility
2. Verify all links and references are correct
3. Check figures are publication-ready (proper labels, legends, resolution)

## Output Checklist

Before marking chapter complete, verify:

- [ ] `chapters/XX_topic/analysis.py` runs without errors
- [ ] `chapters/XX_topic/figures/` contains all visualizations
- [ ] `chapters/XX_topic/results/` contains output CSVs
- [ ] `chapters/XX_topic/README.md` is complete
- [ ] `book/partX_category/chXX_topic.md` is complete
- [ ] Code has English comments
- [ ] All figures have proper titles and labels

## Example Usage

User: "Create chapter 5 about spin rate trends"

Response:
1. Create `chapters/05_spin_rate/` structure
2. Write `analysis.py` using spin rate columns (release_spin_rate, spin_axis)
3. Generate trend visualizations
4. Write documentation
5. Validate and commit
