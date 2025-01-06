# Chat with PDF Application

This is a Streamlit-based application that allows users to upload PDF files, extract their content, and interact with the documents using natural language processing (NLP). After uploading the PDF files, users can ask questions, and the system will answer based on the content extracted from the PDFs.

## API Keys
To run the application, you will need two API keys:
1. **Hugging Face (HF) Token**: 
2. **Groq API Key**: 

## Features
- **Upload PDFs**: Add multiple PDF files for content extraction.
- **View Content**: See the extracted content of each uploaded PDF.
- **Chat with Content**: Ask questions about the uploaded PDFs and get answers based on the document's content.
- **Session History**: Maintains chat history for interactive queries.

## How to Use
1. Open the app.
2. Upload your PDF files using the upload button.
3. View the extracted content for each file.
4. Ask questions in the input box and receive answers based on the uploaded PDF's content.

## Technology Stack
- **Streamlit**: Provides a simple interface for the app.
- **LangChain**: Handles document retrieval and Q&A workflows.
- **HuggingFace Embeddings**: Converts PDF content into vector representations for search and retrieval.
- **Groq**: Powers the conversational Q&A logic.

## Requirements

The required dependencies are listed in the `requirements.txt` file. 

You can install them all using:

```bash
pip install -r requirements.txt


