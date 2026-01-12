# Chapter 1: The Velocity Arms Race (2015-2025)

## Summary

This chapter analyzes the 10-year trend in MLB fastball velocity, documenting the so-called "velocity arms race" with Statcast data.

## Key Findings

1. **4-seam fastball velocity increased by 1.4 mph** over 10 years
   - 2015: 93.1 mph average
   - 2025: 94.5 mph average

2. **95+ mph fastballs became the norm**
   - 2015: 26% of 4-seamers
   - 2025: 43% of 4-seamers

3. **Acceleration point: 2021**
   - 2015-2020: Gradual increase (+0.3 mph / 5 years)
   - 2021-2025: Rapid increase (+1.1 mph / 4 years)

## Files

| File | Description |
|------|-------------|
| `analysis.py` | Main analysis script |
| `figures/` | Generated visualizations |
| `results/` | Output CSV files |

## Running the Analysis

```bash
cd chapters/01_velocity_trend
python analysis.py
```

## Data Requirements

- Requires: `data/raw/statcast_2015.parquet` through `statcast_2025.parquet`
- Collect with: `python collector/collect_statcast.py --range 2015 2025`

## Methodology

1. Load all pitch data from 2015-2025
2. Filter to 4-seam fastballs (pitch_type == 'FF')
3. Calculate yearly average velocity
4. Calculate 95+ mph percentage by year
5. Analyze velocity distribution changes
