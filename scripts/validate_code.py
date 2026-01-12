#!/usr/bin/env python3
"""
Validate All Chapter Analyses

Runs each chapter's analysis.py and verifies outputs are generated correctly.

Usage:
    python scripts/validate_code.py           # Validate all chapters
    python scripts/validate_code.py 01        # Validate specific chapter
"""
import subprocess
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CHAPTERS_DIR = PROJECT_ROOT / "chapters"


def validate_chapter(chapter_dir: Path, verbose: bool = False) -> dict:
    """
    Run and validate a single chapter.

    Returns:
        dict with keys: name, status, figures, results, error
    """
    result = {
        'name': chapter_dir.name,
        'status': 'UNKNOWN',
        'figures': 0,
        'results': 0,
        'error': None
    }

    analysis_py = chapter_dir / "analysis.py"
    if not analysis_py.exists():
        result['status'] = 'SKIP'
        result['error'] = 'No analysis.py found'
        return result

    print(f"\n  Running: {chapter_dir.name}/analysis.py")

    # Run the analysis
    proc = subprocess.run(
        [sys.executable, str(analysis_py)],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        timeout=300  # 5 minute timeout
    )

    if proc.returncode != 0:
        result['status'] = 'FAIL'
        result['error'] = proc.stderr[-500:] if proc.stderr else 'Unknown error'
        if verbose:
            print(f"    STDERR: {proc.stderr}")
        return result

    # Check outputs
    figures_dir = chapter_dir / "figures"
    results_dir = chapter_dir / "results"

    if figures_dir.exists():
        figures = list(figures_dir.glob("*.png"))
        result['figures'] = len(figures)

        # Verify file sizes
        for fig in figures:
            if fig.stat().st_size < 1000:  # Less than 1KB is suspicious
                result['status'] = 'WARN'
                result['error'] = f'{fig.name} is suspiciously small'

    if results_dir.exists():
        csvs = list(results_dir.glob("*.csv"))
        result['results'] = len(csvs)

    if result['status'] != 'WARN':
        result['status'] = 'PASS'

    return result


def main():
    parser = argparse.ArgumentParser(description='Validate chapter analyses')
    parser.add_argument('chapter', nargs='?', help='Specific chapter number (e.g., 01)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    print("=" * 60)
    print("  MLB Statcast Book - Code Validation")
    print("=" * 60)

    results = []

    if args.chapter:
        # Validate specific chapter
        matches = list(CHAPTERS_DIR.glob(f"{args.chapter}*"))
        if not matches:
            print(f"  ERROR: No chapter matching '{args.chapter}' found")
            return 1
        chapters = matches
    else:
        # Validate all chapters
        chapters = sorted([d for d in CHAPTERS_DIR.iterdir()
                          if d.is_dir() and not d.name.startswith('.')])

    for chapter_dir in chapters:
        try:
            result = validate_chapter(chapter_dir, verbose=args.verbose)
            results.append(result)

            status_symbol = {
                'PASS': '\u2713',  # checkmark
                'FAIL': '\u2717',  # X
                'WARN': '!',
                'SKIP': '-'
            }.get(result['status'], '?')

            print(f"  [{status_symbol}] {result['name']}: {result['status']}")
            if result['status'] == 'PASS':
                print(f"      Figures: {result['figures']}, Results: {result['results']}")
            elif result['error']:
                print(f"      Error: {result['error'][:100]}")

        except subprocess.TimeoutExpired:
            results.append({
                'name': chapter_dir.name,
                'status': 'TIMEOUT',
                'figures': 0,
                'results': 0,
                'error': 'Execution exceeded 5 minutes'
            })
            print(f"  [T] {chapter_dir.name}: TIMEOUT")

        except Exception as e:
            results.append({
                'name': chapter_dir.name,
                'status': 'ERROR',
                'figures': 0,
                'results': 0,
                'error': str(e)
            })
            print(f"  [E] {chapter_dir.name}: ERROR - {e}")

    # Summary
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] in ('FAIL', 'ERROR', 'TIMEOUT'))
    warned = sum(1 for r in results if r['status'] == 'WARN')
    skipped = sum(1 for r in results if r['status'] == 'SKIP')

    print("\n" + "=" * 60)
    print(f"  Summary: {passed} passed, {failed} failed, {warned} warnings, {skipped} skipped")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
