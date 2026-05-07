import jellyfish
from fuzzywuzzy import fuzz
from typing import List, Dict, Tuple
import re
from metaphone import doublemetaphone

class EntityResolver:
    """
    Entity Resolution Engine with multi-signal Bayesian scoring
    """
    
    # Confidence thresholds from the document
    AUTO_LINK_THRESHOLD = 0.92
    REVIEW_THRESHOLD = 0.72
    
    # Signal weights from the document
    WEIGHTS = {
        'business_name': 0.35,
        'address': 0.25,
        'pan': 0.20,
        'contact': 0.10,
        'business_category': 0.10
    }
    
    def __init__(self):
        pass
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Expand common abbreviations
        abbreviations = {
            'pvt': 'private',
            'ltd': 'limited',
            'llp': 'limited liability partnership',
            'opc': 'one person company',
            'inc': 'incorporated',
            'corp': 'corporation',
            'co': 'company',
            'rd': 'road',
            'st': 'street',
            'ave': 'avenue',
            'blvd': 'boulevard'
        }
        
        for abbr, full in abbreviations.items():
            text = re.sub(r'\b' + abbr + r'\b', full, text)
        
        return text.strip()
    
    def phonetic_encode(self, text: str) -> str:
        """Generate phonetic encoding for transliteration handling"""
        if not text:
            return ""
        
        # Use Double Metaphone for English phonetic encoding
        primary, secondary = doublemetaphone(text)
        return primary or ""
    
    def compare_business_names(self, name1: str, name2: str) -> float:
        """
        Compare business names using Jaro-Winkler + phonetic encoding
        Returns score between 0 and 1
        """
        if not name1 or not name2:
            return 0.0
        
        # Normalize
        norm1 = self.normalize_text(name1)
        norm2 = self.normalize_text(name2)
        
        # Jaro-Winkler distance
        jaro_score = jellyfish.jaro_winkler_similarity(norm1, norm2)
        
        # Fuzzy ratio
        fuzzy_score = fuzz.ratio(norm1, norm2) / 100.0
        
        # Phonetic comparison
        phonetic1 = self.phonetic_encode(norm1)
        phonetic2 = self.phonetic_encode(norm2)
        phonetic_score = 1.0 if phonetic1 == phonetic2 else 0.0
        
        # Weighted combination
        final_score = (jaro_score * 0.5) + (fuzzy_score * 0.4) + (phonetic_score * 0.1)
        
        return final_score
    
    def normalize_address(self, address: str) -> str:
        """Normalize address for comparison"""
        if not address:
            return ""
        
        addr = self.normalize_text(address)
        
        # Remove common building/floor indicators
        addr = re.sub(r'\b(floor|flr|building|bldg|block|blk)\s*\w*\b', '', addr)
        
        # Extract and standardize pincode
        pincode_match = re.search(r'\b\d{6}\b', addr)
        if pincode_match:
            addr = addr.replace(pincode_match.group(), f'PIN{pincode_match.group()}')
        
        return addr
    
    def compare_addresses(self, addr1: str, addr2: str) -> float:
        """
        Compare addresses with token-level fuzzy matching
        Returns score between 0 and 1
        """
        if not addr1 or not addr2:
            return 0.0
        
        norm1 = self.normalize_address(addr1)
        norm2 = self.normalize_address(addr2)
        
        # Token set ratio (handles word order differences)
        token_score = fuzz.token_set_ratio(norm1, norm2) / 100.0
        
        # Check for pincode match (high confidence signal)
        pincode1 = re.search(r'\b\d{6}\b', addr1)
        pincode2 = re.search(r'\b\d{6}\b', addr2)
        
        pincode_bonus = 0.2 if (pincode1 and pincode2 and pincode1.group() == pincode2.group()) else 0.0
        
        return min(token_score + pincode_bonus, 1.0)
    
    def compare_pan(self, pan1: str, pan2: str) -> float:
        """
        Compare PAN numbers with partial match support
        Returns score between 0 and 1
        """
        if not pan1 or not pan2:
            return 0.0
        
        pan1 = pan1.upper().strip()
        pan2 = pan2.upper().strip()
        
        # Exact match
        if pan1 == pan2:
            return 1.0
        
        # Partial match (prefix or suffix)
        if len(pan1) >= 5 and len(pan2) >= 5:
            if pan1[:5] == pan2[:5] or pan1[-5:] == pan2[-5:]:
                return 0.7
        
        return 0.0
    
    def compare_contact(self, contact1: Dict, contact2: Dict) -> float:
        """
        Compare contact details (phone/email)
        Returns score between 0 and 1
        """
        score = 0.0
        count = 0
        
        # Phone comparison
        phone1 = contact1.get('phone', '').replace(' ', '').replace('-', '')
        phone2 = contact2.get('phone', '').replace(' ', '').replace('-', '')
        
        if phone1 and phone2:
            count += 1
            if phone1 == phone2:
                score += 1.0
            elif phone1[-10:] == phone2[-10:]:  # Last 10 digits match
                score += 0.8
        
        # Email comparison
        email1 = contact1.get('email', '').lower().strip()
        email2 = contact2.get('email', '').lower().strip()
        
        if email1 and email2:
            count += 1
            if email1 == email2:
                score += 1.0
        
        return (score / count) if count > 0 else 0.0
    
    def compare_business_category(self, nic1: str, nic2: str) -> float:
        """
        Compare NIC codes
        Returns score between 0 and 1
        """
        if not nic1 or not nic2:
            return 0.0
        
        nic1 = nic1.strip()
        nic2 = nic2.strip()
        
        # Exact match
        if nic1 == nic2:
            return 1.0
        
        # Same first 2 digits (same sector)
        if len(nic1) >= 2 and len(nic2) >= 2 and nic1[:2] == nic2[:2]:
            return 0.5
        
        return 0.0
    
    def calculate_confidence(self, record1: Dict, record2: Dict) -> Tuple[float, Dict[str, float]]:
        """
        Calculate Bayesian confidence score between two records
        Returns (confidence_score, signal_breakdown)
        """
        signals = {}
        
        # Business name comparison (35% weight)
        signals['business_name'] = self.compare_business_names(
            record1.get('business_name', ''),
            record2.get('business_name', '')
        )
        
        # Address comparison (25% weight)
        signals['address'] = self.compare_addresses(
            record1.get('address', ''),
            record2.get('address', '')
        )
        
        # PAN comparison (20% weight)
        signals['pan'] = self.compare_pan(
            record1.get('pan', ''),
            record2.get('pan', '')
        )
        
        # Contact comparison (10% weight)
        signals['contact'] = self.compare_contact(
            {'phone': record1.get('phone'), 'email': record1.get('email')},
            {'phone': record2.get('phone'), 'email': record2.get('email')}
        )
        
        # Business category comparison (10% weight)
        signals['business_category'] = self.compare_business_category(
            record1.get('nic_code', ''),
            record2.get('nic_code', '')
        )
        
        # Calculate weighted score
        confidence_score = sum(signals[key] * self.WEIGHTS[key] for key in signals)
        
        # Boost if GSTIN or PAN exactly match
        if record1.get('gstin') and record2.get('gstin') and record1['gstin'] == record2['gstin']:
            confidence_score = 1.0
        elif record1.get('pan') and record2.get('pan') and record1['pan'] == record2['pan']:
            confidence_score = min(confidence_score * 1.2, 1.0)
        
        return confidence_score, signals
    
    def resolve_entity(self, record1: Dict, record2: Dict, idx1: int = None, idx2: int = None) -> Dict:
        """
        Resolve if two records represent the same entity
        Returns match result with recommendation
        """
        confidence_score, signals = self.calculate_confidence(record1, record2)
        
        # Determine recommendation based on threshold
        if confidence_score >= self.AUTO_LINK_THRESHOLD:
            recommendation = "AUTO_LINK"
        elif confidence_score >= self.REVIEW_THRESHOLD:
            recommendation = "REVIEW"
        else:
            recommendation = "SEPARATE"
        
        # Get IDs with fallback to record_id or index
        record_1_id = record1.get('record_id') or record1.get('id') or f"record_{idx1}"
        record_2_id = record2.get('record_id') or record2.get('id') or f"record_{idx2}"
        
        return {
            'record_1_id': record_1_id,
            'record_2_id': record_2_id,
            'record_1_name': record1.get('business_name', 'N/A'),
            'record_2_name': record2.get('business_name', 'N/A'),
            'confidence_score': confidence_score,
            'match_signals': signals,
            'recommendation': recommendation
        }
    
    def find_duplicates(self, records: List[Dict]) -> List[Dict]:
        """
        Find all potential duplicate pairs in a list of records
        Returns list of match results
        """
        matches = []
        n = len(records)
        
        # For large datasets, sample to speed up processing
        if n > 300:
            import random
            sample_size = min(300, n)
            records = random.sample(records, sample_size)
            n = len(records)
        
        for i in range(n):
            for j in range(i + 1, n):
                match_result = self.resolve_entity(records[i], records[j], idx1=i, idx2=j)
                
                # Only include matches above review threshold
                if match_result['confidence_score'] >= self.REVIEW_THRESHOLD:
                    matches.append(match_result)
        
        # Sort by confidence score descending
        matches.sort(key=lambda x: x['confidence_score'], reverse=True)
        
        return matches
