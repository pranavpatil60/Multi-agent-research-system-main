import streamlit as st
import sys
import os
import re

# --- Page Config ---
st.set_page_config(
    page_title="ResearchIQ",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- CSS Styling (Same as your design with minor fixes) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'); 
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; } 
html, body, [class*="css"] { 
     font-family: 'Inter', sans-serif; 
     font-size: 14px; 
} 
.stApp { 
     background: #f8f9fb; 
     color: #1a1d23; 
} 
#MainMenu, footer, header { visibility: hidden; } 
.block-container { padding: 2.5rem 2rem 4rem; max-width: 780px; } 

/* Animations */
@keyframes fadeUp { 
     from { opacity: 0; transform: translateY(12px); } 
     to   { opacity: 1; transform: translateY(0); } 
} 
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.35} } 

.fade-up   { animation: fadeUp 0.45s ease both; } 
.fade-up-1 { animation-delay: 0.05s; } 
.fade-up-2 { animation-delay: 0.12s; } 
.fade-up-3 { animation-delay: 0.20s; } 
.dot-pulse { animation: pulse 1.2s ease infinite; display: inline-block; margin-right: 5px; } 

/* Header */
.app-header { text-align: center; padding: 2.5rem 0 2rem; } 
.app-logo { 
     width: 42px; height: 42px; background: #1a1d23; border-radius: 10px; 
     display: inline-flex; align-items: center; justify-content: center; 
     font-size: 1.2rem; margin-bottom: 1rem; color: white;
} 
.app-title { font-size: 1.6rem; font-weight: 700; color: #1a1d23; letter-spacing: -0.03em; margin-bottom: 0.35rem; } 
.app-subtitle { font-size: 0.85rem; color: #8b93a0; font-weight: 400; letter-spacing: 0.01em; } 

/* Input card */
.input-wrap { 
     background: #ffffff; border: 1px solid #e5e8ed; border-radius: 14px; 
     padding: 1.4rem 1.6rem; margin: 1.2rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.04); 
} 

/* Button & Inputs */
.stTextInput > div > div > input { 
     background: #f4f5f7 !important; border: 1.5px solid #e5e8ed !important; 
     border-radius: 8px !important; color: #1a1d23 !important; 
} 
.stButton > button { 
     background: #1a1d23 !important; color: #ffffff !important; border-radius: 8px !important; 
     width: 100%; transition: all 0.2s;
} 
.stButton > button:hover { background: #2d3240 !important; transform: translateY(-1px); }

/* Step bar */
.step-bar { 
     display: flex; align-items: center; background: #ffffff; border: 1px solid #e5e8ed; 
     border-radius: 12px; padding: 1rem 1.4rem; margin: 1.2rem 0; gap: 0; 
} 
.step-item { flex: 1; display: flex; align-items: center; gap: 0.55rem; position: relative; } 
.step-dot { 
     width: 28px; height: 28px; border-radius: 50%; border: 1.5px solid #d1d5db; 
     background: #f4f5f7; display: flex; align-items: center; justify-content: center; 
     font-size: 0.68rem; font-weight: 600; color: #9ca3af; z-index: 1; 
} 
.step-dot.active { border-color: #1a1d23; background: #1a1d23; color: #fff; box-shadow: 0 0 0 4px rgba(26,29,35,0.08); } 
.step-dot.done { border-color: #22c55e; background: #22c55e; color: #fff; } 
.step-name { font-size: 0.73rem; font-weight: 600; color: #9ca3af; } 
.step-name.active { color: #1a1d23; } 
.step-name.done   { color: #16a34a; } 

/* Status pill */
.status-pill { 
     display: inline-flex; align-items: center; gap: 0.5rem; 
     font-size: 0.82rem; font-weight: 500; padding: 0.42rem 1rem; 
     border-radius: 100px; margin: 0.6rem 0; 
} 
.status-pill.running { background:#eff6ff; color:#2563eb; border:1px solid #bfdbfe; } 
.status-pill.done    { background:#f0fdf4; color:#16a34a; border:1px solid #bbf7d0; } 

/* Result sections */
.section-block { 
     background: #ffffff; border: 1px solid #e5e8ed; border-radius: 12px; 
     margin: 0.9rem 0; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.04); 
     animation: fadeUp 0.4s ease both; 
} 
.section-head { display: flex; align-items: center; gap: 0.6rem; padding: 0.75rem 1.2rem; background: #fafafa; border-bottom: 1px solid #f0f1f3; } 
.section-badge { font-size: 0.67rem; font-weight: 600; text-transform: uppercase; padding: 0.18rem 0.5rem; border-radius: 4px; } 
.badge-blue   { background:#eff6ff; color:#2563eb; } 
.badge-violet { background:#f5f3ff; color:#7c3aed; } 
.badge-amber  { background:#fffbeb; color:#d97706; } 
.badge-green  { background:#f0fdf4; color:#16a34a; } 
.section-label { font-size: 0.83rem; font-weight: 600; color: #1a1d23; } 
.section-body { padding: 1rem 1.2rem; font-size: 0.83rem; line-height: 1.75; color: #4b5563; white-space: pre-wrap; max-height: 300px; overflow-y: auto; } 

/* Critic Score UI Fix */
.score-row { display: flex; align-items: center; gap: 1rem; padding: 1.2rem; background: #fcfcfc; border-bottom: 1px solid #f0f1f3; } 
.score-num { font-size: 2.2rem; font-weight: 800; color: #1a1d23; letter-spacing: -0.04em; line-height: 1; } 
.score-sub { font-size: 0.75rem; color: #8b93a0; font-weight: 500; text-transform: uppercase; margin-top: 4px; }

</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="app-header fade-up"> 
     <div class="app-logo">🔬</div> 
     <div class="app-title">ResearchIQ</div> 
     <div class="app-subtitle">Search &nbsp;·&nbsp; Scrape &nbsp;·&nbsp; Write &nbsp;·&nbsp; Critique</div> 
</div> 
""", unsafe_allow_html=True)

# --- Step Bar Renderer ---
STEPS = [("1","Search"),("2","Reader"),("3","Writer"),("4","Critic")] 

def render_steps(active=-1, done_up_to=-1): 
    items = "" 
    for i, (num, name) in enumerate(STEPS): 
        if i < done_up_to: dc, nc, inner = "done",  "done",  "✓" 
        elif i == active: dc, nc, inner = "active","active", num 
        else: dc, nc, inner = "", "", num 
        items += f""" 
        <div class="step-item"> 
            <div class="step-dot {dc}">{inner}</div> 
            <div class="step-name {nc}">{name}</div> 
        </div>""" 
    st.markdown(f'<div class="step-bar fade-up fade-up-1">{items}</div>', unsafe_allow_html=True)

# --- Main Input ---
st.markdown('<div class="input-wrap fade-up fade-up-2">', unsafe_allow_html=True)
topic = st.text_input("Topic", placeholder="Enter research topic (e.g. Quantum Computing trends)", label_visibility="collapsed")
run_btn = st.button("Run Research Pipeline →")
st.markdown('</div>', unsafe_allow_html=True)

# --- Pipeline Execution ---
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    # Import handling
    current_dir = os.path.dirname(__file__)
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        
    try:
        from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
    except ImportError as e:
        st.error(f"Error: Could not find 'agents.py' in the current directory.")
        st.stop()

    state = {}
    step_ph = st.empty()
    status_ph = st.empty()

    # Step 1: Search
    with step_ph.container(): render_steps(active=0, done_up_to=0)
    status_ph.markdown('<div class="status-pill running"><span class="dot-pulse">●</span> Search agent scanning the web...</div>', unsafe_allow_html=True)
    sa = build_search_agent()
    res = sa.invoke({"messages": [("user", f"Find recent, reliable information about: {topic}")]})
    state["search_results"] = res["messages"][-1].content

    # Step 2: Reader
    with step_ph.container(): render_steps(active=1, done_up_to=1)
    status_ph.markdown('<div class="status-pill running"><span class="dot-pulse">●</span> Scraped top resources...</div>', unsafe_allow_html=True)
    ra = build_reader_agent()
    res2 = ra.invoke({"messages": [("user", f"Analyze and scrape details from results for: {topic}\n\n{state['search_results'][:1000]}")]})
    state["scraped_content"] = res2["messages"][-1].content

    # Step 3: Writer
    with step_ph.container(): render_steps(active=2, done_up_to=2)
    status_ph.markdown('<div class="status-pill running"><span class="dot-pulse">●</span> Drafting research report...</div>', unsafe_allow_html=True)
    state["report"] = writer_chain.invoke({"topic": topic, "research": f"{state['search_results']}\n\n{state['scraped_content']}"})

    # Step 4: Critic
    with step_ph.container(): render_steps(active=3, done_up_to=3)
    status_ph.markdown('<div class="status-pill running"><span class="dot-pulse">●</span> Critique review in progress...</div>', unsafe_allow_html=True)
    state["feedback"] = critic_chain.invoke({"report": state["report"]})

    # Completion
    with step_ph.container(): render_steps(active=-1, done_up_to=4)
    status_ph.markdown(f'<div class="status-pill done">✓ Pipeline complete for: {topic[:40]}</div>', unsafe_allow_html=True)

    # --- Display Results ---
    st.markdown(f'<div class="section-block"><div class="section-head"><span class="section-badge badge-blue">Search</span><span class="section-label">Web Results</span></div><div class="section-body">{state["search_results"]}</div></div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="section-block"><div class="section-head"><span class="section-badge badge-violet">Reader</span><span class="section-label">Key Content</span></div><div class="section-body">{state["scraped_content"]}</div></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-block"><div class="section-head"><span class="section-badge badge-amber">Report</span><span class="section-label">Draft</span></div><div class="section-body" style="max-height:none;">{state["report"]}</div></div>', unsafe_allow_html=True)

    # Score Extraction & Rendering Fix
    # Regex designed to catch "Score: 8/10", "Score: 8.5/10", "8/10", etc.
    score_match = re.search(r'(?:Score:?\s*)?(\d+(?:\.\d+)?)\s*/\s*10', state["feedback"], re.IGNORECASE)
    score_display = ""
    if score_match:
        val = score_match.group(1)
        score_display = f"""
        <div class="score-row">
            <div>
                <div class="score-num">{val}<span style="font-size:1.2rem; color:#9ca3af; font-weight:400;">/10</span></div>
                <div class="score-sub">Quality Score</div>
            </div>
        </div>
        """

    st.markdown(f"""
    <div class="section-block">
        <div class="section-head">
            <span class="section-badge badge-green">Critic</span>
            <span class="section-label">Review Feedback</span>
        </div>
        {score_display}
        <div class="section-body">{state['feedback']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button("↓ Download Report", state["report"], file_name="research_report.txt")

else:
    render_steps()
    st.markdown('<div class="empty-hint fade-up fade-up-3"><div class="big">⟶</div>Type a topic above to begin</div>', unsafe_allow_html=True)