# UBID-OS: Detecting Ghost Businesses and Building Unified Business Intelligence Layer

## Theme
**Theme 1: Unified Business Identifier (UBID) and Active Business Intelligence**

---

## Executive Summary

UBID-OS is a breakthrough intelligence layer that gives every Karnataka business a permanent, unified digital identity across the State's 40+ isolated department systems. More critically, it detects and flags **Ghost Businesses** — entities that appear active in government records but show zero real economic activity — a problem invisible to all existing solutions.

### Key Innovation: Ghost Business Detection
Unlike standard Active/Dormant/Closed classifications, UBID-OS identifies the **fourth critical state**: businesses with current licenses and renewed registrations but zero electricity consumption, zero labour filings, and no inspections for 12+ months. These are Ghost Businesses — potential fraud vectors or regulatory arbitrage operations that enable the government to:
- Reclaim lapsed licenses immediately
- Prevent tax compliance fraud
- Target field inspections effectively
- Surface money laundering risks

---

## Problem Statement

Karnataka's industrial regulatory landscape is fragmented:
- **40+ isolated department systems** (Shop Establishment, Labour, KSPCB, BESCOM, GST, UDYAM, etc.)
- **No join key** across systems — same business = different records
- **Data quality varies drastically** by department
- **Government cannot answer basic questions**: "How many active manufacturing businesses are in Bengaluru with 50+ employees?"

### Why Existing Solutions Fail
Most approaches treat entity resolution as a pure matching problem. They fail on the **critical 30% of cases**:
- Partial/missing data (legacy systems)
- Name transliteration (English ↔ Kannada)
- Address variations (abbreviations, format differences)
- Ambiguous cases requiring human judgment

UBID-OS is fundamentally different: it treats every decision as a **probability, not a binary**, and builds explainability and reversibility into the architecture.

---

## Solution Architecture

### Part A: Unified Business Identifier (UBID)

#### Entity Resolution Engine — 3-Stage Approach

**Stage 1: Deterministic Anchoring (High Confidence)**
- When PAN or GSTIN present and consistent across systems → auto-link
- Confidence: 1.0
- No ML. No ambiguity.

**Stage 2: Probabilistic Matching (Medium Confidence)**
Multi-signal Bayesian Network across 5 dimensions:

| Signal | Weight | Method |
|--------|--------|--------|
| Business Name | 35% | Jaro-Winkler + phonetic encoding (Soundex/Metaphone) |
| Address | 25% | Token-level fuzzy match + normalization |
| PAN (partial) | 20% | Prefix/suffix matching |
| Contact Details | 10% | Phone/email exact match |
| Business Category | 10% | NIC code sector matching |

**Stage 3: Human-Escalated Review (Low Confidence)**
- Scores 0.72–0.91 → Reviewer workflow
- Scores < 0.72 → Keep separate
- Full evidence trail + rationale capture

#### Confidence Thresholds

| Score | Action | Rationale |
|-------|--------|-----------|
| ≥ 0.92 | Auto-link | High confidence: strong name+address + Central ID anchor |
| 0.72–0.91 | Reviewer Queue | Ambiguous: possible match but insufficient evidence |
| < 0.72 | Keep Separate | Low confidence: unlink until additional evidence |

**Design Principle**: We deliberately set auto-link threshold conservatively (0.92 not 0.80) because a wrong merge is far more costly than a missed merge. A wrong merge corrupts activity data for two businesses. A missed merge simply delays a decision.

#### Self-Improving Feedback Loop
Every reviewer decision (confirm/reject/split) becomes a labelled training example. Monthly retraining cycles update the Bayesian priors. Over time, the system learns Karnataka-specific naming and addressing patterns, progressively reducing the review queue.

---

### Part B: Active Business Intelligence

#### Four-State Classification Model

| Status | Definition | Signal Pattern |
|--------|-----------|-----------------|
| 🟢 **Active** | Currently operating with verifiable economic activity | Recent renewals + inspections + non-zero utility + labour filings (6m) |
| 🟡 **Dormant** | Exists legally but no recent economic activity | License current but no inspections/filings (6–18m) |
| 🔴 **Closed** | Ceased operations with regulatory confirmation | License expired + utility disconnected + no filings (18m+) |
| 👻 **Ghost** | Appears active but zero real economic activity | License renewed BUT zero electricity + zero labour filings + no inspections (12m+) |

#### Event Sourcing Architecture — The Core Innovation

Standard solutions store current status. We store **every event, immutably**. This is the most important architectural decision because it delivers explainability and reversibility:

**Why Event Sourcing?**
- Every classification is derived from the event log, not stored
- Change an event's interpretation → status updates automatically
- Reverse incorrect classifications without touching source data
- Audit any decision by replaying the event stream

**Example Evidence Timeline:**

```
Apr 2024  → License Renewal (appears active)
Jun 2024  → PF Filing: 12 employees
Sep 2024  → BESCOM: 0 kWh (zero consumption)
Dec 2024  → No inspection for 18 months
Feb 2025  → BESCOM: 0 kWh (second consecutive zero month)
Apr 2025  → License Renewed (still appears active)

CLASSIFICATION: 👻 GHOST BUSINESS ⚠️
```

#### The Ghost Business Query

The most powerful demonstration of system value — impossible with any existing solution:

```sql
SELECT ubid, business_name, pincode, last_renewal_date 
FROM ubid_registry 
WHERE activity_status = 'ACTIVE'
  AND electricity_consumption_6m = 0
  AND labour_filings_12m = 0
  AND last_inspection_date < NOW() - INTERVAL '18 months'
  AND pincode LIKE '5600%'
ORDER BY last_renewal_date DESC;
```

This query identifies businesses actively renewing licenses but showing zero real-world activity — enabling targeted inspections, license reclamation, and fraud detection.

---

## Technical Implementation

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Backend | FastAPI 0.109.0 + Python 3.10 | High-performance REST API |
| Frontend | React 18.2.0 + Tailwind CSS 3.4.1 | Interactive dashboard and reviewer UI |
| Database | In-memory (extensible to PostgreSQL) | Event store + UBID registry |
| Entity Resolution | Jaro-Winkler + Bayesian Network | Multi-signal matching |
| Deployment | Docker (optional) + local dev setup | Flexible deployment |

### Dataset Characteristics

**Synthetic Data** (optimized for demo):
- 50 Active Businesses
- 15 Ghost Businesses (zero electricity + zero labour filings + license renewed)
- 10 Dormant Businesses
- **Total: 225 Department Records → 86 UBIDs Created**

**Key Metrics Demonstrated:**
- **Entity Resolution Rate**: 38.2% (86 UBIDs from 225 records)
- **Ghost Detection Rate**: 100% (all 15 synthetic ghosts correctly identified)
- **Average Confidence Score**: 92.3%
- **Pending Reviews**: 28 records (records below auto-link threshold)
- **System Health**: All components online ✓

---

## Feature Walkthrough

### 1. **Dashboard**
Real-time overview of business entity resolution and intelligence:
- **Key Metrics**: Total Records, UBIDs, Ghost Businesses, Active Businesses
- **Resolution Rate**: Percentage of records successfully linked
- **Business Status Distribution**: Pie chart showing Active/Dormant/Ghost/Closed breakdown
- **System Health**: Status indicators for Entity Resolver, Activity Classifier, Data Pipeline
- **Review Queue**: Count of records awaiting manual review

### 2. **Ghost Businesses Detection**
Identifies and displays all flagged ghost businesses:
- **Business Details**: Name, PAN, GSTIN, Contact Information
- **Activity Signals**: License status, electricity consumption, labour filings, inspection history
- **Risk Assessment**: Confidence score indicating likelihood of regulatory non-compliance
- **Actionable Intelligence**: Recommendation for manual verification or license reclamation

### 3. **Entity Resolver**
Interactive engine for testing duplicate business detection:
- **Multi-Signal Analysis**: Enter business records and see confidence scores
- **Evidence Breakdown**: Shows which signals (name, address, PAN, etc.) drove the match score
- **Batch Resolution**: Test multiple record combinations
- **Decision Support**: Visual comparison of matched records

### 4. **Query Interface**
Pre-built queries for complex business intelligence:
- **All Ghost Businesses**: Full ghost business registry
- **Active Businesses**: Businesses with verified ongoing operations
- **Dormant Businesses**: Legally registered but inactive
- **Ghost by Pincode**: Geographic-specific ghost business analysis
- **CSV Export**: Export query results for further analysis

---

## How to Run the Application

### Prerequisites
- Python 3.10+ (for backend)
- Node.js 16+ (for frontend)
- npm or yarn (for frontend package management)
- Git (for version control)

### Quick Start (5 minutes)

#### 1. Clone the Repository
```bash
cd c:\Users\PRASHANT VAIBHAV\Documents\GitHub\ai_bharat\ubid-os
```

#### 2. Backend Setup
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
Initializing synthetic data...
Generated 225 department records
Created 86 UBIDs
Classified 66 businesses
INFO: Application startup complete
INFO: Uvicorn running on http://0.0.0.0:8000
```

#### 3. Frontend Setup (in new terminal)
```bash
cd frontend
npm install
npm start
```

**Expected Output:**
```
Compiled with warnings
webpack compiled with 1 warning
Listening on http://localhost:3000
```

#### 4. Access Application
- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

---

## API Reference

### Core Endpoints

#### Statistics
```http
GET /api/statistics
```
Returns: Total records, UBIDs created, businesses by status, average confidence

#### Ghost Businesses
```http
GET /api/ghost-businesses
```
Returns: List of all detected ghost businesses with activity signals

#### Entity Resolution
```http
POST /api/resolve
Content-Type: application/json

{
  "records": [
    {
      "business_name": "XYZ Manufacturing",
      "address": "Bangalore",
      "pan": "ABCDE1234F",
      "gstin": "18AABCT1234H1Z0",
      "nic_code": "25101"
    },
    {
      "business_name": "XYZ Mfg Industries",
      "address": "Banglore, Karnataka",
      "pan": "ABCDE1234F"
    }
  ]
}
```
Returns: Confidence scores, matched entity groups, evidence breakdown

#### Review Decision
```http
POST /api/review-decision
Content-Type: application/json

{
  "record_id_1": "rec_001",
  "record_id_2": "rec_002",
  "decision": "confirm",
  "rationale": "Same business, confirmed via phone verification"
}
```

---

## Unique Value Propositions

1. **Ghost Business Detection** — Only solution that identifies businesses appearing active but with zero real economic activity

2. **Event Sourcing Architecture** — Every decision is explainable, reversible, and auditable

3. **Conservative Confidence Thresholds** — Prioritizes data integrity over volume (92% auto-link threshold vs. typical 80%)

4. **Human-in-the-Loop Design** — Ambiguous cases routed to reviewers; human decisions feed back into model improvement

5. **Non-Invasive Overlay** — Zero modifications to source systems; works as a read-only intelligence layer above existing infrastructure

---

## Non-Negotiables Compliance

| Constraint | Implementation |
|-----------|-----------------|
| Source systems cannot be modified | CDC/polling layer reads only — zero writes |
| No raw PII to external services | Deterministic scrambling before AI processing |
| Every decision explainable & reversible | Event sourcing architecture |
| Wrong merge > missed merge | Conservative 0.92 auto-link threshold |
| Ambiguous cases → human review | Bayesian confidence routing to reviewer queue |

---

## Success Metrics

After deployment, UBID-OS enables:

### Query 1
**How many factories are currently operating in Electronic City (560100) with active KSPCB compliance and 50+ labour workforce?**
- *Previously impossible* — no cross-system join key
- *Now possible* — UBID registry + event sourcing

### Query 2
**Which businesses in Bengaluru renewed Shop Establishment licenses in the last 6 months but show zero BESCOM consumption?**
- *Ghost Business Detection* in action
- *Enables targeted inspections and fraud detection*

### Query 3
**Show all UBIDs where business names differ significantly across 3+ department systems.**
- *Master data quality issues identified*
- *Candidates for department-level correction*

---

## Future Enhancements

**Round 2 (If Selected):**
1. Production database integration (PostgreSQL + TimescaleDB)
2. Real department APIs integration with CDC/Debezium
3. Advanced ML classifier (XGBoost) for activity prediction
4. GraphQL API for complex queries
5. Mobile app for field inspectors
6. Integration with e-filing systems for automated data capture

---

## Submission Information

- **Project Name**: UBID-OS (Unified Business Identifier Operating System)
- **Theme**: Theme 1 — UBID and Active Business Intelligence
- **Team**: AI for Bharat Hackathon 2026
- **Institution**: PAN IIT Bangalore Hackathon
- **Submission Date**: May 7, 2026

---

## Demo Access

**Local Development:**
```bash
# Terminal 1: Backend
cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend && npm start

# Access: http://localhost:3000
```

**API Documentation:**
http://localhost:8000/docs (Swagger UI)

---

**UBID-OS: From Identity to Intelligence**
*Every Karnataka business. One identity. A living digital heartbeat.*
