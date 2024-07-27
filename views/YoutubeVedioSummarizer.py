import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # Load environment variables if needed, not used in this example
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi


css_file = "./styles/paper_css.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

# Configure Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Use os.getenv for environment variables

# Function to extract video ID from YouTube URL
def extract_video_id(url):
    # Check if the URL contains 'youtu.be/' format
    if 'youtu.be/' in url:
        video_id_index = url.index('youtu.be/') + len('youtu.be/')
        video_id = url[video_id_index:]
        return video_id
    # Check if the URL contains 'watch?v=' format
    elif 'watch?v=' in url:
        video_id_index = url.index('watch?v=') + len('watch?v=')
        video_id = url[video_id_index:]
        return video_id
    # If the URL format is not recognized
    else:
        return None

# Function to get video transcript from YouTube
def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ' '.join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        st.error(f"Error fetching transcript: {str(e)}")
        return None

# Function to generate summary using Google Gemini Pro API with language selection
def generate_gemini_content(transcript_text, prompt, language, word_count):
    try:
        if language == "English":
            model = genai.GenerativeModel("gemini-pro")
        elif language == "Hindi":
            model = genai.GenerativeModel("gemini-pro-hindi")
        else:
            st.warning("Language not supported.")
            return None
        
        response = model.generate_content(prompt.format(word_count=word_count) + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None

# Streamlit UI
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

# Dropdown for selecting summary language
language = st.selectbox("Select Summary Language:", ["English", "Hindi"])

# Dropdown for selecting word count
word_count_options = [100, 200, 250, 400]
word_count = st.selectbox("Select Word Count for Summary:", word_count_options)

if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/default.jpg", use_column_width=True)
    else:
        st.warning("Please enter a valid YouTube video link.")

if st.button("Get Detailed Notes"):
    if youtube_link:
        video_id = extract_video_id(youtube_link)
        if video_id:
            transcript_text = get_video_transcript(video_id)
            if transcript_text:
                # English and Hindi prompts for summary
                prompt_english = """Hello, I am your YouTube video summarizer. I will take the transcript text and summarize the entire video, providing an important summary within {word_count} words. Please provide the summary of the text given here: """
                prompt_hindi = """नमस्कार, मैं आपका YouTube वीडियो सारांशकर्ता हूं। मैं ट्रांसक्रिप्ट पाठ को लेकर वीडियो का सारांश दूंगा, {word_count} शब्दों के भीतर महत्वपूर्ण सारांश प्रदान करें। कृपया दिए गए पाठ का सारांश प्रदान करें: """

                if language == "English":
                    summary = generate_gemini_content(transcript_text, prompt_english, language, word_count)
                elif language == "Hindi":
                    summary = generate_gemini_content(transcript_text, prompt_hindi, language, word_count)
                
                if summary:
                    st.markdown("## Detailed Notes:")
                    st.write(summary)
                else:
                    st.warning("Failed to generate detailed notes.")
            else:
                st.warning("Failed to fetch transcript.")
        else:
            st.warning("Invalid YouTube URL. Please enter a valid URL.")
    else:
        st.warning("Please enter a YouTube URL.")
