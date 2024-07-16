import streamlit as st

# Title
st.title("Social Media Dashboard")

# Grid Layout
cols = st.columns(3)  # Adjusted to 3 columns
platforms = ["Facebook", "Instagram", "Twitter", "LinkedIn", "YouTube", "Pinterest"]  # List of platforms

# Display platform boxes
for i, platform in enumerate(platforms):
    with cols[i % 3]:  # Use modulo to wrap around columns
        with st.expander(platform):
            st.write(f"This is the {platform} container.")
            st.button(f"See General Metrics", key=f"button_{platform}")

option = st.selectbox(
   "What would you like to focus on today?",
   ("Best Time to Post", "Video Duration Performance", "Content Type Preference", "Hashtag Effectiveness", "Audience Demographics", "Engagement Trends"),
   index=None,
   placeholder="Select contact method...",
)



