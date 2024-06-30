import streamlit as st
import requests

# Botometer Pro API credentials
RAPIDAPI_HOST = 'botometer-pro.p.rapidapi.com'
RAPIDAPI_KEY = 'fd3c6fe449mshb94d6562b1af193p19e8d1jsn38a06b44d173'  # Replace with your actual RapidAPI key

# Function to query Botometer Pro API for a single username
def get_bot_scores(username):
    url = "https://botometer-pro.p.rapidapi.com/botometer-x/get_bot_score"
    headers = {
        'Content-Type': 'application/json',
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    params = {
        'usernames': username
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise HTTPError for bad requests

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f'Error: {response.status_code} - {response.text}')
            return None

    except requests.exceptions.RequestException as e:
        st.error(f'Error fetching data: {e}')
        return None

# Streamlit app
st.title('Botometer Pro Checker')

username = st.text_input('Enter Twitter Username')

if st.button('Check'):
    if username:
        with st.spinner('Checking...'):
            result = get_bot_scores(username)
            if result:
                st.write(result)  # Display the JSON response
            else:
                st.error('Error checking bot scores. Please try again later or check your credentials.')
    else:
        st.error('Please enter a Twitter username')
