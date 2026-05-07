from faker import Faker
import random
from datetime import datetime, timedelta
from typing import List, Dict

fake = Faker('en_IN')

class SyntheticDataGenerator:
    """
    Generates synthetic business data with intentional duplicates and ghost businesses
    """
    
    DEPARTMENTS = [
        'Shop_Establishment',
        'Labour_Department',
        'KSPCB',
        'BESCOM'
    ]
    
    NIC_CODES = [
        '46101', '46102', '47111', '47191', '56101',
        '62011', '68201', '71201', '85101', '93110'
    ]
    
    def __init__(self):
        self.business_base_data = []
        self.generated_records = []
    
    def generate_pan(self) -> str:
        """Generate realistic PAN number"""
        letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5))
        numbers = ''.join(random.choices('0123456789', k=4))
        return f"{letters[:3]}{random.choice('ABCFGHLJPT')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{numbers}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
    
    def generate_gstin(self, pan: str) -> str:
        """Generate GSTIN from PAN"""
        state_code = str(random.randint(10, 36))
        entity_code = ''.join(random.choices('0123456789', k=3))
        check_digit = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        return f"{state_code}{pan}{entity_code}Z{check_digit}"
    
    def generate_base_business(self) -> Dict:
        """Generate a base business entity"""
        company_name = fake.company()
        pan = self.generate_pan()
        gstin = self.generate_gstin(pan)
        
        return {
            'business_name': company_name,
            'address': fake.address().replace('\n', ', '),
            'pincode': fake.postcode(),
            'pan': pan,
            'gstin': gstin,
            'phone': fake.phone_number(),
            'email': fake.company_email(),
            'nic_code': random.choice(self.NIC_CODES)
        }
    
    def create_variant(self, base: Dict, department: str) -> Dict:
        """Create a variant of base business with slight differences"""
        record = base.copy()
        record['department'] = department
        
        # Introduce variations
        if random.random() < 0.3:
            # Name variation
            variations = [
                lambda n: n.replace('Private Limited', 'Pvt Ltd'),
                lambda n: n.replace('Limited', 'Ltd'),
                lambda n: n.upper(),
                lambda n: n.lower(),
                lambda n: n + ' India'
            ]
            record['business_name'] = random.choice(variations)(record['business_name'])
        
        if random.random() < 0.2:
            # Missing PAN in some departments
            record['pan'] = None
        
        if random.random() < 0.3:
            # Missing GSTIN in some departments
            record['gstin'] = None
        
        if random.random() < 0.2:
            # Address variation
            record['address'] = record['address'].replace('Street', 'St').replace('Road', 'Rd')
        
        return record
    
    def generate_ghost_business(self) -> Dict:
        """Generate a ghost business with activity data"""
        base = self.generate_base_business()
        
        # Ghost characteristics
        return {
            **base,
            'license_active': True,
            'last_license_renewal': (datetime.now() - timedelta(days=random.randint(30, 180))).isoformat(),
            'electricity_consumption_6m': random.uniform(0, 5),  # Very low
            'labour_filings_12m': 0,  # No filings
            'last_inspection_date': None,
            'months_since_inspection': random.randint(18, 36),  # Long gap
            'is_ghost': True
        }
    
    def generate_active_business(self) -> Dict:
        """Generate an active business with normal activity"""
        base = self.generate_base_business()
        
        return {
            **base,
            'license_active': True,
            'last_license_renewal': (datetime.now() - timedelta(days=random.randint(30, 180))).isoformat(),
            'electricity_consumption_6m': random.uniform(1000, 50000),
            'labour_filings_12m': random.randint(4, 12),
            'last_inspection_date': (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat(),
            'months_since_inspection': random.randint(1, 12),
            'is_ghost': False
        }
    
    def generate_dormant_business(self) -> Dict:
        """Generate a dormant business"""
        base = self.generate_base_business()
        
        return {
            **base,
            'license_active': True,
            'last_license_renewal': (datetime.now() - timedelta(days=random.randint(180, 365))).isoformat(),
            'electricity_consumption_6m': random.uniform(10, 100),
            'labour_filings_12m': 0,
            'last_inspection_date': (datetime.now() - timedelta(days=random.randint(365, 730))).isoformat(),
            'months_since_inspection': random.randint(12, 24),
            'is_ghost': False
        }
    
    def generate_dataset(self, num_active: int = 200, num_ghost: int = 50, num_dormant: int = 30) -> List[Dict]:
        """
        Generate complete synthetic dataset
        """
        self.business_base_data = []
        self.generated_records = []
        
        # Generate active businesses
        for _ in range(num_active):
            business = self.generate_active_business()
            self.business_base_data.append(business)
        
        # Generate ghost businesses
        for _ in range(num_ghost):
            business = self.generate_ghost_business()
            self.business_base_data.append(business)
        
        # Generate dormant businesses
        for _ in range(num_dormant):
            business = self.generate_dormant_business()
            self.business_base_data.append(business)
        
        # Create department records with variations
        for business in self.business_base_data:
            num_departments = random.randint(2, 4)
            departments = random.sample(self.DEPARTMENTS, num_departments)
            
            for dept in departments:
                record = self.create_variant(business, dept)
                self.generated_records.append(record)
        
        return self.generated_records
