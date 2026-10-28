import os
import json
import joblib
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, median_absolute_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
import xgboost as xgb

os.makedirs('results/faculty_revision', exist_ok=True)
os.makedirs('figures/faculty_revision', exist_ok=True)

# 1. Load Data
df_k = pd.read_csv('data/processed/processed_kharif.csv')
df_r = pd.read_csv('data/processed/processed_rabi.csv')
df_s = pd.read_csv('data/processed/processed_seasonal.csv')

df_k['Season_Group'] = 'Kharif'
df_r['Season_Group'] = 'Rabi'
df_s['Season_Group'] = 'Seasonal'

df_comb = pd.concat([df_k, df_r, df_s], ignore_index=True)

feature_cols = ['Area', 'Continent', 'Item', 'Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']
cat_cols = ['Area', 'Continent', 'Item']
num_cols = ['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']

# Model hyperparameters from verified project settings
MODEL_SPECS = {
    'Kharif': {
        'KNN': {'k': 3, 'p': 2, 'weights': 'distance'},
        'XGB': {'n_estimators': 150, 'learning_rate': 0.05, 'max_depth': 7},
        'GBR': {'n_estimators': 150, 'learning_rate': 0.05, 'max_depth': 4},
        'MLP': {'hidden_layer_sizes': (64, 32), 'max_iter': 200, 'random_state': 42}
    },
    'Rabi': {
        'KNN': {'k': 7, 'p': 1, 'weights': 'distance'},
        'XGB': {'n_estimators': 150, 'learning_rate': 0.05, 'max_depth': 6},
        'GBR': {'n_estimators': 150, 'learning_rate': 0.05, 'max_depth': 3},
        'MLP': {'hidden_layer_sizes': (64, 32), 'max_iter': 200, 'random_state': 42}
    },
    'Seasonal': {
        'KNN': {'k': 3, 'p': 1, 'weights': 'distance'},
        'XGB': {'n_estimators': 150, 'learning_rate': 0.05, 'max_depth': 8},
        'GBR': {'n_estimators': 150, 'learning_rate': 0.05, 'max_depth': 4},
        'MLP': {'hidden_layer_sizes': (64, 32), 'max_iter': 200, 'random_state': 42}
    }
}

def get_pipeline(model_name, season):
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols),
            ('num', StandardScaler(), num_cols)
        ]
    )
    if model_name == 'KNN':
        cfg = MODEL_SPECS[season]['KNN']
        reg = KNeighborsRegressor(n_neighbors=cfg['k'], p=cfg['p'], weights=cfg['weights'])
    elif model_name == 'XGBoost':
        cfg = MODEL_SPECS[season]['XGB']
        reg = xgb.XGBRegressor(**cfg, random_state=42)
    elif model_name == 'Gradient Boosting':
        cfg = MODEL_SPECS[season]['GBR']
        reg = GradientBoostingRegressor(**cfg, random_state=42)
    elif model_name == 'MLP':
        cfg = MODEL_SPECS[season]['MLP']
        reg = MLPRegressor(**cfg)
    elif model_name == 'Linear Regression':
        reg = LinearRegression()
    else:
        raise ValueError(f"Unknown model {model_name}")
        
    return Pipeline([('preprocessor', preprocessor), ('regressor', reg)])

# -------------------------------------------------------------
# 1. SECTION 6.1: DESCRIPTIVE STATISTICS TABLE
# -------------------------------------------------------------
print("--- Computing Section 6.1: Descriptive Statistics ---")
desc_stats = []
vars_to_summarize = [
    ('hg/ha_yield', 'Yield (hg/ha)'),
    ('average_rain_fall_mm_per_year', 'Rainfall (mm/yr)'),
    ('avg_temp', 'Temperature (°C)'),
    ('pesticides_tonnes', 'Pesticides (tonnes)')
]

for s_name, df in [('Kharif', df_k), ('Rabi', df_r), ('Seasonal', df_s), ('Combined', df_comb)]:
    n_countries = df['Area'].nunique()
    n_crops = df['Item'].nunique()
    total_n = len(df)
    
    for col, display_name in vars_to_summarize:
        s = df[col].dropna()
        q75, q25 = np.percentile(s, [75, 25])
        iqr = q75 - q25
        desc_stats.append({
            'Variable': display_name,
            'Season': s_name,
            'N': int(len(s)),
            'Mean': float(s.mean()),
            'Median': float(s.median()),
            'SD': float(s.std()),
            'IQR': float(iqr),
            'Min': float(s.min()),
            'Max': float(s.max()),
            'Skewness': float(stats.skew(s)),
            'Countries': int(n_countries),
            'Crops': int(n_crops)
        })

df_desc_table = pd.DataFrame(desc_stats)
df_desc_table.to_json('results/faculty_revision/descriptive_statistics.json', orient='records', indent=2)

# -------------------------------------------------------------
# 2. SECTION 6.2: QUANTITATIVE DISTRIBUTION SHIFT (TRAIN vs 2013)
# -------------------------------------------------------------
print("--- Computing Section 6.2: Temporal Distribution Shift ---")
dist_shifts = []
shift_vars = [
    ('hg/ha_yield', 'Yield (hg/ha)'),
    ('average_rain_fall_mm_per_year', 'Rainfall (mm/yr)'),
    ('avg_temp', 'Temperature (°C)'),
    ('pesticides_tonnes', 'Pesticides (tonnes)')
]

for s_name, df in [('Kharif', df_k), ('Rabi', df_r), ('Seasonal', df_s), ('Combined', df_comb)]:
    train = df[df['Year'] <= 2012]
    test = df[df['Year'] == 2013]
    
    for col, display_name in shift_vars:
        tr = train[col].dropna()
        te = test[col].dropna()
        ks_res = stats.ks_2samp(tr, te)
        w_dist = stats.wasserstein_distance(tr, te)
        pct_change = ((te.mean() - tr.mean()) / tr.mean()) * 100
        # Standardized Mean Difference (Cohen's d)
        pooled_sd = np.sqrt(((len(tr)-1)*tr.var() + (len(te)-1)*te.var()) / (len(tr)+len(te)-2))
        smd = (te.mean() - tr.mean()) / pooled_sd if pooled_sd > 0 else 0
        
        dist_shifts.append({
            'Season': s_name,
            'Feature': display_name,
            'Train_Mean': float(tr.mean()),
            'Train_SD': float(tr.std()),
            'Holdout_2013_Mean': float(te.mean()),
            'Holdout_2013_SD': float(te.std()),
            'Pct_Mean_Change': float(pct_change),
            'Standardized_Mean_Diff': float(smd),
            'KS_Statistic': float(ks_res.statistic),
            'KS_p_value': float(ks_res.pvalue),
            'Wasserstein_Distance': float(w_dist)
        })

df_shift_table = pd.DataFrame(dist_shifts)
df_shift_table.to_json('results/faculty_revision/distribution_shift.json', orient='records', indent=2)

# -------------------------------------------------------------
# 3. SECTION 6.3: MODEL PERFORMANCE + 95% BOOTSTRAP CONFIDENCE INTERVALS
# -------------------------------------------------------------
print("--- Computing Section 6.3: Model Performance with Bootstrap CIs ---")
np.random.seed(42)
N_BOOTSTRAP = 1000

model_list = ['KNN', 'XGBoost', 'Gradient Boosting', 'MLP', 'Linear Regression']
model_perf_with_ci = []

# Fit and evaluate models on 2013 holdout
for s_name, df in [('Kharif', df_k), ('Rabi', df_r), ('Seasonal', df_s)]:
    train = df[df['Year'] <= 2012].reset_index(drop=True)
    test = df[df['Year'] == 2013].reset_index(drop=True)
    y_test = test['hg/ha_yield'].values
    y_mean = float(np.mean(y_test))
    y_range = float(np.max(y_test) - np.min(y_test))
    
    for m_name in model_list:
        pipe = get_pipeline(m_name, s_name)
        pipe.fit(train[feature_cols], train['hg/ha_yield'])
        preds = pipe.predict(test[feature_cols])
        
        # Point metrics
        rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
        mae = float(mean_absolute_error(y_test, preds))
        r2 = float(r2_score(y_test, preds))
        r = float(stats.pearsonr(y_test, preds)[0])
        med_ae = float(median_absolute_error(y_test, preds))
        mbe = float(np.mean(preds - y_test)) # Mean bias error
        nrmse_mean = float(rmse / y_mean) # Normalized RMSE by mean
        nrmse_range = float(rmse / y_range) # Normalized RMSE by range
        
        # Bootstrap CIs
        b_rmse, b_mae, b_r2 = [], [], []
        n_pts = len(y_test)
        for _ in range(N_BOOTSTRAP):
            boot_idx = np.random.choice(n_pts, size=n_pts, replace=True)
            yb = y_test[boot_idx]
            pb = preds[boot_idx]
            b_rmse.append(np.sqrt(mean_squared_error(yb, pb)))
            b_mae.append(mean_absolute_error(yb, pb))
            # Handle possible zero variance edge case
            if np.std(yb) > 0:
                b_r2.append(r2_score(yb, pb))
            else:
                b_r2.append(1.0)
                
        rmse_ci = [float(np.percentile(b_rmse, 2.5)), float(np.percentile(b_rmse, 97.5))]
        mae_ci = [float(np.percentile(b_mae, 2.5)), float(np.percentile(b_mae, 97.5))]
        r2_ci = [float(np.percentile(b_r2, 2.5)), float(np.percentile(b_r2, 97.5))]
        
        model_perf_with_ci.append({
            'Season': s_name,
            'Model': m_name,
            'RMSE': rmse,
            'RMSE_CI_lower': rmse_ci[0],
            'RMSE_CI_upper': rmse_ci[1],
            'MAE': mae,
            'MAE_CI_lower': mae_ci[0],
            'MAE_CI_upper': mae_ci[1],
            'R2': r2,
            'R2_CI_lower': r2_ci[0],
            'R2_CI_upper': r2_ci[1],
            'Pearson_r': r,
            'MedAE': med_ae,
            'MBE': mbe,
            'NRMSE_mean': nrmse_mean,
            'NRMSE_range': nrmse_range
        })

df_perf = pd.DataFrame(model_perf_with_ci)
# Assign numeric rank within season based on RMSE
df_perf['Rank'] = df_perf.groupby('Season')['RMSE'].rank(ascending=True).astype(int)
df_perf = df_perf.sort_values(by=['Season', 'Rank'])
df_perf.to_json('results/faculty_revision/prospective_performance_with_ci.json', orient='records', indent=2)

# -------------------------------------------------------------
# 4. SECTION 6.5: MULTI-MODEL ROLLING-ORIGIN TEMPORAL VALIDATION
# -------------------------------------------------------------
print("--- Computing Section 6.5: Multi-Model Rolling Origin Validation ---")
rolling_all = []
cutoffs = [2010, 2011, 2012, 2013]

for s_name, df in [('Kharif', df_k), ('Rabi', df_r), ('Seasonal', df_s)]:
    for yr in cutoffs:
        train = df[df['Year'] < yr]
        test = df[df['Year'] == yr]
        if len(test) == 0:
            continue
        y_test = test['hg/ha_yield'].values
        
        for m_name in ['KNN', 'XGBoost', 'Linear Regression']:
            pipe = get_pipeline(m_name, s_name)
            pipe.fit(train[feature_cols], train['hg/ha_yield'])
            preds = pipe.predict(test[feature_cols])
            
            rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
            mae = float(mean_absolute_error(y_test, preds))
            r2 = float(r2_score(y_test, preds))
            r = float(stats.pearsonr(y_test, preds)[0]) if np.std(preds) > 0 else 0
            
            rolling_all.append({
                'Season': s_name,
                'Cutoff_Year': yr,
                'Model': m_name,
                'N_Test': int(len(test)),
                'RMSE': rmse,
                'MAE': mae,
                'R2': r2,
                'Pearson_r': r
            })

df_rolling = pd.DataFrame(rolling_all)
# Summary mean +- SD per season & model
rolling_summary = []
for (s_name, m_name), grp in df_rolling.groupby(['Season', 'Model']):
    rolling_summary.append({
        'Season': s_name,
        'Model': m_name,
        'Mean_RMSE': float(grp['RMSE'].mean()),
        'SD_RMSE': float(grp['RMSE'].std()),
        'Mean_MAE': float(grp['MAE'].mean()),
        'SD_MAE': float(grp['MAE'].std()),
        'Mean_R2': float(grp['R2'].mean()),
        'SD_R2': float(grp['R2'].std())
    })

pd.DataFrame(rolling_all).to_json('results/faculty_revision/rolling_origin_folds.json', orient='records', indent=2)
pd.DataFrame(rolling_summary).to_json('results/faculty_revision/rolling_origin_summary.json', orient='records', indent=2)

# -------------------------------------------------------------
# 5. SECTION 6.6: RANDOM VS CHRONOLOGICAL VALIDATION (ALL 5 MODELS)
# -------------------------------------------------------------
print("--- Computing Section 6.6: Random vs Chronological Validation ---")
rand_chrono_all = []

for s_name, df in [('Kharif', df_k), ('Rabi', df_r), ('Seasonal', df_s)]:
    # Chronological: train <= 2012, test 2013
    train_c = df[df['Year'] <= 2012].reset_index(drop=True)
    test_c = df[df['Year'] == 2013].reset_index(drop=True)
    test_frac = len(test_c) / len(df)
    
    # Random split
    train_r, test_r = train_test_split(df, test_size=test_frac, random_state=42)
    train_r = train_r.reset_index(drop=True)
    test_r = test_r.reset_index(drop=True)
    
    for m_name in model_list:
        # Chrono fit
        pipe_c = get_pipeline(m_name, s_name)
        pipe_c.fit(train_c[feature_cols], train_c['hg/ha_yield'])
        pred_c = pipe_c.predict(test_c[feature_cols])
        rmse_c = float(np.sqrt(mean_squared_error(test_c['hg/ha_yield'], pred_c)))
        mae_c = float(mean_absolute_error(test_c['hg/ha_yield'], pred_c))
        r2_c = float(r2_score(test_c['hg/ha_yield'], pred_c))
        
        # Random fit
        pipe_r = get_pipeline(m_name, s_name)
        pipe_r.fit(train_r[feature_cols], train_r['hg/ha_yield'])
        pred_r = pipe_r.predict(test_r[feature_cols])
        rmse_r = float(np.sqrt(mean_squared_error(test_r['hg/ha_yield'], pred_r)))
        mae_r = float(mean_absolute_error(test_r['hg/ha_yield'], pred_r))
        r2_r = float(r2_score(test_r['hg/ha_yield'], pred_r))
        
        # Delta & Optimism
        rmse_optimism_pct = float(((rmse_c - rmse_r) / rmse_c) * 100)
        r2_gain = float(r2_r - r2_c)
        
        rand_chrono_all.append({
            'Season': s_name,
            'Model': m_name,
            'Chrono_RMSE': rmse_c,
            'Chrono_MAE': mae_c,
            'Chrono_R2': r2_c,
            'Random_RMSE': rmse_r,
            'Random_MAE': mae_r,
            'Random_R2': r2_r,
            'RMSE_Optimism_Pct': rmse_optimism_pct,
            'R2_Inflation': r2_gain
        })

pd.DataFrame(rand_chrono_all).to_json('results/faculty_revision/random_vs_chronological_all.json', orient='records', indent=2)

# -------------------------------------------------------------
# 6. SECTION 6.7: SEASON-SPECIFIC VS POOLED MODEL (ALL 3 SEASONS + ERROR PENALTY FORMULA)
# -------------------------------------------------------------
print("--- Computing Section 6.7: Season-Specific vs Pooled Model ---")
# Fit pooled KNN on combined train
train_comb = df_comb[df_comb['Year'] <= 2012].reset_index(drop=True)
pooled_features = ['Area', 'Continent', 'Item', 'Season_Group', 'Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']
pooled_cats = ['Area', 'Continent', 'Item', 'Season_Group']
pooled_nums = ['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']

pipe_pooled = Pipeline([
    ('preprocessor', ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), pooled_cats),
        ('num', StandardScaler(), pooled_nums)
    ])),
    ('regressor', KNeighborsRegressor(n_neighbors=5, p=1, weights='distance'))
])
pipe_pooled.fit(train_comb[pooled_features], train_comb['hg/ha_yield'])

pooled_comparison = []
for s_name, df, k, p in [('Kharif', df_k, 3, 2), ('Rabi', df_r, 7, 1), ('Seasonal', df_s, 3, 1)]:
    test = df[df['Year'] == 2013].reset_index(drop=True)
    y_true = test['hg/ha_yield'].values
    
    # Specific model
    pipe_spec = get_pipeline('KNN', s_name)
    train_spec = df[df['Year'] <= 2012].reset_index(drop=True)
    pipe_spec.fit(train_spec[feature_cols], train_spec['hg/ha_yield'])
    pred_spec = pipe_spec.predict(test[feature_cols])
    
    rmse_spec = float(np.sqrt(mean_squared_error(y_true, pred_spec)))
    mae_spec = float(mean_absolute_error(y_true, pred_spec))
    r2_spec = float(r2_score(y_true, pred_spec))
    
    # Pooled model
    pred_pool = pipe_pooled.predict(test[pooled_features])
    rmse_pool = float(np.sqrt(mean_squared_error(y_true, pred_pool)))
    mae_pool = float(mean_absolute_error(y_true, pred_pool))
    r2_pool = float(r2_score(y_true, pred_pool))
    
    # Error penalty formula: (RMSE_pooled - RMSE_spec) / RMSE_spec * 100
    penalty_pct = float(((rmse_pool - rmse_spec) / rmse_spec) * 100)
    
    # Statistical test on paired absolute errors
    err_spec = np.abs(y_true - pred_spec)
    err_pool = np.abs(y_true - pred_pool)
    w_stat, w_pval = stats.wilcoxon(err_spec, err_pool)
    t_stat, t_pval = stats.ttest_rel(err_spec, err_pool)
    
    pooled_comparison.append({
        'Season': s_name,
        'Specific_RMSE': rmse_spec,
        'Specific_MAE': mae_spec,
        'Specific_R2': r2_spec,
        'Pooled_RMSE': rmse_pool,
        'Pooled_MAE': mae_pool,
        'Pooled_R2': r2_pool,
        'RMSE_Error_Penalty_Pct': penalty_pct,
        'Wilcoxon_Stat': float(w_stat),
        'Wilcoxon_p_value': float(w_pval),
        'Paired_t_Stat': float(t_stat),
        'Paired_t_p_value': float(t_pval)
    })

pd.DataFrame(pooled_comparison).to_json('results/faculty_revision/pooled_vs_specific.json', orient='records', indent=2)

# -------------------------------------------------------------
# 7. SECTION 6.9: HISTORICAL-NEIGHBORHOOD ANALYSIS + WORKED EXAMPLES
# -------------------------------------------------------------
print("--- Computing Section 6.9: Historical Neighborhood Details & 3 Examples ---")
neighbor_details = {}
worked_examples_3 = {}

for s_name, df, k, p in [('Kharif', df_k, 3, 2), ('Rabi', df_r, 7, 1), ('Seasonal', df_s, 3, 1)]:
    train = df[df['Year'] <= 2012].reset_index(drop=True)
    test = df[df['Year'] == 2013].reset_index(drop=True)
    
    pipe = get_pipeline('KNN', s_name)
    pipe.fit(train[feature_cols], train['hg/ha_yield'])
    
    preproc = pipe.named_steps['preprocessor']
    reg = pipe.named_steps['regressor']
    
    X_train_trans = preproc.transform(train[feature_cols])
    X_test_trans = preproc.transform(test[feature_cols])
    
    distances, indices = reg.kneighbors(X_test_trans)
    preds = pipe.predict(test[feature_cols])
    y_true = test['hg/ha_yield'].values
    errors = np.abs(y_true - preds)
    
    mean_dist = np.mean(distances, axis=1)
    
    # Correlation with 95% CI and p-value
    r_val, p_val = stats.pearsonr(mean_dist, errors)
    # Fisher z-transformation for CI
    z = np.arctanh(r_val)
    se = 1.0 / np.sqrt(len(test) - 3)
    z_ci = [z - 1.96*se, z + 1.96*se]
    r_ci = [float(np.tanh(z_ci[0])), float(np.tanh(z_ci[1]))]
    
    # Impact of k on distance and error
    k_eval = []
    for test_k in [1, 3, 5, 7, 9, 15]:
        reg_k = KNeighborsRegressor(n_neighbors=test_k, p=p, weights='distance')
        reg_k.fit(X_train_trans, train['hg/ha_yield'])
        p_k = reg_k.predict(X_test_trans)
        rmse_k = np.sqrt(mean_squared_error(y_true, p_k))
        mae_k = mean_absolute_error(y_true, p_k)
        r2_k = r2_score(y_true, p_k)
        k_eval.append({'k': test_k, 'RMSE': float(rmse_k), 'MAE': float(mae_k), 'R2': float(r2_k)})
        
    neighbor_details[s_name] = {
        'mean_distance': float(np.mean(mean_dist)),
        'median_distance': float(np.median(mean_dist)),
        'std_distance': float(np.std(mean_dist)),
        'pearson_r_dist_vs_error': float(r_val),
        'r_p_value': float(p_val),
        'r_95_CI': r_ci,
        'k_sensitivity': k_eval
    }
    
    # 3 Worked Examples: High Confidence (low distance, low error), Medium Confidence, Low Confidence (high distance)
    # Sort test indices by mean_dist
    sorted_by_dist = np.argsort(mean_dist)
    high_idx = sorted_by_dist[0] # Lowest distance
    med_idx = sorted_by_dist[len(sorted_by_dist)//2] # Median distance
    low_idx = sorted_by_dist[-1] # Highest distance
    
    examples = []
    for tier_name, ex_idx in [('High Confidence (Tight Analogs)', high_idx),
                               ('Medium Confidence (Typical Analogs)', med_idx),
                               ('Low Confidence (Sparse Analogs)', low_idx)]:
        q_row = test.iloc[ex_idx]
        q_dist = distances[ex_idx]
        q_neigh_idx = indices[ex_idx]
        q_neigh = train.iloc[q_neigh_idx]
        
        # Distance weighting: w_i = 1 / (d_i + 1e-10)
        w = 1.0 / (q_dist + 1e-10)
        w_norm = w / np.sum(w)
        manual_pred = np.sum(w_norm * q_neigh['hg/ha_yield'].values)
        
        neighbors_list = []
        for rank_i, (_, n_r) in enumerate(q_neigh.iterrows()):
            neighbors_list.append({
                'Neighbor_Rank': rank_i + 1,
                'Country': n_r['Area'],
                'Crop': n_r['Item'],
                'Year': int(n_r['Year']),
                'Distance': float(q_dist[rank_i]),
                'Observed_Yield': float(n_r['hg/ha_yield']),
                'Normalized_Weight': float(w_norm[rank_i])
            })
            
        examples.append({
            'Tier': tier_name,
            'Query': {
                'Country': q_row['Area'],
                'Crop': q_row['Item'],
                'Year': int(q_row['Year']),
                'Rainfall': float(q_row['average_rain_fall_mm_per_year']),
                'Temperature': float(q_row['avg_temp']),
                'Pesticides': float(q_row['pesticides_tonnes']),
                'Actual_Yield': float(q_row['hg/ha_yield']),
                'Model_Predicted_Yield': float(preds[ex_idx]),
                'Manual_Weighted_Yield': float(manual_pred),
                'Mean_Neighbor_Distance': float(mean_dist[ex_idx]),
                'Absolute_Error': float(errors[ex_idx]),
                'Percentage_Error': float((errors[ex_idx] / q_row['hg/ha_yield']) * 100)
            },
            'Retrieved_Neighbors': neighbors_list
        })
    worked_examples_3[s_name] = examples

with open('results/faculty_revision/neighbor_metrics.json', 'w') as f:
    json.dump({'metrics': neighbor_details, 'worked_examples': worked_examples_3}, f, indent=2)

# -------------------------------------------------------------
# 8. SECTION 6.11: FEATURE INTERACTION (RAINFALL x TEMP REGRESSION & 2D SURFACE)
# -------------------------------------------------------------
print("--- Computing Section 6.11: Rainfall x Temperature Interaction ---")
def run_ols(X_mat, y_vec, col_names):
    n, p = X_mat.shape
    beta = np.linalg.pinv(X_mat.T @ X_mat) @ (X_mat.T @ y_vec)
    preds = X_mat @ beta
    residuals = y_vec - preds
    s2 = np.sum(residuals**2) / (n - p)
    cov_beta = s2 * np.linalg.pinv(X_mat.T @ X_mat)
    se = np.sqrt(np.maximum(0, np.diag(cov_beta)))
    t_vals = beta / np.maximum(se, 1e-12)
    p_vals = 2 * (1 - stats.t.cdf(np.abs(t_vals), df=n-p))
    r2 = 1.0 - (np.sum(residuals**2) / np.sum((y_vec - np.mean(y_vec))**2))
    return {
        'params': dict(zip(col_names, beta)),
        'pvalues': dict(zip(col_names, p_vals)),
        'se': dict(zip(col_names, se)),
        'r2': float(r2)
    }

interaction_results = {}
for s_name, df in [('Kharif', df_k), ('Rabi', df_r), ('Seasonal', df_s)]:
    rain = df['average_rain_fall_mm_per_year'].values
    temp = df['avg_temp'].values
    inter = rain * temp
    ones = np.ones(len(df))
    X_mat = np.column_stack([ones, rain, temp, inter])
    y_reg = df['hg/ha_yield'].values
    
    ols_res = run_ols(X_mat, y_reg, ['const', 'Rainfall', 'Temperature', 'Rain_x_Temp'])
    interaction_results[s_name] = {
        'b0_const': float(ols_res['params']['const']),
        'b1_rain': float(ols_res['params']['Rainfall']),
        'b2_temp': float(ols_res['params']['Temperature']),
        'b3_interaction': float(ols_res['params']['Rain_x_Temp']),
        'b3_pvalue': float(ols_res['pvalues']['Rain_x_Temp']),
        'r2': float(ols_res['r2'])
    }

with open('results/faculty_revision/feature_interaction.json', 'w') as f:
    json.dump(interaction_results, f, indent=2)

# -------------------------------------------------------------
# 9. SECTION 6.12: CROP ERROR & SAMPLE DENSITY REGRESSION
# -------------------------------------------------------------
print("--- Computing Section 6.12: Subgroup Analysis & Density Regression ---")
crop_density_analysis = []
for s_name, df in [('Kharif', df_k), ('Rabi', df_r), ('Seasonal', df_s)]:
    train = df[df['Year'] <= 2012]
    test = df[df['Year'] == 2013].copy()
    
    pipe = get_pipeline('KNN', s_name)
    pipe.fit(train[feature_cols], train['hg/ha_yield'])
    test['preds'] = pipe.predict(test[feature_cols])
    test['abs_err'] = np.abs(test['hg/ha_yield'] - test['preds'])
    test['sq_err'] = (test['hg/ha_yield'] - test['preds'])**2
    
    train_crop_counts = train['Item'].value_counts().to_dict()
    
    for crop, grp in test.groupby('Item'):
        n_train = train_crop_counts.get(crop, 0)
        n_test = len(grp)
        mean_y = float(grp['hg/ha_yield'].mean())
        mae = float(grp['abs_err'].mean())
        rmse = float(np.sqrt(grp['sq_err'].mean()))
        rel_err = float((mae / mean_y) * 100) if mean_y > 0 else 0
        r2 = float(r2_score(grp['hg/ha_yield'], grp['preds'])) if len(grp) > 3 and grp['hg/ha_yield'].std() > 0 else None
        
        crop_density_analysis.append({
            'Season': s_name,
            'Crop': crop,
            'Test_N': n_test,
            'Train_Frequency': n_train,
            'Train_Share_Pct': float((n_train / len(train)) * 100),
            'Mean_Yield': mean_y,
            'MAE': mae,
            'RMSE': rmse,
            'R2': r2,
            'Relative_Error_Pct': rel_err
        })

df_crop_err = pd.DataFrame(crop_density_analysis)

# Regress MAE on log(Train_Frequency) across crops
X_dens = np.column_stack([np.ones(len(df_crop_err)), np.log(df_crop_err['Train_Frequency'].values)])
y_dens = df_crop_err['MAE'].values
res_dens = run_ols(X_dens, y_dens, ['const', 'log_N'])
density_reg_summary = {
    'b0_const': float(res_dens['params']['const']),
    'b1_log_N': float(res_dens['params']['log_N']),
    'pvalue': float(res_dens['pvalues']['log_N']),
    'r2': float(res_dens['r2']),
    'n_crops': int(len(df_crop_err))
}

with open('results/faculty_revision/crop_subgroup_analysis.json', 'w') as f:
    json.dump({'crop_table': crop_density_analysis, 'sample_density_regression': density_reg_summary}, f, indent=2)

# -------------------------------------------------------------
# 10. SECTION 6.13: SYSTEMATIC FEATURE ABLATION (ALL SEASONS)
# -------------------------------------------------------------
print("--- Computing Section 6.13: Systematic Feature Ablation ---")
ablation_groups = {
    'None (Full Pipeline)': feature_cols,
    'Crop': ['Area', 'Continent', 'Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp'],
    'Geographic': ['Item', 'Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp'],
    'Climate': ['Area', 'Continent', 'Item', 'Year', 'pesticides_tonnes'],
    'Pesticide': ['Area', 'Continent', 'Item', 'Year', 'average_rain_fall_mm_per_year', 'avg_temp'],
    'Crop + Geographic': ['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp'],
    'Climate + Pesticide': ['Area', 'Continent', 'Item', 'Year']
}

ablation_table = []
for s_name, df, k, p in [('Kharif', df_k, 3, 2), ('Rabi', df_r, 7, 1), ('Seasonal', df_s, 3, 1)]:
    train = df[df['Year'] <= 2012]
    test = df[df['Year'] == 2013]
    y_test = test['hg/ha_yield'].values
    
    # Full baseline
    base_pipe = Pipeline([
        ('preprocessor', ColumnTransformer([
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols),
            ('num', StandardScaler(), num_cols)
        ])),
        ('regressor', KNeighborsRegressor(n_neighbors=k, p=p, weights='distance'))
    ])
    base_pipe.fit(train[feature_cols], train['hg/ha_yield'])
    base_preds = base_pipe.predict(test[feature_cols])
    base_rmse = np.sqrt(mean_squared_error(y_test, base_preds))
    base_r2 = r2_score(y_test, base_preds)
    
    for g_name, cols in ablation_groups.items():
        cur_cats = [c for c in cat_cols if c in cols]
        cur_nums = [c for c in num_cols if c in cols]
        
        pipe = Pipeline([
            ('preprocessor', ColumnTransformer([
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cur_cats),
                ('num', StandardScaler(), cur_nums)
            ])),
            ('regressor', KNeighborsRegressor(n_neighbors=k, p=p, weights='distance'))
        ])
        pipe.fit(train[cols], train['hg/ha_yield'])
        preds = pipe.predict(test[cols])
        
        rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
        mae = float(mean_absolute_error(y_test, preds))
        r2 = float(r2_score(y_test, preds))
        
        delta_r2 = float(r2 - base_r2)
        delta_rmse = float(rmse - base_rmse)
        
        ablation_table.append({
            'Season': s_name,
            'Feature_Group_Removed': g_name,
            'R2': r2,
            'Delta_R2': delta_r2,
            'RMSE': rmse,
            'Delta_RMSE': delta_rmse,
            'MAE': mae
        })

pd.DataFrame(ablation_table).to_json('results/faculty_revision/systematic_ablation.json', orient='records', indent=2)

# -------------------------------------------------------------
# 11. SECTION 6.14: FORMAL UNCERTAINTY & PREDICTION INTERVAL COVERAGE
# -------------------------------------------------------------
print("--- Computing Section 6.14: Prediction Intervals & Empirical Coverage ---")
uncertainty_metrics = []

for s_name, df, k, p in [('Kharif', df_k, 3, 2), ('Rabi', df_r, 7, 1), ('Seasonal', df_s, 3, 1)]:
    train = df[df['Year'] <= 2012].reset_index(drop=True)
    test = df[df['Year'] == 2013].reset_index(drop=True)
    
    pipe = get_pipeline('KNN', s_name)
    pipe.fit(train[feature_cols], train['hg/ha_yield'])
    preproc = pipe.named_steps['preprocessor']
    reg = pipe.named_steps['regressor']
    
    X_train_trans = preproc.transform(train[feature_cols])
    X_test_trans = preproc.transform(test[feature_cols])
    
    distances, indices = reg.kneighbors(X_test_trans)
    y_test = test['hg/ha_yield'].values
    
    covered_90 = 0
    covered_95 = 0
    widths_90 = []
    
    for i, idx_list in enumerate(indices):
        y_neigh = train.loc[idx_list, 'hg/ha_yield'].values
        # Empirical prediction interval based on neighbor dispersion
        # For small k, interval spanned by min and max plus sample t-distribution margin
        y_mean_n = np.mean(y_neigh)
        y_std_n = np.std(y_neigh, ddof=1) if len(y_neigh) > 1 else 0
        t_val_90 = stats.t.ppf(0.95, df=k-1) if k > 1 else 1.645
        
        # 90% PI
        half_width_90 = t_val_90 * np.sqrt(y_std_n**2 + (y_std_n/np.sqrt(k))**2 + 1e-4)
        low_90 = y_mean_n - half_width_90
        high_90 = y_mean_n + half_width_90
        widths_90.append(high_90 - low_90)
        
        if low_90 <= y_test[i] <= high_90:
            covered_90 += 1
            
    cov_rate_90 = float(covered_90 / len(test))
    mean_w = float(np.mean(widths_90))
    med_w = float(np.median(widths_90))
    
    uncertainty_metrics.append({
        'Season': s_name,
        'Nominal_Interval': '90%',
        'N_Holdout': int(len(test)),
        'Empirical_Coverage_Rate': cov_rate_90,
        'Mean_Interval_Width_hg_ha': mean_w,
        'Median_Interval_Width_hg_ha': med_w,
        'Calibration_Bias': float(cov_rate_90 - 0.90)
    })

pd.DataFrame(uncertainty_metrics).to_json('results/faculty_revision/prediction_intervals.json', orient='records', indent=2)

# -------------------------------------------------------------
# 12. SECTION 6.15: STATISTICAL COMPARISONS & MULTIPLE TESTING CORRECTION
# -------------------------------------------------------------
print("--- Computing Section 6.15: Statistical Comparisons with Holm Correction ---")
stat_tests = []

for s_name, df, k, p in [('Kharif', df_k, 3, 2), ('Rabi', df_r, 7, 1), ('Seasonal', df_s, 3, 1)]:
    train = df[df['Year'] <= 2012].reset_index(drop=True)
    test = df[df['Year'] == 2013].reset_index(drop=True)
    y_test = test['hg/ha_yield'].values
    
    pipe_knn = get_pipeline('KNN', s_name)
    pipe_knn.fit(train[feature_cols], train['hg/ha_yield'])
    e_knn = np.abs(y_test - pipe_knn.predict(test[feature_cols]))
    
    # Compare with each competitor
    comparisons = ['XGBoost', 'Gradient Boosting', 'MLP', 'Linear Regression']
    p_vals_raw = []
    temp_res = []
    
    for comp_m in comparisons:
        pipe_comp = get_pipeline(comp_m, s_name)
        pipe_comp.fit(train[feature_cols], train['hg/ha_yield'])
        e_comp = np.abs(y_test - pipe_comp.predict(test[feature_cols]))
        
        diff = e_knn - e_comp
        t_stat, t_pval = stats.ttest_rel(e_knn, e_comp)
        w_stat, w_pval = stats.wilcoxon(e_knn, e_comp)
        
        # Effect sizes:
        # Cohen's d for paired differences
        d_val = float(np.mean(diff) / np.std(diff, ddof=1)) if np.std(diff, ddof=1) > 0 else 0
        # Rank-biserial correlation: r_rb = 1 - 2*W / (N*(N+1)/2)
        n_pairs = len(diff)
        w_max = n_pairs * (n_pairs + 1) / 2
        r_rb = float(1 - (2 * w_stat / w_max))
        # Percent error reduction: (mean(e_comp) - mean(e_knn)) / mean(e_comp) * 100
        reduction_pct = float(((np.mean(e_comp) - np.mean(e_knn)) / np.mean(e_comp)) * 100)
        
        # 95% CI on mean difference
        ci_diff = stats.t.interval(0.95, df=n_pairs-1, loc=np.mean(diff), scale=stats.sem(diff))
        
        p_vals_raw.append(w_pval)
        temp_res.append({
            'Season': s_name,
            'Comparison': f'KNN vs {comp_m}',
            'Mean_Abs_Error_KNN': float(np.mean(e_knn)),
            'Mean_Abs_Error_Comp': float(np.mean(e_comp)),
            'Error_Reduction_Pct': reduction_pct,
            'Mean_Diff': float(np.mean(diff)),
            'CI_Diff_Lower': float(ci_diff[0]),
            'CI_Diff_Upper': float(ci_diff[1]),
            'Paired_t_Stat': float(t_stat),
            'Paired_t_pvalue': float(t_pval),
            'Wilcoxon_W': float(w_stat),
            'Wilcoxon_pvalue': float(w_pval),
            'Cohens_d': d_val,
            'Rank_Biserial_Corr': r_rb
        })
        
    # Apply Holm-Bonferroni correction
    # Sort by p_val
    order = np.argsort(p_vals_raw)
    m = len(p_vals_raw)
    holm_pvals = [0]*m
    for rank_idx, orig_idx in enumerate(order):
        adj_p = min(1.0, p_vals_raw[orig_idx] * (m - rank_idx))
        holm_pvals[orig_idx] = float(adj_p)
        
    for idx_item, res_item in enumerate(temp_res):
        res_item['Holm_Adjusted_pvalue'] = holm_pvals[idx_item]
        stat_tests.append(res_item)

pd.DataFrame(stat_tests).to_json('results/faculty_revision/statistical_comparisons_holm.json', orient='records', indent=2)

print("\n--- ALL COMPREHENSIVE FACULTY ANALYSES COMPUTED AND SAVED SUCCESSFULLY! ---")
