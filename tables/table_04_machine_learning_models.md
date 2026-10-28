# Table 04 Machine Learning Models

| Model Family | Algorithm Class | Inductive Bias & Operational Mechanism | Key Strengths | Primary Limitations | Study Role |
| --- | --- | --- | --- | --- | --- |
| Linear Regression | Parametric Linear | Ordinary Least Squares minimizing residual sum of squares | Interpretable, zero hyperparameters, fast computation | Fails to capture complex non-linear agro-climatic interactions | Baseline (Ours) |
| K-Nearest Neighbors | Instance-Based Non-Parametric | Predicts local weighted average based on Minkowski metric neighborhood | Captures local micro-clusters, no strong functional form assumptions | Inference scales with dataset size; highly sensitive to feature scaling | Core (Reference 2) |
| Gradient Boosting Regressor | Ensemble Boosting | Sequentially fits shallow regression trees on negative gradient of loss function | High predictive power, handles mixed distributions, strong generalization | Susceptible to overfitting if tree depth and learning rate are unregularized | Core (Reference 2) |
| XGBoost Regressor | Regularized Boosting | Second-order Taylor gradient boosting with L1/L2 structural penalties | Hardware-accelerated, robust regularization, tree pruning | Requires extensive hyperparameter tuning across subsampling and learning rate | Core (Reference 2) |
| Multilayer Perceptron | Deep Artificial Neural Net | Feedforward artificial neural network with backpropagation and ReLU activations | Universal function approximator for complex non-linear interactions | Prone to local minima on tabular data, requires high tuning overhead | Core (Reference 2) |
