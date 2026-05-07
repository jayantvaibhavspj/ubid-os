from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class ActivityStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DORMANT = "DORMANT"
    CLOSED = "CLOSED"
    GHOST = "GHOST"

class DepartmentRecord(BaseModel):
    record_id: str = None
    department: str = None
    business_name: str
    address: Optional[str] = None
    pincode: Optional[str] = None
    pan: Optional[str] = None
    gstin: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    nic_code: Optional[str] = None
    
class MatchResult(BaseModel):
    record_1_id: str
    record_2_id: str
    confidence_score: float
    match_signals: Dict[str, float]
    recommendation: str  # "AUTO_LINK", "REVIEW", "SEPARATE"
    
class UBID(BaseModel):
    ubid: str
    linked_records: List[Dict]
    primary_name: str
    primary_address: Optional[str] = None
    primary_pan: Optional[str] = None
    primary_gstin: Optional[str] = None
    confidence_score: float
    created_at: datetime
    updated_at: datetime
    
class ActivityEvidence(BaseModel):
    timestamp: datetime
    source_system: str
    event_type: str
    evidence: str
    
class BusinessIntelligence(BaseModel):
    ubid: str
    business_name: str
    activity_status: ActivityStatus
    evidence_timeline: List[ActivityEvidence]
    last_license_renewal: Optional[datetime] = None
    electricity_consumption_6m: float
    labour_filings_12m: int
    last_inspection_date: Optional[datetime] = None
    ghost_business_score: float
    
class ReviewQueueItem(BaseModel):
    queue_id: str = None
    record_1: Dict = None
    record_2: Dict = None
    confidence_score: float = None
    match_signals: Dict[str, float] = None
    status: str = "PENDING"
    
class ReviewDecision(BaseModel):
    queue_id: str
    decision: str  # "CONFIRM", "REJECT", "SPLIT"
    rationale: str
    reviewer_id: str
