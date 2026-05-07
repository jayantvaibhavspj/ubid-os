from typing import List, Dict, Tuple
from datetime import datetime
from .entity_resolver import EntityResolver
from .database import db

class UBIDRegistry:
    """
    UBID Registry manages the creation and management of Unified Business Identifiers
    """
    
    def __init__(self):
        self.resolver = EntityResolver()
    
    def create_ubid_from_records(self, records: List[Dict]) -> str:
        """
        Create a new UBID from a list of linked records
        """
        if not records:
            return None
        
        # Select primary data (prefer records with most complete information)
        primary_record = self.select_primary_record(records)
        
        # Calculate overall confidence (average of pairwise confidences)
        confidence = self.calculate_group_confidence(records)
        
        # Create UBID in registry
        ubid = db.create_ubid(
            linked_records=[{'record_id': r.get('id'), 'department': r.get('department')} for r in records],
            primary_data=primary_record,
            confidence=confidence
        )
        
        return ubid
    
    def select_primary_record(self, records: List[Dict]) -> Dict:
        """
        Select the most complete record as primary
        """
        def completeness_score(record):
            score = 0
            if record.get('business_name'): score += 1
            if record.get('address'): score += 1
            if record.get('pan'): score += 2
            if record.get('gstin'): score += 2
            if record.get('phone'): score += 1
            if record.get('email'): score += 1
            return score
        
        return max(records, key=completeness_score)
    
    def calculate_group_confidence(self, records: List[Dict]) -> float:
        """
        Calculate confidence score for a group of linked records
        """
        if len(records) <= 1:
            return 1.0
        
        confidences = []
        for i in range(len(records)):
            for j in range(i + 1, len(records)):
                confidence, _ = self.resolver.calculate_confidence(records[i], records[j])
                confidences.append(confidence)
        
        return sum(confidences) / len(confidences) if confidences else 1.0
    
    def process_entity_resolution(self, records: List[Dict]) -> Dict:
        """
        Process entity resolution for all records
        Returns statistics and results
        """
        # Find all potential matches
        matches = self.resolver.find_duplicates(records)
        
        auto_linked = []
        review_queue = []
        
        # Group records by confidence level
        linked_groups = []
        processed_ids = set()
        
        for match in matches:
            rec1_id = match['record_1_id']
            rec2_id = match['record_2_id']
            
            if match['recommendation'] == 'AUTO_LINK':
                # Find or create group
                group_found = False
                for group in linked_groups:
                    if rec1_id in [r['id'] for r in group] or rec2_id in [r['id'] for r in group]:
                        # Add to existing group
                        if rec1_id not in [r['id'] for r in group]:
                            rec1 = next(r for r in records if r['id'] == rec1_id)
                            group.append(rec1)
                        if rec2_id not in [r['id'] for r in group]:
                            rec2 = next(r for r in records if r['id'] == rec2_id)
                            group.append(rec2)
                        group_found = True
                        break
                
                if not group_found:
                    # Create new group
                    rec1 = next(r for r in records if r['id'] == rec1_id)
                    rec2 = next(r for r in records if r['id'] == rec2_id)
                    linked_groups.append([rec1, rec2])
                
                processed_ids.add(rec1_id)
                processed_ids.add(rec2_id)
                auto_linked.append(match)
                
            elif match['recommendation'] == 'REVIEW':
                # Add to review queue
                rec1 = next(r for r in records if r['id'] == rec1_id)
                rec2 = next(r for r in records if r['id'] == rec2_id)
                
                queue_item = {
                    'record_1': rec1,
                    'record_2': rec2,
                    'confidence_score': match['confidence_score'],
                    'match_signals': match['match_signals']
                }
                
                queue_id = db.add_to_review_queue(queue_item)
                review_queue.append({**queue_item, 'queue_id': queue_id})
        
        # Create UBIDs for linked groups
        created_ubids = []
        for group in linked_groups:
            ubid = self.create_ubid_from_records(group)
            created_ubids.append(ubid)
        
        # Create UBIDs for unlinked records (singleton UBIDs)
        for record in records:
            if record['id'] not in processed_ids:
                ubid = self.create_ubid_from_records([record])
                created_ubids.append(ubid)
        
        return {
            'total_records': len(records),
            'total_ubids_created': len(created_ubids),
            'auto_linked_pairs': len(auto_linked),
            'review_queue_items': len(review_queue),
            'ubids': created_ubids
        }
