from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI(
    title="Simple API",
    description="A simple API ready to be extended with ML models",
    version="0.1.0"
)

# CORS middleware - adjust origins for your needs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class HealthResponse(BaseModel):
    status: str
    version: str


class MessageRequest(BaseModel):
    text: str
    max_length: Optional[int] = 100


class MessageResponse(BaseModel):
    original: str
    processed: str
    length: int


# Endpoints
@app.get("/", tags=["General"])
def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Simple API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "version": "0.1.0"
    }


@app.post("/process", response_model=MessageResponse, tags=["Processing"])
def process_message(request: MessageRequest):
    """
    Process a text message.
    
    This is a placeholder endpoint - extend this to call your ML model.
    """
    processed_text = request.text.upper()  # Simple example processing
    
    return {
        "original": request.text,
        "processed": processed_text,
        "length": len(request.text)
    }


@app.get("/info", tags=["General"])
def get_info():
    """Get system information."""
    return {
        "python_version": os.sys.version,
        "environment": os.getenv("ENVIRONMENT", "development")
    }


# Placeholder for your future ML model endpoint
@app.post("/predict", tags=["ML"])
def predict(request: MessageRequest):
    """
    Placeholder for ML model predictions.
    
    Replace this with your language model inference code.
    """
    return {
        "message": "ML model endpoint - ready to be implemented",
        "input": request.text,
        "note": "Add your model loading and inference code here"
    }