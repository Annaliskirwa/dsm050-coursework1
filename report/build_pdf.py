"""Build report/DSM050_CW1.pdf from report/DSM050_CW1.md

Pipeline:
    Markdown  --markdown-->  HTML  --Playwright/Chromium-->  PDF

Run:
    python report/build_pdf.py
"""
from __future__ import annotations

import re
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
MD   = HERE / "DSM050_CW1.md"
HTML = HERE / "DSM050_CW1.html"
PDF  = HERE / "DSM050_CW1.pdf"
ROOT = HERE.parent

# --- CSS: A4, academic, print-friendly -------------------------------------
CSS = """
@page { size: A4; margin: 22mm 20mm; }
html { font-size: 11pt; }
body {
  font-family: "Helvetica Neue", Arial, sans-serif;
  color: #222; line-height: 1.5; max-width: 100%;
}
h1, h2, h3, h4 { color: #1a3a5c; font-weight: 700; page-break-after: avoid; }
h1 { font-size: 20pt; border-bottom: 2px solid #1a3a5c; padding-bottom: 4pt; }
h2 { font-size: 15pt; margin-top: 1.4em; }
h3 { font-size: 12pt; margin-top: 1.2em; }
p  { text-align: justify; margin: 0.4em 0 0.8em; }
figure { text-align: center; margin: 1em 0; page-break-inside: avoid; }
figure img { max-width: 100%; height: auto; }
figcaption {
  font-size: 9.5pt; color: #555; font-style: italic;
  margin-top: 4pt;
}
img { max-width: 100%; height: auto; }
table { border-collapse: collapse; width: 100%; margin: 0.6em 0; font-size: 10pt; }
th, td { border: 1px solid #bbb; padding: 4pt 6pt; text-align: left; }
th { background: #eef2f7; }
blockquote {
  border-left: 3px solid #1a3a5c; margin: 0.6em 0;
  padding: 0.2em 0.9em; color: #444; background: #f6f9fc;
}
code {
  font-family: "SF Mono", Menlo, Consolas, monospace;
  background: #f2f4f7; padding: 1pt 4pt; border-radius: 3px; font-size: 9.5pt;
}
pre code { display: block; padding: 8pt; overflow-x: auto; }
hr { border: 0; border-top: 1px solid #ccc; margin: 1.2em 0; }
a { color: #1a3a5c; text-decoration: none; }
.footer { font-size: 9pt; color: #888; text-align: center; margin-top: 2em; }
"""

# --- Markdown --------------------------------------------------------------
md_text = MD.read_text(encoding="utf-8")
html_body = markdown.markdown(
    md_text,
    extensions=[
        "extra",           # tables, fenced code, footnotes, attr_list
        "sane_lists",
        "toc",
        "codehilite",
    ],
    extension_configs={
        "codehilite": {"guess_lang": False, "noclasses": True},
    },
)

# Wrap bare <img> tags in <figure>/<figcaption> when alt text is present so
# that image captions render as proper figures in the PDF.
def wrap_figures(html: str) -> str:
    pattern = re.compile(
        r'<p>\s*(<img[^>]*alt="([^"]+)"[^>]*/?>)\s*</p>',
        flags=re.IGNORECASE,
    )
    return pattern.sub(
        lambda m: f'<figure>{m.group(1)}<figcaption>{m.group(2)}</figcaption></figure>',
        html,
    )

html_body = wrap_figures(html_body)

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>DSM050 Coursework 1</title>
<style>{CSS}</style>
</head>
<body>
{html_body}
</body>
</html>
"""
HTML.write_text(full_html, encoding="utf-8")
print(f"HTML written   → {HTML.relative_to(ROOT)}")

# --- HTML → PDF via headless Chromium --------------------------------------
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(HTML.as_uri(), wait_until="networkidle")
    page.pdf(
        path=str(PDF),
        format="A4",
        margin={"top": "22mm", "right": "20mm", "bottom": "22mm", "left": "20mm"},
        print_background=True,
    )
    browser.close()

print(f"PDF written    → {PDF.relative_to(ROOT)}")
