from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.services.chat_service import ChatService
from app.utils.validators import sanitize_input, validate_message
import uuid
import logging

api_bp = Blueprint('api', __name__)
chat_service = ChatService()
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

@api_bp.route('/analyze', methods=['POST'])
@limiter.limit("30 per minute")
def analyze():
    """Analyze user message for emotions"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
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
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": "Error analyzing message"}), 500

@api_bp.route('/chat', methods=['POST'])
@limiter.limit("30 per minute")
def chat():
    """Main chat endpoint"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
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
        
        # Process message (synchronous)
        result = chat_service.process_message(message, session_id, features)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": "Error processing message. Please try again."}), 500

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