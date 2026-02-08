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
    
    print(f"Generating PDF for: {date_range}")
    
    # Create PDF
    buffer = BytesIO()
    c = pdf_canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # ===== PAGE 1: COVER =====
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width/2, height - 80, "Your Journal Analysis")
    
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.Color(0.4, 0.4, 0.4))
    c.drawCentredString(width/2, height - 105, f"{date_range}  |  {len(entries)} entries")
    
    # How to use box
    c.setFillColor(colors.Color(0.94, 0.97, 1.0))
    c.roundRect(80, height - 280, width - 160, 140, 10, fill=1, stroke=0)
    
    c.setFillColor(colors.Color(0.23, 0.51, 0.97))
    c.rect(80, height - 280, 4, 140, fill=1, stroke=0)
    
    c.setFillColor(colors.Color(0.12, 0.25, 0.55))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 160, "How to use:")
    
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    c.drawString(100, height - 190, "1. Upload this PDF to ChatGPT, Claude, or any AI")
    c.drawString(100, height - 215, '2. Type: "Do as the PDF tells you to do, please"')
    c.drawString(100, height - 240, "3. Get your analysis")
    
    # ===== PAGE 2: PROMPT =====
    c.showPage()
    
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawString(50, height - 50, "ANALYSIS PROMPT")
    
    c.setFillColor(colors.Color(0.96, 0.96, 0.96))
    c.roundRect(40, height - 400, width - 80, 330, 8, fill=1, stroke=0)
    
    prompt_lines = [
        "Analyze these journal entries from 4 perspectives:",
        "",
        "1. EVIDENCE-BASED PATTERNS",
        "What patterns appear consistently (3+ times)?",
        "Cite specific quotes or examples.",
        "",
        "2. BLIND SPOTS", 
        "What contradictions exist between stated values and actions?",
        "What topics are avoided?",
        "",
        "3. GROWTH & STRENGTHS",
        "What capabilities do they demonstrate?",
        "What's one actionable next step?",
        "",
        "4. DEEPER THEMES",
        "What's the core tension across all entries?",
        "What question do they keep circling back to?",
        "",
        "GUIDELINES:",
        "- Be specific, cite evidence",
        "- Keep each section under 150 words",
        "- Be honest but constructive",
        "- Don't use names of people mentioned"
    ]
    
    c.setFillColor(colors.black)
    c.setFont("Courier", 10)
    y = height - 85
    for line in prompt_lines:
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
        
        cat_idx = question_idx % 3
        category = ['PAST', 'PRESENT', 'FUTURE'][cat_idx]
        
        if y < 120:
            c.showPage()
            y = height - 50
        
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.Color(0.3, 0.3, 0.3))
        c.drawString(50, y, f"{date} — {category}")
        y -= 18
        
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        
        words = answer.split()
        line = ""
        for word in words:
            if len(line + word) > 90:
                c.drawString(50, y, line.strip())
                y -= 13
                line = word + " "
                if y < 60:
                    c.showPage()
                    y = height - 50
            else:
                line += word + " "
        if line.strip():
            c.drawString(50, y, line.strip())
            y -= 13
        
        y -= 18
    
    c.save()
    buffer.seek(0)
    
    return send_file(
        buffer, 
        mimetype='application/pdf',
        as_attachment=True,
        download_name='journal-analysis.pdf'
    )

@app.route("/ocr", methods=["POST"])
def ocr():
    print("\n=== OCR REQUEST ===")
    
    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "sk-ant-your-key-here":
        print("ERROR: API key not set!")
        return jsonify({"error": "API key not configured"}), 500
    
    data = request.json
    image_base64 = data.get("image", "")
    
    if not image_base64:
        return jsonify({"error": "No image provided"}), 400
    
    print(f"Image base64 length: {len(image_base64)}")
    
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
                "max_tokens": 2000,
                "messages": [{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_base64
                            }
                        },
                        {
                            "type": "text",
                            "text": "Please transcribe all the handwritten text in this image. Output only the transcribed text, nothing else. Preserve paragraph breaks where they appear."
                        }
                    ]
                }],
            },
            timeout=60
        )
        
        print(f"OCR Status code: {response.status_code}")
        
        if response.status_code != 200:
            return jsonify({"error": f"API error: {response.text}"}), response.status_code
        
        result = response.json()
        text = ""
        if "content" in result and len(result["content"]) > 0:
            text = result["content"][0].get("text", "")
            print(f"Transcribed text length: {len(text)}")
        else:
            return jsonify({"error": "No content in API response"}), 500
        
        return jsonify({"text": text})
        
    except Exception as e:
        print(f"OCR ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    print(f"API key configured: {bool(ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != 'sk-ant-your-key-here')}")
    app.run(host='0.0.0.0', port=10000)
