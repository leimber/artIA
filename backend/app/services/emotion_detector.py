from typing import Dict, List, Optional
import re
from collections import defaultdict

class EmotionDetector:
    def __init__(self):
        # Diccionario de emociones y sus palabras clave asociadas
        self.emotion_keywords = {
            'alegría': [
                'feliz', 'contento', 'alegre', 'emocionado', 'positivo',
                'satisfecho', 'encantado', 'radiante', 'entusiasmado'
            ],
            'tristeza': [
                'triste', 'deprimido', 'solo', 'melancolía', 'desanimado',
                'abatido', 'desesperanzado', 'angustiado', 'apenado'
            ],
            'ansiedad': [
                'ansioso', 'preocupado', 'nervioso', 'estresado', 'inquieto',
                'tenso', 'intranquilo', 'agobiado', 'asustado'
            ],
            'enojo': [
                'enojado', 'molesto', 'frustrado', 'irritado', 'furioso',
                'indignado', 'enfadado', 'rabioso', 'disgustado'
            ],
            'calma': [
                'tranquilo', 'relajado', 'sereno', 'paz', 'calma',
                'sosegado', 'plácido', 'apacible', 'quieto'
            ]
        }
        
        # Compilar expresiones regulares para cada palabra clave
        self.emotion_patterns = {
            emotion: [re.compile(rf'\b{word}\w*\b') 
                     for word in keywords]
            for emotion, keywords in self.emotion_keywords.items()
        }

    def detect_emotions(self, text: str) -> Dict[str, float]:
        """
        Detecta emociones en el texto y devuelve un diccionario con las
        emociones y sus intensidades.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Dict con emociones como claves y sus intensidades como valores (0-1)
        """
        text = text.lower()
        emotion_counts = defaultdict(float)
        total_matches = 0
        
        # Buscar coincidencias para cada emoción
        for emotion, patterns in self.emotion_patterns.items():
            matches = sum(1 for pattern in patterns 
                        for _ in pattern.finditer(text))
            if matches > 0:
                emotion_counts[emotion] = matches
                total_matches += matches
        
        # Si no se detectan emociones, devolver neutral
        if not emotion_counts:
            return {'neutral': 1.0}
        
        # Normalizar las puntuaciones
        normalized_emotions = {
            emotion: count / total_matches
            for emotion, count in emotion_counts.items()
        }
        
        return normalized_emotions

    def get_primary_emotion(self, text: str) -> str:
        """
        Obtiene la emoción principal del texto.
        
        Args:
            text: Texto a analizar
            
        Returns:
            String con la emoción principal
        """
        emotions = self.detect_emotions(text)
        return max(emotions.items(), key=lambda x: x[1])[0]

    def get_emotion_intensity(self, text: str, emotion: str) -> float:
        """
        Obtiene la intensidad de una emoción específica en el texto.
        
        Args:
            text: Texto a analizar
            emotion: Emoción a buscar
            
        Returns:
            Float con la intensidad de la emoción (0-1)
        """
        emotions = self.detect_emotions(text)
        return emotions.get(emotion, 0.0)