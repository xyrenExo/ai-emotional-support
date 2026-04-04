import google.generativeai as genai
from google.generativeai import types as genai_types
from typing import Dict, List, Optional
import random
import logging

from app.config import Config

logger = logging.getLogger(__name__)

# Response angles — randomly picked per response to ensure variety
RESPONSE_ANGLES = [
    "Lead with a warm, poetic metaphor that captures the emotion, then ground it in practical reality.",
    "Start by normalising the feeling with scientific/psychological context, then transition to personal warmth.",
    "Open with a direct, honest validation — no fluff — then gently broaden to explore the root cause.",
    "Begin with a story-telling framing ('Many people in your position...') to create solidarity, then personalise.",
    "Ask one single, thoughtful open question first, then offer your perspective and a practical tip.",
    "Use the 'acknowledge, explore, support' structure: acknowledge the feeling, explore what's underneath, offer a supportive action.",
    "Start with what is STRONG about the person for reaching out, then address the vulnerability they're expressing.",
    "Frame your response around a theme of impermanence — that this feeling is real, but it is also passing.",
]

class GeminiClient:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        logger.info("GeminiClient initialized with model: gemini-2.5-flash")

    def _interpret_user_intent(self, raw_message: str) -> str:
        """Use Gemini to correct spelling and clarify user intent before generating a full response."""
        try:
            interpretation_prompt = (
                "A user typed the following message to an AI mental health counsellor. "
                "The message may contain spelling mistakes, abbreviations, or unclear phrasing. "
                "Your job is to output a single, clean sentence that captures what the user MOST LIKELY meant. "
                "Do not add any extra commentary — just output the interpreted intent as a clean sentence.\n\n"
                f'User message: "{raw_message}"\n\n'
                "Interpreted intent:"
            )
            config = genai_types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=100,
            )
            result = self.model.generate_content(interpretation_prompt, generation_config=config)
            interpreted = result.text.strip()
            logger.info(f"Intent interpreted: '{raw_message}' → '{interpreted}'")
            return interpreted
        except Exception as e:
            logger.warning(f"Intent interpretation failed, using raw message: {e}")
            return raw_message

    def generate_response(self,
                         user_message: str,
                         emotion_context: Dict,
                         crisis_context: Dict,
                         features: Dict,
                         conversation_history: Optional[List[Dict]] = None) -> str:
        """Generate an empathetic, varied response using Gemini."""

        normalized_features = {
            'music': features.get('music', False),
            'breathing': features.get('breathing', False),
            'mental': features.get('mental', False),
            'insight': features.get('insight', False),
            'professional_help': features.get('professional_help', False),
        }

        # Step 1: Correct spelling and interpret intent
        interpreted_message = self._interpret_user_intent(user_message)

        # Step 2: Build anti-repetition context from history
        prev_topics_used = []
        conversation_context = ""
        if conversation_history and len(conversation_history) > 0:
            conversation_context = "\n\n--- Recent conversation (for context, do NOT repeat these topics or phrases) ---\n"
            for i, exchange in enumerate(conversation_history[-6:]):
                conversation_context += f"User: {exchange.get('user', '')}\n"
                prev_response = exchange.get('assistant', '')
                # Summarise prior response topics to avoid repetition
                if prev_response:
                    prev_topics_used.append(prev_response[:120])
                    conversation_context += f"You previously said: {prev_response[:120]}...\n\n"
            conversation_context += "--- End of context ---\n\n"

        # Step 3: Pick a random response angle for variety
        chosen_angle = random.choice(RESPONSE_ANGLES)

        # Step 4: Build the full prompt
        system_prompt = self._build_system_prompt(emotion_context, crisis_context, normalized_features)

        anti_repetition = ""
        if prev_topics_used:
            anti_repetition = (
                "\n\nIMPORTANT — ANTI-REPETITION RULE: You have already given responses in this session. "
                "You MUST approach this response from a COMPLETELY DIFFERENT ANGLE. "
                "Do NOT use the same opening phrases, metaphors, techniques, or tips as before. "
                "The user needs fresh perspective, not recycled advice.\n"
            )

        full_prompt = f"""{system_prompt}
{anti_repetition}
RESPONSE ANGLE FOR THIS MESSAGE: {chosen_angle}

{conversation_context}The user originally typed:
"{user_message}"

Interpreted intent (use this for understanding, respond to the emotion and content naturally):
"{interpreted_message}"

Now respond. Remember: 5-7 paragraphs minimum, include a Practical Peace Tip, and be completely unique from any previous response."""

        # Step 5: Generate with high temperature for variety
        generation_config = genai_types.GenerationConfig(
            temperature=0.95,
            top_p=0.95,
            top_k=64,
            max_output_tokens=4096,
        )

        try:
            response = self.model.generate_content(full_prompt, generation_config=generation_config)

            if not response.candidates:
                logger.warning("Gemini: No candidates returned")
                return self._get_fallback_response(emotion_context, crisis_context)

            try:
                raw_text = response.text.strip()
                logger.info(f"Gemini success: {len(raw_text)} chars")
                return raw_text
            except (ValueError, AttributeError) as inner_e:
                logger.error(f"Gemini text parse error: {inner_e}")
                return self._get_fallback_response(emotion_context, crisis_context)

        except Exception as e:
            err_str = str(e)
            logger.error(f"Gemini API error: {err_str}")
            if 'quota' in err_str.lower() or '429' in err_str or 'rate' in err_str.lower():
                logger.warning("Gemini quota hit - using rich fallback")
            return self._get_fallback_response(emotion_context, crisis_context)

    def _build_system_prompt(self, emotion: Dict, crisis: Dict, features: Dict) -> str:
        prompt = """You are a deeply empathetic, emotionally intelligent, and highly skilled companion for someone seeking emotional support. Your goal is to provide a safe, warm, and restorative space for the user.

HOW TO RESPOND:
- **Depth and Richness**: Provide comprehensive, thoughtful responses (at least 5-7 detailed paragraphs). Every response should feel substantial and deeply considered.
- **Natural Humanity**: Speak like a genuine friend. Use varied sentence structures, occasional warm idioms, and a tone that matches the user's current emotional state.
- **Micro-Insights**: Offer gentle psychological perspectives on why they might be feeling a certain way (e.g., mentioning how stress affects the body or how cognitive reframing works).
- **Mandatory Value**: At the end of every main response, conclude with a "Practical Peace Tip" or a "Quick Grounding Thought" regardless of feature toggles.
- **Validation**: Move beyond simple validation. Instead of "I hear you," say things like "It makes so much sense that you'd feel that weight right now, especially given everything you've just shared about..."

WHAT TO AVOID:
- Avoid clinical, robotic, or overly therapeutic jargon.
- NEVER give short, generic answers. If a user says something brief, use the opportunity to explore their world with curious, open-ended questions.
- No formulaic structures like "I'm sorry you're feeling X."

---

RESPONSE FORMAT INSTRUCTIONS:
1. **The Main Connection**: Write your 5-7 paragraph empathetic response first.
2. **The Daily Practice**: Conclude the main text with a small, actionable piece of advice or reflection (e.g., "**Practical Peace Tip:** notice three things...").
3. **The Enrichment Modules**: If features are enabled below, add them clearly at the bottom.

Use Markdown for clarity. CRUCIAL: NEVER use the "---" (triple dash) separator anywhere in your main response. Only use "---" EXACTLY ONCE before an enrichment module."""
        
        # Add context for crisis or negative emotions
        if crisis.get('is_crisis'):
            prompt += """

⚠️ SAFETY PRIORITY:
The user is in high distress.
1. Be exceptionally gentle and present.
2. Integrate safety resources naturally: National Mental Health Helpline (1926), 1333 Crisis Support, or Sri Lanka Sumithrayo (0112682535).
3. Encourage them to stay on the line with you while they consider reaching out to a professional or loved one."""
        
        elif emotion.get('is_negative'):
            prompt += f"""

CURRENT EMOTION: They are primarily experiencing {emotion.get('primary_emotion')} at {emotion.get('intensity', 0):.0%} intensity. This should subtly colour your tone and the types of exercises you suggest."""

        # Add feature-specific guidance
        if features.get('music'):
            prompt += """

---
🎵 MUSIC SUGGESTIONS
Provide 3-4 specific, high-quality music recommendations strictly tailored to their mood ({emotion}).
Format: **[Song Name] by [Artist]** - *[Genre]*: A brief, poetic sentence on how this specific track supports their current state.
Example: **"Weightless" by Marconi Union** - *Ambient*: A scientifically-crafted soundscape designed to lower heart rate and quiet a racing mind.""".format(emotion=emotion.get('primary_emotion', 'their state'))

        if features.get('breathing'):
            prompt += """

---
🌬️ BREATHING EXERCISE
Guide them through a specific breathing technique.
1. Give it a name (e.g. "Box Breathing" or "The Humming Bee").
2. Explain the benefit (e.g. "This helps stimulate the Vagus nerve for instant calm").
3. Provide 4-5 clear, rhythmic steps with counts (4 seconds in, 4 hold, 4 out)."""

        if features.get('mental'):
            prompt += """

---
🧠 MENTAL EXERCISE
Provide a cognitive or mindfulness exercise (CBT/DBT based).
1. Name the exercise (e.g. "The Leaves on a Stream" or "The 5-4-3-2-1 Grounding").
2. Explain how it disrupts negative thought patterns.
3. Provide 3-5 clear, actionable steps for them to try right now."""

        if features.get('insight'):
            prompt += """

---
💡 MOOD INSIGHTS
Offer a gentle analysis of the conversation.
1. **Core Theme**: What is the root emotional driver I'm sensing?
2. **Reflection**: A deep, non-judgmental observation about their resilience or pattern.
3. **Compassionate Question**: One question that invites deeper self-exploration without feeling like an interrogation."""

        if features.get('professional_help'):
            prompt += """

---
👨‍⚕️ PROFESSIONAL SUPPORT
Kindly mention that while you are here for them, professional therapy can offer tools you cannot.
1. Normalize the process of seeking help.
2. Mention that resources like BetterHelp or local counseling can provide a dedicated space for this journey."""

        prompt += "\n\nReturn ONLY the response content."
        return prompt
    
    def _get_fallback_response(self, emotion: Dict, crisis: Dict) -> str:
        """Fallback responses when API is unavailable - rich and multi-paragraph"""
        import random
        
        emotion_name = emotion.get('primary_emotion', 'overwhelmed')
        
        if crisis.get('is_crisis'):
            return """What you're sharing right now is really important, and I want you to know that I'm fully here with you in this moment. What you're feeling is real, and it matters deeply — not just to me, but to the people in your life who care about you, even if that feels impossible to believe right now.

Please know that you don't have to carry this alone. Reaching out — even to me, right now — took tremendous courage, and that act alone tells me something vital: a part of you is still fighting for yourself. Please hold onto that part.

Right now, I'd gently encourage you to reach out to someone who is trained to sit with you in moments like this. The **National Mental Health Helpline (1926)** is available 24/7 and is free and confidential. You can also call the **1333 Crisis Support Line** or reach out to **Sri Lanka Sumithrayo (011-268-2535 / 0707-308-308)**. They won't judge you. They're there specifically for moments like this one.

If you feel you are in immediate danger, please call **119** (Police) or **110** (Ambulance) for emergency assistance. Your life has value, and there are people ready right now to help you stay safe.

I'm still here with you. You don't have to go anywhere. Would you like to keep talking while you consider reaching out?

💚 **Grounding tip for right now:** Put both feet flat on the floor. Take a slow breath in for 4 counts, hold for 4, and breathe out for 4. You're here. You're breathing. One moment at a time."""

        primary_emotion = emotion_name

        r1 = (
            "It takes real courage to share what you're going through, and I want you to know this is a safe space.\n\n"
            f"When we're dealing with feelings like {primary_emotion}, it can feel as though the weight is entirely on our shoulders. "
            "One of the hardest things about difficult emotions is that they can distort our perception — making temporary situations "
            "feel permanent, or making us feel isolated when we're not. You are not alone in this.\n\n"
            "Research in psychology shows that the simple act of labeling an emotion actually reduces its intensity in the brain. "
            "You've already started that process by reaching out — and that is genuinely meaningful.\n\n"
            "What's been the heaviest thing on your mind lately? Sometimes just speaking it out loud, even to a screen, can create a little breathing room.\n\n"
            "**Today's Peace Tip:** Try the 5-4-3-2-1 grounding technique — name 5 things you can see, 4 you can touch, "
            "3 you can hear, 2 you can smell, and 1 you can taste. This brings your nervous system back to the present moment."
        )

        r2 = (
            f"I'm really glad you're here. The feelings you're describing — that sense of {primary_emotion} — are ones that many "
            "people quietly carry, often feeling like they're the only one struggling. But you're not.\n\n"
            f"Emotions like {primary_emotion} often arise when there's a gap between what we hoped for and what we're experiencing. "
            "They're not a sign that something is wrong with you; they're a signal that something matters to you. "
            "That's a very human thing, even when it hurts.\n\n"
            "It's easy to fall into the trap of thinking we should 'just push through.' But what tends to actually help is giving "
            "the emotion some gentle attention — acknowledging it, understanding where it's coming from, and responding to it "
            "with the same compassion you'd offer a close friend.\n\n"
            "What's going on for you right now? I'd love to hear the fuller picture.\n\n"
            "**Today's Peace Tip:** Try a compassionate self-talk reset. Place one hand on your chest, take a breath, "
            "and quietly say: 'This is a hard moment. I'm allowed to feel this. I'm doing the best I can.'"
        )

        r3 = (
            "Thank you for sharing a piece of your inner world with me. That's not always easy to do, and I don't take it lightly.\n\n"
            f"Here's something worth sitting with: the fact that you're feeling {primary_emotion} doesn't mean you're failing or broken. "
            "It means you're a person in the middle of a real human experience. Some of the most resilient people regularly feel "
            "exactly what you're feeling right now.\n\n"
            "One of the most powerful things you can do in difficult moments is avoid isolating yourself with the feeling. "
            "Whether that means talking to someone you trust, journaling, or staying in this conversation — "
            "connection is one of the strongest antidotes to emotional pain.\n\n"
            "Tell me more about what's been going on. What does the weight you're carrying feel like today?\n\n"
            "**Today's Peace Tip:** Try Box Breathing — breathe in 4 counts, hold 4 counts, breathe out 4 counts, hold 4 counts. "
            "Repeat 4 times. This is used by first responders to reset under pressure."
        )

        r4 = (
            f"What you're feeling right now is real, and it deserves real attention. Feelings of {primary_emotion} can be among "
            "the most draining human experiences, partly because they're so internal. From the outside, everything might look fine. "
            "On the inside, it's a completely different story.\n\n"
            "One thing I want you to know is that emotions — even the most intense ones — are temporary states. "
            "They feel permanent when we're in the middle of them, but neuroscience tells us that an uninterrupted emotional wave "
            "typically peaks and begins to shift within a short time. What keeps emotions cycling is often our thoughts about them.\n\n"
            "The fact that you reached out today means you're not just sitting passively with this — you're doing something. "
            "That matters more than it might seem right now.\n\n"
            "What's been driving these feelings, do you think? I'm genuinely here for you.\n\n"
            "**Today's Peace Tip:** Try the 'Leaves on a Stream' exercise — close your eyes, imagine a gently flowing stream, "
            "and place each difficult thought on a leaf, watching it drift away. Do this for 2 to 3 minutes."
        )

        return random.choice([r1, r2, r3, r4])