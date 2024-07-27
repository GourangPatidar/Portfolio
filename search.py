import streamlit as st
from serpapi import GoogleSearch

# Fetch search results from SerpApi
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

# Streamlit app
st.title("Google Search Results")

# Input field for search query
query = st.text_input("Search Query", "who is rohit sharma")

if st.button("Search"):
    if query:
        st.write("Fetching results...")
        search_results = fetch_search_results(query)
        
        if search_results:
            # Show the best content (top result) that defines the query
            best_result = search_results[0]  # Assuming the first result is the most relevant
            st.header("Best Content")
            st.subheader(best_result.get('title', 'No Title'))
            st.write(best_result.get('snippet', 'No Snippet'))
            st.write(f"[Read more]({best_result.get('link', '#')})")

            # Show High Quality Images in a 4x4 grid
            st.header("Images")
            image_urls = [result.get('thumbnail') for result in search_results if 'thumbnail' in result]
            
            if image_urls:
                num_images_per_row = 4
                num_rows = (len(image_urls) + num_images_per_row - 1) // num_images_per_row  # Calculate number of rows

                for row in range(num_rows):
                    cols = st.columns(num_images_per_row)
                    for i in range(num_images_per_row):
                        index = row * num_images_per_row + i
                        if index < len(image_urls):
                            cols[i].image(image_urls[index], use_column_width=True)
            else:
                st.write("No images available.")

            # Show Referral Links with Titles
            st.header("Referral Links")
            for result in search_results:
                title = result.get('title', 'No Title')
                referral_link = result.get('link', None)
                if referral_link:
                    st.write(f"[{title}]({referral_link})")
        else:
            st.write("No results found.")
    else:
        st.write("Please enter a search query.")

st.write("Powered by SerpApi")
