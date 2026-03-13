from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(
    title="Energy Monitor API",
    description="Backend API for Energy Monitoring System",
    version="1.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Energy Monitor API running"}
