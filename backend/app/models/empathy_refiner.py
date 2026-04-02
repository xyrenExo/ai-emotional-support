from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import List

class EmpathyRefiner:
    def __init__(self):
        self.model_name = "AliiaR/DialoGPT-medium-empathetic-dialogues"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        
        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def refine(self, gemini_response: str, user_message: str) -> str:
        """Refine Gemini response using DialoGPT for enhanced empathy"""
        
        # Create context with user message and initial response
        context = f"User: {user_message}\nAssistant: {gemini_response}\nRefined:"
        
        # Encode the context
        inputs = self.tokenizer.encode(context, return_tensors='pt')
        
        # Generate refined response
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=200,
                num_return_sequences=1,
                temperature=0.7,
                pad_token_id=self.tokenizer.pad_token_id,
                do_sample=True,
                top_p=0.9
            )
        
        refined = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the refined part
        if "Refined:" in refined:
            refined = refined.split("Refined:")[-1].strip()
        
        # Ensure response isn't too long or short
        if len(refined) < 10:
            refined = gemini_response
        
        if len(refined) > 500:
            refined = refined[:500] + "..."
        
        return refined