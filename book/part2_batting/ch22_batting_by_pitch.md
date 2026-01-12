# Chapter 22: Batting Against the Arsenal

So far in this section, we've analyzed batting from the hitter's perspective—exit velocity, launch angle, contact quality. But hitting doesn't happen in a vacuum. Every swing is a response to a pitch. Some pitches are easier to hit than others.

In this chapter, we'll explore batting performance by pitch type and discover which pitches give hitters the most trouble.

## Getting Started

Let's begin by loading outcome data by pitch type:

```python
from statcast_analysis import load_seasons

df = load_seasons(2015, 2025, columns=['game_year', 'pitch_type', 'woba_value',
                                        'woba_denom', 'launch_speed', 'events'])

# Filter to plate appearances with outcomes
pa_data = df[df['woba_denom'] > 0]
pa_data = pa_data.dropna(subset=['pitch_type'])
print(f"Plate appearances by pitch: {len(pa_data):,}")
```

With nearly 2 million plate appearances categorized by pitch type, we can see exactly how hitters perform against each offering.

## The Hittability Hierarchy

Suppose we want to rank pitch types by how effectively hitters attack them:

```python
# Calculate wOBA by pitch type
pitch_woba = pa_data.groupby('pitch_type').apply(
    lambda x: x['woba_value'].sum() / x['woba_denom'].sum()
)
pitch_woba = pitch_woba.sort_values(ascending=False)
print(pitch_woba.round(3))
```

| Pitch Type | wOBA | Avg EV | Category |
|------------|------|--------|----------|
| Sinker (SI) | .363 | 89.2 mph | Fastball |
| 4-Seam (FF) | .355 | 90.3 mph | Fastball |
| Cutter (FC) | .335 | 87.3 mph | Fastball |
| Changeup (CH) | .302 | 85.9 mph | Offspeed |
| Slider (SL) | .287 | 86.8 mph | Breaking |
| Curveball (CU) | .282 | 86.8 mph | Breaking |
| Knuckle Curve (KC) | .273 | 88.0 mph | Breaking |
| Sweeper (ST) | .273 | 85.3 mph | Breaking |
| Splitter (FS) | .266 | 86.6 mph | Offspeed |

![wOBA by Pitch](../../chapters/22_batting_by_pitch/figures/fig01_woba_by_pitch.png)

The hierarchy is clear: fastballs are hittable, offspeed is tougher, breaking balls are hardest.

## Fastballs: The Hitters' Friend

Let's examine why fastballs are the most productive pitches for hitters:

```python
# Fastball analysis
fastballs = ['FF', 'SI', 'FC']
fb_data = pa_data[pa_data['pitch_type'].isin(fastballs)]

fb_woba = fb_data['woba_value'].sum() / fb_data['woba_denom'].sum()
fb_ev = fb_data[fb_data['launch_speed'].notna()]['launch_speed'].mean()

print(f"Fastball wOBA: {fb_woba:.3f}")
print(f"Fastball avg EV: {fb_ev:.1f} mph")
```

Fastballs produce higher wOBA (.345-.365) because:

1. **Predictable velocity**: Hitters know roughly when to swing
2. **Less movement**: Straighter paths are easier to track
3. **Higher exit velocity**: Ball coming in faster means ball goes out faster
4. **More count leverage**: Often thrown when hitter is ahead

## The Sinker Paradox

The sinker (.363 wOBA) being the most hittable pitch seems to contradict its purpose—it's supposed to produce weak contact. What's happening?

```python
# Sinker investigation
sinker = pa_data[pa_data['pitch_type'] == 'SI']
four_seam = pa_data[pa_data['pitch_type'] == 'FF']

print("Sinker vs 4-Seam:")
print(f"Sinker wOBA: {sinker['woba_value'].sum() / sinker['woba_denom'].sum():.3f}")
print(f"4-Seam wOBA: {four_seam['woba_value'].sum() / four_seam['woba_denom'].sum():.3f}")
```

The sinker paradox has several explanations:

1. **Sinkers are often belt-high**: The movement profile puts them in hittable zones
2. **Selection effects**: Sinkers thrown when pitcher needs strike
3. **Grounders ≠ outs**: Even weak ground balls sometimes find holes
4. **Exit velocity**: Hard grounders still produce hits

## The Splitter Dominance

At the other extreme, the splitter (.266 wOBA) is the hardest pitch to hit:

```python
# Splitter analysis
splitter = pa_data[pa_data['pitch_type'] == 'FS']

sp_woba = splitter['woba_value'].sum() / splitter['woba_denom'].sum()
print(f"Splitter wOBA: {sp_woba:.3f}")
print(f"Splitter events: {len(splitter):,}")
```

The splitter's dominance comes from:

1. **Deception**: Looks like fastball, drops at last moment
2. **Chase rate**: Generates swings out of zone
3. **Weak contact**: Even when hit, contact is often poor
4. **Late movement**: Hardest to adjust to

## The Breaking Ball Zone

Breaking balls cluster together in effectiveness:

```python
# Breaking ball analysis
breaking = ['SL', 'CU', 'ST', 'KC']
brk_data = pa_data[pa_data['pitch_type'].isin(breaking)]

brk_woba = brk_data['woba_value'].sum() / brk_data['woba_denom'].sum()
print(f"Breaking ball wOBA: {brk_woba:.3f}")
```

| Pitch | wOBA | Notes |
|-------|------|-------|
| Slider | .287 | Most common breaking ball |
| Curveball | .282 | Highest movement |
| Knuckle Curve | .273 | Combines curveball features |
| Sweeper | .273 | Horizontal break specialist |

Breaking balls are effective because they change the plane of attack. Instead of hitters timing straight lines, they must track curves—a much harder task.

## Exit Velocity by Pitch Type

Let's see if contact quality varies by pitch:

```python
# EV by pitch type
ev_by_pitch = pa_data[pa_data['launch_speed'].notna()].groupby('pitch_type')['launch_speed'].mean()
print(ev_by_pitch.round(1))
```

| Pitch | Avg Exit Velocity |
|-------|-------------------|
| 4-Seam (FF) | 90.3 mph |
| Sinker (SI) | 89.2 mph |
| Knuckle Curve | 88.0 mph |
| Cutter (FC) | 87.3 mph |
| Slider (SL) | 86.8 mph |
| Curveball (CU) | 86.8 mph |
| Splitter (FS) | 86.6 mph |
| Changeup (CH) | 85.9 mph |
| Sweeper (ST) | 85.3 mph |

Fastballs generate the hardest contact (90+ mph). Off-speed and breaking balls produce weaker contact (85-87 mph). This 4-5 mph gap translates to significant outcome differences.

## The Strategic Implication

This data explains pitching strategy:

```python
# Strategy connections
print("Why pitchers sequence this way:")
print()
print("1. Start with fastball (establish timing)")
print("2. Use breaking ball off fastball (change plane)")
print("3. Splitter/changeup as put-away (late movement)")
print()
print("The hitter's dilemma:")
print("- Sit fastball: Miss breaking balls")
print("- Look breaking: Late on fastball")
print("- Guess right: Success")
print("- Guess wrong: Failure")
```

This connects to our pitching chapters (3-14): pitch effectiveness is the mirror of batting effectiveness.

## What We Learned

Let's summarize what the data revealed:

1. **Sinker is most hittable**: .363 wOBA despite being a "pitch to contact"
2. **Splitter is hardest**: .266 wOBA, best put-away pitch
3. **Fastballs produce highest EV**: 90+ mph exit velocity
4. **Breaking balls cluster**: All in .273-.287 wOBA range
5. **Speed differential matters**: 4-5 mph EV gap between fastball and offspeed
6. **Pitching is cat-and-mouse**: Sequence matters as much as stuff

The batting-by-pitch analysis shows that hitting is fundamentally reactive. Hitters must respond to what pitchers throw, and some pitches simply give hitters less chance to succeed.

## Try It Yourself

The complete analysis code is available at:
`github.com/mingksong/mlb-statcast-book/chapters/22_batting_by_pitch/`

Try modifying the code to explore:
- How has batting against the splitter changed as usage increased?
- Which hitters are best against breaking balls?
- Is there a count-specific pattern to pitch hittability?

```bash
cd chapters/22_batting_by_pitch
python analysis.py
```
