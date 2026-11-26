"""
IntelliFlow Technical Report & Viva Dossier PDF Generator.
Converts Markdown to styled HTML and renders it to vector PDF using Headless Chromium.
"""
import os
import re
import subprocess
import markdown

import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_MD_PATH = os.path.join(PROJECT_ROOT, "INTELLIFLOW_VIVA_AND_PROJECT_REPORT.md")
DEFAULT_PDF_PATH = os.path.join(PROJECT_ROOT, "INTELLIFLOW_VIVA_AND_PROJECT_REPORT.pdf")

def build_pdf(md_path=None, pdf_path=None, title=None):
    md_file = os.path.abspath(md_path) if md_path else DEFAULT_MD_PATH
    pdf_file = os.path.abspath(pdf_path) if pdf_path else DEFAULT_PDF_PATH
    html_file = os.path.abspath(os.path.join(PROJECT_ROOT, f"scratch_{os.path.splitext(os.path.basename(md_file))[0]}.html"))
    doc_title = title or "IntelliFlow - Technical Report & Viva Defense Dossier"

    print(f"Reading markdown from: {md_file}")
    with open(md_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Clean up mermaid blocks into pre tags
    text = re.sub(r'```mermaid\s+(.*?)\s+```', r'<pre class="mermaid">\1</pre>', text, flags=re.DOTALL)

    # Convert Markdown to HTML
    html_body = markdown.markdown(text, extensions=["tables", "fenced_code", "nl2br"])

    # Format custom GitHub alert callouts
    html_body = re.sub(
        r'<blockquote>\s*<p>\[!NOTE\]\s*(.*?)</p>\s*</blockquote>',
        r'<div class="alert alert-note"><strong>NOTE:</strong> \1</div>',
        html_body,
        flags=re.DOTALL
    )
    html_body = re.sub(
        r'<blockquote>\s*<p>\[!IMPORTANT\]\s*(.*?)</p>\s*</blockquote>',
        r'<div class="alert alert-important"><strong>IMPORTANT:</strong> \1</div>',
        html_body,
        flags=re.DOTALL
    )
    html_body = re.sub(
        r'<blockquote>\s*<p>\[!WARNING\]\s*(.*?)</p>\s*</blockquote>',
        r'<div class="alert alert-warning"><strong>WARNING:</strong> \1</div>',
        html_body,
        flags=re.DOTALL
    )

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>IntelliFlow - Technical Report & Viva Defense Dossier</title>
<style>
@page {{
    size: A4;
    margin: 16mm 15mm 16mm 15mm;
    @bottom-right {{
        content: counter(page);
    }}
}}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.5;
    font-size: 9.5pt;
}}
h1 {{
    color: #0f172a;
    font-size: 19pt;
    border-bottom: 2.5px solid #2563eb;
    padding-bottom: 5px;
    margin-top: 0;
    margin-bottom: 10px;
}}
h2 {{
    color: #1e3a8a;
    font-size: 13.5pt;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 3px;
    margin-top: 18px;
    margin-bottom: 8px;
    page-break-after: avoid;
}}
h3 {{
    color: #0369a1;
    font-size: 11pt;
    margin-top: 12px;
    margin-bottom: 5px;
    page-break-after: avoid;
}}
p, li {{
    color: #334155;
    margin-top: 2px;
    margin-bottom: 5px;
}}
strong {{
    color: #0f172a;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
}}
th, td {{
    border: 1px solid #cbd5e1;
    padding: 5px 8px;
    text-align: left;
}}
th {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
}}
tr:nth-child(even) {{
    background-color: #f8fafc;
}}
pre {{
    background: #0f172a;
    color: #f8fafc;
    padding: 8px 12px;
    border-radius: 5px;
    font-size: 7.5pt;
    overflow-x: auto;
    page-break-inside: avoid;
    font-family: "JetBrains Mono", Consolas, Monaco, monospace;
    line-height: 1.3;
}}
code {{
    background: #f1f5f9;
    color: #0f172a;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 8.5pt;
    font-family: "JetBrains Mono", Consolas, Monaco, monospace;
}}
pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
}}
.alert {{
    border-left: 4px solid #3b82f6;
    background: #eff6ff;
    padding: 7px 11px;
    margin: 8px 0;
    border-radius: 0 4px 4px 0;
    font-size: 9pt;
}}
.alert-note {{
    border-color: #3b82f6;
    background: #eff6ff;
}}
.alert-important {{
    border-color: #f59e0b;
    background: #fffbeb;
}}
.alert-warning {{
    border-color: #ef4444;
    background: #fef2f2;
}}
hr {{
    border: 0;
    height: 1px;
    background: #e2e8f0;
    margin: 14px 0;
}}
.mermaid {{
    background: #f8fafc;
    color: #0f172a;
    border: 1px dashed #cbd5e1;
    white-space: pre-wrap;
}}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(full_html)

    # Locate Chrome or Edge
    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    browser_bin = None
    for cand in chrome_candidates:
        if os.path.exists(cand):
            browser_bin = cand
            break

    if not browser_bin:
        raise RuntimeError("Neither Chrome nor Edge was found on the system.")

    print(f"Using browser renderer: {browser_bin}")
    cmd = [
        browser_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        html_file
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_file):
        size_kb = os.path.getsize(pdf_file) / 1024
        print(f"SUCCESS: PDF created at {pdf_file} ({size_kb:.1f} KB)")
    else:
        print(f"Error generating PDF: {res.stderr}")

    if os.path.exists(html_file):
        os.remove(html_file)

if __name__ == "__main__":
    in_md = sys.argv[1] if len(sys.argv) > 1 else None
    out_pdf = sys.argv[2] if len(sys.argv) > 2 else None
    build_pdf(in_md, out_pdf)
