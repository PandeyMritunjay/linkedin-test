import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Import your existing modules
from linkedin_scraper import scrape_linkedin_profile
from agents.orchestrator import route_request
from ai_providers import get_provider_status

# Page configuration
st.set_page_config(
    page_title="LinkedIn Profile Optimizer Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for advanced dark theme with neon effects
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Global Dark Theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Custom Headers with Neon Effect */
    .neon-header {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00, #00ff00);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: neonGlow 3s ease-in-out infinite alternate;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        margin-bottom: 2rem;
    }
    
    .sub-header {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #00ffff;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
        margin: 1.5rem 0;
    }
    
    /* Neon Animation */
    @keyframes neonGlow {
        0% { text-shadow: 0 0 20px rgba(0, 255, 255, 0.5), 0 0 30px rgba(0, 255, 255, 0.3); }
        100% { text-shadow: 0 0 30px rgba(255, 0, 255, 0.8), 0 0 40px rgba(255, 0, 255, 0.4); }
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #00ffff;
    }
    
    /* Cards and Containers */
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(255, 0, 255, 0.1) 100%);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 255, 255, 0.2);
        border-color: rgba(0, 255, 255, 0.6);
    }
    
    /* Profile Card */
    .profile-card {
        background: linear-gradient(135deg, rgba(16, 213, 194, 0.15) 0%, rgba(255, 0, 255, 0.15) 100%);
        border: 2px solid rgba(16, 213, 194, 0.4);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 40px rgba(16, 213, 194, 0.2);
        backdrop-filter: blur(15px);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #00ffff, #ff00ff);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(0, 255, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 255, 255, 0.5);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 10px;
        color: white;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 10px;
        color: white;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Selectbox */
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 255, 0.3);
        color: white;
    }
    
    /* Progress Bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00ffff, #ff00ff);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: rgba(255, 255, 255, 0.7);
        font-family: 'Rajdhani', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, rgba(0, 255, 255, 0.2), rgba(255, 0, 255, 0.2));
        color: #00ffff;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.1), rgba(0, 255, 255, 0.1));
        border: 1px solid rgba(0, 255, 0, 0.3);
        border-radius: 10px;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.1), rgba(255, 0, 255, 0.1));
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 10px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #00ffff, #ff00ff);
        border-radius: 10px;
    }
    
    /* Glow Effects */
    .glow-text {
        color: #00ffff;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Score Indicators */
    .score-excellent { color: #00ff00; text-shadow: 0 0 10px rgba(0, 255, 0, 0.5); }
    .score-good { color: #ffff00; text-shadow: 0 0 10px rgba(255, 255, 0, 0.5); }
    .score-average { color: #ff8800; text-shadow: 0 0 10px rgba(255, 136, 0, 0.5); }
    .score-poor { color: #ff0000; text-shadow: 0 0 10px rgba(255, 0, 0, 0.5); }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def get_score_class(score):
    """Return CSS class based on score"""
    if score >= 80:
        return "score-excellent"
    elif score >= 60:
        return "score-good"
    elif score >= 40:
        return "score-average"
    else:
        return "score-poor"

def create_radar_chart(scores_dict):
    """Create a radar chart for profile scores"""
    categories = list(scores_dict.keys())
    values = [int(score.split('/')[0]) if '/' in str(score) else int(score) for score in scores_dict.values()]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Profile Scores',
        line=dict(color='cyan', width=3),
        fillcolor='rgba(0, 255, 255, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255, 255, 255, 0.2)',
                tickcolor='white'
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.2)',
                tickcolor='white'
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Rajdhani')
    )
    
    return fig

def create_progress_chart(completeness):
    """Create a circular progress chart"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = completeness,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Profile Completeness", 'font': {'color': 'white', 'family': 'Rajdhani'}},
        delta = {'reference': 100},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': 'white'},
            'bar': {'color': "cyan"},
            'steps': [
                {'range': [0, 50], 'color': "rgba(255, 0, 0, 0.3)"},
                {'range': [50, 80], 'color': "rgba(255, 255, 0, 0.3)"},
                {'range': [80, 100], 'color': "rgba(0, 255, 0, 0.3)"}
            ],
            'threshold': {
                'line': {'color': "magenta", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white', 'family': 'Rajdhani'}
    )
    
    return fig

def display_profile_card(profile_data):
    """Display enhanced profile information card"""
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center;">
            <img src="{profile_data.get('profile_image', 'https://via.placeholder.com/150')}" 
                 style="border-radius: 50%; width: 150px; height: 150px; border: 3px solid #00ffff; box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);">
            <h2 class="glow-text" style="margin: 1rem 0;">{profile_data.get('name', 'Unknown')}</h2>
            <p style="color: #ff00ff; font-size: 1.2rem; font-weight: 500;">{profile_data.get('headline', 'No headline')}</p>
            <p style="color: rgba(255, 255, 255, 0.7);">📍 {profile_data.get('location', 'Location not specified')}</p>
            <p style="color: rgba(255, 255, 255, 0.7);">🏢 {profile_data.get('company', 'Company not specified')}</p>
            <p style="color: rgba(255, 255, 255, 0.7);">🎓 {profile_data.get('school', 'Education not specified')}</p>
            <p style="color: #00ffff;">🔗 {profile_data.get('connections', 0)} connections</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display detailed sections
    if profile_data.get('summary'):
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Professional Summary")
        st.write(profile_data['summary'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Experience Section
    if profile_data.get('experience'):
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 💼 Professional Experience")
        for exp in profile_data['experience'][:3]:  # Show top 3 experiences
            st.markdown(f"""
            **{exp.get('title', 'Position')}** at **{exp.get('company', 'Company')}**  
            📅 {exp.get('duration', 'Duration not specified')} | 📍 {exp.get('location', 'Location not specified')}  
            {exp.get('description', 'No description available')}
            """)
            st.markdown("---")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Skills Section
    if profile_data.get('skills'):
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🛠️ Skills & Expertise")
        skills_text = " • ".join(profile_data['skills'][:15])  # Show top 15 skills
        st.markdown(f"**{skills_text}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Education Section
    if profile_data.get('education'):
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🎓 Education")
        for edu in profile_data['education']:
            st.markdown(f"""
            **{edu.get('degree', 'Degree')}**  
            🏫 {edu.get('school', 'Institution')} | 📅 {edu.get('duration', 'Duration not specified')}  
            {edu.get('description', '')}
            """)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="neon-header">🚀 LinkedIn Profile Optimizer Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: rgba(255, 255, 255, 0.8); font-family: Rajdhani;">AI-Powered Career Enhancement Platform</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<h2 class="sub-header">🎛️ Control Panel</h2>', unsafe_allow_html=True)
        
        # AI Provider Status
        provider_status = get_provider_status()
        status_color = "🟢" if provider_status.get('status') == 'active' else "🔴"
        st.markdown(f"""
        <div class="metric-card">
            <h4>🤖 AI Engine Status</h4>
            <p>{status_color} {provider_status.get('provider', 'Unknown').upper()}</p>
            <p>Model: {provider_status.get('model', 'Unknown')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown('<h3 class="sub-header">📋 Navigation</h3>', unsafe_allow_html=True)
        page = st.selectbox(
            "Choose Your Journey",
            ["🏠 Home", "👤 Profile Analysis", "🎯 Job Fit Analysis", "✨ Content Optimization", "🚀 Career Guidance", "💬 AI Chat Assistant"],
            key="navigation"
        )
        
        # Quick Actions
        st.markdown('<h3 class="sub-header">⚡ Quick Actions</h3>', unsafe_allow_html=True)
        if st.button("🔄 Refresh Data", key="refresh"):
            st.session_state.profile_data = None
            st.session_state.analysis_results = {}
            st.rerun()
        
        if st.button("📊 Demo Profile", key="demo"):
            st.session_state.profile_data = scrape_linkedin_profile("demo")
            st.success("Demo profile loaded!")
            st.rerun()
    
    # Main Content Area
    if page == "🏠 Home":
        show_home_page()
    elif page == "👤 Profile Analysis":
        show_profile_analysis()
    elif page == "🎯 Job Fit Analysis":
        show_job_fit_analysis()
    elif page == "✨ Content Optimization":
        show_content_optimization()
    elif page == "🚀 Career Guidance":
        show_career_guidance()
    elif page == "💬 AI Chat Assistant":
        show_chat_assistant()

def show_home_page():
    """Enhanced home page with better visuals"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="sub-header">🎯 Transform Your LinkedIn Presence</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h3>🚀 What We Offer</h3>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li><strong>🔍 Deep Profile Analysis</strong> - Comprehensive scoring and insights</li>
                <li><strong>🎯 Job Fit Assessment</strong> - Match your profile against dream jobs</li>
                <li><strong>✨ Content Optimization</strong> - AI-powered content enhancement</li>
                <li><strong>🚀 Career Guidance</strong> - Personalized development roadmaps</li>
                <li><strong>💬 AI Chat Support</strong> - 24/7 career coaching assistant</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # LinkedIn URL Input
        st.markdown('<h3 class="sub-header">🔗 Start Your Analysis</h3>', unsafe_allow_html=True)
        linkedin_url = st.text_input(
            "Enter LinkedIn Profile URL",
            placeholder="https://www.linkedin.com/in/your-profile",
            help="Paste the full LinkedIn profile URL here"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("🚀 Analyze Profile", key="analyze_home"):
                if linkedin_url:
                    with st.spinner("🔄 Scraping profile data..."):
                        st.session_state.profile_data = scrape_linkedin_profile(linkedin_url)
                    st.success("✅ Profile data loaded successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a LinkedIn URL")
        
        with col_btn2:
            if st.button("🎭 Try Demo", key="demo_home"):
                st.session_state.profile_data = scrape_linkedin_profile("demo")
                st.success("🎭 Demo profile loaded!")
                st.rerun()
        
        with col_btn3:
            if st.button("📊 View Stats", key="stats_home"):
                st.info("📈 Analytics coming soon!")
    
    with col2:
        st.markdown("""
        <div class="metric-card pulse-animation">
            <h3 style="color: #00ffff;">📈 Success Metrics</h3>
            <div style="text-align: center; margin: 2rem 0;">
                <h2 style="color: #00ff00;">95%</h2>
                <p>Profile Improvement Rate</p>
            </div>
            <div style="text-align: center; margin: 2rem 0;">
                <h2 style="color: #ff00ff;">3.2x</h2>
                <p>Average View Increase</p>
            </div>
            <div style="text-align: center; margin: 2rem 0;">
                <h2 style="color: #ffff00;">24/7</h2>
                <p>AI Assistant Available</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display profile if loaded
    if st.session_state.profile_data:
        st.markdown('<h2 class="sub-header">👤 Your Profile Overview</h2>', unsafe_allow_html=True)
        display_profile_card(st.session_state.profile_data)

def show_profile_analysis():
    """Enhanced profile analysis page"""
    st.markdown('<h2 class="sub-header">👤 Comprehensive Profile Analysis</h2>', unsafe_allow_html=True)
    
    if not st.session_state.profile_data:
        st.warning("⚠️ Please load a profile first from the Home page.")
        return
    
    # Run analysis if not already done
    if 'profile_analysis' not in st.session_state.analysis_results:
        with st.spinner("🧠 AI is analyzing your profile..."):
            profile_text = f"""
            Name: {st.session_state.profile_data.get('name', '')}
            Headline: {st.session_state.profile_data.get('headline', '')}
            Summary: {st.session_state.profile_data.get('summary', '')}
            Experience: {json.dumps(st.session_state.profile_data.get('experience', []))}
            Education: {json.dumps(st.session_state.profile_data.get('education', []))}
            Skills: {', '.join(st.session_state.profile_data.get('skills', []))}
            Location: {st.session_state.profile_data.get('location', '')}
            Industry: {st.session_state.profile_data.get('industry', '')}
            """
            
            analysis = route_request(profile_text, "profile")
            st.session_state.analysis_results['profile_analysis'] = analysis
    
    analysis = st.session_state.analysis_results['profile_analysis']
    
    # Display analysis results
    if isinstance(analysis, dict):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Overall Score
            overall_score = analysis.get('overall_score', 75)
            score_class = get_score_class(overall_score)
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎯 Overall Profile Score</h3>
                <h1 class="{score_class}" style="text-align: center; font-size: 4rem;">{overall_score}/100</h1>
            </div>
            """, unsafe_allow_html=True)
            
            # Profile Completeness
            completeness = analysis.get('profile_completeness', 85)
            fig_progress = create_progress_chart(completeness)
            st.plotly_chart(fig_progress, use_container_width=True)
        
        with col2:
            # Section Scores Radar Chart
            section_scores = analysis.get('section_scores', {})
            if section_scores:
                fig_radar = create_radar_chart(section_scores)
                st.plotly_chart(fig_radar, use_container_width=True)
        
        # Strengths and Weaknesses
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("### 💪 Key Strengths")
            strengths = analysis.get('strengths', [])
            for i, strength in enumerate(strengths, 1):
                st.markdown(f"**{i}.** {strength}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("### 🎯 Areas for Improvement")
            weaknesses = analysis.get('weaknesses', [])
            for i, weakness in enumerate(weaknesses, 1):
                st.markdown(f"**{i}.** {weakness}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Keywords and Recommendations
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🔑 Recommended Keywords")
        keywords = analysis.get('keywords', [])
        if keywords:
            keyword_text = " • ".join(keywords)
            st.markdown(f"**{keyword_text}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Detailed Recommendations")
        recommendations = analysis.get('recommendations', [])
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**{i}.** {rec}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Fallback for string response
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Analysis Results")
        st.write(analysis)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Export functionality
    if st.button("📥 Export Analysis", key="export_analysis"):
        export_data = {
            "profile_data": st.session_state.profile_data,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        st.download_button(
            label="💾 Download JSON Report",
            data=json.dumps(export_data, indent=2),
            file_name=f"linkedin_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def show_job_fit_analysis():
    """Enhanced job fit analysis page"""
    st.markdown('<h2 class="sub-header">🎯 Job Fit Analysis</h2>', unsafe_allow_html=True)
    
    if not st.session_state.profile_data:
        st.warning("⚠️ Please load a profile first from the Home page.")
        return
    
    # Job description input
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Paste the complete job description including requirements, responsibilities, and qualifications..."
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🎯 Analyze Job Fit", key="analyze_job_fit"):
        if job_description:
            with st.spinner("🧠 Analyzing job compatibility..."):
                profile_summary = f"""
                Profile: {st.session_state.profile_data.get('name', '')}
                Headline: {st.session_state.profile_data.get('headline', '')}
                Summary: {st.session_state.profile_data.get('summary', '')}
                Skills: {', '.join(st.session_state.profile_data.get('skills', []))}
                Experience: {json.dumps(st.session_state.profile_data.get('experience', [])[:3])}
                Education: {json.dumps(st.session_state.profile_data.get('education', []))}
                
                Job Description: {job_description}
                """
                
                job_fit_analysis = route_request(profile_summary, "job_fit")
                st.session_state.analysis_results['job_fit'] = job_fit_analysis
        else:
            st.error("Please enter a job description")
    
    # Display job fit results
    if 'job_fit' in st.session_state.analysis_results:
        analysis = st.session_state.analysis_results['job_fit']
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Job Fit Analysis Results")
        st.write(analysis)
        st.markdown('</div>', unsafe_allow_html=True)

def show_content_optimization():
    """Enhanced content optimization page"""
    st.markdown('<h2 class="sub-header">✨ Content Optimization</h2>', unsafe_allow_html=True)
    
    if not st.session_state.profile_data:
        st.warning("⚠️ Please load a profile first from the Home page.")
        return
    
    # Content selection
    content_type = st.selectbox(
        "Select content to optimize",
        ["Headline", "Summary", "Experience Description", "Skills Section"]
    )
    
    # Current content display
    current_content = ""
    if content_type == "Headline":
        current_content = st.session_state.profile_data.get('headline', '')
    elif content_type == "Summary":
        current_content = st.session_state.profile_data.get('summary', '')
    elif content_type == "Experience Description":
        experiences = st.session_state.profile_data.get('experience', [])
        if experiences:
            current_content = experiences[0].get('description', '')
    elif content_type == "Skills Section":
        skills = st.session_state.profile_data.get('skills', [])
        current_content = ', '.join(skills)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Current Content")
        st.text_area("Current", value=current_content, height=200, disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Target Role (Optional)")
        target_role = st.text_input("Enter target job title for optimization")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("✨ Optimize Content", key="optimize_content"):
        if current_content:
            with st.spinner("🧠 AI is optimizing your content..."):
                optimization_prompt = f"""
                Content Type: {content_type}
                Current Content: {current_content}
                Target Role: {target_role if target_role else 'General improvement'}
                Profile Context: {st.session_state.profile_data.get('name', '')} - {st.session_state.profile_data.get('headline', '')}
                """
                
                optimized_content = route_request(optimization_prompt, "content")
                st.session_state.analysis_results['content_optimization'] = optimized_content
        else:
            st.error("No content found to optimize")
    
    # Display optimization results
    if 'content_optimization' in st.session_state.analysis_results:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 Optimized Content")
        st.write(st.session_state.analysis_results['content_optimization'])
        st.markdown('</div>', unsafe_allow_html=True)

def show_career_guidance():
    """Enhanced career guidance page"""
    st.markdown('<h2 class="sub-header">🚀 Career Guidance</h2>', unsafe_allow_html=True)
    
    if not st.session_state.profile_data:
        st.warning("⚠️ Please load a profile first from the Home page.")
        return
    
    # Career goals input
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Your Career Goals")
    
    col1, col2 = st.columns(2)
    with col1:
        career_goal = st.text_input("Desired job title/role")
        industry_preference = st.text_input("Preferred industry")
    
    with col2:
        timeline = st.selectbox("Timeline", ["3 months", "6 months", "1 year", "2+ years"])
        experience_level = st.selectbox("Target level", ["Entry", "Mid-level", "Senior", "Executive"])
    
    additional_info = st.text_area(
        "Additional information (challenges, preferences, etc.)",
        height=100
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Get Career Guidance", key="get_guidance"):
        if career_goal:
            with st.spinner("🧠 Generating personalized career roadmap..."):
                guidance_prompt = f"""
                Current Profile: {st.session_state.profile_data.get('name', '')}
                Current Role: {st.session_state.profile_data.get('headline', '')}
                Current Skills: {', '.join(st.session_state.profile_data.get('skills', []))}
                Experience: {json.dumps(st.session_state.profile_data.get('experience', [])[:2])}
                
                Career Goals:
                - Desired Role: {career_goal}
                - Industry: {industry_preference}
                - Timeline: {timeline}
                - Target Level: {experience_level}
                - Additional Info: {additional_info}
                """
                
                career_guidance = route_request(guidance_prompt, "guidance")
                st.session_state.analysis_results['career_guidance'] = career_guidance
        else:
            st.error("Please enter your career goal")
    
    # Display guidance results
    if 'career_guidance' in st.session_state.analysis_results:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🗺️ Your Personalized Career Roadmap")
        st.write(st.session_state.analysis_results['career_guidance'])
        st.markdown('</div>', unsafe_allow_html=True)

def show_chat_assistant():
    """Enhanced AI chat assistant page"""
    st.markdown('<h2 class="sub-header">💬 AI Career Coach</h2>', unsafe_allow_html=True)
    
    # Chat interface
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    
    # Display chat history
    for i, message in enumerate(st.session_state.chat_history):
        if message['role'] == 'user':
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1)); 
                        padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 3px solid #00ffff;">
                <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(0, 255, 0, 0.1)); 
                        padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 3px solid #ff00ff;">
                <strong>AI Coach:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input(
        "Ask your AI career coach anything...",
        placeholder="e.g., How can I improve my LinkedIn headline?",
        key="chat_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("💬 Send", key="send_chat"):
            if user_input:
                # Add user message to history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # Get AI response
                with st.spinner("🤔 AI is thinking..."):
                    context = ""
                    if st.session_state.profile_data:
                        context = f"User's profile context: {st.session_state.profile_data.get('name', '')} - {st.session_state.profile_data.get('headline', '')}"
                    
                    full_prompt = f"{context}\n\nUser question: {user_input}"
                    ai_response = route_request(full_prompt, "chat")
                    
                    # Add AI response to history
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                
                st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Quick questions
    st.markdown("### ⚡ Quick Questions")
    quick_questions = [
        "How can I optimize my LinkedIn headline?",
        "What skills should I add to my profile?",
        "How do I write a compelling summary?",
        "What's the best way to network on LinkedIn?",
        "How can I increase my profile visibility?"
    ]
    
    cols = st.columns(len(quick_questions))
    for i, question in enumerate(quick_questions):
        with cols[i]:
            if st.button(f"❓ {question[:20]}...", key=f"quick_{i}"):
                st.session_state.chat_history.append({"role": "user", "content": question})
                
                with st.spinner("🤔 AI is thinking..."):
                    context = ""
                    if st.session_state.profile_data:
                        context = f"User's profile context: {st.session_state.profile_data.get('name', '')} - {st.session_state.profile_data.get('headline', '')}"
                    
                    full_prompt = f"{context}\n\nUser question: {question}"
                    ai_response = route_request(full_prompt, "chat")
                    
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                
                st.rerun()

if __name__ == "__main__":
    main()