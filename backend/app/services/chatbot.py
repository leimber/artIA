from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
import openai

load_dotenv()

class Chatbot:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY no encontrada en variables de entorno")
            
        openai.api_key = self.api_key
        self.conversation_history = []
        self.max_history = 5
        
        # Prompts base para diferentes situaciones
        self.base_prompts = {
            'alegría': "Me alegro de que te sientas así. ¿Qué ha contribuido a esta sensación positiva?",
            'tristeza': "Entiendo que te sientas así. ¿Quieres hablar sobre lo que te entristece?",
            'ansiedad': "La ansiedad puede ser abrumadora. ¿Te gustaría intentar un ejercicio de respiración juntos?",
            'enojo': "Es natural sentirse enojado. ¿Podemos explorar qué ha desencadenado esta emoción?",
            'neutral': "¿Cómo te gustaría aprovechar este momento?"
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

    def is_crisis_situation(self, text: str) -> bool:
        """Detecta si el mensaje indica una situación de crisis."""
        return any(keyword in text.lower() for keyword in self.crisis_keywords)

    def get_response(
        self,
        message: str,
        emotions: Dict[str, float],
        context: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Genera una respuesta empática basada en el mensaje y las emociones detectadas.
        """
        if self.is_crisis_situation(message):
            return self.crisis_response

        # Construir el prompt base según la emoción principal
        primary_emotion = max(emotions.items(), key=lambda x: x[1])[0]
        base_response = self.base_prompts.get(primary_emotion, self.base_prompts['neutral'])

        try:
            # Construir el contexto para el modelo
            system_prompt = """Eres un asistente empático especializado en apoyo emocional.
            Debes:
            1. Mostrar comprensión y validación emocional
            2. Hacer preguntas abiertas apropiadas
            3. Sugerir recursos o técnicas útiles
            4. Mantener un tono cálido y respetuoso
            5. Evitar consejos directivos o juicios"""

            messages = [{"role": "system", "content": system_prompt}]
            
            # Añadir contexto previo si existe
            if context:
                messages.extend(context[-self.max_history:])

            # Añadir el mensaje actual con información emocional
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

        except Exception as e:
            print(f"Error al generar respuesta: {e}")
            return base_response