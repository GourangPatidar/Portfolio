# LangChain components to use
import os

from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from PyPDF2 import PdfReader
import cassio

# Support for dataset retrieval with Hugging Face
from datasets import load_dataset
import streamlit as st

css_file = "./styles/main.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

def get_pdf_text(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


st.title("Ask anything from multiple PDF's")

    # Upload PDF file(s)
uploaded_files = st.file_uploader("Upload PDF file(s)", type=["pdf"], accept_multiple_files=True)

pdf_text=""
if uploaded_files:
    

    for file in uploaded_files:
            

            # Read PDF file and display content
        pdf_text = get_pdf_text(file)
        

ASTRA_DB_APPLICATION_TOKEN=st.secrets["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_ID=st.secrets["ASTRA_DB_ID"]
OPENAI_API_KEY=st.secrets["OPENAI_API_KEY"]

cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

llm = OpenAI(openai_api_key=OPENAI_API_KEY)
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

astra_vector_store = Cassandra(
    embedding=embedding,
    table_name="qa_mini_demo",
    session=None,
    keyspace=None,
)

from langchain.text_splitter import CharacterTextSplitter
# We need to split the text using Character Text Split such that it sshould not increse token size
text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 800,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(pdf_text)

astra_vector_store.add_texts(texts)


astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

question = st.text_input("Enter your question here:")

if st.button("Get Answer"):
    with st.spinner("Generating Answer..."):
        if question:
            answer = answer = astra_vector_index.query(question, llm=llm).strip()
            st.success(answer)
        else:
            st.warning("Please enter a question.")