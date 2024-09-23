import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from poshmark import poshmark_query
from ebay import ebay_query


st.title("Poshmark Insights")
st.write("Instructions: Enter keyword in input box below, and 1000 results gotten from the Poshmark website will be downloaded onto your local computer")
keyword_input = st.text_input("Enter keyword:")

if st.button("Search"):
    if keyword_input:
        poshmark_query(keyword_input)
       
    else:
        st.write('Please enter a query.')
