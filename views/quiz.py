import json
import requests
import streamlit as st
from PyPDF2 import PdfReader
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
from openai import OpenAI

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
        response = requests.get(url)
        with open('temp.pdf', 'wb') as f:
            f.write(response.content)
        text = get_pdf_text('temp.pdf')
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = '\n'.join([p.get_text() for p in paragraphs])
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

# Function to split text into smaller chunks
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

# Function to generate quiz questions
def generate_quiz_questions(inputs):
    prompt = f"""
    Please list {inputs['num_questions']} quiz questions in {inputs['language']} on the following subject for {inputs['schooling_level']} and difficulty level of the quiz should be {inputs['level']}.
    Cover all of the topics given in the content while making questions.
    Include only the following types of questions: {inputs['question_types']}.
    Return the data in JSON format exactly matching this schema:

    [
        {{
            "question": "str",
            "options": "list",
            "answer": "list" if type == "multiple_select" else "str",
            "type": "str",  # Indicating question type (multiple_choice / true_false / numeric / theory / multiple_select)
            "explanation": "str"  # Add an explanation for the answer
        }}
    ]

    Subject Content:
    {inputs['subject']}
    """

    try:
        response = OpenAI(api_key=OPENAI_API_KEY).completions.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=1500,
        )
        return json.loads(response.choices[0].text.strip())
    except Exception as e:
        st.error(f"Error generating quiz questions: {str(e)}")
        return []

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
            questions = generate_quiz_questions(inputs)
            all_questions.extend(questions)

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
                    'explanation': question.get('explanation'),
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
