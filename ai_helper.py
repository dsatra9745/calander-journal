from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import os
from io import BytesIO
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

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
        date_range = f"{dates[0]} to {dates[-1]}"
    else:
        date_range = "Unknown dates"
    
    print(f"Generating clean PDF for: {date_range}")
    
    # Create PDF
    buffer = BytesIO()
    c = pdf_canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # ===== PAGE 1: COVER =====
    # Title
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, height - 100, "Your Journal Analysis")
    
    # Date info
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.Color(0.4, 0.4, 0.4))
    c.drawCentredString(width/2, height - 130, f"{date_range}  •  {len(entries)} entries")
    
    # How to use box
    box_top = height - 180
    box_height = 140
    c.setFillColor(colors.Color(0.94, 0.97, 1.0))  # Light blue
    c.roundRect(60, box_top - box_height, width - 120, box_height, 10, fill=1, stroke=0)
    
    # Blue left border
    c.setFillColor(colors.Color(0.23, 0.51, 0.97))
    c.rect(60, box_top - box_height, 4, box_height, fill=1, stroke=0)
    
    c.setFillColor(colors.Color(0.12, 0.25, 0.55))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(80, box_top - 25, "How to use:")
    
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    
    steps = [
        ("1", "Upload this PDF to ChatGPT, Claude, or any AI"),
        ("2", 'Type: "Do as the PDF tells you to do, please"'),
        ("3", "Get your analysis")
    ]
    
    y = box_top - 55
    for num, text in steps:
        # Number circle
        c.setFillColor(colors.Color(0.23, 0.51, 0.97))
        c.circle(90, y + 4, 10, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(90, y, num)
        
        # Text
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 11)
        c.drawString(110, y, text)
        y -= 32
    
    c.setFillColor(colors.black)
    
    # ===== PAGE 2: THE PROMPT =====
    c.showPage()
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "ANALYSIS PROMPT")
    
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.Color(0.4, 0.4, 0.4))
    c.drawString(50, height - 70, "The AI will follow these instructions when analyzing your entries.")
    
    # Prompt box
    c.setFillColor(colors.Color(0.96, 0.96, 0.96))
    prompt_box_top = height - 95
    prompt_box_height = 320
    c.roundRect(40, prompt_box_top - prompt_box_height, width - 80, prompt_box_height, 8, fill=1, stroke=0)
    
    prompt_text = """Analyze these journal entries from 4 perspectives:

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
- Don't use names of people mentioned"""

    c.setFillColor(colors.black)
    c.setFont("Courier", 9)
    
    y = prompt_box_top - 20
    for line in prompt_text.split('\n'):
        c.drawString(55, y, line)
        y -= 14
    
    # ===== PAGE 3+: ENTRIES =====
    c.showPage()
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "JOURNAL ENTRIES")
    
    y = height - 90
    
    for i, entry in enumerate(entries):
        date = entry.get('date', 'Unknown')
        answer = entry.get('answer', '')
        question_idx = entry.get('questionIndex', 0)
        
        # Determine category
        cat_idx = question_idx % 3
        category = ['PAST', 'PRESENT', 'FUTURE'][cat_idx]
        
        # Check if we need a new page
        if y < 150:
            c.showPage()
            y = height - 50
        
        # Entry header
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.Color(0.4, 0.4, 0.4))
        c.drawString(50, y, f"Entry {i+1}  —  {date}  —  {category}")
        y -= 20
        
        # Entry text
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        
        # Word wrap the answer
        words = answer.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            if len(test_line) > 85:
                c.drawString(50, y, line.strip())
                y -= 14
                line = word + " "
                if y < 60:
                    c.showPage()
                    y = height - 50
            else:
                line = test_line
        if line.strip():
            c.drawString(50, y, line.strip())
            y -= 14
        
        y -= 20  # Space between entries
    
    c.save()
    buffer.seek(0)
    
    print("Clean PDF generated successfully")
    
    return send_file(
        buffer, 
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'journal-analysis.pdf'
    )

if __name__ == "__main__":
    print("Starting Flask server...")
    print(f"API key configured: {bool(ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != 'sk-ant-your-key-here')}")
    app.run(host='0.0.0.0', port=10000)
