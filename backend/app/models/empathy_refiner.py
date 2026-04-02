from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import List
import logging

logger = logging.getLogger(__name__)

# Global model cache to load model only once
_EMPATHY_MODEL = None
_EMPATHY_TOKENIZER = None
_MODEL_LOADED = False

class EmpathyRefiner:
    def __init__(self, skip_empathy=False):
        self.model_name = "AliiaR/DialoGPT-medium-empathetic-dialogues"
        self.skip_empathy = skip_empathy
        self.tokenizer = None
        self.model = None
        
        # Only load model if empathy refinement is enabled
        if not skip_empathy:
            self._ensure_model_loaded()
    
    @classmethod
    def _ensure_model_loaded(cls):
        """Load model only once, globally"""
        global _EMPATHY_MODEL, _EMPATHY_TOKENIZER, _MODEL_LOADED
        
        if _MODEL_LOADED:
            return
        
        try:
            logger.info("Loading EmpathyRefiner model...")
            _EMPATHY_TOKENIZER = AutoTokenizer.from_pretrained("AliiaR/DialoGPT-medium-empathetic-dialogues")
            _EMPATHY_MODEL = AutoModelForCausalLM.from_pretrained("AliiaR/DialoGPT-medium-empathetic-dialogues")
            
            # Add padding token if not present
            if _EMPATHY_TOKENIZER.pad_token is None:
                _EMPATHY_TOKENIZER.pad_token = _EMPATHY_TOKENIZER.eos_token
            
            _MODEL_LOADED = True
            logger.info("EmpathyRefiner model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load EmpathyRefiner model: {e}")
            _MODEL_LOADED = False
    
    def _get_model_and_tokenizer(self):
        """Get cached model and tokenizer"""
        global _EMPATHY_MODEL, _EMPATHY_TOKENIZER
        self._ensure_model_loaded()
        return _EMPATHY_TOKENIZER, _EMPATHY_MODEL
    
    def refine(self, gemini_response: str, user_message: str) -> str:
        """Refine Gemini response using DialoGPT for enhanced empathy"""
        
        # If empathy refinement is disabled, return original response
        if self.skip_empathy:
            return gemini_response
        
        try:
            # Get model and tokenizer
            tokenizer, model = self._get_model_and_tokenizer()
            
            if model is None or tokenizer is None:
                logger.warning("Model not available, returning unrefined response")
                return gemini_response
            
            # Create context with user message and initial response
            context = f"User: {user_message}\nAssistant: {gemini_response}\nRefined:"
            
            # Encode the context
            inputs = tokenizer.encode(context, return_tensors='pt')
            
            # Generate refined response
            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_length=200,
                    num_return_sequences=1,
                    temperature=0.7,
                    pad_token_id=tokenizer.pad_token_id,
                    do_sample=True,
                    top_p=0.9
                )
            
            refined = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the refined part
            if "Refined:" in refined:
                refined = refined.split("Refined:")[-1].strip()
            
            # Ensure response isn't too long or short
            if len(refined) < 10:
                refined = gemini_response
            
            if len(refined) > 500:
                refined = refined[:500] + "..."
            
            return refined
        except Exception as e:
            logger.error(f"Error refining response: {e}")
            # Return original response if refinement fails
            return gemini_response