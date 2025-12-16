from rag_store import retriever
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings



def run_rag(cards, question):
    if not cards:
        return "해당 카드 정보를 찾을 수 없습니다."

    docs = [
        Document(
            page_content=c.get("desc", ""),
            metadata={"name": c.get("name", "")}
        )
        for c in cards
        if c.get("desc")
    ]

    if not docs:
        return "카드 설명 데이터가 없습니다."

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 🔥 핵심 1: Chroma를 in-memory로 명시
    db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="yugioh_cards"
    )

    retriever = db.as_retriever()

    # 🔥 핵심 2: Gemini 설정
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        convert_system_message_to_human=True
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )

    return qa.run(question)
