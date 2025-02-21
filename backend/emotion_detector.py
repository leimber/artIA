from transformers import pipeline

# Modelo de detección de emociones
emotion_model = pipeline("text-classification", model="joeddav/distilbert-base-uncased-go-emotions-student")

def detect_emotion(text: str) -> str:
    """Detecta la emoción en el texto ingresado."""
    result = emotion_model(text)
    return result[0]['label']
