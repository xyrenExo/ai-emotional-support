from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.services.chat_service import ChatService
from app.utils.validators import sanitize_input, validate_message
import uuid

api_bp = Blueprint('api', __name__)
chat_service = ChatService()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

@api_bp.route('/analyze', methods=['POST'])
@limiter.limit("30 per minute")
def analyze():
    """Analyze user message for emotions"""
    data = request.json
    message = data.get('message', '')
    
    # Validate and sanitize input
    if not validate_message(message):
        return jsonify({"error": "Invalid message"}), 400
    
    message = sanitize_input(message)
    
    # Detect emotions
    emotion_result = chat_service.emotion_detector.detect(message)
    
    return jsonify({
        "emotion": emotion_result["primary_emotion"],
        "intensity": emotion_result["intensity"],
        "is_negative": emotion_result["is_negative"]
    })

@api_bp.route('/chat', methods=['POST'])
@limiter.limit("30 per minute")
async def chat():
    """Main chat endpoint"""
    data = request.json
    message = data.get('message', '')
    session_id = data.get('session_id', str(uuid.uuid4()))
    features = data.get('features', {
        "music": False,
        "breathing": False,
        "mental": False,
        "insight": False,
        "professional_help": False
    })
    
    # Validate input
    if not validate_message(message):
        return jsonify({"error": "Invalid message"}), 400
    
    message = sanitize_input(message)
    
    # Process message
    result = await chat_service.process_message(message, session_id, features)
    
    return jsonify(result)

@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "services": {
            "emotion_detection": "active",
            "crisis_detection": "active",
            "gemini": "configured",
            "empathy_refiner": "active"
        }
    })

@api_bp.route('/crisis-resources', methods=['GET'])
def crisis_resources():
    """Get crisis support resources"""
    return jsonify({
        "resources": [
            {
                "name": "988 Suicide and Crisis Lifeline",
                "type": "phone",
                "contact": "988",
                "description": "24/7 free and confidential support"
            },
            {
                "name": "Crisis Text Line",
                "type": "text",
                "contact": "741741",
                "description": "Text HOME to 741741"
            },
            {
                "name": "Emergency Services",
                "type": "emergency",
                "contact": "911",
                "description": "For immediate life-threatening situations"
            }
        ]
    })