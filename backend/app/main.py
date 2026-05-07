from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from .models import *
from .database import db
from .entity_resolver import EntityResolver
from .activity_classifier import ActivityClassifier
from .ubid_registry import UBIDRegistry
from .synthetic_data import SyntheticDataGenerator

app = FastAPI(title="UBID-OS API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
resolver = EntityResolver()
classifier = ActivityClassifier()
registry = UBIDRegistry()
data_generator = SyntheticDataGenerator()

# Initialize flag
data_initialized = False

def initialize_data():
    """Initialize synthetic data on first request"""
    global data_initialized
    if not data_initialized:
        print("Initializing synthetic data...")
        
        # Generate synthetic dataset (smaller for faster startup)
        records = data_generator.generate_dataset(num_active=50, num_ghost=15, num_dormant=10)
        
        # Add to database
        for record in records:
            db.add_department_record(record)
        
        print(f"Generated {len(records)} department records")
        
        # Process entity resolution
        result = registry.process_entity_resolution(db.get_all_records())
        print(f"Created {result['total_ubids_created']} UBIDs")
        
        # Classify businesses
        for ubid_data in db.get_all_ubids():
            # Find corresponding activity data
            activity_data = next(
                (r for r in data_generator.business_base_data 
                 if r.get('business_name') == ubid_data.get('primary_name')),
                None
            )
            
            if activity_data:
                intelligence = classifier.classify_business(ubid_data, activity_data)
                db.add_activity_intelligence(ubid_data['ubid'], intelligence)
        
        print(f"Classified {len(db.activity_intelligence)} businesses")
        data_initialized = True

@app.on_event("startup")
async def startup_event():
    """Initialize data on startup"""
    initialize_data()

@app.get("/")
def read_root():
    return {
        "message": "UBID-OS API - Business Operating System for Karnataka",
        "version": "1.0.0",
        "endpoints": {
            "statistics": "/api/statistics",
            "ubids": "/api/ubids",
            "ghost_businesses": "/api/ghost-businesses",
            "resolve": "/api/resolve",
            "review_queue": "/api/review-queue"
        }
    }

@app.get("/api/statistics")
def get_statistics():
    """Get system statistics"""
    return db.get_statistics()

@app.get("/api/ubids")
def get_all_ubids():
    """Get all UBIDs"""
    return {
        "count": len(db.get_all_ubids()),
        "ubids": db.get_all_ubids()
    }

@app.get("/api/ubids/{ubid}")
def get_ubid(ubid: str):
    """Get specific UBID details"""
    ubid_data = db.get_ubid(ubid)
    if not ubid_data:
        raise HTTPException(status_code=404, detail="UBID not found")
    
    # Get activity intelligence
    intelligence = db.get_activity_intelligence(ubid)
    
    # Get event timeline
    events = db.get_events_for_ubid(ubid)
    
    return {
        **ubid_data,
        "activity_intelligence": intelligence,
        "event_timeline": events
    }

@app.get("/api/ghost-businesses")
def get_ghost_businesses():
    """Get all ghost businesses"""
    ghosts = db.get_ghost_businesses()
    return {
        "count": len(ghosts),
        "ghost_businesses": ghosts
    }

@app.get("/api/active-businesses")
def get_active_businesses():
    """Get all active businesses"""
    active = []
    for ubid, intel in db.activity_intelligence.items():
        if intel.get('activity_status') == 'ACTIVE':
            ubid_data = db.get_ubid(ubid)
            active.append({**ubid_data, **intel})
    
    return {
        "count": len(active),
        "active_businesses": active
    }

@app.get("/api/dormant-businesses")
def get_dormant_businesses():
    """Get all dormant businesses"""
    dormant = []
    for ubid, intel in db.activity_intelligence.items():
        if intel.get('activity_status') == 'DORMANT':
            ubid_data = db.get_ubid(ubid)
            dormant.append({**ubid_data, **intel})
    
    return {
        "count": len(dormant),
        "dormant_businesses": dormant
    }

@app.post("/api/resolve")
def resolve_entities(records: List[DepartmentRecord]):
    """Resolve entity matching for given records"""
    try:
        record_dicts = [r.dict() for r in records]
        matches = resolver.find_duplicates(record_dicts)
        
        return {
            "total_records": len(records),
            "matches_found": len(matches),
            "matches": matches
        }
    except Exception as e:
        print(f"Error in resolve_entities: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error resolving entities: {str(e)}")

@app.get("/api/review-queue")
def get_review_queue(status: str = "PENDING"):
    """Get review queue items"""
    queue = db.get_review_queue(status)
    return {
        "count": len(queue),
        "items": queue
    }

@app.post("/api/review-decision")
def submit_review_decision(decision: ReviewDecision):
    """Submit a review decision"""
    success = db.update_review_decision(
        decision.queue_id,
        decision.decision,
        decision.rationale
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Review item not found")
    
    return {"status": "success", "message": "Review decision recorded"}

@app.get("/api/query/ghost-by-pincode/{pincode}")
def query_ghost_by_pincode(pincode: str):
    """Query ghost businesses by pincode"""
    ghosts = db.get_ghost_businesses()
    filtered = [g for g in ghosts if g.get('primary_address', '').find(pincode) != -1]
    
    return {
        "pincode": pincode,
        "count": len(filtered),
        "ghost_businesses": filtered
    }

@app.get("/api/analytics/status-distribution")
def get_status_distribution():
    """Get distribution of business statuses"""
    distribution = {
        'ACTIVE': 0,
        'DORMANT': 0,
        'CLOSED': 0,
        'GHOST': 0
    }
    
    for intel in db.activity_intelligence.values():
        status = intel.get('activity_status')
        if status in distribution:
            distribution[status] += 1
    
    return distribution

@app.get("/api/analytics/department-coverage")
def get_department_coverage():
    """Get number of businesses per department"""
    coverage = {}
    
    for record in db.get_all_records():
        dept = record.get('department', 'Unknown')
        coverage[dept] = coverage.get(dept, 0) + 1
    
    return coverage

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
