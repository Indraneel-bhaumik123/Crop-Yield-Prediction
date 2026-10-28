"""
paper_section_5_6.py
Section 5: EXPLORATORY DATA ANALYSIS and Section 6: EXPERIMENTAL DESIGN.
"""

from paper_common import add_p, add_h, add_fig

def build_section_5_6(doc):
    # -------------------------------------------------------------
    # 5. EXPLORATORY DATA ANALYSIS
    # -------------------------------------------------------------
    add_h(doc, "5. EXPLORATORY DATA ANALYSIS", 1)
    
    add_p(doc, 
        "Prior to model training, exhaustive exploratory data analysis (EDA) was performed across the consolidated global agricultural dataset (13,130 records). The exploratory investigation examined dataset composition, crop commodity representation, yield density distributions, longitudinal trajectories over the 1990–2013 epoch, bivariate agro-environmental relationships, and feature correlation structures."
    )
    
    # 5.1 Distribution of Crop-Yield Observations
    add_h(doc, "5.1 Distribution of Crop-Yield Observations", 2)
    add_p(doc, 
        "Figure 1 illustrates the dataset composition and sample distribution across the three agricultural regimes. The Seasonal multi-crop category constitutes the largest proportion (52.7%, 6,916 records), followed by the Kharif monsoon-dependent regime (33.5%, 4,404 records) and the Rabi winter regime (13.8%, 1,810 records). This sample distribution reflects global agricultural production realities, where multi-season and perennial commodities span wider geographical belts and harvesting intervals."
    )
    
    # Figure 1: Dataset Composition (Caption ABOVE)
    add_fig(doc, "figures/revised/fig01_dataset_composition.png", 1,
            "Dataset Composition Across Kharif, Rabi, and Seasonal Agricultural Regimes (N = 13,130)",
            "(a) Proportional share of records across seasonal regimes; (b) Absolute sample record counts across Kharif, Rabi, and Seasonal partitions.",
            width=5.8)
    
    add_p(doc, 
        "Figure 2 illustrates the distribution of records across the ten major food commodities. Potatoes (4,276 records) and Rice paddy (2,188 records) are the most heavily represented commodities in the Seasonal dataset, reflecting extensive international cultivation of root crops and wetland rice. In Kharif, Maize (2,028 records), Sorghum (1,435 records), and Cassava (941 records) predominate, representing classic rainfed tropical cultivars. In Rabi, Wheat (1,810 records) forms the exclusive agricultural commodity in our consolidated dataset."
    )
    
    # Figure 2: Crop Distribution (Caption ABOVE)
    add_fig(doc, "figures/revised/fig02_crop_distribution.png", 2,
            "Representation of Agricultural Crops Across the Consolidated Global Dataset",
            "Frequency distribution of historical harvest records (1990–2013) across the ten major food crop commodities.",
            width=5.8)
    
    add_p(doc, 
        "Figure 3 presents the estimated probability density distributions of harvested crop yield (hg/ha) across the three seasonal regimes. The target distributions exhibit pronounced right-skewness and distinct multi-modal behavior. Tuber and root commodities—such as Potatoes and Cassava—exhibit vastly higher fresh harvested mass per hectare (frequently exceeding 200,000 to 350,000 hg/ha) due to high moisture content and dense tuberous biomass. In contrast, cereal grains such as Wheat, Sorghum, and Maize exhibit substantially lower mass yields per hectare (typically clustered between 15,000 and 60,000 hg/ha). Forcing these divergent distributions into a single pooled regression model would induce severe heteroscedasticity and distort residual variance."
    )
    
    # Figure 3: Yield Distribution (Caption ABOVE)
    add_fig(doc, "figures/revised/fig03_yield_distribution.png", 3,
            "Density Distribution of Historical Crop Yield Across Seasonal Regimes",
            "Kernel density estimates of crop yield (hg/ha, where 1 hg/ha = 0.1 kg/ha) across Kharif, Rabi, and Seasonal agricultural partitions.",
            width=5.8)
    
    # 5.2 Distribution of Agricultural and Environmental Variables
    add_h(doc, "5.2 Distribution of Agricultural and Environmental Variables", 2)
    add_p(doc, 
        "Figure 5 depicts the bivariate relationship between average annual rainfall (mm/year) and harvested crop yield across seasonal regimes, overlaid with a quadratic polynomial trend fit. The empirical scatter pattern highlights clear non-linear dynamics: while crop yield responds positively to increasing precipitation up to moderate thresholds (800–1,600 mm/year), extreme precipitation (>2,200 mm/year) does not yield continuous gains and is frequently associated with stagnant or declining yields due to waterlogging, nutrient leaching, and fungal disease."
    )
    
    # Figure 5: Rainfall vs Yield (Caption ABOVE)
    add_fig(doc, "figures/revised/fig05_rainfall_vs_yield.png", 5,
            "Bivariate Relationship Between Annual Rainfall and Crop Yield",
            "Scatter plot and polynomial trend line showing non-linear yield response across precipitation levels for Kharif, Rabi, and Seasonal groups.",
            width=5.6)
    
    add_p(doc, 
        "Figure 6 illustrates the relationship between mean atmospheric temperature (°C) and harvested yield. Agronomic productivity exhibits a non-linear thermal response curve: yields peak within a moderate thermal window (12°C–22°C), while elevated temperatures (>25°C) are associated with reduced yields for temperate cereals and tubers due to accelerated senescence, pollen sterility, and high respiration losses [31]."
    )
    
    # Figure 6: Temperature vs Yield (Caption ABOVE)
    add_fig(doc, "figures/revised/fig06_temperature_vs_yield.png", 6,
            "Thermal Growing Conditions vs. Crop Yield Showing Agronomic Optimum",
            "Bivariate distribution and thermal response curve illustrating temperature optimums across seasonal regimes.",
            width=5.6)
    
    add_p(doc, 
        "Figure 7 depicts the relationship between national pesticide application (metric tonnes, plotted on a logarithmic scale) and harvested crop yield. Increased pesticide utilization is positively correlated with yield up to an asymptotic threshold (~1,000 to 10,000 tonnes), reflecting effective suppression of pest and pathogen damage. Beyond this threshold, additional chemical application yields diminishing marginal returns."
    )
    
    # Figure 7: Pesticides vs Yield (Caption ABOVE)
    add_fig(doc, "figures/revised/fig07_pesticides_vs_yield.png", 7,
            "Chemical Crop Protection Intensity vs. Harvested Yield",
            "Bivariate response curve of crop yield as a function of nationwide pesticide utilization on a logarithmic scale.",
            width=5.6)
    
    # 5.3 Seasonal and Temporal Variability
    add_h(doc, "5.3 Seasonal and Temporal Variability", 2)
    add_p(doc, 
        "Figure 4 tracks annual mean crop yields across the 1990–2013 historical epoch. A steady secular upward trend is evident across all three seasonal categories over the 24-year period, driven by global agricultural modernization, synthetic fertilizer adoption, improved hybrid seed varieties, and expanding irrigation infrastructure. The prospective 2013 holdout boundary (vertical red dashed line) demarcates the training and test periods, confirming that our model evaluation tests prospective forward-year generalization rather than historical interpolation."
    )
    
    # Figure 4: Historical Yield Trajectory (Caption ABOVE)
    add_fig(doc, "figures/revised/fig04_yield_over_time.png", 4,
            "Historical Crop Yield Trajectory Over Time (1990–2013)",
            "Longitudinal evolution of mean crop yield across agricultural seasons from 1990 to 2013, with the prospective 2013 holdout split highlighted.",
            width=5.8)
    
    add_p(doc, 
        "Figure 8 presents the pairwise Pearson correlation matrix across the numerical predictors (Year, Rainfall, Pesticides, Avg Temp) and crop yield. Bivariate linear correlations between individual numerical features and crop yield are modest (|r| < 0.15). Specifically, Year exhibits r = 0.088, Rainfall exhibits r = 0.013, Pesticides exhibits r = 0.092, and Avg Temp exhibits r = -0.143 with yield. These modest linear correlations confirm that crop yield cannot be captured through simplistic linear combinations of isolated variables, reinforcing the necessity of non-linear machine learning regressors capable of modeling complex feature interactions."
    )
    
    # Figure 8: Correlation Heatmap (Caption ABOVE)
    add_fig(doc, "figures/revised/fig08_correlation_heatmap.png", 8,
            "Pairwise Pearson Correlation Heatmap Across Numerical Agricultural Features",
            "Correlation matrix between calendar Year, annual Rainfall, Pesticide applications, Average Temperature, and crop yield (hg/ha).",
            width=5.2)
    
    # -------------------------------------------------------------
    # 6. EXPERIMENTAL DESIGN
    # -------------------------------------------------------------
    add_h(doc, "6. EXPERIMENTAL DESIGN", 1)
    
    add_h(doc, "6.1 Benchmarking Framework and Software Environment", 2)
    add_p(doc, 
        "All experimental pipelines were implemented in Python 3.12 utilizing verified, standardized open-source scientific computing libraries: Scikit-Learn 1.9.0 for preprocessing and regression modeling, XGBoost 3.1.3 for regularized gradient-boosted decision trees, Pandas 3.0.5 and NumPy for tabular data wrangling, and SciPy for statistical distribution and hypothesis testing. Deterministic reproducibility was enforced across all stochastic routines (including cross-validation splitting and tree fitting) by fixing random_state = 42."
    )
    
    add_h(doc, "6.2 Time-Aware Hyperparameter Optimization Protocol", 2)
    add_p(doc, 
        "Hyperparameter selection was executed strictly within the 1990–2012 historical training partition using a 3-fold time-aware GridSearchCV protocol. Rather than shuffling data randomly across temporal boundaries, the training partition was segmented into chronological folds to preserve the temporal ordering of agricultural records. Cross-validation evaluated candidate parameter grids, selecting optimal configurations based on mean cross-validated negative root mean squared error. The prospective 2013 holdout set was strictly segregated and never exposed to the hyperparameter search."
    )
    
    add_h(doc, "6.3 Evaluation Protocol and Baseline Calibration", 2)
    add_p(doc, 
        "To establish a rigorous comparative benchmark, five regression algorithms were calibrated for each season: Ordinary Least Squares Linear Regression (baseline), K-Nearest Neighbors (tuned candidate), Gradient Boosting Regressor (tuned candidate), XGBoost Regressor (tuned candidate), and Multilayer Perceptron (tuned candidate). All models were evaluated on the identical 2013 prospective holdout across RMSE, MAE, R², and Pearson r, ensuring completely controlled comparisons."
    )

print("paper_section_5_6.py created.")
