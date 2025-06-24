import os
import sys
import streamlit as st
from datetime import datetime
import json
import time
import random

# === BULLETPROOF DEPENDENCY HANDLING ===
def setup_environment():
    # First try normal imports
    try:
        import nltk
        from textblob import TextBlob
        return nltk, TextBlob
    except ImportError:
        # If normal imports fail, use system pip with user flag
        os.system(f"{sys.executable} -m pip install --user nltk==3.8.1 textblob==0.17.1")
        
        # Add user site-packages to path (critical for Streamlit Cloud)
        import site
        site.USER_SITE = os.path.expanduser("~/.local/lib/python3.13/site-packages")
        sys.path.append(site.USER_SITE)
        
        # Now import again
        import nltk
        from textblob import TextBlob
        return nltk, TextBlob

# Initialize dependencies
nltk, TextBlob = setup_environment()

# Download NLTK data silently
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# ============= CONFIGURATION =============
BIRTHDAY = (6, 25)  # June 25
CREDENTIALS = {"username": "peterparker", "password": "withgreatpower"}

# ============= STREAMLIT CONFIG =============
st.set_page_config(
    page_title="For the best spidey of multiverse :)",
    page_icon="💌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============= CUSTOM CSS =============
def inject_css():
    st.markdown("""
    <style>
        /* BLACK BACKGROUND */
        [data-testid="stAppViewContainer"] > .main {
            background-color: #000000;
        }
        
        /* CUTE FONTS */
        @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Rubik+Bubbles&display=swap');
        
        body {
            color: white !important;
            font-family: 'Patrick Hand', cursive !important;
        }
        
        /* ANIMATED HEADER */
        .header {
            font-family: 'Rubik Bubbles', cursive !important;
            font-size: 2.5rem !important;
            text-align: center;
            margin-bottom: 1.5rem;
            background: linear-gradient(45deg, #ff6b6b, #6b6bff, #6bff6b);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            animation: gradient 8s ease infinite;
            background-size: 200% 200%;
        }
        
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        /* MESSAGE CARDS */
        .message-card {
            background: rgba(40, 40, 40, 0.9) !important;
            border-radius: 15px !important;
            padding: 1.5rem !important;
            margin: 1.25rem 0 !important;
            border-left: 4px solid #ff6b6b;
            box-shadow: 0 4px 12px rgba(255, 107, 107, 0.25);
            transition: all 0.3s ease;
        }
        
        .message-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 18px rgba(255, 107, 107, 0.4);
        }
        
        /* SPECIAL ELEMENTS */
        .birthday-special {
            border-left: 4px solid #6b6bff !important;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% {transform: scale(1);}
            50% {transform: scale(1.02);}
            100% {transform: scale(1);}
        }
        
        /* RESPONSIVE DESIGN */
        @media (max-width: 768px) {
            .header {
                font-size: 2rem !important;
            }
            .message-card {
                padding: 1rem !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ============= SENTIMENT ANALYSIS =============
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.3: return "happy"
    elif polarity < -0.3: return "sad"
    elif "angry" in text.lower(): return "angry"
    elif "nostalgic" in text.lower(): return "nostalgic"
    elif "birthday" in text.lower(): return "birthday"
    return "default"

# ============= LOAD EMOTIONS =============
@st.cache_data
def load_emotions():
    try:
        with open("emotions.json", "r") as f:
            return json.load(f)
    except:
        return {
            "default": {
                "title": "For You",
                "message": "Thinking of you!",
                "note": "You're amazing!"
            }
        }

# ============= AUTHENTICATION =============
def authenticate():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div class="header">
            💌 For the best Spidey of Multiverse :) 💌
        </div>
        <div style='text-align: center; font-size: 1.1rem; margin-bottom: 2rem;'>
            A feeling. A phrase. A piece of you.
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("auth_form"):
            username = st.text_input("Username", placeholder="🕷️ mj's favourite")
            password = st.text_input("Password", type="password", placeholder="🔑 comes great responsibility")
            
            if st.form_submit_button("✨ web-sling in ✨", type="primary"):
                if username == CREDENTIALS["username"] and password == CREDENTIALS["password"]:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("go away, this is reserved for the real spidey.")
        st.stop()

# ============= MAIN APP =============
def main():
    inject_css()
    authenticate()
    
    emotions = load_emotions()
    today = datetime.now().date()
    is_bday = today.month == BIRTHDAY[0] and today.day == BIRTHDAY[1]
    
    # Birthday Special - WILL ACTIVATE ON JUNE 25
    if is_bday:
        st.balloons()
        st.markdown("""
        <div class="header">
            🎂 Happy Birthday! 🎂
        </div>
        """, unsafe_allow_html=True)
        
        bday_msg = emotions.get("birthday", emotions["default"])
        st.markdown(f"""
        <div class="message-card birthday-special">
            <h3>{bday_msg['title']}</h3>
            <p style='font-size: 1.1rem;'>{bday_msg['message']}</p>
            <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
                ✨ {bday_msg.get('note', '')} ✨
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main App Interface
    st.markdown("""
    <div class="header">
        How are you feeling?
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("feeling_form"):
        user_input = st.text_area("", placeholder="💖 Type your feelings here...", height=100)
        submitted = st.form_submit_button("🕷️ Get Message 🕷️", type="primary")
    
    if submitted and user_input:
        with st.spinner("Reading your feelings..."):
            time.sleep(1.5)
            
            emotion = analyze_sentiment(user_input)
            response = emotions.get(emotion, emotions["default"])
            
            st.markdown(f"""
            <div class="message-card">
                <h3>When You're Feeling {emotion.title()}</h3>
                <p style='font-size: 1.1rem;'>{response['message']}</p>
                <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
                    ✨ {response.get('note', '')} ✨
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Random memory (40% chance)
            if random.random() < 0.4 and "memories" in emotions:
                with st.expander("💭 Random Memory", expanded=True):
                    st.markdown(f"""
                    <div style='
                        background: rgba(255,255,255,0.1);
                        padding: 1rem;
                        border-radius: 10px;
                        font-style: italic;
                    '>
                        Remember when... {random.choice(emotions["memories"])}
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()