from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

def create_vector_store(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings()

    vector_store = FAISS.from_texts(chunks, embeddings)

    return vector_store


def get_relevant_context(vector_store, query):

    docs = vector_store.similarity_search(query, k=3)

    context = "\n".join([doc.page_content for doc in docs])

    return context