"""
API Routes - Main endpoints untuk Agen AI Inaproc
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["agent"])

# Pydantic Models
class ChatRequest(BaseModel):
    """Chat request model"""
    prompt: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    """Chat response model"""
    status: str
    response: str
    user_id: Optional[str] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str

# Health check
@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    Returns: Health status of the API
    """
    return {
        "status": "healthy",
        "service": "Agen AI Inaproc API"
    }

# Chat endpoint
@router.post("/agent/chat", response_model=ChatResponse)
async def agent_chat(request: ChatRequest):
    """
    Chat dengan Agen AI
    
    Request:
        - prompt: Pertanyaan atau pesan dari user
        - user_id: ID user (optional)
        - context: Context tambahan (optional)
    
    Response:
        - status: Status response
        - response: Jawaban dari AI
        - user_id: User ID yang dikirim
    """
    try:
        if not request.prompt or len(request.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        logger.info(f"📨 Chat request from user {request.user_id}: {request.prompt[:50]}...")
        
        # Generate response (placeholder - bisa diintegrasikan dengan OpenAI)
        ai_response = await generate_response(request.prompt, request.user_id, request.context)
        
        logger.info(f"✅ Response generated: {ai_response[:50]}...")
        
        return {
            "status": "success",
            "response": ai_response,
            "user_id": request.user_id
        }
    
    except HTTPException as e:
        logger.error(f"❌ HTTP Error: {str(e)}")
        raise e
    
    except Exception as e:
        logger.error(f"❌ Error in agent_chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

# Status endpoint
@router.get("/status")
async def status():
    """
    Get API status
    Returns: Detailed status information
    """
    return {
        "status": "operational",
        "service": "Agen AI Inaproc",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "chat": "/api/agent/chat",
            "status": "/api/status"
        }
    }

# Info endpoint
@router.get("/info")
async def info():
    """
    Get API information
    Returns: API documentation
    """
    return {
        "name": "Agen AI Inaproc API",
        "version": "1.0.0",
        "description": "API untuk Agen AI Inaproc dengan Telegram Bot Integration",
        "endpoints": {
            "GET /api/health": "Health check",
            "GET /api/status": "API status",
            "GET /api/info": "API information",
            "POST /api/agent/chat": "Chat dengan AI agent"
        }
    }

# Helper function untuk generate response
async def generate_response(prompt: str, user_id: Optional[str] = None, context: Optional[Dict] = None) -> str:
    """
    Generate response dari AI
    
    Args:
        prompt: User prompt
        user_id: User ID
        context: Additional context
    
    Returns:
        AI response string
    """
    try:
        # TODO: Integrasikan dengan OpenAI API
        # Untuk sekarang, return placeholder response
        
        # Cek environment variable untuk OpenAI API key
        import os
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if not openai_key or openai_key == "your_openai_api_key_here":
            # Return placeholder response jika API key belum setup
            response = f"""
ℹ️ **Bot Response (Placeholder Mode)**

Anda mengirim: "{prompt}"

🔧 **Note:** Bot sedang dalam mode placeholder karena:
1. OpenAI API key belum dikonfigurasi
2. Atau OpenAI belum terintegrasi

✅ **Setup OpenAI:**
1. Dapatkan API key dari: https://platform.openai.com/api-keys
2. Tambah ke file .env:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
3. Restart bot dan API

Saat ini bot hanya echo pesan Anda. Setelah OpenAI terintegrasi, bot akan memberikan response AI yang sesungguhnya.
            """
        else:
            # Jika ada API key, coba gunakan OpenAI
            response = await call_openai_api(prompt, context)
        
        return response
    
    except Exception as e:
        logger.error(f"❌ Error generating response: {str(e)}")
        return f"❌ Error: Tidak bisa generate response. Detail: {str(e)}"

async def call_openai_api(prompt: str, context: Optional[Dict] = None) -> str:
    """
    Call OpenAI API untuk generate response
    
    Args:
        prompt: User prompt
        context: Additional context
    
    Returns:
        Response dari OpenAI
    """
    try:
        import os
        import openai
        
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Build messages
        messages = []
        if context and "history" in context:
            messages.extend(context["history"])
        
        messages.append({"role": "user", "content": prompt})
        
        # Call OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        ai_response = response.choices[0].message.content
        logger.info(f"✅ OpenAI response received")
        
        return ai_response
    
    except Exception as e:
        logger.error(f"❌ OpenAI API Error: {str(e)}")
        # Fallback ke placeholder jika OpenAI error
        return f"⚠️ OpenAI Error: {str(e)}\n\nBut here's a placeholder response:\nYou asked: {prompt}"
