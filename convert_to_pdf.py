#!/usr/bin/env python3
"""Convert the methodology report from Markdown to a styled PDF using markdown + weasyprint."""

import sys
import os
import re

try:
    import markdown
    from weasyprint import HTML
except ImportError:
    print("ERROR: markdown or weasyprint not installed. Run: pip install markdown weasyprint")
    sys.exit(1)

try:
    import latex2mathml.converter as l2m
    HAS_MATHML = True
except ImportError:
    HAS_MATHML = False
    print("WARNING: latex2mathml not installed. Math will render as plain text. Run: pip install latex2mathml")

REPORT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(REPORT_DIR, "Rajasthan_Royals_SupeRR_Selector_Round1_Methodology_Report.md")
PDF_PATH = os.path.join(REPORT_DIR, "Rajasthan_Royals_SupeRR_Selector_Round1_Report.pdf")
CHARTS_DIR = os.path.join(REPORT_DIR, "charts")

with open(MD_PATH, 'r', encoding='utf-8') as f:
    md_content = f.read()


def latex_to_mathml(latex: str, display: bool) -> str:
    """Convert a LaTeX string to a MathML element."""
    if not HAS_MATHML:
        return f"<code>{latex}</code>"
    try:
        display_attr = 'block' if display else 'inline'
        mml = l2m.convert(latex, display=display_attr)
        return mml
    except Exception as e:
        # Graceful fallback: wrap raw LaTeX in a code span
        return f"<code>{latex}</code>"


def preprocess_math(text: str) -> str:
    """Replace $$...$$ and $...$ with MathML before markdown parsing."""
    # 1. Display math: $$...$$  (may span multiple lines)
    def replace_display(m):
        return latex_to_mathml(m.group(1).strip(), display=True)
    text = re.sub(r'\$\$(.*?)\$\$', replace_display, text, flags=re.DOTALL)

    # 2. Inline math: $...$  (not crossing newlines, not escaped)
    def replace_inline(m):
        return latex_to_mathml(m.group(1), display=False)
    text = re.sub(r'(?<!\$)\$([^\$\n]+?)\$(?!\$)', replace_inline, text)

    return text


md_content = preprocess_math(md_content)

# Convert markdown to HTML
html_body = markdown.markdown(
    md_content,
    extensions=['tables', 'fenced_code', 'toc', 'md_in_html'],
    output_format='html5'
)

# Embed charts as base64 images if they exist
import base64
for chart in ['scatter_batters_sr_csr.png', 'scatter_bowlers_econ_csr.png',
              'top_performers_radar_profile.png', 'rankings_rpcs_barchart.png']:
    chart_path = os.path.join(CHARTS_DIR, chart)
    if os.path.exists(chart_path):
        with open(chart_path, 'rb') as img_f:
            b64 = base64.b64encode(img_f.read()).decode('utf-8')
        # Add chart images at the end of the document before closing
        chart_title = chart.replace('.png', '').replace('_', ' ').title()
        html_body += f'<div class="chart"><h3>{chart_title}</h3><img src="data:image/png;base64,{b64}" style="max-width:100%;"></div>\n'

# Full HTML with CSS styling
html_full = f"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8">
<style>
@page {{
    size: A4;
    margin: 1.8cm 1.5cm;
    @top-center {{
        content: "Rajasthan Royals SupeRR Selector — Round 1 Methodology Report";
        font-size: 8pt;
        color: #999;
    }}
    @bottom-center {{
        content: "Page " counter(page) " of " counter(pages);
        font-size: 8pt;
        color: #999;
    }}
}}

body {{
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #1a1a1a;
    max-width: 100%;
}}

h1 {{
    font-size: 20pt;
    color: #EA1A8E;
    border-bottom: 3px solid #EA1A8E;
    padding-bottom: 8px;
    margin-top: 24px;
    page-break-after: avoid;
}}

h2 {{
    font-size: 15pt;
    color: #2D3691;
    border-bottom: 2px solid #2D3691;
    padding-bottom: 5px;
    margin-top: 22px;
    page-break-after: avoid;
}}

h3 {{
    font-size: 12pt;
    color: #333;
    margin-top: 16px;
    page-break-after: avoid;
}}

h4 {{
    font-size: 11pt;
    color: #EA1A8E;
    margin-top: 14px;
    page-break-after: avoid;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
}}

th {{
    background-color: #2D3691;
    color: white;
    font-weight: bold;
    padding: 6px 8px;
    text-align: left;
    border: 1px solid #1a237e;
}}

td {{
    padding: 5px 8px;
    border: 1px solid #ddd;
}}

tr:nth-child(even) {{
    background-color: #f8f9ff;
}}

tr:hover {{
    background-color: #eef0ff;
}}

code {{
    background-color: #f4f4f4;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 9pt;
    font-family: 'Consolas', 'Courier New', monospace;
}}

pre {{
    background-color: #f4f4f4;
    padding: 12px;
    border-radius: 5px;
    border-left: 4px solid #2D3691;
    overflow-x: auto;
    font-size: 8.5pt;
    page-break-inside: avoid;
}}

pre code {{
    background: none;
    padding: 0;
}}

strong {{
    color: #1a1a1a;
}}

em {{
    color: #555;
}}

blockquote {{
    border-left: 4px solid #EA1A8E;
    padding-left: 12px;
    margin-left: 0;
    color: #555;
    font-style: italic;
}}

hr {{
    border: none;
    border-top: 2px solid #e0e0e0;
    margin: 20px 0;
}}

.chart {{
    page-break-inside: avoid;
    margin: 15px 0;
    text-align: center;
}}

.chart img {{
    max-width: 95%;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}}

/* RR Brand Colors */
.rr-pink {{ color: #EA1A8E; }}
.rr-blue {{ color: #2D3691; }}

/* Math-like rendering */
sup {{ font-size: 0.75em; }}
sub {{ font-size: 0.75em; }}

/* MathML display */
math {{ font-family: 'STIX Two Math', 'Times New Roman', serif; }}
math[display="block"] {{
    display: block;
    text-align: center;
    margin: 12px 0;
    font-size: 11pt;
}}
math[display="inline"] {{
    display: inline;
    font-size: 10pt;
}}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

print(f"Converting to PDF... ({len(html_full)} bytes of HTML)")
HTML(string=html_full).write_pdf(PDF_PATH)
print(f"PDF written to: {PDF_PATH}")
print(f"PDF size: {os.path.getsize(PDF_PATH) / 1024:.1f} KB")

