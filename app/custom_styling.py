"""
Custom CSS styling for Recipe Recommender application
Includes professional cooking-themed background
"""

def get_custom_css():
    """Return custom CSS for the Recipe Recommender application."""
    return """
    <style>
    /* Main background styling */
    .stApp {
        background: linear-gradient(135deg, #f5d547 0%, #f2b545 100%);
        background-attachment: fixed;
    }
    
    /* Kitchen-themed background pattern */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3Ccircle cx='15' cy='45' r='1'/%3E%3Ccircle cx='45' cy='15' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        background-size: 60px 60px;
        z-index: -1;
        opacity: 0.3;
    }
    
    /* Blue kitchen tile header */
    .main .block-container {
        padding-top: 80px;
        position: relative;
    }
    
    .main .block-container::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 80px;
        background: linear-gradient(90deg, #4a90a4 0%, #5ba4c2 100%);
        background-image: 
            repeating-linear-gradient(0deg, transparent, transparent 10px, rgba(255,255,255,0.1) 10px, rgba(255,255,255,0.1) 11px),
            repeating-linear-gradient(90deg, transparent, transparent 10px, rgba(255,255,255,0.1) 10px, rgba(255,255,255,0.1) 11px);
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    /* Kitchen utensils decoration */
    .main .block-container::after {
        content: "🍳";
        position: fixed;
        top: 25px;
        right: 30px;
        font-size: 30px;
        z-index: 1001;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
    }
    
    /* Content area styling */
    .main .block-container > div {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
    }
    
    /* Header styling */
    h1 {
        color: #2c3e50;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        border-bottom: 3px solid #f39c12;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    h2, h3 {
        color: #34495e;
        margin-top: 25px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-right: 3px solid #f39c12;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #f39c12, #e67e22);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(243, 156, 18, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(243, 156, 18, 0.4);
        background: linear-gradient(45deg, #e67e22, #d35400);
    }
    
    /* Success/Info/Warning styling */
    .stSuccess {
        background: rgba(46, 204, 113, 0.1);
        border-left: 4px solid #2ecc71;
        border-radius: 5px;
    }
    
    .stInfo {
        background: rgba(52, 152, 219, 0.1);
        border-left: 4px solid #3498db;
        border-radius: 5px;
    }
    
    .stWarning {
        background: rgba(241, 196, 15, 0.1);
        border-left: 4px solid #f1c40f;
        border-radius: 5px;
    }
    
    /* Metric styling */
    .metric-container {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #f39c12;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #2c3e50;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #f39c12, #e67e22);
        color: white !important;
    }
    
    /* Image styling */
    .stImage > img {
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(45deg, #f39c12, #e67e22);
    }
    
    /* Selectbox and input styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        border: 2px solid #ecf0f1;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        border: 2px solid #ecf0f1;
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        border: 2px dashed #f39c12;
        padding: 20px;
    }
    
    /* Camera input styling */
    .stCameraInput {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 15px;
        border: 2px solid #f39c12;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        border-left: 4px solid #f39c12;
    }
    
    /* Column styling for better layout */
    .element-container {
        margin-bottom: 15px;
    }
    
    /* Custom ingredient card styling */
    .ingredient-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #27ae60;
        transition: transform 0.3s ease;
    }
    
    .ingredient-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Recipe card styling */
    .recipe-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #e74c3c;
        transition: transform 0.3s ease;
    }
    
    .recipe-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Loading spinner styling */
    .stSpinner > div {
        border-top-color: #f39c12 !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container > div {
            padding: 20px;
            margin: 10px;
        }
        
        .main .block-container::after {
            right: 15px;
            font-size: 24px;
        }
    }
    </style>
    """

def apply_custom_css():
    """Apply custom CSS to the Streamlit app."""
    import streamlit as st
    st.markdown(get_custom_css(), unsafe_allow_html=True)
