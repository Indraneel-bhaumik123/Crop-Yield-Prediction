import re

script_path = r'C:\Users\indra\OneDrive\Desktop\Seasonal Crop Yield Prediction\Seasonal_Crop_Yield_Prediction_Rebuilt\build_submission_paper.py'

with open(script_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Exact 500-word combined paragraph with 8 research paper citations [1], [3], [7], [4], [2], [5], [10], [12]
combined_paragraph = (
    "Agricultural productivity constitutes the fundamental backbone of global food security, macroeconomic stability, "
    "and rural livelihoods, yet satisfying the caloric demands of an accelerating worldwide population requires precise, "
    "timely, and agro-climatically localized crop yield forecasts [1]. Standardized in hectograms per hectare (hg/ha, where "
    "1 hg/ha = 0.1 kg/ha), harvested agricultural yields exhibit substantial inter-annual and seasonal volatility driven "
    "by non-linear interactions among atmospheric weather fluctuations, agronomic fertilizer and pesticide applications, "
    "geographic soil compositions, and cultivar-specific phenology [3]. Historically, agricultural yield estimation has "
    "relied upon retrospective field surveys, post-harvest census sampling, agrometeorological index averages, and subjective "
    "expert heuristics [7]. While these traditional empirical frameworks provide valuable archival baselines, they are "
    "labor-intensive, logistically slow, spatially constrained, and inherently incapable of generating early pre-harvest "
    "yield projections required for proactive grain reserve management, commodity market pricing, grain storage logistics, "
    "and national humanitarian relief planning [4]. Machine learning algorithms have emerged as an effective data-driven "
    "paradigm for modeling complex agro-ecological dependencies directly from historical multi-decade datasets without "
    "imposing restrictive parametric assumptions or requiring intractable mechanistic biophysical simulations [2]. "
    "Nevertheless, a widespread and critical methodological deficiency across published agricultural yield studies is the "
    "pervasive practice of aggregating multi-season harvest records into single monolithic regression models. In South Asian "
    "and tropical global agricultural ecosystems across 101 countries, crop cultivation is fundamentally governed by "
    "distinct cropping seasons exhibiting divergent hydrological, thermal, and biological mechanisms [5]. Warm-season "
    "Kharif crops, such as maize, cassava, and sorghum, rely directly on monsoon precipitation, active solar radiation, "
    "and elevated summer temperatures, whereas cool-season Rabi crops, such as winter wheat, depend on residual soil "
    "moisture, regulated irrigation infrastructure, and cooler thermal envelopes. Furthermore, perennial and commercial "
    "commodities, represented within broader seasonal datasets, exhibit distinct multi-month developmental cycles and "
    "year-round physiological dependencies. Consequently, fitting a single unstratified regression model across pooled "
    "seasons conflates divergent seasonal response functions, masks critical season-specific sensitivities, and produces "
    "conflicting parameter updates that degrade prospective forecasting accuracy [10]. This fundamental modeling limitation "
    "is further compounded by pervasive evaluation flaws in existing literature, where models are frequently assessed via "
    "randomized k-fold cross-validation that shuffles observations across calendar years, resulting in severe temporal data "
    "leakage and artificially inflated accuracy metrics that fail under true forward-looking prospective deployment [12]. "
    "Motivated by these agronomic realities and methodological gaps, this research develops a comprehensive, season-stratified "
    "machine learning framework encompassing dedicated Kharif, Rabi, and Seasonal pipelines trained strictly on historical "
    "observations spanning 1990 to 2012 and rigorously evaluating against a true chronological prospective holdout in 2013. "
    "By strictly enforcing this leak-free chronological evaluation protocol, we ensure models generalize reliably to unseen "
    "future agricultural cycles. By systematically benchmarking five diverse regression architectures—ranging from baseline "
    "Ordinary Least Squares to distance-weighted K-Nearest Neighbors, Gradient Boosting, XGBoost, and Multilayer Perceptrons—and "
    "subsequently deploying the calibrated champion pipelines into an authenticated, production-grade FastAPI web application "
    "backed by SQLite persistence, this study demonstrates how season-aware modeling, robust preprocessing, and leakage-free "
    "prospective validation resolve key operational hurdles in digital agriculture, empowering diverse agronomic stakeholders "
    "with dependable, reproducible, and scalable predictive decision support across volatile growing seasons."
)

# Search for the old 1.1 and 1.2 block
old_sec1_pattern = re.compile(
    r'add_heading_styled\(doc, "1\. INTRODUCTION", 1\)\s*'
    r'add_heading_styled\(doc, "1\.1 Problem Statement", 2\)\s*'
    r'add_p_linked\(doc, .*?\)\s*'
    r'add_heading_styled\(doc, "1\.2 Motivation", 2\)\s*'
    r'add_p_linked\(doc, .*?\)\s*'
    r'add_heading_styled\(doc, "1\.3 Research Objectives", 2\)',
    re.DOTALL
)

replacement_sec1 = (
    'add_heading_styled(doc, "1. INTRODUCTION", 1)\n\n'
    'add_heading_styled(doc, "1.1 Problem Statement and Motivation", 2)\n'
    f'add_p_linked(doc, "{combined_paragraph}")\n\n'
    'add_heading_styled(doc, "1.2 Research Objectives", 2)'
)

assert old_sec1_pattern.search(code) is not None, "Failed to match old Section 1.1 & 1.2 pattern!"
code = old_sec1_pattern.sub(replacement_sec1, code, count=1)

# Now update the remaining subsection numbers in Section 1:
# 1.4 Research Questions -> 1.3 Research Questions
code = code.replace('add_heading_styled(doc, "1.4 Research Questions", 2)', 'add_heading_styled(doc, "1.3 Research Questions", 2)')

# 1.5 Research Contributions -> 1.4 Research Contributions
code = code.replace('add_heading_styled(doc, "1.5 Research Contributions", 2)', 'add_heading_styled(doc, "1.4 Research Contributions", 2)')

# 1.6 Paper Organization -> 1.5 Paper Organization
code = code.replace('add_heading_styled(doc, "1.6 Paper Organization", 2)', 'add_heading_styled(doc, "1.5 Paper Organization", 2)')

# Update QC template summary for Section 1
old_qc_sec1 = '1. INTRODUCTION (1.1 Problem Statement, 1.2 Motivation, 1.3 Objectives, 1.4 Research Questions, 1.5 Contributions, 1.6 Organization)'
new_qc_sec1 = '1. INTRODUCTION (1.1 Problem Statement and Motivation [500 words, 8 citations], 1.2 Objectives, 1.3 Research Questions, 1.4 Contributions, 1.5 Organization)'
code = code.replace(old_qc_sec1, new_qc_sec1)

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully replaced Section 1.1 and 1.2 with the combined 500-word paragraph and 8 research paper hyperlinks.")
