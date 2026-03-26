from fastapi import FastAPI
from backend.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Energy Monitor API",
    description="Backend API for Energy Monitoring System",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router)

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Energy Monitor API running"}
