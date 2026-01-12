# MLB Statcast Analytics Book: Research Plan

**Version**: 1.0
**Data Coverage**: 2015-2025 MLB Statcast (11 seasons, 7.4M+ pitches)
**Target**: 45 chapters across 5 parts

---

## Data Availability Summary

| Metric Category | Coverage | Notes |
|-----------------|----------|-------|
| Pitch basics (type, speed, location) | 99%+ | All years |
| Spin rate / movement | 99%+ | All years |
| Exit velocity / launch angle | ~33% | In-play events only |
| Bat tracking (bat speed) | ~45% | **2023+ only** |
| Release point / arm angle | 99%+ | Arm angle 2020+ |
| Defense alignment (shift) | 99%+ | All years |

### Key Technical Discovery

**PA-Level Aggregation**: `PA_KEY = game_pk + at_bat_number`

Enables K%, BB%, HR% calculations at plate appearance level.

---

## Part I: Getting Started (2 chapters)

| Ch | Title | Status | Description |
|----|-------|--------|-------------|
| 00 | Introduction | DRAFT | Book overview and structure |
| 01 | Understanding Statcast Data | PENDING | Data dictionary and methodology |

---

## Part II: Pitching Analysis (13 chapters)

| Ch | Title | Status | Key Columns | Notes |
|----|-------|--------|-------------|-------|
| 02 | The Velocity Arms Race | **DONE** | release_speed | 10-year velocity trend |
| 03 | Pitch Type Evolution | **GO** | pitch_type | Sweeper emergence, pitch mix changes |
| 04 | Spin Rate Trends | **GO** | release_spin_rate | Historical spin analysis |
| 05 | Movement Analysis | **GO** | pfx_x, pfx_z | Horizontal/vertical break patterns |
| 06 | L/R Pitcher Differences | **GO** | p_throws | Handedness patterns |
| 07 | Count-Based Pitch Selection | **GO** | balls, strikes, pitch_type | Strategy by count |
| 08 | Velocity/Spin Decay by Inning | **GO** | inning, release_speed, spin | Fatigue analysis |
| 09 | Pitcher Arsenal Diversity | **GO** | pitch_type per pitcher | Multi-pitch repertoire |
| 10 | First Pitch Strategy | **GO** | pitch_number=1 | Opening pitch patterns |
| 11 | Tunneling Effect Analysis | **PARTIAL** | release_pos, plate_pos | Complex 3D calculation |
| 12 | Pitch Effectiveness by Type | **GO** | woba_value, pitch_type | wOBA/BA by pitch |
| 13 | Release Point Consistency | **GO** | release_pos_x/y/z | Deception analysis |
| 14 | Pitch Clock Effect (2023+) | **GO** | game_year | Pre/post 2023 comparison |

**Required columns**: release_speed, release_spin_rate, pitch_type, pfx_x, pfx_z, p_throws, balls, strikes, inning, release_pos_x/y/z, plate_x, plate_z, woba_value

---

## Part III: Batting Analysis (11 chapters)

| Ch | Title | Status | Key Columns | Notes |
|----|-------|--------|-------------|-------|
| 15 | Exit Velocity Revolution | **GO** | launch_speed | EV trend analysis |
| 16 | Launch Angle Transformation | **GO** | launch_angle | Fly ball revolution |
| 17 | Barrel Rate Leaderboard | **GO** | launch_speed, launch_angle | Optimal batted balls |
| 18 | Hard Hit Rate Analysis | **GO** | launch_speed >= 95 | Power metrics |
| 19 | Sweet Spot Rate Trends | **GO** | launch_angle 8-32° | Ideal contact |
| 20 | Count-Based Batting Success | **GO** | balls, strikes, events | Hitter's vs pitcher's counts |
| 21 | xBA vs Actual BA Gap | **GO** | estimated_ba, events | Luck analysis |
| 22 | Batting Success by Pitch Type | **GO** | pitch_type, events | What pitches get hit |
| 23 | Strikeout Rate Trends | **GO** | PA aggregation | K% over time |
| 24 | Clutch Hitting Analysis | **GO** | on_1b/2b/3b, outs_when_up | High-leverage situations |
| 25 | Bat Speed Analysis (2024+) | **PARTIAL** | bat_speed | 2023+ only, limited coverage |

**Required columns**: launch_speed, launch_angle, estimated_ba, events, description, balls, strikes, on_1b, on_2b, on_3b, outs_when_up, bat_speed (2023+)

---

## Part IV: Game Management (8 chapters)

| Ch | Title | Status | Key Columns | Notes |
|----|-------|--------|-------------|-------|
| 26 | Starter Innings Trend | **GO** | pitcher, inning | Innings per start decline |
| 27 | Bullpen Usage Patterns | **GO** | pitcher changes | Relief strategy evolution |
| 28 | Pitcher Change Timing | **GO** | pitcher, inning, outs | When managers act |
| 29 | Run Scoring by Inning | **GO** | inning, post_bat_score | When runs happen |
| 30 | Lead Situation Win Rate | **GO** | score differential | Comeback probability |
| 31 | 3-Ball Walk/Swing Rate | **GO** | balls=3, description | Full count strategy |
| 32 | Extra Innings Rule Effect | **GO** | inning >= 10, runner | Manfred runner analysis |
| 33 | Catcher Framing Analysis | **GO** | plate_x, plate_z, description | Strike zone manipulation |

**Required columns**: pitcher, batter, inning, outs_when_up, post_bat_score, post_away_score, description, plate_x, plate_z

---

## Part V: League Trends (7 chapters)

| Ch | Title | Status | Key Columns | Notes |
|----|-------|--------|-------------|-------|
| 34 | Home Run Trends | **GO** | events='home_run' | HR rate analysis |
| 35 | Offense/Pitching Cycle | **GO** | runs, ERA derivable | League-wide balance |
| 36 | Team Offensive Styles | **GO** | home_team, metrics | Team identity |
| 37 | AL vs NL Differences | **GO** | league derivable | DH impact analysis |
| 38 | Park Factors | **GO** | home_team, events | Venue effects |
| 39 | Complete Game Decline | **GO** | pitcher innings | CG rarity |
| 40 | Game Duration Trends | **GO** | pitch counts | Pace of play |

**Required columns**: game_pk, game_year, home_team, away_team, events, post_bat_score

---

## NOT Feasible Topics (Excluded)

These topics require data not available in pitch-level Statcast:

| Original # | Topic | Missing Data | Alternative Source |
|------------|-------|--------------|-------------------|
| 28 | OAA Analysis | Defensive metrics | Savant Leaderboard |
| 30 | Pop Time | Catcher arm metrics | Savant Leaderboard |
| 31 | Sprint Speed | Running metrics | Savant Leaderboard |
| 33 | OF Jump/Route | Route efficiency | Savant Leaderboard |
| 35 | Shift Ban Effect | Positioning details | Limited analysis only |

---

## Research Priority Order

### Phase 1: Foundation Chapters (Ch 02-08)
Core Statcast metrics with strong data coverage:
- Velocity, Spin Rate, Pitch Types, Movement

### Phase 2: Batting Revolution (Ch 15-19)
Exit velocity and launch angle era:
- EV trends, LA transformation, Barrel rates

### Phase 3: Strategic Insights (Ch 20-25, 26-33)
Count-based analysis and game management:
- Situational hitting, bullpen strategy, framing

### Phase 4: Big Picture (Ch 34-40)
League-wide trends and conclusions:
- HR trends, park factors, era comparison

---

## Statistical Validation Requirements

Each chapter analysis must include:

### 1. Descriptive Statistics
- Mean, median, standard deviation
- Percentiles (10th, 25th, 75th, 90th)
- Sample sizes with confidence thresholds

### 2. Trend Analysis
- Year-over-year change rates
- Linear regression with R² values
- Confidence intervals (95%)

### 3. Comparison Tests
- Two-sample t-tests (before/after periods)
- Effect size (Cohen's d)
- Statistical significance (p < 0.05)

### 4. Data Quality Checks
- Missing value percentages
- Outlier detection (>3 SD)
- Sample size adequacy

---

## Chapter File Structure

```
chapters/XX_topic_name/
├── README.md           # Methodology & findings
├── analysis.py         # Main analysis script
├── figures/            # Generated visualizations
│   ├── fig01_*.png
│   └── fig02_*.png
└── results/            # Output data
    ├── main_results.csv
    └── summary.csv
```

---

## Quick Reference: Key Statcast Columns

| Column | Type | Description |
|--------|------|-------------|
| pitch_type | str | FF, SI, FC, SL, CU, CH, etc. |
| release_speed | float | Pitch velocity (mph) |
| release_spin_rate | int | Spin rate (rpm) |
| pfx_x | float | Horizontal movement (in) |
| pfx_z | float | Vertical movement (in) |
| plate_x | float | Horizontal location (ft) |
| plate_z | float | Vertical location (ft) |
| launch_speed | float | Exit velocity (mph) |
| launch_angle | float | Launch angle (degrees) |
| events | str | PA outcome (single, home_run, etc.) |
| description | str | Pitch outcome (called_strike, etc.) |
| game_pk | int | Unique game ID |
| at_bat_number | int | PA number within game |

---

*Last Updated: 2025-01-12*
