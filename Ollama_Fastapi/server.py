from fastapi import FastAPI, Body
import ollama

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat")
def chat(message: str = Body(..., embed=True)):
    response = ollama.chat(
        model="gemma:2b",
        messages=[{"role": "user", "content": message}],
    )
    return {"response": response.message.content}

 

