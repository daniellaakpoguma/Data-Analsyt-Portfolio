import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Multipage App"
)

# Read the contents of styles.css
with open('styles.css') as f:
    css = f.read()

# Embed the CSS styles into the Streamlit app
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title("Home Page")
st.sidebar.success("Select a page above")

st.markdown("""
    This is a multi-page Streamlit app containing a dashboard and a web scraper.

    - Dashboard
    - Web Scraper
    """)

st.markdown("""
### Dataset Description
This dataset contains information related to buyer reviews and evaluations of products, gathered from AliExpress. 
The data includes various attributes that provide insights into the sentiment, feedback, and interaction surrounding product evaluations.
""")

if "dataset" not in st.session_state:
    st.session_state.dataset = pd.read_csv("C:\\Users\\rukev\\OneDrive\\Desktop\\Data Analsyt Portfolio\\Data-Analsyt-Portfolio\\Data Sets\\Online Retail Business\\OnlineRetail.csv", encoding='latin1')

st.subheader("Dataset Preview")
st.write(st.session_state.dataset)