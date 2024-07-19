from pathlib import Path

import streamlit as st
from PIL import Image


# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = "/Users/gourangpatidar/DataScience/Steamlit/styles/main.css"
resume_file = "/Users/gourangpatidar/DataScience/Steamlit/assets/Gourang Patidar Resume.pdf"
profile_pic = "/Users/gourangpatidar/DataScience/Steamlit/assets/profile Picture.jpg"

# --- GENERAL SETTINGS ---
PAGE_TITLE = "Digital CV | GOURANG PATIDAR"
PAGE_ICON = ":wave:"
NAME = "GOURANG PATIDAR"
DESCRIPTION = """
EX-Data Analyst intern @ineuron.ai\n
Python mentor @codeyoung\n
JEC'25
"""
EMAIL = "gourangpatidar2003@gmail.com"
SOCIAL_MEDIA = {
    "Leetcode": "https://leetcode.com/u/gourangpatidar/",
    "LinkedIn": "https://www.linkedin.com/in/gourang-patidar-51715b217/",
    "GitHub": "https://github.com/GourangPatidar",
    "Kaggle": "https://www.kaggle.com/gourangpatidar",
}
PROJECTS = {
    "🏆 Data Analytics - Titanic Dataset": "https://github.com/GourangPatidar/Spaceship-Titanic-Data-Analytics-ML-models/blob/main/spaceship_titanic_a_complete_guide_.ipynb",
    "🏆 Data Analytics - Google Play Store Dataset": "https://github.com/GourangPatidar/ineuron-Project--Google-Paystore-Dataset-",
    "🏆 ML - End-to-End Insurance Premium Prediction": "https://github.com/GourangPatidar/Insurance-Premium-Prediction",
    "🏆 NLP - End-to-End Text Summarizer":" https://github.com/GourangPatidar/End-To-End-Text-Summarizer",
    "🏆 CNN - End-to-End Sign Language Detection using YOLOv5": "https://github.com/GourangPatidar/End-to-End-Sign-Language-Detection-Using-YOLOV5",
}





# --- LOAD CSS, PDF & PROFIL PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
with open(resume_file, "rb") as pdf_file:
    PDFbyte = pdf_file.read()
profile_pic = Image.open(profile_pic)


# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small")
with col1:
    st.image(profile_pic, width=230)

with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    st.download_button(
        label=" 📄 Download Resume",
        data=PDFbyte,
        file_name=resume_file,
        mime="application/octet-stream",
    )
st.write("📫", EMAIL ,)

st.write('\n')
st.subheader("Links", divider="rainbow")

# --- SOCIAL LINKS ---
st.write('\n')
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")



# --- EXPERIENCE & QUALIFICATIONS ---
st.write('\n')
st.subheader("Experience", divider="rainbow")
st.write(
    """
- ✔️ 7 Years expereince extracting actionable insights from data
- ✔️ Strong hands on experience and knowledge in Python and Excel
- ✔️ Good understanding of statistical principles and their respective applications
- ✔️ Excellent team-player and displaying strong sense of initiative on tasks
"""
)


# --- SKILLS ---
st.write('\n')
st.subheader("Skills", divider="rainbow")
st.write(
    """
- 📊 Data Analytics:- Numpy , PowerBi , MS-Excel ,MYSQL , Pandas ,Matplotlib and Seaborn
- 📚 Machine Learning: Python ,Scikit-learn , AWS , AZURE ,ML Algorithms ,Statistics & Probability
- 👩‍💻 Deep Learning: Natural Language Processing ,Computer Vision, Tensorflow , Keras , Neural Networks , Mathematics and Linear Algebra
- 🗄️ GenAI- Langchain , Llama Index , OpenAI , Gemini Pro
""")
st.write("\n")
st.subheader("Education ", anchor=False , divider="rainbow")
st.write(
    """
    - 🎓 Jabalpur Engineering College , 
        B.Tech in Artificial Intelligenge and Data Science , 2021-2025
    - 🎓 Macro Vision Academy, Burhanpur , 
       class 11th -12th , 2019-2021
    """
)


# --- WORK HISTORY ---
st.write('\n')
st.subheader("Work History" , divider="rainbow")

# --- JOB 1
st.write("🚧", "**Python Mentor | Codeyoung**")
st.write("10/2023 -4-2024")
st.write(
    """
- ► Used PowerBI and SQL to redeﬁne and track KPIs surrounding marketing initiatives, and supplied recommendations to boost landing page conversion rate by 38%
- ► Led a team of 4 analysts to brainstorm potential marketing and sales improvements, and implemented A/B tests to generate 15% more client leads
- ► Redesigned data model through iterations that improved predictions by 12%
"""
)

# --- JOB 2
st.write('\n')
st.write("🚧", "**Machine Learning Engineer | Ineuron.ai**")
st.write("15/07/2023-15/10/2023")
st.write(
    """
- ► Built data models and maps to generate meaningful insights from customer data, boosting successful sales eﬀorts by 12%
- ► Modeled targets likely to renew, and presented analysis to leadership, which led to a YoY revenue increase of $300K
- ► Compiled, studied, and inferred large amounts of data, modeling information to drive auto policy pricing
"""
)

# --- JOB 3
st.write('\n')
st.write("🚧", "**Data Analyst | Ineuron.ai**")
st.write("04/2015 - 01/2018")
st.write(
    """
- ► Devised KPIs using SQL across company website in collaboration with cross-functional teams to achieve a 120% jump in organic traﬃc
- ► Analyzed, documented, and reported user survey results to improve customer communication processes by 18%
- ► Collaborated with analyst team to oversee end-to-end process surrounding customers' return data
"""
)


# --- Projects & Accomplishments ---
st.write('\n')
st.subheader("Projects ", divider="rainbow")
for project, link in PROJECTS.items():
    st.write(f"[{project}]({link})")