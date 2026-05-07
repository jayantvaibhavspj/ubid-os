from datetime import datetime
from typing import List, Dict, Optional
import json

class InMemoryDatabase:
    """Simple in-memory database for demo purposes"""
    
    def __init__(self):
        self.department_records: List[Dict] = []
        self.ubid_registry: Dict[str, Dict] = {}
        self.activity_intelligence: Dict[str, Dict] = {}
        self.review_queue: List[Dict] = []
        self.event_store: List[Dict] = []
        self.ubid_counter = 1000
        
    def add_department_record(self, record: Dict) -> str:
        record['id'] = f"REC{len(self.department_records):06d}"
        self.department_records.append(record)
        return record['id']
    
    def get_all_records(self) -> List[Dict]:
        return self.department_records
    
    def create_ubid(self, linked_records: List[Dict], primary_data: Dict, confidence: float) -> str:
        ubid = f"UBID{self.ubid_counter:08d}"
        self.ubid_counter += 1
        
        self.ubid_registry[ubid] = {
            'ubid': ubid,
            'linked_records': linked_records,
            'primary_name': primary_data.get('business_name'),
            'primary_address': primary_data.get('address'),
            'primary_pan': primary_data.get('pan'),
            'primary_gstin': primary_data.get('gstin'),
            'confidence_score': confidence,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Add event
        self.add_event(ubid, "UBID_CREATED", f"Created with {len(linked_records)} linked records")
        
        return ubid
    
    def get_ubid(self, ubid: str) -> Optional[Dict]:
        return self.ubid_registry.get(ubid)
    
    def get_all_ubids(self) -> List[Dict]:
        return list(self.ubid_registry.values())
    
    def add_activity_intelligence(self, ubid: str, intelligence: Dict):
        self.activity_intelligence[ubid] = intelligence
        self.add_event(ubid, "ACTIVITY_CLASSIFIED", f"Status: {intelligence.get('activity_status')}")
    
    def get_activity_intelligence(self, ubid: str) -> Optional[Dict]:
        return self.activity_intelligence.get(ubid)
    
    def get_ghost_businesses(self) -> List[Dict]:
        ghosts = []
        for ubid, intel in self.activity_intelligence.items():
            if intel.get('activity_status') == 'GHOST':
                ubid_data = self.ubid_registry.get(ubid, {})
                ghosts.append({
                    **ubid_data,
                    **intel
                })
        return ghosts
    
    def add_to_review_queue(self, item: Dict) -> str:
        item['queue_id'] = f"REV{len(self.review_queue):06d}"
        item['status'] = 'PENDING'
        item['created_at'] = datetime.now().isoformat()
        self.review_queue.append(item)
        return item['queue_id']
    
    def get_review_queue(self, status: str = "PENDING") -> List[Dict]:
        return [item for item in self.review_queue if item['status'] == status]
    
    def update_review_decision(self, queue_id: str, decision: str, rationale: str):
        for item in self.review_queue:
            if item['queue_id'] == queue_id:
                item['status'] = decision
                item['rationale'] = rationale
                item['reviewed_at'] = datetime.now().isoformat()
                return True
        return False
    
    def add_event(self, ubid: str, event_type: str, evidence: str):
        event = {
            'ubid': ubid,
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'evidence': evidence
        }
        self.event_store.append(event)
    
    def get_events_for_ubid(self, ubid: str) -> List[Dict]:
        return [e for e in self.event_store if e['ubid'] == ubid]
    
    def get_statistics(self) -> Dict:
        total_records = len(self.department_records)
        total_ubids = len(self.ubid_registry)
        
        status_counts = {
            'ACTIVE': 0,
            'DORMANT': 0,
            'CLOSED': 0,
            'GHOST': 0
        }
        
        for intel in self.activity_intelligence.values():
            status = intel.get('activity_status')
            if status in status_counts:
                status_counts[status] += 1
        
        pending_reviews = len(self.get_review_queue("PENDING"))
        
        return {
            'total_records': total_records,
            'total_ubids': total_ubids,
            'ghost_businesses': status_counts['GHOST'],
            'active_businesses': status_counts['ACTIVE'],
            'dormant_businesses': status_counts['DORMANT'],
            'closed_businesses': status_counts['CLOSED'],
            'pending_reviews': pending_reviews,
            'resolution_rate': (total_ubids / total_records * 100) if total_records > 0 else 0
        }

# Global database instance
db = InMemoryDatabase()
