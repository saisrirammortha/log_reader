from fastapi import FastAPI
from app.routes import get_files, get_logs


app = FastAPI(title="My Log Server", version="1.0")


app.include_router(get_files.router, prefix="/api/v1/files", tags=["Files"])
app.include_router(get_logs.router, prefix="/api/v1/logs", tags=["Logs"])


@app.get("/")
async def root():
    return {"message": "Welcome to LogServer!"}