import streamlit as st
from google import genai

# Page config
st.set_page_config(page_title="Health Assistant Bot", page_icon="🩺")

# Title
st.title("🩺 AI Health Assistant")
st.caption("For general health guidance only. Not a medical diagnosis.")

# API Key
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# System prompt (VERY IMPORTANT)
SYSTEM_PROMPT = """
You are a polite, professional AI health assistant.
Rules:
- Give only general health and wellness advice.
- Do NOT diagnose diseases.
- Do NOT prescribe medicines.
- Always suggest consulting a doctor for serious issues.
- Be calm, supportive, and clear.
"""

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask your health question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=SYSTEM_PROMPT + "\nUser: " + user_input
        )
        st.markdown(response.text)

    st.session_state.messages.append(
        {"role": "assistant", "content": response.text}
    )

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This chatbot provides **general health guidance** only.
    
    ❌ No diagnosis  
    ❌ No prescriptions  
    ✅ Wellness tips  
    ✅ Preventive care advice
    """)
