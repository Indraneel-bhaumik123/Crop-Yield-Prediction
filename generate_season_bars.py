import matplotlib.pyplot as plt
import numpy as np

# Styling configuration
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.0

# Kharif
models = ['KNN\n(Tuned)', 'XGBoost', 'Gradient\nBoosting', 'MLP', 'Linear\nRegression']
kharif_r2 = [0.9380, 0.9064, 0.8379, 0.7398, 0.6753]
kharif_rmse = [14026.44, 17235.88, 22679.27, 28734.16, 32099.53]

fig, ax1 = plt.subplots(figsize=(6.2, 4.2), dpi=300)
colors = ['#10b981', '#3b82f6', '#64748b', '#a855f7', '#f59e0b']
bars = ax1.bar(models, kharif_r2, color=colors, width=0.55, edgecolor='#1e293b')
ax1.set_ylabel('Test R² Score', fontsize=10, fontweight='bold', color='#0f172a')
ax1.set_ylim(0.5, 1.0)
ax1.grid(axis='y', linestyle='--', alpha=0.4)
ax1.set_title('Kharif Holdout (2013): Model R² Comparison', fontsize=11, fontweight='bold', color='#0f172a', pad=10)
for bar in bars:
    y = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, y + 0.015, f'{y:.4f}', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#0f172a')
plt.tight_layout()
plt.savefig('figures/kharif_comparison_bar.png', dpi=300)
plt.close()

# Rabi
rabi_models = ['KNN\n(Tuned)', 'XGBoost', 'Linear\nRegression', 'Gradient\nBoosting', 'MLP']
rabi_r2 = [0.9636, 0.9297, 0.9158, 0.8362, 0.5812]
colors_rabi = ['#10b981', '#3b82f6', '#f59e0b', '#64748b', '#a855f7']

fig, ax = plt.subplots(figsize=(6.2, 4.2), dpi=300)
bars = ax.bar(rabi_models, rabi_r2, color=colors_rabi, width=0.55, edgecolor='#1e293b')
ax.set_ylabel('Test R² Score', fontsize=10, fontweight='bold', color='#0f172a')
ax.set_ylim(0.45, 1.02)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.set_title('Rabi Holdout (2013): Model R² Comparison', fontsize=11, fontweight='bold', color='#0f172a', pad=10)
for bar in bars:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + 0.015, f'{y:.4f}', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#0f172a')
plt.tight_layout()
plt.savefig('figures/rabi_comparison_bar.png', dpi=300)
plt.close()

# Seasonal
seasonal_models = ['KNN\n(Tuned)', 'XGBoost', 'Gradient\nBoosting', 'MLP', 'Linear\nRegression']
seasonal_r2 = [0.9642, 0.9377, 0.8127, 0.7845, 0.7459]
colors_seasonal = ['#10b981', '#3b82f6', '#64748b', '#a855f7', '#f59e0b']

fig, ax = plt.subplots(figsize=(6.2, 4.2), dpi=300)
bars = ax.bar(seasonal_models, seasonal_r2, color=colors_seasonal, width=0.55, edgecolor='#1e293b')
ax.set_ylabel('Test R² Score', fontsize=10, fontweight='bold', color='#0f172a')
ax.set_ylim(0.65, 1.02)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.set_title('Seasonal Holdout (2013): Model R² Comparison', fontsize=11, fontweight='bold', color='#0f172a', pad=10)
for bar in bars:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + 0.012, f'{y:.4f}', ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#0f172a')
plt.tight_layout()
plt.savefig('figures/seasonal_comparison_bar.png', dpi=300)
plt.close()

print('Season comparison bar charts generated successfully!')
