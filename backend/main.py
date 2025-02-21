from fastapi import FastAPI
from backend.chatbot import get_chatbot_response
from backend.emotion_detector import detect_emotion

app = FastAPI(title="Asistente IA de Bienestar Emocional")

@app.get("/")
def home():
    return {"message": "ArtIA, Asistente IA de Bienestar Emocional"}

@app.post("/chat")
def chat(query: str):
    """Procesa la entrada del usuario, responde y detecta emociones."""
    response = get_chatbot_response(query)
    emotion = detect_emotion(query)
    return {"response": response, "emotion": emotion}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
