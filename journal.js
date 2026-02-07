// ============================================
// JOURNAL WRITING
// ============================================

function openJournal(dateStr) {
    state.currentDate = dateStr;
    
    const date = new Date(dateStr + 'T00:00:00');
    const questionIndex = getQuestionForDate(date);
    const question = getQuestionDetails(questionIndex);
    
    // Initialize entry if it doesn't exist
    if (!state.entries[dateStr]) {
        state.entries[dateStr] = {
            questionIndex: questionIndex,
            answer: '',
            freeform: '',
            imageUrl: null
        };
    }
    
    const entry = state.entries[dateStr];
    
    // Set up banner
    const banner = document.getElementById('questionBanner');
    banner.className = `question-banner ${question.category.toLowerCase()}`;
    
    document.getElementById('questionCategory').textContent = question.category;
    document.getElementById('questionText').textContent = question.text;
    document.getElementById('hintContent').textContent = question.hint;
    
    // Load existing data
    document.getElementById('journalAnswer').value = entry.answer || '';
    document.getElementById('freeformText').value = entry.freeform || '';
    
    // Reset hint/freeform visibility
    document.getElementById('hintContent').classList.remove('visible');
    document.getElementById('freeformContent').classList.remove('visible');
    
    updateWordCount();
    
    // Show overlay
    const overlay = document.getElementById('journalOverlay');
    overlay.style.display = 'block';
}

function closeJournal() {
    document.getElementById('journalOverlay').style.display = 'none';
    render();
}

function handleAnswerInput(event) {
    event.stopPropagation();
    
    const dateStr = state.currentDate;
    const answer = document.getElementById('journalAnswer').value;
    
    state.entries[dateStr].answer = answer;
    
    // Save to Supabase
    saveEntry(dateStr, state.entries[dateStr]);
    
    updateWordCount();
    showAutoSaved();
}

function saveFreeform() {
    const dateStr = state.currentDate;
    const freeform = document.getElementById('freeformText').value;
    
    state.entries[dateStr].freeform = freeform;
    
    // Save to Supabase
    saveEntry(dateStr, state.entries[dateStr]);
    
    showAutoSaved();
}

function updateWordCount() {
    const answer = document.getElementById('journalAnswer').value;
    const count = getWordCount(answer);
    const wordCountEl = document.getElementById('wordCount');
    
    wordCountEl.textContent = `${count} / 149 words`;
    
    if (count < 149) {
        wordCountEl.classList.add('invalid');
    } else {
        wordCountEl.classList.remove('invalid');
    }
}

function showAutoSaved() {
    const el = document.getElementById('autoSaved');
    el.textContent = '✓ Saved';
    setTimeout(() => {
        el.textContent = '';
    }, 2000);
}

function toggleHints() {
    const content = document.getElementById('hintContent');
    content.classList.toggle('visible');
}

function toggleFreeform() {
    const content = document.getElementById('freeformContent');
    content.classList.toggle('visible');
}
