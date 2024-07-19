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
    title="Search in Research Paper",
    icon=":material/bar_chart:",
)
project_2_page = st.Page(
    "views/chatbot.py",
    title="Chat Bot",
    icon=":material/smart_toy:",
)

project_3_page = st.Page(
    "views/YoutubeVedioSummarizer.py",
    title="Youtube Vedio Summarizer",
    icon=":material/bar_chart:",
)


# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "INFO": [about_page],
        "PROJECTS": [project_1_page, project_2_page, project_3_page],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo("assets/profile Picture.jpg")
st.sidebar.markdown("Made by gourang patidar")


# --- RUN NAVIGATION ---
pg.run()