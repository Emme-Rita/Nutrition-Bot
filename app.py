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

# --- INIT STATE ---
if "started" not in st.session_state:
    st.session_state.started = False

def start_chat():
    st.session_state.started = True

# --- SIDEBAR ---
st.sidebar.title("Bot Settings")
st.sidebar.write("Adjust settings or view instructions here.")
model_name = st.sidebar.selectbox("Select Model", ["gemini-2.5-flash"])
st.sidebar.markdown("""
*Instructions:*  
- Ask about Cameroonian meals like Achu, Ndolé, Eru, Corn Fufu.  
- The bot will provide ingredients, steps, and nutrition info.
""")

# --- MAIN LOGIC ---
if not st.session_state.started:
    # --- HOME PAGE ---
    st.title("🍲 Welcome to the Local Recipe & Nutrition Bot")
    st.subheader("Discover Authentic Cameroonian Cuisine")
    
    st.markdown("Explore delicious recipes, nutritional facts, and cooking tips from Cameroon.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image("Beignet-Haricot.jpg.webp", caption="Beignet Haricot", use_column_width=True)
    with col2:
        st.image("Fufu-and-Eru.jpg.webp", caption="Fufu and Eru", use_column_width=True)
    with col3:
        st.image("Egusi-Puddingjpg.jpg.webp", caption="Egusi Pudding", use_column_width=True)
    with col4:
        st.image("Koki-1.jpg.webp", caption="Koki", use_column_width=True)

    st.markdown("---")
    st.button("Start Chatting 💬", on_click=start_chat, type="primary")

else:
    # --- MAIN CHAT ---
    col_header, col_home = st.columns([8, 1])
    with col_header:
        st.title("🍲 Local Recipe & Nutrition Bot")
    with col_home:
        if st.button("🏠 Home"):
            st.session_state.started = False
            st.rerun()

    st.write("Type your request below:")

    # Display previous messages
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- USER INPUT ---
    query = st.chat_input("You: ", key="input")

    if query:
        # Show user input
        with st.chat_message("user"):
            st.markdown(query)
        st.session_state.history.append({"role": "user", "content": query})

        with st.spinner("Cooking up your recipe... 🍳"):
            try:
                prompt = f"""
                You are a Cameroonian culinary expert. 
                Only suggest authentic Cameroonian dishes (achu, eru, ndolé, corn fufu, beans cake, koki, puff-puff, etc.).
                User request: {query}
                Respond with:
                1. Meal name
                2. Ingredients
                3. Short recipe (use Cameroonian terms, clear & concise, avoid jargon)
                4. Nutrition info
                Format clearly for display in chat interface using markdown.
                """

                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                answer = response.text

                # Show bot response
                with st.chat_message("assistant"):
                    st.markdown(answer)

                # Save AI response
                st.session_state.history.append({"role": "assistant", "content": answer})

                # Save to JSON
                with open(CHAT_FILE, "w") as f:
                    json.dump(st.session_state.history, f, indent=4)
            except Exception as e:
                st.error(f"Error: {e}")
