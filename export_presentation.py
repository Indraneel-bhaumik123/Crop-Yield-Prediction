import os
import sys
import shutil
from pathlib import Path
import win32com.client

BASE_DIR = Path(r"c:\Users\indra\OneDrive\Desktop\Seasonal Crop Yield Prediction\Seasonal_Crop_Yield_Prediction_Rebuilt")
ROOT_DIR = Path(r"c:\Users\indra\OneDrive\Desktop\Seasonal Crop Yield Prediction")

pptx_path = BASE_DIR / "FINAL_15_SLIDE_PROJECT_PRESENTATION.pptx"
pdf_path = BASE_DIR / "FINAL_15_SLIDE_PROJECT_PRESENTATION.pdf"
preview_dir = BASE_DIR / "presentation_previews"
preview_dir.mkdir(parents=True, exist_ok=True)

print(f"Opening {pptx_path} via PowerPoint COM...")
ppt_app = win32com.client.Dispatch("PowerPoint.Application")
presentation = ppt_app.Presentations.Open(str(pptx_path), WithWindow=False)

# Export to PDF (ppSaveAsPDF = 32)
print(f"Exporting to PDF: {pdf_path}...")
presentation.SaveAs(str(pdf_path), 32)
print(f"PDF export successful! Size: {pdf_path.stat().st_size} bytes")

# Export slide PNG previews
print(f"Exporting slide PNG previews to {preview_dir}...")
for i in range(1, presentation.Slides.Count + 1):
    slide = presentation.Slides(i)
    slide_img_path = preview_dir / f"slide_{i:02d}.png"
    slide.Export(str(slide_img_path), "PNG", 1920, 1080)
    print(f"Saved slide {i:02d} -> {slide_img_path.name}")

presentation.Close()
ppt_app.Quit()

# Also copy to root folder for convenient user access
root_pptx = ROOT_DIR / "FINAL_15_SLIDE_PROJECT_PRESENTATION.pptx"
root_pdf = ROOT_DIR / "FINAL_15_SLIDE_PROJECT_PRESENTATION.pdf"
shutil.copy2(pptx_path, root_pptx)
shutil.copy2(pdf_path, root_pdf)
print(f"Copied PPTX and PDF to root directory: {ROOT_DIR}")

print("All exports completed successfully!")
