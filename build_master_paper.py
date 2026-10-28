"""
build_master_paper.py
Master compiler script that stitches together all paper sections,
generates FINAL_RESEARCH_PAPER_REVISED.docx, and exports to PDF.
"""

import os
import sys
import docx
import win32com.client
from paper_common import format_p
from paper_section_1 import build_section_1
from paper_section_2 import build_section_2
from paper_section_3_4 import build_section_3_4
from paper_section_5_6 import build_section_5_6
from paper_section_7 import build_section_7
from paper_section_8_9 import build_section_8_9
from paper_section_10_12_app import build_section_10_12_app

def build_complete_paper():
    print("Initializing Document Generation...")
    doc = docx.Document()
    
    print("Building Section 1: Title, Abstract, Keywords, and Introduction...")
    build_section_1(doc)
    
    print("Building Section 2: Related Work and Research Gap...")
    build_section_2(doc)
    
    print("Building Section 3: Data Description & Section 4: Methodology...")
    build_section_3_4(doc)
    
    print("Building Section 5: Exploratory Data Analysis & Section 6: Experimental Design...")
    build_section_5_6(doc)
    
    print("Building Section 7: Results and Experimental Evaluation (Advanced Analyses)...")
    build_section_7(doc)
    
    print("Building Section 8: Discussion & Section 9: System Implementation and Deployment...")
    build_section_8_9(doc)
    
    print("Building Section 10: Reliability/Limitations, Section 11: Future Work, Section 12: Conclusion, References, and Appendices...")
    build_section_10_12_app(doc)
    
    output_docx = "FINAL_RESEARCH_PAPER_REVISED.docx"
    output_pdf = "FINAL_RESEARCH_PAPER_REVISED.pdf"
    
    doc.save(output_docx)
    print(f"Successfully saved {output_docx} (File size: {os.path.getsize(output_docx):,} bytes)")
    
    # Export to PDF via Word COM
    print("Converting to PDF via Word COM...")
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        abs_docx = os.path.abspath(output_docx)
        abs_pdf = os.path.abspath(output_pdf)
        
        w_doc = word.Documents.Open(abs_docx)
        page_count = w_doc.ComputeStatistics(2) # 2 = wdStatisticPages
        print(f"Computed Document Page Count: {page_count} pages")
        
        w_doc.SaveAs(abs_pdf, FileFormat=17) # 17 = wdFormatPDF
        w_doc.Close()
        word.Quit()
        print(f"Successfully exported {output_pdf} ({page_count} pages, {os.path.getsize(output_pdf):,} bytes)!")
    except Exception as e:
        print(f"PDF Conversion encountered error: {e}")

if __name__ == "__main__":
    build_complete_paper()
