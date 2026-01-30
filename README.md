[README-FOR-TESTERS.md](https://github.com/user-attachments/files/24954920/README-FOR-TESTERS.md)
# 📖 Calendar Journal - Testing Guide

**Thanks for testing! This is a self-reflection journal app with AI-powered insights.**

---

## 🚀 How to Start

1. **Put all 4 files in one folder:**
   - `calendar2nd.html`
   - `ai_helper.py`
   - `start-calendar.vbs`
   - `stop-calendar.bat`

2. **Double-click `start-calendar.vbs`**
   - Wait 5 seconds
   - Browser opens automatically
   - You'll see the calendar interface

3. **When you're done, double-click `stop-calendar.bat`**
   - This closes all background processes

---

## ✍️ How to Use

### **Writing Entries:**
1. Click any day on the calendar
2. Answer the daily question (minimum 50 words)
3. Optional: Add extra thoughts in the "Anything else?" box
4. Click "💾 Save Entry"
5. Green checkmark appears on calendar

**Tips:**
- Click "Need help?" for writing hints
- Each day has a different rotating question
- The app prevents lazy one-word answers

### **Getting AI Insights (Paid Feature):**
1. Write at least **7 entries**
2. Click the **"🧠 Auto Insights"** button
3. Wait ~30 seconds
4. You'll get **4 different perspectives** on your journal:
   - 📊 Evidence-Based (patterns)
   - 🔍 Blind Spot Hunter (contradictions)
   - 🌱 Growth Mirror (actionable advice)
   - 🎨 Thematic (the deeper story)

5. Click any insight in the sidebar to read it again
6. Delete button (⋮) lets you remove insights

### **Free Alternative (PDF Export):**
1. Write 7+ entries
2. Click **"📄 Export PDF"**
3. PDF downloads with 4 AI prompts
4. Paste each prompt into claude.ai yourself
5. Get the same insights for free!

---

## 🧪 What to Test

### **Priority 1 - Core Features:**
- [ ] Write 7+ journal entries
- [ ] Generate AI insights (should take ~30 seconds)
- [ ] Read all 4 analysis perspectives
- [ ] Export PDF and verify it has 4 prompts
- [ ] Delete an insight and generate new ones

### **Priority 2 - Selection Feature:**
- [ ] Write 10+ entries
- [ ] Click "Select & Analyze" button
- [ ] Selection modal should appear
- [ ] Choose exactly 7 entries
- [ ] Generate insights for those specific entries

### **Priority 3 - Polish:**
- [ ] Try hints on different questions
- [ ] Upload a month theme image
- [ ] Upload a day image
- [ ] Check if data persists after closing/reopening
- [ ] Try validation (write <50 words - should reject)

---

## 🐛 Found a Bug? Report It!

**[PASTE YOUR GOOGLE FORM LINK HERE]**

Please include:
- What were you doing?
- What happened?
- What did you expect?
- Screenshot (if possible)

---

## ❓ Troubleshooting

### **"Can't see AI Insights button"**
- Make sure you wrote at least 7 entries
- Try refreshing the page (Ctrl+R)
- Check if Flask server is running (see console for errors)

### **"AI Insights not generating"**
- Did you double-click `start-calendar.vbs`? (starts both servers)
- Check browser console (F12) for errors
- Try manually running: `python ai_helper.py` in command prompt

### **"Nothing happens when I click start-calendar.vbs"**
- Make sure Python is installed
- Try right-click → "Run as administrator"
- Check all 4 files are in the same folder

### **"My entries disappeared!"**
- Did you move the HTML file? (data is tied to file location)
- Check browser cache wasn't cleared
- Data is stored locally per-browser

### **"I closed my browser, where's my data?"**
- Open the app again with `start-calendar.vbs`
- Data should still be there (stored in browser)

---

## 💡 Tips for Testers

- **Write real entries** - AI insights work better with honest writing
- **Test the PDF export** - that's the free tier users will use
- **Try breaking it** - click things quickly, refresh randomly
- **Check different days** - questions rotate across 60 different prompts
- **Test selection** - the ability to choose which 7 entries matters

---

## 📝 What's This App For?

This is a **journaling app with AI analysis**. The goal:

- Help people reflect on their week
- Get 4 different AI perspectives (not just generic advice)
- Freemium model: Free PDF export OR paid auto-generation
- Designed to be brutally honest (especially "Blind Spot Hunter")

**Target users:** People doing self-improvement, therapy journaling, or personal growth work.

---

## ⏱️ Expected Testing Time

- **Quick test:** 15 minutes (write a few entries, try one feature)
- **Full test:** 45-60 minutes (write 7+ entries, test everything)
- **Thorough test:** 2+ hours (write 10+ days, test edge cases)

---

## 🙏 Thank You!

Your feedback will help make this app actually useful. The most valuable feedback:

✅ "This feature confused me because..."
✅ "I expected X to happen, but Y happened"
✅ "I wanted to do X but couldn't figure out how"

Less valuable:
❌ "This is cool"
❌ "Nice app"

**Be brutally honest** - I'd rather fix issues now than ship a broken product!

---

**Questions? [YOUR CONTACT INFO HERE]**
