// ============================================
// CALENDAR RENDERING
// ============================================

function renderCalendar() {
    const calendar = document.getElementById('calendar');
    const monthTitle = document.getElementById('monthTitle');
    
    const date = new Date(state.currentYear, state.currentMonth, 1);
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December'];
    
    monthTitle.textContent = `${monthNames[state.currentMonth]} ${state.currentYear}`;
    
    const firstDay = date.getDay();
    const daysInMonth = new Date(state.currentYear, state.currentMonth + 1, 0).getDate();
    const daysInPrevMonth = new Date(state.currentYear, state.currentMonth, 0).getDate();
    
    let html = '';
    
    // Day headers
    const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    dayHeaders.forEach(day => {
        html += `<div class="day-header">${day}</div>`;
    });
    
    // Previous month days
    for (let i = firstDay - 1; i >= 0; i--) {
        const day = daysInPrevMonth - i;
        html += `<div class="day-cell other-month"><div class="day-number">${day}</div></div>`;
    }
    
    // Current month days
    const today = new Date();
    const isCurrentMonth = state.currentMonth === today.getMonth() && state.currentYear === today.getFullYear();
    
    for (let day = 1; day <= daysInMonth; day++) {
        const dateStr = `${state.currentYear}-${String(state.currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const entry = state.entries[dateStr];
        const isToday = isCurrentMonth && day === today.getDate();
        
        let classes = 'day-cell';
        if (isToday) classes += ' today';
        if (entry && isValidEntry(entry.answer)) classes += ' completed';
        
        const hasIndicator = entry && isValidEntry(entry.answer);
        
        html += `
            <div class="${classes}" onclick="openJournal('${dateStr}')">
                <div class="day-number">${day}</div>
                ${hasIndicator ? '<div class="day-indicator">✓</div>' : ''}
            </div>
        `;
    }
    
    // Next month days
    const totalCells = firstDay + daysInMonth;
    const remainingCells = totalCells % 7 === 0 ? 0 : 7 - (totalCells % 7);
    for (let day = 1; day <= remainingCells; day++) {
        html += `<div class="day-cell other-month"><div class="day-number">${day}</div></div>`;
    }
    
    calendar.innerHTML = html;
}

function changeMonth(delta) {
    if (delta === 0) {
        const today = new Date();
        state.currentMonth = today.getMonth();
        state.currentYear = today.getFullYear();
    } else {
        state.currentMonth += delta;
        if (state.currentMonth > 11) {
            state.currentMonth = 0;
            state.currentYear++;
        } else if (state.currentMonth < 0) {
            state.currentMonth = 11;
            state.currentYear--;
        }
    }
    render();
}
