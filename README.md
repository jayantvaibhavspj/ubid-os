# UBID-OS: Unified Business Identifier Operating System for Karnataka

**From Identity to Intelligence • Every Karnataka business. One identity. A living digital heartbeat.**

## 🎯 Executive Summary

UBID-OS is an AI-driven Business Operating System designed to solve one of Karnataka's most critical regulatory challenges: **Detecting Ghost Businesses and Building a Unified Business Intelligence Layer**.

### The Problem
Karnataka's industrial regulatory landscape comprises 40+ department systems with isolated, unintegrated databases:
- **Shop Establishment Registry**
- **Labour Department** (PF/ESI filings)
- **Environmental Board (KSPCB)**
- **Power Authority (BESCOM)**

**Result**: Thousands of "ghost businesses" — entities with active licenses but zero operational activity across all systems — escape regulatory oversight, creating revenue loss and compliance gaps.

### The Solution
UBID-OS provides:
1. **Entity Resolution Engine**: Multi-signal Bayesian matching to identify the same business across 40+ department systems
2. **Unified Business Identifier (UBID)**: Single identity for every unique business entity
3. **Active Business Intelligence**: Real-time activity classification (Active/Dormant/Closed/Ghost)
4. **Ghost Business Detection**: Automated identification of inactive licenses with evidence timeline
5. **Human-in-the-Loop Review**: Confidence-based routing for automated vs manual decisions

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     UBID-OS Platform                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │
│  │  Department     │  │  Entity          │  │  Activity       │ │
│  │  Records        │→ │  Resolution      │→ │  Classification │ │
│  │  (40+ Systems)  │  │  Engine          │  │  Engine         │ │
│  └─────────────────┘  └──────────────────┘  └─────────────────┘ │
│                               ↓                                    │
│                    ┌──────────────────────┐                       │
│                    │  UBID Registry       │                       │
│                    │  (Unified Identity)  │                       │
│                    └──────────────────────┘                       │
│                               ↓                                    │
│              ┌────────────────────────────────┐                   │
│              │  Business Intelligence        │                   │
│              │  • Active/Dormant/Closed      │                   │
│              │  • Ghost Business Score       │                   │
│              │  • Evidence Timeline          │                   │
│              │  • Risk Assessment            │                   │
│              └────────────────────────────────┘                   │
│                               ↓                                    │
│              ┌────────────────────────────────┐                   │
│              │  Frontend Dashboard            │                   │
│              │  • Analytics & Visualization  │                   │
│              │  • Ghost Detection Results    │                   │
│              │  • Review Queue Management    │                   │
│              └────────────────────────────────┘                   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)

### Option 1: Docker (Recommended for Demo)

```bash
# Clone or download the project
cd ubid-os

# Start all services
docker-compose up

# Access the application
Frontend: http://localhost:3000
API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

---

## 📊 Features

### 1. **Entity Resolution Engine**
- **Jaro-Winkler** string matching for business names
- **Phonetic encoding** for transliteration handling
- **Token-based** address matching
- **PAN/GSTIN** anchoring for high-confidence linking
- **Multi-signal Bayesian** confidence scoring

**Confidence Thresholds:**
- **≥92%**: Auto-linked (high confidence)
- **72-92%**: Manual review queue (medium confidence)
- **<72%**: Separate records (low confidence)

### 2. **Ghost Business Detection**
Identifies businesses with:
- ✓ Active license status
- ✗ Zero electricity consumption (BESCOM)
- ✗ Zero labour filings (Labour Dept)
- ✗ No recent inspections (KSPCB/BWSSB)

**Evidence Timeline:**
Shows all activity signals chronologically with source system attribution

### 3. **Business Intelligence Classification**
Each UBID is classified as:
- **ACTIVE**: Operating across multiple signals
- **DORMANT**: Licensed but minimal activity
- **CLOSED**: License revoked or expired
- **GHOST**: Active license, zero operations (high risk)

### 4. **Dashboard & Analytics**
- Real-time statistics
- Status distribution (pie chart)
- Resolution rate metrics
- Department coverage analysis
- Pending review management

### 5. **Query Interface**
Pre-built query templates:
- All ghost businesses
- Active businesses by status
- Dormant businesses
- Ghost businesses by pincode
- CSV export capability

---

## 🔄 Entity Resolution Process

### Step 1: Input Normalization
```
Input: "WIPRO Ltd  Private  Co."
↓
Normalized: "wipro limited private company"
Phonetic: "AFRO"
```

### Step 2: Multi-Signal Comparison
```
Business Name Match:    95%  (weight: 35%)
Address Match:          78%  (weight: 25%)
PAN Match:             100%  (weight: 20%)
Contact Match:          50%  (weight: 10%)
NIC Code Match:         80%  (weight: 10%)
─────────────────────────────────
Confidence Score:      87.8%  → REVIEW QUEUE
```

### Step 3: Decision Routing
```
Confidence ≥ 92%  → AUTO_LINK (Create UBID)
Confidence 72-92% → HUMAN REVIEW (Review Queue)
Confidence < 72%  → SEPARATE (Keep separate)
```

### Step 4: UBID Creation
```
UBID: UBID00001234
├── Linked Records:
│   ├── REC000001 (Shop Establishment)
│   ├── REC000045 (Labour Department)
│   └── REC000089 (KSPCB)
├── Primary Data: WIPRO Private Limited, Bangalore
├── Confidence: 92.1%
└── Event Timeline:
    ├── License Renewed (Shop Est) - 30 days ago
    ├── PF Filing (Labour) - 60 days ago
    └── Inspection (KSPCB) - 90 days ago
```

---

## 👻 Ghost Business Detection Example

```
Business: "XYZ Manufacturing Solutions Pvt Ltd"
UBID: UBID00005678

Evidence Collected:
─────────────────────────────────────────────
Shop Establishment: License Active (60 days ago)
BESCOM: 0 kWh in 6 months          ← CRITICAL
Labour Dept: 0 filings in 12 months ← CRITICAL
KSPCB: No inspection in 24 months   ← CRITICAL
─────────────────────────────────────────────

Classification: GHOST BUSINESS
Ghost Score: 85%
Risk Level: HIGH
Action: Flag for regulatory review
```

---

## 📁 Project Structure

```
ubid-os/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app
│   │   ├── models.py               # Pydantic models
│   │   ├── database.py             # In-memory DB
│   │   ├── entity_resolver.py      # Matching engine
│   │   ├── activity_classifier.py  # Classification logic
│   │   ├── ubid_registry.py        # UBID management
│   │   └── synthetic_data.py       # Test data generator
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 # Main app
│   │   ├── index.jsx               # Entry point
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── GhostBusinesses.jsx
│   │   │   ├── EntityResolver.jsx
│   │   │   └── QueryInterface.jsx
│   │   └── styles/
│   │       └── index.css
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   ├── Dockerfile
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── docker-compose.yml
├── README.md                        # This file
└── SETUP_GUIDE.md                   # Detailed setup instructions
```

---

## 🔌 API Endpoints

### Statistics & Analytics
- `GET /api/statistics` - System overview
- `GET /api/analytics/status-distribution` - Business status counts
- `GET /api/analytics/department-coverage` - Records per department

### UBID Management
- `GET /api/ubids` - All UBIDs
- `GET /api/ubids/{ubid}` - Specific UBID details
- `GET /api/ghost-businesses` - All ghost businesses
- `GET /api/active-businesses` - All active businesses
- `GET /api/dormant-businesses` - All dormant businesses

### Entity Resolution
- `POST /api/resolve` - Resolve entities (returns matches)

### Review Management
- `GET /api/review-queue` - Pending reviews
- `POST /api/review-decision` - Submit review decision

### Queries
- `GET /api/query/ghost-by-pincode/{pincode}` - Query ghosts by location

---

## 💡 Demo Scenarios

### Scenario 1: Duplicate Detection
1. Enter two similar business records with slight name/address variations
2. System calculates 87% match confidence
3. Routes to manual review queue
4. Reviewer can confirm and create single UBID

### Scenario 2: Ghost Business Discovery
1. System processes 280 business records from 4 departments
2. Identifies 50 ghost businesses
3. Dashboard shows statistics + evidence timeline
4. Regulatory team gets actionable list for compliance action

### Scenario 3: Department Coverage Analysis
1. Query shows which departments have data on a specific business
2. Identifies data gaps
3. Helps prioritize system integration work

---

## 🎓 Technology Stack

**Backend:**
- FastAPI (Python web framework)
- Jellyfish (string similarity)
- FuzzyWuzzy (fuzzy matching)
- Metaphone (phonetic encoding)
- Pandas (data processing)
- Faker (test data generation)

**Frontend:**
- React 18
- Tailwind CSS
- Recharts (data visualization)
- Axios (API client)
- Lucide React (icons)

**Infrastructure:**
- Docker & Docker Compose
- Python 3.11
- Node.js 18

---

## 📊 Data Model

### DepartmentRecord
```python
{
    "id": "REC000001",
    "department": "Shop_Establishment",
    "business_name": "WIPRO Private Limited",
    "address": "Bangalore, Karnataka",
    "pan": "AAACR5055K",
    "gstin": "29AABCR5055K1Z0",
    "phone": "8080808080",
    "email": "contact@wipro.com",
    "nic_code": "62011"
}
```

### UBID
```python
{
    "ubid": "UBID00001234",
    "linked_records": [
        {"record_id": "REC000001", "department": "Shop_Establishment"},
        {"record_id": "REC000045", "department": "Labour_Department"}
    ],
    "primary_name": "WIPRO Private Limited",
    "primary_address": "Bangalore, Karnataka",
    "confidence_score": 0.921,
    "created_at": "2026-05-07T10:30:00"
}
```

### ActivityIntelligence
```python
{
    "ubid": "UBID00001234",
    "business_name": "WIPRO Private Limited",
    "activity_status": "ACTIVE",
    "ghost_business_score": 0.15,
    "electricity_consumption_6m": 45000.0,
    "labour_filings_12m": 8,
    "evidence_timeline": [
        {
            "timestamp": "2026-05-01T00:00:00",
            "source_system": "BESCOM",
            "event_type": "Electricity Consumption",
            "evidence": "Units consumed: 45000 kWh"
        }
    ]
}
```

---

## 🔐 Security Considerations

- Implement JWT authentication for API endpoints
- Rate limiting on resolution endpoints
- Audit logging for all review decisions
- Encrypt PAN/GSTIN in transit and at rest
- Role-based access control (Admin/Reviewer/Analyst)

---

## 📈 Performance Notes

- Synthetic dataset: ~900 business records generated
- Entity resolution: ~10K pairwise comparisons
- Auto-linked pairs: ~100 (confidence ≥ 92%)
- Review queue items: ~50 (72-92% confidence)
- Execution time: <5 seconds for full resolution

---

## 🚧 Future Enhancements

1. **Machine Learning**: Train custom matching models on historical review decisions
2. **Graph Database**: Store relationship networks (owners, addresses, etc.)
3. **Real-time Integration**: Direct APIs with department systems
4. **Mobile App**: On-field compliance verification
5. **Advanced Analytics**: Sector-wise ghost business patterns
6. **Explainability**: LIME/SHAP for interpretable matching decisions
7. **Workflow Automation**: Trigger regulatory notices programmatically

---

## 📞 Support

For questions or issues:
1. Check this README
2. Review API documentation at http://localhost:8000/docs
3. Check application logs in Docker containers

---

## 🏆 Hackathon Submission

**Theme**: Theme 1: Unified Business Identifier (UBID) and Active Business Intelligence

**PAN IIT Bangalore Hackathon 2026**
**Karnataka Commerce & Industry**

---

## 📝 License

This project is submitted for the AI for Bharat hackathon.

---

**UBID-OS: From Identity to Intelligence**
*Every Karnataka business. One identity. A living digital heartbeat.*
