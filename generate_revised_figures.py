import os
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs('figures/revised', exist_ok=True)

# Load data
df_k = pd.read_csv('data/processed/processed_kharif.csv')
df_r = pd.read_csv('data/processed/processed_rabi.csv')
df_s = pd.read_csv('data/processed/processed_seasonal.csv')

df_k['Season_Group'] = 'Kharif'
df_r['Season_Group'] = 'Rabi'
df_s['Season_Group'] = 'Seasonal'
df_all = pd.concat([df_k, df_r, df_s], ignore_index=True)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# Figure 1: Dataset Composition
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)
season_counts = df_all['Season_Group'].value_counts()
colors = ['#3b82f6', '#10b981', '#f59e0b']
ax1.pie(season_counts, labels=[f'{k}\n({v:,} records)' for k, v in season_counts.items()],
        autopct='%1.1f%%', startangle=140, colors=colors, explode=(0.04, 0.04, 0.04),
        textprops={'fontsize': 9, 'fontweight': 'bold'})
ax1.set_title('(a) Relative Record Share by Season', fontsize=10, fontweight='bold', pad=10)

bars = ax2.bar(season_counts.index, season_counts.values, color=colors, width=0.55, edgecolor='#334155')
ax2.set_ylabel('Total Number of Records', fontsize=10, fontweight='bold')
ax2.set_title('(b) Absolute Sample Count', fontsize=10, fontweight='bold', pad=10)
for bar in bars:
    y = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, y + 150, f'{int(y):,}', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax2.set_ylim(0, 8000)
plt.suptitle('Figure 1: Dataset Composition Across Kharif, Rabi, and Seasonal Agricultural Regimes (N = 13,130)', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('figures/revised/fig01_dataset_composition.png', bbox_inches='tight')
plt.close()

# Figure 2: Crop Distribution
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
crop_counts = df_all['Item'].value_counts()
colors_crops = sns.color_palette('tab10', len(crop_counts))
bars = ax.barh(crop_counts.index[::-1], crop_counts.values[::-1], color=colors_crops[::-1], edgecolor='#334155', height=0.65)
ax.set_xlabel('Number of Historical Harvest Records (1990–2013)', fontsize=10, fontweight='bold')
ax.set_title('Figure 2: Representation of Agricultural Crops Across the Consolidated Global Dataset', fontsize=11, fontweight='bold', pad=12)
for bar in bars:
    w = bar.get_width()
    ax.text(w + 50, bar.get_y() + bar.get_height()/2, f'{int(w):,}', ha='left', va='center', fontsize=8.5, fontweight='bold')
ax.set_xlim(0, 4800)
plt.tight_layout()
plt.savefig('figures/revised/fig02_crop_distribution.png', bbox_inches='tight')
plt.close()

# Figure 3: Yield Distribution
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
for grp, col in zip(['Kharif', 'Rabi', 'Seasonal'], ['#3b82f6', '#10b981', '#f59e0b']):
    sns.kdeplot(df_all[df_all['Season_Group'] == grp]['hg/ha_yield'], ax=ax, label=f'{grp} Season', color=col, fill=True, alpha=0.35, linewidth=2)
ax.set_xlabel('Crop Yield (hg/ha, where 1 hg/ha = 0.1 kg/ha)', fontsize=10, fontweight='bold')
ax.set_ylabel('Probability Density', fontsize=10, fontweight='bold')
ax.set_title('Figure 3: Density Distribution of Historical Crop Yield Across Seasonal Regimes', fontsize=11, fontweight='bold', pad=12)
ax.set_xlim(0, 400000)
ax.legend(frameon=True, loc='upper right')
plt.tight_layout()
plt.savefig('figures/revised/fig03_yield_distribution.png', bbox_inches='tight')
plt.close()

# Figure 4: Yield Over Time
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
yearly = df_all.groupby(['Year', 'Season_Group'])['hg/ha_yield'].mean().reset_index()
for grp, col, marker in zip(['Kharif', 'Rabi', 'Seasonal'], ['#3b82f6', '#10b981', '#f59e0b'], ['o', 's', '^']):
    sub = yearly[yearly['Season_Group'] == grp]
    ax.plot(sub['Year'], sub['hg/ha_yield'], marker=marker, label=f'{grp} Mean Yield', color=col, linewidth=2, markersize=5)
ax.axvline(2012.5, color='#dc2626', linestyle='--', linewidth=1.8, label='Prospective 2013 Holdout Split')
ax.set_xlabel('Calendar Year', fontsize=10, fontweight='bold')
ax.set_ylabel('Mean Yield (hg/ha)', fontsize=10, fontweight='bold')
ax.set_title('Figure 4: Historical Crop Yield Trajectory Over Time (1990–2013)', fontsize=11, fontweight='bold', pad=12)
ax.legend(frameon=True, loc='upper left')
plt.tight_layout()
plt.savefig('figures/revised/fig04_yield_over_time.png', bbox_inches='tight')
plt.close()

# Figure 5: Rainfall vs Yield
fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=300)
sns.scatterplot(data=df_all, x='average_rain_fall_mm_per_year', y='hg/ha_yield', hue='Season_Group',
                palette={'Kharif': '#3b82f6', 'Rabi': '#10b981', 'Seasonal': '#f59e0b'}, alpha=0.45, s=25, ax=ax)
# Add polynomial trend line
x_vals = df_all['average_rain_fall_mm_per_year'].values
y_vals = df_all['hg/ha_yield'].values
valid_idx = ~np.isnan(x_vals) & ~np.isnan(y_vals)
poly = np.poly1d(np.polyfit(x_vals[valid_idx], y_vals[valid_idx], 2))
x_grid = np.linspace(x_vals[valid_idx].min(), x_vals[valid_idx].max(), 200)
ax.plot(x_grid, poly(x_grid), color='#1e293b', linestyle='--', linewidth=2.2, label='Polynomial Trend Fit')
ax.set_xlabel('Average Annual Rainfall (mm/year)', fontsize=10, fontweight='bold')
ax.set_ylabel('Crop Yield (hg/ha)', fontsize=10, fontweight='bold')
ax.set_title('Figure 5: Bivariate Relationship Between Annual Rainfall and Crop Yield', fontsize=11, fontweight='bold', pad=12)
ax.legend(frameon=True, loc='upper right')
plt.tight_layout()
plt.savefig('figures/revised/fig05_rainfall_vs_yield.png', bbox_inches='tight')
plt.close()

# Figure 6: Temperature vs Yield
fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=300)
sns.scatterplot(data=df_all, x='avg_temp', y='hg/ha_yield', hue='Season_Group',
                palette={'Kharif': '#3b82f6', 'Rabi': '#10b981', 'Seasonal': '#f59e0b'}, alpha=0.45, s=25, ax=ax)
x_vals = df_all['avg_temp'].values
valid_idx = ~np.isnan(x_vals) & ~np.isnan(y_vals)
poly = np.poly1d(np.polyfit(x_vals[valid_idx], y_vals[valid_idx], 2))
x_grid = np.linspace(x_vals[valid_idx].min(), x_vals[valid_idx].max(), 200)
ax.plot(x_grid, poly(x_grid), color='#1e293b', linestyle='--', linewidth=2.2, label='Thermal Response Trend Fit')
ax.set_xlabel('Average Atmospheric Temperature (°C)', fontsize=10, fontweight='bold')
ax.set_ylabel('Crop Yield (hg/ha)', fontsize=10, fontweight='bold')
ax.set_title('Figure 6: Thermal Growing Conditions vs. Crop Yield Showing Agronomic Optimum', fontsize=11, fontweight='bold', pad=12)
ax.legend(frameon=True, loc='upper right')
plt.tight_layout()
plt.savefig('figures/revised/fig06_temperature_vs_yield.png', bbox_inches='tight')
plt.close()

# Figure 7: Pesticides vs Yield
fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=300)
sns.scatterplot(data=df_all, x='pesticides_tonnes', y='hg/ha_yield', hue='Season_Group',
                palette={'Kharif': '#3b82f6', 'Rabi': '#10b981', 'Seasonal': '#f59e0b'}, alpha=0.45, s=25, ax=ax)
ax.set_xscale('log')
ax.set_xlabel('National Pesticide Application (Tonnes, Logarithmic Scale)', fontsize=10, fontweight='bold')
ax.set_ylabel('Crop Yield (hg/ha)', fontsize=10, fontweight='bold')
ax.set_title('Figure 7: Chemical Crop Protection Intensity vs. Harvested Yield', fontsize=11, fontweight='bold', pad=12)
ax.legend(frameon=True, loc='upper left')
plt.tight_layout()
plt.savefig('figures/revised/fig07_pesticides_vs_yield.png', bbox_inches='tight')
plt.close()

# Figure 8: Correlation Heatmap
fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=300)
num_cols = ['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp', 'hg/ha_yield']
rename_cols = ['Year', 'Rainfall (mm)', 'Pesticides (t)', 'Avg Temp (°C)', 'Yield (hg/ha)']
corr = df_all[num_cols].corr()
corr.columns = rename_cols
corr.index = rename_cols
sns.heatmap(corr, annot=True, fmt='.3f', cmap='coolwarm', cbar=True, square=True,
            annot_kws={'size': 9, 'fontweight': 'bold'}, ax=ax, vmin=-0.4, vmax=1.0)
ax.set_title('Figure 8: Pairwise Pearson Correlation Heatmap Across Numerical Agricultural Features', fontsize=11, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig('figures/revised/fig08_correlation_heatmap.png', bbox_inches='tight')
plt.close()

# Figure 9: Model comparison
shutil.copy('figures/evaluation/07_tuned_model_comparison.png', 'figures/revised/fig09_model_comparison.png')

# Figure 10: Actual vs predicted values
shutil.copy('figures/evaluation/08_actual_vs_predicted_parity.png', 'figures/revised/fig10_actual_vs_predicted.png')

# Figure 11: Final cross-season performance
shutil.copy('figures/10_final_model_performance.png', 'figures/revised/fig11_final_cross_season_performance.png')

# Figure 12: System architecture
shutil.copy('figures/11_system_architecture_diagram.png', 'figures/revised/fig12_system_architecture.png')

print('All 12 figures successfully created and linked in figures/revised/!')
