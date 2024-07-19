import streamlit as st
'''
from forms.contact import contact_form


@st.experimental_dialog("Contact Me")
def show_contact_form():
    contact_form()

'''
# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/profile Picture.jpg", width=230)

with col2:
    st.title("GOURANG PATIDAR", anchor=False)
    st.write(
        "EX-ML intern at Ineuron.ai"
    )
    #if st.button("✉️ Contact Me"):
        #show_contact_form()


# --- EXPERIENCE & QUALIFICATIONS ---
st.write("\n")
st.subheader("Education ", anchor=False)
st.write(
    """
    - Jabalpur Engineering College , B.Tech in Artificial Intelligenge and Data Science , 2021-2025
    - Macro Vision Academy, Burhanpur , class 11th -12th , 2019-2021
    """
)

# --- SKILLS ---
st.write("\n")
st.subheader("Skills", anchor=False)
st.write(
    """
    - Data Analytics:- Numpy , PowerBi , MS-Excel ,MYSQL , Pandas ,Matplotlib and Seaborn
    - Machine Learning: Python ,Scikit-learn , AWS , AZURE ,ML Algorithms ,Statistics & Probability
    - Deep Learning: Natural Language Processing ,Computer Vision, Tensorflow , Keras , Neural Networks , Mathematics and Linear Algebra
    - GenAI- Langchain , Llama Index , OpenAI , Gemini Pro
    """
)