import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Model paths
    EMOTION_MODEL = "SamLowe/roberta-base-go_emotions"
    EMPATHY_MODEL = "AliiaR/DialoGPT-medium-empathetic-dialogues"
    
    # Rate limiting
    RATELIMIT_DEFAULT = "100 per day"
    RATELIMIT_CHAT = "30 per minute"
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///emotional_support.db')
    
    # Crisis keywords
    CRISIS_KEYWORDS = [
        'suicide', 'kill myself', 'end my life', 'want to die',
        'self harm', 'hurt myself', 'crisis hotline'
    ]
    
    # Safety settings
    MAX_MESSAGE_LENGTH = 2000
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')