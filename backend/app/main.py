from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from schemas import AskRequest, AskResponse
from rag import run_rag

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    res = requests.get(
        f"http://mcp:8001/mcp/card/{req.card_name}"
    )

    cards = res.json()

    # 🔥 핵심: 카드 없음 처리
    if not cards:
        raise HTTPException(
            status_code=404,
            detail="카드를 찾을 수 없습니다."
        )

    try:
        answer = run_rag(cards, req.question)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {"answer": answer}
