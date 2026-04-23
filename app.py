import streamlit as st
from core.pdf_parser import extract_text_from_pdf

st.set_page_config(
    page_title="HireReady AI",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── GLOBAL STYLES ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600&family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400&display=swap');

/* ── ROOT & BACKGROUND ── */
:root {
    --glass: rgba(255,255,255,0.04);
    --glass-border: rgba(255,255,255,0.08);
    --glass-hover: rgba(255,255,255,0.07);
    --accent: #a78bfa;
    --accent2: #60a5fa;
    --accent3: #34d399;
    --glow: rgba(167,139,250,0.15);
    --text-primary: rgba(255,255,255,0.92);
    --text-secondary: rgba(255,255,255,0.45);
    --text-tertiary: rgba(255,255,255,0.25);
}

/* Full dark background with animated gradient orbs */
.stApp {
    background: #080808 !important;
    font-family: 'Syne', sans-serif !important;
}

/* Animated background orbs */
.stApp::before {
    content: '';
    position: fixed;
    top: -30%;
    left: -20%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(167,139,250,0.12) 0%, transparent 70%);
    border-radius: 50%;
    animation: orbFloat 8s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

.stApp::after {
    content: '';
    position: fixed;
    bottom: -20%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(96,165,250,0.1) 0%, transparent 70%);
    border-radius: 50%;
    animation: orbFloat 10s ease-in-out infinite reverse;
    pointer-events: none;
    z-index: 0;
}

@keyframes orbFloat {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(30px, -30px) scale(1.05); }
    66% { transform: translate(-20px, 20px) scale(0.95); }
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: rgba(10,10,10,0.95) !important;
    border-right: 1px solid var(--glass-border) !important;
    backdrop-filter: blur(40px) !important;
}

[data-testid="stSidebar"] > div {
    padding: 2rem 1.5rem !important;
}

/* ── TYPOGRAPHY ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.03em !important;
}

p, span, div, label {
    font-family: 'Syne', sans-serif !important;
    color: var(--text-secondary) !important;
}

/* ── GLASS CARD ── */
.glass-card {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 1.5rem;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
}

.glass-card:hover {
    background: var(--glass-hover);
    border-color: rgba(167,139,250,0.2);
    transform: translateY(-2px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 30px rgba(167,139,250,0.05);
}

/* ── LOGO ── */
.logo-container {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 2rem;
}

.logo-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: 0 0 20px rgba(167,139,250,0.4);
}

.logo-text {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em !important;
}

.logo-sub {
    font-size: 0.65rem !important;
    color: var(--text-tertiary) !important;
    font-weight: 400 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* ── METRIC CARDS ── */
.metric-card {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    opacity: 0.6;
}

.metric-number {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}

.metric-label {
    font-size: 0.65rem;
    color: var(--text-tertiary);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}

/* ── SKILL PILLS ── */
.skill-pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 500;
    margin: 3px;
    letter-spacing: 0.02em;
    font-family: 'JetBrains Mono', monospace;
}

.skill-have {
    background: rgba(52,211,153,0.1);
    border: 1px solid rgba(52,211,153,0.25);
    color: #34d399;
}

.skill-missing {
    background: rgba(251,113,133,0.1);
    border: 1px solid rgba(251,113,133,0.25);
    color: #fb7185;
}

/* ── SCORE RING ── */
.score-ring-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1rem;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(167,139,250,0.15), rgba(96,165,250,0.15)) !important;
    border: 1px solid rgba(167,139,250,0.3) !important;
    color: var(--text-primary) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(10px) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(167,139,250,0.25), rgba(96,165,250,0.25)) !important;
    border-color: rgba(167,139,250,0.5) !important;
    box-shadow: 0 0 20px rgba(167,139,250,0.2) !important;
    transform: translateY(-1px) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #a78bfa, #60a5fa) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 0 30px rgba(167,139,250,0.3) !important;
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 40px rgba(167,139,250,0.5) !important;
    transform: translateY(-2px) !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: var(--glass) !important;
    border: 1px dashed rgba(167,139,250,0.3) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    transition: all 0.3s ease !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(167,139,250,0.5) !important;
    background: rgba(167,139,250,0.05) !important;
}

/* ── TEXT AREA ── */
.stTextArea textarea {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    transition: all 0.3s ease !important;
}

.stTextArea textarea:focus {
    border-color: rgba(167,139,250,0.4) !important;
    box-shadow: 0 0 0 2px rgba(167,139,250,0.1) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--glass) !important;
    border-radius: 14px !important;
    padding: 4px !important;
    border: 1px solid var(--glass-border) !important;
    gap: 2px !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    border-radius: 10px !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    padding: 0.5rem 1rem !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(167,139,250,0.2), rgba(96,165,250,0.2)) !important;
    color: var(--text-primary) !important;
    border: 1px solid rgba(167,139,250,0.25) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.8rem !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}

.streamlit-expanderContent {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid var(--glass-border) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
}

/* ── ALERTS ── */
.stSuccess {
    background: rgba(52,211,153,0.08) !important;
    border: 1px solid rgba(52,211,153,0.2) !important;
    border-radius: 12px !important;
    color: #34d399 !important;
}

.stWarning {
    background: rgba(251,191,36,0.08) !important;
    border: 1px solid rgba(251,191,36,0.2) !important;
    border-radius: 12px !important;
    color: #fbbf24 !important;
}

.stInfo {
    background: rgba(96,165,250,0.08) !important;
    border: 1px solid rgba(96,165,250,0.2) !important;
    border-radius: 12px !important;
    color: #60a5fa !important;
}

.stError {
    background: rgba(251,113,133,0.08) !important;
    border: 1px solid rgba(251,113,133,0.2) !important;
    border-radius: 12px !important;
    color: #fb7185 !important;
}

/* ── PROGRESS BAR ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #a78bfa, #60a5fa) !important;
    border-radius: 100px !important;
}

.stProgress > div {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 100px !important;
}

/* ── DIVIDER ── */
hr {
    border-color: var(--glass-border) !important;
    margin: 1.5rem 0 !important;
}

/* ── SPINNER ── */
.stSpinner > div {
    border-top-color: #a78bfa !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.3); border-radius: 100px; }
::-webkit-scrollbar-thumb:hover { background: rgba(167,139,250,0.5); }

/* ── HIDE STREAMLIT DEFAULTS ── */
#MainMenu { visibility: hidden; }
/* Force sidebar always visible, hide collapse button */
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }
[data-testid="stLogoSpacer"] { display: none !important; }
div[class*="stLogoSpacer"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
section[data-testid="stSidebar"] { 
    min-width: 320px !important; 
    width: 320px !important;
    transform: none !important;
    left: 0 !important;
    visibility: visible !important;
    display: block !important;
}
section[data-testid="stSidebar"] > div {
    width: 320px !important;
}
[data-testid="collapsedControl"] { display: none !important; }
/* Hide keyboard shortcut tooltip */
.stActionButton { display: none !important; }
/* Remove keyboard text from expanders and interactive elements */
.st-emotion-cache-ujm5ma { display: none !important; }
.st-emotion-cache-pkm19r { display: none !important; }
span[data-testid="stIconMaterial"] { display: none !important; }
button[data-testid="baseButton-headerNoPadding"] { display: none !important; }
iframe[title="keyboard_shortcut"] { display: none !important; }
div[class*="keyboard"] { display: none !important; }
button[aria-label*="keyboard"] { display: none !important; }
button[aria-label*="shortcuts"] { display: none !important; }
.st-emotion-cache-czk5ss { display: none !important; }
.st-emotion-cache-1dp5vir { display: none !important; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)
# Kill the keyboard shortcut floating element
st.iframe("""
<script>
function removeKeyboardOverlay() {
    // Find and remove any element containing 'keyboard' text
    const allElements = document.querySelectorAll('*');
    allElements.forEach(el => {
        if (el.children.length === 0 && 
            el.textContent.trim().toLowerCase().includes('keyboard')) {
            el.style.display = 'none';
        }
    });
    
    // Also hide the stLogoSpacer area
    const spacers = document.querySelectorAll('[data-testid="stLogoSpacer"]');
    spacers.forEach(el => el.style.display = 'none');
    
    // Hide header area
    const headers = document.querySelectorAll('header');
    headers.forEach(el => el.style.display = 'none');
}

// Run immediately
removeKeyboardOverlay();

// Run again after page loads fully
setTimeout(removeKeyboardOverlay, 500);
setTimeout(removeKeyboardOverlay, 1500);
setTimeout(removeKeyboardOverlay, 3000);
</script>
""", height=0)

# ── SESSION STATE ─────────────────────────────────────────────────
defaults = {
    "resume_text": None,
    "jd_text": "",
    "analysis_result": None,
    "questions": None,
    "bullet_rewrites": {},
    "extracted_bullets": [],
    "simulator_stage": "setup",
    "simulator_role": None,
    "simulator_questions": [],
    "simulator_current_index": 0,
    "simulator_answers": [],
    "simulator_evaluations": [],
    "simulator_report": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='logo-container'>
        <div class='logo-icon'><svg width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='3'/><path d='M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83'/></svg></div>
        <div>
            <div class='logo-text'>HireReady AI</div>
            <div class='logo-sub'>Job Readiness Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='font-size:0.65rem; color:rgba(255,255,255,0.2); text-transform:uppercase;
    letter-spacing:0.1em; margin-bottom:0.5rem;'>Resume</div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        extracted = extract_text_from_pdf(uploaded_file)
        if extracted:
            st.session_state.resume_text = extracted
            st.markdown("""
            <div style='display:flex;align-items:center;gap:8px;padding:8px 12px;
            background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.2);
            border-radius:10px;margin-top:8px;'>
            <span style='color:#34d399;font-size:0.7rem;'>Resume loaded</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Could not read PDF.")

    st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='font-size:0.65rem; color:rgba(255,255,255,0.2); text-transform:uppercase;
    letter-spacing:0.1em; margin-bottom:0.5rem;'>Job Description</div>
    """, unsafe_allow_html=True)

    st.session_state.jd_text = st.text_area(
        "JD",
        value=st.session_state.jd_text,
        height=180,
        placeholder="Paste job description...",
        label_visibility="collapsed"
    )

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    analyse_button = st.button("Analyse Now", use_container_width=True, type="primary")

    # Status indicators
    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.65rem; color:rgba(255,255,255,0.2); text-transform:uppercase;
    letter-spacing:0.1em; margin-bottom:0.8rem;'>Status</div>
    """, unsafe_allow_html=True)

    resume_status = "● Loaded" if st.session_state.resume_text else "○ Waiting"
    resume_color = "#34d399" if st.session_state.resume_text else "rgba(255,255,255,0.2)"
    jd_status = "● Ready" if st.session_state.jd_text.strip() else "○ Waiting"
    jd_color = "#34d399" if st.session_state.jd_text.strip() else "rgba(255,255,255,0.2)"
    analysis_status = "● Done" if st.session_state.analysis_result else "○ Pending"
    analysis_color = "#34d399" if st.session_state.analysis_result else "rgba(255,255,255,0.2)"

    st.markdown(f"""
    <div style='display:flex;flex-direction:column;gap:8px;'>
        <div style='display:flex;justify-content:space-between;align-items:center;'>
            <span style='font-size:0.7rem;color:rgba(255,255,255,0.3);'>Resume</span>
            <span style='font-size:0.7rem;color:{resume_color};font-family:monospace;'>{resume_status}</span>
        </div>
        <div style='display:flex;justify-content:space-between;align-items:center;'>
            <span style='font-size:0.7rem;color:rgba(255,255,255,0.3);'>Job Description</span>
            <span style='font-size:0.7rem;color:{jd_color};font-family:monospace;'>{jd_status}</span>
        </div>
        <div style='display:flex;justify-content:space-between;align-items:center;'>
            <span style='font-size:0.7rem;color:rgba(255,255,255,0.3);'>Analysis</span>
            <span style='font-size:0.7rem;color:{analysis_color};font-family:monospace;'>{analysis_status}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── MAIN TABS ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  Analysis  ",
    "  Predictor  ",
    "  Batch  ",
    "  Interview  "
])

# ══════════════════════════════════════════════════════════════════
# TAB 1 — RESUME ANALYSIS
# ══════════════════════════════════════════════════════════════════
with tab1:
    if analyse_button:
        if not st.session_state.resume_text:
            st.error("Upload your resume PDF first.")
        elif not st.session_state.jd_text.strip():
            st.error("Paste a job description first.")
        else:
            from features.resume_analyzer import analyse_resume
            from features.bullet_rewriter import extract_bullets

            with st.spinner("Running AI analysis..."):
                result = analyse_resume(st.session_state.resume_text, st.session_state.jd_text)

            if result:
                st.session_state.analysis_result = result
                st.session_state.extracted_bullets = extract_bullets(st.session_state.resume_text)
            else:
                st.error("Analysis failed. Try again.")

    if st.session_state.analysis_result:
        from utils.formatters import display_skills, display_bullet_rewrite
        from features.bullet_rewriter import rewrite_bullet

        r = st.session_state.analysis_result
        score = r["match_score"]

        # Determine glow color based on score
        if score >= 70:
            glow_color = "rgba(52,211,153,0.3)"
            score_color = "#34d399"
        elif score >= 50:
            glow_color = "rgba(251,191,36,0.3)"
            score_color = "#fbbf24"
        else:
            glow_color = "rgba(251,113,133,0.3)"
            score_color = "#fb7185"

        # Hero score section
        st.markdown(f"""
        <div style='text-align:center;padding:3rem 1rem 2rem;'>
            <div style='font-size:0.65rem;color:rgba(255,255,255,0.25);text-transform:uppercase;
            letter-spacing:0.15em;margin-bottom:1rem;'>Match Score</div>
            <div style='font-size:5.5rem;font-weight:800;font-family:Syne,sans-serif;
            background:linear-gradient(135deg,{score_color},rgba(255,255,255,0.7));
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;line-height:1;
            filter:drop-shadow(0 0 30px {glow_color});'>{score}</div>
            <div style='font-size:0.8rem;color:rgba(255,255,255,0.3);margin-top:0.3rem;'>out of 100</div>
        </div>
        """, unsafe_allow_html=True)

        # Recommendation badge
        rec = r["hiring_recommendation"]
        rec_colors = {
            "Strong Yes": ("#34d399", "rgba(52,211,153,0.12)", "rgba(52,211,153,0.25)"),
            "Yes": ("#34d399", "rgba(52,211,153,0.08)", "rgba(52,211,153,0.2)"),
            "Maybe": ("#fbbf24", "rgba(251,191,36,0.08)", "rgba(251,191,36,0.2)"),
            "No": ("#fb7185", "rgba(251,113,133,0.08)", "rgba(251,113,133,0.2)")
        }
        rc, rbg, rborder = rec_colors.get(rec, ("#fff", "rgba(255,255,255,0.05)", "rgba(255,255,255,0.1)"))

        st.markdown(f"""
        <div style='text-align:center;margin-bottom:2rem;'>
            <span style='background:{rbg};border:1px solid {rborder};color:{rc};
            padding:6px 20px;border-radius:100px;font-size:0.75rem;font-weight:600;
            letter-spacing:0.05em;font-family:Syne,sans-serif;'>{rec}</span>
            <div style='color:rgba(255,255,255,0.3);font-size:0.72rem;margin-top:0.8rem;
            font-style:italic;'>{r["recommendation_reason"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # Three metric cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-number'>{score}</div>
                <div class='metric-label'>Match Score</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-number' style='font-size:1.5rem;'>{r["experience_match"]}</div>
                <div class='metric-label'>Experience</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-number' style='font-size:1.5rem;'>{r["education_match"]}</div>
                <div class='metric-label'>Education</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin:2rem 0;'></div>", unsafe_allow_html=True)

        # Skills section
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class='glass-card'>
                <div style='font-size:0.65rem;color:rgba(255,255,255,0.25);text-transform:uppercase;
                letter-spacing:0.1em;margin-bottom:1rem;'>Skills You Have</div>
            """, unsafe_allow_html=True)
            if r["matched_skills"]:
                pills = "".join([f"<span class='skill-pill skill-have'>{s}</span>" for s in r["matched_skills"]])
                st.markdown(f"<div>{pills}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:rgba(255,255,255,0.2);font-size:0.75rem;'>None found</p></div>", unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class='glass-card'>
                <div style='font-size:0.65rem;color:rgba(255,255,255,0.25);text-transform:uppercase;
                letter-spacing:0.1em;margin-bottom:1rem;'>Skills to Learn</div>
            """, unsafe_allow_html=True)
            if r["missing_skills"]:
                pills = "".join([f"<span class='skill-pill skill-missing'>{s}</span>" for s in r["missing_skills"]])
                st.markdown(f"<div>{pills}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:rgba(255,255,255,0.2);font-size:0.75rem;'>None missing</p></div>", unsafe_allow_html=True)

        # Feedback
        st.markdown("<div style='margin:1.5rem 0;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='glass-card'>
            <div style='font-size:0.65rem;color:rgba(255,255,255,0.25);text-transform:uppercase;
            letter-spacing:0.1em;margin-bottom:0.8rem;'>AI Feedback</div>
            <p style='color:rgba(255,255,255,0.6);font-size:0.82rem;line-height:1.7;margin:0;'>{r["overall_feedback"]}</p>
        </div>
        """, unsafe_allow_html=True)

        # Bullet rewriter
        st.markdown("<div style='margin:2rem 0 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:0.65rem;color:rgba(255,255,255,0.25);text-transform:uppercase;
        letter-spacing:0.1em;margin-bottom:1rem;'>Bullet Rewriter</div>
        """, unsafe_allow_html=True)

        bullets = st.session_state.extracted_bullets
        if not bullets:
            st.markdown("<p style='color:rgba(255,255,255,0.2);font-size:0.75rem;'>No bullets detected in your resume.</p>", unsafe_allow_html=True)
        else:
            for i, bullet in enumerate(bullets):
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
                    border-radius:10px;padding:10px 14px;font-size:0.78rem;
                    color:rgba(255,255,255,0.5);font-family:JetBrains Mono,monospace;'>
                    {bullet}</div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("Rewrite", key=f"rewrite_{i}"):
                        with st.spinner("Rewriting..."):
                            res = rewrite_bullet(bullet, st.session_state.jd_text)
                        if res:
                            st.session_state.bullet_rewrites[i] = res

                if i in st.session_state.bullet_rewrites:
                    rw = st.session_state.bullet_rewrites[i]
                    st.markdown(f"""
                    <div style='background:rgba(52,211,153,0.05);border:1px solid rgba(52,211,153,0.15);
                    border-radius:10px;padding:12px 16px;margin-top:6px;margin-bottom:12px;'>
                        <div style='font-size:0.6rem;color:rgba(52,211,153,0.5);text-transform:uppercase;
                        letter-spacing:0.1em;margin-bottom:6px;'>Rewritten</div>
                        <div style='font-size:0.8rem;color:rgba(255,255,255,0.75);
                        font-family:JetBrains Mono,monospace;line-height:1.6;'>{rw.get("rewritten","")}</div>
                    </div>
                    """, unsafe_allow_html=True)

    else:
        # Empty state
        st.markdown("""
        <div style='text-align:center;padding:5rem 2rem;'>
            <div style='font-size:3rem;margin-bottom:1.5rem;opacity:0.2;font-family:monospace;font-size:2rem;'>[ ]</div>
            <div style='font-size:0.85rem;color:rgba(255,255,255,0.2);font-weight:500;
            letter-spacing:0.02em;'>Upload your resume and paste a job description</div>
            <div style='font-size:0.72rem;color:rgba(255,255,255,0.12);margin-top:0.5rem;'>
            then click Analyse Now in the sidebar</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 2 — INTERVIEW PREDICTOR
# ══════════════════════════════════════════════════════════════════
with tab2:
    if not st.session_state.analysis_result:
        st.markdown("""
        <div style='text-align:center;padding:5rem 2rem;'>
            <div style='font-size:3rem;margin-bottom:1.5rem;opacity:0.2;font-family:monospace;font-size:2rem;'>[ ]</div>
            <div style='font-size:0.85rem;color:rgba(255,255,255,0.2);'>Complete Resume Analysis first</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='margin-bottom:1.5rem;'>
            <div style='font-size:0.65rem;color:rgba(255,255,255,0.25);text-transform:uppercase;
            letter-spacing:0.1em;margin-bottom:0.3rem;'>Interview Predictor</div>
            <div style='font-size:0.8rem;color:rgba(255,255,255,0.35);'>AI predicts the exact questions you'll be asked</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            experience_level = st.selectbox("Experience Level", ["Fresher", "1-2 years", "3-5 years"])
        with col2:
            st.markdown("<div style='padding-top:1.8rem;'></div>", unsafe_allow_html=True)
            predict_btn = st.button("Predict", use_container_width=True, type="primary")

        if predict_btn:
            from features.interview_predictor import predict_questions
            with st.spinner("Predicting your questions..."):
                result = predict_questions(st.session_state.resume_text, st.session_state.jd_text, experience_level)
            if result:
                st.session_state.questions = result
            else:
                st.error("Could not predict questions. Try again.")

        if st.session_state.questions:
            from utils.formatters import display_question_card
            qdata = st.session_state.questions
            st.markdown(f"""
            <div style='display:flex;align-items:center;justify-content:space-between;margin:1.5rem 0 1rem;'>
                <div style='font-size:0.72rem;color:rgba(255,255,255,0.25);'>
                    Role detected: <span style='color:#a78bfa;'>{qdata.get("role","")}</span>
                </div>
                <div style='font-size:0.65rem;color:rgba(255,255,255,0.2);'>
                    {len(qdata["questions"])} questions
                </div>
            </div>
            """, unsafe_allow_html=True)

            cat_colors = {
                "Technical": "#60a5fa",
                "Behavioural": "#a78bfa",
                "Role-specific": "#34d399",
                "Culture": "#fbbf24"
            }

            for i, q in enumerate(qdata["questions"], 1):
                cat = q.get("category", "General")
                cc = cat_colors.get(cat, "#fff")
                with st.expander(f"Q{i}  —  {q['question'][:70]}..."):
                    st.markdown(f"""
                    <span style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
                    color:{cc};padding:2px 10px;border-radius:100px;font-size:0.65rem;
                    letter-spacing:0.05em;'>{cat}</span>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <p style='color:rgba(255,255,255,0.35);font-size:0.75rem;font-style:italic;
                    margin-top:0.8rem;'>Why you'll be asked this: {q.get("why_asked","")}</p>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style='background:rgba(96,165,250,0.06);border:1px solid rgba(96,165,250,0.15);
                    border-radius:10px;padding:12px;margin-top:0.5rem;'>
                        <div style='font-size:0.6rem;color:rgba(96,165,250,0.5);text-transform:uppercase;
                        letter-spacing:0.1em;margin-bottom:6px;'>How to Answer</div>
                        <p style='color:rgba(255,255,255,0.55);font-size:0.78rem;margin:0;line-height:1.6;'>
                        {q.get("answer_framework","")}</p>
                    </div>
                    <div style='background:rgba(52,211,153,0.05);border:1px solid rgba(52,211,153,0.12);
                    border-radius:10px;padding:12px;margin-top:0.5rem;'>
                        <div style='font-size:0.6rem;color:rgba(52,211,153,0.5);text-transform:uppercase;
                        letter-spacing:0.1em;margin-bottom:6px;'>Strong Answer Example</div>
                        <p style='color:rgba(255,255,255,0.55);font-size:0.78rem;margin:0;line-height:1.6;'>
                        {q.get("sample_strong_answer","")}</p>
                    </div>
                    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 3 — BATCH SCREENER
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div style='margin-bottom:1.5rem;'>
        <div style='font-size:0.65rem;color:rgba(255,255,255,0.25);text-transform:uppercase;
        letter-spacing:0.1em;margin-bottom:0.3rem;'>Batch Screener</div>
        <div style='font-size:0.8rem;color:rgba(255,255,255,0.35);'>Screen multiple resumes against one job description</div>
    </div>
    """, unsafe_allow_html=True)

    batch_files = st.file_uploader("Upload Resumes", type=["pdf"], accept_multiple_files=True)
    batch_jd = st.text_area("Job Description", height=120, placeholder="Paste JD here...")

    if st.button("Screen All", use_container_width=True, type="primary"):
        if not batch_files:
            st.error("Upload at least one PDF.")
        elif not batch_jd.strip():
            st.error("Paste a job description.")
        else:
            from features.batch_screener import screen_resumes
            with st.spinner(f"Screening {len(batch_files)} resumes..."):
                df = screen_resumes(batch_files, batch_jd)

            if df is not None and len(df) > 0:
                total = len(df)
                recommended = len(df[df["Recommendation"].isin(["Strong Yes", "Yes"])])

                st.markdown(f"""
                <div style='display:flex;gap:1rem;margin-bottom:1.5rem;'>
                    <div class='metric-card' style='flex:1;'>
                        <div class='metric-number'>{total}</div>
                        <div class='metric-label'>Total Screened</div>
                    </div>
                    <div class='metric-card' style='flex:1;'>
                        <div class='metric-number' style='color:#34d399;-webkit-text-fill-color:#34d399;'>{recommended}</div>
                        <div class='metric-label'>Recommended</div>
                    </div>
                    <div class='metric-card' style='flex:1;'>
                        <div class='metric-number' style='color:#fb7185;-webkit-text-fill-color:#fb7185;'>{total - recommended}</div>
                        <div class='metric-label'>Not Recommended</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.dataframe(df, use_container_width=True)
                st.download_button(
                    "Download CSV",
                    df.to_csv(index=False),
                    "screening_results.csv",
                    "text/csv",
                    use_container_width=True
                )

# ══════════════════════════════════════════════════════════════════
# TAB 4 — MOCK INTERVIEW
# ══════════════════════════════════════════════════════════════════
with tab4:
    from features.interview_simulator import generate_questions, evaluate_answer, generate_report

    # ── SETUP STAGE ──
    if st.session_state.simulator_stage == "setup":
        st.markdown("""
        <div style='text-align:center;padding:2rem 1rem 2.5rem;'>
            <div style='font-size:0.65rem;color:rgba(255,255,255,0.15);text-transform:uppercase;letter-spacing:0.2em;margin-bottom:1.5rem;'>AI Interviewer</div>
            <div style='font-size:1.1rem;font-weight:700;color:rgba(255,255,255,0.85);
            font-family:Syne,sans-serif;letter-spacing:-0.02em;'>Mock Interview</div>
            <div style='font-size:0.75rem;color:rgba(255,255,255,0.25);margin-top:0.4rem;'>
            8 questions · instant feedback · full report</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            sim_role = st.selectbox("Role", ["Full Stack Developer", "Frontend Developer",
                "Backend Developer", "Data Analyst", "ML Engineer", "DevOps Engineer"])
        with col2:
            sim_exp = st.selectbox("Level", ["Fresher", "1-2 years", "3-5 years"])

        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

        if st.button("Begin Interview", use_container_width=True, type="primary"):
            with st.spinner("Preparing your interview..."):
                questions = generate_questions(sim_role, sim_exp)
            if questions:
                st.session_state.simulator_questions = questions
                st.session_state.simulator_role = sim_role
                st.session_state.simulator_stage = "in_progress"
                st.session_state.simulator_current_index = 0
                st.session_state.simulator_answers = []
                st.session_state.simulator_evaluations = []
                st.rerun()
            else:
                st.error("Could not generate questions. Try again.")

    # ── IN PROGRESS STAGE ──
    elif st.session_state.simulator_stage == "in_progress":
        questions = st.session_state.simulator_questions
        idx = st.session_state.simulator_current_index
        total = len(questions)
        q = questions[idx]

        # Progress
        progress_pct = idx / total
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;'>
            <div style='font-size:0.65rem;color:rgba(255,255,255,0.25);text-transform:uppercase;
            letter-spacing:0.1em;'>Question {idx+1} of {total}</div>
            <div style='font-size:0.65rem;color:rgba(167,139,250,0.5);font-family:monospace;'>
            {int(progress_pct*100)}% complete</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progress_pct)
        st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)

        diff_colors = {"Easy": "#34d399", "Medium": "#fbbf24", "Hard": "#fb7185"}
        cat_colors2 = {"Technical": "#60a5fa", "Behavioural": "#a78bfa", "Role-specific": "#34d399"}
        dc = diff_colors.get(q.get("difficulty", "Medium"), "#fff")
        cc = cat_colors2.get(q.get("category", "Technical"), "#fff")

        st.markdown(f"""
        <div class='glass-card' style='margin-bottom:1.5rem;'>
            <div style='display:flex;gap:8px;margin-bottom:1rem;'>
                <span style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                color:{cc};padding:2px 10px;border-radius:100px;font-size:0.65rem;'>{q.get("category","")}</span>
                <span style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                color:{dc};padding:2px 10px;border-radius:100px;font-size:0.65rem;'>{q.get("difficulty","")}</span>
            </div>
            <div style='font-size:1rem;font-weight:600;color:rgba(255,255,255,0.88);
            font-family:Syne,sans-serif;line-height:1.5;letter-spacing:-0.01em;'>
            {q["question"]}</div>
            <div style='font-size:0.7rem;color:rgba(255,255,255,0.2);margin-top:0.8rem;font-style:italic;'>
            {q.get("what_interviewer_wants","")}</div>
        </div>
        """, unsafe_allow_html=True)

        # Show last eval
        if st.session_state.simulator_evaluations:
            last = st.session_state.simulator_evaluations[-1]
            score_val = last.get("score", 0)
            sc = "#34d399" if score_val >= 7 else "#fbbf24" if score_val >= 5 else "#fb7185"
            with st.expander(f"Previous answer — {score_val}/10"):
                st.markdown(f"""
                <div style='display:flex;gap:1rem;margin-bottom:1rem;'>
                    <div style='font-size:2rem;font-weight:800;color:{sc};font-family:Syne,sans-serif;'>{score_val}/10</div>
                </div>
                <p style='color:rgba(255,255,255,0.4);font-size:0.75rem;'>{last.get("score_reason","")}</p>
                <div style='background:rgba(52,211,153,0.05);border:1px solid rgba(52,211,153,0.12);
                border-radius:8px;padding:10px;margin-top:8px;'>
                    <div style='font-size:0.6rem;color:rgba(52,211,153,0.4);margin-bottom:4px;'>WHAT WORKED</div>
                    <p style='color:rgba(255,255,255,0.5);font-size:0.75rem;margin:0;'>{last.get("what_was_good","")}</p>
                </div>
                <div style='background:rgba(251,191,36,0.05);border:1px solid rgba(251,191,36,0.12);
                border-radius:8px;padding:10px;margin-top:8px;'>
                    <div style='font-size:0.6rem;color:rgba(251,191,36,0.4);margin-bottom:4px;'>WHAT WAS MISSING</div>
                    <p style='color:rgba(255,255,255,0.5);font-size:0.75rem;margin:0;'>{last.get("what_was_missing","")}</p>
                </div>
                """, unsafe_allow_html=True)

        user_answer = st.text_area("Your Answer", height=180,
            placeholder="Take your time. Think out loud if needed...",
            key=f"ans_{idx}")

        if st.button("Submit Answer  →", use_container_width=True, type="primary"):
            if not user_answer.strip():
                st.warning("Type your answer before submitting.")
            else:
                with st.spinner("Evaluating..."):
                    ev = evaluate_answer(q["question"], user_answer, st.session_state.simulator_role)
                if ev:
                    st.session_state.simulator_answers.append(user_answer)
                    st.session_state.simulator_evaluations.append(ev)
                    if idx + 1 >= total:
                        with st.spinner("Generating your report..."):
                            report = generate_report(
                                st.session_state.simulator_questions,
                                st.session_state.simulator_answers,
                                st.session_state.simulator_evaluations,
                                st.session_state.simulator_role
                            )
                        st.session_state.simulator_report = report
                        st.session_state.simulator_stage = "complete"
                    else:
                        st.session_state.simulator_current_index += 1
                    st.rerun()
                else:
                    st.error("Evaluation failed. Try again.")

    # ── COMPLETE STAGE ──
    elif st.session_state.simulator_stage == "complete":
        report = st.session_state.simulator_report

        if not report:
            st.error("Report failed. Restart the interview.")
        else:
            overall = report.get("overall_score", 0)
            grade = report.get("grade", "?")

            grade_color = "#34d399" if grade in ["A"] else "#fbbf24" if grade in ["B","C"] else "#fb7185"

            st.markdown(f"""
            <div style='text-align:center;padding:2.5rem 1rem 2rem;'>
                <div style='font-size:0.65rem;color:rgba(255,255,255,0.2);text-transform:uppercase;
                letter-spacing:0.15em;margin-bottom:0.8rem;'>Interview Complete</div>
                <div style='font-size:5rem;font-weight:800;font-family:Syne,sans-serif;
                background:linear-gradient(135deg,{grade_color},rgba(255,255,255,0.6));
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text;line-height:1;'>{grade}</div>
                <div style='font-size:1rem;color:rgba(255,255,255,0.3);margin-top:0.3rem;'>{overall}/100</div>
                <div style='font-size:0.78rem;color:rgba(255,255,255,0.25);margin-top:0.8rem;
                font-style:italic;'>{report.get("hire_verdict","")}</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class='glass-card'>
                    <div style='font-size:0.6rem;color:rgba(255,255,255,0.2);text-transform:uppercase;
                    letter-spacing:0.1em;margin-bottom:0.8rem;'>Top Strengths</div>
                    {''.join([f'<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;"><span style="color:#34d399;font-size:0.8rem;">+</span><span style="color:rgba(255,255,255,0.55);font-size:0.75rem;line-height:1.5;">{s}</span></div>' for s in report.get("top_3_strengths",[])])}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class='glass-card'>
                    <div style='font-size:0.6rem;color:rgba(255,255,255,0.2);text-transform:uppercase;
                    letter-spacing:0.1em;margin-bottom:0.8rem;'>Areas to Improve</div>
                    {''.join([f'<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;"><span style="color:#fbbf24;font-size:0.8rem;">→</span><span style="color:rgba(255,255,255,0.55);font-size:0.75rem;line-height:1.5;">{s}</span></div>' for s in report.get("top_3_improvements",[])])}
                </div>
                """, unsafe_allow_html=True)

            # Question breakdown
            st.markdown("<div style='margin:1.5rem 0 1rem;'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div style='font-size:0.65rem;color:rgba(255,255,255,0.25);text-transform:uppercase;
            letter-spacing:0.1em;margin-bottom:1rem;'>Question Breakdown</div>
            """, unsafe_allow_html=True)

            for i, (q, e) in enumerate(zip(st.session_state.simulator_questions, st.session_state.simulator_evaluations), 1):
                sc_val = e.get("score", 0)
                sc = "#34d399" if sc_val >= 7 else "#fbbf24" if sc_val >= 5 else "#fb7185"
                with st.expander(f"Q{i}  ·  {sc_val}/10  —  {q['question'][:60]}..."):
                    st.markdown(f"""
                    <p style='color:rgba(255,255,255,0.35);font-size:0.75rem;font-style:italic;
                    margin-bottom:0.8rem;'>Your answer: {st.session_state.simulator_answers[i-1][:200]}...</p>
                    <div style='font-size:0.75rem;color:{sc};font-weight:600;margin-bottom:0.5rem;'>{sc_val}/10 — {e.get("score_reason","")}</div>
                    <p style='color:rgba(255,255,255,0.4);font-size:0.73rem;'>{e.get("improved_answer","")}</p>
                    """, unsafe_allow_html=True)

            # Next steps
            st.markdown("<div style='margin:1.5rem 0 1rem;'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='glass-card'>
                <div style='font-size:0.6rem;color:rgba(255,255,255,0.2);text-transform:uppercase;
                letter-spacing:0.1em;margin-bottom:0.8rem;'>Recommended Next Steps</div>
                {''.join([f'<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;"><span style="color:#a78bfa;">→</span><span style="color:rgba(255,255,255,0.55);font-size:0.75rem;line-height:1.5;">{s}</span></div>' for s in report.get("recommended_next_steps",[])])}
            </div>
            """, unsafe_allow_html=True)

            # Report text for download
            report_text = f"""HIREREADY AI — MOCK INTERVIEW REPORT
Role: {st.session_state.simulator_role}
Overall Score: {overall}/100  |  Grade: {grade}
Verdict: {report.get('hire_verdict','')}

TOP STRENGTHS:
{chr(10).join(['• ' + s for s in report.get('top_3_strengths',[])])}

AREAS TO IMPROVE:
{chr(10).join(['• ' + s for s in report.get('top_3_improvements',[])])}

QUESTION BREAKDOWN:
{''.join([f"Q{i}: {q['question']}{chr(10)}Answer: {a}{chr(10)}Score: {e['score']}/10 — {e['score_reason']}{chr(10)}{chr(10)}" for i,(q,a,e) in enumerate(zip(st.session_state.simulator_questions, st.session_state.simulator_answers, st.session_state.simulator_evaluations),1)])}

NEXT STEPS:
{chr(10).join(['• ' + s for s in report.get('recommended_next_steps',[])])}
"""
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("Download Report", report_text,
                    "interview_report.txt", "text/plain", use_container_width=True)
            with col2:
                if st.button("New Interview", use_container_width=True):
                    for key in ["simulator_stage","simulator_questions","simulator_current_index",
                                "simulator_answers","simulator_evaluations","simulator_report"]:
                        st.session_state[key] = "setup" if key == "simulator_stage" else [] if isinstance(st.session_state[key], list) else None
                    st.rerun()
