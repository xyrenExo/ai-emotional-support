import re
from typing import Tuple, List, Dict

class CrisisDetector:
    def __init__(self):
        self.crisis_patterns = [
            r'\b(suicide|kill myself|end my life|want to die)\b',
            r'\b(self[-]?harm|hurt myself|cut myself)\b',
            r'\b(hopeless|worthless|no reason to live)\b',
            r'\b(crisis hotline|emergency|help me)\b',
            r'\b(going to end it|can\'t go on)\b'
        ]
        
        self.high_risk_patterns = [
            r'\b(today|tonight|right now)\s+(i will|i\'m going to)',
            r'\b(plan to|have a plan)'
        ]
        
        self.support_resources = {
            "national_suicide_prevention": "988 Suicide and Crisis Lifeline",
            "crisis_text_line": "Text HOME to 741741",
            "emergency": "Call 911 for immediate emergency assistance"
        }
    
    def detect(self, text: str) -> Dict:
        """Detect crisis indicators in user message"""
        text_lower = text.lower()
        
        # Check for crisis patterns
        crisis_matches = []
        for pattern in self.crisis_patterns:
            if re.search(pattern, text_lower):
                crisis_matches.append(pattern)
        
        # Check for high risk indicators
        high_risk = False
        for pattern in self.high_risk_patterns:
            if re.search(pattern, text_lower):
                high_risk = True
                crisis_matches.append(pattern)
        
        is_crisis = len(crisis_matches) > 0
        
        return {
            "is_crisis": is_crisis,
            "high_risk": high_risk,
            "matches": crisis_matches,
            "severity": "high" if high_risk else ("medium" if is_crisis else "none"),
            "resources": self.support_resources if is_crisis else {}
        }