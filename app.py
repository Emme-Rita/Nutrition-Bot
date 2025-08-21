import streamlit as st
import google.generativeai as genai
import os
GEMINI_API_KEY = "AIzaSyAEWdwr1-Dpuu3cMxLKeLYwMT_cWYBHclI"
# --- CONFIG ---
st.set_page_config(page_title="Local Recipe & Nutrition Bot", page_icon="🍲")

# Get API key (set as environment variable in Streamlit Cloud)
# api_key = os.getenv("GEMINI_API_KEY")
api_key = GEMINI_API_KEY

if not api_key:
    st.error("⚠ No Gemini API key found. Please set GEMINI_API_KEY in your environment.")
else:
    genai.configure(api_key=api_key)

    # Title
    st.title("🍲 Local Recipe & Nutrition Bot")
    st.write("Ask me for local meals and I’ll suggest recipes + nutrition info!")

    # User input
    query = st.text_input("What meal or type of food are you craving?")

    if query:
        with st.spinner("Cooking up suggestions... 🍳"):
            try:
                # Call Gemini model
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = f"""
                Suggest a local Cameroonian/African meal based on this request: {query}.
                Provide:
                1. Meal name
                2. ingredients
                3. Short recipe (4–8 steps)
                4. Nutrition info (calories, carbs, protein, vitamins)
                Format clearly.
                """
                response = model.generate_content(prompt)
                st.success(response.text)
            except Exception as e:
                st.error(f"Error: {e}")