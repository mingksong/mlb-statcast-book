# Figure Generator

Creates publication-ready visualizations for MLB Statcast book chapters.

## Trigger

Use when creating or improving visualizations for analysis chapters.

Keywords: figure, visualization, plot, chart, graph, create figure

## Standards

All figures must meet these requirements:

### Technical Specifications

- **Resolution**: 150 DPI minimum
- **Format**: PNG
- **Size**: Standard `(10, 6)`, Large `(12, 8)`, Small `(8, 5)`
- **Font**: Default matplotlib (readable at all sizes)

### Required Elements

1. **Title**: Descriptive, includes time period if relevant
2. **Axis Labels**: Clear units (mph, %, count, etc.)
3. **Legend**: When multiple series present
4. **Grid**: Light grid for readability (seaborn whitegrid)

### Naming Convention

```
fig01_main_topic.png
fig02_secondary_topic.png
fig03_comparison.png
```

## Plot Types & Templates

### 1. Time Series Trend

```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['year'], df['value'], 'o-', linewidth=2, markersize=8, color='#1f77b4')
ax.fill_between(df['year'], df['value'] - df['std'], df['value'] + df['std'], alpha=0.2)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Metric (units)', fontsize=12)
ax.set_title('Metric Trend Over Time (2015-2025)', fontsize=14)
ax.set_xlim(2014.5, 2025.5)

# Add start/end annotations
ax.annotate(f"{df.iloc[0]['value']:.1f}", (df.iloc[0]['year'], df.iloc[0]['value']),
            textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)
ax.annotate(f"{df.iloc[-1]['value']:.1f}", (df.iloc[-1]['year'], df.iloc[-1]['value']),
            textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'fig01_trend.png', dpi=150)
plt.close()
```

### 2. Bar Chart (Yearly Comparison)

```python
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df['year'], df['value'], color='#ff7f0e', edgecolor='black', linewidth=0.5)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Percentage (%)', fontsize=12)
ax.set_title('Metric by Year', fontsize=14)

# Add value labels
for bar, val in zip(bars, df['value']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'fig02_bars.png', dpi=150)
plt.close()
```

### 3. Distribution Comparison (Histogram)

```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(data_before, bins=50, alpha=0.6, label='2015', density=True, color='#1f77b4')
ax.hist(data_after, bins=50, alpha=0.6, label='2025', density=True, color='#ff7f0e')
ax.axvline(data_before.mean(), color='#1f77b4', linestyle='--', linewidth=2)
ax.axvline(data_after.mean(), color='#ff7f0e', linestyle='--', linewidth=2)
ax.set_xlabel('Value (units)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Distribution Shift: Before vs After', fontsize=14)
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'fig03_distribution.png', dpi=150)
plt.close()
```

### 4. Scatter Plot with Regression

```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df['x'], df['y'], alpha=0.5, s=20)

# Add regression line
z = np.polyfit(df['x'], df['y'], 1)
p = np.poly1d(z)
ax.plot(df['x'].sort_values(), p(df['x'].sort_values()),
        'r--', linewidth=2, label=f'R² = {r2:.3f}')

ax.set_xlabel('X Metric', fontsize=12)
ax.set_ylabel('Y Metric', fontsize=12)
ax.set_title('X vs Y Relationship', fontsize=14)
ax.legend()

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'fig04_scatter.png', dpi=150)
plt.close()
```

### 5. Heatmap (Pitch Location / Zone Analysis)

```python
fig, ax = plt.subplots(figsize=(10, 8))
heatmap = ax.imshow(matrix, cmap='RdYlBu_r', aspect='auto')
plt.colorbar(heatmap, ax=ax, label='Value')

ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels)
ax.set_yticks(range(len(y_labels)))
ax.set_yticklabels(y_labels)

ax.set_xlabel('X Category', fontsize=12)
ax.set_ylabel('Y Category', fontsize=12)
ax.set_title('Heatmap Analysis', fontsize=14)

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'fig05_heatmap.png', dpi=150)
plt.close()
```

### 6. Multi-panel Figure

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Panel A
axes[0, 0].plot(...)
axes[0, 0].set_title('A) First Panel')

# Panel B
axes[0, 1].bar(...)
axes[0, 1].set_title('B) Second Panel')

# Panel C
axes[1, 0].scatter(...)
axes[1, 0].set_title('C) Third Panel')

# Panel D
axes[1, 1].hist(...)
axes[1, 1].set_title('D) Fourth Panel')

plt.tight_layout()
plt.savefig(FIGURES_DIR / 'fig06_multipanel.png', dpi=150)
plt.close()
```

## Color Palette

Use consistent colors throughout the book:

```python
# Primary palette (seaborn husl)
COLORS = {
    'primary': '#1f77b4',    # Blue
    'secondary': '#ff7f0e',  # Orange
    'tertiary': '#2ca02c',   # Green
    'quaternary': '#d62728', # Red
    'accent': '#9467bd',     # Purple
}

# Year-based gradient
import matplotlib.cm as cm
colors = cm.viridis(np.linspace(0, 1, len(years)))

# Pitch type colors
PITCH_COLORS = {
    'FF': '#e41a1c',  # Red - 4-seam
    'SI': '#377eb8',  # Blue - Sinker
    'FC': '#4daf4a',  # Green - Cutter
    'SL': '#984ea3',  # Purple - Slider
    'CU': '#ff7f00',  # Orange - Curveball
    'CH': '#ffff33',  # Yellow - Changeup
}
```

## Quality Checklist

Before saving any figure:

- [ ] Title is descriptive and includes time period
- [ ] Axis labels include units
- [ ] Legend is positioned clearly (if needed)
- [ ] Font sizes are readable (12pt minimum for labels)
- [ ] Colors are distinguishable
- [ ] Grid is subtle but helpful
- [ ] `tight_layout()` applied
- [ ] Saved at 150 DPI minimum
- [ ] File named following convention
