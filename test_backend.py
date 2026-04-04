import requests
import json

url = "http://localhost:5000/api/chat"

# Test 1: Regular message
payload = {
    "message": "I'm feeling really anxious about my future and nothing seems certain.",
    "features": {"music": True, "breathing": False, "mental": False, "insight": False, "professional_help": False}
}

print("=" * 60)
print("TEST 1: Regular message with music feature")
print("=" * 60)
try:
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Crisis detected: {data.get('crisis', {}).get('is_crisis')}")
    print(f"Emotion: {data.get('emotion', {}).get('primary_emotion')}")
    print(f"\nRESPONSE:\n{data.get('response', 'NO RESPONSE')}")
    print(f"\nResponse length: {len(data.get('response', ''))} chars")
except Exception as e:
    print(f"Error: {e}")
