// ============================================
// INSIGHTS GENERATION
// ============================================

function updateGenerateButton() {
    const btn = document.getElementById('generateBtn');
    const validEntries = Object.entries(state.entries).filter(([_, entry]) => 
        isValidEntry(entry.answer)
    );
    
    btn.disabled = validEntries.length < 7;
    btn.textContent = `🧠 AI Insights (${validEntries.length}/7)`;
}

async function generateInsights() {
    // Get all analyzed dates from insights history
    const analyzedDates = new Set();
    state.insightsHistory.forEach(insight => {
        insight.entries.forEach(date => analyzedDates.add(date));
    });
    
    // Get valid entries that haven't been analyzed yet
    const validEntries = Object.entries(state.entries)
        .filter(([date, entry]) => isValidEntry(entry.answer) && !analyzedDates.has(date))
        .map(([date, entry]) => ({ date, ...entry }));
    
    if (validEntries.length < 7) {
        alert('You need at least 7 new (unanalyzed) entries to generate insights.');
        return;
    }
    
    if (validEntries.length > 7) {
        openSelectionModal(validEntries);
        return;
    }
    
    await runInsightsGeneration(validEntries);
}

function openSelectionModal(entries) {
    const modal = document.getElementById('selectionModal');
    const grid = document.getElementById('selectionGrid');
    
    grid.innerHTML = entries.map((entry, idx) => {
        const question = getQuestionDetails(entry.questionIndex);
        return `
            <div class="selection-item" onclick="toggleSelection(${idx})">
                <div class="selection-date">${entry.date}</div>
                <div class="selection-question">${question.text.substring(0, 60)}...</div>
            </div>
        `;
    }).join('');
    
    modal.classList.add('visible');
    window.selectionState = { entries, selected: [] };
    updateSelectionCount();
}

function closeSelectionModal() {
    document.getElementById('selectionModal').classList.remove('visible');
}

function toggleSelection(idx) {
    const selected = window.selectionState.selected;
    const index = selected.indexOf(idx);
    
    if (index > -1) {
        selected.splice(index, 1);
    } else if (selected.length < 7) {
        selected.push(idx);
    }
    
    const items = document.querySelectorAll('.selection-item');
    items[idx].classList.toggle('selected', selected.includes(idx));
    
    updateSelectionCount();
}

function updateSelectionCount() {
    const count = window.selectionState.selected.length;
    document.getElementById('selectionCount').textContent = `${count} / 7 selected`;
    document.getElementById('confirmSelectionBtn').disabled = count !== 7;
}

async function confirmSelection() {
    const { entries, selected } = window.selectionState;
    const selectedEntries = selected.map(idx => entries[idx]);
    
    closeSelectionModal();
    await runInsightsGeneration(selectedEntries);
}

async function runInsightsGeneration(entries) {
    const btn = document.getElementById('generateBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Generating...';
    
    const prompts = [
        {
            title: "Evidence-Based Insights",
            subtitle: "What the data actually shows",
            type: "evidence",
            prompt: `Analyze these 7 journal entries and provide evidence-based insights. Focus on:\n1. Patterns that appear consistently\n2. Contradictions or areas of internal conflict\n3. Specific examples that illustrate key themes\n\nBe direct and cite specific evidence from the entries. Avoid generic statements.\n\n${formatEntriesForAI(entries)}`
        },
        {
            title: "Blind Spot Hunter",
            subtitle: "What you might not be seeing",
            type: "blindspot",
            prompt: `Act as a perceptive observer analyzing these entries. Point out:\n1. Things the writer seems to be avoiding or not acknowledging\n2. Patterns they might not recognize in themselves\n3. Questions they should be asking but aren't\n\nBe honest but constructive. Challenge assumptions.\n\n${formatEntriesForAI(entries)}`
        },
        {
            title: "Growth Mirror",
            subtitle: "Your capabilities & potential",
            type: "growth",
            prompt: `Identify genuine strengths and growth opportunities based on these entries:\n1. Skills and qualities demonstrated (with evidence)\n2. Areas showing progress or development\n3. Concrete next steps for growth\n\nFocus on earned optimism - point out real capabilities while addressing actual problems.\n\n${formatEntriesForAI(entries)}`
        },
        {
            title: "Thematic Synthesizer",
            subtitle: "The bigger picture",
            type: "thematic",
            prompt: `Synthesize these entries into key themes:\n1. Core struggles or tensions\n2. Central questions or dilemmas\n3. How different aspects of their life connect\n\nProvide a cohesive narrative that ties everything together.\n\n${formatEntriesForAI(entries)}`
        }
    ];
    
    try {
        const results = await Promise.all(prompts.map(p => callAI(p.prompt)));
        
        const insights = {
            id: Date.now(),
            timestamp: new Date().toISOString().split('.')[0] + 'Z',
            entries: entries.map(e => e.date),
            analyses: prompts.map((p, i) => ({
                title: p.title,
                subtitle: p.subtitle,
                type: p.type,
                content: results[i]
            }))
        };
        
        // Save to Supabase
        await saveInsight(insights);
        
        state.insights = insights;
        state.insightsHistory.unshift(insights);
        
        openInsightsModal(insights);
        render();
        
    } catch (error) {
        alert('Error generating insights: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Generate Insights';
    }
}

function formatEntriesForAI(entries) {
    return entries.map((entry, i) => {
        const question = getQuestionDetails(entry.questionIndex);
        return `Entry ${i + 1} (${entry.date}):\nQuestion: ${question.text}\nAnswer: ${entry.answer}${entry.freeform ? `\nFreeform thoughts: ${entry.freeform}` : ''}`;
    }).join('\n\n---\n\n');
}

async function callAI(prompt) {
    const response = await fetch('https://calendar-journal-api.onrender.com/ask-ai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
    });
    
    if (!response.ok) {
        throw new Error('AI request failed');
    }
    
    const data = await response.json();
    return data.text;
}

// ============================================
// INSIGHTS DISPLAY
// ============================================

function openInsightsModal(insights) {
    const modal = document.getElementById('insightsModal');
    const grid = document.getElementById('insightsGrid');
    
    const icons = {
        evidence: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>',
        blindspot: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2"><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>',
        growth: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>',
        thematic: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"/></svg>'
    };
    
    const colors = {
        evidence: 'blue',
        blindspot: 'rose',
        growth: 'green',
        thematic: 'amber'
    };
    
    grid.innerHTML = insights.analyses.map(analysis => `
        <div class="insight-card">
            <div class="insight-header">
                <div class="insight-icon ${colors[analysis.type]}">
                    ${icons[analysis.type]}
                </div>
                <div class="insight-title-group">
                    <h3>${analysis.title}</h3>
                    <div class="insight-subtitle">${analysis.subtitle}</div>
                </div>
            </div>
            <div class="insight-text">${analysis.content}</div>
        </div>
    `).join('');
    
    modal.classList.add('visible');
    window.currentInsightId = insights.id;
}

function closeInsightsModal() {
    document.getElementById('insightsModal').classList.remove('visible');
}

async function deleteCurrentInsight() {
    if (!confirm('Delete this analysis? The entries will become available for re-analysis.')) {
        return;
    }
    
    const id = window.currentInsightId;
    
    // Delete from Supabase
    await deleteInsightFromDB(id);
    
    state.insightsHistory = state.insightsHistory.filter(i => i.id !== id);
    
    if (state.insights && state.insights.id === id) {
        state.insights = null;
    }
    
    closeInsightsModal();
    render();
}

function renderInsightsList() {
    const list = document.getElementById('insightsList');
    
    if (state.insightsHistory.length === 0) {
        list.innerHTML = '<div style="color: #6b6b6b; font-size: 14px; text-align: center;">No insights yet</div>';
        return;
    }
    
    list.innerHTML = state.insightsHistory.map(insight => {
        const dates = insight.entries.sort();
        const dateRange = dates.length > 0 ? `${dates[0]} to ${dates[dates.length - 1]}` : 'Unknown dates';
        
        return `
            <div class="insight-item" onclick='openInsightsModal(${JSON.stringify(insight).replace(/'/g, "&#39;")})'>
                <div class="insight-date-range">${dateRange}</div>
                <div class="insight-preview">${insight.analyses.length} perspectives</div>
            </div>
        `;
    }).join('');
}

// ============================================
// SIDEBAR
// ============================================

function toggleSidebar() {
    state.sidebarCollapsed = !state.sidebarCollapsed;
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('sidebarToggle');
    sidebar.classList.toggle('collapsed', state.sidebarCollapsed);
    toggle.classList.toggle('collapsed', state.sidebarCollapsed);
    toggle.textContent = state.sidebarCollapsed ? '◀' : '▶';
}

// ============================================
// PDF EXPORT
// ============================================

async function exportToPDF() {
    const validEntries = Object.entries(state.entries)
        .filter(([_, entry]) => isValidEntry(entry.answer))
        .map(([date, entry]) => ({ date, ...entry }));
    
    if (validEntries.length < 7) {
        alert('You need at least 7 completed entries to export.');
        return;
    }
    
    const btn = document.querySelector('.export-pdf-btn');
    btn.disabled = true;
    btn.textContent = 'Generating PDF...';
    
    try {
        const response = await fetch('https://calendar-journal-api.onrender.com/export-prompt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ entries: validEntries.slice(0, 7) })
        });
        
        if (!response.ok) throw new Error('Export failed');
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'journal-prompts.pdf';
        a.click();
        
    } catch (error) {
        alert('Error exporting PDF: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Export Prompts (PDF)';
    }
}
