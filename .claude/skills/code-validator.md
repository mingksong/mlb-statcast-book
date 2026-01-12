# Code Validator

Validates that chapter analysis scripts run correctly and produce expected outputs.

## Trigger

Use when verifying that chapter code is complete and reproducible.

Keywords: validate, test, verify, check code, run analysis, reproducibility

## Validation Steps

### Step 1: Pre-run Checks

Before running analysis, verify:

```bash
# Check that required files exist
ls chapters/XX_topic/analysis.py

# Check that data directory has required files
ls data/raw/statcast_*.parquet

# Check that output directories exist (or will be created)
```

### Step 2: Run Analysis

Execute the analysis script and capture output:

```bash
cd chapters/XX_topic
python analysis.py
```

**Expected behavior:**
- Script runs without errors
- Progress messages are printed
- Execution completes with "Analysis complete!" message

### Step 3: Verify Outputs

After running, check that all expected files were created:

```bash
# Check figures
ls -la chapters/XX_topic/figures/
# Should contain: fig01_*.png, fig02_*.png, etc.

# Check results
ls -la chapters/XX_topic/results/
# Should contain: *.csv files

# Verify file sizes are non-zero
find chapters/XX_topic/figures -name "*.png" -size +0
find chapters/XX_topic/results -name "*.csv" -size +0
```

### Step 4: Content Verification

Verify output quality:

```python
# Check CSV has expected columns and rows
import pandas as pd
df = pd.read_csv('chapters/XX_topic/results/main_results.csv')
print(f"Rows: {len(df)}, Columns: {list(df.columns)}")

# Verify no NaN in critical columns
assert df['year'].notna().all(), "Missing year values"

# Check figure file sizes (should be > 10KB)
import os
for fig in os.listdir('chapters/XX_topic/figures'):
    size = os.path.getsize(f'chapters/XX_topic/figures/{fig}')
    assert size > 10000, f"{fig} is too small ({size} bytes)"
```

### Step 5: Reproducibility Test

Run the analysis again and verify outputs match:

```bash
# Save hashes of current outputs
md5sum chapters/XX_topic/results/*.csv > /tmp/before.md5

# Re-run analysis
python chapters/XX_topic/analysis.py

# Compare hashes
md5sum chapters/XX_topic/results/*.csv > /tmp/after.md5
diff /tmp/before.md5 /tmp/after.md5
# Should show no differences (or explain any expected differences)
```

## Common Issues & Solutions

### Issue: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'statcast_analysis'
```

**Solution**: Ensure the script adds project root to path:
```python
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
```

### Issue: FileNotFoundError (data)

```
FileNotFoundError: data/raw/statcast_2024.parquet not found
```

**Solution**: Run data collector:
```bash
python collector/collect_statcast.py --year 2024
```

### Issue: Empty DataFrame

**Solution**: Check filters are not too restrictive:
```python
print(f"Before filter: {len(df)}")
filtered = df[df['pitch_type'] == 'FF']
print(f"After filter: {len(filtered)}")
```

### Issue: Figure not saved

**Solution**: Ensure directories exist:
```python
FIGURES_DIR = Path(__file__).parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)
```

### Issue: Memory error

**Solution**: Load data in chunks or use column filtering:
```python
# Only load needed columns
df = load_season(2024, columns=['pitch_type', 'release_speed'])
```

## Validation Checklist

Complete validation requires all items checked:

### Code Quality
- [ ] Script runs without errors
- [ ] No deprecation warnings
- [ ] Execution time is reasonable (< 5 minutes typical)
- [ ] Memory usage is acceptable

### Output Completeness
- [ ] All expected figures generated
- [ ] All expected CSV files created
- [ ] Figure file sizes > 10KB
- [ ] CSV files have expected columns

### Reproducibility
- [ ] Re-running produces identical results
- [ ] No hardcoded paths (uses relative paths)
- [ ] Random seeds set if randomness used

### Documentation Alignment
- [ ] README lists correct output files
- [ ] Book chapter references correct figures
- [ ] Summary statistics match printed output

## Batch Validation Script

For validating all chapters at once:

```python
#!/usr/bin/env python3
"""Validate all chapter analyses."""
import subprocess
import sys
from pathlib import Path

CHAPTERS_DIR = Path(__file__).parent.parent / "chapters"

def validate_chapter(chapter_dir: Path) -> bool:
    """Run and validate a single chapter."""
    analysis_py = chapter_dir / "analysis.py"
    if not analysis_py.exists():
        print(f"  SKIP: {chapter_dir.name} (no analysis.py)")
        return True

    print(f"\n  Validating: {chapter_dir.name}")
    result = subprocess.run(
        [sys.executable, str(analysis_py)],
        capture_output=True,
        text=True,
        cwd=chapter_dir
    )

    if result.returncode != 0:
        print(f"  FAIL: {chapter_dir.name}")
        print(result.stderr)
        return False

    # Check outputs exist
    figures_dir = chapter_dir / "figures"
    results_dir = chapter_dir / "results"

    if not list(figures_dir.glob("*.png")):
        print(f"  WARN: {chapter_dir.name} - no figures generated")

    if not list(results_dir.glob("*.csv")):
        print(f"  WARN: {chapter_dir.name} - no results generated")

    print(f"  PASS: {chapter_dir.name}")
    return True


def main():
    chapters = sorted(CHAPTERS_DIR.iterdir())
    passed = 0
    failed = 0

    for chapter in chapters:
        if chapter.is_dir() and not chapter.name.startswith('.'):
            if validate_chapter(chapter):
                passed += 1
            else:
                failed += 1

    print(f"\n{'='*60}")
    print(f"  Results: {passed} passed, {failed} failed")
    print(f"{'='*60}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
```

Save this as `scripts/validate_code.py` and run with:
```bash
python scripts/validate_code.py
```
