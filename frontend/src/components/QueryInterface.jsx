import React, { useState } from 'react';
import axios from 'axios';
import { Search, Download } from 'lucide-react';

const QueryInterface = () => {
  const [queryType, setQueryType] = useState('ghost-by-status');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pincode, setPincode] = useState('');

  const queryTemplates = [
    { id: 'ghost-by-status', label: 'All Ghost Businesses', icon: '👻' },
    { id: 'active', label: 'Active Businesses', icon: '✓' },
    { id: 'dormant', label: 'Dormant Businesses', icon: '💤' },
    { id: 'by-pincode', label: 'Ghost by Pincode', icon: '📍' }
  ];

  const handleQuery = async () => {
    const apiUrl = process.env.REACT_APP_API_URL || 'https://backend-rho-pearl.vercel.app';
    setLoading(true);
    setError(null);

    try {
      let res;
      switch (queryType) {
        case 'ghost-by-status':
          res = await axios.get(`${apiUrl}/api/ghost-businesses`);
          setResults(res.data.ghost_businesses || []);
          break;
        case 'active':
          res = await axios.get(`${apiUrl}/api/active-businesses`);
          setResults(res.data.active_businesses || []);
          break;
        case 'dormant':
          res = await axios.get(`${apiUrl}/api/dormant-businesses`);
          setResults(res.data.dormant_businesses || []);
          break;
        case 'by-pincode':
          if (!pincode) {
            setError('Please enter a pincode');
            setLoading(false);
            return;
          }
          res = await axios.get(`${apiUrl}/api/query/ghost-by-pincode/${pincode}`);
          setResults(res.data.ghost_businesses || []);
          break;
        default:
          break;
      }
    } catch (err) {
      setError('Failed to execute query');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = () => {
    const csv = [
      ['Business Name', 'Address', 'PAN', 'GSTIN', 'Activity Status', 'Ghost Score'],
      ...results.map(r => [
        r.primary_name || r.business_name,
        r.primary_address || r.address || '',
        r.primary_pan || r.pan || '',
        r.primary_gstin || r.gstin || '',
        r.activity_status || '',
        ((r.ghost_business_score || 0) * 100).toFixed(1)
      ])
    ].map(row => row.map(cell => `"${cell}"`).join(',')).join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `query-results-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Query Interface</h2>
        <p className="text-gray-600">Execute pre-built queries to analyze business intelligence data</p>
      </div>

      {/* Query Templates */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {queryTemplates.map((template) => (
          <button
            key={template.id}
            onClick={() => setQueryType(template.id)}
            className={`p-4 rounded-lg border-2 transition text-center ${
              queryType === template.id
                ? 'border-purple-500 bg-purple-50'
                : 'border-gray-200 bg-white hover:border-gray-300'
            }`}
          >
            <div className="text-3xl mb-2">{template.icon}</div>
            <p className="font-medium text-sm text-gray-900">{template.label}</p>
          </button>
        ))}
      </div>

      {/* Query Configuration */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Query Configuration</h3>

        {queryType === 'by-pincode' && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">Pincode</label>
            <input
              type="text"
              placeholder="Enter pincode (e.g., 560001)"
              value={pincode}
              onChange={(e) => setPincode(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            />
          </div>
        )}

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm">
            {error}
          </div>
        )}

        <button
          onClick={handleQuery}
          disabled={loading}
          className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-medium disabled:opacity-50 flex items-center justify-center space-x-2"
        >
          <Search className="w-5 h-5" />
          <span>{loading ? 'Executing...' : 'Execute Query'}</span>
        </button>
      </div>

      {/* Results */}
      {results.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-900">
              Results ({results.length} records)
            </h3>
            <button
              onClick={handleExport}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 font-medium text-sm"
            >
              <Download className="w-4 h-4" />
              <span>Export CSV</span>
            </button>
          </div>

          {/* Results Table */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50">
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Business Name</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Address</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Status</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">PAN</th>
                  {queryType === 'ghost-by-status' && (
                    <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Ghost Score</th>
                  )}
                </tr>
              </thead>
              <tbody>
                {results.slice(0, 20).map((result, idx) => (
                  <tr key={idx} className="border-b border-gray-200 hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">
                      {result.primary_name || result.business_name}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600">
                      {(result.primary_address || result.address || '')?.substring(0, 50)}...
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        result.activity_status === 'ACTIVE' ? 'bg-green-100 text-green-800' :
                        result.activity_status === 'DORMANT' ? 'bg-yellow-100 text-yellow-800' :
                        result.activity_status === 'GHOST' ? 'bg-red-100 text-red-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {result.activity_status || 'Unknown'}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600">
                      {result.primary_pan || result.pan || '-'}
                    </td>
                    {queryType === 'ghost-by-status' && (
                      <td className="px-4 py-3 text-sm font-semibold text-red-600">
                        {((result.ghost_business_score || 0) * 100).toFixed(0)}%
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {results.length > 20 && (
            <p className="mt-4 text-sm text-gray-600">
              Showing 20 of {results.length} results. Export CSV to see all results.
            </p>
          )}
        </div>
      )}

      {results.length === 0 && !loading && queryType && (
        <div className="text-center py-12 text-gray-500">
          <p>No results found. Click "Execute Query" to get started.</p>
        </div>
      )}
    </div>
  );
};

export default QueryInterface;
