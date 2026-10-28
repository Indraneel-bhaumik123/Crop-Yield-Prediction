"""
Generate additional high-resolution publication diagrams for the research paper:
- Figure 1: Research Methodology Framework
- Figure 11: End-to-End System Deployment Architecture
- Figure 12: Hierarchical Prediction and Decision Support Workflow
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

BASE_DIR = Path(r"c:\Users\indra\OneDrive\Desktop\Seasonal Crop Yield Prediction\Seasonal_Crop_Yield_Prediction_Rebuilt")
FIG_DIR = BASE_DIR / "figures"
FIG_EVAL = FIG_DIR / "evaluation"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------------------
# Figure 1: Research Methodology Framework
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
ax.axis('off')

# Box helper
def draw_box(x, y, w, h, title, subtitle, color, text_color='#14281d'):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03",
                                  facecolor=color, edgecolor='#1e7e48', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h*0.62, title, ha='center', va='center', fontsize=10, fontweight='bold', color=text_color)
    if subtitle:
        ax.text(x + w/2, y + h*0.28, subtitle, ha='center', va='center', fontsize=8, color=text_color)

def draw_arrow(x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor='#1e7e48', edgecolor='#1e7e48', width=1.5, headwidth=7, shrink=0.05))

# Row 1: Raw Data & Ingestion
draw_box(0.05, 0.78, 0.25, 0.16, "Multi-Source Agro Data", "13,130 records (1990–2013)\n101 Countries, 10 Crops", "#eaf6ee")
draw_box(0.38, 0.78, 0.25, 0.16, "Seasonal Stratification", "Kharif (Monsoon: 4,404)\nRabi (Winter: 1,810)\nSeasonal (Multi: 6,916)", "#eaf6ee")
draw_box(0.70, 0.78, 0.25, 0.16, "Data Integrity & Audit", "0 Missing Values\n0 Duplicates\nPhysical Bounds Verified", "#eaf6ee")

draw_arrow(0.30, 0.86, 0.38, 0.86)
draw_arrow(0.63, 0.86, 0.70, 0.86)

# Row 2: Preprocessing & Temporal Splitting
draw_box(0.05, 0.48, 0.25, 0.16, "Time-Aware Split", "Train: 1990–2012 (23 Yrs)\nTest: 2013 (Holdout)\nNo Lookahead Bias", "#dcfce7")
draw_box(0.38, 0.48, 0.25, 0.16, "Leakage-Free Preprocessing", "OneHotEncoder(Categoricals)\nStandardScaler(Numericals)\nStrictly Fit on Train Only", "#dcfce7")
draw_box(0.70, 0.48, 0.25, 0.16, "5-Model Zoo Evaluation", "Baseline: Linear Regression\nCandidates: KNN, GBR,\nXGBoost, MLP Regressor", "#dcfce7")

draw_arrow(0.82, 0.78, 0.82, 0.64) # Down from audit
draw_arrow(0.70, 0.56, 0.63, 0.56) # Right to left
draw_arrow(0.38, 0.56, 0.30, 0.56) # Preproc to Zoo

# Row 3: Tuning & Deployment
draw_box(0.05, 0.16, 0.25, 0.16, "Hyperparameter Tuning", "GridSearchCV + 3-Fold CV\nDistance-Weighted KNN\nShrinkage & Tree Depths", "#fef9c3")
draw_box(0.38, 0.16, 0.25, 0.16, "Champion Selection", "Hold-Out 2013 Testing\nKharif R²=0.938, Rabi R²=0.964\nSeasonal R²=0.964 (KNN)", "#fef9c3")
draw_box(0.70, 0.16, 0.25, 0.16, "Full-Stack Deployment", "FastAPI REST Server\nSQLite History + JWT\nAgriYield Interactive UI", "#eaf6ee")

draw_arrow(0.17, 0.48, 0.17, 0.32) # Down from time-aware
draw_arrow(0.30, 0.24, 0.38, 0.24)
draw_arrow(0.63, 0.24, 0.70, 0.24)

plt.tight_layout()
fig.savefig(FIG_DIR / "09_research_methodology_framework.png", dpi=300)
plt.close(fig)
print("Saved Figure 9 -> 09_research_methodology_framework.png")

# ------------------------------------------------------------------------------
# Figure 11: End-to-End System Deployment Architecture
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
ax.axis('off')

draw_box(0.05, 0.55, 0.24, 0.32, "Client Dashboard\n(HTML5/CSS3/Vanilla JS)", "• Login-First Auth Modal\n• Cascading Selectors\n• Numeric Form Inputs\n• Interactive Chart.js\n• Real-Time Yield Gauge", "#eaf6ee")
draw_box(0.38, 0.55, 0.26, 0.32, "FastAPI Application Server\n(Uvicorn ASGI Engine)", "• JWT Bearer Auth (/login)\n• Dynamic Options (/options)\n• Prediction Gateway (/predict)\n• Analytics Engine (/analytics)\n• Static File Delivery", "#dcfce7")
draw_box(0.72, 0.55, 0.24, 0.32, "Persistent Data Layer\n(SQLite + SQLAlchemy)", "• User Accounts (PBKDF2)\n• Prediction Audit Log\n• Location & Crop Index\n• Timestamped Queries", "#fef9c3")

draw_box(0.38, 0.10, 0.58, 0.30, "Serialized Machine Learning Pipelines (Joblib)", "• ColumnTransformer (OneHotEncoder + StandardScaler)\n• Kharif Champion Pipeline (Tuned Distance-Weighted KNN, k=3, p=2)\n• Rabi Champion Pipeline (Tuned Distance-Weighted KNN, k=7, p=1)\n• Seasonal Champion Pipeline (Tuned Distance-Weighted KNN, k=3, p=1)", "#e0f2fe")

draw_arrow(0.29, 0.71, 0.38, 0.71)
draw_arrow(0.64, 0.71, 0.72, 0.71)
draw_arrow(0.51, 0.55, 0.51, 0.40)

plt.tight_layout()
fig.savefig(FIG_DIR / "11_system_architecture_diagram.png", dpi=300)
plt.close(fig)
print("Saved Figure 11 -> 11_system_architecture_diagram.png")
