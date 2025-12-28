from fastapi import FastAPI
from routers import auth
from routers import resume

app = FastAPI(title="AI Resume Analyzer API")

app.include_router(auth.router)
app.include_router(resume.router)

@app.get("/")
def health():
    return {"status": "ok"}
