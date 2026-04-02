from typing import Dict, List
from app.models.emotion_model import EmotionDetector
from app.models.crisis_detector import CrisisDetector
from app.models.gemini_client import GeminiClient
from app.models.empathy_refiner import EmpathyRefiner
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.emotion_detector = EmotionDetector()
        self.crisis_detector = CrisisDetector()
        self.gemini_client = GeminiClient()
        self.empathy_refiner = EmpathyRefiner()
        
        # Simple session memory (in production, use Redis)
        self.sessions = {}
    
    def process_message(self, 
                       message: str, 
                       session_id: str,
                       features: Dict) -> Dict:
        """Process user message through the full AI pipeline"""
        
        try:
            # Step 1: Detect emotions
            emotion_result = self.emotion_detector.detect(message)
            
            # Step 2: Detect crisis
            crisis_result = self.crisis_detector.detect(message)
            
            # Step 3: Generate response with Gemini
            gemini_response = self.gemini_client.generate_response(
                message, 
                emotion_result, 
                crisis_result,
                features
            )
            
            # Step 4: Refine with DialoGPT for empathy
            refined_response = self.empathy_refiner.refine(gemini_response, message)
            
            # Step 5: Store in session memory
            if session_id not in self.sessions:
                self.sessions[session_id] = []
            
            self.sessions[session_id].append({
                "user": message,
                "assistant": refined_response,
                "emotion": emotion_result,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only last 20 messages per session
            if len(self.sessions[session_id]) > 20:
                self.sessions[session_id] = self.sessions[session_id][-20:]
            
            return {
                "response": refined_response,
                "emotion": emotion_result,
                "crisis": crisis_result,
                "session_id": session_id
            }
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            # Return a safe fallback response
            return {
                "response": "I'm having some technical difficulties, but I'm still here to listen. Please try again in a moment.",
                "emotion": {"primary_emotion": "neutral", "intensity": 0, "is_negative": False},
                "crisis": {"is_crisis": False, "risk_level": 0},
                "session_id": session_id
            }