import streamlit as st
import openai
import wikipedia

st.header("GoGPT", divider="rainbow")

# Show title and description.
openai.api_key = st.secrets["OPENAI_API_KEY"]
if not openai.api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via st.chat_message.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.text_input("You:", "What's on your mind?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Dropdown for selecting search source
        search_source = st.selectbox("Search Source", ["OpenAI", "Wikipedia", "Web Search"])

        # Determine model or API based on search source
        if search_source == "OpenAI":
            model_name = "gpt-3.5-turbo"
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            assistant_response = response["choices"][0]["message"]["content"]

        elif search_source == "Wikipedia":
            try:
                wikipedia.set_lang("en")  # Set Wikipedia language (e.g., "en" for English)
                assistant_response = wikipedia.summary(prompt, sentences=1)
            except wikipedia.exceptions.DisambiguationError as e:
                assistant_response = f"Please be more specific: {', '.join(e.options)}"
            except wikipedia.exceptions.PageError:
                assistant_response = "Sorry, I couldn't find any relevant information."

        elif search_source == "Web Search":
            # Implement your custom web search functionality here
            assistant_response = "Web Search functionality coming soon!"

        # Display the response based on the selected search source.
        with st.spinner("Thinking..."):
            st.chat_message("assistant").markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})


