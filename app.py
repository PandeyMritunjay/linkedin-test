# app.py
"""
LinkedIn Profile Optimizer - Streamlit Application
Single agent system using NVIDIA's free AI API for comprehensive LinkedIn optimization.
Updated design with advanced interactive landing page and modern CSS effects.
"""
import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, Any, List
import re

# Import our modules from the project
from linkedin_scraper import scrape_linkedin_profile

from ai_providers import get_provider_status
try:
    from agents.orchestrator import route_request
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from agents.orchestrator import route_request

# --- Page Configuration ---
st.set_page_config(
    page_title="LinkedIn Profile Optimizer",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Modern Dynamic UI Design from Scratch ---
st.markdown("""
<style>
    /* === IMPORTS & RESET === */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body, [class*="css"] { font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif; scroll-behavior: smooth; }
    /* === HIDE STREAMLIT DEFAULTS === */
    .stDeployButton, footer, .stDecoration, header[data-testid="stHeader"] { display: none !important; visibility: hidden !important; }
    /* === BLACK BACKGROUND WITH EFFECT === */
    .stApp {
        background: linear-gradient(120deg, #000 0%, #111 100%);
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
        /* Subtle animated stars effect */
        background-image: repeating-radial-gradient(circle at 20% 30%, #222 1px, transparent 2px),
                          repeating-radial-gradient(circle at 70% 80%, #222 1px, transparent 2px),
                          linear-gradient(120deg, #000 0%, #111 100%);
        background-size: 100% 100%, 100% 100%, 100% 100%;
        animation: bgMove 30s linear infinite;
    }
    @keyframes bgMove {
        0% { background-position: 0 0, 0 0, 0 0; }
        100% { background-position: 100px 200px, 200px 100px, 0 0; }
    }
    /* === HERO SECTION === */
    .hero-wrapper {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 4rem 2rem;
        position: relative;
    }
    .hero-content {
        max-width: 1000px;
        z-index: 20;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(90deg, #00ffe7 0%, #ff00c8 100%);
        border-radius: 50px;
        padding: 0.75rem 1.5rem;
        margin-bottom: 2rem;
        color: #fff;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        letter-spacing: 1px;
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(3rem, 8vw, 5.5rem);
        font-weight: 900;
        color: #fff;
        margin-bottom: 1.5rem;
        line-height: 1.1;
        text-shadow: 0 4px 20px #00ffe7, 0 2px 8px #ff00c8;
        letter-spacing: -0.02em;
    }
    .hero-gradient-text {
        background: linear-gradient(90deg, #ffe600 0%, #00ffe7 50%, #ff00c8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: inline-block;
        font-weight: 900;
    }
    .hero-subtitle {
        font-size: clamp(1.1rem, 3vw, 1.4rem);
        color: #fff;
        margin-bottom: 3rem;
        line-height: 1.6;
        font-weight: 500;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        text-shadow: 0 2px 8px #000;
    }
    /* === STATS SECTION === */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #00ffe7 0%, #ff00c8 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        color: #111;
    }
    .stat-number {
        font-size: 3rem;
        font-weight: 900;
        display: block;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #ffe600 0%, #00ffe7 50%, #ff00c8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Space Grotesk', sans-serif;
    }
    .stat-label {
        font-size: 1rem;
        color: #fff;
        font-weight: 700;
        text-shadow: 0 2px 8px #000;
    }
    /* === FEATURE CARDS === */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 4rem 0;
    }
    .feature-card {
        background: linear-gradient(135deg, #111 0%, #222 100%);
        border: 2px solid #00ffe7;
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,255,231,0.15), 0 2px 8px #ff00c8;
        color: #fff;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    .feature-card:hover {
        border-color: #ffe600;
        box-shadow: 0 16px 48px #ff00c8, 0 2px 8px #00ffe7;
        background: linear-gradient(135deg, #222 0%, #111 100%);
    }
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        display: block;
        color: #ffe600;
        text-shadow: 0 2px 8px #00ffe7;
    }
    .feature-title {
        color: #00ffe7;
        font-size: 1.4rem;
        font-weight: 900;
        margin-bottom: 1rem;
        font-family: 'Space Grotesk', sans-serif;
        text-shadow: 0 2px 8px #000;
    }
    .feature-description {
        color: #fff;
        font-size: 1rem;
        line-height: 1.6;
        font-weight: 500;
        text-shadow: 0 1px 4px #000;
    }
    /* === INPUT SYSTEM === */
    .input-wrapper {
        position: relative;
        margin: 1.5rem 0;
    }
    .input-label {
        color: #ffe600;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.75rem;
        display: block;
        text-shadow: 0 2px 8px #000;
    }
    .modern-input {
        width: 100%;
        background: #111;
        border: 2px solid #00ffe7;
        border-radius: 16px;
        padding: 1rem 1.5rem;
        color: #fff;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        outline: none;
    }
    .modern-input::placeholder {
        color: #00ffe7;
        font-weight: 400;
    }
    .modern-input:focus {
        border-color: #ffe600;
        background: #222;
        box-shadow: 0 0 20px #ff00c8;
        transform: translateY(-2px);
    }
    /* === DYNAMIC FEATURE GRID === */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 4rem 0;
        animation: fadeInUp 1s ease-out 0.8s both;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, transparent 50%, rgba(255, 255, 255, 0.1) 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-card:hover {
        transform: translateY(-12px) scale(1.03);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        display: block;
        color: #ffe600;
        text-shadow: 0 2px 8px #00ffe7;
    }
    
    .feature-title {
        color: #00ffe7;
        font-size: 1.4rem;
        font-weight: 900;
        margin-bottom: 1rem;
        font-family: 'Space Grotesk', sans-serif;
        text-shadow: 0 2px 8px #000;
    }
    
    .feature-description {
        color: rgba(255, 255, 255, 0.85);
        font-size: 1rem;
        line-height: 1.6;
        font-weight: 400;
    }
    
    /* === MODERN BUTTON SYSTEM === */
    .button-group {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
        margin: 2rem 0;
    }
    
    .modern-btn {
        padding: 1rem 2rem;
        border-radius: 16px;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        min-width: 180px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        backdrop-filter: blur(10px);
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
    }
    
    .btn-primary:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6);
    }
    
    .btn-secondary {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 30px rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    .btn-accent {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        color: white;
        box-shadow: 0 8px 25px rgba(78, 205, 196, 0.4);
    }
    
    .btn-accent:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 40px rgba(78, 205, 196, 0.6);
    }
    
    /* === DYNAMIC STATS DISPLAY === */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
        animation: fadeInUp 1s ease-out 1.2s both;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stat-card:hover::before {
        opacity: 1;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        display: block;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Space Grotesk', sans-serif;
        animation: numberPulse 2s ease-in-out infinite;
    }
    
    .stat-label {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    @keyframes numberPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* === MAIN APP HEADER === */
    .app-header {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%, rgba(255, 255, 255, 0.05) 100%);
        opacity: 0.5;
    }
    
    .app-header h1 {
        color: white;
        font-size: clamp(1.8rem, 4vw, 2.5rem);
        font-weight: 800;
        margin: 0;
        font-family: 'Space Grotesk', sans-serif;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 2;
    }
    
    /* === DYNAMIC TAB NAVIGATION === */
    .nav-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 1rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .tab-navigation {
        display: flex;
        gap: 0.75rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .nav-tab {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: 0.875rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        backdrop-filter: blur(10px);
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        position: relative;
        overflow: hidden;
    }
    
    .nav-tab::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .nav-tab:hover::before {
        left: 100%;
    }
    
    .nav-tab:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    .nav-tab.active {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        border-color: rgba(255, 107, 107, 0.5);
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
    }
    
    /* === CONTENT DISPLAY AREA === */
    .content-wrapper {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .content-wrapper::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, transparent 50%, rgba(255, 255, 255, 0.02) 100%);
        opacity: 0.8;
    }
    
    .content-inner {
        position: relative;
        z-index: 2;
    }
    
    /* === GLOBAL INPUT TEXT COLOR FIX === */
    input, textarea, select {
        color: #1a1a1a !important;
        background: #fff !important;
    }
    input::placeholder, textarea::placeholder {
        color: #888 !important;
        opacity: 1 !important;
    }
    /* Streamlit overrides for all input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        color: #1a1a1a !important;
        background: #fff !important;
    }
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #888 !important;
        opacity: 1 !important;
    }
    
    /* === STREAMLIT BUTTON OVERRIDES === */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    /* === ANIMATIONS === */
    @keyframes heroFadeIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes heroSlideUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* === RESPONSIVE DESIGN === */
    @media (max-width: 1200px) {
        .app-container {
            padding: 1.5rem;
        }
        
        .features-grid {
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
        }
    }
    
    @media (max-width: 768px) {
        .app-container {
            padding: 1rem;
        }
        
        .hero-wrapper {
            padding: 2rem 1rem;
        }
        
        .hero-title {
            font-size: clamp(2rem, 8vw, 3rem) !important;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .feature-card {
            padding: 2rem;
        }
        
        .button-group {
            flex-direction: column;
            align-items: center;
            gap: 1rem;
        }
        
        .modern-btn {
            width: 100%;
            max-width: 280px;
        }
        
        .stats-grid {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }
        
        .stat-card {
            padding: 1.5rem;
        }
        
        .stat-number {
            font-size: 2.5rem;
        }
        
        .vibrant-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .content-wrapper {
            padding: 2rem;
        }
        
        .nav-container {
            padding: 0.75rem;
        }
        
        .tab-navigation {
            gap: 0.5rem;
        }
        
        .nav-tab {
            padding: 0.75rem 1rem;
            font-size: 0.85rem;
        }
    }
    
    @media (max-width: 480px) {
        .app-container {
            padding: 0.75rem;
        }
        
        .hero-wrapper {
            padding: 1.5rem 0.75rem;
        }
        
        .hero-badge {
            padding: 0.5rem 1rem;
            font-size: 0.8rem;
        }
        
        .features-grid,
        .stats-grid {
            gap: 1rem;
        }
        
        .feature-card,
        .stat-card,
        .vibrant-card {
            padding: 1.25rem;
        }
        
        .content-wrapper,
        .app-header {
            padding: 1.5rem;
        }
        
        .nav-tab {
            padding: 0.625rem 0.875rem;
            font-size: 0.8rem;
        }
    }
    
    /* --- Loading Animations --- */
    .loading-spinner {
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top: 3px solid white;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* --- Glassmorphism Effects --- */
    .glass-effect {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
    }
    
    /* --- Particle Animation --- */
    .particle {
        position: absolute;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        pointer-events: none;
        animation: particle-float 8s infinite linear;
    }
    
    @keyframes particle-float {
        0% {
            transform: translateY(100vh) scale(0);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) scale(1);
            opacity: 0;
        }
    }
    
    /* Enhanced Results Page Styling with Different Colors */
    .results-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Removed empty colored metric blocks - no longer needed */
    
    /* Action Button Containers */
    .action-button-container {
        border-radius: 25px;
        padding: 1rem 1.5rem;
        margin: 0.5rem;
        text-align: center;
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .action-button-model {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(139, 69, 19, 0.3));
        border-color: rgba(168, 85, 247, 0.5);
    }
    
    .action-button-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }
    
    .action-icon {
        font-size: 1.5rem;
    }
    
    .action-text {
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Enhanced white blocks for better content display */
    .white-block {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #1a1a1a !important;
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    /* Make all text, headings, labels, spans, and list items inside .white-block black */
    .white-block,
    .white-block * {
        color: #1a1a1a !important;
        background: transparent !important;
    }
    .white-block h1, .white-block h2, .white-block h3, 
    .white-block h4, .white-block h5, .white-block h6 {
        color: #1a1a1a !important;
    }
    .white-block p, .white-block div, .white-block span, 
    .white-block li, .white-block td, .white-block label {
        color: #1a1a1a !important;
    }
    /* Input fields and textareas inside white-block */
    .white-block input,
    .white-block textarea,
    .white-block select {
        color: #1a1a1a !important;
        background: #fff !important;
    }
    .white-block input::placeholder,
    .white-block textarea::placeholder {
        color: #888 !important;
        opacity: 1 !important;
    }
    /* Streamlit metric overrides for white-block */
    .white-block .stMetric,
    .white-block [data-testid="metric-container"] {
        background: transparent !important;
        border: none !important;
        color: #1a1a1a !important;
    }
    .white-block .stMetric > div,
    .white-block [data-testid="metric-container"] > div {
        background: transparent !important;
        color: #1a1a1a !important;
    }
    .white-block .stMetric label,
    .white-block [data-testid="metric-container"] label {
        color: #1a1a1a !important;
    }
    .white-block .stMetric [data-testid="metric-value"],
    .white-block [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #1a1a1a !important;
    }
    .white-block .stMetric [data-testid="metric-delta"],
    .white-block [data-testid="metric-container"] [data-testid="metric-delta"] {
        color: #1a1a1a !important;
    }
    .white-block .stMetric [data-testid="metric-delta"] svg,
    .white-block [data-testid="metric-container"] [data-testid="metric-delta"] svg {
        color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'job_fit_results' not in st.session_state:
        st.session_state.job_fit_results = None
    if 'optimization_results' not in st.session_state:
        st.session_state.optimization_results = None
    if 'guidance_results' not in st.session_state:
        st.session_state.guidance_results = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Profile Analysis"

initialize_session_state()

# --- Helper Functions for Displaying Content ---
def display_profile_analysis(results):
    st.subheader("📊 Profile Analysis Results")
    if results:
        if isinstance(results, str):
            st.markdown("<div style='background: linear-gradient(120deg, #ffd200 0%, #ff8800 100%); color: #222; border-radius: 18px; padding: 2rem 1.5rem; margin-bottom: 2rem;'><h4>AI Analysis</h4>" + results + "</div>", unsafe_allow_html=True)
            return
        # Card: Section-by-Section Scores
        section_scores = results.get('section_scores', {})
        st.markdown("<div style='background: linear-gradient(120deg, #ffd200 0%, #ff8800 100%); color: #222; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'>"
            "<b>Section-by-Section Scores:</b>"
            "<ol style='margin-top:1em;'>"
            f"<li><b>Headline:</b> {section_scores.get('headline', 'N/A')}/10 (Needs improvement)</li>"
            f"<li><b>Summary:</b> {section_scores.get('summary', 'N/A')}/10 (Good, but could be more engaging)</li>"
            f"<li><b>Experience:</b> {section_scores.get('experience', 'N/A')}/10 (Strong, but lacks quantifiable results)</li>"
            f"<li><b>Education:</b> {section_scores.get('education', 'N/A')}/10 (Complete and well-formatted)</li>"
            f"<li><b>Skills:</b> {section_scores.get('skills', 'N/A')}/10 (Incomplete and lacks relevance)</li>"
            "</ol></div>", unsafe_allow_html=True)
        # Card: Key Strengths
        strengths = results.get('strengths', [])
        st.markdown("<div style='background: linear-gradient(120deg, #ffd200 0%, #ff8800 100%); color: #222; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'>"
            "<b>Key Strengths:</b>"
            "<ol style='margin-top:1em;'>"
            + ''.join(f"<li>{item}</li>" for item in strengths)
            + "</ol></div>", unsafe_allow_html=True)
        # Card: Areas for Improvement
        weaknesses = results.get('weaknesses', [])
        st.markdown("<div style='background: linear-gradient(120deg, #ffd200 0%, #ff8800 100%); color: #222; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'>"
            "<b>Areas for Improvement:</b>"
            "<ol style='margin-top:1em;'>"
            + ''.join(f"<li>{item}</li>" for item in weaknesses)
            + "</ol></div>", unsafe_allow_html=True)
        # Card: Detailed Recommendations with Step-by-Step Actions
        recommendations = results.get('recommendations', [])
        st.markdown("<div style='background: linear-gradient(120deg, #ffd200 0%, #ff8800 100%); color: #222; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'>"
            "<b>Detailed Recommendations with Step-by-Step Actions:</b>"
            "<ol style='margin-top:1em;'>"
            + ''.join(f"<li>{rec}</li>" for rec in recommendations)
            + "</ol></div>", unsafe_allow_html=True)
    else:
        st.info("💡 No analysis results to display. Please analyze a profile first.")

def display_job_fit(results):
    st.subheader("🎯 Job Fit Analysis")
    if results:
        if isinstance(results, str):
            st.markdown("<div style='background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%); color: #fff; border-radius: 18px; padding: 2rem 1.5rem; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.10);'><h4>Job Fit Analysis</h4>" + results + "</div>", unsafe_allow_html=True)
            return
        # Card: Metrics
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); color: #222; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'>
        <b>Metrics</b><br/>
        <div style='display: flex; gap: 2rem;'>
        <div>Overall Fit: <b>{}</b></div>
        <div>Skill Match: <b>{}</b></div>
        <div>Experience Match: <b>{}</b></div>
        <div>Education Match: <b>{}</b></div>
                </div>
        </div>
        """.format(
            f"{results.get('fit_score', 'N/A')}/100",
            f"{results.get('skill_match', 'N/A')}/100",
            f"{results.get('experience_match', 'N/A')}/100",
            f"{results.get('education_match', 'N/A')}/100"
        ), unsafe_allow_html=True)
        # Card: Competitive Advantages
        st.markdown("<div style='background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%); color: #fff; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'><b>Competitive Advantages:</b><ul>" + ''.join(f"<li>{item}</li>" for item in results.get('advantages', [])) + "</ul></div>", unsafe_allow_html=True)
        # Card: Missing Skills to Develop
        st.markdown("<div style='background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); color: #fff; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'><b>Missing Skills to Develop:</b><ul>" + ''.join(f"<li>{item}</li>" for item in results.get('missing_skills', [])) + "</ul></div>", unsafe_allow_html=True)
        # Card: Application Strategy Tips
        st.markdown("<div style='background: linear-gradient(135deg, #ffb347 0%, #ffcc33 100%); color: #222; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'><b>Application Strategy Tips:</b><ul>" + ''.join(f"<li>{item}</li>" for item in results.get('application_tips', [])) + "</ul></div>", unsafe_allow_html=True)
        # Card: Improvement Recommendations
        st.markdown("<div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: #fff; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'><b>Improvement Recommendations:</b><ol>" + ''.join(f"<li>{item}</li>" for item in results.get('recommendations', [])) + "</ol></div>", unsafe_allow_html=True)
    else:
        st.info("📝 Paste a job description above and click 'Analyze Job Fit' to get started.")

def display_content_optimization(results):
    st.subheader("✨ Content Optimization")
    if results:
        if isinstance(results, str):
            st.markdown("<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; border-radius: 18px; padding: 2rem 1.5rem; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.10);'><h4>Content Optimization</h4>" + results + "</div>", unsafe_allow_html=True)
            return
        # Card: Original Content
        st.markdown("<div style='background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%); color: #fff; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'><b>Original Content:</b><br/>" + results.get('original_content', 'N/A') + "</div>", unsafe_allow_html=True)
        # Card: Optimized Version
        st.markdown("<div style='background: linear-gradient(135deg, #ffb347 0%, #ffcc33 100%); color: #222; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'><b>Optimized Version:</b><br/>" + results.get('optimized_content', 'N/A') + "</div>", unsafe_allow_html=True)
        # Card: Key Improvements
        st.markdown("<div style='background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); color: #fff; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'><b>Key Improvements Made:</b><ul>" + ''.join(f"<li>{item}</li>" for item in results.get('improvements', [])) + "</ul></div>", unsafe_allow_html=True)
        # Card: Keywords Added
        st.markdown("<div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: #fff; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'><b>Keywords Added:</b><br/>" + ', '.join(f"<span style='font-weight:bold'>{k}</span>" for k in results.get('keywords_added', [])) + "</div>", unsafe_allow_html=True)
        # Card: Alternatives
        if results.get('alternatives'):
            st.markdown("<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'><b>Alternative Versions:</b><ul>" + ''.join(f"<li>{item}</li>" for item in results.get('alternatives', [])) + "</ul></div>", unsafe_allow_html=True)
    else:
        st.info("🎨 Select a section to optimize and click 'Optimize Section' to enhance your content.")

def display_career_guidance(results):
    st.subheader("🚀 Career Guidance")
    if results:
        if isinstance(results, str):
            st.markdown("<div style='background: linear-gradient(135deg, #ffb347 0%, #ffcc33 100%); color: #222; border-radius: 18px; padding: 2rem 1.5rem; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.10);'><h4>Career Guidance</h4>" + results + "</div>", unsafe_allow_html=True)
            return
        # Card: Growth Opportunities
        st.markdown("<div style='background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%); color: #fff; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'><b>Growth Opportunities:</b><ul>" + ''.join(f"<li>{item}</li>" for item in results.get('growth_opportunities', [])) + "</ul></div>", unsafe_allow_html=True)
        # Card: Learning Resources
        st.markdown("<div style='background: linear-gradient(135deg, #ffb347 0%, #ffcc33 100%); color: #222; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'><b>Learning Resources:</b><ul>" + ''.join(f"<li>{item}</li>" for item in results.get('learning_resources', [])) + "</ul></div>", unsafe_allow_html=True)
        # Card: Networking Strategy
        st.markdown("<div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: #fff; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'><b>Networking Strategy:</b><ul>" + ''.join(f"<li>{item}</li>" for item in results.get('networking_strategy', [])) + "</ul></div>", unsafe_allow_html=True)
        # Card: Market Trends
        st.markdown("<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; border-radius: 18px; padding: 1.5rem; margin-bottom: 1.5rem;'><b>Market Trends:</b><ul>" + ''.join(f"<li>{item}</li>" for item in results.get('market_trends', [])) + "</ul></div>", unsafe_allow_html=True)
    else:
        st.info("🎯 Enter your career goals above and click 'Get Career Guidance' for personalized advice.")

def display_landing_page():
    """Combine the new heading/button row design with the previous landing page content (stats, input, etc.)."""
    st.markdown("""
    <style>
    body, .stApp { background: #111 !important; }
    .custom-landing-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100vw;
        margin: 0 auto;
        margin-top: 2.5rem;
    }
    .custom-title {
        font-family: 'Outfit', 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: #fff;
        margin-bottom: 2.5rem;
        margin-top: 2.5rem;
        text-align: center;
        letter-spacing: -0.01em;
    }
    .custom-title .gradient {
        background: linear-gradient(90deg, #43e97b 0%, #38f9d7 50%, #f9ea8f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }
    .feature-btn-row {
        display: flex;
        flex-direction: row;
        gap: 2rem;
        justify-content: center;
        margin-top: 2.5rem;
        flex-wrap: wrap;
        margin-bottom: 3.5rem;
    }
    .feature-btn {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        background: #232323;
        color: #fff;
        font-weight: 700;
        font-size: 1.25rem;
        border: none;
        border-radius: 1.7rem;
        padding: 1.1rem 2.2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.18);
        cursor: pointer;
        transition: background 0.2s, box-shadow 0.2s, color 0.2s;
        outline: none;
        min-width: 230px;
        justify-content: center;
        border: 3px solid transparent;
    }
    .feature-btn .icon {
        font-size: 1.5rem;
        display: flex;
        align-items: center;
    }
    .feature-btn.profile { border-color: #1ec8fc; }
    .feature-btn.jobfit { border-color: #ff3b3b; }
    .feature-btn.content { border-color: #7ed957; }
    .feature-btn.guidance { border-color: #f9ea8f; }
    .feature-btn.chat { border-color: #38f9d7; }
    .feature-btn.new { border-color: #a7a7a7; }
    .feature-btn:hover { background: #292929; color: #ffe600; }
    .custom-landing-outer { max-width: 600px; margin: 0 auto; padding: 0 2vw; }
    .custom-hero-badge {
        display: inline-block;
        background: linear-gradient(90deg, #00ffe7 0%, #ff00c8 100%);
        color: #fff;
        font-weight: 800;
        font-size: 1.1rem;
        border-radius: 2rem;
        padding: 0.6rem 1.7rem;
        margin-bottom: 2.2rem;
        margin-top: 2.5rem;
        letter-spacing: 1px;
        box-shadow: 0 2px 12px #000;
        border: none;
    }
    .custom-hero-subtitle {
        font-size: 1.15rem;
        color: #e0e0e0;
        margin-bottom: 2.5rem;
        font-weight: 500;
        text-align: left;
        max-width: 600px;
    }
    .custom-stats-row {
        display: flex;
        flex-direction: row;
        gap: 2rem;
        margin: 2.5rem 0 2.5rem 0;
        justify-content: flex-start;
        flex-wrap: wrap;
    }
    .custom-stat-card {
        background: linear-gradient(135deg, #181818 60%, #232323 100%);
        border: none;
        border-radius: 2rem;
        padding: 2.2rem 2.5rem;
        min-width: 180px;
        text-align: center;
        box-shadow: 0 2px 16px #000;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .custom-stat-number {
        font-size: 2.3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ffe600 0%, #00ffe7 50%, #ff00c8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
    }
    .custom-stat-label {
        color: #fff;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-shadow: 0 1px 8px #000;
    }
    .custom-input-block {
        margin-top: 2.5rem;
        width: 100%;
        max-width: 600px;
    }
    .custom-input-label {
        color: #ffe600;
        font-weight: 800;
        font-size: 1.1rem;
        margin-bottom: 0.7rem;
        display: block;
        text-shadow: 0 2px 8px #000;
        letter-spacing: 0.5px;
    }
    .custom-input-box {
        width: 100%;
        background: #181818;
        border: 2.5px solid #00ffe7;
        border-radius: 1.5rem;
        padding: 1.1rem 1.5rem;
        color: #fff;
        font-size: 1.1rem;
        font-weight: 600;
        outline: none;
        margin-bottom: 0.5rem;
        transition: border 0.2s, box-shadow 0.2s;
        box-shadow: 0 2px 12px #000;
    }
    .custom-input-box::placeholder {
        color: #00ffe7;
        opacity: 1;
    }
    .custom-input-box:focus {
        border-color: #ffe600;
        box-shadow: 0 0 12px #ff00c8;
        background: #232323;
    }
    .custom-btn-row {
        display: flex;
        flex-direction: row;
        gap: 1.2rem;
        margin-top: 0.7rem;
    }
    .custom-analyze-btn, .custom-demo-btn {
        font-weight: 800;
        font-size: 1.1rem;
        border: none;
        border-radius: 1.5rem;
        padding: 0.9rem 2.2rem;
        cursor: pointer;
        box-shadow: 0 2px 12px #000;
        transition: background 0.2s, color 0.2s;
        outline: none;
        margin-bottom: 0.2rem;
    }
    .custom-analyze-btn {
        background: linear-gradient(90deg, #00ffe7 0%, #ff00c8 100%);
        color: #181818;
    }
    .custom-analyze-btn:hover {
        background: linear-gradient(90deg, #ffe600 0%, #00ffe7 100%);
        color: #000;
    }
    .custom-demo-btn {
        background: linear-gradient(90deg, #ffe600 0%, #00ffe7 100%);
        color: #181818;
    }
    .custom-demo-btn:hover {
        background: linear-gradient(90deg, #ff00c8 0%, #ffe600 100%);
        color: #000;
    }
    </style>
    <div class="custom-landing-container">
        <div class="custom-title">
            🚀 LinkedIn Profile <span class="gradient">Optimizer</span>
        </div>
        <div class="feature-btn-row">
            <div class="feature-btn profile"><span class="icon">📊</span> Profile Analysis</div>
            <div class="feature-btn jobfit"><span class="icon">🎯</span> Job Fit</div>
            <div class="feature-btn content"><span class="icon">✨</span> Content Optimizer</div>
            <div class="feature-btn guidance"><span class="icon">🚀</span> Career Guidance</div>
            <div class="feature-btn chat"><span class="icon">💬</span> AI Chat</div>
            <div class="feature-btn new"><span class="icon">🔄</span> New Profile</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="custom-landing-outer">', unsafe_allow_html=True)
    st.markdown('<div class="custom-hero-badge">🚀 <b>Powered by NVIDIA AI • Free Forever</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-hero-subtitle">Get AI-powered insights, job fit analysis, and personalized career guidance to accelerate your professional growth and land your dream job.</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-stats-row">\
        <div class="custom-stat-card">\
            <div class="custom-stat-number">10K+</div>\
            <div class="custom-stat-label">Profiles Optimized</div>\
        </div>\
        <div class="custom-stat-card">\
            <div class="custom-stat-number">95%</div>\
            <div class="custom-stat-label">Success Rate</div>\
        </div>\
        <div class="custom-stat-card">\
            <div class="custom-stat-number">24/7</div>\
            <div class="custom-stat-label">AI Support</div>\
        </div>\
    </div>', unsafe_allow_html=True)
    with st.form(key="profile_form"):
        st.markdown('<div class="custom-input-block">', unsafe_allow_html=True)
        st.markdown('<label class="custom-input-label">🔗 Enter Your LinkedIn Profile URL</label>', unsafe_allow_html=True)
        profile_url = st.text_input(
            "",
            placeholder="https://linkedin.com/in/your-profile-name",
            help="Enter a LinkedIn profile URL to analyze",
            label_visibility="collapsed",
            key="profile_url_input",
        )
        st.markdown('</div>', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            analyze_button = st.form_submit_button("🔍 Analyze", use_container_width=True)
        with col2:
            demo_button = st.form_submit_button("🎭 Try Demo", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    return analyze_button, demo_button, profile_url

# --- Main Application ---
def main():
    # Check if profile data exists to determine which view to show
    if not st.session_state.profile_data:
        # Show landing page
        analyze_button, demo_button, profile_url = display_landing_page()
        
        # Handle form submissions
        if analyze_button and profile_url:
            with st.spinner("🔍 Analyzing LinkedIn profile..."):
                st.session_state.profile_data = scrape_linkedin_profile(profile_url)
                user_input = f"Analyze this LinkedIn profile: {profile_url}"
                st.session_state.analysis_results = route_request(user_input, "profile")
                st.session_state.active_tab = "Profile Analysis"
                st.rerun()

        if demo_button:
            with st.spinner("🎭 Loading demo profile..."):
                st.session_state.profile_data = scrape_linkedin_profile("demo")
                user_input = f"Analyze this LinkedIn profile: demo"
                st.session_state.analysis_results = route_request(user_input, "profile")
                st.session_state.active_tab = "Profile Analysis"
                st.rerun()
    
    else:
        # Show modern main application with large colored-outline buttons as navigation (horizontal row)
        tab_defs = [
            ("Profile Analysis", "📊", "#1ec8fc"),
            ("Job Fit", "🎯", "#ff3b3b"),
            ("Content Optimizer", "✨", "#7ed957"),
            ("Career Guidance", "🚀", "#f9ea8f"),
            ("AI Chat", "💬", "#38f9d7"),
            ("New Profile", "🔄", "#a7a7a7"),
        ]
        if "active_tab" not in st.session_state:
            st.session_state.active_tab = "Profile Analysis"
        st.markdown("""
        <style>
        .big-nav-btn {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            font-size: 1.35rem;
            font-weight: 700;
            padding: 1.1rem 2.2rem;
            border-radius: 1.5rem;
            border: 3px solid transparent;
            background: #181818;
            color: #fff;
            margin-bottom: 0.5rem;
            box-shadow: none;
            transition: border 0.2s, box-shadow 0.2s, color 0.2s;
            cursor: pointer;
            width: 100%;
            justify-content: center;
        }
        .big-nav-btn.active {
            color: #ffd700;
            box-shadow: 0 0 0 3px #fff2, 0 2px 16px #0004;
        }
        .big-nav-btn .icon { font-size: 1.5em; }
        .big-nav-row {
            display: flex;
            flex-direction: row;
            gap: 2.2rem;
            justify-content: center;
            margin: 2.5rem 0 2.5rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown('<div class="big-nav-row">', unsafe_allow_html=True)
        cols = st.columns(len(tab_defs), gap="large")
        for i, (tab_name, icon, color) in enumerate(tab_defs):
            is_active = st.session_state.active_tab == tab_name
            btn_style = f"border-color: {color}; color: {'#ffd700' if is_active else '#fff'};"
            btn_class = "big-nav-btn active" if is_active else "big-nav-btn"
            btn_label = f"{icon} {tab_name}"
            with cols[i]:
                if st.button(btn_label, key=f"tab_{tab_name}", help=tab_name, use_container_width=True):
                    st.session_state.active_tab = tab_name
                st.markdown(f"<style>div[data-testid='stButton'] button{{{btn_style} font-size:1.35rem;font-weight:700;border-radius:1.5rem;background:#181818;}}</style>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        # Show content for the selected tab only
        if st.session_state.active_tab == "Profile Analysis":
            # Use orchestrator for profile analysis
            if st.session_state.profile_data:
                user_input = f"Analyze this LinkedIn profile: {st.session_state.profile_data.get('profile_url', '')}"
                analysis_result = route_request(user_input, "profile")
                display_profile_analysis(analysis_result)
            else:
                st.info("Please provide a LinkedIn profile to analyze.")
        
        elif st.session_state.active_tab == "Job Fit":
            job_desc = st.text_area(
                "📋 Paste Job Description Here", 
                st.session_state.get("job_description", ""),
                height=120,
                key="job_desc_input",
            )
            if st.button("Analyze Job Fit", key="analyze_job_fit"):
                st.session_state["job_description"] = job_desc
                with st.spinner("Analyzing job fit..."):
                    st.session_state.job_fit_results = route_request(job_desc, "job_fit")
                st.rerun()
            if st.session_state.job_fit_results:
                st.markdown('<div style="color:#111">', unsafe_allow_html=True)
                display_job_fit(st.session_state.job_fit_results)
                st.markdown('</div>', unsafe_allow_html=True)
        
        elif st.session_state.active_tab == "Content Optimizer":
            col1, col2 = st.columns(2)
            with col1:
                section_to_optimize = st.selectbox(
                    "📝 Select Section", 
                    ["headline", "summary", "experience"],
                    help="Choose which section of your profile to optimize"
                )
            with col2:
                target_role = st.text_input(
                    "🎯 Target Role (Optional)",
                    placeholder="e.g., Senior Software Engineer"
                )
            if st.button("✨ Optimize Section", key="optimize_btn"):
                with st.spinner(f"✨ Optimizing {section_to_optimize}..."):
                    user_input = f"Rewrite my {section_to_optimize} for the role: {target_role}"
                    st.session_state.optimization_results = route_request(user_input, "content")
                    st.rerun()
            display_content_optimization(st.session_state.optimization_results)

        elif st.session_state.active_tab == "Career Guidance":
            career_goals = st.text_area(
                "🎯 Career Goals (Optional)", 
                height=100,
                placeholder="What are your career aspirations? e.g., 'I want to transition into tech leadership roles...'"
            )
            if st.button("🚀 Get Career Guidance", key="guidance_btn"):
                with st.spinner("🚀 Generating personalized career guidance..."):
                    user_input = f"Career guidance for: {career_goals}"
                    st.session_state.guidance_results = route_request(user_input, "guidance")
                    st.rerun()
            display_career_guidance(st.session_state.guidance_results)
        
        elif st.session_state.active_tab == "AI Chat":
            st.markdown('<h2 style="color:#fff;">💬 AI Chat Assistant</h2>', unsafe_allow_html=True)
            st.markdown('<em style="color:#fff;">Ask me anything about LinkedIn optimization, career advice, or job search strategies!</em>', unsafe_allow_html=True)
            # Render chat history with white text
            if "chat_history" in st.session_state and st.session_state.chat_history:
                for msg in st.session_state.chat_history:
                    role = msg.get("role", "assistant")
                    content = msg.get("content", "")
                    if role == "user":
                        st.markdown(f'<div style="color:#fff;"><b>You:</b> {content}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="color:#fff;"><b>AI Assistant:</b> {content}</div>', unsafe_allow_html=True)
            # Input box and send button
            st.markdown('<h3 style="color:#fff;">Send a Message</h3>', unsafe_allow_html=True)
            user_message = st.text_input("Type your message here...", "", key="chat_input", label_visibility="collapsed")
            send_col, _ = st.columns([1, 8])
            with send_col:
                if st.button("Send", key="send_chat_btn"):
                    if user_message.strip():
                        st.session_state.chat_history.append({"role": "user", "content": user_message.strip()})
                        st.session_state.chat_input = ""
                        st.rerun()
        
        elif st.session_state.active_tab == "New Profile":
            # Reset all session state and rerun to show landing page
            st.session_state.profile_data = None
            st.session_state.analysis_results = None
            st.session_state.job_fit_results = None
            st.session_state.optimization_results = None
            st.session_state.guidance_results = None
            st.session_state.chat_history = []
            st.session_state.active_tab = "Profile Analysis"
            st.rerun()
        
        st.markdown("""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        


        





if __name__ == "__main__":
    main()
