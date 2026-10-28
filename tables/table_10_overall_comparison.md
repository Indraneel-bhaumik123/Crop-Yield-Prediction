# Table 10 Overall Comparison

| Season | Selected Champion Model | Best Configuration | Prospective Test RMSE (hg/ha) | Prospective Test MAE (hg/ha) | Prospective Test R² | Pearson r | Error Reduction vs Baseline |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kharif | K-Nearest Neighbors | k=3, p=2 (Euclidean), distance-weighted | 14,026.44 | 6,681.12 | 0.9380 | 0.9688 | 56.30% RMSE reduction vs Linear |
| Rabi | K-Nearest Neighbors | k=7, p=1 (Manhattan), distance-weighted | 4,065.82 | 3,184.93 | 0.9636 | 0.9868 | 34.24% RMSE reduction vs Linear |
| Seasonal | K-Nearest Neighbors | k=3, p=1 (Manhattan), distance-weighted | 19,646.94 | 9,630.07 | 0.9642 | 0.9827 | 62.48% RMSE reduction vs Linear |
| Cross-Season Average | Tuned KNN Regressor | Distance-weighted Minkowski k-NN | 12,579.73 | 6,498.71 | 0.9553 | 0.9794 | 50.98% Mean RMSE reduction vs Linear |
