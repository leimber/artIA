from typing import Dict, List, Optional
import os
import random
from dotenv import load_dotenv
import openai

load_dotenv()

class Chatbot:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("OPENAI_API_KEY no encontrada, usando respuestas predefinidas")
        
        self.conversation_history = []
        self.max_history = 5
        
        # Respuestas variadas para diferentes emociones
        self.responses = {
            'tristeza': [
                "Veo que estás pasando por un momento difícil. ¿Te gustaría contarme más sobre ello?",
                "Es normal sentirse triste a veces. ¿Qué te ayuda normalmente cuando te sientes así?",
                "Estoy aquí para escucharte. ¿Hay algo específico que te haga sentir así?",
                "A veces hablar de lo que nos entristece puede ayudar. ¿Quieres compartirlo?",
                "Tus sentimientos son válidos. ¿Qué necesitas en este momento?"
            ],
            'enojo': [
                "Entiendo tu frustración. ¿Quieres contarme qué ha pasado?",
                "El enojo es una emoción natural. ¿Qué te ha hecho sentir así?",
                "A veces el enojo nos señala algo importante. ¿Quieres explorar qué puede ser?",
                "Es válido sentirse enfadado. ¿Cómo podemos manejar esta situación?",
                "Respiro contigo. ¿Te gustaría intentar alguna técnica para calmarnos juntos?"
            ],
            'ansiedad': [
                "La ansiedad puede ser abrumadora. ¿Quieres intentar un ejercicio de respiración?",
                "Estoy aquí contigo. ¿Qué te está preocupando en este momento?",
                "A veces ayuda desglosar lo que nos preocupa. ¿Podemos intentarlo?",
                "¿Te gustaría que exploremos juntos algunas técnicas de relajación?",
                "Tus preocupaciones son válidas. ¿Quieres hablar sobre ellas?"
            ],
            'soledad': [
                "Aunque te sientas solo/a, estoy aquí para escucharte. ¿Quieres hablar?",
                "La soledad puede ser muy difícil. ¿Hay alguien con quien podrías conectar hoy?",
                "A veces nos sentimos solos incluso rodeados de gente. ¿Te ha pasado?",
                "¿Te gustaría explorar juntos algunas formas de conectar con otros?",
                "Estoy aquí contigo. ¿Qué te ayudaría a sentirte más acompañado/a?"
            ],
            'neutral': [
                "¿Cómo te gustaría aprovechar este momento?",
                "¿Hay algo específico de lo que te gustaría hablar?",
                "¿Qué tal va tu día hasta ahora?",
                "Estoy aquí para escucharte. ¿Qué hay en tu mente?",
                "¿Hay algo en particular que quieras explorar juntos?"
            ]
        }
        
        # Sistema de respuesta de emergencia
        self.crisis_keywords = [
            'suicid', 'morir', 'muerte', 'acabar', 'no puedo más',
            'amenaza', 'crisis', 'emergencia'
        ]
        
        self.crisis_response = """
        Entiendo que estás pasando por un momento muy difícil. Es importante que sepas que:
        1. Tu vida es valiosa y hay personas que pueden ayudarte
        2. Hay líneas de ayuda disponibles 24/7:
           - Teléfono de la Esperanza: 717 003 717
           - Emergencias: 112
        3. Te recomiendo buscar ayuda profesional inmediata
        ¿Puedes contactar ahora con alguien de confianza o con estos servicios de ayuda?
        """

    def get_emotion_specific_response(self, emotions: Dict[str, float]) -> str:
        """Obtiene una respuesta específica basada en la emoción dominante."""
        if not emotions:
            return random.choice(self.responses['neutral'])
            
        # Obtener la emoción dominante
        primary_emotion = max(emotions.items(), key=lambda x: x[1])[0]
        
        # Mapear emociones similares
        emotion_mapping = {
            'tristeza': 'tristeza',
            'triste': 'tristeza',
            'melancolía': 'tristeza',
            'enojo': 'enojo',
            'enfado': 'enojo',
            'ira': 'enojo',
            'ansiedad': 'ansiedad',
            'nervios': 'ansiedad',
            'preocupación': 'ansiedad',
            'soledad': 'soledad',
            'solo': 'soledad',
            'neutral': 'neutral'
        }
        
        # Obtener la categoría de emoción mapeada
        emotion_category = emotion_mapping.get(primary_emotion.lower(), 'neutral')
        
        # Obtener una respuesta aleatoria para esa emoción
        return random.choice(self.responses[emotion_category])

    def get_response(
        self,
        message: str,
        emotions: Dict[str, float],
        context: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Genera una respuesta basada en el mensaje y las emociones detectadas."""
        # Verificar situación de crisis
        if self.is_crisis_situation(message):
            return self.crisis_response

        try:
            if self.api_key:
                # Intentar usar OpenAI si hay API key
                return self._get_openai_response(message, emotions, context)
            else:
                # Usar respuestas predefinidas si no hay API key
                return self.get_emotion_specific_response(emotions)
                
        except Exception as e:
            print(f"Error al generar respuesta: {e}")
            return self.get_emotion_specific_response(emotions)

    def _get_openai_response(self, message: str, emotions: Dict[str, float], context: Optional[List[Dict[str, str]]] = None) -> str:
        """Obtiene una respuesta usando OpenAI."""
        system_prompt = """Eres un asistente empático especializado en apoyo emocional.
        Debes:
        1. Mostrar comprensión y validación emocional genuina
        2. Hacer preguntas abiertas apropiadas
        3. Sugerir recursos o técnicas útiles cuando sea apropiado
        4. Mantener un tono cálido y respetuoso
        5. Evitar repetir las mismas frases
        6. Adaptar tus respuestas al contexto emocional
        7. Ser conciso pero significativo"""

        messages = [{"role": "system", "content": system_prompt}]
        
        if context:
            messages.extend(context[-self.max_history:])

        emotions_str = ", ".join(f"{k}: {v:.2f}" for k, v in emotions.items())
        current_message = f"[Emociones: {emotions_str}] {message}"
        messages.append({"role": "user", "content": current_message})

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content

    def is_crisis_situation(self, text: str) -> bool:
        """Detecta si el mensaje indica una situación de crisis."""
        return any(keyword in text.lower() for keyword in self.crisis_keywords)