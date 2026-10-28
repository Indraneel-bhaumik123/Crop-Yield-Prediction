import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

os.makedirs('figures/faculty_revision', exist_ok=True)

# Set high-DPI academic styling
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 12

# 1. Load Data
df_k = pd.read_csv('data/processed/processed_kharif.csv')
df_r = pd.read_csv('data/processed/processed_rabi.csv')
df_s = pd.read_csv('data/processed/processed_seasonal.csv')
df_k['Season'] = 'Kharif'
df_r['Season'] = 'Rabi'
df_s['Season'] = 'Seasonal'
df_all = pd.concat([df_k, df_r, df_s], ignore_index=True)

# -------------------------------------------------------------------------
# Figure F1: Flowchart of Whole Study (Methodology Pipeline)
# -------------------------------------------------------------------------
print("Generating Flowchart of Whole Study...")
fig, ax = plt.subplots(figsize=(11, 2.6), dpi=300)
ax.axis('off')

boxes = [
    ("1. Data Ingestion\n13,130 Records (1990-2013)\n101 Sovereign Nations\nData Hygiene Audits", "#1E3A8A"),
    ("2. Season Stratification\nKharif (N = 4,404)\nRabi (N = 1,810)\nSeasonal (N = 6,916)", "#0284C7"),
    ("3. Leak-Free Preproc.\nOne-Hot Encoding\nStandardScaler on Numerics\nFitted Strictly on Train", "#0D9488"),
    ("4. Chronological Split\nTrain: 1990-2012 (95.5%)\nHoldout: 2013 (4.5%)\nZero Temporal Leakage", "#16A34A"),
    ("5. Model Benchmarking\n5 Models x 3 Seasons\nTime-Aware 3-Fold CV\nKNN, XGB, GBR, MLP, LR", "#D97706"),
    ("6. System Deployment\nFastAPI REST Microservice\nJWT Auth & SQLite DB\nInteractive Web Portal", "#4F46E5")
]

x_start = 0.015
box_width = 0.138
spacing = 0.030
y_box = 0.12
box_height = 0.76

from matplotlib.patches import FancyBboxPatch

for i, (text, color) in enumerate(boxes):
    x = x_start + i * (box_width + spacing)
    rect = FancyBboxPatch((x, y_box), box_width, box_height, facecolor=color, edgecolor='#0F172A',
                          linewidth=1.2, transform=ax.transAxes, zorder=2, boxstyle="round,pad=0.015")
    ax.add_patch(rect)
    ax.text(x + box_width/2, y_box + box_height/2, text, transform=ax.transAxes,
            ha='center', va='center', color='white', fontsize=7.2, fontweight='bold', zorder=3,
            linespacing=1.25)
    
    # Arrow to next box
    if i < len(boxes) - 1:
        arrow_x = x + box_width
        arrow_dx = spacing
        ax.annotate('', xy=(arrow_x + arrow_dx - 0.003, y_box + box_height/2),
                    xytext=(arrow_x + 0.003, y_box + box_height/2),
                    xycoords='axes fraction', textcoords='axes fraction',
                    arrowprops=dict(arrowstyle="-|>", color='#334155', lw=1.8, mutation_scale=12), zorder=4)

plt.tight_layout()
fig.savefig('figures/faculty_revision/fig_flowchart_whole_study.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------------------
# Figure F2: Violin / Box Plot of Yield Distribution Across Seasons (Section 6.1)
# -------------------------------------------------------------------------
print("Generating Violin/Box Plot of Yield Distribution...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)

palette = {'Kharif': '#10B981', 'Rabi': '#3B82F6', 'Seasonal': '#F59E0B'}

# Subplot 1: Violin plot
sns.violinplot(x='Season', y='hg/ha_yield', data=df_all, ax=ax1, palette=palette, cut=0, inner='quartile')
ax1.set_title('(a) Kernel Density & Interquartile Ranges', fontweight='bold')
ax1.set_ylabel('Crop Yield (hg/ha, 10,000 hg/ha = 1 t/ha)')
ax1.set_xlabel('Agricultural Season Cohort')
ax1.grid(True, linestyle='--', alpha=0.5)

# Subplot 2: Box plot with log scale for clear visibility of outliers
sns.boxplot(x='Season', y='hg/ha_yield', data=df_all, ax=ax2, palette=palette, width=0.45, fliersize=2.5)
ax2.set_yscale('log')
ax2.set_title('(b) Boxplot with Outlier Diagnostics (Log Scale)', fontweight='bold')
ax2.set_ylabel('Crop Yield (log10 hg/ha)')
ax2.set_xlabel('Agricultural Season Cohort')
ax2.grid(True, linestyle='--', alpha=0.5, which='both')

plt.tight_layout()
fig.savefig('figures/faculty_revision/fig_yield_distribution_violin_box.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------------------
# Figure F3: Random Split vs Chronological Evaluation (Section 6.6)
# -------------------------------------------------------------------------
print("Generating Random vs Chronological Comparison Figure...")
with open('results/faculty_revision/random_vs_chronological_all.json') as f:
    rand_chrono_data = json.load(f)

df_rc = pd.DataFrame(rand_chrono_data)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)

# Filter for Kharif as primary benchmark
df_rc_k = df_rc[df_rc['Season'] == 'Kharif']
models_order = ['KNN', 'XGBoost', 'Gradient Boosting', 'MLP', 'Linear Regression']
df_rc_k = df_rc_k.set_index('Model').reindex(models_order).reset_index()

x = np.arange(len(models_order))
w = 0.35

# Panel A: RMSE Comparison
ax1.bar(x - w/2, df_rc_k['Chrono_RMSE'], w, label='Chronological Holdout (2013)', color='#1E40AF', edgecolor='black')
ax1.bar(x + w/2, df_rc_k['Random_RMSE'], w, label='Random 80/20 Partition', color='#93C5FD', edgecolor='black')
ax1.set_xticks(x)
ax1.set_xticklabels(['KNN', 'XGB', 'GBR', 'MLP', 'LR'], rotation=0)
ax1.set_ylabel('RMSE (hg/ha)')
ax1.set_title('(a) Generalization RMSE Comparison (Kharif)', fontweight='bold')
ax1.legend(loc='upper left', frameon=True)
ax1.grid(True, linestyle='--', alpha=0.4, axis='y')

# Panel B: R² Comparison
ax2.bar(x - w/2, df_rc_k['Chrono_R2'], w, label='Chronological Holdout (2013)', color='#065F46', edgecolor='black')
ax2.bar(x + w/2, df_rc_k['Random_R2'], w, label='Random 80/20 Partition', color='#6EE7B7', edgecolor='black')
ax2.set_xticks(x)
ax2.set_xticklabels(['KNN', 'XGB', 'GBR', 'MLP', 'LR'], rotation=0)
ax2.set_ylabel('Coefficient of Determination (R²)')
ax2.set_title('(b) Explanatory Power R² Comparison (Kharif)', fontweight='bold')
ax2.set_ylim(0.5, 1.0)
ax2.legend(loc='lower left', frameon=True)
ax2.grid(True, linestyle='--', alpha=0.4, axis='y')

plt.tight_layout()
fig.savefig('figures/faculty_revision/fig_random_vs_chronological_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------------------
# Figure F4: Neighbor Distance vs Absolute Error (Section 6.9)
# -------------------------------------------------------------------------
print("Generating Neighbor Distance vs Absolute Error Scatter & Fit...")
with open('results/faculty_revision/neighbor_metrics.json') as f:
    neigh_data = json.load(f)

# Recompute distance vs error points for Kharif test set
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline

train_k = df_k[df_k['Year'] <= 2012].reset_index(drop=True)
test_k = df_k[df_k['Year'] == 2013].reset_index(drop=True)
feature_cols = ['Area', 'Continent', 'Item', 'Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']
cat_cols = ['Area', 'Continent', 'Item']
num_cols = ['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']

pipe_k = Pipeline([
    ('preprocessor', ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols),
        ('num', StandardScaler(), num_cols)
    ])),
    ('regressor', KNeighborsRegressor(n_neighbors=3, p=2, weights='distance'))
])
pipe_k.fit(train_k[feature_cols], train_k['hg/ha_yield'])
pre_k = pipe_k.named_steps['preprocessor']
reg_k = pipe_k.named_steps['regressor']
X_test_k = pre_k.transform(test_k[feature_cols])
dists_k, _ = reg_k.kneighbors(X_test_k)
preds_k = pipe_k.predict(test_k[feature_cols])
errs_k = np.abs(test_k['hg/ha_yield'].values - preds_k)
mean_dists_k = np.mean(dists_k, axis=1)

r_k = neigh_data['metrics']['Kharif']['pearson_r_dist_vs_error']
p_k = neigh_data['metrics']['Kharif']['r_p_value']
ci_k = neigh_data['metrics']['Kharif']['r_95_CI']

fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)
sns.regplot(x=mean_dists_k, y=errs_k, ax=ax, color='#1E40AF',
            scatter_kws={'alpha': 0.65, 's': 30, 'edgecolor': 'white'},
            line_kws={'color': '#DC2626', 'linewidth': 2.0})

ax.set_title('Historical-Neighbor Distance vs. Absolute Prediction Error (Kharif 2013 Holdout)', fontweight='bold')
ax.set_xlabel('Mean Euclidean Distance to k=3 Neighbors (Normalized Feature Space)')
ax.set_ylabel('Absolute Prediction Error |y - ŷ| (hg/ha)')
ax.grid(True, linestyle='--', alpha=0.5)

# Annotation text box
text_str = f"Pearson r = +{r_k:.4f}\np-value = {p_k:.4f}\n95% CI: [{ci_k[0]:.4f}, {ci_k[1]:.4f}]\nN = {len(test_k)} holdout records"
props = dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC', edgecolor='#94A3B8', alpha=0.9)
ax.text(0.04, 0.94, text_str, transform=ax.transAxes, fontsize=9, verticalalignment='top', bbox=props)

plt.tight_layout()
fig.savefig('figures/faculty_revision/fig_neighbor_distance_vs_error.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------------------
# Figure F5: 2D Rainfall x Temperature Response Surface (Section 6.11)
# -------------------------------------------------------------------------
print("Generating Rainfall x Temperature Response Surface...")
rain_grid = np.linspace(df_all['average_rain_fall_mm_per_year'].min(), df_all['average_rain_fall_mm_per_year'].max(), 100)
temp_grid = np.linspace(df_all['avg_temp'].min(), df_all['avg_temp'].max(), 100)
R_mesh, T_mesh = np.meshgrid(rain_grid, temp_grid)

# Bivariate interaction regression surface from Kharif
with open('results/faculty_revision/feature_interaction.json') as f:
    inter_data = json.load(f)

k_params = inter_data['Kharif']
Z_mesh = (k_params['b0_const'] + 
          k_params['b1_rain'] * R_mesh + 
          k_params['b2_temp'] * T_mesh + 
          k_params['b3_interaction'] * (R_mesh * T_mesh))

fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
cp = ax.contourf(R_mesh, T_mesh, Z_mesh, levels=25, cmap='YlGnBu')
cbar = fig.colorbar(cp)
cbar.set_label('Estimated Crop Yield (hg/ha)', rotation=270, labelpad=15)

# Overlay scatter of actual observations
ax.scatter(df_k['average_rain_fall_mm_per_year'], df_k['avg_temp'], c='#D97706', s=8, alpha=0.35, label='Kharif Observations')

# Optimal thermal envelope lines
ax.axhline(12, color='#DC2626', linestyle='--', alpha=0.7, label='Optimal Thermal Window (12°C–22°C)')
ax.axhline(22, color='#DC2626', linestyle='--', alpha=0.7)

ax.set_title('Rainfall × Temperature Yield Response Surface with Interaction', fontweight='bold')
ax.set_xlabel('Annual Precipitation (mm/year)')
ax.set_ylabel('Mean Atmospheric Temperature (°C)')
ax.legend(loc='lower right', frameon=True, fontsize=8)
ax.grid(True, linestyle=':', alpha=0.4)

plt.tight_layout()
fig.savefig('figures/faculty_revision/fig_rainfall_temperature_response_surface.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------------------
# Figure F6: Redesigned Model Performance with 95% CIs (Section 6.3 - Figure 9 replacement)
# -------------------------------------------------------------------------
print("Generating Model Performance Dot Plot with 95% CIs...")
with open('results/faculty_revision/prospective_performance_with_ci.json') as f:
    perf_ci_data = json.load(f)

df_pci = pd.DataFrame(perf_ci_data)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)

seasons = ['Kharif', 'Rabi', 'Seasonal']
season_colors = {'Kharif': '#059669', 'Rabi': '#2563EB', 'Seasonal': '#D97706'}
markers = {'KNN': 'o', 'XGBoost': 's', 'Gradient Boosting': '^', 'MLP': 'D', 'Linear Regression': 'v'}

# Panel A: RMSE with error bars
for s in seasons:
    sub = df_pci[df_pci['Season'] == s].sort_values('Rank')
    y_pos = np.arange(len(sub)) + (seasons.index(s) - 1) * 0.22
    err_lower = sub['RMSE'] - sub['RMSE_CI_lower']
    err_upper = sub['RMSE_CI_upper'] - sub['RMSE']
    ax1.errorbar(sub['RMSE'], y_pos, xerr=[err_lower, err_upper], fmt='o',
                 color=season_colors[s], label=s, capsize=4, capthick=1.2, elinewidth=1.2, markersize=6)

ax1.set_yticks(np.arange(5))
ax1.set_yticklabels(['Rank 1 (KNN)', 'Rank 2 (XGB)', 'Rank 3 (GBR/LR)', 'Rank 4 (MLP/GBR)', 'Rank 5 (LR/MLP)'])
ax1.set_xlabel('RMSE (hg/ha, 95% Bootstrap CI)')
ax1.set_title('(a) Model Prospective Error Ranking (RMSE)', fontweight='bold')
ax1.legend(loc='lower right', frameon=True)
ax1.grid(True, linestyle='--', alpha=0.5)

# Panel B: R² with error bars
for s in seasons:
    sub = df_pci[df_pci['Season'] == s].sort_values('Rank')
    y_pos = np.arange(len(sub)) + (seasons.index(s) - 1) * 0.22
    err_lower = sub['R2'] - sub['R2_CI_lower']
    err_upper = sub['R2_CI_upper'] - sub['R2']
    ax2.errorbar(sub['R2'], y_pos, xerr=[err_lower, err_upper], fmt='s',
                 color=season_colors[s], label=s, capsize=4, capthick=1.2, elinewidth=1.2, markersize=6)

ax2.set_yticks(np.arange(5))
ax2.set_yticklabels(['Rank 1 (KNN)', 'Rank 2 (XGB)', 'Rank 3 (GBR/LR)', 'Rank 4 (MLP/GBR)', 'Rank 5 (LR/MLP)'])
ax2.set_xlabel('Coefficient of Determination R² (95% Bootstrap CI)')
ax2.set_title('(b) Explanatory Fidelity Ranking (R²)', fontweight='bold')
ax2.set_xlim(0.5, 1.0)
ax2.legend(loc='lower left', frameon=True)
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
fig.savefig('figures/faculty_revision/fig_model_performance_with_ci.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------------------
# Figure F7: Enhanced Actual vs Predicted Parity Plots with Identity & Regression Fits
# -------------------------------------------------------------------------
print("Generating Enhanced Parity Plots...")
fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), dpi=300)

for i, (s_name, df_s_data, k_val, p_val, col_c) in enumerate([
    ('Kharif', df_k, 3, 2, '#059669'),
    ('Rabi', df_r, 7, 1, '#2563EB'),
    ('Seasonal', df_s, 3, 1, '#D97706')
]):
    tr = df_s_data[df_s_data['Year'] <= 2012].reset_index(drop=True)
    te = df_s_data[df_s_data['Year'] == 2013].reset_index(drop=True)
    
    pipe = Pipeline([
        ('preprocessor', ColumnTransformer([
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols),
            ('num', StandardScaler(), num_cols)
        ])),
        ('regressor', KNeighborsRegressor(n_neighbors=k_val, p=p_val, weights='distance'))
    ])
    pipe.fit(tr[feature_cols], tr['hg/ha_yield'])
    y_obs = te['hg/ha_yield'].values
    y_pred = pipe.predict(te[feature_cols])
    
    ax = axes[i]
    # Scatter
    ax.scatter(y_obs, y_pred, color=col_c, alpha=0.7, s=28, edgecolors='white', linewidth=0.5, label='Holdout 2013')
    
    # 45-degree identity line
    max_val = max(np.max(y_obs), np.max(y_pred)) * 1.05
    min_val = min(np.min(y_obs), np.min(y_pred)) * 0.95
    ax.plot([min_val, max_val], [min_val, max_val], 'k--', lw=1.5, label='45° Identity Line')
    
    # Linear fit line
    slope, intercept, r_val, p_val, _ = stats.linregress(y_obs, y_pred)
    fit_x = np.linspace(min_val, max_val, 100)
    ax.plot(fit_x, intercept + slope * fit_x, color='#DC2626', lw=1.2, label='Fitted Trend')
    
    # Metrics
    rmse = np.sqrt(mean_squared_error(y_obs, y_pred))
    mae = mean_absolute_error(y_obs, y_pred)
    r2 = r2_score(y_obs, y_pred)
    
    ax.set_title(f'{s_name} Pipeline (N = {len(te)})', fontweight='bold')
    ax.set_xlabel('Observed Crop Yield (hg/ha)')
    if i == 0:
        ax.set_ylabel('KNN Predicted Crop Yield (hg/ha)')
    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)
    ax.grid(True, linestyle='--', alpha=0.4)
    
    stat_box = f"R² = {r2:.4f}\nRMSE = {rmse:,.1f}\nMAE = {mae:,.1f}"
    ax.text(0.05, 0.94, stat_box, transform=ax.transAxes, fontsize=8.5, verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#CBD5E1', alpha=0.9))
    if i == 0:
        ax.legend(loc='lower right', fontsize=7.5, frameon=True)

plt.tight_layout()
fig.savefig('figures/faculty_revision/fig_enhanced_actual_vs_predicted.png', dpi=300, bbox_inches='tight')
plt.close()

print("ALL FACULTY REVISED FIGURES SUCCESSFULLY GENERATED!")
