from datetime import datetime, timedelta
from typing import Dict, List
from enum import Enum

class ActivityStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DORMANT = "DORMANT"
    CLOSED = "CLOSED"
    GHOST = "GHOST"

class ActivityClassifier:
    """
    Classifies business activity status including Ghost Business detection
    """
    
    # Thresholds for classification
    GHOST_ELECTRICITY_THRESHOLD = 10  # kWh per 6 months
    GHOST_LABOUR_THRESHOLD = 0  # No filings in 12 months
    GHOST_INSPECTION_MONTHS = 18
    
    DORMANT_ELECTRICITY_THRESHOLD = 50  # kWh per 6 months
    DORMANT_MONTHS = 6
    
    CLOSED_MONTHS = 18
    
    def __init__(self):
        pass
    
    def build_evidence_timeline(self, ubid_data: Dict, activity_data: Dict) -> List[Dict]:
        """
        Build evidence timeline from various data sources
        """
        timeline = []
        current_time = datetime.now()
        
        # License renewal event
        if activity_data.get('last_license_renewal'):
            timeline.append({
                'timestamp': activity_data['last_license_renewal'],
                'source_system': 'Shop Establishment',
                'event_type': 'License Renewal',
                'evidence': 'Annual license renewed. Status: Current.'
            })
        
        # Electricity consumption
        elec_consumption = activity_data.get('electricity_consumption_6m', 0)
        timeline.append({
            'timestamp': (current_time - timedelta(days=30)).isoformat(),
            'source_system': 'BESCOM',
            'event_type': 'Electricity Consumption',
            'evidence': f'Units consumed (6 months): {elec_consumption} kWh'
        })
        
        # Labour filings
        labour_filings = activity_data.get('labour_filings_12m', 0)
        if labour_filings > 0:
            timeline.append({
                'timestamp': (current_time - timedelta(days=60)).isoformat(),
                'source_system': 'Labour Department',
                'event_type': 'PF Filing',
                'evidence': f'{labour_filings} filings in last 12 months'
            })
        else:
            timeline.append({
                'timestamp': (current_time - timedelta(days=365)).isoformat(),
                'source_system': 'Labour Department',
                'event_type': 'PF Filing',
                'evidence': 'No filings in last 12 months'
            })
        
        # Inspection
        last_inspection = activity_data.get('last_inspection_date')
        if last_inspection:
            timeline.append({
                'timestamp': last_inspection,
                'source_system': 'KSPCB',
                'event_type': 'Inspection',
                'evidence': 'Environmental compliance inspection completed'
            })
        else:
            months_since = activity_data.get('months_since_inspection', 24)
            timeline.append({
                'timestamp': (current_time - timedelta(days=months_since * 30)).isoformat(),
                'source_system': 'KSPCB',
                'event_type': 'Inspection Due',
                'evidence': f'No inspection in {months_since} months'
            })
        
        # Sort by timestamp
        timeline.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return timeline
    
    def calculate_ghost_score(self, activity_data: Dict) -> float:
        """
        Calculate Ghost Business probability score (0-1)
        Higher score = more likely to be ghost
        """
        score = 0.0
        
        # Check license status
        has_active_license = activity_data.get('license_active', False)
        last_renewal = activity_data.get('last_license_renewal')
        
        if has_active_license and last_renewal:
            score += 0.3  # Has active license
        
        # Check electricity consumption
        elec_consumption = activity_data.get('electricity_consumption_6m', 0)
        if elec_consumption <= self.GHOST_ELECTRICITY_THRESHOLD:
            score += 0.3  # Zero/minimal electricity
        
        # Check labour filings
        labour_filings = activity_data.get('labour_filings_12m', 0)
        if labour_filings <= self.GHOST_LABOUR_THRESHOLD:
            score += 0.2  # No labour activity
        
        # Check inspections
        months_since_inspection = activity_data.get('months_since_inspection', 0)
        if months_since_inspection >= self.GHOST_INSPECTION_MONTHS:
            score += 0.2  # No recent inspection
        
        return min(score, 1.0)
    
    def classify_business(self, ubid_data: Dict, activity_data: Dict) -> Dict:
        """
        Classify business into Active/Dormant/Closed/Ghost
        Returns classification with evidence
        """
        
        # Extract key signals
        has_active_license = activity_data.get('license_active', False)
        last_renewal = activity_data.get('last_license_renewal')
        elec_consumption = activity_data.get('electricity_consumption_6m', 0)
        labour_filings = activity_data.get('labour_filings_12m', 0)
        months_since_inspection = activity_data.get('months_since_inspection', 0)
        
        # Calculate ghost score
        ghost_score = self.calculate_ghost_score(activity_data)
        
        # Build evidence timeline
        evidence_timeline = self.build_evidence_timeline(ubid_data, activity_data)
        
        # Classification logic
        status = ActivityStatus.ACTIVE
        
        # Check for CLOSED first
        if not has_active_license:
            status = ActivityStatus.CLOSED
        
        # Check for GHOST (critical condition)
        elif (has_active_license and 
              elec_consumption <= self.GHOST_ELECTRICITY_THRESHOLD and
              labour_filings <= self.GHOST_LABOUR_THRESHOLD and
              months_since_inspection >= self.GHOST_INSPECTION_MONTHS):
            status = ActivityStatus.GHOST
        
        # Check for DORMANT
        elif (has_active_license and
              elec_consumption <= self.DORMANT_ELECTRICITY_THRESHOLD and
              labour_filings == 0):
            status = ActivityStatus.DORMANT
        
        # Otherwise ACTIVE
        else:
            status = ActivityStatus.ACTIVE
        
        return {
            'ubid': ubid_data.get('ubid'),
            'business_name': ubid_data.get('primary_name'),
            'activity_status': status.value,
            'evidence_timeline': evidence_timeline,
            'last_license_renewal': last_renewal,
            'electricity_consumption_6m': elec_consumption,
            'labour_filings_12m': labour_filings,
            'last_inspection_date': activity_data.get('last_inspection_date'),
            'months_since_inspection': months_since_inspection,
            'ghost_business_score': ghost_score
        }
