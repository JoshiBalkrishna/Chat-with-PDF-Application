# Chat-with-PDF-Application

This is a Streamlit-based app that allows users to upload PDF files and interact with their content using natural language. The app leverages LangChain, HuggingFace Embeddings, and Groq for intelligent question answering and document retrieval.
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
