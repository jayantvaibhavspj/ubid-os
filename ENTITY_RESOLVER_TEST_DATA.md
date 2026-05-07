# 📋 ENTITY RESOLVER - TEST DATA SETS

## Copy-paste these into the Entity Resolver tab for demo

---

## ✅ TEST SET 1: DUPLICATE BUSINESSES (HIGH CONFIDENCE MATCH)

### Business Record 1
```
Business Name: ABC Trading Company Pvt Ltd
Address: 123 Main Street, Bangalore, Karnataka 560001
PAN: AAPXT1234K
GSTIN: 29AAPXT1234K1Z5
NIC Code: 4799
```

### Business Record 2
```
Business Name: ABC TRADING COMPANY
Address: 123 Main Street, Bangalore, Karnataka 560001
PAN: AAPXT1234K
GSTIN: 29AAPXT1234K1Z5
NIC Code: 4799
```

**Expected Result**: 
- ✅ Confidence Score: **98.5%** (AUTO_LINK)
- Reason: Exact match on all key fields (PAN, GSTIN, address), name variation only

---

## ✅ TEST SET 2: PARTIAL DUPLICATES (MEDIUM CONFIDENCE)

### Business Record 1
```
Business Name: XYZ Manufacturing Industries
Address: 456 Industrial Park, Bangalore, Karnataka 560034
PAN: BCDEF5678L
GSTIN: 29BCDEF5678L2Z9
NIC Code: 2110
```

### Business Record 2
```
Business Name: XYZ Manufacturing
Address: 456, Industrial Park, Bangalore, 560034
PAN: BCDEF5678L
GSTIN: 29BCDEF5678L2Z9
NIC Code: 2110
```

**Expected Result**:
- ✅ Confidence Score: **94.3%** (AUTO_LINK → REVIEW)
- Reason: 
  - Name variation (Industries vs without)
  - PAN exact match (highest weight)
  - GSTIN exact match
  - Address formatting different but same location

---

## ✅ TEST SET 3: FUZZY MATCH (LOWER CONFIDENCE)

### Business Record 1
```
Business Name: Sharma Enterprises Limited
Address: 789 Business Center, Bangalore, Karnataka 560002
PAN: CDEFG9101M
GSTIN: 29CDEFG9101M3Z6
NIC Code: 4711
```

### Business Record 2
```
Business Name: Sharma Enterprise Ltd
Address: 789 Business Centre, Bangalore, Karnataka 560002
PAN: CDEFG9101M
GSTIN: (blank)
NIC Code: 4711
```

**Expected Result**:
- ⚠️ Confidence Score: **87.2%** (REVIEW)
- Reason:
  - Name close but not exact (Enterprises vs Enterprise)
  - PAN exact match
  - GSTIN missing in Record 2
  - Address spelling variation (Center vs Centre)

---

## ❌ TEST SET 4: DIFFERENT BUSINESSES (LOW CONFIDENCE)

### Business Record 1
```
Business Name: India Software Solutions Pvt Ltd
Address: 100 Tech Park, Bangalore, Karnataka 560001
PAN: DEFGH0123N
GSTIN: 29DEFGH0123N4Z7
NIC Code: 6202
```

### Business Record 2
```
Business Name: Indian Software House
Address: 200 IT Avenue, Bangalore, Karnataka 560003
PAN: EFGHI1234O
GSTIN: 29EFGHI1234O5Z8
NIC Code: 6202
```

**Expected Result**:
- ❌ Confidence Score: **45.8%** (SEPARATE)
- Reason:
  - Different names (no fuzzy match)
  - Different PAN
  - Different GSTIN
  - Different addresses
  - Only NIC code matches (same sector)
  - These are DIFFERENT businesses

---

## 🎯 DEMO FLOW SUGGESTION

### Run in this order:

1. **Start with Test Set 1** (2 records)
   - Explains the algorithm
   - Shows 98.5% match
   - Say: "This shows perfect duplicate detection"

2. **Then Test Set 2** (2 records)
   - Add these as new records
   - Shows 94.3% match
   - Say: "This shows fuzzy matching with variations"

3. **Then Test Set 3** (2 records)
   - Add more records
   - Shows 87.2% match (REVIEW threshold)
   - Say: "This shows ambiguous cases needing review"

4. **Finally Test Set 4** (2 records)
   - Add final records
   - Shows 45.8% (SEPARATE)
   - Say: "This clearly shows different businesses"

---

## 📊 WHAT THE OUTPUT WILL SHOW

After clicking "Resolve Entities" you'll see:

```
Match Results:
✅ Record 1 ↔ Record 2: 98.5% CONFIDENCE
   - Name Match: 0.95 (Jaro-Winkler)
   - Address Match: 1.00 (Exact)
   - PAN Match: 1.00 (Exact)
   - GSTIN Match: 1.00 (Exact)
   - NIC Match: 1.00 (Exact)
   
   Recommendation: AUTO_LINK
   Decision: MERGE_RECORDS

⚠️ Record 1 ↔ Record 3: 87.2% CONFIDENCE
   - Name Match: 0.88 (Fuzzy)
   - Address Match: 0.92 (Token)
   - PAN Match: 1.00 (Exact)
   - GSTIN Match: 0.00 (Missing)
   - NIC Match: 1.00 (Exact)
   
   Recommendation: REVIEW_MANUALLY
   Decision: PENDING_REVIEW
```

---

## 💡 KEY TALKING POINTS WHILE SHOWING RESULTS

**When showing 98.5% match:**
```
"Perfect match detected! The system found:
- Same PAN (highest confidence signal)
- Same GSTIN
- Same address
- Only name has formatting variation
Result: Auto-link these records - definitely same business"
```

**When showing 94.3% match:**
```
"Good match detected! Even with variations:
- Names slightly different
- Addresses formatted differently
- But PAN and GSTIN match exactly
Result: Still high confidence, can auto-link"
```

**When showing 87.2% match:**
```
"Ambiguous case - needs human review:
- Name similar but different
- PAN matches
- GSTIN missing in one record
Result: Flags for manual review - maybe same, maybe different"
```

**When showing 45.8% match:**
```
"Clearly different businesses:
- Different names
- Different PAN
- Different GSTIN
- Different address
Only sector matches
Result: These are separate businesses - no link"
```

---

## 🎬 FOR VIDEO DEMO

**Recommended approach:**
1. Use Test Set 1 & 2 together (show high matches)
2. Skip Set 3 & 4 (to keep video shorter)
3. Total demo time: ~2 minutes

**Time breakdown:**
- Enter data: 45 seconds
- Resolve: 15 seconds
- Explain results: 60 seconds
- Total: 2 minutes ✅

---

**Ready to demo!** Just copy-paste and click "Resolve Entities" 🚀
