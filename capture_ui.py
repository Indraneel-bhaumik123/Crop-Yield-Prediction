import subprocess
import os

html_path = r"c:\Users\indra\OneDrive\Desktop\Seasonal Crop Yield Prediction\Seasonal_Crop_Yield_Prediction_Rebuilt\Frontend\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace auth overlay to be hidden by default
content_mod = content.replace('class="auth-overlay"', 'class="auth-overlay hidden" style="display:none !important;"')
temp_html = r"c:\Users\indra\OneDrive\Desktop\Seasonal Crop Yield Prediction\Seasonal_Crop_Yield_Prediction_Rebuilt\Frontend\temp_dash.html"
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(content_mod)

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out = r"c:\Users\indra\OneDrive\Desktop\Seasonal Crop Yield Prediction\Seasonal_Crop_Yield_Prediction_Rebuilt\figures\ui_dashboard.png"

subprocess.run([
    chrome,
    "--headless",
    "--disable-gpu",
    f"--screenshot={out}",
    "--window-size=1400,900",
    f"file:///{temp_html}"
])

if os.path.exists(temp_html):
    os.remove(temp_html)

print("Dashboard screenshot created:", os.path.exists(out), os.path.getsize(out) if os.path.exists(out) else 0)
