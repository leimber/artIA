from transformers import pipeline

# Cambiar a un modelo mejorado
chatbot = pipeline("text-generation", model="facebook/blenderbot-1B-distill")  # O usa otro modelo de la lista

def get_chatbot_response(query: str) -> str:
    """Genera una respuesta más natural y mejorada."""
    response = chatbot(query, max_length=100, do_sample=True)
    return response[0]['generated_text']
