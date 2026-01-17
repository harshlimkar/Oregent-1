from fastapi import FastAPI, Query
from conversation_agent import conversation_agent

app = FastAPI(title="Oregent – Super Intelligent Shopping Agent")

@app.post("/chat")
def chat(user_input: str = Query(...)):
    return conversation_agent(user_input)
