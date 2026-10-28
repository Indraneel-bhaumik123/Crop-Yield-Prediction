# Experiment Provenance & Scientific Ground Truth Documentation

## 1. Provenance Metadata
- **Project Title:** Seasonal Crop Yield Prediction Using Machine Learning: A Comparative Study of KNN, Gradient Boosting, XGBoost, and MLP
- **Execution Date:** September 2026
- **Lead System:** AgriYield Research Engineering
- **Target Variable:** `hg/ha_yield` (Hectograms per Hectare; $1\text{ hg/ha} = 0.1\text{ kg/ha}$)
- **Evaluation Strategy:** Prospective Out-of-Time Chronological Validation
  - **Training Period:** 1990 – 2012 (23 historical cultivation years)
  - **Testing Holdout Period:** 2013 (future prospective holdout)
- **Primary Source of Truth Files:**
  - `notebooks/Seasonal_Crop_Yield_Prediction.ipynb` (54 cells, verified execution)
  - `results/tuned_model_evaluation.csv`
  - `results/initial_model_evaluation.csv`
  - `models/kharif_model.joblib`
  - `models/rabi_model.joblib`
  - `models/seasonal_model.joblib`

---

## 2. Dataset Versioning & Statistics
- **Original Source Files (Safe & Untouched):**
  - `data/original/kharif_combined.csv` (SHA-256: `6130c9fb31c28bc8...`)
  - `data/original/rabi_combined.csv` (SHA-256: `7fa5fe29a5b41e92...`)
  - `data/original/seasonal_combined.csv` (SHA-256: `376fd659491f1de6...`)
- **Verified Record Counts:**
  - Kharif: 4,404 rows, 9 columns (Train: 4,205, Test: 199)
  - Rabi: 1,810 rows, 9 columns (Train: 1,729, Test: 81)
  - Seasonal: 6,916 rows, 9 columns (Train: 6,604, Test: 312)
  - Total Multi-Season Observations: 13,130 records across 101 countries and 6 continents.
- **Attributes (9 variables):**
  - Categoricals (3): `Area`, `Continent`, `Item`
  - Temporals/Splits (2): `Season`, `Year`
  - Environmental / Inputs (3): `average_rain_fall_mm_per_year`, `pesticides_tonnes`, `avg_temp`
  - Target (1): `hg/ha_yield`
  - *Note on Absence:* Relative humidity was NOT collected in the original dataset and is strictly excluded from all models and documentation.

---

## 3. Evaluated Model Zoo & Architecture
- **Reference Paper Models (aligned with El-Kenawy et al., 2025):**
  1. K-Nearest Neighbors (KNN Regressor)
  2. Gradient Boosting Regressor (GBR)
  3. XGBoost Regressor (XGB)
  4. Multilayer Perceptron (MLP Regressor)
- **Additional Baseline Model:**
  5. Linear Regression (Ordinary Least Squares)

---

## 4. Empirical Evaluation Benchmark (Hold-Out Test Year: 2013)

### Kharif Season
| Model | RMSE (hg/ha) | MAE (hg/ha) | R² Score | Pearson r | Selection Status |
|:---|:---:|:---:|:---:|:---:|:---:|
| **KNN Regressor (Tuned)** | **14,026.44** | **6,681.12** | **0.9380** | **0.9688** | **Selected Champion (k=3, p=2, distance)** |
| XGBoost Regressor | 17,235.88 | 9,779.95 | 0.9064 | 0.9533 | Paper Candidate |
| Gradient Boosting | 22,679.27 | 14,818.38 | 0.8379 | 0.9278 | Paper Candidate |
| MLP Regressor | 28,734.16 | 17,988.13 | 0.7398 | 0.8635 | Paper Candidate |
| Linear Regression | 32,099.53 | 20,507.06 | 0.6753 | 0.8305 | Additional Baseline |

### Rabi Season
| Model | RMSE (hg/ha) | MAE (hg/ha) | R² Score | Pearson r | Selection Status |
|:---|:---:|:---:|:---:|:---:|:---:|
| **KNN Regressor (Tuned)** | **4,065.82** | **3,184.93** | **0.9636** | **0.9868** | **Selected Champion (k=7, p=1, distance)** |
| XGBoost Regressor | 5,649.94 | 4,456.27 | 0.9297 | 0.9678 | Paper Candidate |
| Linear Regression | 6,182.82 | 4,554.99 | 0.9158 | 0.9592 | Additional Baseline |
| Gradient Boosting | 8,621.76 | 7,386.21 | 0.8362 | 0.9333 | Paper Candidate |
| MLP Regressor | 13,787.41 | 9,815.03 | 0.5812 | 0.7987 | Paper Candidate |

### Seasonal / Whole-Year
| Model | RMSE (hg/ha) | MAE (hg/ha) | R² Score | Pearson r | Selection Status |
|:---|:---:|:---:|:---:|:---:|:---:|
| **KNN Regressor (Tuned)** | **19,646.94** | **9,630.07** | **0.9642** | **0.9827** | **Selected Champion (k=3, p=1, distance)** |
| XGBoost Regressor | 25,933.82 | 15,245.57 | 0.9377 | 0.9698 | Paper Candidate |
| Gradient Boosting | 44,947.15 | 29,792.24 | 0.8127 | 0.9149 | Paper Candidate |
| MLP Regressor | 48,214.55 | 34,303.93 | 0.7845 | 0.8870 | Paper Candidate |
| Linear Regression | 52,357.50 | 36,511.22 | 0.7459 | 0.8674 | Additional Baseline |
