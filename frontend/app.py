import streamlit as st

# Page configuration
st.set_page_config(page_title='Local Recipe & Nutrition Bot', layout='wide')

# Sidebar
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Home', 'Recipes', 'Nutrition Advice', 'About'])

# Home Page
if page == 'Home':
    st.title('Welcome to the Local Recipe & Nutrition Bot')
    st.subheader('Discover affordable local recipes and get nutritional advice')
    st.image('https://images.unsplash.com/photo-1504674900247-0877df9cc836', use_container_width=True)

# Recipes Page
elif page == 'Recipes':
    st.title('Local Recipes')
    recipe_list = ['Achu Soup', 'Ndolé', 'Corn Fufu', 'Beans Cake']
    selected_recipe = st.selectbox('Select a recipe', recipe_list)
    st.write(f'You selected: {selected_recipe}')
    st.write('Here is a simple way to prepare it:')
    st.text_area('Recipe Steps', 'Step 1: ...\nStep 2: ...\nStep 3: ...')

# Nutrition Advice Page
elif page == 'Nutrition Advice':
    st.title('Nutrition Advice')
    ingredient = st.text_input('Enter a local ingredient')
    if ingredient:
        st.write(f'Nutrition facts and health benefits of {ingredient}:')
        st.text_area('Details', 'Calories: ...\nProteins: ...\nVitamins: ...')

# About Page
elif page == 'About':
    st.title('About this Bot')
    st.write('This bot suggests affordable local recipes and provides nutritional advice.')
    st.write('Built with Python and Streamlit.')
