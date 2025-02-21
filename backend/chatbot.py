from transformers import pipeline

# Cargar modelo de chatbot desde Hugging Face
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")  

def get_chatbot_response(query: str) -> str:
    """Genera una respuesta basada en el input del usuario."""
    response = chatbot(query, max_length=100, do_sample=True)
    return response[0]['generated_text']
