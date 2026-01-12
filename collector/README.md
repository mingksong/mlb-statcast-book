# Data Collector

Scripts for collecting MLB Statcast data from Baseball Savant.

## Usage

```bash
# Collect 2024 season (~700K pitches, ~5-10 minutes)
python collect_statcast.py --year 2024

# Collect specific month (~120K pitches, ~30 seconds)
python collect_statcast.py --year 2024 --month 5

# Collect multiple seasons
python collect_statcast.py --range 2015 2025

# List collected data
python collect_statcast.py --list
```

## Data Storage

Data is saved as Parquet files in `data/raw/`:
- `statcast_2024.parquet` - Full season
- `statcast_2024_05.parquet` - Single month

## Supported Seasons

- 2015-2025 (11 seasons)
- 2020 is a shortened season (COVID-19)

## Data Volume

| Season | Pitches | Size |
|--------|---------|------|
| 2024 | ~710K | ~65 MB |
| 2015-2025 | ~7.4M | ~750 MB |
