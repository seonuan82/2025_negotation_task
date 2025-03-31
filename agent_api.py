from fastapi import FastAPI
from pydantic import BaseModel
from utils.llm import get_llm_response
from utils.logging import log_json

app = FastAPI()

class Query(BaseModel):
    user_id: str
    prompt: str

@app.post("/agent_response")
def agent_response(query: Query):
    response = get_llm_response(query.prompt)
    log_json({"User": query.prompt, "Agent": response}, query.user_id)
    return {"response": response}
