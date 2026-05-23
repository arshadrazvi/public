import os
import torch
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

conversation_retrieval_chain = None
chat_history = []
llm_hub = None
embeddings = None


def init_llm():
    global llm_hub, embeddings

    logger.info("Initializing ChatGPT and embeddings...")

    llm_hub = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        max_tokens=256,
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": DEVICE}
    )

    logger.debug("ChatGPT initialized: %s", llm_hub)
    logger.debug("Embeddings initialized with device: %s", DEVICE)


def process_document(document_path):
    global conversation_retrieval_chain

    logger.info("Loading document from path: %s", document_path)

    loader = PyPDFLoader(document_path)
    documents = loader.load()

    logger.debug("Loaded %d document(s)", len(documents))

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,
        chunk_overlap=64
    )

    texts = text_splitter.split_documents(documents)

    logger.debug("Document split into %d text chunks", len(texts))

    db = Chroma.from_documents(
        documents=texts,
        embedding=embeddings
    )

    conversation_retrieval_chain = RetrievalQA.from_chain_type(
        llm=llm_hub,
        chain_type="stuff",
        retriever=db.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 6, "lambda_mult": 0.25}
        ),
        return_source_documents=False,
        input_key="question"
    )

    logger.info("RetrievalQA chain created successfully.")


def process_prompt(prompt):
    global conversation_retrieval_chain
    global chat_history

    logger.info("Processing prompt: %s", prompt)

    if conversation_retrieval_chain is None:
        return "Please upload/process a PDF document first."

    output = conversation_retrieval_chain.invoke({
        "question": prompt
    })

    answer = output["result"]

    chat_history.append((prompt, answer))

    logger.debug("Chat history updated. Total exchanges: %d", len(chat_history))

    return answer


init_llm()
logger.info("LLM and embeddings initialization complete.")