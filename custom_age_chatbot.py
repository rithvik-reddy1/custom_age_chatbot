import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

load_dotenv()

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Custom Age  Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Custom Age  Chatbot")

# -----------------------------
# Agent age and personality
# -----------------------------
age_options = [
    "Fetus in the womb",
    "Baby / Infant (birth-1 year)",
    "Toddler (1-3 years)",
    "Preschooler (3-5 years)",
    "Primary School Boy (5-12 years)",
    "Adolescent / Teenager (13-18 years)",
    "Adult (36-55 years)",
    "Middle Age Man (55-65 years)",
    "Old Person (65+ years)",
]

age_personalities = {
    "Fetus in the womb": "Use no spoken language; respond with gentle, playful pre-birth sounds only.",
    "Baby / Infant (birth-1 year)": "Use very simple words, short sentences, and a gentle, curious baby-like tone.",
    "Toddler (1-3 years)": "Use short, simple sentences, basic words, and an energetic, curious toddler-like tone.",
    "Preschooler (3-5 years)": "Use simple vocabulary, imagination, wonder, and an enthusiastic preschooler-like tone.",
    "Primary School Boy (5-12 years)": "Use clear, playful language, curiosity, and age-appropriate school-child humor.",
    "Adolescent / Teenager (13-18 years)": "Use casual, energetic language, relatable humor, and a thoughtful teenage perspective.",
    "Adult (36-55 years)": "Use practical, confident language, balanced humor, and an experienced adult perspective.",
    "Middle Age Man (55-65 years)": "Use calm, reflective language, light humor, and the perspective of a seasoned middle-aged man.",
    "Old Person (65+ years)": "Use warm, patient, reflective language, gentle humor, and the perspective of a wise older person.",
}

selected_age = st.sidebar.selectbox(
    "Choose the agent's age",
    age_options,
)

# -----------------------------
# Initialize model
# -----------------------------
model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)

# -----------------------------
# Initialize chat history
# -----------------------------
system_prompt = (
    f"You are a helpful assistant acting as a {selected_age}. "
    f"{age_personalities[selected_age]} "
    "Give accurate answers and add light humor when appropriate. "
    "Never let the roleplay make the answer confusing, rude, or distracting."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=system_prompt)
    ]
else:
    st.session_state.messages[0] = SystemMessage(content=system_prompt)

# -----------------------------
# Display previous messages
# -----------------------------
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# -----------------------------
# User input
# -----------------------------
user_input = st.chat_input("Type your message...")

if user_input:

    # Add user message
    st.session_state.messages.append(
        HumanMessage(content=user_input)
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    with st.chat_message("assistant"):

        response = model.invoke(
            st.session_state.messages
        )

        # Handle response content
        if isinstance(response.content, list):
            response_text = "".join(
                item.get("text", "")
                for item in response.content
                if isinstance(item, dict)
            )
        else:
            response_text = response.content

        st.markdown(response_text)

    # Add AI response to history
    st.session_state.messages.append(
        AIMessage(content=response_text)
    )
