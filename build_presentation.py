"""
Script to generate the complete, professional, academic 15-slide PowerPoint presentation:
"SEASONAL CROP YIELD PREDICTION USING MACHINE LEARNING"
A Comparative Study Across Kharif, Rabi and Seasonal Agricultural Datasets

Outputs:
- FINAL_15_SLIDE_PROJECT_PRESENTATION.pptx
"""

import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

BASE_DIR = Path(r"c:\Users\indra\OneDrive\Desktop\Seasonal Crop Yield Prediction\Seasonal_Crop_Yield_Prediction_Rebuilt")
OUTPUT_PPTX = BASE_DIR / "FINAL_15_SLIDE_PROJECT_PRESENTATION.pptx"
FIG_DIR = BASE_DIR / "figures"
FIG_EDA = FIG_DIR / "eda"
FIG_EVAL = FIG_DIR / "evaluation"

# -----------------------------------------------------------------------------
# Color Palette Constants (Academic Agro-Tech Theme)
# -----------------------------------------------------------------------------
COLOR_BG = RGBColor(248, 250, 252)          # Slate 50 (Very soft off-white)
COLOR_WHITE = RGBColor(255, 255, 255)       # Pure White
COLOR_DARK_TEXT = RGBColor(15, 23, 42)      # Slate 900
COLOR_MUTED_TEXT = RGBColor(71, 85, 105)    # Slate 600
COLOR_LIGHT_MUTED = RGBColor(148, 163, 184) # Slate 400

# Primary Accents (Emerald / Forest Green)
COLOR_PRIMARY = RGBColor(21, 128, 61)       # Emerald 700
COLOR_PRIMARY_DARK = RGBColor(20, 83, 45)   # Emerald 900
COLOR_PRIMARY_LIGHT = RGBColor(220, 252, 231)# Emerald 100
COLOR_ACCENT_BLUE = RGBColor(37, 99, 235)   # Blue 600
COLOR_ACCENT_AMBER = RGBColor(217, 119, 6)  # Amber 600
COLOR_CARD_BORDER = RGBColor(226, 232, 240) # Slate 200
COLOR_CARD_BG = RGBColor(255, 255, 255)     # Card White
COLOR_CARD_ALT_BG = RGBColor(241, 245, 249) # Slate 100

FONT_HEADING = "Calibri"
FONT_BODY = "Calibri"

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # completely blank slide

    # Helper: Set slide background color
    def set_slide_background(slide, color=COLOR_BG):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background() # no border
        return bg

    # Helper: Create Header Block (Pill Category + Title + Subtitle + Slide Number)
    def add_header(slide, slide_num, category, title, subtitle=None):
        # Top banner line (emerald accent)
        top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
        top_line.fill.solid()
        top_line.fill.fore_color.rgb = COLOR_PRIMARY
        top_line.line.fill.background()

        # Category Pill Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(2.8), Inches(0.32))
        badge.fill.solid()
        badge.fill.fore_color.rgb = COLOR_PRIMARY_LIGHT
        badge.line.color.rgb = COLOR_PRIMARY
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        tf_b.word_wrap = False
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_b = tf_b.paragraphs[0]
        p_b.text = category.upper()
        p_b.font.name = FONT_HEADING
        p_b.font.size = Pt(9.5)
        p_b.font.bold = True
        p_b.font.color.rgb = COLOR_PRIMARY_DARK
        p_b.alignment = PP_ALIGN.CENTER

        # Slide Number Badge (Right top)
        num_box = slide.shapes.add_textbox(Inches(10.8), Inches(0.38), Inches(1.8), Inches(0.35))
        tf_n = num_box.text_frame
        tf_n.word_wrap = False
        p_n = tf_n.paragraphs[0]
        p_n.text = f"SLIDE {slide_num:02d} / 15"
        p_n.font.name = FONT_BODY
        p_n.font.size = Pt(10)
        p_n.font.bold = True
        p_n.font.color.rgb = COLOR_MUTED_TEXT
        p_n.alignment = PP_ALIGN.RIGHT

        # Main Title Box
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.8), Inches(0.75))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_DARK_TEXT

        if subtitle:
            p_s = tf_t.add_paragraph()
            p_s.text = subtitle
            p_s.font.name = FONT_BODY
            p_s.font.size = Pt(11)
            p_s.font.color.rgb = COLOR_MUTED_TEXT
            p_s.space_before = Pt(3)

    # Helper: Add Footer
    def add_footer(slide, source_text="Source: AgriYield Research Project & Empirical Benchmarks"):
        f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.8), Inches(0.32))
        tf = f_box.text_frame
        tf.word_wrap = False
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"📌 {source_text}  |  SRM Institute of Science and Technology (B.Tech Capstone Project 2025–2026)"
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_LIGHT_MUTED

    # Helper: Add Card Container
    def add_card(slide, left, top, width, height, bg_color=COLOR_WHITE, border_color=COLOR_CARD_BORDER, line_width=1):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(line_width)
        else:
            card.line.fill.background()
        return card

    # Helper: Add Speaker Notes
    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, COLOR_WHITE)

    # Decorative top and side bands
    band_top = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    band_top.fill.solid()
    band_top.fill.fore_color.rgb = COLOR_PRIMARY
    band_top.line.fill.background()

    # Left accent bar
    bar_left = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(0.12), Inches(4.5))
    bar_left.fill.solid()
    bar_left.fill.fore_color.rgb = COLOR_PRIMARY
    bar_left.line.fill.background()

    # Category Pill
    pill1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(1.5), Inches(3.8), Inches(0.38))
    pill1.fill.solid()
    pill1.fill.fore_color.rgb = COLOR_PRIMARY_LIGHT
    pill1.line.color.rgb = COLOR_PRIMARY
    pill1.line.width = Pt(1)
    tf_p1 = pill1.text_frame
    tf_p1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_p1 = tf_p1.paragraphs[0]
    p_p1.text = "FINAL-YEAR B.TECH CAPSTONE RESEARCH DEFENSE"
    p_p1.font.name = FONT_HEADING
    p_p1.font.size = Pt(9.5)
    p_p1.font.bold = True
    p_p1.font.color.rgb = COLOR_PRIMARY_DARK
    p_p1.alignment = PP_ALIGN.CENTER

    # Main Title
    t1_box = s1.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.2), Inches(2.0))
    tf1 = t1_box.text_frame
    tf1.word_wrap = True
    p1_1 = tf1.paragraphs[0]
    p1_1.text = "Seasonal Crop Yield Prediction\nUsing Machine Learning"
    p1_1.font.name = FONT_HEADING
    p1_1.font.size = Pt(36)
    p1_1.font.bold = True
    p1_1.font.color.rgb = COLOR_DARK_TEXT
    p1_1.space_after = Pt(10)

    p1_2 = tf1.add_paragraph()
    p1_2.text = "A Comparative Study Across Kharif, Rabi and Seasonal Agricultural Datasets"
    p1_2.font.name = FONT_BODY
    p1_2.font.size = Pt(16)
    p1_2.font.bold = True
    p1_2.font.color.rgb = COLOR_PRIMARY

    # Metadata Cards (2-column layout at bottom)
    card_meta = add_card(s1, Inches(1.1), Inches(4.3), Inches(11.4), Inches(2.0), bg_color=COLOR_CARD_ALT_BG)
    
    # Text inside card
    meta_box = s1.shapes.add_textbox(Inches(1.3), Inches(4.45), Inches(11.0), Inches(1.7))
    tf_m = meta_box.text_frame
    tf_m.word_wrap = True
    
    pm1 = tf_m.paragraphs[0]
    pm1.text = "PROJECT & RESEARCH TEAM DETAILS"
    pm1.font.size = Pt(10.5)
    pm1.font.bold = True
    pm1.font.color.rgb = COLOR_PRIMARY_DARK
    pm1.space_after = Pt(8)

    # 3 sub-columns of metadata
    pm2 = tf_m.add_paragraph()
    pm2.text = "• Candidate / Lead Researcher: Indranil Gupta (with Capstone Project Team)\n• Department: Department of Computer Science and Engineering\n• Institution: SRM Institute of Science and Technology, Delhi-NCR Campus, India\n• Academic Year: Final-Year B.Tech Capstone Project (2025–2026) | Target Variable: hg/ha_yield"
    pm2.font.size = Pt(11)
    pm2.font.color.rgb = COLOR_DARK_TEXT
    pm2.line_spacing = 1.3

    add_footer(s1, "Final-Year B.Tech Capstone Presentation | SRM Institute of Science and Technology")
    add_notes(s1, 
        "Good morning respected external examiners, project coordinator, and faculty committee members.\n\n"
        "Welcome to our final-year project presentation titled 'Seasonal Crop Yield Prediction Using Machine Learning: "
        "A Comparative Study Across Kharif, Rabi and Seasonal Agricultural Datasets'.\n\n"
        "In this work, we present a complete end-to-end research and software engineering effort. "
        "Unlike generic machine learning demonstrations, our work addresses the fundamental agricultural reality "
        "that crop yields do not follow a single monolithic pattern. They differ profoundly by seasonal regime: "
        "Kharif, Rabi, and Seasonal/Perennial cycles.\n\n"
        "Over the next 15 slides, we will walk you through our problem formulation, our consolidated multi-decade "
        "dataset of 13,130 records, rigorous chronological evaluation on a 2013 holdout, benchmark comparisons across "
        "five distinct regression models, and our working full-stack FastAPI deployment."
    )

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, 2, "Introduction & Motivation", "Problem Statement", 
               "Challenges in global agricultural forecasting and the need for season-stratified machine learning")

    # Left: Process Flow Diagram (Agriculture -> Data -> ML -> Early Prediction)
    add_card(s2, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1), bg_color=COLOR_WHITE)
    flow_box = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf_f = flow_box.text_frame
    tf_f.word_wrap = True

    pf0 = tf_f.paragraphs[0]
    pf0.text = "AGRONOMIC PROBLEM & SYSTEM PIPELINE"
    pf0.font.size = Pt(11.5)
    pf0.font.bold = True
    pf0.font.color.rgb = COLOR_PRIMARY_DARK
    pf0.space_after = Pt(12)

    steps = [
        ("1. Agro-Climatic Dynamics", "Crop yields fluctuate heavily due to rainfall, temperature extremes, pesticide application, and soil geography."),
        ("2. Traditional Limitations", "Conventional estimation relies on post-harvest surveys and manual reporting—too slow for proactive market intervention."),
        ("3. Seasonal Divergence", "Monsoon Kharif crops, winter Rabi crops, and multi-cycle crops possess distinct phenology, water needs, and yield distributions."),
        ("4. Data-Driven Solution", "Machine learning offers early, scalable in-season yield forecasting using accessible meteorological and agronomic features.")
    ]
    for stitle, sdesc in steps:
        p_st = tf_f.add_paragraph()
        p_st.text = f"▶ {stitle}"
        p_st.font.size = Pt(11)
        p_st.font.bold = True
        p_st.font.color.rgb = COLOR_DARK_TEXT
        p_st.space_before = Pt(6)

        p_sd = tf_f.add_paragraph()
        p_sd.text = sdesc
        p_sd.font.size = Pt(9.5)
        p_sd.font.color.rgb = COLOR_MUTED_TEXT
        p_sd.space_after = Pt(4)

    # Right: Key Research Challenges & Visual Cards
    right_cards = [
        ("High Yield Non-Linearity", "Yield response to inputs (e.g. rainfall and pesticides) is non-linear and exhibits saturation thresholds across different continents.", COLOR_PRIMARY_LIGHT, COLOR_PRIMARY_DARK),
        ("Cross-Season Disparity", "Treating Kharif, Rabi, and Seasonal crops under one single model causes massive skew and blurs season-specific feature sensitivities.", COLOR_CARD_ALT_BG, COLOR_DARK_TEXT),
        ("Data Leakage Risk in ML", "Random train-test splits leak future weather into historical training. Strict chronological out-of-time evaluation is mandatory for true prospective validity.", COLOR_CARD_ALT_BG, COLOR_DARK_TEXT)
    ]
    y_rc = 1.65
    for title_c, desc_c, bg_c, txt_c in right_cards:
        c_box = add_card(s2, Inches(6.7), Inches(y_rc), Inches(5.8), Inches(1.55), bg_color=bg_c)
        c_tb = s2.shapes.add_textbox(Inches(6.9), Inches(y_rc + 0.12), Inches(5.4), Inches(1.3))
        tf_c = c_tb.text_frame
        tf_c.word_wrap = True
        p_ct = tf_c.paragraphs[0]
        p_ct.text = title_c
        p_ct.font.size = Pt(11.5)
        p_ct.font.bold = True
        p_ct.font.color.rgb = txt_c
        p_ct.space_after = Pt(4)
        p_cd = tf_c.add_paragraph()
        p_cd.text = desc_c
        p_cd.font.size = Pt(9.5)
        p_cd.font.color.rgb = COLOR_MUTED_TEXT
        y_rc += 1.75

    add_footer(s2, "Agronomic Context and Problem Formulation")
    add_notes(s2,
        "Here on Slide 2, we establish the core problem statement.\n\n"
        "Agriculture is inherently volatile. Crop yields depend on complex non-linear interactions between weather "
        "(rainfall, temperature), agro-chemical inputs (pesticides), geographic soil suitability, and seasonal timing.\n\n"
        "Traditionally, agricultural census departments estimate yields through physical crop-cutting experiments "
        "and post-harvest reporting. While accurate, these reports arrive weeks or months AFTER harvest. "
        "By that time, supply chain bottlenecks have already occurred and food security policies are delayed.\n\n"
        "Secondly, existing academic papers often lump all crops and seasons into a single generic model. "
        "However, monsoon-dependent Kharif crops (like Maize and Sorghum) behave fundamentally differently from "
        "temperate irrigated Rabi crops (such as Wheat), and whole-year crops (like Potatoes and Cassava). "
        "This motivated our stratified, multi-pipeline architecture."
    )

    # =========================================================================
    # SLIDE 3: OBJECTIVES & RESEARCH QUESTIONS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, 3, "Research Scope", "Objectives and Research Questions", 
               "Systematic roadmap guiding data curation, model experimentation, and software deployment")

    # Left Column: 6 Research Objectives
    add_card(s3, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.1), bg_color=COLOR_WHITE)
    obj_box = s3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf_o = obj_box.text_frame
    tf_o.word_wrap = True

    po0 = tf_o.paragraphs[0]
    po0.text = "RESEARCH OBJECTIVES"
    po0.font.size = Pt(12)
    po0.font.bold = True
    po0.font.color.rgb = COLOR_PRIMARY_DARK
    po0.space_after = Pt(10)

    objectives = [
        "1. Multi-Decade Data Analysis: Audit 13,130 records across 101 countries from 1990 to 2013.",
        "2. Season-Specific Pipelines: Build dedicated Kharif, Rabi, and Seasonal feature pipelines.",
        "3. Multi-Model Benchmark: Compare five regressors (Linear, KNN, GBR, XGBoost, MLP).",
        "4. Leakage-Safe Evaluation: Implement strict chronological validation with 2013 holdout.",
        "5. Hyperparameter Optimization: Tune candidate models using time-aware cross-validation.",
        "6. Full-Stack Deployment: Deploy models via FastAPI backend, SQLite history, and responsive UI."
    ]
    for obj in objectives:
        po = tf_o.add_paragraph()
        po.text = obj
        po.font.size = Pt(10)
        po.font.color.rgb = COLOR_DARK_TEXT
        po.space_after = Pt(8)

    # Right Column: 4 Research Questions
    add_card(s3, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.1), bg_color=COLOR_WHITE)
    rq_box = s3.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf_r = rq_box.text_frame
    tf_r.word_wrap = True

    pr0 = tf_r.paragraphs[0]
    pr0.text = "CORE RESEARCH QUESTIONS"
    pr0.font.size = Pt(12)
    pr0.font.bold = True
    pr0.font.color.rgb = COLOR_PRIMARY_DARK
    pr0.space_after = Pt(10)

    rqs = [
        ("RQ1 — Model Comparison", "How do baseline Linear Regression, tree ensembles (GBR, XGBoost), neural networks (MLP), and distance-based models (KNN) compare in predictive accuracy?"),
        ("RQ2 — Seasonal Sensitivity", "How does predictive accuracy vary when models are tailored to specific agricultural regimes (Kharif monsoon vs. Rabi winter vs. Seasonal rotations)?"),
        ("RQ3 — Temporal Generalization", "Can models trained strictly on historical data (1990–2012) accurately predict an unseen future holdout year (2013) without lookahead leakage?"),
        ("RQ4 — Operational Deployment", "Which model architecture achieves the optimal balance of empirical accuracy, latency, and reliability for full-stack production serving?")
    ]
    for rq_title, rq_desc in rqs:
        p_rt = tf_r.add_paragraph()
        p_rt.text = f"❓ {rq_title}"
        p_rt.font.size = Pt(10.5)
        p_rt.font.bold = True
        p_rt.font.color.rgb = COLOR_ACCENT_BLUE
        p_rt.space_before = Pt(4)

        p_rd = tf_r.add_paragraph()
        p_rd.text = rq_desc
        p_rd.font.size = Pt(9.5)
        p_rd.font.color.rgb = COLOR_MUTED_TEXT
        p_rd.space_after = Pt(6)

    add_footer(s3, "Methodological Objectives and Scientific Inquiry")
    add_notes(s3,
        "Slide 3 frames our study scientifically around six objectives and four clear research questions.\n\n"
        "Our six objectives span the entire data engineering lifecycle: from dataset auditing, feature engineering, "
        "and 5-model benchmarking, through to hyperparameter tuning, chronological holdout evaluation, and FastAPI web deployment.\n\n"
        "Our four Research Questions represent the core inquiries examined by our committee:\n"
        "- RQ1 asks which family of algorithms performs strongest for yield regression.\n"
        "- RQ2 asks whether seasonal stratification provides distinct performance gains.\n"
        "- RQ3 tests temporal validity: unlike random K-Fold splits that shuffle future years into the past, our chronological 2013 holdout tests true forecasting realism.\n"
        "- RQ4 identifies the champion production model for deployment."
    )

    # =========================================================================
    # SLIDE 4: DATASET OVERVIEW
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, 4, "Data Engineering", "Dataset Overview: 3-Season Stratification", 
               "Consolidated multi-country agricultural dataset spanning 1990–2013 across 101 nations and 6 continents")

    # 3-Card Column Layout for Kharif, Rabi, Seasonal
    col_w = Inches(3.65)
    gap = Inches(0.4)
    y_c4 = Inches(1.65)
    h_c4 = Inches(3.6)

    seasons_data = [
        ("KHARIF PIPELINE", "4,404 Records (33.5%)", [
            ("Cultivation Regime", "Monsoon / Autumn Harvest"),
            ("Primary Crops", "Maize (46.0%), Sorghum (32.6%), Cassava (21.4%)"),
            ("Mean Rainfall", "1,248.5 mm / year"),
            ("Mean Temperature", "21.8 °C"),
            ("Key Dynamic", "High moisture sensitivity & coarse grains")
        ], COLOR_PRIMARY),
        ("RABI PIPELINE", "1,810 Records (13.8%)", [
            ("Cultivation Regime", "Winter / Spring Harvest"),
            ("Primary Crops", "Wheat (100.0% dedicated)"),
            ("Mean Rainfall", "856.2 mm / year"),
            ("Mean Temperature", "15.4 °C"),
            ("Key Dynamic", "Temperate, controlled irrigation & single-crop")
        ], COLOR_ACCENT_BLUE),
        ("SEASONAL PIPELINE", "6,916 Records (52.7%)", [
            ("Cultivation Regime", "Multi-Cycle & Perennial Staples"),
            ("Primary Crops", "Potatoes (30.2%), Rice (21.7%), Soybeans (18.0%), Sweet potatoes (16.8%), Yams, Plantains"),
            ("Mean Rainfall", "1,142.1 mm / year"),
            ("Mean Temperature", "19.6 °C"),
            ("Key Dynamic", "Broad yield variance & global staples")
        ], COLOR_ACCENT_AMBER)
    ]

    for i, (title_s, count_s, details, border_c) in enumerate(seasons_data):
        x_c4 = Inches(0.8) + i * (col_w + gap)
        card = add_card(s4, x_c4, y_c4, col_w, h_c4, bg_color=COLOR_WHITE, border_color=border_c, line_width=1.5)
        
        # Header inside card
        tb = s4.shapes.add_textbox(x_c4 + Inches(0.15), y_c4 + Inches(0.15), col_w - Inches(0.3), h_c4 - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = title_s
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = border_c
        
        p2 = tf.add_paragraph()
        p2.text = count_s
        p2.font.size = Pt(10.5)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_DARK_TEXT
        p2.space_after = Pt(8)

        for label, val in details:
            p_lbl = tf.add_paragraph()
            p_lbl.text = f"• {label}: {val}"
            p_lbl.font.size = Pt(9)
            p_lbl.font.color.rgb = COLOR_MUTED_TEXT
            p_lbl.space_after = Pt(3)

    # Bottom Summary Strip: Features, Target, and Quality Metrics
    strip = add_card(s4, Inches(0.8), Inches(5.45), Inches(11.75), Inches(1.4), bg_color=COLOR_CARD_ALT_BG)
    st_box = s4.shapes.add_textbox(Inches(1.0), Inches(5.55), Inches(11.35), Inches(1.2))
    tf_st = st_box.text_frame
    tf_st.word_wrap = True

    pst1 = tf_st.paragraphs[0]
    pst1.text = "DATA DICTIONARY & INTEGRITY AUDIT (13,130 TOTAL OBSERVATIONS)"
    pst1.font.size = Pt(10.5)
    pst1.font.bold = True
    pst1.font.color.rgb = COLOR_PRIMARY_DARK
    pst1.space_after = Pt(4)

    pst2 = tf_st.add_paragraph()
    pst2.text = (
        "• Common Features (8): Area (101 countries), Continent (6), Item (10 crops), Season (Kharif/Rabi/Seasonal), "
        "Year (1990–2013), Rainfall (mm/yr), Pesticides (tonnes), Temperature (°C)\n"
        "• Target Variable: hg/ha_yield (Hectograms per hectare; 1 hg/ha = 0.1 kg/ha)  |  "
        "• Quality Audit: 0 Missing Values (100% complete), 0 Duplicate Records"
    )
    pst2.font.size = Pt(9.5)
    pst2.font.color.rgb = COLOR_DARK_TEXT
    pst2.line_spacing = 1.3

    add_footer(s4, "Project Datasets: FAO & Global Agro-Climatic Observations (1990–2013)")
    add_notes(s4,
        "Moving to Slide 4, here is our empirical dataset breakdown.\n\n"
        "Our consolidated dataset contains exactly 13,130 historical crop observations spanning 24 years from 1990 to 2013, "
        "covering 101 countries across 6 continents.\n\n"
        "We partitioned the data into three agronomic pipelines:\n"
        "1. Kharif: 4,404 records (33.5% of dataset), representing monsoon-grown crops like Maize, Sorghum, and Cassava.\n"
        "2. Rabi: 1,810 records (13.8%), representing winter-grown Wheat across temperate growing regions.\n"
        "3. Seasonal: 6,916 records (52.7%), covering multi-cycle staples like Potatoes, Rice, Soybeans, and Sweet potatoes.\n\n"
        "Importantly, every record contains eight input features including country, continent, crop item, year, rainfall, "
        "pesticides, and ambient temperature, predicting our normalized target 'hg/ha_yield'.\n"
        "Our audit verified zero missing values and zero duplicate rows across all three datasets."
    )

    # =========================================================================
    # SLIDE 5: EXPLORATORY DATA ANALYSIS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, 5, "Data Engineering & EDA", "Exploratory Data Analysis: Real Project Figures", 
               "Visualizing empirical yield densities, crop compositions, and multi-decade temporal trends")

    # Embed 3 Actual Project Figures
    # 1. Yield Distribution
    img_yield = FIG_EDA / "01_yield_distribution_by_season.png"
    img_crop = FIG_EDA / "02_crop_distribution_breakdown.png"
    img_time = FIG_EDA / "04_temporal_yield_trajectory.png"

    # Layout: Top row has 3 graphs side-by-side or 2 top, 1 bottom
    # Let's do 3 graphs side-by-side in upper section:
    gw = Inches(3.75)
    gh = Inches(2.7)
    gy = Inches(1.65)

    if img_yield.exists():
        card_g1 = add_card(s5, Inches(0.8), gy, gw, gh + Inches(0.6), bg_color=COLOR_WHITE)
        s5.shapes.add_picture(str(img_yield), Inches(0.85), gy + Inches(0.35), gw - Inches(0.1), gh)
        t_b1 = s5.shapes.add_textbox(Inches(0.9), gy + Inches(0.05), gw - Inches(0.2), Inches(0.3))
        p = t_b1.text_frame.paragraphs[0]
        p.text = "(a) Yield Density by Season"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_DARK_TEXT

    if img_crop.exists():
        card_g2 = add_card(s5, Inches(4.8), gy, gw, gh + Inches(0.6), bg_color=COLOR_WHITE)
        s5.shapes.add_picture(str(img_crop), Inches(4.85), gy + Inches(0.35), gw - Inches(0.1), gh)
        t_b2 = s5.shapes.add_textbox(Inches(4.9), gy + Inches(0.05), gw - Inches(0.2), Inches(0.3))
        p = t_b2.text_frame.paragraphs[0]
        p.text = "(b) Crop Breakdown by Pipeline"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_DARK_TEXT

    if img_time.exists():
        card_g3 = add_card(s5, Inches(8.8), gy, gw, gh + Inches(0.6), bg_color=COLOR_WHITE)
        s5.shapes.add_picture(str(img_time), Inches(8.85), gy + Inches(0.35), gw - Inches(0.1), gh)
        t_b3 = s5.shapes.add_textbox(Inches(8.9), gy + Inches(0.05), gw - Inches(0.2), Inches(0.3))
        p = t_b3.text_frame.paragraphs[0]
        p.text = "(c) Temporal Yield Trajectory"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_DARK_TEXT

    # Bottom: 3 Concise Observations
    obs_card = add_card(s5, Inches(0.8), Inches(5.15), Inches(11.75), Inches(1.7), bg_color=COLOR_CARD_ALT_BG)
    obs_box = s5.shapes.add_textbox(Inches(1.0), Inches(5.25), Inches(11.35), Inches(1.5))
    tf_obs = obs_box.text_frame
    tf_obs.word_wrap = True

    po_t = tf_obs.paragraphs[0]
    po_t.text = "KEY EMPIRICAL OBSERVATIONS FROM PROJECT EDA"
    po_t.font.size = Pt(10.5)
    po_t.font.bold = True
    po_t.font.color.rgb = COLOR_PRIMARY_DARK
    po_t.space_after = Pt(4)

    obs_points = [
        "1. Yield Distribution Disparity: Seasonal crops show highest mean yield (98,125 hg/ha) with heavy right-tail skewness; Kharif averages 44,838 hg/ha; Rabi averages 30,783 hg/ha with compact, low variance.",
        "2. Crop Composition Specialization: Kharif is dominated by coarse grains/tubers (Maize 46%, Sorghum 33%); Rabi is 100% Wheat; Seasonal is anchored by high-yield tubers (Potatoes 30%, Rice 22%).",
        "3. Multi-Decadal Productivity Growth: Mean crop yields trend upward steadily from 1990 to 2012; the red vertical line highlights our chronological holdout boundary (2012/2013) ensuring no lookahead bias."
    ]
    for pt in obs_points:
        p_pt = tf_obs.add_paragraph()
        p_pt.text = f"• {pt}"
        p_pt.font.size = Pt(9.5)
        p_pt.font.color.rgb = COLOR_DARK_TEXT
        p_pt.space_after = Pt(3)

    add_footer(s5, "Project Datasets and Exploratory Data Analysis (EDA)")
    add_notes(s5,
        "Slide 5 presents our exploratory data analysis using the actual figures generated directly from our codebase.\n\n"
        "In Graph (a) on the left, you can observe the kernel density and box plots of crop yield across seasons. "
        "Notice the profound distribution differences: Seasonal crops average nearly 98,000 hg/ha with extreme high-yield "
        "outliers caused by potato cultivation. Kharif averages 44,800 hg/ha, while Rabi wheat is tightly clustered around 30,800 hg/ha.\n\n"
        "In Graph (b), our crop breakdown shows why a single model fails: Kharif consists of Maize, Sorghum, and Cassava; "
        "Rabi is 100% Wheat; and Seasonal features six diverse crops.\n\n"
        "In Graph (c), we plot the 24-year historical yield trajectory. There is a clear upward trend driven by agricultural "
        "technology, fertilizer adoption, and mechanization. Notice the red dashed line at 2012: that is our train-test split boundary, "
        "proving that our 2013 test set is strictly out-of-time."
    )

    # =========================================================================
    # SLIDE 6: DATA PREPROCESSING
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, 6, "Feature Engineering", "Data Preprocessing: Leakage-Safe Pipeline", 
               "Strict scikit-learn ColumnTransformer architecture fitted exclusively on historical training data")

    # Pipeline Flow Blocks (Horizontal steps)
    flow_steps = [
        ("Raw CSV Data", "13,130 Records\n3 Seasonal Splits"),
        ("Data Audit", "Verify 0 Missing\nVerify 0 Duplicates"),
        ("Categorical Encoding", "OneHotEncoder\n(handle_unknown='ignore')"),
        ("Numerical Scaling", "StandardScaler\n(Zero mean, unit variance)"),
        ("Feature Assembly", "ColumnTransformer\nSparse Matrix Output"),
        ("Model Training", "1990–2012 Fit\nStrict Boundary")
    ]
    step_w = Inches(1.8)
    step_gap = Inches(0.18)
    y_p = Inches(1.65)
    for i, (title_p, desc_p) in enumerate(flow_steps):
        x_p = Inches(0.8) + i * (step_w + step_gap)
        card_p = add_card(s6, x_p, y_p, step_w, Inches(1.5), 
                          bg_color=COLOR_PRIMARY_LIGHT if i in [2, 3] else COLOR_WHITE,
                          border_color=COLOR_PRIMARY if i in [2, 3] else COLOR_CARD_BORDER)
        tb = s6.shapes.add_textbox(x_p + Inches(0.05), y_p + Inches(0.1), step_w - Inches(0.1), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title_p
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_PRIMARY_DARK if i in [2, 3] else COLOR_DARK_TEXT
        p1.space_after = Pt(4)
        p2 = tf.add_paragraph()
        p2.text = desc_p
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = COLOR_MUTED_TEXT

    # 2 Detailed Cards Below Flow
    # Left Card: Detailed Feature Transformers
    add_card(s6, Inches(0.8), Inches(3.35), Inches(5.7), Inches(3.4), bg_color=COLOR_WHITE)
    t_box = s6.shapes.add_textbox(Inches(1.0), Inches(3.5), Inches(5.3), Inches(3.1))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True

    pt0 = tf_t.paragraphs[0]
    pt0.text = "TRANSFORMATION SPECIFICATIONS"
    pt0.font.size = Pt(11.5)
    pt0.font.bold = True
    pt0.font.color.rgb = COLOR_PRIMARY_DARK
    pt0.space_after = Pt(8)

    trans_details = [
        ("Categorical Features (3)", "Area (101 countries), Continent (6), Item (10 crops)", "OneHotEncoder(handle_unknown='ignore', sparse_output=False)", "Prevents unseen geographical categories in production from crashing the inference pipeline."),
        ("Numerical Features (4)", "Year, Rainfall (mm/yr), Pesticides (tonnes), Temperature (°C)", "StandardScaler()", "Standardizes features to zero mean and unit variance; vital for distance-weighted KNN and MLP convergence."),
        ("Target Variable (1)", "hg/ha_yield", "Unscaled Continuous Target", "Preserves exact physical agronomic scale (hg/ha) for direct stakeholder interpretability.")
    ]
    for name, cols, enc, purpose in trans_details:
        p_n = tf_t.add_paragraph()
        p_n.text = f"• {name}: {cols}"
        p_n.font.size = Pt(9.5)
        p_n.font.bold = True
        p_n.font.color.rgb = COLOR_DARK_TEXT

        p_e = tf_t.add_paragraph()
        p_e.text = f"  Method: {enc}"
        p_e.font.size = Pt(8.5)
        p_e.font.color.rgb = COLOR_ACCENT_BLUE

        p_u = tf_t.add_paragraph()
        p_u.text = f"  Rationale: {purpose}"
        p_u.font.size = Pt(8.5)
        p_u.font.color.rgb = COLOR_MUTED_TEXT
        p_u.space_after = Pt(4)

    # Right Card: Leakage Control Callout
    add_card(s6, Inches(6.8), Inches(3.35), Inches(5.75), Inches(3.4), bg_color=COLOR_CARD_ALT_BG, border_color=COLOR_PRIMARY, line_width=1.5)
    lc_box = s6.shapes.add_textbox(Inches(7.0), Inches(3.5), Inches(5.35), Inches(3.1))
    tf_lc = lc_box.text_frame
    tf_lc.word_wrap = True

    plc0 = tf_lc.paragraphs[0]
    plc0.text = "🔒 DATA LEAKAGE CONTROL CALLOUT"
    plc0.font.size = Pt(11.5)
    plc0.font.bold = True
    plc0.font.color.rgb = COLOR_PRIMARY_DARK
    plc0.space_after = Pt(8)

    leakage_points = [
        ("Strict Fit on Training Only", "All transformers (OneHotEncoder categories, StandardScaler means & variances) are computed ONLY on 1990–2012 records."),
        ("Zero Future Contamination", "Test holdout (2013) data is transformed strictly using frozen pre-computed training parameters."),
        ("Pipeline Encapsulation", "Both preprocessor and regressor are bundled into a single serialized scikit-learn Pipeline object (`joblib`), ensuring identical preprocessing during live FastAPI inference."),
        ("Production Robustness", "`handle_unknown='ignore'` guarantees that novel or rare regional inputs produce zero-vectors without throwing unhandled exceptions.")
    ]
    for l_title, l_desc in leakage_points:
        p_lt = tf_lc.add_paragraph()
        p_lt.text = f"▶ {l_title}"
        p_lt.font.size = Pt(9.5)
        p_lt.font.bold = True
        p_lt.font.color.rgb = COLOR_DARK_TEXT

        p_ld = tf_lc.add_paragraph()
        p_ld.text = l_desc
        p_ld.font.size = Pt(8.5)
        p_ld.font.color.rgb = COLOR_MUTED_TEXT
        p_ld.space_after = Pt(4)

    add_footer(s6, "Project Preprocessing Pipeline & scikit-learn Architecture")
    add_notes(s6,
        "Slide 6 details our data preprocessing and leakage prevention strategy.\n\n"
        "In machine learning for agriculture, data leakage is one of the most common methodological errors. "
        "Many published papers inadvertently fit their standardizers or one-hot encoders across the entire dataset "
        "before splitting into train and test sets. This leaks future distributional properties into the training model.\n\n"
        "To guarantee scientific integrity, our preprocessing is strictly encapsulated in a scikit-learn ColumnTransformer:\n"
        "- Categoricals (Country, Continent, Crop) are processed with OneHotEncoder with handle_unknown='ignore'.\n"
        "- Numericals (Year, Rainfall, Pesticides, Temperature) are scaled using StandardScaler.\n"
        "- Most critically, the pipeline is fit strictly on the 1990–2012 historical training partition. "
        "The 2013 holdout is transformed strictly using the frozen parameters from training."
    )

    # =========================================================================
    # SLIDE 7: EXPERIMENTAL METHODOLOGY
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, 7, "Methodology", "Experimental Methodology: Prospective Validation", 
               "Chronological holdout strategy simulating true prospective operational deployment")

    # Top: Visual Timeline
    time_w = Inches(3.6)
    y_tm = Inches(1.65)
    h_tm = Inches(1.7)

    t_steps = [
        ("1990 – 2012 (23 Years)", "HISTORICAL TRAINING SET", "• Kharif: 4,205 samples\n• Rabi: 1,729 samples\n• Seasonal: 6,604 samples\n• Total: 12,538 samples", COLOR_CARD_ALT_BG, COLOR_DARK_TEXT),
        ("Time-Aware GridSearch", "HYPERPARAMETER TUNING", "• 3-Fold Cross-Validation\n• Evaluated on training only\n• Metric: Negative RMSE\n• Optimizes distance & trees", COLOR_PRIMARY_LIGHT, COLOR_PRIMARY_DARK),
        ("2013 (Future Holdout)", "PROSPECTIVE TEST SET", "• Kharif: 199 samples\n• Rabi: 81 samples\n• Seasonal: 312 samples\n• Total: 592 samples", COLOR_CARD_ALT_BG, COLOR_DARK_TEXT)
    ]
    for i, (title_t, sub_t, bullet_t, bg_t, txt_t) in enumerate(t_steps):
        x_tm = Inches(0.8) + i * (time_w + Inches(0.48))
        card_tm = add_card(s7, x_tm, y_tm, time_w, h_tm, bg_color=bg_t, border_color=COLOR_PRIMARY if i==1 else COLOR_CARD_BORDER)
        tb = s7.shapes.add_textbox(x_tm + Inches(0.12), y_tm + Inches(0.1), time_w - Inches(0.24), h_tm - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title_t
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = txt_t
        p2 = tf.add_paragraph()
        p2.text = sub_t
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_PRIMARY
        p2.space_after = Pt(3)
        p3 = tf.add_paragraph()
        p3.text = bullet_t
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = COLOR_MUTED_TEXT

    # Arrows between timeline boxes
    for i in [1, 2]:
        x_arr = Inches(0.8) + i * (time_w + Inches(0.48)) - Inches(0.35)
        arr_box = s7.shapes.add_textbox(x_arr, Inches(2.2), Inches(0.3), Inches(0.5))
        p_a = arr_box.text_frame.paragraphs[0]
        p_a.text = "➔"
        p_a.font.size = Pt(18)
        p_a.font.bold = True
        p_a.font.color.rgb = COLOR_PRIMARY

    # Bottom Section: Experimental Design Matrix
    add_card(s7, Inches(0.8), Inches(3.6), Inches(11.75), Inches(3.2), bg_color=COLOR_WHITE)
    mat_box = s7.shapes.add_textbox(Inches(1.0), Inches(3.75), Inches(11.35), Inches(2.9))
    tf_m = mat_box.text_frame
    tf_m.word_wrap = True

    pm0 = tf_m.paragraphs[0]
    pm0.text = "3 SEASON PIPELINES × 5 CANDIDATE REGRESSION MODELS = 15 BENCHMARK EXPERIMENTS"
    pm0.font.size = Pt(12)
    pm0.font.bold = True
    pm0.font.color.rgb = COLOR_PRIMARY_DARK
    pm0.space_after = Pt(8)

    matrix_desc = (
        "• Evaluation Protocol: In strict accordance with real-world agricultural forecasting, models must predict future harvests "
        "without having seen future weather or economic shifts. Naive random 80/20 splits artificially inflate test scores by interpolating "
        "between years. Our out-of-time evaluation ensures authentic prospective testing.\n\n"
        "• 5 Evaluated Models Across Each Season:\n"
        "   1. Linear Regression (Ordinary Least Squares Baseline)\n"
        "   2. K-Nearest Neighbors Regressor (Distance-Weighted Minkowski KNN)\n"
        "   3. Gradient Boosting Regressor (Sequential Ensembling)\n"
        "   4. XGBoost Regressor (Extreme Gradient Boosting with Regularization)\n"
        "   5. Multi-Layer Perceptron (Artificial Neural Network with ReLU Activations)\n\n"
        "• Integrity Guarantee: Zero future 2013 data was accessed during feature engineering, model fitting, or hyperparameter selection."
    )
    pm_d = tf_m.add_paragraph()
    pm_d.text = matrix_desc
    pm_d.font.size = Pt(9.5)
    pm_d.font.color.rgb = COLOR_DARK_TEXT
    pm_d.line_spacing = 1.3

    add_footer(s7, "Research Methodology & Prospective Chronological Validation Protocol")
    add_notes(s7,
        "Slide 7 describes our experimental methodology and validation framework.\n\n"
        "In many machine learning projects, researchers perform a random 80/20 train-test split. "
        "In agricultural forecasting, random splitting is fatally flawed: if the model trains on year 2013 data from France "
        "and tests on year 2013 data from Germany, it is simply interpolating spatial weather patterns.\n\n"
        "To provide a realistic operational benchmark, we implemented strict Chronological Prospective Validation:\n"
        "- Years 1990 to 2012 (23 full cultivation years, 12,538 records) serve as the historical training set.\n"
        "- Year 2013 (592 records) is held out as a completely unseen future year.\n"
        "- Hyperparameter tuning was conducted strictly within the training set using 3-fold cross-validation.\n"
        "- We tested 3 season pipelines against 5 distinct model architectures, yielding 15 rigorous experiments."
    )

    # =========================================================================
    # SLIDE 8: MACHINE LEARNING MODELS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, 8, "Model Zoo", "Models Evaluated: 5 Distinct Architectural Paradigms", 
               "Selected in alignment with contemporary agricultural ML literature (El-Kenawy et al., 2025; Chen & Guestrin, 2016)")

    # 5 Visual Cards Across the Slide
    card_w = Inches(2.22)
    card_gap = Inches(0.16)
    y_c8 = Inches(1.65)
    h_c8 = Inches(3.8)

    models_info = [
        ("Linear Regression", "EMPIRICAL BASELINE", "Ordinary Least Squares (OLS)", [
            "• Closed-form analytical solution",
            "• Assumes linear relationship without interactions",
            "• Fast baseline benchmark",
            "• Explains linear component of yield trajectory"
        ], COLOR_CARD_BORDER, COLOR_DARK_TEXT),

        ("K-Nearest Neighbors", "DISTANCE-BASED", "Minkowski k-NN Regressor", [
            "• Non-parametric local regression",
            "• Inverse-distance weighting (1/d)",
            "• Captures localized agro-ecological clusters",
            "• Highly robust to multi-modal distributions"
        ], COLOR_PRIMARY, COLOR_PRIMARY_DARK),

        ("Gradient Boosting", "SEQUENTIAL ENSEMBLE", "Gradient Boosted Trees", [
            "• Greedy stagewise additive model",
            "• Shrinkage / learning rate control",
            "• Minimizes mean squared error",
            "• Handles non-linear feature interactions"
        ], COLOR_CARD_BORDER, COLOR_DARK_TEXT),

        ("XGBoost Regressor", "REGULARIZED BOOSTING", "Extreme Gradient Boosting", [
            "• 2nd-order Taylor expansion loss",
            "• L1 / L2 leaf weight regularization",
            "• Optimized tree splitting algorithms",
            "• Standard benchmark in agro-informatics"
        ], COLOR_ACCENT_BLUE, COLOR_ACCENT_BLUE),

        ("Multilayer Perceptron", "NEURAL NETWORK", "Feedforward Deep Regressor", [
            "• Dense layers (64, 32 units)",
            "• Non-linear ReLU activations",
            "• Adam optimizer with backpropagation",
            "• Evaluates deep representation learning"
        ], COLOR_CARD_BORDER, COLOR_DARK_TEXT)
    ]

    for i, (m_name, m_cat, m_full, m_bullets, border_c, title_c) in enumerate(models_info):
        x_c8 = Inches(0.8) + i * (card_w + card_gap)
        card = add_card(s8, x_c8, y_c8, card_w, h_c8, bg_color=COLOR_WHITE, border_color=border_c, line_width=1.5 if border_c!=COLOR_CARD_BORDER else 1)
        tb = s8.shapes.add_textbox(x_c8 + Inches(0.08), y_c8 + Inches(0.12), card_w - Inches(0.16), h_c8 - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = m_cat
        p1.font.size = Pt(8)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_PRIMARY if border_c==COLOR_PRIMARY else COLOR_MUTED_TEXT

        p2 = tf.add_paragraph()
        p2.text = m_name
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = title_c
        p2.space_after = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = m_full
        p3.font.size = Pt(8.5)
        p3.font.bold = True
        p3.font.color.rgb = COLOR_MUTED_TEXT
        p3.space_after = Pt(6)

        for b in m_bullets:
            pb = tf.add_paragraph()
            pb.text = b
            pb.font.size = Pt(8)
            pb.font.color.rgb = COLOR_DARK_TEXT
            pb.space_after = Pt(2)

    # Bottom Literature Alignment Banner
    lit_card = add_card(s8, Inches(0.8), Inches(5.65), Inches(11.75), Inches(1.2), bg_color=COLOR_CARD_ALT_BG)
    lit_box = s8.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(11.35), Inches(1.0))
    tf_lit = lit_box.text_frame
    tf_lit.word_wrap = True

    plit0 = tf_lit.paragraphs[0]
    plit0.text = "LITERATURE ALIGNMENT & SCIENTIFIC CITATIONS"
    plit0.font.size = Pt(10)
    plit0.font.bold = True
    plit0.font.color.rgb = COLOR_PRIMARY_DARK
    plit0.space_after = Pt(3)

    plit1 = tf_lit.add_paragraph()
    plit1.text = (
        "• Model Selection Rationale: KNN, Gradient Boosting, XGBoost, and MLP Regressors were directly selected in alignment with "
        "contemporary agricultural ML literature (El-Kenawy et al., Potato Research, 2025; van Klompenburg et al., 2020).\n"
        "• Baseline Addition: Ordinary Least Squares (OLS) Linear Regression was added as an empirical baseline to rigorously measure "
        "non-linear accuracy gains."
    )
    plit1.font.size = Pt(8.5)
    plit1.font.color.rgb = COLOR_DARK_TEXT
    plit1.line_spacing = 1.25

    add_footer(s8, "Sources: El-Kenawy et al. (Potato Research, 2025); Chen & Guestrin (KDD 2016); Pedregosa et al. (JMLR 2011)")
    add_notes(s8,
        "On Slide 8, we present the five machine learning model architectures evaluated in our benchmark.\n\n"
        "Our model zoo spans five distinct theoretical families:\n"
        "1. Linear Regression serves as our baseline to verify if simple linear correlations suffice.\n"
        "2. K-Nearest Neighbors represents non-parametric instance-based learning. As we will see, crop yield clusters strongly "
        "by agro-climatic similarity (e.g. similar rainfall, temperature, and regional practices).\n"
        "3. Gradient Boosting Regressor sequentially corrects residual errors using shallow decision trees.\n"
        "4. XGBoost builds upon gradient boosting with second-order gradients and explicit tree regularization.\n"
        "5. Multi-Layer Perceptron tests whether deep artificial neural networks can generalize agricultural patterns.\n\n"
        "Importantly, KNN, Gradient Boosting, XGBoost, and MLP were directly inspired by recent agricultural AI research "
        "such as El-Kenawy et al. (Potato Research, 2025)."
    )

    # =========================================================================
    # SLIDE 9: MODEL EVALUATION & TUNING
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, 9, "Optimization", "Model Evaluation & Hyperparameter Tuning", 
               "Systematic grid search over candidate parameter spaces evaluated via 4 complementary performance metrics")

    # Left: 4 Metrics Visual Cards
    metrics_info = [
        ("RMSE", "Root Mean Squared Error", "Penalizes large errors quadratically. Same physical unit as target (hg/ha). Primary ranking metric."),
        ("MAE", "Mean Absolute Error", "Average magnitude of absolute prediction residuals. Linear penalty, robust to extreme outliers."),
        ("R² Score", "Coefficient of Determination", "Proportion of total crop yield variance explained by model predictors (ranges 0 to 1.0)."),
        ("Pearson r", "Correlation Coefficient", "Linear agreement and directionality between predicted and actual prospective holdout yields.")
    ]
    y_m = Inches(1.65)
    h_m = Inches(1.15)
    for m_short, m_long, m_desc in metrics_info:
        card = add_card(s9, Inches(0.8), y_m, Inches(4.5), h_m, bg_color=COLOR_WHITE)
        tb = s9.shapes.add_textbox(Inches(0.95), y_m + Inches(0.08), Inches(4.2), h_m - Inches(0.16))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"{m_short} — {m_long}"
        p1.font.size = Pt(10.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_PRIMARY_DARK
        p2 = tf.add_paragraph()
        p2.text = m_desc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = COLOR_MUTED_TEXT
        y_m += Inches(1.28)

    # Right: Hyperparameter Tuning Table
    table_card = add_card(s9, Inches(5.6), Inches(1.65), Inches(6.95), Inches(5.1), bg_color=COLOR_WHITE)
    
    # Table Header & Rows
    table_shape = s9.shapes.add_table(6, 4, Inches(5.8), Inches(2.2), Inches(6.55), Inches(3.6))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(1.8)
    tbl.columns[1].width = Inches(1.6)
    tbl.columns[2].width = Inches(1.65)
    tbl.columns[3].width = Inches(1.5)

    headers = ["Model Architecture", "Tuned Parameter", "Search Space", "Optimal Config"]
    for c_idx, h_text in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    tuning_rows = [
        ("KNN Regressor", "k, weights, p", "k ∈ [3,5,7,9]\nw ∈ ['uniform','distance']\np ∈ [1, 2]", "Kharif: k=3, p=2, dist\nRabi: k=7, p=1, dist\nSeasonal: k=3, p=1, dist"),
        ("XGBoost Regressor", "n_est, lr, max_depth", "n_est ∈ [100, 150]\nlr ∈ [0.05, 0.1]\ndepth ∈ [4, 6, 7, 8]", "lr=0.05, n_est=150\nKharif: depth 7\nRabi: depth 6\nSeasonal: depth 8"),
        ("Gradient Boosting", "n_est, lr, max_depth", "n_est ∈ [100, 150]\nlr ∈ [0.05, 0.1]\ndepth ∈ [3, 4, 5]", "lr=0.05, n_est=150\nKharif: depth 4\nRabi: depth 3\nSeasonal: depth 4"),
        ("Multilayer Perceptron", "hidden_layer_sizes", "[(64, 32), (100,)]\nmax_iter=500\nrelu activation", "(64, 32) hidden units\nOptimal across all 3 pipelines"),
        ("Linear Regression", "Standard OLS", "No hyperparameter tuning\n(Ordinary Least Squares)", "Analytical baseline\nUnpenalized weights")
    ]
    for r_idx, row_vals in enumerate(tuning_rows):
        for c_idx, val in enumerate(row_vals):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 0 else COLOR_CARD_ALT_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8)
            p.font.color.rgb = COLOR_DARK_TEXT
            if c_idx == 0:
                p.font.bold = True

    # Title above table
    tb_title = s9.shapes.add_textbox(Inches(5.8), Inches(1.75), Inches(6.5), Inches(0.4))
    p_tt = tb_title.text_frame.paragraphs[0]
    p_tt.text = "HYPERPARAMETER SEARCH SPACE & VERIFIED OPTIMAL CONFIGURATIONS"
    p_tt.font.size = Pt(10)
    p_tt.font.bold = True
    p_tt.font.color.rgb = COLOR_PRIMARY_DARK

    add_footer(s9, "Hyperparameter Tuning Results from 3-Fold Time-Aware Cross-Validation")
    add_notes(s9,
        "Slide 9 outlines our evaluation criteria and hyperparameter optimization.\n\n"
        "To evaluate models comprehensively, we employ four complementary metrics:\n"
        "- RMSE reflects penalization of severe errors in physical yield units (hg/ha).\n"
        "- MAE gives average expected absolute error, less influenced by extreme harvest anomalies.\n"
        "- R-squared measures the proportion of crop yield variance explained.\n"
        "- Pearson correlation measures the linearity of predictions against ground truth.\n\n"
        "On the right, you see our verified hyperparameter grid search results:\n"
        "- For KNN, we optimized k between 3 and 9, evaluated uniform vs distance weighting, and Manhattan vs Euclidean distance. "
        "Distance weighting was universally optimal, with k=3 in Kharif, k=7 in Rabi, and k=3 in Seasonal.\n"
        "- For XGBoost and Gradient Boosting, learning rates were optimal at 0.05 with 150 trees, while tree depths ranged between 3 and 8.\n"
        "- For MLP, a dual hidden layer architecture of (64, 32) neurons provided the best stability."
    )

    # =========================================================================
    # SLIDE 10: KHARIF RESULTS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, 10, "Empirical Results", "Kharif Season Results (Monsoon Holdout: Year 2013)", 
               "Predicting monsoon-dependent coarse grains and tubers (Maize, Sorghum, Cassava) across 199 holdout test records")

    # Left: Results Table + Key Takeaway Card
    add_card(s10, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.1), bg_color=COLOR_WHITE)
    
    t_box10 = s10.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.4), Inches(0.4))
    p10 = t_box10.text_frame.paragraphs[0]
    p10.text = "KHARIF 2013 PROSPECTIVE HOLDOUT PERFORMANCE"
    p10.font.size = Pt(11)
    p10.font.bold = True
    p10.font.color.rgb = COLOR_PRIMARY_DARK

    # Table
    table_shape10 = s10.shapes.add_table(6, 4, Inches(1.0), Inches(2.2), Inches(5.4), Inches(2.3))
    t10 = table_shape10.table
    t10.columns[0].width = Inches(2.1)
    t10.columns[1].width = Inches(1.2)
    t10.columns[2].width = Inches(1.05)
    t10.columns[3].width = Inches(1.05)

    headers10 = ["Model", "RMSE (hg/ha)", "R² Score", "Pearson r"]
    for c_idx, h in enumerate(headers10):
        c = t10.cell(0, c_idx)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_PRIMARY_DARK
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    kharif_table_data = [
        ("KNN Regressor (Tuned) 🏆", "14,026.44", "0.9380", "0.9688", True),
        ("XGBoost Regressor", "17,235.88", "0.9064", "0.9533", False),
        ("Gradient Boosting", "22,679.27", "0.8379", "0.9278", False),
        ("MLP Regressor", "28,734.16", "0.7398", "0.8635", False),
        ("Linear Regression (Base)", "32,099.53", "0.6753", "0.8305", False)
    ]
    for r_idx, (m_n, rmse, r2, pr, is_champ) in enumerate(kharif_table_data):
        for c_idx, val in enumerate([m_n, rmse, r2, pr]):
            cell = t10.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_PRIMARY_LIGHT if is_champ else (COLOR_WHITE if r_idx % 2 == 0 else COLOR_CARD_ALT_BG)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.bold = is_champ
            p.font.color.rgb = COLOR_PRIMARY_DARK if is_champ else COLOR_DARK_TEXT
            if c_idx > 0:
                p.alignment = PP_ALIGN.RIGHT

    # Kharif Takeaway Card below table
    card_k_takeaway = add_card(s10, Inches(1.0), Inches(4.7), Inches(5.4), Inches(1.85), bg_color=COLOR_CARD_ALT_BG, border_color=COLOR_PRIMARY)
    tb_kt = s10.shapes.add_textbox(Inches(1.15), Inches(4.8), Inches(5.1), Inches(1.65))
    tf_kt = tb_kt.text_frame
    tf_kt.word_wrap = True

    pkt0 = tf_kt.paragraphs[0]
    pkt0.text = "EMPIRICAL FINDING & CHAMPION SELECTION"
    pkt0.font.size = Pt(10)
    pkt0.font.bold = True
    pkt0.font.color.rgb = COLOR_PRIMARY_DARK
    pkt0.space_after = Pt(3)

    pkt1 = tf_kt.add_paragraph()
    pkt1.text = (
        "• Tuned KNN (k=3, Euclidean, distance) achieved the strongest Kharif performance:\n"
        "   - Achieved R² of 0.9380 and Pearson r of 0.9688.\n"
        "   - Reduced RMSE by 56.30% compared to baseline Linear Regression (32,099.53 ➔ 14,026.44 hg/ha).\n"
        "   - Outperformed XGBoost by 3,209.44 hg/ha in RMSE.\n"
        "• Agronomic Significance: Coarse grains cluster closely by geographic soil conditions and rainfall bands."
    )
    pkt1.font.size = Pt(8.5)
    pkt1.font.color.rgb = COLOR_DARK_TEXT
    pkt1.line_spacing = 1.25

    # Right: Embedded Project Chart
    # Let's embed the Kharif comparison bar chart or tuned comparison
    img_k_chart = BASE_DIR / "figures" / "kharif_comparison_bar.png"
    add_card(s10, Inches(6.8), Inches(1.65), Inches(5.75), Inches(5.1), bg_color=COLOR_WHITE)
    if img_k_chart.exists():
        s10.shapes.add_picture(str(img_k_chart), Inches(6.9), Inches(1.9), Inches(5.55), Inches(3.8))
        
        # Caption
        cap_box = s10.shapes.add_textbox(Inches(7.0), Inches(5.8), Inches(5.35), Inches(0.8))
        tf_cap = cap_box.text_frame
        tf_cap.word_wrap = True
        p_c = tf_cap.paragraphs[0]
        p_c.text = "Figure 10A: Kharif 2013 Holdout R² Benchmark. Tuned KNN (0.9380) demonstrates superior fit over tree ensembles and neural regressors."
        p_c.font.size = Pt(8.5)
        p_c.font.italic = True
        p_c.font.color.rgb = COLOR_MUTED_TEXT

    add_footer(s10, "Source: Project evaluation results, 2013 prospective holdout (N = 199 records)")
    add_notes(s10,
        "Slide 10 presents the empirical results for our Kharif Season pipeline on the 2013 prospective holdout.\n\n"
        "Looking at the benchmark table:\n"
        "- Our tuned KNN regressor achieved the highest R² of 0.9380 and the lowest RMSE of 14,026.44 hg/ha.\n"
        "- XGBoost followed closely in second place with R² = 0.9064 and RMSE = 17,235.88 hg/ha.\n"
        "- Gradient Boosting achieved R² = 0.8379, MLP scored 0.7398, and Linear Regression lagged at 0.6753.\n\n"
        "In terms of percentage gain: Tuned KNN reduced prediction error (RMSE) by 56.30% compared to baseline Linear Regression, "
        "and by 18.6% compared to XGBoost.\n\n"
        "In viva questions regarding why KNN outperformed XGBoost here: Kharif crops (Maize, Sorghum, Cassava) exhibit "
        "strong local geographical clustering. In multi-dimensional space, farms in similar agro-climatic zones share "
        "almost identical soil management and yield ceilings, which inverse-distance KNN exploits with minimal overfitting."
    )

    # =========================================================================
    # SLIDE 11: RABI RESULTS
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, 11, "Empirical Results", "Rabi Season Results (Winter Holdout: Year 2013)", 
               "Predicting winter-cultivated, temperate Wheat across 81 prospective holdout test records")

    # Left: Results Table + Key Takeaway Card
    add_card(s11, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.1), bg_color=COLOR_WHITE)
    
    t_box11 = s11.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.4), Inches(0.4))
    p11 = t_box11.text_frame.paragraphs[0]
    p11.text = "RABI 2013 PROSPECTIVE HOLDOUT PERFORMANCE"
    p11.font.size = Pt(11)
    p11.font.bold = True
    p11.font.color.rgb = COLOR_PRIMARY_DARK

    table_shape11 = s11.shapes.add_table(6, 4, Inches(1.0), Inches(2.2), Inches(5.4), Inches(2.3))
    t11 = table_shape11.table
    t11.columns[0].width = Inches(2.1)
    t11.columns[1].width = Inches(1.2)
    t11.columns[2].width = Inches(1.05)
    t11.columns[3].width = Inches(1.05)

    headers11 = ["Model", "RMSE (hg/ha)", "R² Score", "Pearson r"]
    for c_idx, h in enumerate(headers11):
        c = t11.cell(0, c_idx)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_PRIMARY_DARK
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    rabi_table_data = [
        ("KNN Regressor (Tuned) 🏆", "4,065.82", "0.9636", "0.9868", True),
        ("XGBoost Regressor", "5,649.94", "0.9297", "0.9678", False),
        ("Linear Regression (Base)", "6,182.82", "0.9158", "0.9592", False),
        ("Gradient Boosting", "8,621.76", "0.8362", "0.9333", False),
        ("MLP Regressor", "13,787.41", "0.5812", "0.7987", False)
    ]
    for r_idx, (m_n, rmse, r2, pr, is_champ) in enumerate(rabi_table_data):
        for c_idx, val in enumerate([m_n, rmse, r2, pr]):
            cell = t11.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_PRIMARY_LIGHT if is_champ else (COLOR_WHITE if r_idx % 2 == 0 else COLOR_CARD_ALT_BG)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.bold = is_champ
            p.font.color.rgb = COLOR_PRIMARY_DARK if is_champ else COLOR_DARK_TEXT
            if c_idx > 0:
                p.alignment = PP_ALIGN.RIGHT

    # Rabi Takeaway Card below table
    card_r_takeaway = add_card(s11, Inches(1.0), Inches(4.7), Inches(5.4), Inches(1.85), bg_color=COLOR_CARD_ALT_BG, border_color=COLOR_PRIMARY)
    tb_rt = s11.shapes.add_textbox(Inches(1.15), Inches(4.8), Inches(5.1), Inches(1.65))
    tf_rt = tb_rt.text_frame
    tf_rt.word_wrap = True

    prt0 = tf_rt.paragraphs[0]
    prt0.text = "EMPIRICAL FINDING & MONOCULTURE DYNAMICS"
    prt0.font.size = Pt(10)
    prt0.font.bold = True
    prt0.font.color.rgb = COLOR_PRIMARY_DARK
    prt0.space_after = Pt(3)

    prt1 = tf_rt.add_paragraph()
    prt1.text = (
        "• Tuned KNN (k=7, Manhattan, distance) achieved outstanding accuracy in Rabi:\n"
        "   - Delivered R² of 0.9636 and an exceptional Pearson r of 0.9868.\n"
        "   - Achieved lowest absolute error across the entire project: RMSE 4,065.82 hg/ha.\n"
        "• Note on Linear Regression: Linear baseline was unusually competitive (R² = 0.9158), because Rabi is a single-crop "
        "(Wheat) regime where yield scales strongly with technology year and controlled irrigation."
    )
    prt1.font.size = Pt(8.5)
    prt1.font.color.rgb = COLOR_DARK_TEXT
    prt1.line_spacing = 1.25

    # Right: Embedded Project Chart
    img_r_chart = BASE_DIR / "figures" / "rabi_comparison_bar.png"
    add_card(s11, Inches(6.8), Inches(1.65), Inches(5.75), Inches(5.1), bg_color=COLOR_WHITE)
    if img_r_chart.exists():
        s11.shapes.add_picture(str(img_r_chart), Inches(6.9), Inches(1.9), Inches(5.55), Inches(3.8))
        
        cap_box11 = s11.shapes.add_textbox(Inches(7.0), Inches(5.8), Inches(5.35), Inches(0.8))
        tf_c11 = cap_box11.text_frame
        tf_c11.word_wrap = True
        p_c11 = tf_c11.paragraphs[0]
        p_c11.text = "Figure 11A: Rabi 2013 Holdout R² Benchmark. Tuned KNN (0.9636) and XGBoost (0.9297) lead performance, followed by Linear Regression."
        p_c11.font.size = Pt(8.5)
        p_c11.font.italic = True
        p_c11.font.color.rgb = COLOR_MUTED_TEXT

    add_footer(s11, "Source: Project evaluation results, 2013 prospective holdout (N = 81 records)")
    add_notes(s11,
        "Slide 11 examines the Rabi season holdout results.\n\n"
        "In the Rabi dataset, our models are predicting winter wheat yields. Notice two fascinating findings:\n"
        "First, tuned KNN achieved an outstanding R² of 0.9636 with a Pearson correlation of 0.9868 and an RMSE of only 4,065 hg/ha. "
        "This is the lowest absolute prediction error of any pipeline in our study.\n\n"
        "Second, look at Linear Regression: it scored 0.9158, outperforming both Gradient Boosting and MLP! "
        "Examiners will likely ask: 'Why did Linear Regression perform so well in Rabi?'\n"
        "The agronomic answer is straightforward: Rabi is 100% Wheat. Unlike multi-crop datasets that introduce categorical non-linearities, "
        "wheat productivity across countries scales almost linearly with time (Year), fertilizer/pesticide intensity, and irrigation.\n\n"
        "However, KNN still achieved a 34.24% reduction in RMSE over Linear Regression by capturing subtle non-linear climate thresholds."
    )

    # =========================================================================
    # SLIDE 12: SEASONAL RESULTS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, 12, "Empirical Results", "Seasonal Results (Whole-Year Holdout: Year 2013)", 
               "Predicting multi-cycle & perennial staples (Potatoes, Rice, Soybeans, Sweet potatoes) across 312 holdout records")

    # Left: Results Table + Key Takeaway Card
    add_card(s12, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.1), bg_color=COLOR_WHITE)
    
    t_box12 = s12.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.4), Inches(0.4))
    p12 = t_box12.text_frame.paragraphs[0]
    p12.text = "SEASONAL 2013 PROSPECTIVE HOLDOUT PERFORMANCE"
    p12.font.size = Pt(11)
    p12.font.bold = True
    p12.font.color.rgb = COLOR_PRIMARY_DARK

    table_shape12 = s12.shapes.add_table(6, 4, Inches(1.0), Inches(2.2), Inches(5.4), Inches(2.3))
    t12 = table_shape12.table
    t12.columns[0].width = Inches(2.1)
    t12.columns[1].width = Inches(1.2)
    t12.columns[2].width = Inches(1.05)
    t12.columns[3].width = Inches(1.05)

    headers12 = ["Model", "RMSE (hg/ha)", "R² Score", "Pearson r"]
    for c_idx, h in enumerate(headers12):
        c = t12.cell(0, c_idx)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_PRIMARY_DARK
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    seasonal_table_data = [
        ("KNN Regressor (Tuned) 🏆", "19,646.94", "0.9642", "0.9827", True),
        ("XGBoost Regressor", "25,933.82", "0.9377", "0.9698", False),
        ("Gradient Boosting", "44,947.15", "0.8127", "0.9149", False),
        ("MLP Regressor", "48,214.55", "0.7845", "0.8870", False),
        ("Linear Regression (Base)", "52,357.50", "0.7459", "0.8674", False)
    ]
    for r_idx, (m_n, rmse, r2, pr, is_champ) in enumerate(seasonal_table_data):
        for c_idx, val in enumerate([m_n, rmse, r2, pr]):
            cell = t12.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_PRIMARY_LIGHT if is_champ else (COLOR_WHITE if r_idx % 2 == 0 else COLOR_CARD_ALT_BG)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.bold = is_champ
            p.font.color.rgb = COLOR_PRIMARY_DARK if is_champ else COLOR_DARK_TEXT
            if c_idx > 0:
                p.alignment = PP_ALIGN.RIGHT

    # Seasonal Takeaway Card below table
    card_s_takeaway = add_card(s12, Inches(1.0), Inches(4.7), Inches(5.4), Inches(1.85), bg_color=COLOR_CARD_ALT_BG, border_color=COLOR_PRIMARY)
    tb_st = s12.shapes.add_textbox(Inches(1.15), Inches(4.8), Inches(5.1), Inches(1.65))
    tf_st = tb_st.text_frame
    tf_st.word_wrap = True

    pst0 = tf_st.paragraphs[0]
    pst0.text = "EMPIRICAL FINDING & MULTI-CROP ROBUSTNESS"
    pst0.font.size = Pt(10)
    pst0.font.bold = True
    pst0.font.color.rgb = COLOR_PRIMARY_DARK
    pst0.space_after = Pt(3)

    pst1 = tf_st.add_paragraph()
    pst1.text = (
        "• Tuned KNN (k=3, Manhattan, distance) dominated the highly diverse Seasonal pipeline:\n"
        "   - Achieved highest R² of the entire study: 0.9642 (Pearson r = 0.9827).\n"
        "   - Slashed RMSE by 62.48% vs Linear Regression (52,357.50 ➔ 19,646.94 hg/ha).\n"
        "   - Outperformed XGBoost by 6,286.88 hg/ha in RMSE.\n"
        "• Robustness: Accurately models extreme potato yields (~300,000 hg/ha) alongside lower-yield soybean and rice records."
    )
    pst1.font.size = Pt(8.5)
    pst1.font.color.rgb = COLOR_DARK_TEXT
    pst1.line_spacing = 1.25

    # Right: Embedded Project Chart
    img_s_chart = BASE_DIR / "figures" / "seasonal_comparison_bar.png"
    add_card(s12, Inches(6.8), Inches(1.65), Inches(5.75), Inches(5.1), bg_color=COLOR_WHITE)
    if img_s_chart.exists():
        s12.shapes.add_picture(str(img_s_chart), Inches(6.9), Inches(1.9), Inches(5.55), Inches(3.8))
        
        cap_box12 = s12.shapes.add_textbox(Inches(7.0), Inches(5.8), Inches(5.35), Inches(0.8))
        tf_c12 = cap_box12.text_frame
        tf_c12.word_wrap = True
        p_c12 = tf_c12.paragraphs[0]
        p_c12.text = "Figure 12A: Seasonal 2013 Holdout R² Benchmark. Tuned KNN (0.9642) delivers highest explanatory power across multi-crop rotations."
        p_c12.font.size = Pt(8.5)
        p_c12.font.italic = True
        p_c12.font.color.rgb = COLOR_MUTED_TEXT

    add_footer(s12, "Source: Project evaluation results, 2013 prospective holdout (N = 312 records)")
    add_notes(s12,
        "Slide 12 covers the Seasonal / Whole-Year pipeline results.\n\n"
        "This dataset is the largest (6,916 records total; 312 in the 2013 holdout) and the most complex, "
        "because it combines tuber crops like potatoes that reach 300,000 hg/ha with cereal crops like rice and grain legumes like soybeans.\n\n"
        "Here, tuned KNN achieved our study's peak R² score: 0.9642, with a Pearson r of 0.9827.\n"
        "Look at the dramatic error reduction: baseline Linear Regression had an RMSE of 52,357 hg/ha. "
        "KNN reduced this to 19,646 hg/ha—a massive 62.48% error reduction.\n\n"
        "XGBoost also performed commendably with R² = 0.9377, but distance-weighted KNN maintained an edge of over 6,000 hg/ha in RMSE."
    )

    # =========================================================================
    # SLIDE 13: CROSS-SEASON FINAL MODEL
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, 13, "Cross-Season Synthesis", "Final Model Selection Across Seasons", 
               "Comprehensive comparison establishing tuned distance-weighted KNN as the deployment champion across all 3 regimes")

    # Embed Figure 10: Dual chart of R² & RMSE
    img_fig10 = BASE_DIR / "figures" / "10_final_model_performance.png"
    add_card(s13, Inches(0.8), Inches(1.65), Inches(7.5), Inches(5.1), bg_color=COLOR_WHITE)
    if img_fig10.exists():
        s13.shapes.add_picture(str(img_fig10), Inches(0.9), Inches(1.85), Inches(7.3), Inches(3.9))
        
        cap13 = s13.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(7.1), Inches(0.7))
        tf_c13 = cap13.text_frame
        tf_c13.word_wrap = True
        p13 = tf_c13.paragraphs[0]
        p13.text = "Figure 13: Multi-Season Champion Model Validation on 2013 Holdout. (a) R² & Pearson r coefficients; (b) Absolute RMSE & MAE errors."
        p13.font.size = Pt(8.5)
        p13.font.italic = True
        p13.font.color.rgb = COLOR_MUTED_TEXT

    # Right: Summary Cards & Rationale
    add_card(s13, Inches(8.5), Inches(1.65), Inches(4.05), Inches(5.1), bg_color=COLOR_WHITE)
    rt_box = s13.shapes.add_textbox(Inches(8.65), Inches(1.8), Inches(3.75), Inches(4.8))
    tf_rt = rt_box.text_frame
    tf_rt.word_wrap = True

    prt0 = tf_rt.paragraphs[0]
    prt0.text = "CHAMPION KNN CONFIGURATIONS"
    prt0.font.size = Pt(11)
    prt0.font.bold = True
    prt0.font.color.rgb = COLOR_PRIMARY_DARK
    prt0.space_after = Pt(6)

    champ_metrics = [
        ("Kharif Champion", "k=3, p=2 (Euclidean), Distance", "• Test R² = 0.9380 | r = 0.9688\n• RMSE: 14,026.44 hg/ha\n• 56.3% error cut vs Linear"),
        ("Rabi Champion", "k=7, p=1 (Manhattan), Distance", "• Test R² = 0.9636 | r = 0.9868\n• RMSE: 4,065.82 hg/ha\n• 34.2% error cut vs Linear"),
        ("Seasonal Champion", "k=3, p=1 (Manhattan), Distance", "• Test R² = 0.9642 | r = 0.9827\n• RMSE: 19,646.94 hg/ha\n• 62.5% error cut vs Linear")
    ]
    for ch_title, ch_param, ch_b in champ_metrics:
        p_ct = tf_rt.add_paragraph()
        p_ct.text = ch_title
        p_ct.font.size = Pt(10)
        p_ct.font.bold = True
        p_ct.font.color.rgb = COLOR_DARK_TEXT
        p_cp = tf_rt.add_paragraph()
        p_cp.text = ch_param
        p_cp.font.size = Pt(8.5)
        p_cp.font.bold = True
        p_cp.font.color.rgb = COLOR_PRIMARY
        p_cb = tf_rt.add_paragraph()
        p_cb.text = ch_b
        p_cb.font.size = Pt(8)
        p_cb.font.color.rgb = COLOR_MUTED_TEXT
        p_cb.space_after = Pt(4)

    p_rat = tf_rt.add_paragraph()
    p_rat.text = "🏆 SELECTION VERDICT"
    p_rat.font.size = Pt(10)
    p_rat.font.bold = True
    p_rat.font.color.rgb = COLOR_PRIMARY_DARK
    p_rat.space_before = Pt(4)

    p_rd = tf_rt.add_paragraph()
    p_rd.text = "Distance-weighted KNN consistently outperformed all tree ensembles and neural regressors across all 3 agricultural regimes (Cross-season Mean R² = 0.9553), making it the definitive production champion."
    p_rd.font.size = Pt(8)
    p_rd.font.color.rgb = COLOR_DARK_TEXT

    add_footer(s13, "Cross-Season Synthesis & Champion Model Justification (Prospective 2013 Holdout)")
    add_notes(s13,
        "Slide 13 synthesizes our findings across all three agricultural seasons.\n\n"
        "On the left, Figure 13 displays our dual validation charts:\n"
        "- Chart (a) shows explanatory power and correlation: R² is 0.9380 for Kharif, 0.9636 for Rabi, and 0.9642 for Seasonal, "
        "with Pearson correlations consistently above 0.968.\n"
        "- Chart (b) shows the absolute prediction errors: Rabi errors are exceptionally low (4,065 hg/ha), "
        "while Seasonal errors are higher (19,646 hg/ha) due to huge baseline potato yields.\n\n"
        "Across the board, tuned distance-weighted KNN achieved an average cross-season R² of 0.9553 and an average error "
        "reduction of 50.98% compared to the linear baseline.\n\n"
        "Therefore, we selected tuned KNN as our production model across all three seasonal deployment pipelines."
    )

    # =========================================================================
    # SLIDE 14: SYSTEM IMPLEMENTATION / WEB APPLICATION
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, 14, "Full-Stack Deployment", "From ML Model to Working Web Application", 
               "Production-grade FastAPI ASGI application with JWT auth, SQLite persistence, and responsive AgriYield dashboard")

    # Left: Architecture Flow & Diagram
    add_card(s14, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.1), bg_color=COLOR_WHITE)
    img_arch = FIG_DIR / "11_system_architecture_diagram.png"
    if img_arch.exists():
        s14.shapes.add_picture(str(img_arch), Inches(0.9), Inches(1.75), Inches(5.6), Inches(3.1))

    # Architecture flow bullets below diagram
    arch_box = s14.shapes.add_textbox(Inches(1.0), Inches(5.0), Inches(5.4), Inches(1.6))
    tf_ab = arch_box.text_frame
    tf_ab.word_wrap = True
    pab0 = tf_ab.paragraphs[0]
    pab0.text = "END-TO-END DATAFLOW ARCHITECTURE"
    pab0.font.size = Pt(10)
    pab0.font.bold = True
    pab0.font.color.rgb = COLOR_PRIMARY_DARK
    pab0.space_after = Pt(2)

    flow_txt = (
        "USER ➔ LOGIN / JWT TOKEN ➔ CLIENT FRONTEND (HTML5/CSS3/Vanilla JS) ➔\n"
        "FASTAPI REST GATEWAY ➔ DYNAMIC SEASON ROUTER ➔\n"
        "SERIALIZED JOBLIB KNN PIPELINE ➔ PREDICTED YIELD + GAUGE ➔ SQLITE AUDIT LOG"
    )
    pab1 = tf_ab.add_paragraph()
    pab1.text = flow_txt
    pab1.font.size = Pt(8.5)
    pab1.font.bold = True
    pab1.font.color.rgb = COLOR_ACCENT_BLUE

    # Right: Actual UI Dashboard Screenshot
    add_card(s14, Inches(6.8), Inches(1.65), Inches(5.75), Inches(5.1), bg_color=COLOR_WHITE)
    img_ui = FIG_DIR / "ui_dashboard.png"
    if img_ui.exists():
        s14.shapes.add_picture(str(img_ui), Inches(6.9), Inches(1.75), Inches(5.55), Inches(3.4))

    # UI features description below screenshot
    ui_box = s14.shapes.add_textbox(Inches(7.0), Inches(5.25), Inches(5.35), Inches(1.4))
    tf_ui = ui_box.text_frame
    tf_ui.word_wrap = True
    pui0 = tf_ui.paragraphs[0]
    pui0.text = "AGRIYIELD DASHBOARD CAPABILITIES"
    pui0.font.size = Pt(10)
    pui0.font.bold = True
    pui0.font.color.rgb = COLOR_PRIMARY_DARK
    pui0.space_after = Pt(2)

    ui_bullets = (
        "• Login-First Security: Secure JWT bearer tokens & PBKDF2 password hashing.\n"
        "• Cascading Dropdowns: Season ➔ Continent ➔ Country ➔ Crop (live API filtered).\n"
        "• Visual Yield Output: Large metric badge, 0–100 agricultural potential gauge, factors impact.\n"
        "• Persistence & Analytics: User query history log + dynamic Chart.js visualizations."
    )
    pui1 = tf_ui.add_paragraph()
    pui1.text = ui_bullets
    pui1.font.size = Pt(8.5)
    pui1.font.color.rgb = COLOR_DARK_TEXT
    pui1.line_spacing = 1.2

    add_footer(s14, "AgriYield Full-Stack Application Architecture & Actual UI Implementation")
    add_notes(s14,
        "Slide 14 showcases our operational software deployment.\n\n"
        "A machine learning model is only valuable if agronomists, farmers, and policy planners can easily interact with it. "
        "We engineered a full-stack, enterprise-grade web application named 'AgriYield'.\n\n"
        "On the left, you see the deployment architecture:\n"
        "- The frontend communicates via authenticated REST requests with a FastAPI backend server running on Uvicorn.\n"
        "- Passwords are encrypted using industry-standard PBKDF2 hashing, and sessions use secure JWT Bearer tokens.\n"
        "- When the user requests a prediction, FastAPI inspects the selected season, routes to the corresponding "
        "serialized KNN pipeline (loaded in memory via Joblib), executes the inference in under 15 milliseconds, "
        "and logs the prediction to an SQLite database via SQLAlchemy ORM.\n\n"
        "On the right is an actual screenshot of our working application: notice the cascading filters (Season -> Continent -> Country -> Crop), "
        "the predicted yield badge (3,250 hg/ha), and the circular agricultural potential gauge."
    )

    # =========================================================================
    # SLIDE 15: CONCLUSION, REFERENCES & FUTURE WORK
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, 15, "Conclusions & Outlook", "Conclusion, Key References & Future Directions", 
               "Summary of research contributions, formal bibliographic citations, and future expansion roadmap")

    # Left: Conclusion (Top half)
    add_card(s15, Inches(0.8), Inches(1.65), Inches(5.7), Inches(2.7), bg_color=COLOR_WHITE)
    c_box15 = s15.shapes.add_textbox(Inches(0.95), Inches(1.75), Inches(5.4), Inches(2.45))
    tf_c = c_box15.text_frame
    tf_c.word_wrap = True

    pc0 = tf_c.paragraphs[0]
    pc0.text = "RESEARCH CONCLUSIONS"
    pc0.font.size = Pt(11)
    pc0.font.bold = True
    pc0.font.color.rgb = COLOR_PRIMARY_DARK
    pc0.space_after = Pt(4)

    conclusions = [
        "1. Seasonal Stratification: Splitting global agriculture into Kharif, Rabi, and Seasonal pipelines prevented feature dilution and improved fidelity.",
        "2. Empirical Dominance of KNN: Distance-weighted Minkowski KNN achieved highest accuracy across all 3 regimes (Holdout R²: 0.9380 to 0.9642).",
        "3. Leakage-Free Validity: Chronological 2013 holdout proved models maintain robust generalization to unseen future cultivation cycles.",
        "4. Operational Deployment: Serialized pipelines were successfully embedded into a secure, responsive FastAPI web portal."
    ]
    for c in conclusions:
        p = tf_c.add_paragraph()
        p.text = f"• {c}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_after = Pt(3)

    # Right: Future Work (Top half)
    add_card(s15, Inches(6.8), Inches(1.65), Inches(5.75), Inches(2.7), bg_color=COLOR_WHITE)
    fw_box15 = s15.shapes.add_textbox(Inches(6.95), Inches(1.75), Inches(5.45), Inches(2.45))
    tf_fw = fw_box15.text_frame
    tf_fw.word_wrap = True

    pfw0 = tf_fw.paragraphs[0]
    pfw0.text = "FUTURE RESEARCH DIRECTIONS"
    pfw0.font.size = Pt(11)
    pfw0.font.bold = True
    pfw0.font.color.rgb = COLOR_PRIMARY_DARK
    pfw0.space_after = Pt(4)

    future_work = [
        "1. Multi-Year Rolling Validation: Evaluate 3-to-5 year rolling test windows across climate shocks.",
        "2. Remote Sensing & Soil Ingestion: Integrate satellite NDVI, EVI, and soil nutrient indices.",
        "3. Real-Time Meteorological Feeds: Connect live ECMWF / NOAA API weather streams.",
        "4. SHAP Explainability: Implement Shapley Additive exPlanations for localized agronomic feature attribution (following Gupta et al., 2026).",
        "5. Uncertainty Quantification: Implement conformal prediction intervals for risk assessment."
    ]
    for fw in future_work:
        p = tf_fw.add_paragraph()
        p.text = f"• {fw}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_after = Pt(3)

    # Bottom: 5 Key Academic References (Exact Bibliographic Citations)
    add_card(s15, Inches(0.8), Inches(4.5), Inches(11.75), Inches(2.35), bg_color=COLOR_CARD_ALT_BG)
    ref_box15 = s15.shapes.add_textbox(Inches(0.95), Inches(4.6), Inches(11.45), Inches(2.15))
    tf_ref = ref_box15.text_frame
    tf_ref.word_wrap = True

    pref0 = tf_ref.paragraphs[0]
    pref0.text = "KEY ACADEMIC BIBLIOGRAPHY & REFERENCES (CITED IN RESEARCH PAPER)"
    pref0.font.size = Pt(10)
    pref0.font.bold = True
    pref0.font.color.rgb = COLOR_PRIMARY_DARK
    pref0.space_after = Pt(4)

    references = [
        "[1] El-Kenawy, E.-S. M., Alhussan, A. A., Khodadadi, N., Mirjalili, S., & Eid, M. M. (2025). Predicting Potato Crop Yield with Machine Learning and Deep Learning for Sustainable Agriculture. Potato Research, 68(2), 759–792. https://doi.org/10.1007/s11540-024-09753-w",
        "[2] Gupta, R., Jha, S. K., Kumar, P., & Yadav, M. (2026). Explainable ensemble machine learning algorithms for predicting wind speed by incorporating Shapley additive explanations. Franklin Open, 10, 100781. https://doi.org/10.1016/j.fraope.2026.100781",
        "[3] van Klompenburg, T., Kassahun, A., & Catal, C. (2020). Crop yield prediction using machine learning: A systematic literature review. Computers and Electronics in Agriculture, 177, 105709. https://doi.org/10.1016/j.compag.2020.105709",
        "[4] Paudel, D., Boogaard, H., de Wit, A., Janssen, S., Osinga, S., Pylianidis, C., & Athanasiadis, I. N. (2021). Machine learning for large-scale crop yield forecasting. Agricultural Systems, 187, 103016. https://doi.org/10.1016/j.agsy.2020.103016",
        "[5] Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. In Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (pp. 785–794). https://doi.org/10.1145/2939672.2939785"
    ]
    for ref in references:
        p = tf_ref.add_paragraph()
        p.text = ref
        p.font.size = Pt(7.5)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_after = Pt(2)

    add_footer(s15, "Final-Year B.Tech Capstone Presentation | Department of Computer Science & Engineering, SRMIST")
    add_notes(s15,
        "Concluding our presentation on Slide 15:\n\n"
        "To summarize our core scientific contributions:\n"
        "1. We demonstrated that seasonal stratification into Kharif, Rabi, and Seasonal pipelines significantly outperforms monolithic modeling.\n"
        "2. Through rigorous out-of-time chronological evaluation on the 2013 prospective holdout, tuned distance-weighted KNN "
        "consistently achieved superior accuracy across all three pipelines, reaching R² scores from 0.9380 to 0.9642.\n"
        "3. We delivered a complete, working software artifact: our AgriYield FastAPI and interactive web application.\n\n"
        "For future work, we plan to incorporate multi-year rolling validation, satellite remote-sensing indices (like NDVI and soil moisture), "
        "and SHAP-based feature attribution following the explainability methodology of Rahul Gupta et al. (2026).\n\n"
        "At the bottom are our key literature citations, exactly matching our final research paper bibliography.\n\n"
        "Thank you for your time and attention. We are now eager and ready to answer your questions!"
    )

    # Save presentation
    prs.save(OUTPUT_PPTX)
    print(f"Presentation successfully created at: {OUTPUT_PPTX}")
    return OUTPUT_PPTX

if __name__ == "__main__":
    create_deck()
