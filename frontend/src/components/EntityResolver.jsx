import React, { useState } from 'react';
import axios from 'axios';
import { Check, X, AlertCircle } from 'lucide-react';

const EntityResolver = () => {
  const [records, setRecords] = useState([
    { business_name: '', address: '', pan: '', gstin: '', nic_code: '' }
  ]);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleRecordChange = (index, field, value) => {
    const newRecords = [...records];
    newRecords[index][field] = value;
    setRecords(newRecords);
  };

  const addRecord = () => {
    setRecords([...records, { business_name: '', address: '', pan: '', gstin: '', nic_code: '' }]);
  };

  const removeRecord = (index) => {
    setRecords(records.filter((_, i) => i !== index));
  };

  const handleResolve = async () => {
    if (records.filter(r => r.business_name).length < 2) {
      setError('Please enter at least 2 business records');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await axios.post('http://localhost:8000/api/resolve', records);
      setMatches(res.data.matches);
    } catch (err) {
      setError('Failed to resolve entities');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Entity Resolution Engine</h2>
        <p className="text-gray-600">
          Enter multiple business records to detect duplicates and potential matches using multi-signal analysis
        </p>
      </div>

      {/* Input Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Enter Business Records</h3>
        
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
            {error}
          </div>
        )}

        <div className="space-y-4">
          {records.map((record, index) => (
            <div key={index} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
              <div className="flex justify-between items-center mb-3">
                <h4 className="font-semibold text-gray-900">Record {index + 1}</h4>
                {index > 0 && (
                  <button
                    onClick={() => removeRecord(index)}
                    className="text-red-600 hover:text-red-800 text-sm"
                  >
                    Remove
                  </button>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <input
                  type="text"
                  placeholder="Business Name"
                  value={record.business_name}
                  onChange={(e) => handleRecordChange(index, 'business_name', e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
                />
                <input
                  type="text"
                  placeholder="Address"
                  value={record.address}
                  onChange={(e) => handleRecordChange(index, 'address', e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
                />
                <input
                  type="text"
                  placeholder="PAN"
                  value={record.pan}
                  onChange={(e) => handleRecordChange(index, 'pan', e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
                />
                <input
                  type="text"
                  placeholder="GSTIN"
                  value={record.gstin}
                  onChange={(e) => handleRecordChange(index, 'gstin', e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
                />
                <input
                  type="text"
                  placeholder="NIC Code"
                  value={record.nic_code}
                  onChange={(e) => handleRecordChange(index, 'nic_code', e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
                />
              </div>
            </div>
          ))}
        </div>

        <div className="mt-4 flex space-x-3">
          <button
            onClick={addRecord}
            className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 font-medium"
          >
            + Add Record
          </button>
          <button
            onClick={handleResolve}
            disabled={loading}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-medium disabled:opacity-50"
          >
            {loading ? 'Resolving...' : 'Resolve Entities'}
          </button>
        </div>
      </div>

      {/* Results Section */}
      {matches.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Found {matches.length} Potential Match{matches.length !== 1 ? 'es' : ''}
          </h3>

          <div className="space-y-4">
            {matches.map((match, index) => (
              <div key={index} className="p-4 border border-gray-200 rounded-lg">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <p className="text-sm text-gray-600">
                      <strong>Record {match.record_1_id}</strong> ↔ <strong>Record {match.record_2_id}</strong>
                    </p>
                  </div>
                  
                  {/* Recommendation Badge */}
                  <div className="ml-3">
                    {match.recommendation === 'AUTO_LINK' && (
                      <span className="inline-flex items-center space-x-1 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                        <Check className="w-4 h-4" />
                        <span>Auto Link</span>
                      </span>
                    )}
                    {match.recommendation === 'REVIEW' && (
                      <span className="inline-flex items-center space-x-1 px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium">
                        <AlertCircle className="w-4 h-4" />
                        <span>Manual Review</span>
                      </span>
                    )}
                    {match.recommendation === 'SEPARATE' && (
                      <span className="inline-flex items-center space-x-1 px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm font-medium">
                        <X className="w-4 h-4" />
                        <span>Separate</span>
                      </span>
                    )}
                  </div>
                </div>

                {/* Confidence Score */}
                <div className="mb-3">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-sm text-gray-600">Confidence Score</span>
                    <span className="text-lg font-bold text-purple-600">
                      {(match.confidence_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                    <div 
                      className={`h-full transition-all duration-300 ${
                        match.confidence_score >= 0.92 ? 'bg-green-500' :
                        match.confidence_score >= 0.72 ? 'bg-yellow-500' :
                        'bg-gray-400'
                      }`}
                      style={{ width: `${match.confidence_score * 100}%` }}
                    />
                  </div>
                </div>

                {/* Match Signals */}
                <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                  {Object.entries(match.match_signals || {}).map(([signal, score]) => (
                    <div key={signal} className="p-2 bg-gray-50 rounded text-center">
                      <p className="text-xs text-gray-600 capitalize">{signal.replace('_', ' ')}</p>
                      <p className="font-semibold text-sm text-gray-900">
                        {(score * 100).toFixed(0)}%
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Legend */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-900">
              <strong>Thresholds:</strong> 92%+ = Auto-linked | 72-92% = Manual review | &lt;72% = Likely separate entities
            </p>
          </div>
        </div>
      )}

      {!matches.length && !loading && (
        <div className="text-center py-12 text-gray-500">
          <p>Enter at least 2 records and click "Resolve Entities" to find matches</p>
        </div>
      )}
    </div>
  );
};

export default EntityResolver;
