import os
import json
import joblib
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb

os.makedirs('results/advanced', exist_ok=True)
os.makedirs('figures/advanced', exist_ok=True)

# 1. Load Data
df_k = pd.read_csv('data/processed/processed_kharif.csv')
df_r = pd.read_csv('data/processed/processed_rabi.csv')
df_s = pd.read_csv('data/processed/processed_seasonal.csv')

df_k['Season_Group'] = 'Kharif'
df_r['Season_Group'] = 'Rabi'
df_s['Season_Group'] = 'Seasonal'

feature_cols = ['Area', 'Continent', 'Item', 'Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']
cat_cols = ['Area', 'Continent', 'Item']
num_cols = ['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']

# Pipeline creator
def make_pipeline(k, p, weights='distance'):
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols),
            ('num', StandardScaler(), num_cols)
        ]
    )
    return Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', KNeighborsRegressor(n_neighbors=k, p=p, weights=weights))
    ])

# -------------------------------------------------------------
# A. TEMPORAL DISTRIBUTION SHIFT ANALYSIS (1990-2012 vs 2013)
# -------------------------------------------------------------
print("--- 1. Computing Temporal Distribution Shift ---")
shift_results = {}
for season, df in [('Kharif', df_k), ('Rabi', df_r), ('Seasonal', df_s), ('Combined', pd.concat([df_k, df_r, df_s]))]:
    train = df[df['Year'] <= 2012]
    test = df[df['Year'] == 2013]
    shift_results[season] = {}
    
    for var in ['average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp', 'hg/ha_yield']:
        tr_v = train[var].dropna()
        te_v = test[var].dropna()
        ks_stat, ks_pval = stats.ks_2samp(tr_v, te_v)
        w_dist = stats.wasserstein_distance(tr_v, te_v)
        shift_results[season][var] = {
            'train_mean': float(tr_v.mean()),
            'train_std': float(tr_v.std()),
            'test_mean': float(te_v.mean()),
            'test_std': float(te_v.std()),
            'pct_mean_change': float(((te_v.mean() - tr_v.mean()) / tr_v.mean()) * 100),
            'ks_stat': float(ks_stat),
            'ks_pvalue': float(ks_pval),
            'wasserstein_dist': float(w_dist)
        }

with open('results/advanced/temporal_distribution_shift.json', 'w') as f:
    json.dump(shift_results, f, indent=2)

# -------------------------------------------------------------
# B. RANDOM VS CHRONOLOGICAL VALIDATION
# -------------------------------------------------------------
print("--- 2. Computing Random vs Chronological Validation ---")
rand_vs_chrono = {}
for season, df, k, p in [('Kharif', df_k, 3, 2), ('Rabi', df_r, 7, 1), ('Seasonal', df_s, 3, 1)]:
    # Chronological: train <= 2012, test == 2013
    train_c = df[df['Year'] <= 2012]
    test_c = df[df['Year'] == 2013]
    pipe_c = make_pipeline(k, p)
    pipe_c.fit(train_c[feature_cols], train_c['hg/ha_yield'])
    pred_c = pipe_c.predict(test_c[feature_cols])
    rmse_c = np.sqrt(mean_squared_error(test_c['hg/ha_yield'], pred_c))
    mae_c = mean_absolute_error(test_c['hg/ha_yield'], pred_c)
    r2_c = r2_score(test_c['hg/ha_yield'], pred_c)
    
    # Random split with same test fraction
    test_frac = len(test_c) / len(df)
    train_r, test_r = train_test_split(df, test_size=test_frac, random_state=42)
    pipe_r = make_pipeline(k, p)
    pipe_r.fit(train_r[feature_cols], train_r['hg/ha_yield'])
    pred_r = pipe_r.predict(test_r[feature_cols])
    rmse_r = np.sqrt(mean_squared_error(test_r['hg/ha_yield'], pred_r))
    mae_r = mean_absolute_error(test_r['hg/ha_yield'], pred_r)
    r2_r = r2_score(test_r['hg/ha_yield'], pred_r)
    
    # Also evaluate Linear Regression
    lr_c = Pipeline([
        ('preprocessor', ColumnTransformer([
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols),
            ('num', StandardScaler(), num_cols)
        ])),
        ('regressor', LinearRegression())
    ])
    lr_c.fit(train_c[feature_cols], train_c['hg/ha_yield'])
    lr_pred_c = lr_c.predict(test_c[feature_cols])
    lr_r2_c = r2_score(test_c['hg/ha_yield'], lr_pred_c)
    
    lr_r = Pipeline([
        ('preprocessor', ColumnTransformer([
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols),
            ('num', StandardScaler(), num_cols)
        ])),
        ('regressor', LinearRegression())
    ])
    lr_r.fit(train_r[feature_cols], train_r['hg/ha_yield'])
    lr_pred_r = lr_r.predict(test_r[feature_cols])
    lr_r2_r = r2_score(test_r['hg/ha_yield'], lr_pred_r)

    rand_vs_chrono[season] = {
        'knn_chronological': {'rmse': float(rmse_c), 'mae': float(mae_c), 'r2': float(r2_c)},
        'knn_random': {'rmse': float(rmse_r), 'mae': float(mae_r), 'r2': float(r2_r)},
        'lr_chronological_r2': float(lr_r2_c),
        'lr_random_r2': float(lr_r2_r)
    }

with open('results/advanced/random_vs_chronological.json', 'w') as f:
    json.dump(rand_vs_chrono, f, indent=2)

# -------------------------------------------------------------
# C. SEASON-SPECIFIC VS POOLED MODEL
# -------------------------------------------------------------
print("--- 3. Computing Season-Specific vs Pooled Model ---")
# Build pooled training data
df_combined = pd.concat([df_k, df_r, df_s], ignore_index=True)
train_comb = df_combined[df_combined['Year'] <= 2012]
test_comb = df_combined[df_combined['Year'] == 2013]

pooled_feature_cols = ['Area', 'Continent', 'Item', 'Season_Group', 'Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']
pooled_cat_cols = ['Area', 'Continent', 'Item', 'Season_Group']
pooled_num_cols = ['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']

# Tune pooled KNN on combined train
pipe_pooled = Pipeline([
    ('preprocessor', ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), pooled_cat_cols),
        ('num', StandardScaler(), pooled_num_cols)
    ])),
    ('regressor', KNeighborsRegressor(n_neighbors=5, p=1, weights='distance'))
])
pipe_pooled.fit(train_comb[pooled_feature_cols], train_comb['hg/ha_yield'])

pooled_vs_specific = {}
for season, df, k, p in [('Kharif', df_k, 3, 2), ('Rabi', df_r, 7, 1), ('Seasonal', df_s, 3, 1)]:
    test_sub = df[df['Year'] == 2013].copy()
    test_sub_pooled = test_sub[pooled_feature_cols]
    pred_pooled = pipe_pooled.predict(test_sub_pooled)
    
    rmse_p = np.sqrt(mean_squared_error(test_sub['hg/ha_yield'], pred_pooled))
    mae_p = mean_absolute_error(test_sub['hg/ha_yield'], pred_pooled)
    r2_p = r2_score(test_sub['hg/ha_yield'], pred_pooled)
    
    # Specific model
    model_s = joblib.load(f'models/{season.lower()}_model.joblib')
    pred_s = model_s.predict(test_sub[feature_cols])
    rmse_s = np.sqrt(mean_squared_error(test_sub['hg/ha_yield'], pred_s))
    mae_s = mean_absolute_error(test_sub['hg/ha_yield'], pred_s)
    r2_s = r2_score(test_sub['hg/ha_yield'], pred_s)
    
    pooled_vs_specific[season] = {
        'season_specific': {'rmse': float(rmse_s), 'mae': float(mae_s), 'r2': float(r2_s)},
        'pooled_model': {'rmse': float(rmse_p), 'mae': float(mae_p), 'r2': float(r2_p)},
        'rmse_advantage_pct': float(((rmse_p - rmse_s) / rmse_p) * 100)
    }

with open('results/advanced/season_specific_vs_pooled.json', 'w') as f:
    json.dump(pooled_vs_specific, f, indent=2)

# -------------------------------------------------------------
# D. HISTORICAL NEIGHBORHOOD ANALYSIS OF KNN & REAL WORKED EXAMPLE
# -------------------------------------------------------------
print("--- 4. Computing Historical-Neighborhood Analysis & Worked Example ---")
neighbor_analysis = {}
worked_examples = {}

for season, df, k, p, metric_name in [('Kharif', df_k, 3, 2, 'euclidean'), ('Rabi', df_r, 7, 1, 'manhattan'), ('Seasonal', df_s, 3, 1, 'manhattan')]:
    train = df[df['Year'] <= 2012].reset_index(drop=True)
    test = df[df['Year'] == 2013].reset_index(drop=True)
    
    model = joblib.load(f'models/{season.lower()}_model.joblib')
    preproc = model.named_steps['preprocessor']
    reg = model.named_steps['regressor']
    
    X_train_trans = preproc.transform(train[feature_cols])
    X_test_trans = preproc.transform(test[feature_cols])
    
    # Find neighbors
    distances, indices = reg.kneighbors(X_test_trans)
    preds = model.predict(test[feature_cols])
    actuals = test['hg/ha_yield'].values
    errors = np.abs(actuals - preds)
    
    mean_dist = np.mean(distances, axis=1)
    # std dev of neighbor yields
    neighbor_yield_stds = [np.std(train.loc[idx_list, 'hg/ha_yield']) for idx_list in indices]
    
    corr_dist_err = stats.pearsonr(mean_dist, errors)[0]
    corr_std_err = stats.pearsonr(neighbor_yield_stds, errors)[0]
    
    neighbor_analysis[season] = {
        'mean_neighbor_distance': float(np.mean(mean_dist)),
        'std_neighbor_distance': float(np.std(mean_dist)),
        'min_distance': float(np.min(mean_dist)),
        'max_distance': float(np.max(mean_dist)),
        'corr_distance_vs_abs_error': float(corr_dist_err),
        'corr_neighbor_dispersion_vs_abs_error': float(corr_std_err)
    }
    
    # Real worked example: choose the first test point
    ex_idx = 0
    ex_row = test.iloc[ex_idx]
    ex_dist = distances[ex_idx]
    ex_neighbors_idx = indices[ex_idx]
    ex_neighbors = train.iloc[ex_neighbors_idx]
    
    # compute weights
    weights = 1.0 / (ex_dist + 1e-10)
    w_sum = np.sum(weights)
    norm_w = weights / w_sum
    calc_pred = np.sum(norm_w * ex_neighbors['hg/ha_yield'].values)
    
    worked_examples[season] = {
        'query_point': {
            'Area': ex_row['Area'],
            'Continent': ex_row['Continent'],
            'Item': ex_row['Item'],
            'Year': int(ex_row['Year']),
            'rainfall': float(ex_row['average_rain_fall_mm_per_year']),
            'pesticides': float(ex_row['pesticides_tonnes']),
            'avg_temp': float(ex_row['avg_temp']),
            'actual_yield': float(ex_row['hg/ha_yield']),
            'pipeline_prediction': float(preds[ex_idx])
        },
        'neighbors': [
            {
                'rank': i + 1,
                'Area': n_row['Area'],
                'Year': int(n_row['Year']),
                'Item': n_row['Item'],
                'actual_yield': float(n_row['hg/ha_yield']),
                'distance': float(ex_dist[i]),
                'weight': float(weights[i]),
                'normalized_weight': float(norm_w[i])
            }
            for i, (_, n_row) in enumerate(ex_neighbors.iterrows())
        ],
        'manual_calculated_yield': float(calc_pred)
    }

with open('results/advanced/neighbor_analysis.json', 'w') as f:
    json.dump({'neighborhood_metrics': neighbor_analysis, 'worked_examples': worked_examples}, f, indent=2)

# -------------------------------------------------------------
# E. PERMUTATION FEATURE IMPORTANCE
# -------------------------------------------------------------
print("--- 5. Computing Permutation Feature Importance ---")
perm_importance = {}
for season, df in [('Kharif', df_k), ('Rabi', df_r), ('Seasonal', df_s)]:
    test = df[df['Year'] == 2013]
    model = joblib.load(f'models/{season.lower()}_model.joblib')
    
    res = permutation_importance(model, test[feature_cols], test['hg/ha_yield'],
                                 scoring='neg_root_mean_squared_error', n_repeats=10, random_state=42)
    
    perm_importance[season] = {
        col: {
            'mean_rmse_increase': float(res.importances_mean[i]),
            'std_rmse_increase': float(res.importances_std[i])
        }
        for i, col in enumerate(feature_cols)
    }

with open('results/advanced/permutation_feature_importance.json', 'w') as f:
    json.dump(perm_importance, f, indent=2)

# -------------------------------------------------------------
# F. PREDICTION ERROR SUBGROUP ANALYSIS
# -------------------------------------------------------------
print("--- 6. Computing Error Subgroup Analysis ---")
subgroups = {}
for season, df in [('Kharif', df_k), ('Rabi', df_r), ('Seasonal', df_s)]:
    test = df[df['Year'] == 2013].copy()
    model = joblib.load(f'models/{season.lower()}_model.joblib')
    test['preds'] = model.predict(test[feature_cols])
    test['abs_err'] = np.abs(test['hg/ha_yield'] - test['preds'])
    test['sq_err'] = (test['hg/ha_yield'] - test['preds'])**2
    
    # By crop
    crop_stats = {}
    for crop, grp in test.groupby('Item'):
        crop_stats[crop] = {
            'count': int(len(grp)),
            'mean_yield': float(grp['hg/ha_yield'].mean()),
            'mae': float(grp['abs_err'].mean()),
            'rmse': float(np.sqrt(grp['sq_err'].mean())),
            'r2': float(r2_score(grp['hg/ha_yield'], grp['preds'])) if len(grp) > 3 and grp['hg/ha_yield'].std() > 0 else None
        }
    
    # By yield tercile
    test['yield_tercile'] = pd.qcut(test['hg/ha_yield'], q=3, labels=['Low', 'Medium', 'High'])
    tercile_stats = {}
    for tercile, grp in test.groupby('yield_tercile'):
        tercile_stats[str(tercile)] = {
            'count': int(len(grp)),
            'yield_range': f"{grp['hg/ha_yield'].min():.0f} - {grp['hg/ha_yield'].max():.0f}",
            'mae': float(grp['abs_err'].mean()),
            'rmse': float(np.sqrt(grp['sq_err'].mean()))
        }
        
    subgroups[season] = {'by_crop': crop_stats, 'by_yield_tercile': tercile_stats}

with open('results/advanced/error_subgroup_analysis.json', 'w') as f:
    json.dump(subgroups, f, indent=2)

# -------------------------------------------------------------
# G. FEATURE GROUP ABLATION ANALYSIS
# -------------------------------------------------------------
print("--- 7. Computing Feature Group Ablation ---")
ablation_results = {}
ablation_configs = {
    'Full Pipeline': feature_cols,
    'No Climate (Excl. Rain & Temp)': ['Area', 'Continent', 'Item', 'Year', 'pesticides_tonnes'],
    'No Ag Inputs (Excl. Pesticides)': ['Area', 'Continent', 'Item', 'Year', 'average_rain_fall_mm_per_year', 'avg_temp'],
    'No Temporal (Excl. Year)': ['Area', 'Continent', 'Item', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp'],
    'No Geo Context (Excl. Area & Continent)': ['Item', 'Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']
}

for season, df, k, p in [('Kharif', df_k, 3, 2), ('Rabi', df_r, 7, 1), ('Seasonal', df_s, 3, 1)]:
    train = df[df['Year'] <= 2012]
    test = df[df['Year'] == 2013]
    ablation_results[season] = {}
    
    for abl_name, cols in ablation_configs.items():
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
        
        rmse = np.sqrt(mean_squared_error(test['hg/ha_yield'], preds))
        mae = mean_absolute_error(test['hg/ha_yield'], preds)
        r2 = r2_score(test['hg/ha_yield'], preds)
        
        ablation_results[season][abl_name] = {
            'rmse': float(rmse),
            'mae': float(mae),
            'r2': float(r2)
        }

with open('results/advanced/feature_ablation.json', 'w') as f:
    json.dump(ablation_results, f, indent=2)

# -------------------------------------------------------------
# H. ROLLING-ORIGIN TEMPORAL VALIDATION (Multi-Year 2010 to 2013)
# -------------------------------------------------------------
print("--- 8. Computing Rolling-Origin Temporal Validation ---")
rolling_results = {}
test_years = [2010, 2011, 2012, 2013]

for season, df, k, p in [('Kharif', df_k, 3, 2), ('Rabi', df_r, 7, 1), ('Seasonal', df_s, 3, 1)]:
    rolling_results[season] = {}
    for yr in test_years:
        train = df[df['Year'] < yr]
        test = df[df['Year'] == yr]
        
        pipe = make_pipeline(k, p)
        pipe.fit(train[feature_cols], train['hg/ha_yield'])
        preds = pipe.predict(test[feature_cols])
        
        rmse = np.sqrt(mean_squared_error(test['hg/ha_yield'], preds))
        mae = mean_absolute_error(test['hg/ha_yield'], preds)
        r2 = r2_score(test['hg/ha_yield'], preds)
        r = stats.pearsonr(test['hg/ha_yield'], preds)[0]
        
        rolling_results[season][yr] = {
            'test_count': int(len(test)),
            'rmse': float(rmse),
            'mae': float(mae),
            'r2': float(r2),
            'pearson_r': float(r)
        }

with open('results/advanced/rolling_origin_validation.json', 'w') as f:
    json.dump(rolling_results, f, indent=2)

# -------------------------------------------------------------
# I. STATISTICAL COMPARISON & UNCERTAINTY
# -------------------------------------------------------------
print("--- 9. Computing Statistical Comparisons & Prediction Intervals ---")
stat_comparisons = {}
uncertainty_results = {}

for season, df, k, p in [('Kharif', df_k, 3, 2), ('Rabi', df_r, 7, 1), ('Seasonal', df_s, 3, 1)]:
    train = df[df['Year'] <= 2012].reset_index(drop=True)
    test = df[df['Year'] == 2013].reset_index(drop=True)
    
    # KNN
    knn_model = joblib.load(f'models/{season.lower()}_model.joblib')
    knn_preds = knn_model.predict(test[feature_cols])
    knn_err = (test['hg/ha_yield'] - knn_preds)**2
    
    # Fit XGBoost and Linear Regression to get paired residuals
    # Train XGBoost
    xgb_params = {
        'Kharif': {'n_estimators': 150, 'learning_rate': 0.05, 'max_depth': 7},
        'Rabi': {'n_estimators': 150, 'learning_rate': 0.05, 'max_depth': 6},
        'Seasonal': {'n_estimators': 150, 'learning_rate': 0.05, 'max_depth': 8}
    }[season]
    
    pipe_xgb = Pipeline([
        ('preprocessor', ColumnTransformer([
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols),
            ('num', StandardScaler(), num_cols)
        ])),
        ('regressor', xgb.XGBRegressor(**xgb_params, random_state=42))
    ])
    pipe_xgb.fit(train[feature_cols], train['hg/ha_yield'])
    xgb_preds = pipe_xgb.predict(test[feature_cols])
    xgb_err = (test['hg/ha_yield'] - xgb_preds)**2
    
    # Train Linear Regression
    pipe_lr = Pipeline([
        ('preprocessor', ColumnTransformer([
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols),
            ('num', StandardScaler(), num_cols)
        ])),
        ('regressor', LinearRegression())
    ])
    pipe_lr.fit(train[feature_cols], train['hg/ha_yield'])
    lr_preds = pipe_lr.predict(test[feature_cols])
    lr_err = (test['hg/ha_yield'] - lr_preds)**2
    
    # Paired tests on squared errors
    t_stat_xgb, t_pval_xgb = stats.ttest_rel(knn_err, xgb_err)
    w_stat_xgb, w_pval_xgb = stats.wilcoxon(knn_err, xgb_err)
    
    t_stat_lr, t_pval_lr = stats.ttest_rel(knn_err, lr_err)
    w_stat_lr, w_pval_lr = stats.wilcoxon(knn_err, lr_err)
    
    stat_comparisons[season] = {
        'knn_vs_xgboost': {
            'paired_t_stat': float(t_stat_xgb),
            'paired_t_pvalue': float(t_pval_xgb),
            'wilcoxon_stat': float(w_stat_xgb),
            'wilcoxon_pvalue': float(w_pval_xgb)
        },
        'knn_vs_linear_reg': {
            'paired_t_stat': float(t_stat_lr),
            'paired_t_pvalue': float(t_pval_lr),
            'wilcoxon_stat': float(w_stat_lr),
            'wilcoxon_pvalue': float(w_pval_lr)
        }
    }
    
    # Uncertainty / Empirical Prediction Intervals from Neighbor Dispersion
    reg = knn_model.named_steps['regressor']
    preproc = knn_model.named_steps['preprocessor']
    X_test_trans = preproc.transform(test[feature_cols])
    distances, indices = reg.kneighbors(X_test_trans)
    
    # Neighbor min and max as empirical intervals
    covered = 0
    widths = []
    for i, idx_list in enumerate(indices):
        y_neigh = train.loc[idx_list, 'hg/ha_yield'].values
        # 10% expansion for coverage buffer
        y_min = np.min(y_neigh)
        y_max = np.max(y_neigh)
        margin = 0.1 * (y_max - y_min + 1e-5)
        low = y_min - margin
        high = y_max + margin
        widths.append(high - low)
        if low <= test.loc[i, 'hg/ha_yield'] <= high:
            covered += 1
            
    coverage_rate = covered / len(test)
    uncertainty_results[season] = {
        'empirical_coverage_rate': float(coverage_rate),
        'mean_interval_width': float(np.mean(widths)),
        'median_interval_width': float(np.median(widths))
    }

with open('results/advanced/statistical_and_uncertainty.json', 'w') as f:
    json.dump({'statistical_comparisons': stat_comparisons, 'uncertainty_intervals': uncertainty_results}, f, indent=2)

print("All advanced analyses completed and saved to results/advanced/!")
