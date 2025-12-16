from fastapi import FastAPI
from pydantic import BaseModel
from rag_store import get_answer

app = FastAPI()


class AskRequest(BaseModel):
    card_name: str
    question: str


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(req: AskRequest):
    return {
        "answer": get_answer(req.card_name, req.question)
    }
