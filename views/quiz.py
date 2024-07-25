import json
from langchain.llms import OpenAI as LangChainOpenAI
from langchain_openai import ChatOpenAI
from langchain import LLMChain, PromptTemplate
from PyPDF2 import PdfReader
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import requests


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
def extract_text_from_url(url):
    if url.endswith('.pdf'):
        # Extract text from PDF
        response = requests.get(url)
        with open('temp.pdf', 'wb') as f:
            f.write(response.content)
        text = get_pdf_text('temp.pdf')
    elif url.startswith('https://www.youtube.com/'):
        # Extract text from YouTube video transcript
        video_id = url.split('v=')[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ' '.join([t['text'] for t in transcript])
    elif url.startswith('https://'):
        # Extract text from web content (assuming it's a blog or article)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = '\n'.join([p.get_text() for p in paragraphs])
    else:
        text = ""  # Handle other types of URLs as needed
    return text

# Initialize OpenAI language model
openai_model = ChatOpenAI(api_key=OPENAI_API_KEY)

# Define the prompt template for generating quiz questions
template = """
Using the following JSON schema,
Please list {num_questions} quiz questions in {language} on {subject} for {schooling_level} and difficulty level of the quiz should be {level} and of type {question_type} .
Make sure to return the data in JSON format exactly matching this schema.
Recipe = {{
    "question": "str",
    "options": "list",
    "answer": "str",
    "type": "str",  # Add a type field for indicating question type (multiple_choice / true_false / numeric / etc.)
    "explanation": "str"  # Add an explanation for the answer
}} 
Return: list[Recipe]

example:
[
    {{
        "question": "What is the largest ocean in the world?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"],
        "answer": "Pacific Ocean",
        "type": "multiple_choice",
        "explanation": "The Pacific Ocean is the largest and deepest ocean on Earth."
    }},
    {{
        "question": " J.K. Rowling is the author of the Harry Potter series.",
        "options": ["True", "False"],
        "answer": "True",
        "type": "true_false",
        "explanation": "J.K. Rowling is indeed the author of the Harry Potter series."
    }},
    
]
"""

# Initialize LangChain LLMChain with the prompt template
llm_chain = LLMChain(llm=LangChainOpenAI(api_key=OPENAI_API_KEY), prompt=PromptTemplate(input_variables=["num_questions", "language", "subject", "schooling_level", "level", "question_type"], template=template))

# Streamlit app setup
st.title("Quiz Generator")
subject=""

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

elif input_type == "Blog URL" or input_type == "Video URL":
    url = st.text_input(f"Enter {input_type} URL")
    
    if st.button("Fetch Content"):
        if url:
            subject = extract_text_from_url(url).strip()
            st.write(subject)
        else:
            st.warning("Please enter a valid URL.")

schooling_level = st.selectbox("Schooling Level", ["Primary", "Secondary", "High School", "College", "University"])
num_questions = st.number_input("Number of Questions", min_value=1, max_value=20, step=1)
level = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard", "Expert"])
language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Chinese", "Hindi"])
question_type = st.selectbox("Question Type", ["Multiple Choice", "True/False", "Both"])

# Mapping question type selection to LangChain template input
if question_type == "Multiple Choice":
    type_filter = "multiple_choice"
elif question_type == "True/False":
    type_filter = "true_false"
else:
    type_filter = "both"

if st.button("Generate Quiz"):
    # Ensure subject is not empty before generating the quiz
    if subject:
        # Generate the prompt inputs
        inputs = {
            "num_questions": num_questions,
            "language": language,
            "subject": subject,
            "schooling_level": schooling_level,
            "level": level,
            "question_type": type_filter  # Pass the selected question type to LangChain
        }

        # Generate the quiz using LangChain
        try:
            raw_response = llm_chain.run(inputs)
            st.write("Raw Response:", raw_response)  # Print raw response for debugging

            # Attempt to parse JSON
            data = json.loads(raw_response)

            # Filter questions based on selected type before saving to session_state
            filtered_questions = []
            for question in data:
                if type_filter == "both" or question["type"] == type_filter:
                    filtered_questions.append(question)

            st.session_state.questions = filtered_questions
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
        st.write(f"Q{idx}: {question['question']}")
        if question['type'] == "multiple_choice":
            options = question['options']
            user_answers[idx] = st.radio(f"Select an answer for Q{idx}:", options)
        elif question['type'] == "true_false":
            options = ["True", "False"]
            user_answers[idx] = st.radio(f"True or False for Q{idx}:", options)

    if st.button("Submit Quiz"):
        score = 0
        results = []

        for idx, question in enumerate(st.session_state.questions, start=1):
            correct_answer = question['answer']
            user_answer = user_answers.get(idx)
            is_correct = user_answer == correct_answer
            if is_correct:
                score += 1
            results.append({
                'question': question['question'],
                'correct_answer': correct_answer,
                'user_answer': user_answer,
                'is_correct': is_correct,
                'explanation': question['explanation'] if 'explanation' in question else None
            })

        st.header("Results")
        for result in results:
            st.write(f"Question: {result['question']}")
            st.write(f"Correct Answer: {result['correct_answer']}")
            st.write(f"Your Answer: {result['user_answer']}")
            st.write("Explanation: " + result['explanation'] if result['explanation'] else "No explanation provided.")
            st.write("Correct!" if result['is_correct'] else "Incorrect.")
            st.write("---")

        st.write(f"Your score: {score} out of {len(st.session_state.questions)}")
