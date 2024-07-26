import streamlit as st
from openai import OpenAI
from serpapi import GoogleSearch
from urllib.parse import urlparse

st.header("GoGPT" , divider="rainbow")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
openai_api_key=st.secrets["OPENAI_API_KEY"]
api_key_serp=st.secrets["SERP_API_KEY"]

css_file = "./styles/main.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

selected_option = st.selectbox("Select an option", ["GPT", "web"])

if selected_option=="GPT":
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    else:

    # Create an OpenAI client.
        client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
        if "messages" not in st.session_state:
            st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
        if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

        # Generate a response using the OpenAI API.
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

elif selected_option=="web":
    def fetch_search_results(query):
        try:
            params = {
            "engine": "google",
            "q": query,
            "api_key": "148cd270379c28b4a2522374c3c02bc8d68d2c2459bc1f3516173518ca3de1ec"  # Replace with your actual API key
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            return results.get("organic_results", [])
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return []


# Input field for search query
    query = st.text_input("Search Query")

    if st.button("Search"):
        if query:
            st.write("Fetching results...")
            search_results = fetch_search_results(query)
        
            if search_results:
            # Show the best content (top result) that defines the query
                best_result = search_results[0]  # Assuming the first result is the most relevant
                st.header("Best Content")
                st.subheader(best_result.get('title', 'No Title'))
            
            # Combine snippets from multiple top results to increase content length
                combined_snippet = ""
                for result in search_results[:3]:  # Combining snippets from the top 3 results
                    combined_snippet += result.get('snippet', '') + " "
                
                st.write(combined_snippet.strip())
                st.write(f"[Read more]({best_result.get('link', '#')})")

            # Show High Quality Images in a 4x4 grid
                st.header("Images")
                image_urls = [(result.get('thumbnail'), result.get('link')) for result in search_results if 'thumbnail' in result]
            
                if image_urls:
                    num_images_per_row = 4
                    num_rows = (len(image_urls) + num_images_per_row - 1) // num_images_per_row  # Calculate number of rows

                    for row in range(num_rows):
                        cols = st.columns(num_images_per_row)
                        for i in range(num_images_per_row):
                            index = row * num_images_per_row + i
                            if index < len(image_urls):
                                image_url, link = image_urls[index]
                                cols[i].markdown(f'<a href="{link}" target="_blank"><img src="{image_url}" style="width:100%;"></a>', unsafe_allow_html=True)
                else:
                    st.write("No images available.")

                # Show Referral Links with Titles and Domain Names
                st.header("Referral Links")
                for result in search_results:
                    title = result.get('title', 'No Title')
                    referral_link = result.get('link', None)
                    if referral_link:
                        domain = urlparse(referral_link).netloc
                        st.write(f"[{title}]({referral_link}) - {domain}")
            else:
                st.write("No results found.")
        else:
            st.write("Please enter a search query.")

    st.write("Powered by SerpApi")

