import joblib
import pandas as pd
import numpy as np

for season, path, test_csv in [
    ('Kharif', 'models/kharif_model.joblib', 'data/processed/processed_kharif.csv'),
    ('Rabi', 'models/rabi_model.joblib', 'data/processed/processed_rabi.csv'),
    ('Seasonal', 'models/seasonal_model.joblib', 'data/processed/processed_seasonal.csv')
]:
    model = joblib.load(path)
    df = pd.read_csv(test_csv)
    df_test = df[df['Year'] == 2013]
    
    # check columns
    feature_cols = ['Area', 'Continent', 'Item', 'Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']
    X_test = df_test[feature_cols]
    y_test = df_test['hg/ha_yield']
    
    preds = model.predict(X_test)
    
    rmse = np.sqrt(np.mean((y_test - preds)**2))
    mae = np.mean(np.abs(y_test - preds))
    ss_tot = np.sum((y_test - np.mean(y_test))**2)
    ss_res = np.sum((y_test - preds)**2)
    r2 = 1 - (ss_res / ss_tot)
    r = np.corrcoef(y_test, preds)[0, 1]
    
    print(f"{season} Holdout 2013:")
    print(f"  RMSE: {rmse:.2f}, MAE: {mae:.2f}, R2: {r2:.4f}, Pearson r: {r:.4f}")
