def get_custom_css():
    return """
    <style>
    /* Simple yellow background */
    .stApp {
        background-color: #f5d547;
    }
    
    /* Content area with white background */
    .main .block-container > div {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    /* Header styling */
    h1 {
        color: #2c3e50;
        border-bottom: 2px solid #f39c12;
        padding-bottom: 10px;
    }
    
    h2, h3 {
        color: #34495e;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #f39c12;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    
    .stButton > button:hover {
        background-color: #e67e22;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: rgba(255, 255, 255, 0.9);
    }
    </style>
    """


def apply_custom_css():
    import streamlit as st
    st.markdown(get_custom_css(), unsafe_allow_html=True)
