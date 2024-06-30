import streamlit as st

# Set the title of your Streamlit app
st.title("Customer Feedback")
st.markdown("""## Social Analyzer""")
# Display a brief description
st.write("Social Analyzer - API, CLI, and Web App for analyzing & finding a person's profile across +1000 social media websites. It includes different analysis and detection modules, and you can choose which modules to use during the investigation process.")

# Instructions for downloading and installing Python
st.write("1. Download & Install Python")
st.write("Download and install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/)")

# Instructions for downloading and extracting the social analyzer repository
st.write(" 2. Download & Extract Social Analyzer")
st.write("Download and extract the Social Analyzer repository from [https://github.com/qeeqbox/social-analyzer/archive/main.zip](https://github.com/qeeqbox/social-analyzer/archive/main.zip)")

# Instructions for installing social-analyzer package
st.write("3. Install Social Analyzer Package")
st.code("pip install social-analyzer")

# Instructions for running social-analyzer
st.write("4, Run Social Analyzer")
example_command = 'python3 -m social-analyzer --username "johndoe" --metadata'
st.code(example_command)


# Instructions
st.markdown("""## SocialMediaScraper""")

st.write("The SocialMediaScraper project on GitHub is a tool that allows users to scrape data from various social media platforms, including Facebook, Twitter, and Instagram. The project is written in Python and uses a combination of web scraping techniques and APIs to gather information such as user profiles, posts, and comments. The collected data can then be exported to a CSV file for further analysis.")
st.write("Instructions to Set Up Social Media Scraper")

st.write("1. Fork/Clone/Download this repo")
st.code("git clone https://github.com/Hotmansifu/SocialMediaScraper.git")

st.write("2. Navigate to the directory")
st.code("cd SocialMediaScraper")

st.write("3. Run ./install.sh")
st.code("./install.sh")

st.write("4. Set permissions for start.sh in Terminal")
st.code("chmod 777 start.sh")

st.write("5. Run the start.sh script in an interactive prompt")
st.code("./start.sh")

