"""
paper_section_1.py
Title, Authors, Abstract, Keywords, and Section 1: INTRODUCTION.
"""

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from paper_common import format_p, add_p, add_h, set_cell_background, set_cell_margins, set_table_borders

def build_section_1(doc):
    # Running Header and Footer setup on section 0
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(0.9)
    section.bottom_margin = Inches(0.9)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)
    
    hp = section.header.paragraphs[0]
    format_p(hp, before=0, after=0, align=WD_ALIGN_PARAGRAPH.RIGHT)
    hr = hp.add_run("Predicting Crop Yield Across Kharif, Rabi and Seasonal Crops Using Machine Learning | Final Research Paper")
    hr.font.name = "Calibri"
    hr.font.size = Pt(8.5)
    hr.font.color.rgb = RGBColor(148, 163, 184)
    
    fp = section.footer.paragraphs[0]
    format_p(fp, before=0, after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    fr = fp.add_run("Final-Year B.Tech Capstone Project | SRM Institute of Science and Technology")
    fr.font.name = "Calibri"
    fr.font.size = Pt(8.5)
    fr.font.color.rgb = RGBColor(148, 163, 184)
    
    # Paper Title
    p_title = doc.add_paragraph()
    format_p(p_title, before=10, after=5, align=WD_ALIGN_PARAGRAPH.CENTER)
    rt = p_title.add_run("Predicting Crop Yield Across Kharif, Rabi and Seasonal Crops Using Machine Learning")
    rt.font.name = "Calibri"
    rt.font.size = Pt(17)
    rt.font.bold = True
    rt.font.color.rgb = RGBColor(30, 58, 138)
    
    # Authors
    p_auth = doc.add_paragraph()
    format_p(p_auth, before=2, after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    ra = p_auth.add_run("Indranil Gupta, Capstone Research Project Team")
    ra.font.name = "Calibri"
    ra.font.size = Pt(10.5)
    ra.font.bold = True
    ra.font.color.rgb = RGBColor(15, 23, 42)
    
    p_aff = doc.add_paragraph()
    format_p(p_aff, before=1, after=10, align=WD_ALIGN_PARAGRAPH.CENTER)
    raf = p_aff.add_run("Department of Computer Science and Engineering, SRM Institute of Science and Technology, Delhi-NCR Campus, India\nFinal-Year B.Tech Capstone Research Project")
    raf.font.name = "Calibri"
    raf.font.size = Pt(8.5)
    raf.font.italic = True
    raf.font.color.rgb = RGBColor(71, 85, 105)
    
    # Abstract Callout Box
    tbl_abs = doc.add_table(rows=1, cols=1)
    tbl_abs.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_abs = tbl_abs.cell(0, 0)
    cell_abs.width = Inches(6.7)
    set_cell_background(cell_abs, "F1F5F9")
    set_cell_margins(cell_abs, top=110, bottom=110, left=150, right=150)
    
    p_ab = cell_abs.paragraphs[0]
    format_p(p_ab, before=0, after=4, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    rab_h = p_ab.add_run("Abstract—")
    rab_h.font.name = "Calibri"
    rab_h.font.size = Pt(9.5)
    rab_h.font.bold = True
    rab_h.font.color.rgb = RGBColor(30, 58, 138)
    
    rab_t = p_ab.add_run(
        "Accurate crop-yield prediction is essential for national food security, agricultural supply chains, and forward-looking farm management amidst mounting climate volatility. While conventional machine-learning benchmarks often fit monolithic models that pool heterogeneous crops across disparate growing seasons, real-world agricultural productivity is strictly governed by seasonal phenology and distinct agro-climatic conditions. In this study, we formulate a season-aware machine-learning framework across three consolidated agricultural datasets: Kharif (4,404 records), Rabi (1,810 records), and Seasonal (6,916 records), comprising 13,130 verified international observations across 101 countries spanning 1990 to 2013. The feature inventory incorporates geographical context (Area, Continent), crop variety (Item), calendar epoch (Year), annual cumulative precipitation, national pesticide application, and average atmospheric temperature, strictly omitting unrecorded micro-climatic attributes such as relative humidity to preserve empirical validity. To replicate operational agricultural forecasting and eliminate temporal data leakage, models are developed and tuned exclusively on historical records from 1990 to 2012, reserving the entire calendar year 2013 (592 records) as an out-of-time prospective holdout. Five regression algorithms are systematically benchmarked: an Ordinary Least Squares Linear Regression baseline alongside four established nonlinear learners—K-Nearest Neighbors (KNN), Gradient Boosting Regressor, XGBoost Regressor, and Multilayer Perceptron (MLP). Systematic 3-fold time-aware hyperparameter optimization reveals that tuned distance-weighted KNN achieves the strongest empirical performance across all three seasonal pipelines, attaining holdout R² scores of 0.9380 (RMSE = 14,026.44 hg/ha; Pearson r = 0.9688) for Kharif, 0.9636 (RMSE = 4,065.82 hg/ha; Pearson r = 0.9868) for Rabi, and 0.9642 (RMSE = 19,646.94 hg/ha; Pearson r = 0.9827) for Seasonal multi-crop regimens. Diagnostic experiments show that random split evaluations inflate R² by up to 2.2 percentage points over chronological holdouts, while multi-year rolling-origin validation (2010–2013) demonstrates robust temporal stability (mean Kharif R² 0.9399). Neighborhood deconstruction verifies that historical neighbor dispersion correlates strongly with test prediction error (r = 0.792 in Kharif), and paired Wilcoxon signed-rank tests confirm KNN's statistical superiority over XGBoost and Linear Regression (p < 0.05). Finally, the calibrated pipelines are deployed in an authenticated FastAPI service featuring JWT authentication, SQLite audit logging, and an interactive dashboard."
    )
    rab_t.font.name = "Calibri"
    rab_t.font.size = Pt(8.5)
    rab_t.font.color.rgb = RGBColor(30, 41, 59)
    
    p_kw = cell_abs.add_paragraph()
    format_p(p_kw, before=4, after=0, align=WD_ALIGN_PARAGRAPH.LEFT)
    rkw_h = p_kw.add_run("Keywords: ")
    rkw_h.font.name = "Calibri"
    rkw_h.font.size = Pt(8.5)
    rkw_h.font.bold = True
    rkw_h.font.color.rgb = RGBColor(30, 58, 138)
    rkw_t = p_kw.add_run("Crop Yield Prediction; Seasonal Agriculture; Machine Learning; KNN Regression; Gradient Boosting; XGBoost; Multilayer Perceptron; Chronological Evaluation; Leakage Prevention; Smart Agriculture.")
    rkw_t.font.name = "Calibri"
    rkw_t.font.size = Pt(8.5)
    rkw_t.font.italic = True
    rkw_t.font.color.rgb = RGBColor(51, 65, 85)
    
    set_table_borders(tbl_abs, color="94A3B8", sz="6")
    
    sp0 = doc.add_paragraph()
    format_p(sp0, before=0, after=4)
    
    # -------------------------------------------------------------
    # 1. INTRODUCTION
    # -------------------------------------------------------------
    add_h(doc, "1. INTRODUCTION", 1)
    
    add_h(doc, "1.1 Problem Statement", 2)
    add_p(doc, 
        "Global agricultural production is confronting unprecedented structural challenges driven by demographic expansion, shifting dietary demands, accelerating climatic volatility, and natural resource scarcity. In this context, accurate crop-yield prediction serves as a foundational instrument for agricultural decision-making, national grain reserve management, international commodity trade, and early humanitarian famine warning systems [1, 3]. Agricultural yield—quantified as harvested mass per unit area in hectograms per hectare (hg/ha, where 1 hg/ha = 0.1 kg/ha)—is an inherently complex agro-ecological phenomenon governed by five major interconnected dimensions:"
    )
    
    add_p(doc, 
        "First, the fundamental importance of crop-yield prediction lies in its capacity to de-risk agricultural supply chains. Governments depend on forward yield forecasts to formulate import-export tariffs, allocate minimum support prices, and coordinate strategic food stockpiles. Simultaneously, agribusinesses and regional farmers rely on reliable yield estimates to plan storage logistics, pre-contract harvest transport, optimize machinery utilization, and procure seasonal financing [1, 5]. Inaccurate estimates induce severe market distortions, leading to catastrophic post-harvest grain gluts or localized food supply deficits.",
        bold_prefix="1. Strategic Importance of Yield Prediction: "
    )
    
    add_p(doc, 
        "Second, crop productivity is dictated by an intricate matrix of interacting environmental, biological, and anthropogenic factors. Macro-climatic drivers—specifically annual cumulative precipitation and atmospheric thermal regimes—govern photosynthetic efficiency, evapotranspiration rates, and phenological development stages [3, 30]. Anthropogenic inputs, particularly chemical crop protection agents (pesticides, fungicides, and herbicides), safeguard cultivated biomass against pathogen outbreaks and pest infestations. Furthermore, spatial geographic context (sovereign nations and continents) encapsulates regional agronomic infrastructure, soil fertility regimes, irrigation penetration, and agricultural mechanization levels [4, 10].",
        bold_prefix="2. Multi-Factor Agro-Environmental Interactions: "
    )
    
    add_p(doc, 
        "Third, traditional crop yield estimation methodologies exhibit substantial structural limitations. Conventional approaches predominantly rely on retrospective farm-level sample surveys, post-harvest crop-cutting experiments (CCEs), and subjective agronomic expert heuristics [4, 7]. While sample-based field assessments offer localized ground truth, they are labor-intensive, logistically cumbersome, cost-prohibitive across vast geographic territories, and fundamentally incapable of generating actionable pre-harvest predictions [5, 12]. Furthermore, empirical agro-meteorological indices frequently fail to capture complex non-linear responses to extreme weather anomalies [31].",
        bold_prefix="3. Limitations of Traditional Yield Estimation: "
    )
    
    add_p(doc, 
        "Fourth, machine-learning paradigms have emerged as powerful data-driven alternatives capable of learning non-linear, multi-dimensional functional mappings directly from observational agricultural datasets without requiring rigid biophysical parameterization [5, 7]. Algorithms such as K-Nearest Neighbors, Gradient Boosted Decision Trees, Extreme Gradient Boosting (XGBoost), and Deep Multilayer Perceptrons can capture non-linear relationships and high-order feature interactions, delivering superior predictive accuracy across diverse geographic regimes [2, 8, 16].",
        bold_prefix="4. Transformative Role of Machine Learning: "
    )
    
    add_p(doc, 
        "Fifth, agricultural production is strictly organized around distinct seasonal cultivation regimes that cannot be treated as a single monolithic domain. The Kharif season (dominated by warm, monsoon-dependent crops such as Maize, Sorghum, and Cassava) operates under high moisture and elevated thermal conditions. In contrast, the Rabi season (dominated by winter-grown crops such as Wheat) relies on cooler atmospheric windows and controlled irrigation. The Seasonal multi-crop category covers perennial, irrigated, or continuous-harvest commodities (such as Potatoes, Rice paddy, and Soybeans) with vastly higher biomass yields. Fitting a single undifferentiated global model pools these conflicting agro-ecological relationships, diluting predictive precision across seasons [9, 10].",
        bold_prefix="5. Necessity of Season-Specific Modeling: "
    )
    
    add_h(doc, "1.2 Motivation", 2)
    add_p(doc, 
        "This research is motivated by two critical methodological challenges in contemporary agricultural machine learning. First, while recent literature demonstrates that ensemble models and neural networks achieve high nominal accuracy on tabular agricultural datasets [2, 7, 8], most published studies pool observations across heterogeneous growing seasons. Forcing monsoon-dependent Kharif crops and temperate Rabi cereals into a solitary global regression model risks confounding crop-specific responses to temperature and precipitation, obscuring distinct physiological thresholds. Constructing independent, season-specific pipelines enables each model to specialize within its respective agronomic regime."
    )
    add_p(doc, 
        "Second, a pervasive limitation in published agricultural predictive models is the uncritical adoption of randomized cross-validation and random train-test splitting [7, 28]. In time-dependent agricultural systems, random splitting allows historical models to be evaluated on past test samples while training on future harvest records from identical geographic regions, creating subtle but pervasive temporal data leakage [29, 32]. In commercial farming and national planning, models must forecast future unobserved crop years strictly from past historical records. This motivates our enforcement of an out-of-time chronological validation design: models are trained exclusively on historical data from 1990 to 2012, reserving the final calendar year 2013 as an untouched prospective holdout."
    )
    
    add_h(doc, "1.3 Research Questions", 2)
    add_p(doc, 
        "To provide a rigorous scientific framework, this investigation addresses five primary research questions:"
    )
    add_p(doc, "RQ1. How do Linear Regression, K-Nearest Neighbors (KNN), Gradient Boosting, XGBoost, and Multilayer Perceptron (MLP) compare in predictive accuracy and computational stability across Kharif, Rabi, and Seasonal agricultural datasets?", bold_prefix="• ")
    add_p(doc, "RQ2. Does season-specific modeling provide measurable predictive advantages, reduced error dispersion, and improved agronomic fidelity compared to a monolithic pooled agricultural model?", bold_prefix="• ")
    add_p(doc, "RQ3. How does a prospective chronological out-of-time evaluation protocol affect performance estimates relative to standard randomized cross-validation, and what is the magnitude of the resulting generalization gap?", bold_prefix="• ")
    add_p(doc, "RQ4. What underlying data manifold properties explain tuned KNN's competitive performance on this tabular representation, and how reliable are its historical neighborhood predictions under feature ablation?", bold_prefix="• ")
    add_p(doc, "RQ5. Which environmental and agricultural predictor variables contribute most significantly to model predictions across the different seasonal regimes?", bold_prefix="• ")
    
    add_h(doc, "1.4 Objectives", 2)
    add_p(doc, 
        "The overarching aim of this study is to formulate, evaluate, and operationalize a season-aware machine-learning framework for international crop-yield forecasting. The specific research objectives are as follows:"
    )
    add_p(doc, "1. Curate, audit, and validate three independent international agricultural datasets—Kharif (4,404 records), Rabi (1,810 records), and Seasonal (6,916 records)—encompassing 13,130 verified records across 101 countries over the 1990–2013 period.", bold_prefix="1. ")
    add_p(doc, "2. Implement an automated, leakage-free preprocessing pipeline incorporating One-Hot Encoding for categorical features and StandardScaler normalization fitted strictly on the training partition.", bold_prefix="2. ")
    add_p(doc, "3. Enforce a chronological out-of-time evaluation protocol partitioning the data into a 1990–2012 development corpus and a 2013 prospective holdout test set to simulate true operational deployment.", bold_prefix="3. ")
    add_p(doc, "4. Benchmark five diverse regression algorithms—Ordinary Least Squares Linear Regression, distance-weighted KNN, Gradient Boosting Regressor, XGBoost, and MLP—using time-aware 3-fold hyperparameter optimization.", bold_prefix="4. ")
    add_p(doc, "5. Conduct extensive diagnostic evaluations, including temporal distribution shift analysis, multi-year rolling-origin validation, random vs. chronological validation, pooled vs. season-specific comparisons, and KNN neighborhood deconstruction.", bold_prefix="5. ")
    add_p(doc, "6. Engineer and deploy an authenticated, production-grade FastAPI microservice architecture backed by SQLite relational persistence, JWT security, and an interactive dashboard interface.", bold_prefix="6. ")
    
    add_h(doc, "1.5 Contributions", 2)
    add_p(doc, 
        "Diverging from existing literature that reports undifferentiated model benchmarks, this paper makes four distinct, non-duplicated contributions to agricultural machine learning and software engineering:"
    )
    add_p(doc, "1. Season-Specific Agricultural Modeling Architecture: We establish and empirically validate separate machine-learning pipelines tailored to the physiological and climatic characteristics of Kharif, Rabi, and Seasonal crops, proving that isolating seasonal regimes avoids cross-season confounding and improves predictive fidelity.", bold_prefix="1. ")
    add_p(doc, "2. Leakage-Free Chronological Benchmark & Diagnostic Protocol: We deliver a verified, reproducible benchmark on an untouched 2013 prospective holdout across 101 nations, accompanied by empirical distribution shift quantification (Kolmogorov-Smirnov and Wasserstein metrics), multi-year rolling-origin validation (2010–2013), and a diagnostic measurement of the optimistic generalization gap induced by random splitting.", bold_prefix="2. ")
    add_p(doc, "3. Empirical Model Comparison with Mathematical KNN Neighborhood Deconstruction: We present a rigorous comparative evaluation of five regression architectures, establishing an explicit Ordinary Least Squares linear baseline against four nonlinear models, while providing full mathematical deconstruction and empirical verification of distance-weighted KNN neighborhood clustering, dispersion bounds, and feature ablation sensitivity.", bold_prefix="3. ")
    add_p(doc, "4. Production-Ready Full-Stack Decision Support System: We translate experimental models into an operational, enterprise-grade software system featuring asynchronous FastAPI microservices, cryptographic JWT authentication, SQLite prediction audit logging, and a responsive web dashboard.", bold_prefix="4. ")
    
    add_h(doc, "1.6 Paper Organization", 2)
    add_p(doc, 
        "The remainder of this research paper is structured as follows. Section 2 reviews related work in crop-yield prediction, agricultural machine learning, seasonal modeling, temporal validation, and explainability, establishing the specific research gaps addressed. Section 3 describes the Kharif, Rabi, and Seasonal datasets, feature inventories, and data quality audits. Section 4 presents the end-to-end methodology, preprocessing formulations, regression models, hyperparameter tuning protocols, and evaluation metrics. Section 5 provides exploratory data analysis. Section 6 details experimental design. Section 7 presents empirical results and advanced diagnostic evaluations. Section 8 provides a discussion of model behavior and limitations. Section 9 describes system implementation and deployment. Section 10 assesses reliability, limitations, and threats to validity. Section 11 outlines future research, and Section 12 concludes the paper. Appendices provide model configurations, reproducibility notes, and mathematical examples."
    )

print("paper_section_1.py created.")
