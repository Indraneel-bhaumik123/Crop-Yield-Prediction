"""
paper_section_8_9.py
Section 8: DISCUSSION and Section 9: SYSTEM IMPLEMENTATION AND DEPLOYMENT.
"""

from paper_common import add_p, add_h, add_fig

def build_section_8_9(doc):
    # -------------------------------------------------------------
    # 8. DISCUSSION
    # -------------------------------------------------------------
    add_h(doc, "8. DISCUSSION", 1)
    
    add_p(doc, 
        "The empirical findings of this study offer meaningful scientific insights into the behavior of machine-learning regressors on longitudinal agricultural tabular datasets. In this section, we interpret why specific model architectures performed well or struggled, distinguish verified empirical findings from plausible agronomic hypotheses, and contextualize our results within broader literature."
    )
    
    # 8.1 Why KNN Performed Strongly
    add_h(doc, "8.1 Why KNN Performed Strongly under this Feature Representation", 2)
    add_p(doc, 
        "A central finding of our benchmark is that tuned distance-weighted K-Nearest Neighbors achieved the highest predictive performance across all three seasonal pipelines (R² = 0.9380 to 0.9642). This result does not imply that KNN is a universally superior algorithm for all agricultural tasks; rather, it indicates that KNN is exceptionally well aligned with the specific topological structure of our tabular dataset."
    )
    add_p(doc, 
        "Agricultural production is characterized by dense localized continuity. In our consolidated database, the same sovereign nations and crop varieties appear repeatedly across the 1990–2012 historical training years. When predicting a 2013 harvest for a specific nation (e.g., Maize in Algeria), the OneHotEncoder projects the query into a subspace where Algeria and Maize share identical binary flags with Algeria's historical harvests from 2010, 2011, and 2012. After continuous features (temperature, rainfall, pesticide application, calendar year) are standardized to unit variance via StandardScaler, the Minkowski distance effectively identifies these immediate preceding harvests as the nearest historical analogs. Because agricultural technology and regional soil regimes evolve gradually, distance-inverse weighting heavily prioritizes the most recent, climatically similar harvests, yielding highly accurate interpolations."
    )
    
    # 8.2 Tree Ensembles
    add_h(doc, "8.2 Tree Ensembles as Robust Competing Alternatives", 2)
    add_p(doc, 
        "Extreme Gradient Boosting (XGBoost) established itself as the consistent runner-up across all three seasonal regimes, achieving prospective holdout R² scores between 0.9064 and 0.9377. Tree-based ensembles partition feature space through orthogonal, axis-aligned splits. In tabular datasets with high-cardinality categorical variables (101 sovereign nations encoded as orthogonal columns), decision trees may partition repeatedly on geographic flags, fragmenting sample size across terminal leaf nodes. Nevertheless, XGBoost's second-order Taylor expansion and L1/L2 leaf weight penalties successfully prevented overfitting, enabling it to model non-linear climate thresholds effectively [8, 16]. Gradient Boosting Regressor also performed competitively (R² = 0.8127 to 0.8379), but lacked the advanced second-order regularization of XGBoost."
    )
    
    # 8.3 Linearity in Rabi vs Non-Linearity in Kharif
    add_h(doc, "8.3 Agronomic Linearity in Rabi vs. Non-Linearity in Kharif and Seasonal", 2)
    add_p(doc, 
        "A striking empirical contrast emerged in the behavior of our Ordinary Least Squares Linear Regression baseline. In the Rabi season, Linear Regression achieved an impressive R² of 0.9158 and RMSE of 6,182.82 hg/ha, outperforming Gradient Boosting (R² = 0.8362) and MLP (R² = 0.5812). In stark contrast, Linear Regression performed poorly in Kharif (R² = 0.6753) and Seasonal (R² = 0.7459). This divergence reflects fundamental agronomic differences: Rabi cultivation in our dataset consists strictly of Wheat, a monoculture cereal grown in temperate or irrigated zones where yield responses to fertilizers, pesticides, and technology follow relatively steady linear increments. Conversely, Kharif and Seasonal datasets combine multiple disparate crops (tubers, wetland rice, coarse grains) with vastly different baseline yields and non-linear rainfall thresholds, rendering simple linear planes inadequate."
    )
    
    # 8.4 Multilayer Perceptron Behavior
    add_h(doc, "8.4 Multilayer Perceptron Behavior on Tabular Agricultural Data", 2)
    add_p(doc, 
        "The Multilayer Perceptron (MLP) exhibited the lowest explanatory power among the non-linear algorithms, attaining holdout R² scores between 0.5812 and 0.7845. This outcome is consistent with recent large-scale machine-learning benchmarking studies on tabular data [4, 7], which demonstrate that artificial neural networks frequently struggle to outperform tree ensembles and instance-based models on medium-sized tabular datasets. Neural networks lack inductive biases tailored to tabular coordinate structures and require massive sample sizes to avoid sub-optimal local minima when training over sparse one-hot encoded categorical vectors."
    )
    
    # 8.5 Distinguishing Results from Interpretations
    add_h(doc, "8.5 Distinguishing Empirical Results from Interpretations and Hypotheses", 2)
    add_p(doc, 
        "To uphold scientific integrity, we explicitly demarcate between: (i) Empirical Results: the verified test metrics, statistical p-values, and distribution shifts recorded in Section 7; (ii) Methodological Interpretations: the explanation that KNN's success stems from localized manifold density and that random splitting introduces evaluation flattery; and (iii) Unproven Hypotheses: the conjecture that fine-grained soil chemistry or daily heatwave indices would elevate tree ensembles above KNN. The latter represents a plausible agronomic hypothesis that cannot be definitively asserted without external micro-data collection."
    )
    
    # -------------------------------------------------------------
    # 9. SYSTEM IMPLEMENTATION AND DEPLOYMENT
    # -------------------------------------------------------------
    add_h(doc, "9. SYSTEM IMPLEMENTATION AND DEPLOYMENT", 1)
    
    add_p(doc, 
        "To bridge the gap between academic experimentation and practical software engineering, we engineered and deployed an end-to-end, production-grade agricultural prediction platform. Figure 12 illustrates the multi-tier production system architecture."
    )
    
    # Figure 12: System Architecture (Caption ABOVE)
    add_fig(doc, "figures/revised/fig12_system_architecture.png", 12,
            "Production System Architecture Diagram",
            "Multi-tier deployment topology showing client dashboard, FastAPI asynchronous REST API, JWT authentication, serialized Scikit-Learn pipelines, and SQLite database persistence.",
            width=5.8)
    
    # 9.1 System Architecture Overview
    add_h(doc, "9.1 System Architecture Overview", 2)
    add_p(doc, 
        "The deployed software ecosystem comprises three decoupled layers: (1) a responsive frontend client dashboard; (2) an asynchronous FastAPI application server; and (3) an embedded SQLite relational database layer managed via SQLAlchemy ORM. The calibrated Scikit-Learn pipelines are serialized using Joblib (models/kharif_model.joblib, models/rabi_model.joblib, models/seasonal_model.joblib), packaging both the fitted ColumnTransformer preprocessor and the calibrated KNN regressor into a single self-contained binary artifact."
    )
    
    # 9.2 FastAPI Backend
    add_h(doc, "9.2 FastAPI Backend and API Endpoints", 2)
    add_p(doc, 
        "The backend is developed with FastAPI (running on Uvicorn ASGI), providing asynchronous request processing, Pydantic schema validation, and automated Swagger/OpenAPI interactive documentation. The service exposes four primary REST endpoints:"
    )
    add_p(doc, "1. POST /api/v1/predict: Receives agricultural parameters (season, continent, country, crop, year, rainfall, pesticides, avg temp), validates payload schemas, authenticates the JWT bearer token, dynamically dispatches the query to the designated seasonal pipeline, persists the query and prediction to SQLite, and returns the estimated yield in hg/ha.", bold_prefix="• ")
    add_p(doc, "2. GET /api/v1/options: Delivers cascading dropdown options (mapping continents to countries, and seasons to supported crops) extracted directly from the underlying datasets to prevent invalid input combinations.", bold_prefix="• ")
    add_p(doc, "3. GET /api/v1/history: Retrieves the complete chronological prediction audit trail for the authenticated user.", bold_prefix="• ")
    add_p(doc, "4. GET /api/v1/analytics: Serves aggregate platform metrics, historical prediction distributions, and benchmark summary statistics for dashboard rendering.", bold_prefix="• ")
    
    # 9.3 Authentication and Security
    add_h(doc, "9.3 Authentication and Security", 2)
    add_p(doc, 
        "User security is enforced via OAuth2 Password Bearer flow utilizing cryptographically signed JSON Web Tokens (JWT). User passwords are protected using Passlib with the Bcrypt hashing algorithm and automated salt rounds. Upon successful authentication at POST /api/v1/auth/token, the server issues an HMAC-SHA256 signed JWT bearer token with a 60-minute expiration window, required in the HTTP Authorization header for protected endpoints."
    )
    
    # 9.4 SQLite Database Persistence
    add_h(doc, "9.4 SQLite Database Persistence and Audit Trail", 2)
    add_p(doc, 
        "Data persistence is managed by an embedded SQLite relational database (crop_prediction.db) accessed through SQLAlchemy ORM. The database schema maintains two primary relational entities: Users (storing user credentials, usernames, and hashed passwords) and PredictionHistory (storing complete audit records of every executed prediction, including input agro-climatic values, selected seasonal model, predicted yield, timestamp, and foreign key user ID). This provides full traceability for agricultural decision support."
    )
    
    # 9.5 Client Dashboard
    add_h(doc, "9.5 Client Dashboard and Interactive Analytics", 2)
    add_p(doc, 
        "The client frontend is built using standard HTML5, modern Vanilla CSS, and JavaScript ES6, adhering to responsive, glassmorphism design principles without external bloated frameworks. The dashboard features dynamic cascading selectors (ensuring users only select crops valid for the selected season), live model benchmark visualizations rendered with Chart.js, and an interactive prediction history table allowing users to review and filter past forecasts."
    )

print("paper_section_8_9.py created.")
