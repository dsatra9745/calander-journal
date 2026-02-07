// ============================================
// VALIDATION FUNCTIONS
// ============================================

function getWordCount(text) {
    if (!text) return 0;
    return text.trim().split(/\s+/).filter(w => w.length > 0).length;
}

function detectMinimumEffort(text) {
    const words = text.trim().split(/\s+/);
    const wordCounts = {};
    const commonWords = ['i', 'a', 'an', 'the', 'to', 'is', 'am', 'are', 'was', 'be', 'my', 'me', 'and', 'or', 'of', 'in', 'it', 'that', 'this', 'for', 'on', 'but', 'with', 'have', 'at', 'want', 'do', 'not'];
    
    words.forEach(w => {
        const cleaned = w.toLowerCase();
        if (!commonWords.includes(cleaned)) {
            wordCounts[cleaned] = (wordCounts[cleaned] || 0) + 1;
        }
    });
    
    for (let count of Object.values(wordCounts)) {
        if (count >= 15) return true;
    }
    
    return false;
}

function isValidEntry(text) {
    if (!text || text.trim().length === 0) return false;
    
    const words = text.trim().split(/\s+/);
    if (words.length < 149) return false;
    
    if (detectMinimumEffort(text)) return false;
    
    return true;
}
