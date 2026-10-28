"""
paper_section_10_12_app.py
Section 10: RELIABILITY AND LIMITATIONS, Section 11: FUTURE WORK,
Section 12: CONCLUSION, REFERENCES, and APPENDICES A, B, C.
"""

from paper_common import format_p, add_p, add_h, add_tbl
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_section_10_12_app(doc):
    # -------------------------------------------------------------
    # 10. RELIABILITY, LIMITATIONS AND THREATS TO VALIDITY
    # -------------------------------------------------------------
    add_h(doc, "10. RELIABILITY, LIMITATIONS AND THREATS TO VALIDITY", 1)
    
    add_p(doc, 
        "Upholding scientific rigor requires an explicit acknowledgment of the methodological boundaries, structural data constraints, and threats to external validity inherent in this study:"
    )
    add_p(doc, 
        "1. Prospective Temporal Boundary: The primary evaluation benchmark relies on calendar year 2013 as an out-of-time prospective holdout. While our rolling-origin validation confirmed stability across 2010–2013, a single subsequent test year cannot establish performance across multi-decade climate shifts or unprecedented extreme weather shocks.",
        bold_prefix="1. Temporal Validation Horizon: "
    )
    add_p(doc, 
        "2. Macroscopic Weather Aggregations: Rainfall and temperature are recorded as annual cumulative and mean aggregates. Annual metrics cannot capture short-interval intra-seasonal weather shocks—such as mid-season dry spells during flowering or acute heatwaves during grain filling—which strongly suppress final yields [30, 31].",
        bold_prefix="2. Intra-Seasonal Weather Granularity: "
    )
    add_p(doc, 
        "3. Omission of Soil Physiochemical and Satellite Features: The consolidated datasets do not incorporate soil chemical parameters (e.g., pH, cation exchange capacity, organic carbon, N-P-K concentrations) or high-resolution satellite remote sensing vegetation indices (e.g., NDVI, EVI) [5, 19]. Crop yield estimation relied entirely on macroscopic inputs and geographical proxies.",
        bold_prefix="3. Absence of Soil and Remote Sensing Data: "
    )
    add_p(doc, 
        "4. Instance-Based Scalability and Memory Footprint: While distance-weighted KNN provides sub-millisecond query execution on our 13,130-record dataset, instance-based algorithms have O(N * d) time complexity per prediction and require storing all training vectors in memory. Scaling this approach to continental field-level datasets with millions of farm records would necessitate approximate nearest-neighbor indexing (e.g., HNSW or ScaNN) [2, 14].",
        bold_prefix="4. KNN Computational and Memory Scaling: "
    )
    add_p(doc, 
        "5. Geographic Generalization and Distributional Drift: Models were calibrated on historical records spanning 101 countries. Extrapolating predictions to unrepresented nations or regions experiencing severe novel climate anomalies may induce out-of-distribution errors.",
        bold_prefix="5. Regional Extrapolation and Climate Shift: "
    )
    
    # -------------------------------------------------------------
    # 11. FUTURE WORK
    # -------------------------------------------------------------
    add_h(doc, "11. FUTURE WORK", 1)
    
    add_p(doc, 
        "Based on the empirical insights and methodological findings of this research, several fruitful avenues for future investigation are identified:"
    )
    add_p(doc, "1. Ingestion of Multi-Spectral Satellite Imagery: Integrating optical and radar satellite earth observations (e.g., Sentinel-2 MSI, Landsat 8/9, Sentinel-1 SAR) to derive 10-day time-series vegetation indices (NDVI, NDRE) and surface moisture dynamics [5, 19].", bold_prefix="• ")
    add_p(doc, "2. High-Resolution Gridded Agro-Meteorology: Connecting the FastAPI prediction engine to daily gridded reanalysis weather datasets (e.g., ERA5-Land, CHIRPS) to capture intra-seasonal heat stress degree-days and precipitation distribution [10, 31].", bold_prefix="• ")
    add_p(doc, "3. Soil Digital Mapping Integration: Linking geographic coordinates with global soil databases (e.g., SoilGrids, ISRIC) to inject localized topsoil texture, pH, and organic matter into feature vectors [6].", bold_prefix="• ")
    add_p(doc, "4. Conformal Prediction and Calibrated Uncertainty Intervals: Implementing formal conformal prediction frameworks to guarantee distribution-free finite-sample prediction intervals for agricultural risk management.", bold_prefix="• ")
    add_p(doc, "5. Real-Time Explainability Dashboard: Integrating interactive SHAP summary plots into the production client dashboard, providing farmers with intuitive feature attributions for individual forecasts [13, 21].", bold_prefix="• ")
    
    # -------------------------------------------------------------
    # 12. CONCLUSION
    # -------------------------------------------------------------
    add_h(doc, "12. CONCLUSION", 1)
    
    add_p(doc, 
        "This research paper presented an empirical investigation into seasonal crop-yield prediction using machine learning across three consolidated international agricultural datasets: Kharif (4,404 records), Rabi (1,810 records), and Seasonal (6,916 records), covering 13,130 verified records across 101 countries from 1990 to 2013. By developing independent, season-specific prediction pipelines, the study addressed the structural limitations of monolithic modeling and prevented cross-season confounding between monsoon-dependent crops, winter cereals, and high-yield perennials."
    )
    add_p(doc, 
        "To replicate true operational agricultural forecasting and eliminate evaluation data leakage, models were developed strictly on historical records from 1990 to 2012 and evaluated prospectively on the unobserved 2013 calendar year holdout. Five regression algorithms were systematically benchmarked: Ordinary Least Squares Linear Regression (baseline), K-Nearest Neighbors, Gradient Boosting Regressor, XGBoost, and Multilayer Perceptron. After 3-fold time-aware hyperparameter optimization, tuned distance-weighted KNN achieved the strongest performance across all three seasonal pipelines, obtaining holdout R² scores of 0.9380 (RMSE = 14,026.44 hg/ha) for Kharif, 0.9636 (RMSE = 4,065.82 hg/ha) for Rabi, and 0.9642 (RMSE = 19,646.94 hg/ha) for Seasonal crops."
    )
    add_p(doc, 
        "Advanced diagnostic evaluations provided rigorous scientific backing for our conclusions: multi-year rolling-origin validation (2010–2013) demonstrated robust temporal stability; randomized cross-validation was shown to inflate R² by up to 2.2 percentage points over chronological holdouts; historical neighborhood deconstruction revealed that neighbor yield dispersion strongly tracks test prediction errors (r = 0.792 in Kharif); and paired Wilcoxon signed-rank tests established KNN's statistical superiority over XGBoost and Linear Regression (p < 0.05). Finally, the calibrated pipelines were successfully deployed into an authenticated FastAPI microservice application featuring JWT security, SQLite audit logging, and an interactive dashboard interface, providing a complete, reproducible pathway from data curation to production agricultural decision support."
    )
    
    # -------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------
    add_h(doc, "REFERENCES", 1)
    
    references = [
        "[1] Jayne, T. S., & Sanchez, P. A. (2021). Agricultural productivity must improve in sub-Saharan Africa. Science, 372(6546), 1045–1047. https://doi.org/10.1126/science.abf5413",
        "[2] El-Kenawy, E.-S. M., Alhussan, A. A., Khodadadi, N., Mirjalili, S., & Eid, M. M. (2025). Predicting potato crop yield with machine learning and deep learning for sustainable agriculture. Potato Research, 68(2), 759–792. https://doi.org/10.1007/s11540-024-09753-w",
        "[3] Ortiz-Bobea, A., Ault, T. R., Carrillo, C. M., Chambers, R. G., & Lobell, D. B. (2021). Anthropogenic climate change has slowed global agricultural productivity growth. Nature Climate Change, 11(4), 306–312. https://doi.org/10.1038/s41558-021-01000-1",
        "[4] Bali, N., & Singla, A. (2022). Emerging trends in machine learning to predict crop yield and study its influential factors: A survey. Archives of Computational Methods in Engineering, 29(1), 95–112. https://doi.org/10.1007/s11831-021-09569-8",
        "[5] Paudel, D., Boogaard, H., de Wit, A., Janssen, S., Osinga, S., Pylianidis, C., & Athanasiadis, I. N. (2021). Machine learning for large-scale crop yield forecasting. Agricultural Systems, 187, Article 103016. https://doi.org/10.1016/j.agsy.2020.103016",
        "[6] Abrougui, K., Gabsi, K., Mercatoris, B., Khemis, C., Amami, R., & Chehaibi, S. (2019). Prediction of organic potato yield using tillage systems and soil properties by artificial neural network (ANN) and multiple linear regressions (MLR). Soil and Tillage Research, 190, 202–208. https://doi.org/10.1016/j.still.2019.01.011",
        "[7] van Klompenburg, T., Kassahun, A., & Catal, C. (2020). Crop yield prediction using machine learning: A systematic literature review. Computers and Electronics in Agriculture, 177, Article 105709. https://doi.org/10.1016/j.compag.2020.105709",
        "[8] Noorunnahar, M., Chowdhury, A. H., & Mila, F. A. (2023). A tree based eXtreme gradient boosting (XGBoost) machine learning model to forecast the annual rice production in Bangladesh. PLoS ONE, 18(3), Article e0283452. https://doi.org/10.1371/journal.pone.0283452",
        "[9] Cedric, L. S., Adoni, W. Y. H., Aworka, R., Zoueu, J. T., Mutombo, F. K., Krichen, M., & Kimpolo, C. L. M. (2022). Crops yield prediction based on machine learning models: Case of West African countries. Smart Agricultural Technology, 2, Article 100049. https://doi.org/10.1016/j.atech.2022.100049",
        "[10] Kang, Y., Ozdogan, M., Zhu, X., Ye, Z., Hain, C., & Anderson, M. (2020). Comparative assessment of environmental variables and machine learning algorithms for maize yield prediction in the US Midwest. Environmental Research Letters, 15(6), Article 064005. https://doi.org/10.1088/1748-9326/ab7df9",
        "[11] Patnaik, P. P., & Padhy, N. (2023). An approach for potato yield prediction using machine learning regression algorithms. In Next Generation of Internet of Things (pp. 327–336). Springer Nature. https://doi.org/10.1007/978-981-19-1412-6_27",
        "[12] Paudel, D., Boogaard, H., de Wit, A., van der Velde, M., Claverie, M., Nisini, L., Janssen, S., Osinga, S., & Athanasiadis, I. N. (2022). Machine learning for regional crop yield forecasting in Europe. Field Crops Research, 276, Article 108377. https://doi.org/10.1016/j.fcr.2021.108377",
        "[13] Gupta, R., Jha, S. K., Kumar, P., & Yadav, M. (2026). Explainable ensemble machine learning algorithms for predicting wind speed by incorporating Shapley additive explanations. Franklin Open, 10, Article 100781. https://doi.org/10.1016/j.fraope.2026.100781",
        "[14] Zaki, A. M., Abdelhamid, A. A., Ibrahim, A., Eid, M. M., & El-Kenawy, E.-S. M. (2023). Enhancing K-nearest neighbors algorithm in wireless sensor networks through stochastic fractal search and particle swarm optimization. Journal of Cybersecurity and Information Management, 13(1), 76–84. https://doi.org/10.54216/JCIM.130108",
        "[15] Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. The Annals of Statistics, 29(5), 1189–1232. https://doi.org/10.1214/aos/1013203451",
        "[16] Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. In Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (pp. 785–794). ACM. https://doi.org/10.1145/2939672.2939785",
        "[17] Ahmed, J. H. (2023). A software framework for predicting the maize yield using modified multi-layer perceptron. Sustainability, 15(4), Article 3017. https://doi.org/10.3390/su15043017",
        "[18] Chai, T., & Draxler, R. R. (2014). Root mean square error (RMSE) or mean absolute error (MAE)? Arguments against avoiding RMSE in the literature. Geoscientific Model Development, 7(3), 1247–1250. https://doi.org/10.5194/gmd-7-1247-2014",
        "[19] Cao, J., Zhang, Z., Luo, Y., Zhang, L., Zhang, J., Li, Z., & Tao, F. (2021). Wheat yield predictions at a county and field scale with deep learning, machine learning, and Google Earth Engine. European Journal of Agronomy, 123, Article 126204. https://doi.org/10.1016/j.eja.2020.126204",
        "[20] Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825–2830.",
        "[21] Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In Advances in Neural Information Processing Systems (Vol. 30, pp. 4765–4774).",
        "[22] Durai, S. K. S., & Shamili, M. D. (2022). Smart farming using machine learning and deep learning techniques. Decision Analytics Journal, 3, Article 100041. https://doi.org/10.1016/j.daj.2022.100041",
        "[23] Mishra, P., et al. (2023). Forecasting potato production in major South Asian countries: A comparative study of machine learning and time series models. Potato Research, 67(4), 987–1006. https://doi.org/10.1007/s11540-023-09683-z",
        "[24] Fan, J., Bai, J., Li, Z., Ortiz-Bobea, A., & Gomes, C. P. (2022). A GNN-RNN approach for harnessing geospatial and temporal information: Application to crop yield prediction. In Proceedings of the AAAI Conference on Artificial Intelligence (Vol. 36, No. 11, pp. 11875–11883). https://doi.org/10.1609/aaai.v36i11.21444",
        "[25] Mateo-Sanchis, A., Adsuara, J. E., Piles, M., Muñoz-Marí, J., Perez-Suay, A., & Camps-Valls, G. (2023). Interpretable long short-term memory networks for crop yield estimation. IEEE Geoscience and Remote Sensing Letters, 20, 1–5. https://doi.org/10.1109/LGRS.2023.3244064",
        "[26] Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324",
        "[27] Cover, T., & Hart, P. (1967). Nearest neighbor pattern classification. IEEE Transactions on Information Theory, 13(1), 21–27. https://doi.org/10.1109/TIT.1967.1053964",
        "[28] Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. (2012). Leakage in data mining: Formulation, detection, and avoidance. ACM Transactions on Knowledge Discovery from Data, 6(4), Article 15. https://doi.org/10.1145/2382577.2382579",
        "[29] Kapoor, S., & Narayanan, A. (2023). Leakage and the reproducibility crisis in machine-learning-based science. Patterns, 4(9), Article 100804. https://doi.org/10.1016/j.patter.2023.100804",
        "[30] Lobell, D. B., & Field, C. B. (2007). Global scale climate–crop yield relationships and the impacts of recent warming. Environmental Research Letters, 2(1), Article 014002. https://doi.org/10.1088/1748-9326/2/1/014002",
        "[31] Schlenker, W., & Roberts, M. J. (2009). Nonlinear temperature effects indicate severe damages to U.S. crop yields under climate change. Proceedings of the National Academy of Sciences, 106(37), 15594–15598. https://doi.org/10.1073/pnas.0906865106",
        "[32] Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera-Arroita, G., Hauenstein, S., Lahoz-Monfort, J. J., Schröder, B., Thuiller, W., Warton, D. I., Wintle, B. A., Hartig, F., & Dormann, C. F. (2017). Cross-validation strategies for data with temporal, spatial, or hierarchical structure. Ecography, 40(8), 913–929. https://doi.org/10.1111/ecog.02881",
        "[33] Bergstra, J., & Bengio, Y. (2012). Random search for hyper-parameter optimization. Journal of Machine Learning Research, 13, 281–305.",
        "[34] Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning representations by back-propagating errors. Nature, 323(6088), 533–536. https://doi.org/10.1038/323533a0",
        "[35] Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., & Lee, S.-I. (2020). From local explanations to global understanding with explainable AI for trees. Nature Machine Intelligence, 2(1), 56–67. https://doi.org/10.1038/s42256-019-0138-9"
    ]
    
    for ref in references:
        p_ref = doc.add_paragraph()
        format_p(p_ref, before=1, after=4, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = "Calibri"
        r_ref.font.size = Pt(8.5)
        r_ref.font.color.rgb = RGBColor(51, 65, 85)
        
    # -------------------------------------------------------------
    # APPENDIX
    # -------------------------------------------------------------
    add_h(doc, "APPENDIX", 1)
    
    # Appendix A
    add_h(doc, "Appendix A: Complete Model Configurations and Hyperparameter Search Grids", 2)
    add_p(doc, 
        "Table A1 records the full hyperparameter configurations, search bounds, and selected parameters across all models and seasons."
    )
    
    add_tbl(doc, "A1", "Complete Model Configurations and Selected Parameters Used in the Final Experiments",
        ["Model Architecture", "Hyperparameter", "Search Grid", "Kharif Selected", "Rabi Selected", "Seasonal Selected"],
        [
            ["K-Nearest Neighbors", "n_neighbors\nweights\np (Minkowski power)", "[3, 5, 7, 9]\n['uniform', 'distance']\n[1, 2]", "3\ndistance\n2 (Euclidean)", "7\ndistance\n1 (Manhattan)", "3\ndistance\n1 (Manhattan)"],
            ["XGBoost Regressor", "n_estimators\nlearning_rate\nmax_depth", "[100, 150]\n[0.05, 0.1]\n[4, 6, 8]", "150\n0.05\n7", "150\n0.05\n6", "150\n0.05\n8"],
            ["Gradient Boosting", "n_estimators\nlearning_rate\nmax_depth", "[100, 150]\n[0.05, 0.1]\n[3, 4, 5]", "150\n0.05\n4", "150\n0.05\n3", "150\n0.05\n4"],
            ["Multilayer Perceptron", "hidden_layer_sizes\nactivation\nmax_iter", "[(64, 32), (100,)]\n['relu']\n[300, 500]", "(64, 32)\nrelu\n300", "(64, 32)\nrelu\n300", "(64, 32)\nrelu\n300"],
            ["Linear Regression", "fit_intercept", "[True]", "True", "True", "True"]
        ],
        [1.3, 1.2, 1.2, 1.0, 1.0, 1.0]
    )
    
    # Appendix B
    add_h(doc, "Appendix B: Reproducibility Notes", 2)
    add_p(doc, 
        "To ensure exact experimental replication, all code, configurations, and data artifacts are documented below:"
    )
    add_p(doc, "• Primary Analysis Code: notebooks/Seasonal_Crop_Yield_Prediction.ipynb and compute_advanced_analyses.py.", bold_prefix="1. Software Environment: ")
    add_p(doc, "• Software Versions: Python 3.12, Scikit-Learn 1.9.0, XGBoost 3.1.3, Pandas 3.0.5, NumPy 2.4.4, SciPy 1.15.2, Joblib 1.4.2.", bold_prefix="2. Library Versions: ")
    add_p(doc, "• Random Seed: Fixed seed 42 used for all stochastic initializations, tree building, and cross-validation splitting.", bold_prefix="3. Seed Specification: ")
    add_p(doc, "• Serialized Model Artifacts: Saved in models/ as kharif_model.joblib, rabi_model.joblib, and seasonal_model.joblib.", bold_prefix="4. Persisted Pipelines: ")
    add_p(doc, "• Evaluation Files: Evaluation metrics stored in results/tuned_model_evaluation.csv and results/advanced/.", bold_prefix="5. Result Datasets: ")
    
    # Appendix C
    add_h(doc, "Appendix C: Production API Request and Response Data Contract", 2)
    add_p(doc, 
        "Listing C1 illustrates the complete JSON REST contract for the POST /api/v1/predict production endpoint."
    )
    add_p(doc, 
        "POST /api/v1/predict HTTP/1.1\n"
        "Host: localhost:8000\n"
        "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...\n"
        "Content-Type: application/json\n\n"
        "{\n"
        '  "season": "Kharif",\n'
        '  "continent": "Africa",\n'
        '  "country": "Algeria",\n'
        '  "crop": "Maize",\n'
        '  "year": 2013,\n'
        '  "rainfall_mm": 89.0,\n'
        '  "pesticides_tonnes": 17278.65,\n'
        '  "avg_temp_c": 17.65\n'
        "}\n\n"
        "HTTP/1.1 200 OK\n"
        "Content-Type: application/json\n\n"
        "{\n"
        '  "prediction_id": 1042,\n'
        '  "season": "Kharif",\n'
        '  "crop": "Maize",\n'
        '  "country": "Algeria",\n'
        '  "predicted_yield_hg_ha": 24988.94,\n'
        '  "model_used": "Tuned K-Nearest Neighbors (k=3, Euclidean, distance-weighted)",\n'
        '  "pipeline_r2_score": 0.9380,\n'
        '  "pipeline_rmse_hg_ha": 14026.44,\n'
        '  "execution_time_ms": 1.45,\n'
        '  "status": "success"\n'
        "}",
        bold_prefix="Listing C1. Complete REST API Request and Response Data Contract:\n"
    )

print("paper_section_10_12_app.py created.")
