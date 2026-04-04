from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.services.chat_service import ChatService
from app.services.location_service import LocationService
from app.utils.validators import sanitize_input, validate_message
import uuid
import logging
import time

api_bp = Blueprint('api', __name__)
chat_service = ChatService()
location_service = LocationService()
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
    start_time = time.time()
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
        
        logger.info(f"Processing chat request (message length: {len(message)}, session: {session_id[:8]}...)")
        
        # Process message (synchronous)
        result = chat_service.process_message(message, session_id, features)
        
        elapsed = time.time() - start_time
        logger.info(f"Chat request completed in {elapsed:.2f}s")
        
        return jsonify(result)
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Error in chat endpoint (after {elapsed:.2f}s): {str(e)}", exc_info=True)
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
                "name": "National Mental Health Helpline (CCC Line)",
                "type": "phone",
                "contact": "1926",
                "description": "24/7 free and confidential - Sri Lanka"
            },
            {
                "name": "Crisis Support Line",
                "type": "phone",
                "contact": "1333",
                "description": "Toll-free, 24/7 support in Sri Lanka"
            },
            {
                "name": "Sri Lanka Sumithrayo",
                "type": "phone",
                "contact": "011 268 2535 / 0707 308 308",
                "description": "Emotional support for those in despair"
            },
            {
                "name": "Police Emergency",
                "type": "emergency",
                "contact": "119",
                "description": "Sri Lanka Police for immediate help"
            },
            {
                "name": "988 Suicide and Crisis Lifeline",
                "type": "phone",
                "contact": "988",
                "description": "US and Canada (24/7)"
            }
        ]
    })

@api_bp.route('/professional-help', methods=['GET'])
def professional_help():
    """Get professional help resources based on user's IP location"""
    try:
        # Get user's IP address
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ',' in user_ip:
            user_ip = user_ip.split(',')[0].strip()
        
        logger.info(f"Getting professional resources for IP: {user_ip}")
        
        # Get location-based resources
        resources = location_service.get_resources_by_ip(user_ip)
        
        return jsonify(resources)
    except Exception as e:
        logger.error(f"Error in professional_help endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Error retrieving resources",
            "country": "Unknown",
            "crisis_hotline": "Contact local emergency services",
            "resources": [
                "International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres",
                "Psychology Today Therapist Directory: https://www.psychologytoday.com"
            ]
        }), 500