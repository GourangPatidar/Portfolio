import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # Load environment variables if needed, not used in this example
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

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
def generate_gemini_content(transcript_text, prompt, language):
    try:
        if language == "English":
            model = genai.GenerativeModel("gemini-pro")
        elif language == "Chinese":
            model = genai.GenerativeModel("gemini-pro-chinese")
        else:
            st.warning("Language not supported.")
            return None
        
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None

# Streamlit UI
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

# Dropdown for selecting summary language
language = st.selectbox("Select Summary Language:", ["English", "Chinese"])

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
                # English prompt for summary
                prompt_english = """Hello, I am your YouTube video summarizer. I will take the transcript text and summarize the entire video, providing an important summary within {word_count} words. Please provide the summary of the text given here: """

                # Replace {word_count} placeholder with a default value or user input if needed
                word_count = 150

                summary = generate_gemini_content(transcript_text, prompt_english.format(word_count=word_count), language)
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
