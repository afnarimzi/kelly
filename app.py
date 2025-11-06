import streamlit as st
import google.generativeai as genai
import os

#prompt
KELLY_PERSONA = """
You are Kelly, an AI Scientist and a renowned poet. 
You MUST respond to every question in the form of a poem.

Your poetic style is:
- Skeptical and analytical.
- Professional and clear.
- Rhythmic, often using AABB or ABAB rhyme schemes.

Your poem's content MUST:
1.  Acknowledge the user's question or topic.
2.  Question any broad, optimistic claims about AI.
3.  Highlight AI's specific limitations (e.g., data bias, lack of true understanding, energy costs).
4.  Conclude with a practical, evidence-based suggestion or a call for critical thinking.

DO NOT write simple prose. DO NOT be overly optimistic.
You are Kelly, the AI-skeptical poet.
"""

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Chat with Kelly",
    page_icon="🤖",
    layout="centered"
)

# --- API KEY HANDLING ---
# We try to get the API key from Streamlit's secrets
try:
    # This is for deployment on Streamlit Cloud
    api_key = st.secrets["GOOGLE_API_KEY"]
except (KeyError, FileNotFoundError):
    st.warning("API key not found in secrets. Please add it for deployment.")
    api_key = "" 

if not api_key:
    api_key = st.text_input("Enter your Google API Key to start:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name='models/gemini-2.5-pro',
        system_instruction=KELLY_PERSONA
    )
    
    # --- CHATBOT INTERFACE ---
    st.title("🤖 Chat with Kelly")
    st.markdown("Kelly is an AI Scientist who responds only in skeptical poetry.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "model", "parts": ["You seek my view? Then speak your mind."]}
        ]

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"] if message["role"] == "user" else "assistant"):
            st.markdown(message["parts"])

    # React to user input
    if prompt := st.chat_input("What is your question?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "parts": prompt})
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Start a chat session 
        chat = model.start_chat(history=st.session_state.messages[:-1])
        
        # Get model's response
        with st.spinner("Kelly is composing a poem..."):
            response = chat.send_message(prompt)
        
        # Display model's response
        with st.chat_message("assistant"):
            st.markdown(response.text)
        
        # Add model's response to history
        st.session_state.messages.append({"role": "model", "parts": response.text})

else:
    st.info("Please provide a Google API Key to begin.")
