import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs('figures/revised', exist_ok=True)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# -------------------------------------------------------------
# Figure 13: KNN Neighborhood Distance, Dispersion and Sensitivity
# -------------------------------------------------------------
with open('results/advanced/neighbor_analysis.json', 'r') as f:
    neigh_data = json.load(f)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), dpi=300)

seasons = ['Kharif', 'Rabi', 'Seasonal']
metrics = neigh_data['neighborhood_metrics']
mean_dists = [metrics[s]['mean_neighbor_distance'] for s in seasons]
std_dists = [metrics[s]['std_neighbor_distance'] for s in seasons]
corr_dist = [metrics[s]['corr_distance_vs_abs_error'] for s in seasons]
corr_disp = [metrics[s]['corr_neighbor_dispersion_vs_abs_error'] for s in seasons]

x = np.arange(len(seasons))
width = 0.35

# Panel (a): Mean Neighbor Distance
bars1 = ax1.bar(x, mean_dists, yerr=std_dists, capsize=5, color=['#3b82f6', '#10b981', '#f59e0b'], edgecolor='#334155', width=0.5)
ax1.set_ylabel('Mean Neighbor Distance in Scaled Space', fontsize=10, fontweight='bold')
ax1.set_title('(a) Average Distance to k-Nearest Historical Neighbors', fontsize=11, fontweight='bold', pad=10)
ax1.set_xticks(x)
ax1.set_xticklabels([f'{s}\n({s=="Rabi" and "k=7, p=1" or "k=3, p=" + str(s=="Kharif" and 2 or 1)})' for s in seasons], fontsize=9)
for bar in bars1:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, h + 0.05, f'{h:.3f}', ha='center', va='bottom', fontsize=8.5, fontweight='bold')

# Panel (b): Correlation with Prediction Error
bars2 = ax2.bar(x - width/2, corr_dist, width, label='Distance vs Error Corr', color='#6366f1')
bars3 = ax2.bar(x + width/2, corr_disp, width, label='Neighbor Yield Dispersion vs Error', color='#ec4899')
ax2.set_ylabel('Pearson Correlation Coefficient (r)', fontsize=10, fontweight='bold')
ax2.set_title('(b) Correlation of Neighbor Metrics with Prediction Error', fontsize=11, fontweight='bold', pad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(seasons, fontsize=9)
ax2.axhline(0, color='gray', linestyle='--', linewidth=1)
ax2.legend(frameon=True, loc='upper left')
for bar in bars2:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, h + (0.02 if h >= 0 else -0.06), f'{h:.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
for bar in bars3:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, h + 0.02, f'{h:.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.suptitle('Figure 13: K-Nearest Neighbors Historical Distance and Neighborhood Dispersion Analysis', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('figures/revised/fig13_knn_neighborhood_analysis.png', bbox_inches='tight')
plt.close()
print("Figure 13 created.")

# -------------------------------------------------------------
# Figure 14: Permutation Feature Importance & Feature Ablation
# -------------------------------------------------------------
with open('results/advanced/permutation_feature_importance.json', 'r') as f:
    pfi_data = json.load(f)
with open('results/advanced/feature_ablation.json', 'r') as f:
    abl_data = json.load(f)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

# Panel (a): Permutation Importance for Kharif
features_display = ['Item (Crop)', 'Rainfall', 'Avg Temp', 'Area (Country)', 'Pesticides', 'Continent']
keys = ['Item', 'average_rain_fall_mm_per_year', 'avg_temp', 'Area', 'pesticides_tonnes', 'Continent']
k_imp = [pfi_data['Kharif'][k]['mean_rmse_increase'] for k in keys]
s_imp = [pfi_data['Seasonal'][k]['mean_rmse_increase'] for k in keys]

y = np.arange(len(features_display))
height = 0.38
ax1.barh(y - height/2, k_imp, height, label='Kharif Model', color='#3b82f6', edgecolor='#1e3a8a')
ax1.barh(y + height/2, s_imp, height, label='Seasonal Model', color='#f59e0b', edgecolor='#b45309')
ax1.set_xlabel('Mean RMSE Increase Under Permutation (hg/ha)', fontsize=10, fontweight='bold')
ax1.set_title('(a) Permutation Feature Importance on 2013 Holdout', fontsize=11, fontweight='bold', pad=10)
ax1.set_yticks(y)
ax1.set_yticklabels(features_display, fontsize=9)
ax1.invert_yaxis()
ax1.legend(frameon=True, loc='lower right')

# Panel (b): Feature Group Ablation R2
abl_lookup = [
    ('Full Pipeline', 'Full'),
    ('No Climate (Excl. Rain & Temp)', 'No Climate'),
    ('No Ag Inputs (Excl. Pesticides)', 'No Pesticides'),
    ('No Temporal (Excl. Year)', 'No Year'),
    ('No Geo Context (Excl. Area & Continent)', 'No Geo')
]
abl_keys = [item[0] for item in abl_lookup]
abl_labels = [item[1] for item in abl_lookup]

k_r2 = [abl_data['Kharif'][a]['r2'] for a in abl_keys]
r_r2 = [abl_data['Rabi'][a]['r2'] for a in abl_keys]
s_r2 = [abl_data['Seasonal'][a]['r2'] for a in abl_keys]

x = np.arange(len(abl_keys))
w = 0.25
ax2.bar(x - w, k_r2, w, label='Kharif', color='#3b82f6')
ax2.bar(x, r_r2, w, label='Rabi', color='#10b981')
ax2.bar(x + w, s_r2, w, label='Seasonal', color='#f59e0b')
ax2.set_ylabel('Prospective Test R² Score', fontsize=10, fontweight='bold')
ax2.set_title('(b) Impact of Feature Group Ablation on R²', fontsize=11, fontweight='bold', pad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(abl_labels, fontsize=8.5)
ax2.set_ylim(0.7, 1.0)
ax2.legend(frameon=True, loc='lower left')

plt.suptitle('Figure 14: Model Explainability via Permutation Importance and Feature Group Ablation', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('figures/revised/fig14_explainability_and_ablation.png', bbox_inches='tight')
plt.close()
print("Figure 14 created.")

# -------------------------------------------------------------
# Figure 15: Rolling-Origin Validation & Generalization Gap
# -------------------------------------------------------------
with open('results/advanced/rolling_origin_validation.json', 'r') as f:
    roll_data = json.load(f)
with open('results/advanced/random_vs_chronological.json', 'r') as f:
    rvc_data = json.load(f)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.8), dpi=300)

# Panel (a): Rolling Validation R2 across 2010-2013
years = [2010, 2011, 2012, 2013]
k_roll_r2 = [roll_data['Kharif'][str(y)]['r2'] for y in years]
r_roll_r2 = [roll_data['Rabi'][str(y)]['r2'] for y in years]
s_roll_r2 = [roll_data['Seasonal'][str(y)]['r2'] for y in years]

ax1.plot(years, k_roll_r2, marker='o', linewidth=2.2, color='#3b82f6', label='Kharif KNN')
ax1.plot(years, r_roll_r2, marker='s', linewidth=2.2, color='#10b981', label='Rabi KNN')
ax1.plot(years, s_roll_r2, marker='^', linewidth=2.2, color='#f59e0b', label='Seasonal KNN')
ax1.set_xlabel('Prospective Forecasting Year', fontsize=10, fontweight='bold')
ax1.set_ylabel('Prospective Test R² Score', fontsize=10, fontweight='bold')
ax1.set_title('(a) Multi-Year Rolling-Origin Forecasting Stability', fontsize=11, fontweight='bold', pad=10)
ax1.set_xticks(years)
ax1.set_ylim(0.91, 0.99)
ax1.legend(frameon=True, loc='lower left')

# Panel (b): Random vs Chronological R2
seasons_b = ['Kharif', 'Rabi', 'Seasonal']
chrono_r2 = [rvc_data[s]['knn_chronological']['r2'] for s in seasons_b]
random_r2 = [rvc_data[s]['knn_random']['r2'] for s in seasons_b]
x_b = np.arange(len(seasons_b))
width_b = 0.35

rects1 = ax2.bar(x_b - width_b/2, chrono_r2, width_b, label='Chronological Holdout (2013)', color='#2563eb')
rects2 = ax2.bar(x_b + width_b/2, random_r2, width_b, label='Random Holdout (Interpolative)', color='#f97316')
ax2.set_ylabel('Test R² Score', fontsize=10, fontweight='bold')
ax2.set_title('(b) Generalization Gap: Chronological vs Random Validation', fontsize=11, fontweight='bold', pad=10)
ax2.set_xticks(x_b)
ax2.set_xticklabels(seasons_b, fontsize=9.5)
ax2.set_ylim(0.90, 1.0)
ax2.legend(frameon=True, loc='upper left')

for rect in rects1:
    h = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width()/2, h + 0.003, f'{h:.4f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
for rect in rects2:
    h = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width()/2, h + 0.003, f'{h:.4f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.suptitle('Figure 15: Temporal Validation Dynamics and Multi-Year Generalization Trajectory', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('figures/revised/fig15_temporal_validation_dynamics.png', bbox_inches='tight')
plt.close()
print("Figure 15 created.")
