# Q&A Chatbot
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage , AIMessage, chat
from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()
#from dotenv import load_dotenv

#load_dotenv()  # take environment variables from .env.

import streamlit as st
import os

openai_api_key=st.secrets["OPENAI_API_KEY"]
## Function to load OpenAI model and get respones
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages']=[
        SystemMessage(content="Yor are a helpful AI assitant")
    ]

def get_openai_response(question):
    llm=ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.7 , openai_api_key=openai_api_key)
    st.session_state['flowmessages'].append(HumanMessage(content=question))
    answer=llm(st.session_state['flowmessages'])
    st.session_state['flowmessages'].append(AIMessage(content=answer.content))
    return answer.content

##initialize our streamlit app

#st.set_page_config(page_title="Conversational Q&A Chatbot")

st.header("Langchain Application : Q/A Chatbot" , divider='rainbow')
st.subheader("by Gourang Patidar : :sunglasses:")

input=st.text_input("Input: ",key="input")
response=get_openai_response(input)

submit=st.button("chat")

## If ask button is clicked

if submit:
    st.subheader("The Response is")
    st.write(response)