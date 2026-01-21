"""
Streamlit Chatbot UI for Personal Assistant - Premium Edition
Beautiful, modern UI with smooth animations and aesthetic design
"""
import streamlit as st
import requests
import json
from datetime import datetime
from typing import Optional
import time


# Configuration
API_BASE_URL = "http://localhost:9000/api/v1"


# Page configuration
st.set_page_config(
    page_title="✨ AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS with animations and modern design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Root variables for theming */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        --shadow-color: rgba(102, 126, 234, 0.25);
    }
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
        background-attachment: fixed;
    }
    
    /* Floating particles animation */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(118, 75, 162, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(79, 172, 254, 0.1) 0%, transparent 40%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Animated header */
    .hero-header {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 8px 32px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        animation: slideDown 0.8s ease-out;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255, 255, 255, 0.05) 50%,
            transparent 70%
        );
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.5); }
        50% { box-shadow: 0 0 40px rgba(102, 126, 234, 0.8), 0 0 60px rgba(118, 75, 162, 0.4); }
    }
    
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
        animation: float 4s ease-in-out infinite;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .hero-badge {
        display: inline-block;
        background: var(--success-gradient);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 1rem;
        animation: pulse 2s infinite;
    }
    
    /* Chat messages with glass morphism */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s ease-out;
        transition: all 0.3s ease;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
    }
    
    [data-testid="stChatMessage"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* User message special styling */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%) !important;
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Assistant message special styling */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%) !important;
        border-color: rgba(79, 172, 254, 0.2);
    }
    
    [data-testid="stChatMessageContent"] {
        color: rgba(255, 255, 255, 0.95) !important;
        font-family: 'Inter', sans-serif;
        line-height: 1.7;
    }
    
    /* Chat input with glow effect */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
    }
    
    .stChatInputContainer:focus-within {
        border-color: rgba(102, 126, 234, 0.6);
        animation: glow 2s infinite;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(26, 26, 46, 0.98) 0%, rgba(15, 15, 35, 0.98) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] .element-container {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Buttons with gradient and hover effects */
    .stButton button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton button:hover::before {
        left: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    }
    
    .stButton button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Status cards */
    .status-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .status-card:hover {
        transform: translateY(-2px);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .status-online {
        background: linear-gradient(135deg, rgba(17, 153, 142, 0.2) 0%, rgba(56, 239, 125, 0.2) 100%);
        border-color: rgba(56, 239, 125, 0.3);
    }
    
    .status-offline {
        background: linear-gradient(135deg, rgba(245, 87, 108, 0.2) 0%, rgba(240, 147, 251, 0.2) 100%);
        border-color: rgba(245, 87, 108, 0.3);
    }
    
    /* Metrics with animation */
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.6) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Source chips with gradient border */
    .source-chip {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 25px;
        font-size: 0.85rem;
        color: #a5b4fc;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .source-chip:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Tabs with modern styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 0.5rem;
        gap: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255, 255, 255, 0.6);
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: rgba(255, 255, 255, 0.9);
        background: rgba(102, 126, 234, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Expander with glass effect */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        color: rgba(255, 255, 255, 0.9) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(102, 126, 234, 0.1) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 0 0 12px 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: none;
    }
    
    /* Text inputs with glow */
    .stTextInput input, .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: rgba(255, 255, 255, 0.9) !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: rgba(102, 126, 234, 0.5) !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Toggle switch styling */
    .stToggle > label > div {
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    .stToggle > label > div[data-checked="true"] {
        background: var(--primary-gradient) !important;
    }
    
    /* Info/Success/Error boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: rgba(255, 255, 255, 0.9) !important;
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Spinner with custom animation */
    .stSpinner > div {
        border-color: #667eea !important;
        border-top-color: transparent !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Divider with gradient */
    hr {
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent) !important;
        height: 1px !important;
        border: none !important;
    }
    
    /* Number input */
    .stNumberInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Welcome message special styling */
    .welcome-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 24px;
        padding: 2rem;
        text-align: center;
        animation: fadeIn 0.8s ease-out;
    }
    
    .welcome-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    .welcome-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .welcome-text {
        font-family: 'Inter', sans-serif;
        color: rgba(255, 255, 255, 0.7);
        line-height: 1.8;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-top: 1.5rem;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(102, 126, 234, 0.3);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: white;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "use_knowledge_base" not in st.session_state:
        st.session_state.use_knowledge_base = True
    if "category_filter" not in st.session_state:
        st.session_state.category_filter = None
    if "api_connected" not in st.session_state:
        st.session_state.api_connected = False


def check_api_health():
    """Check if the API is healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data
        return None
    except Exception:
        return None


def send_message(message: str) -> dict:
    """Send a message to the API and get a response"""
    try:
        payload = {
            "message": message,
            "use_knowledge_base": st.session_state.use_knowledge_base,
            "category_filter": st.session_state.category_filter,
            "stream": False
        }
        
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. The model may be processing a complex query."}
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to the API. Make sure the server is running."}
    except Exception as e:
        return {"error": str(e)}


def ingest_document(text: str, source: str, category: Optional[str] = None) -> dict:
    """Ingest a document into the knowledge base"""
    try:
        payload = {
            "text": text,
            "source": source,
            "category": category
        }
        
        response = requests.post(
            f"{API_BASE_URL}/knowledge/ingest",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


def search_knowledge(query: str, top_k: int = 5) -> dict:
    """Search the knowledge base"""
    try:
        payload = {
            "query": query,
            "top_k": top_k,
            "category": st.session_state.category_filter
        }
        
        response = requests.post(
            f"{API_BASE_URL}/knowledge/search",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


def get_knowledge_stats() -> dict:
    """Get knowledge base statistics"""
    try:
        response = requests.get(f"{API_BASE_URL}/knowledge/stats", timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"error": "Could not fetch stats"}
    except Exception:
        return {"error": "Could not connect to API"}


def render_sidebar():
    """Render the sidebar with settings and knowledge management"""
    with st.sidebar:
        # Animated logo/title
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <div style="font-size: 3rem; animation: float 3s ease-in-out infinite;">✨</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.5rem; font-weight: 700; 
                    background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; 
                    -webkit-text-fill-color: transparent; margin-top: 0.5rem;">
                    AI Assistant
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # API Status with animated card
        st.markdown("#### 🔌 System Status")
        health = check_api_health()
        
        if health:
            st.markdown("""
                <div class="status-card status-online">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.2rem;">🟢</span>
                        <span style="color: #38ef7d; font-weight: 600; font-family: 'Inter', sans-serif;">System Online</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if health.get("llm_loaded"):
                    st.success("🧠 AI Ready")
                else:
                    st.warning("🧠 AI Loading")
            with col2:
                if health.get("vector_db_connected"):
                    st.success("💾 DB Online")
                else:
                    st.warning("💾 DB Offline")
            st.session_state.api_connected = True
        else:
            st.markdown("""
                <div class="status-card status-offline">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.2rem;">🔴</span>
                        <span style="color: #f5576c; font-weight: 600; font-family: 'Inter', sans-serif;">System Offline</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.session_state.api_connected = False
        
        st.markdown("---")
        
        # Knowledge Base Settings
        st.markdown("#### 📚 Knowledge Base")
        
        st.session_state.use_knowledge_base = st.toggle(
            "🔮 Enable Smart Context",
            value=st.session_state.use_knowledge_base,
            help="Use knowledge base for context-aware responses"
        )
        
        st.session_state.category_filter = st.text_input(
            "🏷️ Category Filter",
            value=st.session_state.category_filter or "",
            placeholder="Filter by category...",
            help="Only search documents with this category"
        ) or None
        
        # Knowledge base stats with metrics
        if st.session_state.api_connected:
            with st.expander("📊 Analytics Dashboard"):
                stats = get_knowledge_stats()
                if "error" not in stats:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("📚 Vectors", stats.get("total_vectors", 0))
                    with col2:
                        st.metric("🔢 Dimensions", stats.get("dimension", 0))
                else:
                    st.info("📈 No data available yet")
        
        st.markdown("---")
        
        # Document Ingestion
        st.markdown("#### 📥 Add Knowledge")
        
        with st.expander("➕ Upload New Document"):
            doc_text = st.text_area(
                "📝 Content",
                height=120,
                placeholder="Paste your document content here...",
                label_visibility="collapsed"
            )
            doc_source = st.text_input(
                "🏷️ Source",
                placeholder="e.g., meeting_notes_2024"
            )
            doc_category = st.text_input(
                "📂 Category",
                placeholder="e.g., meetings, research, notes"
            )
            
            if st.button("✨ Add to Knowledge Base", type="primary", use_container_width=True):
                if doc_text and doc_source:
                    with st.spinner("🔄 Processing..."):
                        result = ingest_document(
                            doc_text,
                            doc_source,
                            doc_category if doc_category else None
                        )
                        if "error" in result:
                            st.error(f"❌ {result['error']}")
                        else:
                            st.success(f"✅ Added {result['chunks_created']} chunks!")
                            st.balloons()
                else:
                    st.warning("⚠️ Please provide content and source name")
        
        st.markdown("---")
        
        # Chat Controls
        st.markdown("#### 🎮 Controls")
        
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; color: rgba(255,255,255,0.4); font-size: 0.75rem; padding: 1rem 0;">
                Powered by LLaMA • Pinecone<br/>
                Made with 💜
            </div>
        """, unsafe_allow_html=True)


def render_chat():
    """Render the main chat interface"""
    # Hero Header
    st.markdown("""
        <div class="hero-header">
            <div class="hero-title">✨ AI Personal Assistant</div>
            <div class="hero-subtitle">Powered by Self-Hosted LLaMA with Intelligent Knowledge Retrieval</div>
            <div class="hero-badge">🚀 Ready to Help</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources if available
            if message.get("sources"):
                st.markdown("---")
                st.markdown("**📚 Knowledge Sources:**")
                for source in message["sources"]:
                    st.markdown(
                        f'<span class="source-chip">📄 {source["source"]} • '
                        f'Relevance: {source["relevance"]:.0%}</span>',
                        unsafe_allow_html=True
                    )
    
    # Chat input
    if prompt := st.chat_input("💬 Ask me anything...", disabled=not st.session_state.api_connected):
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("✨ Thinking..."):
                response = send_message(prompt)
                
                if "error" in response:
                    st.error(f"⚠️ {response['error']}")
                    assistant_message = f"I encountered an issue: {response['error']}"
                else:
                    assistant_message = response.get("response", "I couldn't generate a response.")
                    st.markdown(assistant_message)
                    
                    # Show sources if used
                    sources = response.get("sources", [])
                    if sources and response.get("context_used"):
                        st.markdown("---")
                        st.markdown("**📚 Knowledge Sources:**")
                        for source in sources:
                            st.markdown(
                                f'<span class="source-chip">📄 {source["source"]} • '
                                f'Relevance: {source["relevance"]:.0%}</span>',
                                unsafe_allow_html=True
                            )
                
                # Add assistant message to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message,
                    "sources": response.get("sources") if "error" not in response else None
                })
    
    # Show welcome message if no messages
    if not st.session_state.messages:
        st.markdown("""
            <div class="welcome-box">
                <div class="welcome-icon">🤖</div>
                <div class="welcome-title">Welcome to Your AI Assistant!</div>
                <div class="welcome-text">
                    I'm powered by a self-hosted LLaMA model with intelligent knowledge retrieval. 
                    I can answer questions, help with tasks, and learn from documents you add to the knowledge base.
                </div>
                <div class="feature-grid">
                    <div class="feature-card">
                        <div class="feature-icon">💬</div>
                        <div class="feature-title">Natural Chat</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🧠</div>
                        <div class="feature-title">Smart Context</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📚</div>
                        <div class="feature-title">Knowledge Base</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_search_tab():
    """Render the knowledge search interface"""
    # Hero Header for Search
    st.markdown("""
        <div class="hero-header">
            <div class="hero-title">🔍 Knowledge Search</div>
            <div class="hero-subtitle">Explore and Query Your Personal Knowledge Base</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Search input with style
    search_query = st.text_input(
        "🔎 Search Query",
        placeholder="What would you like to find?",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col2:
        top_k = st.number_input("📊 Results", min_value=1, max_value=20, value=5)
    with col3:
        st.write("")
        search_btn = st.button("🔍 Search", type="primary", use_container_width=True)
    
    if search_btn and search_query:
        with st.spinner("🔍 Searching knowledge base..."):
            results = search_knowledge(search_query, top_k)
            
            if "error" in results:
                st.error(f"⚠️ {results['error']}")
            else:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(17, 153, 142, 0.2) 0%, rgba(56, 239, 125, 0.1) 100%);
                        border: 1px solid rgba(56, 239, 125, 0.3); border-radius: 12px; padding: 1rem; margin: 1rem 0;">
                        <span style="color: #38ef7d; font-weight: 600;">✅ Found {results['total_results']} results</span>
                    </div>
                """, unsafe_allow_html=True)
                
                for i, result in enumerate(results.get("results", []), 1):
                    with st.expander(f"📄 Result #{i} • Relevance: {result['score']:.1%}"):
                        st.markdown(f"""
                            <div style="display: grid; grid-template-columns: auto 1fr; gap: 0.5rem 1rem; margin-bottom: 1rem;">
                                <span style="color: rgba(255,255,255,0.5);">📁 Source:</span>
                                <span style="color: #a5b4fc; font-weight: 500;">{result.get('source', 'Unknown')}</span>
                                <span style="color: rgba(255,255,255,0.5);">🆔 ID:</span>
                                <span style="color: rgba(255,255,255,0.6); font-family: monospace; font-size: 0.85rem;">{result['id']}</span>
                            </div>
                        """, unsafe_allow_html=True)
                        st.markdown("---")
                        st.markdown(result["text"])


def main():
    """Main application entry point"""
    init_session_state()
    
    # Sidebar
    render_sidebar()
    
    # Main content with tabs
    tab1, tab2 = st.tabs(["💬 Chat", "🔍 Search"])
    
    with tab1:
        render_chat()
    
    with tab2:
        render_search_tab()


if __name__ == "__main__":
    main()
