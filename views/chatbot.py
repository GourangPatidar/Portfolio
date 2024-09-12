import streamlit as st
from google.cloud import vision
from PIL import Image
import io

# Initialize Google Cloud Vision client
vision_client = vision.ImageAnnotatorClient()

st.header("SearchGPT", divider="rainbow")

css_file = "./styles/main.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

selected_option = st.selectbox("Select an option", ["GPT", "web"])

if selected_option == "GPT":
    # Upload image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_image:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert the image to bytes for Google Cloud Vision API
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        content = image_bytes.getvalue()

        # Call the Google Cloud Vision API to extract text
        image_for_api = vision.Image(content=content)
        response = vision_client.text_detection(image=image_for_api)
        text = response.text_annotations[0].description if response.text_annotations else "No text found."

        st.write("Extracted Text from Image:")
        st.write(text)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display existing chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Send extracted text to GPT for further processing
        if text:
            st.session_state.messages.append({"role": "user", "content": text})
            with st.chat_message("user"):
                st.markdown(text)
elif selected_option=="web":
    def fetch_search_results(query):
        try:
            params = {
            "engine": "google",
            "q": query,
            "api_key": api_key_serp  # Replace with your actual API key
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

 

