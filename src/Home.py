import streamlit as st

st.set_page_config(
    page_title="Trung Dan Phan - Data Science Portfolio",
    page_icon="🤖",
)

st.write("# Welcome to my Data Science Portfolio! 👋")

st.sidebar.success("Select a project above.")

st.markdown(
    """
    Hello! My name is Trung Dan Phan. As a Master's student at Ecole Polytechnique & HEC Paris, 
    I've worked on several projects related to Data Science. 
    I am using Streamlit to share interactive previews of different projects.
    
    **👈 Select a demo from the sidebar** to see some projects I've been working on!
    
    ### Links
    - Check out my [GitHub page](https://streamlit.io)
    - Check out my [LinkedIn profile](https://www.linkedin.com/in/trung-dan-phan/)
    - Check out my [Master's program](https://www.hec.edu/en/master-s-programs/specialized-masters/master-science-data-science-ai-business)

    *TODO:* Homework for the HEC course 'Tooling for Data Scientist' by Ghislain Mazars.
"""
)
