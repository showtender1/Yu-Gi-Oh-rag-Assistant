from pydantic import BaseModel

class AskRequest(BaseModel):
    card_name: str
    question: str

class AskResponse(BaseModel):
    answer: str
