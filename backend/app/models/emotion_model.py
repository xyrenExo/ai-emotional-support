import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

# Global model cache to load model only once
_EMOTION_MODEL = None
_EMOTION_TOKENIZER = None
_EMOTION_MODEL_LOADED = False

class EmotionDetector:
    def __init__(self):
        self.model_name = "SamLowe/roberta-base-go_emotions"
        # Cache will be filled on first use
        self._ensure_model_loaded()
        
        self.emotion_labels = [
            'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
            'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval',
            'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief',
            'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization',
            'relief', 'remorse', 'sadness', 'surprise', 'neutral'
        ]
    
    @classmethod
    def _ensure_model_loaded(cls):
        """Load model only once, globally"""
        global _EMOTION_MODEL, _EMOTION_TOKENIZER, _EMOTION_MODEL_LOADED
        
        if _EMOTION_MODEL_LOADED:
            return
        
        try:
            logger.info("Loading EmotionDetector model...")
            _EMOTION_TOKENIZER = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
            _EMOTION_MODEL = AutoModelForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions")
            _EMOTION_MODEL.eval()
            _EMOTION_MODEL_LOADED = True
            logger.info("EmotionDetector model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load EmotionDetector model: {e}")
            _EMOTION_MODEL_LOADED = False
    
    def detect(self, text: str) -> Dict[str, float]:
        """Detect emotions in text and return top emotions with intensities"""
        global _EMOTION_MODEL, _EMOTION_TOKENIZER
        
        try:
            # Ensure model is loaded
            self._ensure_model_loaded()
            
            if _EMOTION_MODEL is None or _EMOTION_TOKENIZER is None:
                logger.warning("Models not available, returning neutral emotion")
                return {
                    "primary_emotion": "neutral",
                    "intensity": 0,
                    "emotions": {"neutral": 1.0},
                    "is_negative": False
                }
            
            inputs = _EMOTION_TOKENIZER(text, return_tensors="pt", truncation=True, max_length=512)
            
            with torch.no_grad():
                outputs = _EMOTION_MODEL(**inputs)
                scores = torch.sigmoid(outputs.logits).numpy()[0]
            
            # Get top 3 emotions
            top_indices = np.argsort(scores)[-3:][::-1]
            emotions = {
                self.emotion_labels[idx]: float(scores[idx])
                for idx in top_indices
            }
            
            # Determine primary emotion
            primary_emotion = max(emotions.items(), key=lambda x: x[1])
            
            return {
                "primary_emotion": primary_emotion[0],
                "intensity": primary_emotion[1],
                "all_emotions": emotions,
                "is_negative": any(e in ['anger', 'annoyance', 'disappointment', 'disgust', 
                                         'fear', 'nervousness', 'sadness', 'grief', 'remorse']
                                  for e in emotions.keys())
            }
        except Exception as e:
            logger.error(f"Error detecting emotion: {e}")
            return {
                "primary_emotion": "neutral",
                "intensity": 0,
                "emotions": {"neutral": 1.0},
                "is_negative": False
            }