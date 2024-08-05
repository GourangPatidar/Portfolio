
---

# GEN-AI Products Collection

Welcome to the GEN-AI Products Collection! This project hosts a variety of AI-powered products showcased on a Streamlit-hosted website.

## Features

### 1. YouTube Video Summarizer
- **Description**: Converts subtitles to text and provides concise summaries.
- **Technology**: Utilizes Langchain for summarization.

### 2. PDF Data Extraction and Storage
- **Description**: Extracts large datasets from PDFs and stores them as vectors in Cassandra DB.
- **Benefits**: Enables efficient querying and analysis of PDF-related information.

### 3. Live Search Integration
- **Description**: Implements real-time search capabilities using ChatGPT APIs.
- **Benefits**: Enhances user accessibility to up-to-date information.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- Streamlit
- Langchain
- Cassandra DB
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/GourangPatidar/Portfolio.git
   cd gen-ai-products-collection
   ```

2. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Cassandra DB**
   - Ensure your Cassandra DB is up and running.
   

4. **Set up API Keys**
   - Obtain your OpenAI API key.
   - Add your API key to secrets.toml

### Running the Application

Run the Streamlit app using the following command:
```bash
streamlit run streamlit_app.py
```

## Usage

Visit the hosted Streamlit website to explore the various AI products. Each product offers a unique functionality aimed at showcasing the capabilities of GEN-AI.

## Contributing

We welcome contributions to improve and expand this project. Please follow the steps below to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/YourFeature`).
6. Create a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Langchain for providing the summarization capabilities.
- OpenAI for the ChatGPT API.
- Cassandra for the efficient data storage solutions.


