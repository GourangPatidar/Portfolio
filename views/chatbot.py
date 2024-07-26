import streamlit as st
from openai import OpenAI

st.header("GoGPT", divider="rainbow")

# Create an OpenAI client (assuming the API key is set up in the backend).
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # Adjust if API key setup differs.

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create a selection box for choosing between "GPT" and "web".
selected_option = st.selectbox("Select an option", ["GPT", "web"])

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

    if selected_option == "GPT":
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

    elif selected_option == "web":
        # Implement functionality for "web" option.
        st.chat_message("assistant").markdown("Web functionality not yet implemented.")
