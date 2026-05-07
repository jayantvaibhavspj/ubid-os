from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="UBID-OS Backend API")

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes
from app.main import router as api_router
app.include_router(api_router, prefix="/api")

# Health check
@app.get("/health")
def health():
    return {"status": "ok", "service": "UBID-OS Backend"}

# Serverless handler
@app.get("/")
def read_root():
    return {"message": "UBID-OS Backend API", "docs": "/docs"}
