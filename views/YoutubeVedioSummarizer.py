import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_openai import ChatOpenAI
from langchain import LLMChain, PromptTemplate

# OpenAI API key (replace with your own)
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
llm = ChatOpenAI(api_key=OPENAI_API_KEY)
template="you are the youtube video summarizer , given text you have to summarize the content"
llm_chain = LLMChain(llm=llm, prompt=PromptTemplate( template=template))
# Function to extract video ID from YouTube URL
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

# Function to get video transcript from YouTube
def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ' '.join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        st.error(f"Error fetching transcript: {str(e)}")
        return None

# Function to summarize video transcript using OpenAI API
def summarize_video_transcript(video_id):
    transcript_text = get_video_transcript(video_id)
    return llm_chain.run(transcript_text)

# Streamlit UI

st.title('YouTube Video Summarizer')
    
    # Input for YouTube URL
youtube_url = st.text_input('Enter YouTube URL:', '')
    
if st.button('Summarize'):
    if youtube_url:
        video_id = extract_video_id(youtube_url)
        if video_id:
            summary = summarize_video_transcript(video_id)
            if summary:
                st.subheader('Summary:')
                st.write(summary)
            else:
                st.warning('Failed to summarize transcript.')
        else:
            st.warning('Invalid YouTube URL. Please enter a valid URL.')
    else:
        st.warning('Please enter a YouTube URL.')


