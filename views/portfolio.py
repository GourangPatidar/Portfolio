from pathlib import Path

import streamlit as st
from PIL import Image

from forms.contact import contact_form


@st.experimental_dialog("Contact Me")
def show_contact_form():
    contact_form()


# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = "./styles/main.css"
resume_file = "./assets/Resume.pdf"
profile_pic = "./assets/profile Picture.jpg"

# --- GENERAL SETTINGS ---
PAGE_TITLE = "Digital CV | GOURANG PATIDAR"
PAGE_ICON = ":wave:"
NAME = "GOURANG PATIDAR"
DESCRIPTION = """
Building TheQuickAI.com \n
Ex-ML Engineer at Ineuron.ai\n
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
    if st.button("✉️ Contact Me"):
        show_contact_form()
st.write("📫", EMAIL ,)

st.write('\n')
st.subheader("Links", divider="rainbow")

# --- SOCIAL LINKS ---
st.write('\n')
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")






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

# --- JOB 
st.markdown(
    """
    <a href="https://www.thequickai.com/" target="_blank">
        <button >🚧 Building | TheQuickAI.com</button>
    </a>
    """,
    unsafe_allow_html=True
)
st.write("07/2024-Present")
st.write(
    """
- ► Launched a Generative AI SaaS for creating quizzes from four input types (Text , Video url , Blog url , Pdf) , increasing user engagement and content generation efficiency by 40%.
- ► Architected a Cassandra DB solution for the Quiz on Hostinger VPS, achieving 99.9% uptime and enhancing reliability for 1,500+ monthly interactions.
- ► Enabled manual and AI-generated quiz creation, facilitating competitive online assessments with features like auto-grading, and integrated teacher/student dashboards.

"""
)


# --- JOB 1
st.write("🚧", "**Python Mentor | Codeyoung**")
st.write("10/2023 -4/2024")
st.write(
    """
- ► Mentored US students in Python programming at Codeyoung, delivering comprehensive and engaging lessons tailored to their learning needs.
- ► Demonstrated strong communication skills in explaining complex concepts clearly and concisely, contributing to the success of students in mastering Python programming.
"""
)

# --- JOB 2
st.write('\n')
st.write("🚧", "**Machine Learning Engineer | Ineuron.ai**")
st.write("08/2023-09/2023")
st.write(
    """
- ► Achieved 94% accuracy in sentiment analysis on student feedback data using NLTK.
- ► Built predictive models using TensorFlow, reducing forecasting errors by 21%.
- ► Conducted A/B testing on machine learning models to identify optimal model configurations, leading to an 11%
increase in user retention.
"""
)

# --- JOB 3
st.write('\n')
st.write("🚧", "**Data Analyst | Ineuron.ai**")
st.write("10/2022 - 12/2022")
st.write(
    """
- ► Used Python clustering methods to determine groups of states where courses were underperforming, leading to improvements that increased profit by 4%.
- ► Assisted in developing a recommendation engine using collaborative filtering techniques, resulting in a 22% rise in user interaction with recommended listings.

"""
)


# --- Projects & Accomplishments ---
st.write('\n')
st.subheader("Projects ", divider="rainbow")
for project, link in PROJECTS.items():
    st.write(f"[{project}]({link})")
