import streamlit as st
import uuid  
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# set your HF Token and Groq API Key
HF_TOKEN = ""  #  Enter your HuggingFace token
GROQ_API_KEY = ""  # Enter your Groq API key


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


st.title("Chat with PDF Application")
st.write("Upload PDFs and chat with their content")

# Initialize ChatGroq with the fixed API key
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="Gemma2-9b-It")

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  


# State management for chat history
if 'store' not in st.session_state:
    st.session_state.store = {}

uploaded_files = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=True)

if uploaded_files:
    documents = []
    st.write("### Extracted Content from Uploaded PDFs:")
    for uploaded_file in uploaded_files:
        temppdf = f"./temp.pdf"
        with open(temppdf, "wb") as file:
            file.write(uploaded_file.getvalue())
            file_name = uploaded_file.name

        loader = PyPDFLoader(temppdf)
        docs = loader.load()
        documents.extend(docs)
        
        # Display the content of the current PDF
        st.write(f"#### {file_name}")
        for doc in docs:
            st.write(doc.page_content)


    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(documents)

    vector_store = Chroma(
        collection_name="pdf_collection",  
        embedding_function=embeddings,  
        persist_directory="./chroma",  
    )

    # Add all documents from all PDFs to the vector store
    vector_store.add_documents(splits)

    retriever = vector_store.as_retriever()

    contextualize_q_system_prompt = (
        "When the user asks a question, use only the information from the uploaded PDF to answer it." 
        "Don't use any past chat details. Just look at the document to understand and give the answer."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),  
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

    system_prompt = (
        "You are a document-based question-answering assistant. "
        "Use the information from the uploaded PDF to answer the question. If the document doesn't have enough information, "
        "say you don't know. Keep your answer short and clear, with no more than three sentences."
        "\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),  
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

   
    def get_session_history(session: str) -> BaseChatMessageHistory:
        if session not in st.session_state.store:
            st.session_state.store[session] = ChatMessageHistory()
        return st.session_state.store[session]

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain, get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    user_input = st.text_input("Your question:")

    if user_input:
        session_history = get_session_history(st.session_state.session_id)
        response = conversational_rag_chain.invoke(
            {"input": user_input},
            config={
                "configurable": {"session_id": st.session_state.session_id}
            },
        )

        # assistant's response
        st.write("Answer:", response.get('answer', 'No answer found'))
        
        st.write("Chat History:", session_history.messages)
