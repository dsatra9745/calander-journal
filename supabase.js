// ============================================
// SUPABASE INITIALIZATION
// ============================================
console.log('VERSION: SPLIT-FILES-2026-02-07');

const SUPABASE_URL = 'https://umegwazczyzgpqptestt.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_zZXXP8ASqOZMXNWXAswPWw_onXwMUqz';
const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

let currentUser = null;

// ============================================
// AUTH FUNCTIONS
// ============================================
async function initAuth() {
    const { data: { session } } = await supabaseClient.auth.getSession();
    
    if (session) {
        currentUser = session.user;
        showApp();
        await loadUserData();
    } else {
        showAuth();
    }
}

function showAuth() {
    document.getElementById('auth-screen').style.display = 'flex';
    document.getElementById('app-screen').style.display = 'none';
}

function showApp() {
    document.getElementById('auth-screen').style.display = 'none';
    document.getElementById('app-screen').style.display = 'block';
    render();
    checkOnboarding();
}

function setupAuthListeners() {
    let isSignUpMode = false;
    
    document.getElementById('auth-toggle-btn').addEventListener('click', () => {
        isSignUpMode = !isSignUpMode;
        const submitBtn = document.getElementById('auth-submit');
        const toggleText = document.getElementById('auth-toggle-text');
        const toggleBtn = document.getElementById('auth-toggle-btn');
        
        if (isSignUpMode) {
            submitBtn.textContent = 'Sign Up';
            toggleText.textContent = 'Already have an account?';
            toggleBtn.textContent = 'Sign In';
        } else {
            submitBtn.textContent = 'Sign In';
            toggleText.textContent = "Don't have an account?";
            toggleBtn.textContent = 'Sign Up';
        }
        
        clearAuthMessage();
    });
    
    document.getElementById('forgot-password-btn').addEventListener('click', async () => {
        const email = document.getElementById('auth-email').value;
        
        if (!email) {
            showAuthMessage('Please enter your email address first.', 'error');
            return;
        }
        
        try {
            const { error } = await supabaseClient.auth.resetPasswordForEmail(email, {
                redirectTo: window.location.origin
            });
            
            if (error) throw error;
            
            showAuthMessage('Password reset email sent! Check your inbox.', 'success');
        } catch (error) {
            showAuthMessage(error.message, 'error');
        }
    });
    
    document.getElementById('auth-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('auth-email').value;
        const password = document.getElementById('auth-password').value;
        const submitBtn = document.getElementById('auth-submit');
        
        submitBtn.disabled = true;
        submitBtn.textContent = 'Loading...';
        
        try {
            if (isSignUpMode) {
                const { data, error } = await supabaseClient.auth.signUp({
                    email,
                    password,
                });
                
                if (error) throw error;
                
                showAuthMessage('Check your email to confirm your account!', 'success');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Sign Up';
            } else {
                const { data, error } = await supabaseClient.auth.signInWithPassword({
                    email,
                    password,
                });
                
                if (error) throw error;
                
                currentUser = data.user;
                showApp();
                await loadUserData();
            }
        } catch (error) {
            showAuthMessage(error.message, 'error');
            submitBtn.disabled = false;
            submitBtn.textContent = isSignUpMode ? 'Sign Up' : 'Sign In';
        }
    });
}

function showAuthMessage(message, type) {
    const messageDiv = document.getElementById('auth-message');
    messageDiv.textContent = message;
    messageDiv.className = `auth-message ${type}`;
    messageDiv.style.display = 'block';
}

function clearAuthMessage() {
    const messageDiv = document.getElementById('auth-message');
    messageDiv.style.display = 'none';
}

async function handleLogout() {
    await supabaseClient.auth.signOut();
    currentUser = null;
    state = createInitialState();
    showAuth();
}

// ============================================
// DATABASE FUNCTIONS
// ============================================
async function loadUserData() {
    if (!currentUser) return;
    
    try {
        const { data, error } = await supabaseClient
            .from('journal_entries')
            .select('*')
            .eq('user_id', currentUser.id);
        
        if (error) throw error;
        
        // Convert Supabase data to state.entries format
        state.entries = {};
        data.forEach(entry => {
            state.entries[entry.date] = {
                questionIndex: entry.question_index,
                answer: entry.answer,
                freeform: entry.freeform || '',
                imageUrl: entry.image_url || null
            };
        });
        
        // Load insights
        await loadInsights();
        
        render();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

async function saveEntry(date, entryData) {
    if (!currentUser) return;
    
    try {
        const { data, error } = await supabaseClient
            .from('journal_entries')
            .upsert({
                user_id: currentUser.id,
                date: date,
                question_index: entryData.questionIndex,
                answer: entryData.answer,
                freeform: entryData.freeform || '',
                image_url: entryData.imageUrl || null
            }, {
                onConflict: 'user_id,date'
            });
        
        if (error) throw error;
        
    } catch (error) {
        console.error('Error saving entry:', error);
    }
}

async function saveInsight(insight) {
    if (!currentUser) return;
    
    try {
        const { data, error } = await supabaseClient
            .from('insights')
            .insert({
                user_id: currentUser.id,
                timestamp: insight.timestamp,
                entries: insight.entries,
                analyses: insight.analyses
            });
        
        if (error) throw error;
        
        return data;
    } catch (error) {
        console.error('Error saving insight:', error);
    }
}

async function loadInsights() {
    if (!currentUser) return;
    
    try {
        const { data, error } = await supabaseClient
            .from('insights')
            .select('*')
            .eq('user_id', currentUser.id)
            .order('timestamp', { ascending: false });
        
        if (error) throw error;
        
        state.insightsHistory = data.map(row => ({
            id: row.id,
            timestamp: row.timestamp,
            entries: row.entries,
            analyses: row.analyses
        }));
        
        render();
    } catch (error) {
        console.error('Error loading insights:', error);
    }
}

async function deleteInsightFromDB(insightId) {
    if (!currentUser) return;
    
    try {
        const { error } = await supabaseClient
            .from('insights')
            .delete()
            .eq('id', insightId)
            .eq('user_id', currentUser.id);
        
        if (error) throw error;
    } catch (error) {
        console.error('Error deleting insight:', error);
    }
}
