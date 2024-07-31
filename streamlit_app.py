import streamlit as st


# --- PAGE SETUP ---
about_page = st.Page(
    "views/portfolio.py",
    title="My Portfolio",
    icon=":material/account_circle:",
    default=True,
)
project_1_page = st.Page(
    "views/searchinpaper.py",
    title="Search in Paper",
    icon=":material/bar_chart:",
)
project_2_page = st.Page(
    "views/chatbot.py",
    title="GoGPT",
    icon=":material/smart_toy:",
)

project_3_page = st.Page(
    "views/YoutubeVedioSummarizer.py",
    title="Youtube Vedio Summarizer",
    icon=":material/bar_chart:",
)
project_4_page = st.Page(
    "views/textsummarizer.py",
    title="Text Summarizer",
    icon=":material/bar_chart:",
)



project_6_page = st.Page(
    "views/quiz.py",
    title="Quiz",
    icon=":material/thumb_up:",
)



# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---hello
#pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---

pg = st.navigation(
    {
        "INFO": [about_page],
        "PROJECTS": [project_6_page, project_1_page, project_2_page , project_3_page , project_4_page ],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo("assets/profile Picture.jpg")
st.sidebar.markdown("Copyright © 2024 Gourang Patidar. All Rights Reserved.")


# --- RUN NAVIGATION ---
pg.run()
