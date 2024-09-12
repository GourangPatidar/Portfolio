import streamlit as st
import requests
from PIL import Image
import io

OCR_SPACE_API_KEY = K87860374888957  # Store your OCR.space API key in Streamlit secrets

st.header("SearchGPT", divider="rainbow")

css_file = "./styles/main.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

selected_option = st.selectbox("Select an option", ["GPT", "web"])

def ocr_space_api(file_path):
    url = 'https://api.ocr.space/parse/image'
    payload = {
        'apikey': OCR_SPACE_API_KEY,
        'language': 'eng'
    }
    with open(file_path, 'rb') as f:
        response = requests.post(url, files={'file': f}, data=payload)
    return response.json()

if selected_option == "GPT":
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_image:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Save the uploaded image to a temporary location
        with open("temp_image.png", "wb") as f:
            f.write(uploaded_image.getvalue())

        # Use OCR.space API to extract text
        try:
            result = ocr_space_api("temp_image.png")
            text = result.get("ParsedResults", [{}])[0].get("ParsedText", "No text found.")
            st.write("Extracted Text from Image:")
            st.write(text)
        except Exception as e:
            st.error(f"Error extracting text: {e}")

    else:
        st.info("Please upload an image.")

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

 

