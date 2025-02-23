from typing import Dict
import openai

def get_chatbot_response(query: str, context: list = None) -> Dict[str, str]:
    """
    Genera respuestas empáticas usando GPT-3.5/4
    """
    if context is None:
        context = []
    
    messages = [
        {"role": "system", "content": """Eres un asistente empático y comprensivo. 
        Tu objetivo es escuchar, entender y proporcionar apoyo emocional.
        Recuerda:
        - Mostrar empatía y comprensión
        - No juzgar
        - Hacer preguntas abiertas cuando sea apropiado
        - Validar sentimientos
        - Sugerir recursos profesionales cuando sea necesario"""},
    ] + context + [{"role": "user", "content": query}]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return {"error": str(e)}