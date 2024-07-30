import json
from langchain.llms import OpenAI as LangChainOpenAI
from langchain_openai import ChatOpenAI
from langchain import LLMChain, PromptTemplate
from PyPDF2 import PdfReader
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import requests
from fpdf import FPDF

css_file = "./styles/main.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

# Load OpenAI API key from Streamlit secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Function to extract text from PDF file
def get_pdf_text(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from URL (PDF, blog, or video transcript)
def extract_text_from_blog_url(url):
    if url.endswith('.pdf'):
        # Extract text from PDF
        response = requests.get(url)
        with open('temp.pdf', 'wb') as f:
            f.write(response.content)
        text = get_pdf_text('temp.pdf')
    elif url.startswith('https://'):
        # Extract text from web content (assuming it's a blog or article)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = '\n'.join([p.get_text() for p in paragraphs])
        text = text[50:-200]
    else:
        text = ""  # Handle other types of URLs as needed
    return text

def extract_video_id(url):
    # Check if the URL contains 'youtu.be/' format
    if 'youtu.be/' in url:
        video_id_index = url.index('youtu.be/') + len('youtu.be/')
        video_id = url[video_id_index:].split('?')[0]
        return video_id
    # Check if the URL contains 'watch?v=' format
    elif 'watch?v=' in url:
        video_id_index = url.index('watch?v=') + len('watch?v=')
        video_id = url[video_id_index:].split('&')[0]
        return video_id
    # If the URL format is not recognized
    else:
        return None

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ' '.join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        print(f"Error fetching transcript: {str(e)}")
        return None

def sanitize_text(text):
            return text.encode('latin1', 'replace').decode('latin1')


# Initialize OpenAI language model
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")

# Define the prompt template for generating quiz questions
template = """
Using the following JSON schema,
Please list {num_questions} quiz questions in {language} on {subject} for {schooling_level} and difficulty level of the quiz should be {level}.
Cover all of the topics given in the content while making questions.
Include only the following types of questions: {question_types}.
Make sure to return the data in JSON format exactly matching this schema.
Recipe = {{
    "question": "str",
    "options": "list",
    "answer": "list" if type == "multiple_select" else "str",
    "type": "str",  # Indicating question type (single_select / true_false / numeric / theory / multiple_select)
    "explanation": "str"  # Add an explanation for the answer
}}
Return: list[Recipe]

example:
[
    {{
        "question": "What is the largest ocean in the world?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"],
        "answer": "Pacific Ocean",
        "type": "single_select",
        "explanation": "The Pacific Ocean is the largest and deepest ocean on Earth."
    }},
    {{
        "question": " J.K. Rowling is the author of the Harry Potter series.",
        "options": ["True", "False"],
        "answer": "True",
        "type": "true_false",
        "explanation": "J.K. Rowling is indeed the author of the Harry Potter series."
    }},
    {{
        "question": "What is 5 + 3?",
        "options": [],
        "answer": "8",
        "type": "numeric",
        "explanation": "The sum of 5 and 3 is 8."
    }},
    {{
        "question": "Explain the theory of relativity.",
        "options": [],
        "answer": "The theory of relativity is a scientific concept describing the relationship between space, time, and gravity.",
        "type": "theory",
        "explanation": "Einstein's theory of relativity includes both the special relativity and general relativity principles."
    }},
    {{
        "question": "Which of the following are programming languages?",
        "options": ["Python", "HTML", "Java", "CSS"],
        "answer": ["Python", "Java"],
        "type": "multiple_select",
        "explanation": "Python and Java are programming languages, while HTML and CSS are markup and style sheet languages, respectively."
    }}
]
"""

# Initialize LangChain LLMChain with the prompt template
llm_chain = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=["num_questions", "language", "subject", "schooling_level", "level", "question_types"], template=template))

# Streamlit app setup
st.title("Quiz Generator")
subject = ""

# User inputs
input_type = st.selectbox("Input Type", ["Text", "PDF", "Blog URL", "Video URL"])

if input_type == "PDF":
    uploaded_files = st.file_uploader("Upload PDF file(s)", type=["pdf"], accept_multiple_files=True)
    
    pdf_text = ""
    if uploaded_files:
        for file in uploaded_files:
            pdf_text += get_pdf_text(file)
    subject = pdf_text.strip()

elif input_type == "Text":
    input_text = st.text_area("Enter Text")
    subject = input_text.strip()

elif input_type == "Blog URL":
    try:
        url = st.text_input(f"Enter {input_type} URL")
    except:
        st.warning("please provide a valid url")
    
    subject = extract_text_from_blog_url(url)
elif input_type == "Video URL":
    url = st.text_input(f"Enter {input_type} URL")
    video_id = extract_video_id(url)
    subject = get_video_transcript(video_id)

schooling_level = st.selectbox("Schooling Level", ["Primary", "Secondary", "High School", "College", "University"])
num_questions = st.number_input("Number of Questions", min_value=1, max_value=20, step=1)
level = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard", "Expert"])
language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Chinese", "Hindi"])

question_types = st.multiselect("Question Types", ["single_select", "true_false", "numeric", "theory", "multiple_select"], default=["single_select"])

if st.button("Generate Quiz"):
    with st.spinner("Generating quiz..."):
        # Ensure subject is not empty before generating the quiz
        if subject:
            # Generate the prompt inputs
            inputs = {
                "num_questions": num_questions,
                "language": language,
                "subject": subject,
                "schooling_level": schooling_level,
                "level": level,
                "question_types": ", ".join(question_types)
            }

            # Generate the quiz using LangChain
            try:
                raw_response = llm_chain.run(inputs)
            
                # Debugging output: print raw response
                

                # Extract JSON part from response
                json_start_idx = raw_response.find("[")
                json_end_idx = raw_response.rfind("]")
                if (json_start_idx != -1 and json_end_idx != -1):
                    json_response = raw_response[json_start_idx:json_end_idx + 1]
                    data = json.loads(json_response)
                else:
                    raise ValueError("No JSON part found in response")

                # Check if the number of questions generated is less than requested
                if len(data) < num_questions:
                    st.warning(f"Only {len(data)} questions were generated. You may want to adjust the parameters.")

                # Filter questions based on selected type before saving to session_state
                sorted_data = []
                for qtype in question_types:
                    sorted_data.extend([q for q in data if q['type'] == qtype])
                st.session_state.questions = sorted_data
                st.success("Quiz generated successfully!")
            except json.JSONDecodeError as e:
                st.error(f"Error decoding JSON from response: {e}")
                st.error(f"Raw response: {raw_response}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
        else:
            st.warning("Please provide content (text, PDF, blog URL, or video URL) before generating the quiz.")

if 'questions' in st.session_state:
    st.header("Quiz")
    user_answers = {}

    for idx, question in enumerate(st.session_state.questions, start=1):
        st.write(f"**Q{idx}: {question['question']}**")
        if question['type'] == "single_select":
            options = question['options']
            user_answers[idx] = st.radio(f"Select one answer for Q{idx}:", options)
        elif question['type'] == "true_false":
            options = ["True", "False"]
            user_answers[idx] = st.radio(f"Select True or False for Q{idx}:", options)
        elif question['type'] == "multiple_select":
            options = question['options']
            user_answers[idx] = st.multiselect(f"Select one or more answers for Q{idx}:", options)
        elif question['type'] == "numeric":
            user_answers[idx] = st.number_input(f"Enter a numeric answer for Q{idx}:", value=0)
        elif question['type'] == "theory":
            user_answers[idx] = st.text_area(f"Write your answer for Q{idx}:")

    if st.button("Submit Quiz"):
        with st.spinner("Grading quiz..."):
            # Generate quiz results
            correct_answers = 0
            results = []

            for idx, question in enumerate(st.session_state.questions, start=1):
                correct_answer = question['answer']
                user_answer = user_answers.get(idx)

                if isinstance(correct_answer, list):
                    correct = set(user_answer) == set(correct_answer)
                else:
                    correct = user_answer == correct_answer

                result = {
                    "question": question['question'],
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "explanation": question['explanation'],
                    "correct": correct
                }
                results.append(result)

                if correct:
                    correct_answers += 1

            score = (correct_answers / len(st.session_state.questions)) * 100
            st.success(f"You scored {score}%")

            # Display results with correct answers, explanations, user answers, and correct/incorrect status
            st.header("Results")
            for result in results:
                st.write(f"**Question:** {result['question']}")
                st.write(f"**Your Answer:** {result['user_answer']}")
                st.write(f"**Correct Answer:** {result['correct_answer']}")
                st.write(f"**Explanation:** {result['explanation']}")
                st.write(f"**Status:** {'Correct' if result['correct'] else 'Incorrect'}")
                st.write("---")

            # Generate PDF with questions
    download = st.selectbox("Download/share", ["PDF", "share"], placeholder="Choose an option")
    if download=="PDF":

        st.sidebar.header("Question Paper Details")
        school_name = st.sidebar.text_input("School/College Name", "Example School")
        exam_title = st.sidebar.text_input("Exam Title", "Mid-Term Examination")
        exam_time = st.sidebar.text_input("Time Allowed", "2 hours")
        total_marks = st.sidebar.text_input("Total Marks", "50")
        topic=st.sidebar.text_input("Subject" , "Machine Learning")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial","BU", size=16)
        

        pdf.cell(0, 10, txt=school_name, ln=True, align="C")
        pdf.cell(0, 10, txt=exam_title, ln=True, align="C")
        pdf.cell(0, 10, txt=f"Subject : {topic}", ln=True, align="C")
        pdf.cell(0, 10, txt="", ln=True)
        pdf.set_font("Arial","B", size=12)

        # Add header information (smaller text)
        # Add header information (smaller text) on the same line
        
        pdf.cell(0, 10, txt=f"TIME : {exam_time}", ln=False, align="L")
        pdf.cell(0, 10, txt=f"MAXIMUM MARKS {total_marks}", ln=True, align="R")
        pdf.cell(0, 10, txt="--------------------------------------------------------------------------------------------------------------------------------------", ln=True)    
        pdf.cell(0, 10, txt="", ln=True)
        for idx, question in enumerate(st.session_state.questions, start=1):
            pdf.set_font("Arial", 'B', size=12)
            pdf.cell(0, 10, txt=sanitize_text(f"Q{idx}: {question['question']}"), ln=True)
            
            pdf.set_font("Arial", size=12)
            if question['type'] in ["single_select", "multiple_select", "true_false"]:
                for option in question['options']:
                    pdf.cell(0, 10, txt=sanitize_text(f"- {option}"), ln=True)
                    
            pdf.cell(0, 10, txt="", ln=True)  # Add an empty line between questions

        pdf_output = pdf.output(dest='S').encode('latin1')
        st.download_button(
            label="Download Questions PDF",
            data=pdf_output,
            file_name="quiz_questions.pdf",
            mime="application/pdf",
        )

        # Generate PDF with questions and answers
        pdf_answers = FPDF()
        pdf_answers.add_page()
        pdf_answers.set_font("Arial","BU", size=16)


        pdf_answers.cell(200, 10, txt="Questions with Answers", ln=True, align="C")
        pdf_answers.cell(0, 10, txt=school_name, ln=True, align="C")
        pdf_answers.cell(0, 10, txt=exam_title, ln=True, align="C")
        pdf_answers.cell(0, 10, txt=f"Subject : {topic}", ln=True, align="C")
        pdf_answers.cell(0, 10 , txt="" , ln=True)
        pdf_answers.set_font("Arial","B", size=12)


        # Add header information (smaller text)
        # Add header information (smaller text) on the same line
        
        pdf_answers.cell(0, 10, txt=f"TIME : {exam_time}", ln=False, align="L")
        pdf_answers.cell(0, 10, txt=f"MAXIMUM MARKS {total_marks}", ln=True, align="R")
        pdf_answers.cell(0, 10, txt="--------------------------------------------------------------------------------------------------------------------------------------", ln=True)  # Add an empty line after header
        pdf_answers.cell(0, 10 , txt="" , ln=True)


        for idx, question in enumerate(st.session_state.questions, start=1):
            pdf_answers.set_font("Arial", 'B', size=12)
            pdf_answers.cell(0, 10, txt=sanitize_text(f"Q{idx}: {question['question']}"), ln=True)
            pdf_answers.set_font("Arial", size=12)
            if question['type'] in ["single_select", "multiple_select", "true_false"]:
                for option in question['options']:
                    pdf_answers.cell(0, 10, txt=sanitize_text(f"- {option}"), ln=True)
            pdf_answers.cell(0, 10, txt=f"Answer: {question['answer']}", ln=True)
            pdf_answers.cell(0, 10, txt=f"Explanation: {question['explanation']}", ln=True)
            pdf_answers.cell(0, 10, txt="", ln=True)  # Add an empty line between questions

        pdf_answers_output = pdf_answers.output(dest='S').encode('latin1')
        st.download_button(
            label="Download Questions with Answers PDF",
            data=pdf_answers_output,
            file_name="quiz_questions_with_answers.pdf",
            mime="application/pdf",
        )
    elif download=="share":
        st.write("this functionality is not implemented yet !")
        st.button("share quiz with a link")


