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
                         features: Dict,
                         conversation_history: List[Dict] = None) -> str:
        """Generate empathetic response using Gemini (synchronous)"""
        
        # Build the system prompt
        system_prompt = self._build_system_prompt(emotion_context, crisis_context, features)
        
        # Build conversation context
        conversation_context = ""
        if conversation_history and len(conversation_history) > 0:
            conversation_context = "\n\nCONVERSATION HISTORY (last 5 exchanges):\n"
            for exchange in conversation_history[-5:]:
                conversation_context += f"User: {exchange.get('user', '')}\n"
                conversation_context += f"Assistant: {exchange.get('assistant', '')}\n\n"
        
        # Full prompt with user message
        full_prompt = f"""{system_prompt}{conversation_context}

CURRENT USER MESSAGE: {user_message}

Generate a response following the guidelines above. Be specific to what the user just shared, reference their situation, and avoid generic responses."""
        
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
6. BE SPECIFIC – Reference what the user actually said, don't give generic responses
7. VARY YOUR RESPONSES – Don't repeat the same phrases across messages
8. ASK FOLLOW-UP QUESTIONS – Help users explore their feelings deeper

RESPONSE GUIDELINES:
- Acknowledge the specific situation the user described
- Validate their emotional reaction to that situation
- Ask a thoughtful follow-up question to help them reflect
- Offer 1-2 practical suggestions if appropriate
- Keep responses conversational and natural (2-4 paragraphs)
- Avoid starting every response with "I hear that you're feeling..."
- Don't repeat the same validation phrases
- If the user mentions a specific event, reference it directly
- Show genuine curiosity about their experience
- Use conversation history to build on previous topics
- Notice patterns in the user's emotions over time
- If the user mentions a specific event, reference it directly
- Show genuine curiosity about their experience
- Use conversation history to build on previous topics
- Notice patterns in the user's emotions over time

TONE: Warm, human-like, calm, conversational

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
            prompt += """

MUSIC SUGGESTIONS FEATURE ENABLED:
- Provide 3-5 specific song/artist recommendations based on the user's mood
- Include genre suggestions (lo-fi, ambient, classical, nature sounds, etc.)
- Explain why each suggestion might help their current emotional state
- Format as a bulleted list with brief descriptions
- Example: "🎵 'Weightless' by Marconi Union - Scientifically proven to reduce anxiety"
"""
        if features.get('breathing'):
            prompt += """

BREATHING EXERCISES FEATURE ENABLED:
- Provide a specific breathing technique with step-by-step instructions
- Include timing (e.g., 4-7-8 technique, box breathing, alternate nostril)
- Explain how to do it clearly with counts
- Mention how long to practice and when to use it
- Format as numbered steps
- Example: "Try the 4-7-8 technique: 1) Inhale for 4 counts, 2) Hold for 7 counts, 3) Exhale for 8 counts"
"""
        if features.get('mental'):
            prompt += """

MENTAL EXERCISES FEATURE ENABLED:
- Provide a specific cognitive reframing or mental wellness exercise
- Include step-by-step instructions
- Explain the psychological benefit
- Make it actionable and practical
- Format as numbered steps
- Example: "Try the 5-4-3-2-1 grounding technique: Name 5 things you see, 4 you can touch..."
"""
        if features.get('insight'):
            prompt += """

MOOD INSIGHTS FEATURE ENABLED:
- Analyze the emotional patterns in what the user shared
- Identify underlying themes or triggers
- Provide reflective questions to help them understand their emotions better
- Point out any cognitive distortions gently (e.g., catastrophizing, black-and-white thinking)
- Help them see connections between events and feelings
- Format insights as bullet points with explanations
"""
        if features.get('professional_help'):
            prompt += """

PROFESSIONAL HELP FEATURE ENABLED:
- Acknowledge when professional help might be beneficial
- Suggest connecting with a therapist or counselor if appropriate
- Normalize seeking professional mental health support
- Provide gentle encouragement without being pushy
"""
        
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