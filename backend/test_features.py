"""Test script to verify feature integration with Gemini"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import Config
from app.models.gemini_client import GeminiClient

def test_features():
    """Test all features with Gemini"""
    print("=" * 70)
    print("FEATURE INTEGRATION TEST")
    print("=" * 70)
    
    if not Config.GEMINI_API_KEY:
        print("❌ FAILED: GEMINI_API_KEY is not set!")
        return

    client = GeminiClient()
    
    test_cases = [
        {
            "name": "Music Suggestions Test",
            "message": "I've been feeling really stressed and anxious lately. Work has been overwhelming and I can't seem to relax.",
            "emotion": {"primary_emotion": "anxiety", "intensity": 0.8, "is_negative": True},
            "crisis": {"is_crisis": False, "risk_level": 0},
            "features": {"music": True, "breathing": False, "mental": False, "insight": False, "professional_help": False},
        },
        {
            "name": "Breathing Exercise Test",
            "message": "My heart is racing and I feel like I can't breathe. I'm panicking about an upcoming exam.",
            "emotion": {"primary_emotion": "fear", "intensity": 0.85, "is_negative": True},
            "crisis": {"is_crisis": False, "risk_level": 0},
            "features": {"music": False, "breathing": True, "mental": False, "insight": False, "professional_help": False},
        },
        {
            "name": "Mental Exercise Test",
            "message": "I keep having negative thoughts about myself. I feel like everything is my fault and I can't do anything right.",
            "emotion": {"primary_emotion": "sadness", "intensity": 0.75, "is_negative": True},
            "crisis": {"is_crisis": False, "risk_level": 0},
            "features": {"music": False, "breathing": False, "mental": True, "insight": False, "professional_help": False},
        },
        {
            "name": "Mood Insights Test",
            "message": "I notice that every time my friend cancels plans, I feel rejected and worthless. This has been happening since childhood.",
            "emotion": {"primary_emotion": "sadness", "intensity": 0.7, "is_negative": True},
            "crisis": {"is_crisis": False, "risk_level": 0},
            "features": {"music": False, "breathing": False, "mental": False, "insight": True, "professional_help": False},
        },
        {
            "name": "All Features Test",
            "message": "I've been struggling with depression for months now. Nothing seems to help and I don't know what to do anymore.",
            "emotion": {"primary_emotion": "sadness", "intensity": 0.85, "is_negative": True},
            "crisis": {"is_crisis": False, "risk_level": 0},
            "features": {"music": True, "breathing": True, "mental": True, "insight": True, "professional_help": True},
        },
    ]
    
    for test_case in test_cases:
        print(f"\n{'=' * 70}")
        print(f"TEST: {test_case['name']}")
        print(f"{'=' * 70}")
        print(f"\nUser Message: {test_case['message'][:100]}...")
        print(f"Emotion: {test_case['emotion']['primary_emotion']} ({test_case['emotion']['intensity']:.0%})")
        
        enabled_features = [k for k, v in test_case['features'].items() if v]
        print(f"Enabled Features: {', '.join(enabled_features) if enabled_features else 'None'}")
        print("\n" + "-" * 70)
        
        try:
            response = client.generate_response(
                user_message=test_case["message"],
                emotion_context=test_case["emotion"],
                crisis_context=test_case["crisis"],
                features=test_case["features"]
            )
            
            print("RESPONSE:")
            print(response)
            print("\n" + "-" * 70)
            
            # Check if expected sections are present
            sections_found = []
            if test_case['features'].get('music') and '🎵' in response:
                sections_found.append("Music Suggestions ✓")
            if test_case['features'].get('breathing') and '🌬️' in response:
                sections_found.append("Breathing Exercises ✓")
            if test_case['features'].get('mental') and '🧠' in response:
                sections_found.append("Mental Exercise ✓")
            if test_case['features'].get('insight') and '💡' in response:
                sections_found.append("Mood Insights ✓")
            if test_case['features'].get('professional_help') and '👨‍⚕️' in response:
                sections_found.append("Professional Support ✓")
            
            if sections_found:
                print(f"✅ Features found in response:")
                for section in sections_found:
                    print(f"   • {section}")
            else:
                missing = [k for k, v in test_case['features'].items() if v]
                if missing:
                    print(f"⚠️  Expected features not found: {', '.join(missing)}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            if "429" in str(e) or "quota" in str(e).lower():
                print("   → API quota exceeded. Try again later or use a new API key.")
            
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_features()
