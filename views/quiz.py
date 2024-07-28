import json
import requests
import streamlit as st
from PyPDF2 import PdfReader
from langchain.llms import OpenAI as LangChainOpenAI
from langchain_openai import ChatOpenAI
from langchain import LLMChain, PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup

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
        text = '\n.join([p.get_text() for p in paragraphs])
        text = text[50:-200]
    else:
        text = ""  # Handle other types of URLs as needed
    return text

def extract_video_id(url):
    if 'youtu.be/' in url:
        video_id_index = url.index('youtu.be/') + len('youtu.be/')
        video_id = url[video_id_index:]
        return video_id
    elif 'watch?v=' in url:
        video_id_index = url.index('watch?v=') + len('watch?v=')
        video_id = url[video_id_index:]
        return video_id
    else:
        return None

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ' '.join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        st.error(f"Error fetching transcript: {str(e)}")
        return None

# Initialize OpenAI language model
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4")

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
    "type": "str",  # Indicating question type (multiple_choice / true_false / numeric / theory / multiple_select)
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

# User inputs
input_type = st.selectbox("Input Type", ["Text", "PDF", "Blog URL", "Video URL"])

subject = ""
if input_type == "PDF":
    uploaded_files = st.file_uploader("Upload PDF file(s)", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            subject += get_pdf_text(file)
elif input_type == "Text":
    input_text = st.text_area("Enter Text")
    subject = input_text.strip()
elif input_type == "Blog URL":
    url = st.text_input("Enter Blog URL")
    if url:
        subject = extract_text_from_blog_url(url)
elif input_type == "Video URL":
    url = st.text_input("Enter Video URL")
    if url:
        video_id = extract_video_id(url)
        if video_id:
            subject = get_video_transcript(video_id)

schooling_level = st.selectbox("Schooling Level", ["Primary", "Secondary", "High School", "College", "University"])
num_questions = st.number_input("Number of Questions", min_value=1, max_value=20, step=1)
level = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard", "Expert"])
language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Chinese", "Hindi"])
question_types = st.multiselect("Question Types", ["multiple_choice", "true_false", "numeric", "theory", "multiple_select"], default=["multiple_choice", "true_false", "numeric", "theory"])

def split_text_into_chunks(text, max_length=2000):
    words = text.split()
    chunks = []
    current_chunk = []
    for word in words:
        if len(" ".join(current_chunk + [word])) > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
        else:
            current_chunk.append(word)
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

if st.button("Generate Quiz"):
    if subject:
        chunks = split_text_into_chunks(subject)
        all_questions = []
        progress_bar = st.progress(0)

        for i, chunk in enumerate(chunks):
            progress_bar.progress((i + 1) / len(chunks))
            inputs = {
                "num_questions": min(num_questions, 5),  # Limiting the number of questions per chunk
                "language": language,
                "subject": chunk,
                "schooling_level": schooling_level,
                "level": level,
                "question_types": ", ".join(question_types)
            }
            try:
                raw_response = llm_chain.run(inputs)
                json_start_idx = raw_response.find("[")
                json_end_idx = raw_response.rfind("]")
                if json_start_idx != -1 and json_end_idx != -1:
                    json_response = raw_response[json_start_idx:json_end_idx + 1]
                    data = json.loads(json_response)
                    all_questions.extend(data)
                else:
                    raise ValueError("No JSON part found in response")
            except json.JSONDecodeError as e:
                st.error(f"Error decoding JSON from response: {e}")
                st.error(f"Raw response: {raw_response}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

        st.session_state.questions = all_questions

        st.header("Generated Quiz")
        user_answers = {}
        for idx, question in enumerate(st.session_state.questions, start=1):
            st.write(f"Q{idx}: {question['question']}")
            if question['type'] == "multiple_choice":
                options = question['options']
                user_answers[idx] = st.radio(f"Select an answer for Q{idx}:", options)
            elif question['type'] == "true_false":
                options = ["True", "False"]
                user_answers[idx] = st.radio(f"Select True or False for Q{idx}:", options)
            elif question['type'] == "numeric":
                user_answers[idx] = st.number_input(f"Enter a numeric answer for Q{idx}:", step=1)
            elif question['type'] == "theory":
                user_answers[idx] = st.text_area(f"Enter your answer for Q{idx}:")
            elif question['type'] == "multiple_select":
                options = question['options']
                user_answers[idx] = st.multiselect(f"Select one or more answers for Q{idx}:", options)

        if st.button("Submit Quiz"):
            results = []
            score = 0
            for idx, question in enumerate(st.session_state.questions, start=1):
                correct_answer = question['answer']
                user_answer = user_answers.get(idx)
                if question['type'] == 'theory':
                    is_correct = None
                elif question['type'] == 'multiple_select':
                    is_correct = set(user_answer) == set(correct_answer)
                else:
                    is_correct = user_answer == correct_answer
                if is_correct:
                    score += 1
                results.append({
                    'question': question['question'],
                    'correct_answer': correct_answer,
                    'user_answer': user_answer,
                    'is_correct': is_correct,
                    'explanation': question['explanation'] if 'explanation' in question else None,
                    'type': question['type']
                })

            st.header("Results")
            for result in results:
                st.write(f"Question: {result['question']}")
                st.write(f"Correct Answer: {result['correct_answer']}")
                st.write(f"Your Answer: {result['user_answer']}")
                st.write(f"Explanation: {result['explanation']}" if result['explanation'] else "No explanation provided.")
                if result['type'] != 'theory':
                    st.write("Correct!" if result['is_correct'] else "Incorrect.")
                st.write("---")

            non_theory_questions = [q for q in results if q['type'] != 'theory']
            if non_theory_questions:
                st.write(f"Your score: {score} out of {len(non_theory_questions)}")
    else:
        st.warning("Please provide content for the quiz generation.")
