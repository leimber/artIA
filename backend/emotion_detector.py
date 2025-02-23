from transformers import pipeline
import numpy as np

emotion_classifier = pipeline(
    "text-classification",
    model="SamLowe/roberta-base-go_emotions",
    top_k=3
)

def detect_emotion(text: str) -> Dict[str, float]:
    """
    Detecta múltiples emociones y sus intensidades
    """
    try:
        results = emotion_classifier(text)
        emotions = {pred['label']: round(pred['score'], 2) for pred in results[0]}
        return emotions
    except Exception as e:
        return {"error": str(e)}