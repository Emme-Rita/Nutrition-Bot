import streamlit as st
import google.generativeai as genai
import os
import json
import uuid

# --- CONFIG ---
st.set_page_config(
    page_title="Local Recipe & Nutrition Bot",
    page_icon="🍲",
    layout="wide"
)

# --- CUSTOM SIDEBAR WIDTH ---
# --- CUSTOM SIDEBAR WIDTH & STYLE ---
st.markdown(
    """
    <style>
        /* Sidebar width */
        [data-testid="stSidebar"] {
            min-width: 320px;
            max-width: 320px;
        }
        [data-testid="stSidebar"] .block-container {
            padding-left: 15px;
            padding-right: 15px;
        }

        /* Chat title buttons */
        [data-testid="stSidebar"] button {
            background-color: transparent !important;
            text-align: left;
            padding: 5px;
            width: 100%;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: 14px;
            cursor: pointer;
        }
        [data-testid="stSidebar"] button:hover {
            background-color: #f0f0f0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --- GEMINI API ---
GEMINI_API_KEY = "AIzaSyAEWdwr1-Dpuu3cMxLKeLYwMT_cWYBHclI"
# GEMINI_API_KEY = os.getenv(GEMINI_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

# --- USER ACCOUNT ---
if "username" not in st.session_state:
    st.session_state.username = "guest"

# --- CHAT STORAGE ---
DATA_DIR = "chats"
os.makedirs(DATA_DIR, exist_ok=True)

def user_file():
    return os.path.join(DATA_DIR, f"{st.session_state.username}_chats.json")

# Load user’s chats
if "chats" not in st.session_state:
    try:
        with open(user_file(), "r") as f:
            st.session_state.chats = json.load(f)
    except FileNotFoundError:
        st.session_state.chats = {}

# Pick active chat
if "active_chat" not in st.session_state:
    st.session_state.active_chat = None

# --- SIDEBAR ---
st.sidebar.title("🍲 Recipe Bot")

# Account info
st.sidebar.text_input("Your Name", key="username")

st.sidebar.markdown("---")
st.sidebar.subheader("💬 Your Chats")

# New Chat button
if st.sidebar.button("➕ New Chat"):
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": []
    }
    st.session_state.active_chat = chat_id

# Display chat list
for cid, chat in st.session_state.chats.items():
    if st.sidebar.button(chat["title"], key=cid):
        st.session_state.active_chat = cid

st.sidebar.markdown("---")
st.sidebar.write(f"👤 Logged in as: **{st.session_state.username}**")

# --- MAIN AREA ---
st.title("🍲 Local Recipe & Nutrition Bot")

if not st.session_state.active_chat:
    st.subheader("Popular Cameroonian Dishes")

    # Create 4 equal-width columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("Fufu-and-Eru.jpg.webp", caption="Fufu & bitterleaf", use_column_width=True)

    with col2:
        st.image("Koki-1.jpg.webp", caption="Koki and ripe plantains", use_column_width=True)

    with col3:
        st.image("Egusi-Puddingjpg.jpg.webp", caption="Egusi Pudding", use_column_width=True)

    with col4:
        st.image("Beignet-Haricot.jpg.webp", caption="Beignet & Haricot (Achombo)", use_column_width=True)
    st.subheader("Ready to cook cameroonian dishes?")

    st.info("Start a new chat from the sidebar or visit old chats ➕")
    

else:
    chat = st.session_state.chats[st.session_state.active_chat]

    # Display history
    for msg in chat["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    query = st.chat_input("Ask about Cameroonian food recipes...")

    if query:
        # Add user message
        chat["messages"].append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        # Bot response
        with st.spinner("Cooking up suggestions... 🍳"):
            try:
                prompt = f"""
                You must *never* provide information unrelated to food, nutrition, or cooking.
                You are a Cameroonian culinary expert
                Suggest authentic Cameroonian dishes (achu, eru, ndolé, corn fufu, beans cake, koki, puff-puff, etc.).
                User request: {query} and if given dietary restrictions generate the recipe with respect to the diets and respond in teh language of the query 
                Respond with:
                1. Meal name 
                2. cultural background
                3. Ingredients
                4. Short recipe (Cameroonian terms, clear, concise, no jargon)
                5. Nutritional information
                Use markdown for formatting.
                """
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                answer = response.text

                chat["messages"].append({"role": "assistant", "content": answer})
                with st.chat_message("assistant"):
                    st.markdown(answer)

            except Exception as e:
                st.error(f"Error: {e}")

        # Rename chat title after first user message
        if chat["title"] == "New Chat":
            chat["title"] = query[:30] + ("..." if len(query) > 30 else "")

        # Save chats
        with open(user_file(), "w") as f:
            json.dump(st.session_state.chats, f, indent=4)
