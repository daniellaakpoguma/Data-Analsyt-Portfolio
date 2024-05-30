import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt

st.title("Dashboard")

# Load Data
df = pd.read_csv("C:\\Users\\rukev\\OneDrive\\Desktop\\Data Analsyt Portfolio\\Data-Analsyt-Portfolio\\Data Sets\\Food and Services Drinking PLaces\\21100232.csv")

# Sidebar filters
years = st.sidebar.multiselect("Select Years", df["REF_DATE"].unique())
establishments = st.sidebar.multiselect("Select Establishments", df["North American Industry Classification System (NAICS)"].unique())

# Filter the data
filtered_df = df[(df["REF_DATE"].isin(years)) & (df["North American Industry Classification System (NAICS)"].isin(establishments))]

# Create line graph using Plotly Express
fig = px.line(filtered_df, x="REF_DATE", y="VALUE", color="North American Industry Classification System (NAICS)")

# Update layout
fig.update_layout(title="Total Sales Trends", xaxis_title="Date", yaxis_title="Total Sales")

# Show the plot
st.plotly_chart(fig)

# st.header("Total Sales Trends")
# total_sales = filtered_df.groupby(["REF_DATE", "North American Industry Classification System (NAICS)"])["VALUE"].sum().reset_index()

# if total_sales.empty:
#     st.write("No data available for the selected filters.")


# st.header("E-commerce Sales Comparison")
# ecommerce_sales_col = [col for col in filtered_df.columns if 'E-commerce' in col.lower()]
# if ecommerce_sales_col:
#     ecommerce_sales = filtered_df.pivot_table(index="REF_DATE", columns="North American Industry Classification System (NAICS)", values=ecommerce_sales_col[0], aggfunc="sum")
#     st.area_chart(ecommerce_sales)
# else:
#     st.write("E-commerce sales data not found.")

# # Percentage of E-commerce Sales
# st.header("Percentage of E-commerce Sales")
# if ecommerce_sales_col:
#     percentage_ecommerce = (ecommerce_sales / total_sales) * 100
#     st.bar_chart(percentage_ecommerce)
# else:
#     st.write("E-commerce sales data not found.") 




