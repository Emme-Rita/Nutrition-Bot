import streamlit as st
import google.generativeai as genai
import os
import json

# --- CONFIG ---
st.set_page_config(
    page_title="Local Recipe & Nutrition Bot",
    page_icon="🍲",
    layout="wide"
)

# --- GEMINI API ---
GEMINI_API_KEY = "AIzaSyAEWdwr1-Dpuu3cMxLKeLYwMT_cWYBHclI"
api_key = GEMINI_API_KEY
genai.configure(api_key=api_key)

# --- CHAT STORAGE FILE ---
CHAT_FILE = "chat_history.json"

# --- LOAD CHAT HISTORY ---
if "history" not in st.session_state:
    try:
        with open(CHAT_FILE, "r") as f:
            st.session_state.history = json.load(f)
    except FileNotFoundError:
        st.session_state.history = []

# --- SIDEBAR ---
st.sidebar.title("Bot Settings")
st.sidebar.write("Adjust settings or view instructions here.")
model_name = st.sidebar.selectbox("Select Model", ["gemini-2.5-flash"])
st.sidebar.markdown("""
*Instructions:*  
- Ask about Cameroonian meals like Achu, Ndolé, Eru, Corn Fufu.  
- The bot will provide ingredients, steps, and nutrition info.
""")

# --- MAIN CHAT ---
st.title("🍲 Local Recipe & Nutrition Bot")
st.write("Type your request below:")

# Display previous messages
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# --- USER INPUT ---
query = st.chat_input("You: ", key="input")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    # Save user message
    st.session_state.history.append({"role": "user", "content": query})

    with st.spinner("Cooking up suggestions... 🍳"):
        try:
            prompt = f"""
            You are a Cameroonian culinary expert. 
            Only suggest authentic Cameroonian dishes (achu, eru, ndolé, corn fufu, beans cake, koki, puff-puff, etc.).
            User request: {query}
            Respond with:
            1. Meal name
            2. Ingredients
            3. Short recipe and use cameroonian terms be clear n concise avoid jargons
            4. Nutrition info
            Format clearly for display in chat interface. use markdown format to display response in a neat way
            """

            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            answer = response.text
            # Display AI response (left side)
            with st.chat_message("assistant"):
                st.markdown(answer)

            # Save AI response
            st.session_state.history.append({"role": "assistant", "content": answer})

            # Append to session history
            # st.session_state.history.append({"user": query, "bot": answer})

            # Save to JSON
            with open(CHAT_FILE, "w") as f:
                json.dump(st.session_state.history, f, indent=4)
        except Exception as e:
            st.error(f"Error: {e}")

# --- DISPLAY CHAT HISTORY ---
for chat in st.session_state.history:
    st.markdown(f"*You:* {chat['user']}")
    st.markdown(f"*Bot:* {chat['bot']}")
    st.markdown("---")