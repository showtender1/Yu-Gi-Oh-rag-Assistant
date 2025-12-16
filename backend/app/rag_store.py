import requests
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI

_embeddings = None
_vectorstore = None


def _init_store():
    global _embeddings, _vectorstore

    if _vectorstore is not None:
        return

    print("🚀 Initializing embeddings")
    _embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("📦 Loading Yu-Gi-Oh cards")
    res = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")
    data = res.json()["data"][:500]

    docs = [
        Document(
            page_content=f"{c['name']} {c['type']} {c.get('desc','')}",
            metadata={"name": c["name"]}
        )
        for c in data
    ]

    print("🧠 Building vector store")
    _vectorstore = Chroma.from_documents(docs, _embeddings)
    print("✅ Vector store ready")


def get_answer(card_name: str, question: str) -> str:
    _init_store()

    retriever = _vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        convert_system_message_to_human=True
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

    return qa.run(f"{card_name}: {question}")
