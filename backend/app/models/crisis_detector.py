import re
from typing import Tuple, List, Dict

class CrisisDetector:
    def __init__(self):
        self.crisis_patterns = [
            r'\b(suicide|kill myself|end my life|want to die|take my life)\b',
            r'\b(self[-]?harm|hurt myself|cut myself|burning myself)\b',
            r'\b(hopeless|worthless|no reason to live|no way out)\b',
            r'\b(crisis hotline|emergency|help me|need help right now)\b',
            r'\b(going to end it|can\'t go on|it\'s final|goodbye everyone)\b',
            r'\b(burden to everyone|everyone is better off without me)\b'
        ]
        
        self.high_risk_patterns = [
            r'\b(today|tonight|right now|immediately)\s+(i will|i\'m going to|doing it)\b',
            r'\b(have a plan|method|note ready|goodbye letter)\b',
            r'\b(nothing matters anymore|it is time to leave)\b'
        ]
        
        self.support_resources = {
            "ccc_line": "1926 (National Mental Health Helpline - Sri Lanka)",
            "1333_crisis_line": "1333 (Crisis Support Line - Toll Free)",
            "sumithrayo": "011 268 2535 / 0707 308 308 (Sri Lanka Sumithrayo)",
            "emergency_sri_lanka": "Call 119 (Police) or 110 (Ambulance) for immediate assistance",
            "international_resources": "https://www.iasp.info/resources/Crisis_Centres"
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