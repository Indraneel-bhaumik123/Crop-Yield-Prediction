with open('generate_faculty_docx.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update add_figure_above_caption so caption is placed BELOW the figure image
old_fig_fn = '''def add_figure_above_caption(doc, img_rel_path, fig_num, fig_title, fig_desc="", width=4.8):
    full_path = os.path.join(PROJECT_DIR, img_rel_path)
    if not os.path.exists(full_path):
        full_path = os.path.join(BASE_DIR, img_rel_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Missing required figure file: {full_path}")
        
    p_cap = doc.add_paragraph()
    format_p(p_cap, before=5, after=2, align=WD_ALIGN_PARAGRAPH.LEFT)
    add_bookmark(p_cap, f"fig_{fig_num}")
    
    r_lbl = p_cap.add_run(f"Figure {fig_num}. ")
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(9.5)
    r_lbl.font.bold = True
    r_lbl.font.color.rgb = RGBColor(15, 23, 42)
    
    r_title = p_cap.add_run(fig_title)
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(9.5)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(30, 41, 59)
    
    if fig_desc:
        r_col = p_cap.add_run(": ")
        r_col.font.name = "Times New Roman"
        r_col.font.size = Pt(9.5)
        r_col.font.bold = True
        
        r_desc = p_cap.add_run(fig_desc)
        r_desc.font.name = "Times New Roman"
        r_desc.font.size = Pt(9.5)
        r_desc.font.italic = True
        r_desc.font.color.rgb = RGBColor(71, 85, 105)
        
    p_img = doc.add_paragraph()
    format_p(p_img, before=2, after=3, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_img.add_run().add_picture(full_path, width=Inches(width))
    return p_img'''

new_fig_fn = '''def add_figure_above_caption(doc, img_rel_path, fig_num, fig_title, fig_desc="", width=4.8):
    full_path = os.path.join(PROJECT_DIR, img_rel_path)
    if not os.path.exists(full_path):
        full_path = os.path.join(BASE_DIR, img_rel_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Missing required figure file: {full_path}")
        
    # 1. Image paragraph FIRST
    p_img = doc.add_paragraph()
    format_p(p_img, before=4, after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    p_img.paragraph_format.keep_with_next = True  # Glues image to its caption below
    p_img.add_run().add_picture(full_path, width=Inches(width))
    
    # 2. Caption paragraph BELOW IMAGE
    p_cap = doc.add_paragraph()
    format_p(p_cap, before=2, after=5, align=WD_ALIGN_PARAGRAPH.LEFT)
    add_bookmark(p_cap, f"fig_{fig_num}")
    
    r_lbl = p_cap.add_run(f"Figure {fig_num}. ")
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(9.5)
    r_lbl.font.bold = True
    r_lbl.font.color.rgb = RGBColor(15, 23, 42)
    
    r_title = p_cap.add_run(fig_title)
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(9.5)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(30, 41, 59)
    
    if fig_desc:
        r_col = p_cap.add_run(": ")
        r_col.font.name = "Times New Roman"
        r_col.font.size = Pt(9.5)
        r_col.font.bold = True
        
        r_desc = p_cap.add_run(fig_desc)
        r_desc.font.name = "Times New Roman"
        r_desc.font.size = Pt(9.5)
        r_desc.font.italic = True
        r_desc.font.color.rgb = RGBColor(71, 85, 105)
        
    return p_img'''

assert old_fig_fn in code, "Could not find old_fig_fn in generate_faculty_docx.py"
code = code.replace(old_fig_fn, new_fig_fn)

# 2. Do not touch or overwrite the report file (checklist files)
# Find where checklist generation starts and bypass it
checklist_start = 'print("Generating Faculty Red Marks Resolution Checklist...")'
idx = code.find(checklist_start)
if idx != -1:
    code = code[:idx] + '# User instruction: do not change anything in the report file\nprint("Skipping checklist regeneration as requested: report file left untouched.")\n'

with open('generate_faculty_docx.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated generate_faculty_docx.py: figure captions are now placed BELOW the figures, and report file generation is bypassed.")
