from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import os
from io import BytesIO
from weasyprint import HTML

app = Flask(__name__)
CORS(app)

# API KEY - reads from Render environment variable
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    print("\n=== NEW REQUEST ===")
    
    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "sk-ant-your-key-here":
        print("ERROR: API key not set!")
        return jsonify({"error": "API key not configured"}), 500
    
    print(f"API Key present: {ANTHROPIC_API_KEY[:15]}...")
    
    data = request.json
    prompt = data.get("prompt", "")
    print(f"Prompt length: {len(prompt)} characters")
    
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30
        )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code != 200:
            return jsonify({"error": f"API error: {response.text}"}), response.status_code
        
        result = response.json()
        text = ""
        if "content" in result and len(result["content"]) > 0:
            text = result["content"][0].get("text", "")
            print(f"Extracted text length: {len(text)}")
        else:
            return jsonify({"error": "No content in API response"}), 500
        
        return jsonify({"text": text})
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/export-prompt", methods=["POST"])
def export_prompt():
    print("\n=== EXPORT PROMPT REQUEST ===")
    
    data = request.json
    entries = data.get("entries", [])
    
    # Calculate date range
    if entries:
        dates = sorted([e.get('date', '') for e in entries])
        date_range = f"{dates[0]} – {dates[-1]}"
        first_date = dates[-1]  # Most recent date for display
    else:
        date_range = "Unknown dates"
        first_date = "Unknown"
    
    print(f"Generating PDF for: {date_range}")
    
    # Build entries HTML
    entries_html = ""
    for i, entry in enumerate(entries):
        date = entry.get('date', 'Unknown')
        answer = entry.get('answer', '').replace('\n', '<br>')
        question_idx = entry.get('questionIndex', 0)
        
        # Determine category
        cat_idx = question_idx % 3
        category = ['PAST', 'PRESENT', 'FUTURE'][cat_idx]
        
        entries_html += f'''
        <div class="entry">
            <div class="entry-date">{date} — {category}</div>
            <div class="entry-answer">{answer}</div>
        </div>
        '''
    
    # Full HTML template matching the mock
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&display=swap');
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        @page {{
            size: letter;
            margin: 0.5in;
        }}
        
        body {{ 
            font-family: 'DM Sans', -apple-system, sans-serif; 
            line-height: 1.7;
            color: #2d2d2d;
            font-size: 11pt;
        }}
        
        .cover {{
            text-align: center;
            padding: 40px 20px 30px;
            margin-bottom: 30px;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        .cover h1 {{
            font-family: 'DM Serif Display', Georgia, serif;
            font-size: 28pt;
            margin-bottom: 10px;
            font-weight: normal;
        }}
        
        .cover .dates {{
            color: #666;
            margin-bottom: 24px;
            font-size: 11pt;
        }}
        
        .how-to-use {{
            background: #f0f7ff;
            border: 2px solid #3b82f6;
            border-radius: 12px;
            padding: 20px 28px;
            text-align: left;
            max-width: 380px;
            margin: 0 auto;
        }}
        
        .how-to-use h3 {{
            font-size: 13pt;
            margin-bottom: 14px;
            color: #1e40af;
        }}
        
        .step {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 10px;
            font-size: 10.5pt;
        }}
        
        .step:last-child {{
            margin-bottom: 0;
        }}
        
        .step-num {{
            background: #3b82f6;
            color: white;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 10pt;
            font-weight: bold;
            flex-shrink: 0;
        }}
        
        .step strong {{
            background: #e0edff;
            padding: 3px 6px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 9.5pt;
        }}
        
        .prompt-section {{
            background: #fafafa;
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 30px;
            border: 1px solid #e8e8e8;
            page-break-inside: avoid;
        }}
        
        .prompt-section h2 {{
            font-size: 14pt;
            margin-bottom: 16px;
            color: #444;
        }}
        
        .prompt-box {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            line-height: 1.7;
            white-space: pre-wrap;
            border: 1px solid #ddd;
        }}
        
        .entries-section h2 {{
            font-size: 16pt;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .entry {{
            margin-bottom: 24px;
            padding-bottom: 24px;
            border-bottom: 1px solid #eee;
            page-break-inside: avoid;
        }}
        
        .entry:last-child {{
            border-bottom: none;
        }}
        
        .entry-date {{
            font-weight: 600;
            color: #666;
            font-size: 10pt;
            margin-bottom: 8px;
        }}
        
        .entry-answer {{
            font-size: 10.5pt;
            line-height: 1.7;
        }}
    </style>
</head>
<body>

<div class="cover">
    <h1>📔 Your Journal Analysis</h1>
    <div class="dates">{date_range} • {len(entries)} entries</div>
    
    <div class="how-to-use">
        <h3>How to use:</h3>
        <div class="step">
            <span class="step-num">1</span>
            <span>Upload this PDF to ChatGPT, Claude, or any AI</span>
        </div>
        <div class="step">
            <span class="step-num">2</span>
            <span>Type: <strong>"Do as the PDF tells you to do, please"</strong></span>
        </div>
        <div class="step">
            <span class="step-num">3</span>
            <span>Get your analysis</span>
        </div>
    </div>
</div>

<div class="prompt-section">
    <h2>ANALYSIS PROMPT</h2>
    <div class="prompt-box">Analyze these journal entries from 4 perspectives:

1. EVIDENCE-BASED PATTERNS
What patterns appear consistently (3+ times)? Cite specific quotes or examples from the entries.

2. BLIND SPOTS
What contradictions exist between what they say they value and what they actually do? What topics are mentioned once then avoided? What might they not be seeing?

3. GROWTH & STRENGTHS
What capabilities or resilience do they demonstrate (with evidence)? What's one specific, actionable next step?

4. DEEPER THEMES
What's the core tension running through all entries? What question do they keep circling back to?

GUIDELINES:
- Be specific, cite evidence from the entries
- Keep each section under 150 words
- Be honest but constructive
- Don't use names of people mentioned</div>
</div>

<div class="entries-section">
    <h2>JOURNAL ENTRIES</h2>
    {entries_html}
</div>

</body>
</html>'''
    
    # Convert HTML to PDF
    pdf_buffer = BytesIO()
    HTML(string=html_content).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    
    print("PDF generated successfully")
    
    return send_file(
        pdf_buffer, 
        mimetype='application/pdf',
        as_attachment=True,
        download_name='journal-analysis.pdf'
    )

if __name__ == "__main__":
    print("Starting Flask server...")
    print(f"API key configured: {bool(ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != 'sk-ant-your-key-here')}")
    app.run(host='0.0.0.0', port=10000)
