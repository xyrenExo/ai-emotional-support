import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from typing import Dict, List, Tuple

class EmotionDetector:
    def __init__(self):
        self.model_name = "SamLowe/roberta-base-go_emotions"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.model.eval()
        
        self.emotion_labels = [
            'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
            'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval',
            'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief',
            'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization',
            'relief', 'remorse', 'sadness', 'surprise', 'neutral'
        ]
    
    def detect(self, text: str) -> Dict[str, float]:
        """Detect emotions in text and return top emotions with intensities"""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
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