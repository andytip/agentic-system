import os
import importlib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}


class Prompt(BaseModel):
    prompt: str


@app.post("/ask")
def ask(prompt: Prompt):
    try:
        openai = importlib.import_module("openai")
    except ImportError as exc:
        raise HTTPException(
            status_code=500, detail="OpenAI library is not installed"
        ) from exc

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500, detail="OPENAI_API_KEY is not set"
        )

    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt.prompt}],
        )
        answer = response.choices[0].message["content"].strip()
        return {"answer": answer}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
