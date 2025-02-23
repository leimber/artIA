from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict

from app.services.emotion_detector import EmotionDetector
from app.services.chatbot import Chatbot

app = FastAPI(title="ArtIA - Asistente de Bienestar")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica el dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicios
emotion_detector = EmotionDetector()
chatbot = Chatbot()

class ChatRequest(BaseModel):
    query: str
    context: Optional[List[Dict[str, str]]] = None

@app.get("/")
def read_root():
    return {"message": "Bienvenido a ArtIA - API de Bienestar Emocional"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Detectar emociones
        emotions = emotion_detector.detect_emotions(request.query)
        
        # Obtener respuesta del chatbot
        response = chatbot.get_response(
            message=request.query,
            emotions=emotions,
            context=request.context
        )
        
        return {
            "response": response,
            "emotions": emotions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Para debugging
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)