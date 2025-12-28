from fastapi import FastAPI
from routers import auth

app = FastAPI(title="AI Resume Analyzer API")

app.include_router(auth.router)

@app.get("/")
def health():
    return {"status": "ok"}
