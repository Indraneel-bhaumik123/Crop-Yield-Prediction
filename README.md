# Seasonal Crop Yield Prediction Using Machine Learning
### An End-to-End Research-Quality Agricultural Decision-Support System

**System Name:** AgriYield  
**Target Variable:** `hg/ha_yield` (Hectograms per Hectare)  
**Evaluation Paradigm:** Prospective Chronological Validation (Training: 1990–2012, Testing: 2013)  
**Data Preserved:** Original agricultural datasets untouched in `data/original/` and preserved in root `data/`.

---

## 1. Executive Summary & Research Motivation
Agricultural productivity is intrinsically linked to seasonal climate cycles, hydrological patterns, and agronomic inputs. This system implements an end-to-end, research-grade machine learning framework to forecast crop yields under three distinct cultivation regimes:
1. **Kharif Season (Monsoon / Autumn Harvest):** Characterized by high moisture dependency (Maize, Sorghum, Cassava).
2. **Rabi Season (Winter / Spring Harvest):** Defined by temperate conditions and controlled water regimes (Wheat).
3. **Seasonal / Whole-Year Rotations:** Multi-cycle and perennial staple crops (Potatoes, Rice paddy, Soybeans, Sweet potatoes, Plantains, Yams).

---

## 2. Scientific Data Dictionary

| Feature Name | Type | Domain / Units | Role | Agronomic Description |
|:---|:---:|:---:|:---:|:---|
| `Area` | Categorical | Country Name (101 countries) | Predictor | Captures national soil characteristics, infrastructure, and agronomic practices. |
| `Continent` | Categorical | 6 Continents | Predictor | Macro-geographic regional stratifier. |
| `Item` | Categorical | 10 Crop Commodities | Predictor | Crop variety governing genetic yield potential. |
| `Season` | Categorical | Kharif, Rabi, Seasonal | Stratifier | Crop phenological cycle used to specialize model pipelines. |
| `Year` | Numerical | 1990 – 2013 | Chronological Split | Historical calendar year; used strictly to prevent prospective lookahead leakage. |
| `average_rain_fall_mm_per_year` | Numerical | mm / year | Predictor | Total annual cumulative precipitation. |
| `pesticides_tonnes` | Numerical | Metric Tonnes | Predictor | Chemical crop protection load. |
| `avg_temp` | Numerical | Degrees Celsius (°C) | Predictor | Mean annual ambient temperature. |
| **`hg/ha_yield`** | **Numerical** | **hg/ha ($0.1\text{ kg}/\text{ha}$)** | **Target** | **Primary target variable: normalized agricultural yield.** |

---

## 3. Machine Learning Methodology & Empirical Benchmark Results

### 3.1 Time-Aware Chronological Evaluation
To prevent data leakage common in naive random train-test splits, models are evaluated strictly on future holdout data:
- **Training Set (1990 – 2012):** 23 historical cultivation years.
- **Testing Set (2013 onward):** Prospective hold-out test year.

### 3.2 Candidate Model Architectures
- **Baseline:** Linear Regression (Ordinary Least Squares).
- **Paper Candidate 1:** K-Nearest Neighbors (KNN Regressor) with inverse-distance weighting.
- **Paper Candidate 2:** Gradient Boosting Regressor (GBR).
- **Paper Candidate 3:** XGBoost Regressor (Extreme Gradient Boosting).
- **Paper Candidate 4:** Multi-Layer Perceptron (MLP Regressor) artificial neural network.

### 3.3 Verified Empirical Performance Table (Prospective Test Set: Year 2013)

| Season | Model Architecture | RMSE (hg/ha) | MAE (hg/ha) | $R^2$ Score | Pearson $r$ | Status |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **Kharif** | **KNN Regressor (Tuned)** | **14,026.44** | **6,681.12** | **0.9380** | **0.9688** | **Selected Champion** |
| Kharif | XGBoost Regressor | 17,235.88 | 9,779.95 | 0.9064 | 0.9533 | Paper Candidate |
| Kharif | Gradient Boosting | 22,679.27 | 14,818.38 | 0.8379 | 0.9278 | Paper Candidate |
| Kharif | MLP Regressor | 28,734.16 | 17,988.13 | 0.7398 | 0.8635 | Paper Candidate |
| Kharif | Linear Regression | 32,099.53 | 20,507.06 | 0.6753 | 0.8305 | Additional Baseline |
| **Rabi** | **KNN Regressor (Tuned)** | **4,065.82** | **3,184.93** | **0.9636** | **0.9868** | **Selected Champion** |
| Rabi | XGBoost Regressor | 5,649.94 | 4,456.27 | 0.9297 | 0.9678 | Paper Candidate |
| Rabi | Linear Regression | 6,182.82 | 4,554.99 | 0.9158 | 0.9592 | Additional Baseline |
| Rabi | Gradient Boosting | 8,621.76 | 7,386.21 | 0.8362 | 0.9333 | Paper Candidate |
| Rabi | MLP Regressor | 13,787.41 | 9,815.03 | 0.5812 | 0.7987 | Paper Candidate |
| **Seasonal** | **KNN Regressor (Tuned)** | **19,646.94** | **9,630.07** | **0.9642** | **0.9827** | **Selected Champion** |
| Seasonal | XGBoost Regressor | 25,933.82 | 15,245.57 | 0.9377 | 0.9698 | Paper Candidate |
| Seasonal | Gradient Boosting | 44,947.15 | 29,792.24 | 0.8127 | 0.9149 | Paper Candidate |
| Seasonal | MLP Regressor | 48,214.55 | 34,303.93 | 0.7845 | 0.8870 | Paper Candidate |
| Seasonal | Linear Regression | 52,357.50 | 36,511.22 | 0.7459 | 0.8674 | Additional Baseline |

---

## 4. Rebuilt Project Directory Structure

```text
Seasonal_Crop_Yield_Prediction_Rebuilt/
│
├── data/
│   ├── original/               # Safe preservation of original CSV datasets
│   │   ├── kharif_combined.csv
│   │   ├── rabi_combined.csv
│   │   └── seasonal_combined.csv
│   └── processed/              # Verified working datasets
│       ├── processed_kharif.csv
│       ├── processed_rabi.csv
│       └── processed_seasonal.csv
│
├── notebooks/
│   └── Seasonal_Crop_Yield_Prediction.ipynb  # Executed, cell-by-cell research notebook
│
├── figures/
│   ├── eda/                    # Publication-quality EDA charts (DPI 300)
│   │   ├── 01_yield_distribution_by_season.png
│   │   ├── 02_crop_distribution_breakdown.png
│   │   ├── 03_environmental_factors_vs_yield.png
│   │   ├── 04_temporal_yield_trajectory.png
│   │   └── 05_correlation_matrices.png
│   └── evaluation/             # Model evaluation and parity plots
│       ├── 06_initial_model_comparison.png
│       ├── 07_tuned_model_comparison.png
│       └── 08_actual_vs_predicted_parity.png
│
├── models/                     # Serialized production pipelines (Preprocessor + Regressor)
│   ├── kharif_model.joblib
│   ├── rabi_model.joblib
│   └── seasonal_model.joblib
│
├── results/                    # Benchmark result CSVs
│   ├── initial_model_evaluation.csv
│   └── tuned_model_evaluation.csv
│
├── Backend/                    # FastAPI Application
│   ├── __init__.py
│   ├── main.py                 # REST API endpoints & static dashboard mount
│   ├── database.py             # SQLite & SQLAlchemy engine
│   ├── models.py               # ORM models (User, PredictionHistory)
│   ├── auth.py                 # PBKDF2/bcrypt hashing & JWT tokens
│   └── schemas.py              # Pydantic request/response schemas
│
├── Frontend/                   # Interactive Dashboard (matches reference UI)
│   ├── index.html              # HTML5 structure with login-first modal
│   ├── style.css               # Modern emerald/forest green theme
│   └── script.js               # Dynamic cascading options & Chart.js logic
│
├── tests/                      # Automated test suites
│   ├── test_backend.py         # Unit tests (unittest & TestClient)
│   └── test_integration.py     # End-to-end integration and edge-case verification
│
├── crop_prediction.db          # SQLite persistent database
├── requirements.txt            # Python dependencies
└── README.md                   # Comprehensive project documentation
```

---

## 5. Setup & Execution Instructions

### Step 1: Install Dependencies
```bash
cd "Seasonal_Crop_Yield_Prediction_Rebuilt"
pip install -r requirements.txt
```

### Step 2: Run the Jupyter Notebook Workflow
To regenerate or inspect the research notebook:
```bash
python build_notebook.py
```
Or open in JupyterLab / VS Code:
```bash
jupyter notebook notebooks/Seasonal_Crop_Yield_Prediction.ipynb
```

### Step 3: Run the FastAPI Backend & Dashboard
Start the production server:
```bash
python -m uvicorn Backend.main:app --host 127.0.0.1 --port 8000 --reload
```
Open your browser at:
- **Interactive UI Dashboard:** [http://127.0.0.1:8000/frontend/](http://127.0.0.1:8000/frontend/) (or [http://127.0.0.1:8000/](http://127.0.0.1:8000/))
- **Interactive OpenAPI Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Step 4: Run Automated Tests
```bash
python -m unittest tests/test_backend.py
python tests/test_integration.py
```

---

## 6. Frontend Features & Compliance with Visual Reference
The rebuilt interface faithfully captures the spirit, styling, and functionality of the reference `AgriYield` UI screenshot:
- **Login-First Modal:** Unauthenticated visitors are prompted to sign in or register before accessing prediction features. A **"⚡ Quick Fill Demo Credentials"** button is provided for quick evaluation.
- **Hierarchical Prediction Engine:** Dynamically cascades `Season` $\to$ `Continent` $\to$ `Country` $\to$ `Crop`, backed by live API queries.
- **Detailed Prediction Result Card:**
  - Large metric badge with high-yield potential status.
  - Agricultural Potential circular gauge (0–100 score).
  - Complete metadata summary (Crop, Model, Season, Time, Country, Confidence, Year, History ID).
  - Factor impact assessments (Rainfall, Temperature, Pesticides).
- **Interactive Visualizations:**
  - Average Yield by Season (bar chart).
  - Top Crops distribution (doughnut chart).
  - Historical yield trajectory (line chart).
- **User History Table:** Persistent per-user prediction logs with delete and refresh capabilities.
- **Model Comparison View:** Research evaluation table documenting test RMSE, MAE, R², and Pearson correlation.
