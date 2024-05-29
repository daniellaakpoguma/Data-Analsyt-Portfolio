import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Multipage App"
)


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

Below is a brief description of each column:

- **buyerName:** The name or identifier of the buyer who submitted the evaluation.
- **buyerCountry:** The country of the buyer who submitted the evaluation.
- **Evaluation:** The evaluation or rating given by the buyer for the product.
- **buyerFeedback:** The textual feedback provided by the buyer regarding their experience with the product.
- **buyerProductFeedBack:** Specific feedback related to the product's features or performance.
- **buyerTranslationFeedback:** Feedback related to translation services if applicable.
- **downVoteCount:** The count of downvotes received for the evaluation.
- **upVoteCount:** The count of upvotes received for the evaluation.
- **evalData:** Date of the evaluation.
- **evaluationId:** Unique identifier for each evaluation.
- **responsiveness:** Evaluation of the product's responsiveness.
- **warrantyService:** Evaluation of the product's warranty service.
- **functionality:** Evaluation of the product's functionality.
- **status:** Status of the evaluation or review.

This dataset provides valuable insights into buyer sentiments, preferences, and experiences with products. Researchers and analysts can use this data for sentiment analysis, product performance evaluation, and market research purposes.
""")

df = pd.read_csv("C:\\Users\\rukev\\OneDrive\\Desktop\\Data Analsyt Portfolio\\Data-Analsyt-Portfolio\\Data Sets\\AliExpress Product Reviews\\Reviews.csv")
st.subheader("Dataset Preview")
st.write(df)