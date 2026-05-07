import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { AlertTriangle, TrendingDown, MapPin, Lock, Zap, Users } from 'lucide-react';

const GhostBusinesses = () => {
  const [ghosts, setGhosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortBy, setSortBy] = useState('score');
  const [selectedBusiness, setSelectedBusiness] = useState(null);

  useEffect(() => {
    fetchGhostBusinesses();
  }, []);

  const fetchGhostBusinesses = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/ghost-businesses');
      setGhosts(res.data.ghost_businesses || []);
      setLoading(false);
    } catch (err) {
      setError('Failed to load ghost businesses');
      setLoading(false);
      console.error(err);
    }
  };

  const sortedGhosts = [...ghosts].sort((a, b) => {
    if (sortBy === 'score') return (b.ghost_business_score || 0) - (a.ghost_business_score || 0);
    if (sortBy === 'name') return (a.primary_name || '').localeCompare(b.primary_name || '');
    return 0;
  });

  if (loading) {
    return <div className="text-center py-12">Loading ghost businesses...</div>;
  }

  if (error) {
    return <div className="text-red-600 text-center py-12">{error}</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Ghost Businesses Detection</h2>
        <p className="text-gray-600">
          Identify businesses with active licenses but minimal operational activity across multiple department systems
        </p>
      </div>

      {/* Alert */}
      <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
        <div className="flex items-start">
          <AlertTriangle className="w-6 h-6 text-red-600 mt-0.5 mr-3" />
          <div>
            <h3 className="font-semibold text-red-800">Critical Finding</h3>
            <p className="text-red-700 text-sm mt-1">
              {ghosts.length} ghost businesses detected. These entities show active license status but zero operational engagement across electricity, labour, and inspection systems.
            </p>
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="bg-white rounded-lg shadow p-4 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <label className="flex items-center space-x-2">
            <span className="text-gray-600 text-sm font-medium">Sort by:</span>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
            >
              <option value="score">Ghost Score</option>
              <option value="name">Business Name</option>
            </select>
          </label>
        </div>
        <div className="text-right">
          <p className="text-2xl font-bold text-red-600">{ghosts.length}</p>
          <p className="text-gray-600 text-sm">Ghost Businesses</p>
        </div>
      </div>

      {/* Ghosts List */}
      <div className="space-y-4">
        {sortedGhosts.length === 0 ? (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
            <p className="text-green-800">No ghost businesses detected!</p>
          </div>
        ) : (
          sortedGhosts.map((ghost, index) => (
            <div 
              key={index} 
              onClick={() => setSelectedBusiness(ghost)}
              className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition cursor-pointer border-l-4 border-red-500"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <AlertTriangle className="w-5 h-5 text-red-600" />
                    <h3 className="text-lg font-semibold text-gray-900">{ghost.primary_name}</h3>
                  </div>
                  
                  {/* Ghost Score */}
                  <div className="mt-3 inline-block">
                    <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium">
                      Ghost Score: {((ghost.ghost_business_score || 0) * 100).toFixed(0)}%
                    </span>
                  </div>

                  {/* Evidence Grid */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                    <div className="flex items-center space-x-2">
                      <Lock className="w-4 h-4 text-red-600" />
                      <div>
                        <p className="text-xs text-gray-600">License Status</p>
                        <p className="font-semibold text-sm">Active</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <Zap className="w-4 h-4 text-yellow-600" />
                      <div>
                        <p className="text-xs text-gray-600">Electricity (6m)</p>
                        <p className="font-semibold text-sm">{ghost.electricity_consumption_6m?.toFixed(0) || 0} kWh</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <Users className="w-4 h-4 text-blue-600" />
                      <div>
                        <p className="text-xs text-gray-600">Labour Filings (12m)</p>
                        <p className="font-semibold text-sm">{ghost.labour_filings_12m || 0}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <TrendingDown className="w-4 h-4 text-purple-600" />
                      <div>
                        <p className="text-xs text-gray-600">Inspections Since</p>
                        <p className="font-semibold text-sm">{ghost.months_since_inspection || 0}m</p>
                      </div>
                    </div>
                  </div>

                  {/* Address */}
                  <div className="mt-3 flex items-start space-x-2">
                    <MapPin className="w-4 h-4 text-gray-400 mt-0.5" />
                    <p className="text-sm text-gray-600">{ghost.primary_address}</p>
                  </div>
                </div>

                {/* Risk Badge */}
                <div className="ml-4 text-right">
                  <div className="text-center p-2 bg-red-100 rounded-lg">
                    <p className="text-red-800 font-bold text-lg">HIGH RISK</p>
                    <p className="text-red-600 text-xs">Ghost Business</p>
                  </div>
                </div>
              </div>

              {/* Evidence Timeline Preview */}
              <div className="mt-4 pt-4 border-t">
                <p className="text-xs font-semibold text-gray-600 mb-2">RECENT EVIDENCE</p>
                <div className="flex space-x-2 text-xs">
                  {ghost.evidence_timeline && ghost.evidence_timeline.slice(0, 3).map((event, i) => (
                    <span key={i} className="bg-gray-100 px-2 py-1 rounded">
                      {event.event_type}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Detail Modal */}
      {selectedBusiness && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-96 overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-2xl font-bold">{selectedBusiness.primary_name}</h3>
                <button 
                  onClick={() => setSelectedBusiness(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>

              {/* Timeline */}
              <div className="space-y-3">
                <h4 className="font-semibold text-gray-900">Evidence Timeline</h4>
                {selectedBusiness.evidence_timeline && selectedBusiness.evidence_timeline.map((event, i) => (
                  <div key={i} className="flex space-x-3">
                    <div className="w-32 text-sm text-gray-600">
                      {event.event_type}
                    </div>
                    <div className="text-sm">
                      <p className="font-medium text-gray-900">{event.evidence}</p>
                      <p className="text-xs text-gray-500">{event.source_system}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GhostBusinesses;
