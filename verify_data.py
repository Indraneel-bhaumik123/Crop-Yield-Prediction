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
import xgboost as xgb
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor

# Load datasets
df_k = pd.read_csv('data/processed/processed_kharif.csv')
df_r = pd.read_csv('data/processed/processed_rabi.csv')
df_s = pd.read_csv('data/processed/processed_seasonal.csv')

print(f"Kharif rows: {len(df_k)}, Rabi rows: {len(df_r)}, Seasonal rows: {len(df_s)}")

# Verify 1990-2012 train and 2013 test split
for name, df in [('Kharif', df_k), ('Rabi', df_r), ('Seasonal', df_s)]:
    train_n = len(df[df['Year'] <= 2012])
    test_n = len(df[df['Year'] == 2013])
    print(f"{name} -> Train (<=2012): {train_n}, Test (2013): {test_n}")
