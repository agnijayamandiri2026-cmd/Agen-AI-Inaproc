"""
Updated Main Application with Telegram Bot Routes
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from src.api.routes import router as api_router
from src.api.telegram_routes import router as telegram_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Agen AI Inaproc",
    description="Asisten AI profesional Inaproc dengan Telegram Bot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router)
app.include_router(telegram_router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API status"""
    return {
        "status": "running",
        "message": "Agen AI Inaproc API is active",
        "version": "1.0.0",
        "services": {
            "api": "/api",
            "telegram": "/telegram",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Agen AI Inaproc",
        "components": {
            "api": "operational",
            "telegram": "operational"
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("DEBUG", "True") == "True"
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=debug
    )
