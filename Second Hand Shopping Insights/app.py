import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from poshmark import poshmark_query
from ebay import ebay_query


st.title("Second Hand Insights")
st.write("Originally meant to get from depop and ebay, but depop have restritions is robot.txt and ebay did not really sever the same purpose")
keyword_input = st.text_input("Enter keyword:")

if st.button("Search"):
    if keyword_input:
        poshmark_query(keyword_input)
       
    else:
        st.write('Please enter a query.')
