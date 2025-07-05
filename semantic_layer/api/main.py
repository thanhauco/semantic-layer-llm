from fastapi import FastAPI

app = FastAPI(title="Semantic Layer API")

@app.get("/")
def health_check():
    return {"status": "ok"}
