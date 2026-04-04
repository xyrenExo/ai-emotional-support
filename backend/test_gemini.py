"""Test script to verify Gemini API connection and response quality"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import Config
from app.models.gemini_client import GeminiClient

def test_api_key():
    """Test if API key is loaded"""
    print("=" * 60)
    print("TEST 1: API Key Configuration")
    print("=" * 60)
    
    if not Config.GEMINI_API_KEY:
        print("❌ FAILED: GEMINI_API_KEY is not set!")
        print("   Please check your .env file")
        return False
    
    print(f"✅ API Key loaded: {Config.GEMINI_API_KEY[:10]}...")
    return True

def test_gemini_connection():
    """Test Gemini API connection"""
    print("\n" + "=" * 60)
    print("TEST 2: Gemini API Connection")
    print("=" * 60)
    
    try:
        client = GeminiClient()
        print("✅ GeminiClient initialized successfully")
        return client
    except Exception as e:
        print(f"❌ FAILED to initialize GeminiClient: {e}")
        return None

def test_response_quality(client):
    """Test response quality with sample messages"""
    print("\n" + "=" * 60)
    print("TEST 3: Response Quality Test")
    print("=" * 60)
    
    test_cases = [
        {
            "message": "I've been feeling really overwhelmed with work lately. My boss keeps piling on more tasks and I don't know how to keep up.",
            "emotion": {"primary_emotion": "anxiety", "intensity": 0.75, "is_negative": True},
            "crisis": {"is_crisis": False, "risk_level": 0},
            "features": {}
        },
        {
            "message": "I don't really feel anything today. Just kind of neutral I guess.",
            "emotion": {"primary_emotion": "neutral", "intensity": 0.2, "is_negative": False},
            "crisis": {"is_crisis": False, "risk_level": 0},
            "features": {}
        },
        {
            "message": "I had a fight with my best friend and now I'm feeling really sad and lonely.",
            "emotion": {"primary_emotion": "sadness", "intensity": 0.8, "is_negative": True},
            "crisis": {"is_crisis": False, "risk_level": 0},
            "features": {}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"User message: \"{test_case['message'][:80]}...\"")
        print(f"Emotion: {test_case['emotion']['primary_emotion']} ({test_case['emotion']['intensity']:.0%})")
        
        try:
            response = client.generate_response(
                user_message=test_case["message"],
                emotion_context=test_case["emotion"],
                crisis_context=test_case["crisis"],
                features=test_case["features"]
            )
            
            print(f"\n✅ Response ({len(response)} chars):")
            print("-" * 40)
            print(response)
            print("-" * 40)
            
            # Check for common issues
            issues = []
            if response.startswith("I hear that you're feeling"):
                issues.append("Starts with formulaic phrase")
            if "your feelings are valid" in response.lower():
                issues.append("Contains cliché 'your feelings are valid'")
            if "remember, you're not alone" in response.lower():
                issues.append("Contains cliché 'you're not alone'")
            
            if issues:
                print(f"\n⚠️  Quality issues: {', '.join(issues)}")
            else:
                print(f"\n✅ Response looks natural and varied!")
                
        except Exception as e:
            print(f"❌ Error generating response: {e}")

def main():
    print("\n🧪 Gemini API Test Suite\n")
    
    # Test 1: API Key
    if not test_api_key():
        print("\n❌ Cannot proceed without API key. Please check your .env file.")
        return
    
    # Test 2: Connection
    client = test_gemini_connection()
    if not client:
        print("\n❌ Cannot proceed without Gemini client.")
        return
    
    # Test 3: Response Quality
    test_response_quality(client)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
