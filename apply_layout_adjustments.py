import re

with open('generate_faculty_docx.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update format_p default
content = content.replace(
    'def format_p(p, before=0, after=5, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY):',
    'def format_p(p, before=0, after=3.5, line_spacing=1.08, align=WD_ALIGN_PARAGRAPH.JUSTIFY):'
)

# 2. Update add_p_linked default
content = content.replace(
    'def add_p_linked(doc, text, bold_prefix="", before=0, after=5, align=WD_ALIGN_PARAGRAPH.JUSTIFY):',
    'def add_p_linked(doc, text, bold_prefix="", before=0, after=3.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY):'
)

# 3. Update add_heading_styled spacing
old_headings = '''    if level == 1:
        format_p(h, before=14, after=5, align=WD_ALIGN_PARAGRAPH.LEFT)'''
new_headings = '''    if level == 1:
        format_p(h, before=8, after=2.5, align=WD_ALIGN_PARAGRAPH.LEFT)'''
content = content.replace(old_headings, new_headings)

old_h2 = '''    elif level == 2:
        format_p(h, before=10, after=4, align=WD_ALIGN_PARAGRAPH.LEFT)'''
new_h2 = '''    elif level == 2:
        format_p(h, before=6, after=2, align=WD_ALIGN_PARAGRAPH.LEFT)'''
content = content.replace(old_h2, new_h2)

old_h3 = '''    elif level == 3:
        format_p(h, before=7, after=3, align=WD_ALIGN_PARAGRAPH.LEFT)'''
new_h3 = '''    elif level == 3:
        format_p(h, before=4, after=1.5, align=WD_ALIGN_PARAGRAPH.LEFT)'''
content = content.replace(old_h3, new_h3)

# 4. Remove p_sp from add_table_above_caption and tighten padding
old_tbl_end = '''    if col_widths:
        for row in table.rows:
            for c_idx, w in enumerate(col_widths):
                if c_idx < len(row.cells):
                    row.cells[c_idx].width = Inches(w)
                    
    p_sp = doc.add_paragraph()
    format_p(p_sp, before=0, after=4)
    return table'''
new_tbl_end = '''    if col_widths:
        for row in table.rows:
            for c_idx, w in enumerate(col_widths):
                if c_idx < len(row.cells):
                    row.cells[c_idx].width = Inches(w)
    return table'''
content = content.replace(old_tbl_end, new_tbl_end)

content = content.replace('set_cell_margins(hdr_cells[i], top=70, bottom=70, left=50, right=50)', 'set_cell_margins(hdr_cells[i], top=45, bottom=45, left=45, right=45)')
content = content.replace('set_cell_margins(row_cells[c_idx], top=50, bottom=50, left=50, right=50)', 'set_cell_margins(row_cells[c_idx], top=30, bottom=30, left=45, right=45)')

# 5. Remove p_sp from add_omml_equation
old_eq_end = '''    set_table_borders(table, color="E2E8F0", sz="4")
    p_sp = doc.add_paragraph()
    format_p(p_sp, before=0, after=4)
    return table'''
new_eq_end = '''    set_table_borders(table, color="E2E8F0", sz="4")
    return table'''
content = content.replace(old_eq_end, new_eq_end)

# 6. Update figure spacing
content = content.replace('format_p(p_cap, before=10, after=3, align=WD_ALIGN_PARAGRAPH.LEFT)', 'format_p(p_cap, before=5, after=2, align=WD_ALIGN_PARAGRAPH.LEFT)')
content = content.replace('format_p(p_img, before=2, after=6, align=WD_ALIGN_PARAGRAPH.CENTER)', 'format_p(p_img, before=2, after=3, align=WD_ALIGN_PARAGRAPH.CENTER)')

# 7. Margins: 0.85 in
old_margins = '''for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)'''
new_margins = '''for section in doc.sections:
    section.top_margin = Inches(0.85)
    section.bottom_margin = Inches(0.85)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)'''
content = content.replace(old_margins, new_margins)

# 8. Simplify Table 3
old_table3 = '''# Table 3: Hyperparameter Tuning Grid & Selected Configurations (CAPTION ABOVE TABLE)
add_table_above_caption(doc, 3, "Hyperparameter Search Grids and Selected Configurations Across Seasonal Regimes",
    ["Model Family", "Evaluated Hyperparameter Search Grid", "Kharif Selected Configuration", "Rabi Selected Configuration", "Seasonal Selected Configuration"],
    [
        ["K-Nearest Neighbors (KNN)", "k: [3, 5, 7, 9]; weights: ['uniform', 'distance']; metric p: [1 (Manhattan), 2 (Euclidean)]", "k = 3, p = 2 (Euclidean), weights = 'distance'", "k = 7, p = 1 (Manhattan), weights = 'distance'", "k = 3, p = 1 (Manhattan), weights = 'distance'"],
        ["XGBoost Regressor", "n_estimators: [100, 150]; learning_rate: [0.05, 0.1]; max_depth: [4, 6, 7, 8]", "n_estimators = 150, lr = 0.05, max_depth = 7", "n_estimators = 150, lr = 0.05, max_depth = 6", "n_estimators = 150, lr = 0.05, max_depth = 8"],
        ["Gradient Boosting", "n_estimators: [100, 150]; learning_rate: [0.05, 0.1]; max_depth: [3, 4, 5]", "n_estimators = 150, lr = 0.05, max_depth = 4", "n_estimators = 150, lr = 0.05, max_depth = 3", "n_estimators = 150, lr = 0.05, max_depth = 4"],
        ["Multilayer Perceptron (MLP)", "hidden_layer_sizes: [(64, 32), (100,)]; activation: ['relu']; solver: ['adam']", "hidden_layers = (64, 32), solver = 'adam', max_iter = 200", "hidden_layers = (64, 32), solver = 'adam', max_iter = 200", "hidden_layers = (64, 32), solver = 'adam', max_iter = 200"],
        ["Linear Regression", "fit_intercept: [True]; copy_X: [True]", "OLS unregularized baseline", "OLS unregularized baseline", "OLS unregularized baseline"]
    ],
    [1.5, 2.0, 1.2, 1.2, 1.3]
)'''

new_table3 = '''# Table 3: Hyperparameter Tuning Grid & Selected Configurations (SIMPLIFIED 4-COLUMN DESIGN)
add_table_above_caption(doc, 3, "Hyperparameter Search Grids and Selected Configurations Across Seasonal Regimes",
    ["Model Architecture", "Tuned Parameters", "Evaluated Search Space", "Optimal Settings Across Seasons"],
    [
        ["K-Nearest Neighbors (KNN)", "Neighbors k, distance metric, weighting scheme", "k in [3, 5, 7, 9]; weights in ['uniform', 'distance']; metric p in [1 (Manhattan), 2 (Euclidean)]", "• Kharif: k=3, Euclidean (p=2), distance\\n• Rabi: k=7, Manhattan (p=1), distance\\n• Seasonal: k=3, Manhattan (p=1), distance"],
        ["XGBoost Regressor", "Number of estimators, learning rate, max tree depth", "n_estimators in [100, 150]; lr in [0.05, 0.1]; max_depth in [4, 6, 7, 8]", "n_estimators = 150, lr = 0.05; max_depth = 7 (Kharif), 6 (Rabi), 8 (Seasonal)"],
        ["Gradient Boosting", "Number of estimators, learning rate, max tree depth", "n_estimators in [100, 150]; lr in [0.05, 0.1]; max_depth in [3, 4, 5]", "n_estimators = 150, lr = 0.05; max_depth = 4 (Kharif, Seasonal), 3 (Rabi)"],
        ["Multilayer Perceptron (MLP)", "Hidden layer topology, activation, solver, epochs", "hidden_layer_sizes in [(64, 32), (100,)]; activation in ['relu']; solver in ['adam']", "hidden_layers = (64, 32), solver = 'adam', max_iter = 200 (all seasonal cohorts)"],
        ["Linear Regression (Baseline)", "Intercept fitting, data centering", "Parametric Ordinary Least Squares (OLS) with intercept", "Unregularized OLS baseline fitted across all cohorts"]
    ],
    [1.5, 1.4, 1.8, 1.8]
)'''
content = content.replace(old_table3, new_table3)

# 9. Resize figures to avoid unnecessary full-page overflows
replacements = [
    ('fig01_dataset_composition.png", 2,\n    "Dataset Composition Across Agricultural Seasons",\n    "Proportional share and sample count across Kharif (4,404 records), Rabi (1,810 records), and Seasonal (6,916 records) agricultural corpora (Total N = 13,130).",\n    width=5.8)',
     'fig01_dataset_composition.png", 2,\n    "Dataset Composition Across Agricultural Seasons",\n    "Proportional share and sample count across Kharif (4,404 records), Rabi (1,810 records), and Seasonal (6,916 records) agricultural corpora (Total N = 13,130).",\n    width=4.8)'),
    ('fig02_crop_distribution.png", 3,\n    "Crop Representation Across Consolidated Global Dataset",\n    "Frequency distribution of records across individual crop varieties within the Kharif, Rabi, and Seasonal agricultural partitions.",\n    width=5.8)',
     'fig02_crop_distribution.png", 3,\n    "Crop Representation Across Consolidated Global Dataset",\n    "Frequency distribution of records across individual crop varieties within the Kharif, Rabi, and Seasonal agricultural partitions.",\n    width=4.8)'),
    ('fig04_yield_over_time.png", 4,\n    "Historical Yield Trajectory Over Time (1990–2013)",\n    "Longitudinal evolution of mean crop yield across agricultural seasons from 1990 to 2013, with the prospective 2013 holdout boundary highlighted.",\n    width=5.6)',
     'fig04_yield_over_time.png", 4,\n    "Historical Yield Trajectory Over Time (1990–2013)",\n    "Longitudinal evolution of mean crop yield across agricultural seasons from 1990 to 2013, with the prospective 2013 holdout boundary highlighted.",\n    width=4.8)'),
    ('fig05_rainfall_vs_yield.png", 5,\n    "Annual Rainfall vs. Crop Yield",\n    "Bivariate scatter plot and polynomial trend fit showing the non-linear relationship between average annual rainfall and crop yield across seasonal groups.",\n    width=5.6)',
     'fig05_rainfall_vs_yield.png", 5,\n    "Annual Rainfall vs. Crop Yield",\n    "Bivariate scatter plot and polynomial trend fit showing the non-linear relationship between average annual rainfall and crop yield across seasonal groups.",\n    width=4.8)'),
    ('fig06_temperature_vs_yield.png", 6,\n    "Average Temperature vs. Crop Yield",\n    "Thermal response curve and bivariate distribution illustrating optimal temperature ranges for agricultural yield across seasonal groupings.",\n    width=5.6)',
     'fig06_temperature_vs_yield.png", 6,\n    "Average Temperature vs. Crop Yield",\n    "Thermal response curve and bivariate distribution illustrating optimal temperature ranges for agricultural yield across seasonal groupings.",\n    width=4.8)'),
    ('fig07_pesticides_vs_yield.png", 7,\n    "National Pesticide Application vs. Harvested Yield",\n    "Bivariate distribution showing crop yield responses as a function of nationwide pesticide utilization on a logarithmic scale.",\n    width=5.6)',
     'fig07_pesticides_vs_yield.png", 7,\n    "National Pesticide Application vs. Harvested Yield",\n    "Bivariate distribution showing crop yield responses as a function of nationwide pesticide utilization on a logarithmic scale.",\n    width=4.8)'),
    ('fig08_correlation_heatmap.png", 8,\n    "Correlation Heatmap Across Numerical Features",\n    "Pairwise Pearson correlation coefficients between numerical predictors (Year, Rainfall, Pesticides, Temperature) and crop yield.",\n    width=5.6)',
     'fig08_correlation_heatmap.png", 8,\n    "Correlation Heatmap Across Numerical Features",\n    "Pairwise Pearson correlation coefficients between numerical predictors (Year, Rainfall, Pesticides, Temperature) and crop yield.",\n    width=4.5)'),
    ('fig_yield_distribution_violin_box.png", 9,\n    "Historical Crop Yield Distributions Across Agricultural Seasons",\n    "Violin density plots (Panel a) and logarithmic-scale box plots (Panel b) of crop yields across Kharif, Rabi, and Seasonal cohorts, illustrating severe right-skewness and multimodality.",\n    width=5.8)',
     'fig_yield_distribution_violin_box.png", 9,\n    "Historical Crop Yield Distributions Across Agricultural Seasons",\n    "Violin density plots (Panel a) and logarithmic-scale box plots (Panel b) of crop yields across Kharif, Rabi, and Seasonal cohorts, illustrating severe right-skewness and multimodality.",\n    width=4.8)'),
    ('fig_model_performance_with_ci.png", 10,\n    "Prospective Model Performance with 95% Bootstrap Confidence Intervals",\n    "Comparative test RMSE (Panel a) and coefficient of determination R² (Panel b) across five regression architectures on the 2013 holdout, with error bars indicating 95% bootstrap confidence intervals.",\n    width=5.8)',
     'fig_model_performance_with_ci.png", 10,\n    "Prospective Model Performance with 95% Bootstrap Confidence Intervals",\n    "Comparative test RMSE (Panel a) and coefficient of determination R² (Panel b) across five regression architectures on the 2013 holdout, with error bars indicating 95% bootstrap confidence intervals.",\n    width=4.8)'),
    ('fig_enhanced_actual_vs_predicted.png", 11,\n    "Actual vs. Predicted Yield Parity Across Seasonal Holdouts",\n    "Scatter plots of observed vs. predicted crop yields on the 2013 prospective holdouts for champion KNN models across Kharif, Rabi, and Seasonal pipelines, featuring the 45° identity line, empirical linear trend fit, R², RMSE, MAE, and sample size N.",\n    width=6.0)',
     'fig_enhanced_actual_vs_predicted.png", 11,\n    "Actual vs. Predicted Yield Parity Across Seasonal Holdouts",\n    "Scatter plots of observed vs. predicted crop yields on the 2013 prospective holdouts for champion KNN models across Kharif, Rabi, and Seasonal pipelines, featuring the 45° identity line, empirical linear trend fit, R², RMSE, MAE, and sample size N.",\n    width=5.0)'),
    ('fig_random_vs_chronological_comparison.png", 12,\n    "Prospective Generalization Error Under Chronological Holdout vs. Random Partitioning",\n    "Comparison of RMSE (Panel a) and R² (Panel b) across five model architectures on the Kharif dataset, illustrating the optimistic error reduction produced by randomized shuffling.",\n    width=5.8)',
     'fig_random_vs_chronological_comparison.png", 12,\n    "Prospective Generalization Error Under Chronological Holdout vs. Random Partitioning",\n    "Comparison of RMSE (Panel a) and R² (Panel b) across five model architectures on the Kharif dataset, illustrating the optimistic error reduction produced by randomized shuffling.",\n    width=4.8)'),
    ('fig_neighbor_distance_vs_error.png", 13,\n    "KNN Historical Neighborhood Distance vs. Absolute Prediction Error",\n    "Bivariate scatter plot with fitted regression line and 95% confidence interval band on the Kharif prospective holdout, demonstrating positive correlation between neighbor distance and absolute prediction error.",\n    width=5.6)',
     'fig_neighbor_distance_vs_error.png", 13,\n    "KNN Historical Neighborhood Distance vs. Absolute Prediction Error",\n    "Bivariate scatter plot with fitted regression line and 95% confidence interval band on the Kharif prospective holdout, demonstrating positive correlation between neighbor distance and absolute prediction error.",\n    width=4.8)'),
    ('fig_rainfall_temperature_response_surface.png", 14,\n    "Bivariate Agro-Climatic Response Surface for Predicted Crop Yield",\n    "Two-dimensional contour response surface illustrating non-linear interaction between annual precipitation and average growing temperature, demonstrating yield attenuation under high thermal stress.",\n    width=5.6)',
     'fig_rainfall_temperature_response_surface.png", 14,\n    "Bivariate Agro-Climatic Response Surface for Predicted Crop Yield",\n    "Two-dimensional contour response surface illustrating non-linear interaction between annual precipitation and average growing temperature, demonstrating yield attenuation under high thermal stress.",\n    width=4.8)'),
    ('fig12_system_architecture.png", 15,\n    "AgriYield Production System Architecture",\n    "Architectural data flow between the responsive web interface, FastAPI microservice, SQLite relational persistence, and serialized joblib model pipelines.",\n    width=5.8)',
     'fig12_system_architecture.png", 15,\n    "AgriYield Production System Architecture",\n    "Architectural data flow between the responsive web interface, FastAPI microservice, SQLite relational persistence, and serialized joblib model pipelines.",\n    width=4.8)'),
    ('ui_auth_modal.png", 16,\n    "AgriYield User Authentication Portal and Access Control Interface",\n    "Modal dialog supporting user authentication, new account creation, and role-based session token management.",\n    width=4.8)',
     'ui_auth_modal.png", 16,\n    "AgriYield User Authentication Portal and Access Control Interface",\n    "Modal dialog supporting user authentication, new account creation, and role-based session token management.",\n    width=3.8)'),
    ('ui_dashboard.png", 17,\n    "AgriYield Interactive Seasonal Crop Yield Prediction Dashboard",\n    "Operational dashboard displaying real-time prediction inputs (left panel) and inference results (right panel) with predicted yield (3,250 hg/ha), potential score (87/100), and factor impacts.",\n    width=5.8)',
     'ui_dashboard.png", 17,\n    "AgriYield Interactive Seasonal Crop Yield Prediction Dashboard",\n    "Operational dashboard displaying real-time prediction inputs (left panel) and inference results (right panel) with predicted yield (3,250 hg/ha), potential score (87/100), and factor impacts.",\n    width=4.8)')
]

for old_s, new_s in replacements:
    if old_s in content:
        content = content.replace(old_s, new_s)
    else:
        print("Warning: could not find:", old_s[:50])

with open('generate_faculty_docx.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated generate_faculty_docx.py successfully.")
