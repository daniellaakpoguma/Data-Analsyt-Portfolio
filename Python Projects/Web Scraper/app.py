import streamlit as st
from streamlit_option_menu import option_menu
from home import show_home
from scraper import show_scraper


st.set_page_config(
    page_title="Mulitpage App"
)

# Create a sidebar for navigation
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Dashboard", "Scraper"],
        icons=["house", "search"],
        menu_icon="cast",
        default_index=0,
    )

# Show the selected page
if selected == "Home":
    show_home()
elif selected == "Scraper":
    show_scraper()
