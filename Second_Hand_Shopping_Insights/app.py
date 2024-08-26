import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from poshmark import poshmark_query
from ebay import ebay_query
from depop import depop_query

st.title("Second Hand Insights")
st.write("Originally meant to get from depop and ebay, but depop have restritions is robot.txt and ebay did not really sever the same purpose")
keyword_input = st.text_input("Enter keyword:")

           
st.sidebar.header("Filters")
keyword_input = st.sidebar.text_input("Search Keyword", "")
brand = st.sidebar.text_input("Brand", "")
color = st.sidebar.text_input("Color", "")
size = st.sidebar.text_input("Size", "")
min_price = st.sidebar.number_input("Min Price", min_value=0, value=0)
max_price = st.sidebar.number_input("Max Price", min_value=0, value=1000)

if st.sidebar.button("Search"):
    if keyword_input:
        poshmark_query(keyword_input, brand, color, size, min_price, max_price)
       
        #ebay_query(keyword_input)
        #depop_query(keyword_input)
    else:
        st.write('Please enter a query.')
