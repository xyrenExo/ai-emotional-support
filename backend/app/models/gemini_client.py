import google.generativeai as genai
from typing import Dict, List, Optional
import threading
from app.config import Config

class GeminiClient:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def generate_response(self, 
                         user_message: str, 
                         emotion_context: Dict,
                         crisis_context: Dict,
                         features: Dict) -> str:
        """Generate empathetic response using Gemini (synchronous)"""
        
        # Build the system prompt
        system_prompt = self._build_system_prompt(emotion_context, crisis_context, features)
        
        # Full prompt with user message
        full_prompt = f"""{system_prompt}

User message: {user_message}

Generate a response following the guidelines above:"""
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._get_fallback_response(emotion_context, crisis_context)
    
    def _build_system_prompt(self, emotion: Dict, crisis: Dict, features: Dict) -> str:
        prompt = """You are an advanced AI-powered emotional support assistant designed to provide safe, empathetic, and supportive conversations.

MISSION:
- Help users express emotions freely and anonymously
- Provide emotional support for stress, anxiety, sadness, and low confidence
- Encourage calm thinking, self-awareness, and emotional resilience
- Offer simple coping strategies and relaxation techniques
- Detect emotional distress and crisis situations early
- Guide users toward professional help when necessary

CORE RULES:
1. EMPATHY FIRST – Always validate feelings
2. NO MEDICAL AUTHORITY – No diagnosis or prescriptions
3. CLARITY – Keep responses simple and calm
4. SAFETY FIRST – Crisis overrides everything
5. PRIVACY – Never request personal data

RESPONSE STRUCTURE:
1. Emotional Validation
2. Reflection
3. Gentle Guidance (1–2 suggestions)
4. Optional Support
5. Professional Help (if needed)

TONE: Warm, human-like, calm

Return ONLY the final response text."""
        
        # Add context
        if crisis.get('is_crisis'):
            prompt += """

CRISIS MODE ACTIVE:
- Respond with urgency and care
- Encourage reaching out to trusted people
- Suggest crisis hotlines immediately
- Stay emotionally present
- Prioritize safety above all else"""
        
        if emotion.get('is_negative'):
            prompt += f"""

User is feeling {emotion.get('primary_emotion')} with {emotion.get('intensity', 0):.0%} intensity.
Focus on validation and comfort."""
        
        # Add feature-specific guidance
        if features.get('music'):
            prompt += "\n- Suggest calming music or nature sounds"
        if features.get('breathing'):
            prompt += "\n- Include a simple breathing exercise (4-7-8 technique)"
        if features.get('mental'):
            prompt += "\n- Suggest a simple mental wellness exercise"
        if features.get('insight'):
            prompt += "\n- Provide emotional insight and reflection"
        
        return prompt
    
    def _get_fallback_response(self, emotion: Dict, crisis: Dict) -> str:
        """Fallback responses when API is unavailable"""
        if crisis.get('is_crisis'):
            return """I'm really concerned about what you're sharing. Your safety is the most important thing right now.

Please reach out to the Suicide and Crisis Lifeline at 988 - they have trained counselors available 24/7 who can provide immediate support. You can also text HOME to 741741.

You're not alone, and these feelings can get better with proper support. Would you like to talk about what's making you feel this way while we connect you with professional help?"""
        
        return f"""I hear that you're feeling {emotion.get('primary_emotion', 'something')}, and it's completely okay to feel that way. Your feelings are valid.

Would you like to share more about what's on your mind? I'm here to listen and support you. Sometimes just talking about our feelings can help us understand them better.

Remember, you're not alone in this. 💙"""