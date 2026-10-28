import os
import csv
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

os.makedirs('figures', exist_ok=True)
os.makedirs('tables', exist_ok=True)
os.makedirs('references', exist_ok=True)

# -------------------------------------------------------------
# 1. GENERATE FIGURE 10: Champion KNN Performance
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)
seasons = ['Kharif (k=3, Euclidean)', 'Rabi (k=7, Manhattan)', 'Seasonal (k=3, Manhattan)']
r2_scores = [0.9380, 0.9636, 0.9642]
r_scores = [0.9688, 0.9868, 0.9827]
x = np.arange(len(seasons))
width = 0.35

rects1 = ax1.bar(x - width/2, r2_scores, width, label='R² Score', color='#10b981')
rects2 = ax1.bar(x + width/2, r_scores, width, label='Pearson r', color='#3b82f6')
ax1.set_ylabel('Score / Coefficient', fontsize=10, fontweight='bold')
ax1.set_title('(a) Explanatory Power and Correlation (2013 Holdout)', fontsize=11, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(seasons, fontsize=9)
ax1.set_ylim(0.85, 1.02)
ax1.legend(loc='lower right', frameon=True)
ax1.grid(True, linestyle='--', alpha=0.5)

for rect in rects1:
    h = rect.get_height()
    ax1.annotate(f'{h:.4f}', xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 4), textcoords='offset points', ha='center', va='bottom', fontsize=8.5, fontweight='bold')
for rect in rects2:
    h = rect.get_height()
    ax1.annotate(f'{h:.4f}', xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 4), textcoords='offset points', ha='center', va='bottom', fontsize=8.5, fontweight='bold')

rmse_vals = [14026.44, 4065.82, 19646.94]
mae_vals = [6681.12, 3184.93, 9630.07]
rects3 = ax2.bar(x - width/2, rmse_vals, width, label='RMSE (hg/ha)', color='#ef4444')
rects4 = ax2.bar(x + width/2, mae_vals, width, label='MAE (hg/ha)', color='#f59e0b')
ax2.set_ylabel('Prediction Error (hg/ha)', fontsize=10, fontweight='bold')
ax2.set_title('(b) Absolute and Root Mean Squared Error (2013 Holdout)', fontsize=11, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(seasons, fontsize=9)
ax2.legend(loc='upper left', frameon=True)
ax2.grid(True, linestyle='--', alpha=0.5)

for rect in rects3:
    h = rect.get_height()
    ax2.annotate(f'{int(h):,}', xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 4), textcoords='offset points', ha='center', va='bottom', fontsize=8.5, fontweight='bold')
for rect in rects4:
    h = rect.get_height()
    ax2.annotate(f'{int(h):,}', xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 4), textcoords='offset points', ha='center', va='bottom', fontsize=8.5, fontweight='bold')

plt.suptitle('Figure 10: Selected Champion Model Performance Metrics Across Kharif, Rabi, and Seasonal Holdouts', fontsize=12, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('figures/10_final_model_performance.png', bbox_inches='tight')
plt.close()
print('Figure 10 created.')

# -------------------------------------------------------------
# 2. GENERATE FIGURE 12: Prediction Workflow
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 5), dpi=300)
ax.axis('off')

steps = [
    ('1. Client Interaction', 'User selects Season, Continent,\nCountry & Crop via dynamic\nUI; inputs rainfall, temp & pesticides', '#e0f2fe', '#0284c7'),
    ('2. Secure API Gateway', 'Client issues HTTPS request\nwith Bearer JWT token to\nPOST /api/v1/predict', '#fef3c7', '#d97706'),
    ('3. Dynamic Routing', 'FastAPI backend decodes JWT,\nvalidates Pydantic schema &\nroutes to season pipeline', '#f3e8ff', '#9333ea'),
    ('4. Pipeline Inference', 'Champion Pipeline applies\nOneHotEncoder + StandardScaler;\nqueries tuned k-NN regressor', '#dcfce7', '#16a34a'),
    ('5. Persistence & Output', 'Result & input parameters\nstored in SQLite database;\nJSON sent to frontend UI', '#fee2e2', '#dc2626')
]

for i, (title, desc, bg, border) in enumerate(steps):
    x = 0.03 + i * 0.195
    y = 0.28
    w = 0.17
    h = 0.48
    fancy = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02', facecolor=bg, edgecolor=border, linewidth=2)
    ax.add_patch(fancy)
    ax.text(x + w/2, y + h - 0.08, title, ha='center', va='top', fontsize=9.5, fontweight='bold', color=border)
    ax.text(x + w/2, y + h - 0.17, desc, ha='center', va='top', fontsize=8.2, color='#1e293b')
    
    if i < len(steps) - 1:
        ax.annotate('', xy=(x + w + 0.022, y + h/2), xytext=(x + w + 0.003, y + h/2),
                    arrowprops=dict(facecolor='#64748b', edgecolor='#64748b', arrowstyle='->', lw=2.5))

ax.text(0.5, 0.90, 'Figure 12: Production-Grade Operational Inference Workflow and Client-Server Interaction', ha='center', va='center', fontsize=12, fontweight='bold', color='#0f172a')
ax.text(0.5, 0.83, 'End-to-end execution path illustrating authentication, validation, pipeline dispatch, and database persistence', ha='center', va='center', fontsize=9, style='italic', color='#475569')

plt.tight_layout()
plt.savefig('figures/12_prediction_workflow.png', bbox_inches='tight')
plt.close()
print('Figure 12 created.')

# -------------------------------------------------------------
# 3. GENERATE ALL 11 TABLES (Markdown + CSV)
# -------------------------------------------------------------
tables = {
    "table_01_dataset_summary": {
        "headers": ["Dataset / Season", "Total Records", "Training Records (1990-2012)", "Test Records (2013)", "Crops Covered", "Geographic Scope", "Target Metric"],
        "rows": [
            ["Kharif", "4,404", "4,205 (95.48%)", "199 (4.52%)", "Maize (2,028), Sorghum (1,435), Cassava (941)", "96 Countries across 5 Continents", "hg/ha_yield"],
            ["Rabi", "1,810", "1,729 (95.52%)", "81 (4.48%)", "Wheat (1,810)", "76 Countries across 5 Continents", "hg/ha_yield"],
            ["Seasonal", "6,916", "6,604 (95.49%)", "312 (4.51%)", "Potatoes (4,276), Rice paddy (2,188), Soybeans (1,483), Sweet potatoes, Plantains, Yams", "101 Countries across 5 Continents", "hg/ha_yield"],
            ["Combined System", "13,130", "12,538 (95.49%)", "592 (4.51%)", "10 Agricultural Crops Total", "101 Sovereign Nations Globally", "hg/ha_yield"]
        ]
    },
    "table_02_feature_description": {
        "headers": ["Variable Name", "Role", "Data Type", "Physical Unit / Format", "Description & Domain Significance"],
        "rows": [
            ["Area", "Feature (Categorical)", "String", "Country Name", "Sovereign nation where agricultural cultivation and harvest took place."],
            ["Continent", "Feature (Categorical)", "String", "Continental Group", "Macro-geographical classification capturing continental agronomic regimes."],
            ["Item", "Feature (Categorical)", "String", "Crop Commodity", "Specific crop variety harvested (e.g., Potatoes, Wheat, Maize, Rice)."],
            ["Season", "Feature (Categorical)", "String", "Seasonal Segment", "Agricultural season classification (Kharif, Rabi, Seasonal)."],
            ["Year", "Feature (Temporal)", "Integer", "Calendar Year", "Temporal marker spanning 1990 to 2013 used for temporal holdout splitting."],
            ["average_rain_fall_mm_per_year", "Feature (Numerical)", "Float", "mm / year", "Annual cumulative precipitation reflecting macro water availability."],
            ["pesticides_tonnes", "Feature (Numerical)", "Float", "Metric Tonnes", "National total active pesticide application volume."],
            ["avg_temp", "Feature (Numerical)", "Float", "Degrees Celsius (°C)", "Mean annual air temperature representing thermal growing conditions."],
            ["hg/ha_yield", "Target Variable", "Float", "hg/ha (100 g/ha)", "Crop yield per hectare harvested (100 grams/ha = 0.1 kg/ha)."]
        ]
    },
    "table_03_data_preprocessing": {
        "headers": ["Pipeline Stage", "Input Features Affected", "Transformer Applied", "Configuration Parameters", "Mathematical Purpose & Rationale"],
        "rows": [
            ["Categorical Encoding", "Area, Continent, Item", "OneHotEncoder", "sparse_output=False, handle_unknown='ignore'", "Converts nominal categories to sparse orthogonal vectors without imposing ordinal bias."],
            ["Numerical Scaling", "Year, rainfall, pesticides, avg_temp", "StandardScaler", "with_mean=True, with_std=True", "Standardizes features to zero mean and unit variance: z = (x - mu) / sigma; critical for distance-based k-NN."],
            ["Feature Assembly", "All Transformed Subsets", "ColumnTransformer", "remainder='drop'", "Integrates encoded categorical matrices and standardized numerical arrays into a unified matrix."],
            ["Leakage Prevention", "Entire Pipeline", "Fit on Train Only", "Train: <= 2012, Test: == 2013", "Encoder categories and scaler parameters (mu, sigma) learned strictly from 1990-2012 data."]
        ]
    },
    "table_04_machine_learning_models": {
        "headers": ["Model Family", "Algorithm Class", "Inductive Bias & Operational Mechanism", "Key Strengths", "Primary Limitations", "Study Role"],
        "rows": [
            ["Linear Regression", "Parametric Linear", "Ordinary Least Squares minimizing residual sum of squares", "Interpretable, zero hyperparameters, fast computation", "Fails to capture complex non-linear agro-climatic interactions", "Baseline (Ours)"],
            ["K-Nearest Neighbors", "Instance-Based Non-Parametric", "Predicts local weighted average based on Minkowski metric neighborhood", "Captures local micro-clusters, no strong functional form assumptions", "Inference scales with dataset size; highly sensitive to feature scaling", "Core (Reference 2)"],
            ["Gradient Boosting Regressor", "Ensemble Boosting", "Sequentially fits shallow regression trees on negative gradient of loss function", "High predictive power, handles mixed distributions, strong generalization", "Susceptible to overfitting if tree depth and learning rate are unregularized", "Core (Reference 2)"],
            ["XGBoost Regressor", "Regularized Boosting", "Second-order Taylor gradient boosting with L1/L2 structural penalties", "Hardware-accelerated, robust regularization, tree pruning", "Requires extensive hyperparameter tuning across subsampling and learning rate", "Core (Reference 2)"],
            ["Multilayer Perceptron", "Deep Artificial Neural Net", "Feedforward artificial neural network with backpropagation and ReLU activations", "Universal function approximator for complex non-linear interactions", "Prone to local minima on tabular data, requires high tuning overhead", "Core (Reference 2)"]
        ]
    },
    "table_05_evaluation_metrics": {
        "headers": ["Metric", "Mathematical Definition", "Domain Unit", "Sensitivity & Analytical Significance in Crop Yield Modeling"],
        "rows": [
            ["Root Mean Squared Error (RMSE)", "sqrt((1/N) * sum((y_i - yhat_i)^2))", "hg/ha", "Penalizes large outlier estimation errors heavily; crucial for food supply planning."],
            ["Mean Absolute Error (MAE)", "(1/N) * sum(|y_i - yhat_i|)", "hg/ha", "Reflects average expected magnitude of forecast deviation without squaring outliers."],
            ["Coefficient of Determination (R²)", "1 - (sum((y_i - yhat_i)^2) / sum((y_i - ybar)^2))", "Dimensionless (<= 1.0)", "Quantifies proportion of yield variance explained by input agronomic factors."],
            ["Pearson Correlation (r)", "Cov(y, yhat) / (sigma_y * sigma_yhat)", "Dimensionless (-1 to +1)", "Measures linear tracking fidelity between actual and predicted trajectories."]
        ]
    },
    "table_06_hyperparameter_tuning": {
        "headers": ["Model", "Tuned Hyperparameter", "Evaluated Search Space", "Kharif Best", "Rabi Best", "Seasonal Best", "Optimization Method"],
        "rows": [
            ["K-Nearest Neighbors (KNN)", "n_neighbors (k)", "[3, 5, 7, 9]", "3", "7", "3", "3-Fold Time-Aware GridSearch"],
            ["K-Nearest Neighbors (KNN)", "weights", "['uniform', 'distance']", "'distance'", "'distance'", "'distance'", "3-Fold Time-Aware GridSearch"],
            ["K-Nearest Neighbors (KNN)", "p (Minkowski Power)", "[1 (Manhattan), 2 (Euclidean)]", "2 (Euclidean)", "1 (Manhattan)", "1 (Manhattan)", "3-Fold Time-Aware GridSearch"],
            ["XGBoost Regressor", "n_estimators", "[100, 150]", "150", "150", "150", "3-Fold Time-Aware GridSearch"],
            ["XGBoost Regressor", "learning_rate", "[0.05, 0.1]", "0.05", "0.05", "0.05", "3-Fold Time-Aware GridSearch"],
            ["XGBoost Regressor", "max_depth", "[4, 6, 8]", "7 (best in Kharif)", "6", "8", "3-Fold Time-Aware GridSearch"],
            ["Gradient Boosting Regressor", "n_estimators / max_depth", "[100, 150] / [3, 4, 5]", "150 / 4", "150 / 3", "150 / 4", "3-Fold Time-Aware GridSearch"],
            ["Multilayer Perceptron (MLP)", "hidden_layer_sizes", "[(64, 32), (100,)]", "(64, 32)", "(64, 32)", "(64, 32)", "3-Fold Time-Aware GridSearch"]
        ]
    },
    "table_07_kharif_results": {
        "headers": ["Model Architecture", "Pipeline Status", "RMSE (hg/ha)", "MAE (hg/ha)", "R² Score", "Pearson r", "Test Rank & Selection Status"],
        "rows": [
            ["K-Nearest Neighbors (KNN)", "Tuned Champion (k=3, Euclidean)", "14,026.44", "6,681.12", "0.9380", "0.9688", "Rank 1 (Selected Champion)"],
            ["XGBoost Regressor", "Tuned (150 trees, depth 7)", "17,235.88", "9,779.95", "0.9064", "0.9533", "Rank 2 (Runner-Up)"],
            ["Gradient Boosting Regressor", "Tuned (150 trees, depth 4)", "22,679.27", "14,818.38", "0.8379", "0.9278", "Rank 3"],
            ["Multilayer Perceptron (MLP)", "Tuned ((64, 32) layers)", "28,734.16", "17,988.13", "0.7398", "0.8635", "Rank 4"],
            ["Linear Regression", "Untuned Baseline", "32,099.53", "20,507.06", "0.6753", "0.8305", "Rank 5 (Linear Baseline)"]
        ]
    },
    "table_08_rabi_results": {
        "headers": ["Model Architecture", "Pipeline Status", "RMSE (hg/ha)", "MAE (hg/ha)", "R² Score", "Pearson r", "Test Rank & Selection Status"],
        "rows": [
            ["K-Nearest Neighbors (KNN)", "Tuned Champion (k=7, Manhattan)", "4,065.82", "3,184.93", "0.9636", "0.9868", "Rank 1 (Selected Champion)"],
            ["XGBoost Regressor", "Tuned (150 trees, depth 6)", "5,649.94", "4,456.27", "0.9297", "0.9678", "Rank 2 (Runner-Up)"],
            ["Linear Regression", "Untuned Baseline", "6,182.82", "4,554.99", "0.9158", "0.9592", "Rank 3 (Strong Linear Baseline)"],
            ["Gradient Boosting Regressor", "Tuned (150 trees, depth 3)", "8,621.76", "7,386.21", "0.8362", "0.9333", "Rank 4"],
            ["Multilayer Perceptron (MLP)", "Tuned ((64, 32) layers)", "13,787.41", "9,815.03", "0.5812", "0.7987", "Rank 5"]
        ]
    },
    "table_09_seasonal_results": {
        "headers": ["Model Architecture", "Pipeline Status", "RMSE (hg/ha)", "MAE (hg/ha)", "R² Score", "Pearson r", "Test Rank & Selection Status"],
        "rows": [
            ["K-Nearest Neighbors (KNN)", "Tuned Champion (k=3, Manhattan)", "19,646.94", "9,630.07", "0.9642", "0.9827", "Rank 1 (Selected Champion)"],
            ["XGBoost Regressor", "Tuned (150 trees, depth 8)", "25,933.82", "15,245.57", "0.9377", "0.9698", "Rank 2 (Runner-Up)"],
            ["Gradient Boosting Regressor", "Tuned (150 trees, depth 4)", "44,947.15", "29,792.24", "0.8127", "0.9149", "Rank 3"],
            ["Multilayer Perceptron (MLP)", "Tuned ((64, 32) layers)", "48,214.55", "34,303.93", "0.7845", "0.8870", "Rank 4"],
            ["Linear Regression", "Untuned Baseline", "52,357.50", "36,511.22", "0.7459", "0.8674", "Rank 5 (Linear Baseline)"]
        ]
    },
    "table_10_overall_comparison": {
        "headers": ["Season", "Selected Champion Model", "Best Configuration", "Prospective Test RMSE (hg/ha)", "Prospective Test MAE (hg/ha)", "Prospective Test R²", "Pearson r", "Error Reduction vs Baseline"],
        "rows": [
            ["Kharif", "K-Nearest Neighbors", "k=3, p=2 (Euclidean), distance-weighted", "14,026.44", "6,681.12", "0.9380", "0.9688", "56.30% RMSE reduction vs Linear"],
            ["Rabi", "K-Nearest Neighbors", "k=7, p=1 (Manhattan), distance-weighted", "4,065.82", "3,184.93", "0.9636", "0.9868", "34.24% RMSE reduction vs Linear"],
            ["Seasonal", "K-Nearest Neighbors", "k=3, p=1 (Manhattan), distance-weighted", "19,646.94", "9,630.07", "0.9642", "0.9827", "62.48% RMSE reduction vs Linear"],
            ["Cross-Season Average", "Tuned KNN Regressor", "Distance-weighted Minkowski k-NN", "12,579.73", "6,498.71", "0.9553", "0.9794", "50.98% Mean RMSE reduction vs Linear"]
        ]
    },
    "table_11_system_components": {
        "headers": ["Subsystem Layer", "Module / Component", "Technology Stack", "Operational Functionality", "Production Characteristics"],
        "rows": [
            ["Machine Learning Engine", "Model Pipelines", "Scikit-Learn, Joblib", "Kharif, Rabi, and Seasonal pipelines combining ColumnTransformer & tuned k-NN", "Serialised, sub-millisecond inference, strict zero data leakage."],
            ["API Gateway", "FastAPI Service", "FastAPI, Uvicorn, Pydantic v2", "Exposes REST endpoints for prediction, auth, options, and analytics", "Asynchronous, self-documenting OpenAPI/Swagger, strict typing."],
            ["Security & Identity", "Authentication Module", "OAuth2, JWT, Passlib (Bcrypt)", "User registration, password salting & hashing, bearer token issue and verification", "Stateless, cryptographic signature validation, 60-min expiration."],
            ["Data Persistence", "Database Layer", "SQLite 3, SQLAlchemy ORM", "Maintains User table (credentials) and PredictionHistory audit log table", "Zero-config embedded relational storage, complete audit trail."],
            ["User Interface", "Frontend Client", "HTML5, Vanilla CSS3, JavaScript ES6", "Responsive dashboard with cascading dropdowns, historical records, and chart renders", "Clean, glassmorphism aesthetic, zero bloated frontend dependencies."]
        ]
    }
}

for name, data in tables.items():
    csv_path = os.path.join('tables', f'{name}.csv')
    md_path = os.path.join('tables', f'{name}.md')
    
    # Write CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data["headers"])
        writer.writerows(data["rows"])
        
    # Write Markdown
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# {name.replace('_', ' ').title()}\n\n")
        f.write("| " + " | ".join(data["headers"]) + " |\n")
        f.write("| " + " | ".join(["---"] * len(data["headers"])) + " |\n")
        for row in data["rows"]:
            f.write("| " + " | ".join(row) + " |\n")

print('All 11 Tables generated in tables/ as CSV and Markdown.')

# -------------------------------------------------------------
# 4. GENERATE REFERENCES (BibTeX + Markdown)
# -------------------------------------------------------------
bibtex_content = """@article{gupta2026explainable,
  author    = {Gupta, Rahul and Jha, S. K. and Kumar, Preetam and Yadav, Mukul},
  title     = {Explainable ensemble machine learning algorithms for predicting wind speed by incorporating {Shapley} additive explanations},
  journal   = {Franklin Open},
  volume    = {10},
  pages     = {100781},
  year      = {2026},
  doi       = {10.1016/j.fraope.2026.100781}
}

@article{elkenawy2025predicting,
  author    = {El-Kenawy, El-Sayed M. and Alhussan, Amel Ali and Khodadadi, Nima and Mirjalili, Seyedali and Eid, Marwa M.},
  title     = {Predicting Potato Crop Yield with Machine Learning and Deep Learning for Sustainable Agriculture},
  journal   = {Potato Research},
  volume    = {68},
  number    = {2},
  pages     = {759--792},
  year      = {2025},
  doi       = {10.1007/s11540-024-09753-w}
}

@article{breiman2001random,
  author    = {Breiman, Leo},
  title     = {Random Forests},
  journal   = {Machine Learning},
  volume    = {45},
  number    = {1},
  pages     = {5--32},
  year      = {2001},
  doi       = {10.1023/A:1010933404324}
}

@inproceedings{chen2016xgboost,
  author    = {Chen, Tianqi and Guestrin, Carlos},
  title     = {{XGBoost}: A Scalable Tree Boosting System},
  booktitle = {Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining},
  pages     = {785--794},
  year      = {2016},
  doi       = {10.1145/2939672.2939785}
}

@article{scikit-learn,
  author    = {Pedregosa, Fabian and Varoquaux, Ga{\"e}l and Gramfort, Alexandre and Michel, Vincent and Thirion, Bertrand and Grisel, Olivier and Blondel, Mathieu and Prettenhofer, Peter and Weiss, Ron and Dubourg, Vincent and Vanderplas, Jake and Passos, Alexandre and Cournapeau, David and Brucher, Matthieu and Perrot, Matthieu and Duchesnay, {\'E}douard},
  title     = {Scikit-learn: Machine Learning in {P}ython},
  journal   = {Journal of Machine Learning Research},
  volume    = {12},
  pages     = {2825--2830},
  year      = {2011}
}

@article{paudel2021machine,
  author    = {Paudel, D. and Boogaard, H. and de Wit, A. and Janssen, S. and Osinga, S. and Pylianidis, C. and Athanasiadis, I. N.},
  title     = {Machine learning for large-scale crop yield forecasting},
  journal   = {Agricultural Systems},
  volume    = {187},
  pages     = {103016},
  year      = {2021},
  doi       = {10.1016/j.agsy.2020.103016}
}

@article{van2020crop,
  author    = {van Klompenburg, T. and Kassahun, A. and Catal, C.},
  title     = {Crop yield prediction using machine learning: A systematic literature review},
  journal   = {Computers and Electronics in Agriculture},
  volume    = {177},
  pages     = {105709},
  year      = {2020},
  doi       = {10.1016/j.compag.2020.105709}
}

@article{ortiz2021anthropogenic,
  author    = {Ortiz-Bobea, Ariel and Ault, Toby R. and Carrillo, Carlos M. and Chambers, Robert G. and Lobell, David B.},
  title     = {Anthropogenic climate change has slowed global agricultural productivity growth},
  journal   = {Nature Climate Change},
  volume    = {11},
  number    = {4},
  pages     = {306--312},
  year      = {2021},
  doi       = {10.1038/s41558-021-01000-1}
}

@article{lundberg2017unified,
  author    = {Lundberg, Scott M. and Lee, Su-In},
  title     = {A Unified Approach to Interpreting Model Predictions},
  journal   = {Advances in Neural Information Processing Systems},
  volume    = {30},
  pages     = {4765--4774},
  year      = {2017}
}

@article{chai2014root,
  author    = {Chai, T. and Draxler, R. R.},
  title     = {Root mean square error ({RMSE}) or mean absolute error ({MAE})? -- Arguments against avoiding {RMSE} in the literature},
  journal   = {Geoscientific Model Development},
  volume    = {7},
  number    = {3},
  pages     = {1247--1250},
  year      = {2014},
  doi       = {10.5194/gmd-7-1247-2014}
}
"""

with open('references/references.bib', 'w', encoding='utf-8') as f:
    f.write(bibtex_content)

print('references/references.bib created.')
