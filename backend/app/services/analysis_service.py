from typing import Dict, List, Optional
from app.models.emotion_model import EmotionDetector
from app.models.crisis_detector import CrisisDetector
import numpy as np
from collections import defaultdict

class AnalysisService:
    """Service for analyzing user messages and tracking emotional patterns"""
    
    def __init__(self):
        self.emotion_detector = EmotionDetector()
        self.crisis_detector = CrisisDetector()
        self.user_sessions = defaultdict(list)
    
    def analyze_message(self, message: str, session_id: str) -> Dict:
        """Complete analysis of a single message"""
        # Detect emotions
        emotion_result = self.emotion_detector.detect(message)
        
        # Detect crisis
        crisis_result = self.crisis_detector.detect(message)
        
        # Store in session history
        self.user_sessions[session_id].append({
            'message': message,
            'emotion': emotion_result,
            'crisis': crisis_result,
            'timestamp': None  # Add datetime in production
        })
        
        # Keep only last 100 messages per session
        if len(self.user_sessions[session_id]) > 100:
            self.user_sessions[session_id] = self.user_sessions[session_id][-100:]
        
        # Calculate trend analysis
        trend_analysis = self._calculate_trends(session_id)
        
        return {
            'emotion': emotion_result,
            'crisis': crisis_result,
            'trends': trend_analysis,
            'session_length': len(self.user_sessions[session_id])
        }
    
    def _calculate_trends(self, session_id: str) -> Dict:
        """Calculate emotional trends over time"""
        session_history = self.user_sessions[session_id]
        
        if len(session_history) < 3:
            return {'trend': 'insufficient_data', 'message': 'Need more data for trend analysis'}
        
        # Get recent emotions (last 10 messages)
        recent_emotions = [
            item['emotion']['primary_emotion'] 
            for item in session_history[-10:]
        ]
        
        # Count negative emotions
        negative_count = sum(
            1 for item in session_history[-10:] 
            if item['emotion'].get('is_negative', False)
        )
        
        # Determine trend
        negative_percentage = negative_count / min(10, len(session_history))
        
        if negative_percentage > 0.7:
            trend = 'concerning'
            message = "I've noticed you've been feeling distressed recently. Would you like to talk about what's been happening?"
        elif negative_percentage > 0.4:
            trend = 'mixed'
            message = "You're experiencing a mix of emotions. That's completely normal."
        else:
            trend = 'positive'
            message = "I'm glad to see you're feeling better!"
        
        # Get most common emotion
        from collections import Counter
        common_emotion = Counter(recent_emotions).most_common(1)
        
        return {
            'trend': trend,
            'message': message,
            'negative_percentage': negative_percentage,
            'common_emotion': common_emotion[0][0] if common_emotion else 'neutral',
            'total_messages': len(session_history)
        }
    
    def get_session_summary(self, session_id: str) -> Dict:
        """Get comprehensive summary of a session"""
        session_history = self.user_sessions.get(session_id, [])
        
        if not session_history:
            return {'error': 'Session not found'}
        
        # Calculate overall statistics
        emotions = [item['emotion']['primary_emotion'] for item in session_history]
        crisis_events = [item for item in session_history if item['crisis'].get('is_crisis', False)]
        
        from collections import Counter
        emotion_counts = Counter(emotions)
        
        return {
            'session_id': session_id,
            'total_messages': len(session_history),
            'primary_emotions': dict(emotion_counts.most_common(5)),
            'crisis_events_count': len(crisis_events),
            'trends': self._calculate_trends(session_id),
            'recommendation': self._generate_recommendation(emotion_counts)
        }
    
    def _generate_recommendation(self, emotion_counts: Counter) -> str:
        """Generate personalized recommendations based on emotional patterns"""
        if not emotion_counts:
            return "Continue sharing your thoughts and feelings."
        
        top_emotion = emotion_counts.most_common(1)[0][0]
        
        recommendations = {
            'anxiety': "Consider trying deep breathing exercises when you feel anxious.",
            'sadness': "Journaling might help process these feelings.",
            'anger': "Taking a short walk could help release tension.",
            'fear': "Grounding techniques can help manage fear.",
            'joy': "Keep engaging with activities that bring you joy!"
        }
        
        return recommendations.get(top_emotion, "Keep up the good work in expressing yourself.")
    
    def clear_session(self, session_id: str):
        """Clear session data"""
        if session_id in self.user_sessions:
            del self.user_sessions[session_id]
            return True
        return False