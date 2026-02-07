// ============================================
// QUESTIONS AND HINTS
// ============================================

const PAST_QUESTIONS = [
    "What's a childhood memory that still influences how you see yourself today?",
    "Describe a time when you felt you didn't fit in. How did you handle it?",
    "What's a mistake from your past that taught you something valuable?",
    "Who from your past do you wish you could talk to now, and what would you say?",
    "What's something you used to believe strongly but have changed your mind about?",
    "Describe a moment when you felt truly proud of yourself.",
    "What's a risk you took that didn't work out, and what did you learn?",
    "Who was a mentor or role model in your life? What did they teach you?",
    "What's a pattern in your past relationships (romantic, friendship, or family)?",
    "Describe a time when you stood up for yourself or someone else.",
    "What's something from your past you've been avoiding thinking about?",
    "What's a skill or strength you developed through a difficult experience?",
    "Describe your relationship with failure as you were growing up.",
    "What's a family tradition or cultural practice that shaped who you are?",
    "What's something you accomplished that others might not know about?",
    "Describe a turning point in your life. What led to it?",
    "What's a belief your family held that you've questioned or rejected?",
    "What's the hardest thing you've ever had to forgive?",
    "Describe a time when you felt completely understood by someone.",
    "What's something from your past that you're grateful didn't work out the way you wanted?"
];

const PRESENT_QUESTIONS = [
    "What's draining your energy right now, and what's giving you energy?",
    "Describe your current daily routine. What would you change about it?",
    "What are you avoiding dealing with right now?",
    "What's a boundary you need to set but haven't yet?",
    "How are you really feeling today, beyond 'fine' or 'okay'?",
    "What's something you're doing that doesn't align with your values?",
    "Describe your current relationships. Which ones feel healthy? Which don't?",
    "What's taking up too much mental space right now?",
    "What do you need more of in your life right now?",
    "What are you tolerating that you shouldn't be?",
    "How do you handle stress currently? Is it working?",
    "What's something you know you should do but keep putting off?",
    "Describe how you spend your free time. Does it reflect who you want to be?",
    "What's your relationship with your phone/social media like right now?",
    "What's a small change you could make this week that would improve your life?",
    "Who do you need to have a difficult conversation with?",
    "What are you pretending not to know about your current situation?",
    "What's your body trying to tell you right now?",
    "What would someone who loves you want you to know about your current situation?",
    "What's one thing you're doing well right now that you don't give yourself credit for?"
];

const FUTURE_QUESTIONS = [
    "Where do you want to be in 5 years, and what's one step toward that?",
    "What skills do you want to develop in the next year?",
    "Describe your ideal day 5 years from now.",
    "What relationship patterns do you want to break going forward?",
    "What do you want your life to look like when you're 80?",
    "What's a goal you've been afraid to set?",
    "If you could master one thing, what would it be and why?",
    "What do you want to be known for?",
    "What would you do if you knew you couldn't fail?",
    "What's a fear you want to overcome in the next year?",
    "Describe the person you want to become.",
    "What's one habit you want to build in the next month?",
    "What legacy do you want to leave behind?",
    "What would you regret not doing if you looked back on your life?",
    "What's a conversation you want to have in the future that you're not ready for now?",
    "How do you want to handle challenges differently going forward?",
    "What's something you want to learn just for the joy of it?",
    "What kind of friend/partner/family member do you want to be?",
    "What's a vision you have that you haven't shared with anyone?",
    "What does success look like for you, really?"
];

const HINTS = [
    "Think about sights, sounds, smells. What were you wearing? Who was there?",
    "Consider: Where was this? What grade were you in? What did you do to cope?",
    "What specifically went wrong? How did you respond? What would you tell your past self?",
    "This could be someone living or deceased. What questions do you have for them?",
    "What made you believe it then? What changed your perspective?",
    "What did you accomplish? Who was there? How did it feel in your body?",
    "What was the risk? Why did you take it? What specifically did you learn?",
    "How did you meet them? What's a specific thing they said or did that stuck with you?",
    "Do you tend to avoid conflict? Rush into things? Have similar arguments?",
    "What was at stake? What gave you the courage? What happened after?",
    "Why have you been avoiding it? What might happen if you examined it now?",
    "What was the difficulty? What did you have to do? How do you use this skill now?",
    "Did you take risks? Did you fear it? How did adults around you respond to failure?",
    "When did you participate in it? How did it make you feel? Do you continue it now?",
    "Why haven't you shared it? What obstacles did you overcome? What does it mean to you?",
    "What were you doing before? What happened? How are you different now?",
    "What was the belief? When did you first question it? What do you believe instead?",
    "What did they do? How long did it take? What does forgiveness mean to you?",
    "Who was it? What did they understand? How did you know they understood?",
    "What did you want? What happened instead? Why are you grateful now?",
    "List specific activities, people, or situations for each category.",
    "Walk through morning, afternoon, evening. Be specific. What's the impact of your routine?",
    "Be honest. What would happen if you addressed it? What's the cost of avoiding it?",
    "With whom? About what? What makes it hard? What would setting it look like?",
    "Go deeper. What emotions? Where in your body? What's underneath the surface feeling?",
    "Be specific. What's the behavior? What value does it violate? Why do you continue?",
    "Name specific people. What makes each healthy/unhealthy? What patterns do you notice?",
    "What thoughts loop? What problem? What person? Why is it taking up this space?",
    "Less of what? More time? Peace? Support? Connection? Challenge? Be specific.",
    "What behavior? Situation? Person? Treatment? Why are you tolerating it?",
    "List your methods. What works? What makes it worse? What would ideal look like?",
    "What is it? Why haven't you done it? What's one tiny step you could take?",
    "How many hours on what? Does it match your values? What would you change?",
    "How many hours? First/last thing? During meals? What's the impact?",
    "Make it concrete and actionable. What's stopping you from making it?",
    "What needs to be said? What are you afraid of? What's the cost of not having it?",
    "Complete this sentence: 'I know that [blank] but I'm pretending I don't.'",
    "Tension? Pain? Fatigue? Energy? What have you been ignoring?",
    "What would they notice? What would they say? Can you say it to yourself?",
    "Be specific. What exactly? Why don't you acknowledge it? What would happen if you did?",
    "Be specific. What's step one? What skills do you need? Who could help?",
    "Choose one skill. Why this one? What would having it enable you to do?",
    "What time do you wake up? What do you do? Who's around? How do you feel?",
    "What do you repeat? With whom? How does it serve you? What would breaking it look like?",
    "Where are you living? Doing? Who's around? How do you spend your time?",
    "Why haven't you set it? Make it specific. Ambitious but believable. Why does it matter?",
    "What is it? Why? What's the smallest step toward mastery?",
    "By whom? For what? What does that require you to do/be?",
    "Be specific. Make it concrete. Why this? What would it change?",
    "Name it. What does overcoming it look like? What would be different?",
    "What qualities? Values? Habits? How are you different from who you are now?",
    "One habit. Make it small and specific. Why this one? How will you track it?",
    "What impact? What will people remember? What do you want to pass on?",
    "What is it? Why would you regret it? What's stopping you now?",
    "With whom? About what? What needs to happen before you're ready?",
    "What pattern? What trigger? What do you do now? What will you do instead?",
    "What calls to you? No career reasons. Just curiosity. Why this?",
    "What specific behaviors? What do you need to stop? Start? Continue?",
    "What is it? Why haven't you shared it? What would pursuing it require?",
    "Define it for yourself, not society's definition. What does it look like?"
];

// ============================================
// QUESTION UTILITY FUNCTIONS
// ============================================

function getQuestionForDate(date) {
    const dayOfYear = Math.floor((date - new Date(date.getFullYear(), 0, 0)) / 1000 / 60 / 60 / 24);
    const totalQuestions = PAST_QUESTIONS.length + PRESENT_QUESTIONS.length + FUTURE_QUESTIONS.length;
    const index = dayOfYear % totalQuestions;
    return index;
}

function getQuestionDetails(index) {
    const pastLen = PAST_QUESTIONS.length;
    const presentLen = PRESENT_QUESTIONS.length;
    
    if (index < pastLen) {
        return { category: 'PAST', text: PAST_QUESTIONS[index], hint: HINTS[index] };
    } else if (index < pastLen + presentLen) {
        return { category: 'PRESENT', text: PRESENT_QUESTIONS[index - pastLen], hint: HINTS[index] };
    } else {
        return { category: 'FUTURE', text: FUTURE_QUESTIONS[index - pastLen - presentLen], hint: HINTS[index] };
    }
}
