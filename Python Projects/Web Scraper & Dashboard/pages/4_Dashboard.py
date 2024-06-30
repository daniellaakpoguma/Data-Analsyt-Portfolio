import streamlit as st
import pandas as pd
import plotly.express as px

# Load data from CSV file
@st.cache
def load_data():
    # Replace 'your_dataset.csv' with the path to your CSV file
    df = pd.read_csv('amazon_prime_users.csv')
    return df

df = load_data()

# Streamlit app layout
st.title("User Dashboard")

# Sidebar filters
st.sidebar.title("Filters")
selected_gender = st.sidebar.selectbox('Select Gender:', ['All'] + df['Gender'].unique().tolist())
selected_plan = st.sidebar.selectbox('Select Subscription Plan:', ['All'] + df['Subscription Plan'].unique().tolist())
selected_city = st.sidebar.selectbox('Select Location:', ['All'] + df['Location'].unique().tolist())

# Apply filters
filtered_df = df.copy()
if selected_gender != 'All':
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]
if selected_plan != 'All':
    filtered_df = filtered_df[filtered_df['Subscription Plan'] == selected_plan]
if selected_city != 'All':
    filtered_df = filtered_df[filtered_df['Location'] == selected_city]

# Show filtered data
st.write(f"Showing data for Gender: {selected_gender}, Subscription Plan: {selected_plan}, Location: {selected_city}")
st.write(filtered_df)

# Display charts
st.subheader("Data Visualization")

col = st.columns((3.5,6.5), gap='medium')
with col[0]:
    # Subscription Plan Distribution
    st.write("Subscription Plan Distribution:")
    plan_counts = filtered_df['Subscription Plan'].value_counts()
    st.bar_chart(plan_counts)

    # Usage Frequency Distribution
    st.write("Usage Frequency Distribution:")
    usage_hist = px.histogram(filtered_df, x='Usage Frequency', nbins=20)
    st.plotly_chart(usage_hist)


with col[1]:
    # Interactive Scatter Plot (Engagement Metrics vs Feedback/Ratings)
    st.write("Interactive Scatter Plot: Engagement Metrics vs Feedback/Ratings")
    scatter_fig = px.scatter(filtered_df, x='Engagement Metrics', y='Feedback/Ratings', color='Subscription Plan', hover_data=['Name'])
    st.plotly_chart(scatter_fig)

    # Interactive Line Plot (Usage Frequency over Time)
    st.write("Interactive Line Plot: Usage Frequency over Time")
    line_fig = px.line(filtered_df, x='Membership Start Date', y='Usage Frequency', color='Gender')
    st.plotly_chart(line_fig)

    # Update other charts based on hover or selection in the scatter plot
    selected_points = st.sidebar.multiselect('Select points on scatter plot:', filtered_df.index.tolist())
    selected_data = filtered_df.loc[selected_points]

# Update other charts based on the selected points
if selected_points:
    st.write("Data for selected points:")
    st.write(selected_data)

    with col[0]:
        # Update Subscription Plan Distribution
        plan_counts_selected = selected_data['Subscription Plan'].value_counts()
        st.write("Subscription Plan Distribution for selected points:")
        st.bar_chart(plan_counts_selected)

        # Update Usage Frequency Distribution
        usage_hist_selected = px.histogram(selected_data, x='Usage Frequency', nbins=20)
        st.write("Usage Frequency Distribution for selected points:")
        st.plotly_chart(usage_hist_selected)

    with col[1]:
        # Update Line Plot
        line_fig_selected = px.line(selected_data, x='Membership Start Date', y='Usage Frequency', color='Gender')
        st.write("Usage Frequency over Time for selected points:")
        st.plotly_chart(line_fig_selected)
