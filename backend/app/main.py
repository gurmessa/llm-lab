from fastapi import FastAPI

app = FastAPI(title="LLM Lab Backend")

@app.get("/")
def read_root():
    return {"Hello": "World"}
