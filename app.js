// ============================================
// STATE MANAGEMENT
// ============================================

function createInitialState() {
    return {
        currentMonth: new Date().getMonth(),
        currentYear: new Date().getFullYear(),
        entries: {},
        currentDate: null,
        insights: null,
        insightsHistory: [],
        sidebarCollapsed: false,
        monthBackgrounds: {},
        apiKey: 'sk-ant-api03-YOUR-KEY-HERE'
    };
}

let state = createInitialState();

// ============================================
// MAIN RENDER FUNCTION
// ============================================

function render() {
    renderCalendar();
    renderInsightsList();
    updateGenerateButton();
}

// ============================================
// ONBOARDING
// ============================================

function checkOnboarding() {
    const hasSeenOnboarding = localStorage.getItem('hasSeenOnboarding');
    if (!hasSeenOnboarding) {
        document.getElementById('onboardingModal').classList.add('visible');
    }
}

function closeOnboarding() {
    localStorage.setItem('hasSeenOnboarding', 'true');
    document.getElementById('onboardingModal').classList.remove('visible');
}

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    setupAuthListeners();
    initAuth();
});
