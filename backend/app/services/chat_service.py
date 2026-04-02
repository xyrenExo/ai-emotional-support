from typing import Dict, List
from app.models.emotion_model import EmotionDetector
from app.models.crisis_detector import CrisisDetector
from app.models.gemini_client import GeminiClient
from app.models.empathy_refiner import EmpathyRefiner
import logging
from datetime import datetime
import os
import time

logger = logging.getLogger(__name__)

# Skip empathy refinement by default for faster response (can be enabled via env var)
SKIP_EMPATHY_REFINEMENT = os.getenv('SKIP_EMPATHY_REFINEMENT', 'true').lower() == 'true'

class ChatService:
    def __init__(self):
        self.emotion_detector = EmotionDetector()
        self.crisis_detector = CrisisDetector()
        self.gemini_client = GeminiClient()
        # Initialize empathy refiner with skip flag
        self.empathy_refiner = EmpathyRefiner(skip_empathy=SKIP_EMPATHY_REFINEMENT)
        
        logger.info(f"ChatService initialized. Empathy refinement: {'disabled' if SKIP_EMPATHY_REFINEMENT else 'enabled'}")
        
        # Simple session memory (in production, use Redis)
        self.sessions = {}
    
    def process_message(self, 
                       message: str, 
                       session_id: str,
                       features: Dict) -> Dict:
        """Process user message through the full AI pipeline"""
        
        try:
            start_time = time.time()
            logger.info(f"Processing message (length: {len(message)})")
            
            # Step 1: Detect emotions
            emotion_start = time.time()
            emotion_result = self.emotion_detector.detect(message)
            logger.debug(f"Emotion detection took {time.time() - emotion_start:.2f}s")
            
            # Step 2: Detect crisis
            crisis_start = time.time()
            crisis_result = self.crisis_detector.detect(message)
            logger.debug(f"Crisis detection took {time.time() - crisis_start:.2f}s")
            
            # Step 3: Generate response with Gemini
            gemini_start = time.time()
            gemini_response = self.gemini_client.generate_response(
                message, 
                emotion_result, 
                crisis_result,
                features
            )
            logger.debug(f"Gemini response took {time.time() - gemini_start:.2f}s")
            
            # Step 4: Refine with DialoGPT for empathy (can be skipped for faster response)
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
            
            total_time = time.time() - start_time
            logger.info(f"Message processed in {total_time:.2f}s")
            
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
