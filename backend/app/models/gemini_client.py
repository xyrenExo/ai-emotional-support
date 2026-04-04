import google.generativeai as genai
from typing import Dict, List, Optional
import threading
from app.config import Config

class GeminiClient:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def generate_response(self, 
                         user_message: str, 
                         emotion_context: Dict,
                         crisis_context: Dict,
                         features: Dict,
                         conversation_history: Optional[List[Dict]] = None) -> str:
        """Generate empathetic response using Gemini (synchronous)"""
        
        # Normalize features dict (ensure all keys are present with boolean values)
        normalized_features = {
            'music': features.get('music', False),
            'breathing': features.get('breathing', False),
            'mental': features.get('mental', False),
            'insight': features.get('insight', False),
            'professional_help': features.get('professional_help', False),
        }
        
        # Build the system prompt
        system_prompt = self._build_system_prompt(emotion_context, crisis_context, normalized_features)
        
        # Build conversation context
        conversation_context = ""
        if conversation_history and len(conversation_history) > 0:
            conversation_context = "\n\n--- Previous conversation ---\n"
            for exchange in conversation_history[-5:]:
                conversation_context += f"User: {exchange.get('user', '')}\n"
                conversation_context += f"You: {exchange.get('assistant', '')}\n\n"
            conversation_context += "--- End of previous conversation ---\n\n"
        
        # Full prompt with user message
        full_prompt = f"""{system_prompt}

{conversation_context}Here's what they just said:

"{user_message}"

Respond naturally and thoughtfully."""
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._get_fallback_response(emotion_context, crisis_context)
    
    def _build_system_prompt(self, emotion: Dict, crisis: Dict, features: Dict) -> str:
        prompt = """You are a warm, emotionally intelligent companion having a natural conversation with someone who needs support. You're not a therapist or counselor - you're a caring presence who listens well and responds thoughtfully.

HOW TO RESPOND:
- Talk like a real person would - use natural language, varied sentence lengths, and genuine warmth
- Reference specific details from what they shared, not just their emotion label
- Show curiosity about their experience with thoughtful questions
- Validate their feelings without being repetitive or formulaic
- Share gentle insights or perspectives when appropriate
- Keep it conversational - 2-4 short paragraphs feels natural

WHAT TO AVOID:
- Don't start with "I hear that you're feeling..." or similar formulaic openings
- Don't use the same validation phrases repeatedly ("your feelings are valid", "it's okay to feel that way")
- Don't give generic advice that could apply to anyone
- Don't be overly clinical or therapeutic in your language
- Don't repeat yourself across messages
- Avoid clichés like "remember you're not alone" unless genuinely fitting
- Don't use excessive emojis - one at most if it feels natural

RESPONSE STYLE:
- Vary your openings - sometimes acknowledge their situation, sometimes ask a gentle question, sometimes share a thoughtful observation
- Use conversational language - contractions, natural phrasing, occasional pauses
- Be specific to their situation - reference events, people, or circumstances they mentioned
- Show genuine interest - ask questions that help them explore their feelings deeper
- Offer suggestions naturally, not as a list of instructions
- Match their energy - if they're brief, don't overwhelm with long responses
- Build on previous conversation - reference things they've shared before

TONE: Like a thoughtful friend who's good at listening - warm, present, and genuinely interested in understanding them.

---

RESPONSE FORMAT INSTRUCTIONS:
First, write your main empathetic response (2-4 paragraphs).
Then, if any features are enabled below, add them in the order they appear, separated by a blank line."""
        
        # Add context
        if crisis.get('is_crisis'):
            prompt += """

⚠️ CRISIS SITUATION:
This person may be in serious distress. Respond with genuine care and urgency.
- Encourage them to reach out to someone they trust
- Share crisis resources naturally (988 Lifeline, text HOME to 741741)
- Stay present and supportive
- Safety comes first"""
        
        if emotion.get('is_negative'):
            prompt += f"""

They're experiencing {emotion.get('primary_emotion')} ({emotion.get('intensity', 0):.0%} intensity). Be gentle and present with them."""
        
        # Add feature-specific guidance with clear formatting
        if features.get('music'):
            prompt += """

---
🎵 MUSIC SUGGESTIONS (Include this section)
Based on their mood ({emotion}), suggest 3-5 specific songs or artists:
Format each as: [Song/Artist] - Genre (Brief explanation of why it helps)

Examples:
• Weightless - Marconi Union (Ambient) - Scientifically designed to reduce anxiety
• Nuvole Bianche - Ludovico Einaudi (Classical/Piano) - Calming instrumental piece
• Lo-fi hip hop beats - Various Artists (Lo-fi) - Great for focus and gentle relaxation
• Desert Skies - Ólafur Arnalds (Minimalist) - Peaceful and meditative

Include the genre in parentheses and provide brief reasoning for each pick.""".format(emotion=emotion.get('primary_emotion', 'their current state'))
        
        if features.get('breathing'):
            prompt += """

---
🌬️ BREATHING EXERCISES (Include this section)
Provide ONE specific breathing technique with step-by-step instructions:

Format as numbered steps with timing:
1. [Description of starting position]
2. [Inhale instruction with count] (e.g., "Inhale slowly through your nose for 4 counts")
3. [Hold instruction with count] (e.g., "Hold for 7 counts")
4. [Exhale instruction with count] (e.g., "Exhale slowly through your mouth for 8 counts")
5. [Repetition instruction] (e.g., "Repeat 5-10 times")

Include the name of the technique (e.g., "4-7-8 Breathing") and a brief explanation of its benefits."""
        
        if features.get('mental'):
            prompt += """

---
🧠 MENTAL EXERCISE (Include this section)
Provide ONE specific, actionable mental/cognitive exercise:

Format as numbered steps:
1. [Exercise name and purpose]
2. [Clear instruction step 1]
3. [Clear instruction step 2]
4. [Clear instruction step 3]
5. [How to use this regularly]

Examples:
- 5-4-3-2-1 Grounding: Name 5 things you see, 4 you can feel, 3 you hear, 2 you smell, 1 you taste
- Thought Reframing: Identify negative thought → Challenge it → Replace with realistic alternative
- Worry Time: Set 10 minutes to write down worries → Review what's in your control → Plan action

Make it easy to follow and explain the psychological benefit."""
        
        if features.get('insight'):
            prompt += """

---
💡 MOOD INSIGHTS (Include this section)
Analysis of emotional patterns in what they shared:

Identify:
1. PRIMARY TRIGGER or THEME - What seems to be at the root?
2. EMOTIONAL PATTERN - Any patterns you notice?
3. COGNITIVE DISTORTION (if any) - Gently point out (catastrophizing, all-or-nothing thinking, etc.)
4. STRENGTH - Something positive or resilient they showed
5. REFLECTION QUESTION - A thoughtful question to help them explore deeper

Format as a numbered list with brief explanations."""
        
        if features.get('professional_help'):
            prompt += """

---
👨‍⚕️ PROFESSIONAL SUPPORT (Include this section if appropriate)
ONLY include this if it's genuinely relevant to what they shared.
- Acknowledge that professional support could help
- Normalize seeking therapy or counseling
- Avoid being pushy - frame it as an option
- Suggest types of professionals if relevant (therapist, counselor, psychiatrist)

Example: "Speaking with a therapist could really help you work through this. Many people find it helpful to have a trained professional to talk to about anxiety like what you're experiencing."
"""
        
        prompt += """

---

Return ONLY your response - no explanations, no meta-commentary."""
        
        return prompt
    
    def _get_fallback_response(self, emotion: Dict, crisis: Dict) -> str:
        """Fallback responses when API is unavailable"""
        import random
        
        if crisis.get('is_crisis'):
            return """I'm really concerned about what you're sharing. Your safety matters so much.

Please consider reaching out to the Suicide and Crisis Lifeline at 988 - there are trained counselors available right now who can help. You can also text HOME to 741741.

I'm still here with you. Would you like to keep talking while we figure this out together?"""
        
        # Varied fallback responses for non-crisis situations
        fallbacks = [
            f"""That sounds like a lot to carry. {emotion.get('primary_emotion', 'Feeling this way')} is completely understandable given what you're going through.

What's been on your mind lately? I'd love to hear more if you want to share.""",
            
            f"""Thank you for sharing that with me. It takes courage to put feelings into words, especially when things feel {emotion.get('primary_emotion', 'unclear')}.

Is there anything specific that's been weighing on you? Sometimes talking it through can bring some clarity.""",
            
            f"""I appreciate you opening up. {emotion.get('primary_emotion', 'These feelings')} can be really tough to sit with, and you don't have to navigate them alone.

What's been going through your mind? I'm here to listen.""",
            
            f"""That's a lot to process. However you're feeling right now is completely valid - there's no right or wrong way to feel.

Want to talk more about what's been on your mind? Sometimes just putting thoughts into words can help.""",
            
            f"""Thanks for trusting me with this. {emotion.get('primary_emotion', 'Feeling stuck')} can be exhausting, and it's okay to take things one moment at a time.

What would feel most helpful right now - just talking, or exploring some ideas together?"""
        ]
        
        return random.choice(fallbacks)