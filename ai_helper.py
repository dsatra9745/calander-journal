from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
from io import BytesIO
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

app = Flask(__name__)
CORS(app)

# API KEY
ANTHROPIC_API_KEY = "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"

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
                "model": "claude-3-haiku-20240307",
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
    entries = data.get("entries", "")
    date_range = data.get("dateRange", "")
    
    print(f"Generating 4-prompt PDF for: {date_range}")
    
    # Create PDF with canvas
    buffer = BytesIO()
    c = pdf_canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title page
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height - 60, "🧠 Your Journal Analysis Prompts")
    
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.grey)
    c.drawCentredString(width/2, height - 85, f"Entries: {date_range}")
    
    # Instructions
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 120, "HOW TO USE:")
    
    c.setFont("Helvetica", 10)
    instructions = [
        "1. Go to claude.ai (create free account if needed)",
        "2. Start FOUR separate conversations",
        "3. Copy each prompt below into a different conversation",
        "4. Compare the 4 different perspectives you get"
    ]
    
    y = height - 145
    for inst in instructions:
        c.drawString(60, y, inst)
        y -= 18
    
    y -= 10
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Why 4 prompts? Each reveals different patterns:")
    
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.Color(0.2, 0.4, 0.7))
    c.drawString(60, y - 18, "• Evidence-Based: Neutral observations")
    c.setFillColor(colors.Color(0.8, 0.2, 0.2))
    c.drawString(60, y - 33, "• Blind Spot Hunter: Contradictions you miss")
    c.setFillColor(colors.Color(0.2, 0.6, 0.3))
    c.drawString(60, y - 48, "• Growth Mirror: What you can control")
    c.setFillColor(colors.Color(0.9, 0.5, 0))
    c.drawString(60, y - 63, "• Thematic: The connecting thread")
    
    c.setFillColor(colors.black)
    
    # The 4 prompts
    prompts = {
        "Evidence-Based Pattern Detector": {
            "color": colors.Color(0.2, 0.4, 0.7),
            "text": f"""Analyze the following 7 days of journal entries. Your role is to identify patterns that appear multiple times (3+ instances) in the user's own words. Be specific and cite examples when relevant. Focus only on what's clearly present in the text - do not infer or assume beyond the evidence.

Structure your response in two sections:
1) RECURRING PATTERNS: List patterns you observe with evidence
2) UNCLEAR/NEEDS MORE DATA: What's ambiguous or would benefit from more information

Keep response under 200 words, neutral and professional tone. Do not use any names of people mentioned in the entries - refer to them as "a friend," "a relationship," etc.

JOURNAL ENTRIES:

{entries}"""
        },
        "Blind Spot Hunter": {
            "color": colors.Color(0.8, 0.2, 0.2),
            "text": f"""Read these journal entries looking for blind spots:
1) Contradictions between stated values and described behaviors
2) Topics mentioned once then avoided
3) Patterns of attributing outcomes to external factors vs internal choices
4) Gaps between what they say they want and what they're actually doing

Be direct but not harsh. Point out only what you have clear evidence for from their own words. Focus on patterns that appear across multiple entries or life areas.

Keep response under 200 words. Do not use any names of people mentioned in the entries - refer to them as "a friend," "someone you mentioned," etc.

JOURNAL ENTRIES:

{entries}"""
        },
        "Growth-Oriented Mirror": {
            "color": colors.Color(0.2, 0.6, 0.3),
            "text": f"""Analyze these entries as if you're a supportive but honest friend. Identify:
1) Where they're underestimating their own agency
2) Obstacles they might be able to shift with different perspective
3) One pattern that, if changed, might unlock progress in multiple areas

Focus on what they can control. Be encouraging but don't sugarcoat. Point out strengths they've demonstrated in the entries themselves - only claim abilities you have evidence for.

Keep response under 200 words. Do not use any names of people mentioned in the entries.

JOURNAL ENTRIES:

{entries}"""
        },
        "Thematic Synthesizer": {
            "color": colors.Color(0.9, 0.5, 0),
            "text": f"""Look across all entries for the connecting thread - what's the core tension or theme running through multiple areas of their life? Identify the deeper story beneath the surface complaints or observations.

What's the one insight that ties together different domains (career, relationships, creative work, etc.)? What pattern are they running that shows up everywhere?

Be concise and insightful. Keep response under 150 words. Do not use any names of people mentioned in the entries.

JOURNAL ENTRIES:

{entries}"""
        }
    }
    
    # New page for each prompt
    prompt_num = 1
    for title, data in prompts.items():
        c.showPage()
        
        # Header with colored bar
        c.setFillColor(data["color"])
        c.rect(0, height - 40, width, 40, fill=1, stroke=0)
        
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 27, f"PROMPT {prompt_num}: {title}")
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 11)
        y = height - 70
        c.drawString(50, y, f"▼ COPY THIS ENTIRE TEXT INTO CLAUDE.AI ▼")
        
        # Gray box for prompt
        y -= 20
        box_top = y
        box_left = 40
        box_right = width - 40
        
        c.setFillColor(colors.Color(0.95, 0.95, 0.95))
        c.rect(box_left, 50, box_right - box_left, box_top - 50, fill=1, stroke=0)
        
        # Add prompt text
        c.setFillColor(colors.black)
        c.setFont("Courier", 7)
        
        y = box_top - 15
        for line in data["text"].split('\n'):
            if y < 70:  # New page if needed
                c.showPage()
                y = height - 50
                # Continue gray background
                c.setFillColor(colors.Color(0.95, 0.95, 0.95))
                c.rect(box_left, 50, box_right - box_left, height - 100, fill=1, stroke=0)
                c.setFillColor(colors.black)
                c.setFont("Courier", 7)
            
            # Wrap long lines
            if len(line) > 100:
                words = line.split(' ')
                current_line = ""
                for word in words:
                    if len(current_line + word) < 100:
                        current_line += word + " "
                    else:
                        c.drawString(box_left + 10, y, current_line.strip())
                        y -= 10
                        current_line = word + " "
                        if y < 70:
                            c.showPage()
                            y = height - 50
                            c.setFillColor(colors.Color(0.95, 0.95, 0.95))
                            c.rect(box_left, 50, box_right - box_left, height - 100, fill=1, stroke=0)
                            c.setFillColor(colors.black)
                            c.setFont("Courier", 7)
                if current_line.strip():
                    c.drawString(box_left + 10, y, current_line.strip())
                    y -= 10
            else:
                c.drawString(box_left + 10, y, line)
                y -= 10
        
        # End marker
        y -= 5
        if y < 70:
            c.showPage()
            y = height - 50
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, 60, "▲ COPY UNTIL HERE ▲")
        
        prompt_num += 1
    
    # Final page with summary
    c.showPage()
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 100, "Next Steps")
    
    c.setFont("Helvetica", 11)
    y = height - 140
    tips = [
        "1. Paste each prompt into a separate Claude.ai conversation",
        "2. Read all 4 analyses - they each reveal different things",
        "3. The most valuable insights often come from Blind Spot Hunter",
        "4. Use Growth Mirror for actionable next steps",
        "5. Save these analyses and revisit them in a month"
    ]
    
    for tip in tips:
        c.drawString(60, y, tip)
        y -= 25
    
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.grey)
    c.drawCentredString(width/2, 60, "📌 Four perspectives give you a fuller picture than any single analysis could")
    
    c.save()
    buffer.seek(0)
    
    print("4-prompt PDF generated successfully")
    
    return send_file(
        buffer, mimetype='application/pdf',
        as_attachment=True,
        download_name=f'journal-4-prompts-{date_range}.pdf'
    )

if __name__ == "__main__":
    print("Starting Flask server...")
    print(f"API key configured: {bool(ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != 'sk-ant-your-key-here')}")
    app.run(port=3000, debug=True)
