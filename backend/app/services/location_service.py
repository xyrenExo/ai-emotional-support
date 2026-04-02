import requests
import logging
from typing import Dict, Optional
from functools import lru_cache

logger = logging.getLogger(__name__)

# Professional help resources by country
PROFESSIONAL_RESOURCES = {
    "US": {
        "country": "United States",
        "crisis_hotline": "988 Suicide & Crisis Lifeline",
        "crisis_number": "988",
        "crisis_text": "Text HOME to 741741",
        "therapist_directory": "https://www.psychologytoday.com/us/basics/therapy",
        "resources": [
            "NAMI Helpline: 1-800-950-NAMI (6264) - Mon-Fri 10am-10pm ET",
            "Crisis Text Line: Text HOME to 741741",
            "Veterans Crisis Line: 988 then press 1",
            "SAMHSA National Helpline: 1-800-662-4357 (free, confidential, 24/7)"
        ]
    },
    "CA": {
        "country": "Canada",
        "crisis_hotline": "1-833-456-4566 (Canada Suicide Prevention Service)",
        "crisis_number": "1-833-456-4566",
        "crisis_text": "Text HELLO to 741741",
        "therapist_directory": "https://www.psychologytoday.com/ca/basics/therapy",
        "resources": [
            "Talk Suicide Canada: 1-833-456-4566",
            "Kids Help Phone: 1-800-668-6868",
            "Trans Lifeline: 1-877-330-6366",
            "Assoc of Canadian Psychology Services: https://psychologyworks-ca.com"
        ]
    },
    "GB": {
        "country": "United Kingdom",
        "crisis_hotline": "Samaritans: 116 123",
        "crisis_number": "116 123",
        "crisis_text": "Email jo@samaritans.org",
        "therapist_directory": "https://www.bacp.co.uk",
        "resources": [
            "Samaritans: 116 123 (24/7, free)",
            "Mind: 0300 123 3393 (Mon-Fri 9am-6pm)",
            "Rethink Mental Illness: 0300 5000 927",
            "Crisis Text Line: Text HELLO to 50808"
        ]
    },
    "AU": {
        "country": "Australia",
        "crisis_hotline": "Lifeline: 13 11 14",
        "crisis_number": "13 11 14",
        "crisis_text": "Crisis Text Line: 0477 13 11 14",
        "therapist_directory": "https://www.psychologyaustralia.org.au",
        "resources": [
            "Lifeline: 13 11 14 (24/7, free)",
            "Beyond Blue: 1300 22 4636",
            "Black Dog Institute: https://www.blackdoginstitute.org.au",
            "Kids Helpline: 1800 55 1800"
        ]
    },
    "NZ": {
        "country": "New Zealand",
        "crisis_hotline": "1737 (call or text, free)",
        "crisis_number": "1737",
        "crisis_text": "Text 1737",
        "therapist_directory": "https://www.psychotherapycentre.co.nz",
        "resources": [
            "1737 (call or text): Free, confidential, 24/7",
            "Samaritans NZ: 0800 726 666",
            "Lifeline Aotearoa: 0800 543 354",
            "Depression Helpline: 0800 111 757"
        ]
    },
    "IE": {
        "country": "Ireland",
        "crisis_hotline": "Samaritans: 116 123",
        "crisis_number": "116 123",
        "crisis_text": "Text HELLO to 50808",
        "therapist_directory": "https://www.iacp.ie",
        "resources": [
            "Samaritans: 116 123",
            "Pieta House: 1800 247 247",
            "Console: 1800 247 100",
            "Mental Health Ireland: https://www.mentalhealthireland.ie"
        ]
    },
    "DE": {
        "country": "Germany",
        "crisis_hotline": "Telefonseelsorge: 0800 111 0 111 or 0800 111 0 222",
        "crisis_number": "0800 111 0 111",
        "therapist_directory": "https://www.bptk.de",
        "resources": [
            "Telefonseelsorge: 0800 111 0 111 (24/7, free)",
            "Telefonseelsorge: 0800 111 0 222",
            "BPtK Psychotherapist Finder: https://www.bptk.de",
            "Online Counseling: https://www.telefonseelsorge.de"
        ]
    },
    "FR": {
        "country": "France",
        "crisis_hotline": "3114 - National Suicide Prevention",
        "crisis_number": "3114",
        "crisis_text": "SOS Amitié: 09 72 39 40 50",
        "therapist_directory": "https://www.ordre.psychologues.fr",
        "resources": [
            "SOS Amitié: 09 72 39 40 50",
            "3114 - Numéro national de prévention du suicide",
            "SOS Médecins: 15 (emergency medical)",
            "Ordre des Psychologues: https://www.ordre.psychologues.fr"
        ]
    },
    "IN": {
        "country": "India",
        "crisis_hotline": "AASRA: 9820466726",
        "crisis_number": "9820466726",
        "crisis_text": "iCall: 9152987821",
        "therapist_directory": "https://www.indianpsychologicalassociation.org",
        "resources": [
            "AASRA: 9820466726",
            "iCall: 9152987821",
            "Vandrevala Foundation: 9999 666 555",
            "eCounselling India: https://ecounselling.org"
        ]
    },
    "SG": {
        "country": "Singapore",
        "crisis_hotline": "Suicide Prevention Centre: 1800 221 4444",
        "crisis_number": "1800 221 4444",
        "crisis_text": "Crisis Text Line available",
        "therapist_directory": "https://www.mhfa.org.sg",
        "resources": [
            "Suicide Prevention Centre: 1800 221 4444",
            "Institute of Mental Health: +65 6389 2200",
            "TOUCH Community Services: 1800 377 2252",
            "Therapy Today: https://www.therapytoday.sg"
        ]
    },
    "JP": {
        "country": "Japan",
        "crisis_hotline": "Inochi no Denwa: 0570-783-556",
        "crisis_number": "0570-783-556",
        "crisis_text": "Mental Health Support available",
        "therapist_directory": "https://www.jpa.or.jp",
        "resources": [
            "Inochi no Denwa: 0570-783-556",
            "TELL Lifeline: 03-5774-0992",
            "Yoshida Psychiatric Clinic Suicide Prevention: https://www.inochini.net",
            "Mental Health Counseling: https://www.mh-c.jp"
        ]
    },
    "DEFAULT": {
        "country": "Other",
        "crisis_hotline": "Contact local emergency services",
        "crisis_number": "Emergency: Contact local authorities (911, 999, or 112)",
        "crisis_text": "Text or call your local emergency number",
        "therapist_directory": "https://www.psychologytoday.com",
        "resources": [
            "International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres",
            "Befrienders worldwide: https://www.befrienders.org",
            "Psychology Today Therapist Directory: https://www.psychologytoday.com",
            "Contact your local mental health authority or hospital"
        ]
    }
}

class LocationService:
    def __init__(self):
        self.api_url = "https://ipapi.co/json/"
    
    @lru_cache(maxsize=100)
    def get_user_country(self, ip_address: str) -> Optional[str]:
        """Get country code from IP address"""
        try:
            # Free IP geolocation API
            response = requests.get(
                f"{self.api_url}",
                params={"ip": ip_address},
                timeout=2
            )
            response.raise_for_status()
            data = response.json()
            country_code = data.get("country_code", "").upper()
            logger.info(f"IP {ip_address} mapped to country: {country_code}")
            return country_code
        except Exception as e:
            logger.warning(f"Failed to geolocate IP {ip_address}: {e}")
            return None
    
    def get_resources_by_ip(self, ip_address: str) -> Dict:
        """Get professional help resources based on user's IP location"""
        try:
            country_code = self.get_user_country(ip_address)
            
            if not country_code:
                resources = PROFESSIONAL_RESOURCES["DEFAULT"]
            else:
                # Use country-specific resources if available
                resources = PROFESSIONAL_RESOURCES.get(country_code, PROFESSIONAL_RESOURCES["DEFAULT"])
            
            return {
                "country": resources["country"],
                "country_code": country_code or "UNKNOWN",
                "crisis_hotline": resources["crisis_hotline"],
                "crisis_number": resources["crisis_number"],
                "crisis_text": resources["crisis_text"],
                "therapist_directory": resources["therapist_directory"],
                "resources": resources["resources"],
                "success": True
            }
        except Exception as e:
            logger.error(f"Error getting resources for IP {ip_address}: {e}")
            # Return default resources on error
            resources = PROFESSIONAL_RESOURCES["DEFAULT"]
            return {
                "country": resources["country"],
                "country_code": "UNKNOWN",
                "crisis_hotline": resources["crisis_hotline"],
                "crisis_number": resources["crisis_number"],
                "crisis_text": resources["crisis_text"],
                "therapist_directory": resources["therapist_directory"],
                "resources": resources["resources"],
                "success": False,
                "error": str(e)
            }
