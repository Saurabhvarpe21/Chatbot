import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# --- 2. CONFIGURATION & MODERN STYLING ---
st.set_page_config(page_title="Gemini 2.5 Elite", page_icon="🤖", layout="wide")

# Modern UI Colors: Deep Slate Background with Soft Blue Accents
# Modern UI Colors: Light Neutral Background with Clear Dark Text
st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background-color: #f8fafc; /* Very light Gray/White */
        color: #1e293b; /* Dark Slate Blue for text */
    }
    
    /* Input Box Styling */
    .stChatInputContainer {
        padding-bottom: 20px;
        background-color: transparent;
    }

    /* Sidebar Styling - Slight contrast to the main area */
    [data-testid="stSidebar"] {
        background-color: #f1f5f9;
        border-right: 1px solid #e2e8f0;
    }

    /* Headers - Strong Blue for professional look */
    h1, h2, h3 {
        color: #0f172a; 
    }
    
    /* Subheaders and Captions */
    .stMarkdown h5 {
        color: #64748b;
    }

    /* Chat Bubbles - Adding subtle borders for clarity */
    .stChatMessage {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PERSISTENT CLIENT & SESSION ---
if 'genai_client' not in st.session_state:
    st.session_state['genai_client'] = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'chat_session' not in st.session_state:
    # Creating a fresh session using the latest model
    st.session_state['chat_session'] = st.session_state['genai_client'].chats.create(model="gemini-2.5-flash")

# --- 4. SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("⚙️ AI Control Center")
    st.markdown("Use this panel to manage your session.")
    if st.button("🗑️ Clear Conversation"):
        st.session_state['chat_history'] = []
        st.session_state['chat_session'] = st.session_state['genai_client'].chats.create(model="gemini-2.5-flash")
        st.rerun()
    st.divider()
    st.caption("Model: Gemini 2.5 Flash (Verified 2025)")

# --- 5. MAIN CHAT INTERFACE ---
st.title("🚀 Gemini 2.5 Smart Chat")
st.markdown("##### *Your Zero-to-Hero AI Companion*")

# Display history using Streamlit's native chat bubbles (Modern look)
for message in st.session_state['chat_history']:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Handle User Input
if prompt := st.chat_input("Type your message here..."):
    # 1. Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state['chat_history'].append({"role": "user", "text": prompt})

    # 2. Generate and stream Assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Stream the response for better UX
            stream = st.session_state['chat_session'].send_message_stream(prompt)
            for chunk in stream:
                if chunk.text:
                    full_response += chunk.text
                    # Use a cursor symbol during typing
                    response_placeholder.markdown(full_response + "▌")
            
            # Finalize the text
            response_placeholder.markdown(full_response)
            st.session_state['chat_history'].append({"role": "assistant", "text": full_response})
            
        except Exception as e:
            st.error(f"⚠️ Connection Error: {e}")