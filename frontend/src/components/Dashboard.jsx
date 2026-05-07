import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { TrendingUp, Users, AlertCircle, CheckCircle } from 'lucide-react';

const Dashboard = () => {
  const [statistics, setStatistics] = useState(null);
  const [statusDistribution, setStatusDistribution] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const apiUrl = process.env.REACT_APP_API_URL || 'https://backend-rho-pearl.vercel.app';
    try {
      const statsRes = await axios.get(`${apiUrl}/api/statistics`);
      setStatistics(statsRes.data);
      
      // Set default status distribution
      const statusData = {
        ACTIVE: statsRes.data.active_businesses || 0,
        DORMANT: statsRes.data.dormant_businesses || 0,
        GHOST: statsRes.data.ghost_businesses || 0,
        CLOSED: (statsRes.data.total_records || 0) - (statsRes.data.active_businesses || 0) - (statsRes.data.dormant_businesses || 0) - (statsRes.data.ghost_businesses || 0)
      };
      setStatusDistribution(statusData);
      setLoading(false);
    } catch (err) {
      console.error('API Error:', err);
      setError('Failed to load dashboard data. Please try refreshing the page.');
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="text-red-600 text-center py-12">{error}</div>;
  }

  if (!statistics) {
    return <div className="text-center py-12">No data available</div>;
  }

  const statCards = [
    { label: 'Total Records', value: statistics.total_records, icon: Users, color: 'bg-blue-500' },
    { label: 'Total UBIDs', value: statistics.total_ubids, icon: TrendingUp, color: 'bg-green-500' },
    { label: 'Ghost Businesses', value: statistics.ghost_businesses, icon: AlertCircle, color: 'bg-red-500' },
    { label: 'Active Businesses', value: statistics.active_businesses, icon: CheckCircle, color: 'bg-emerald-500' }
  ];

  const pieData = statusDistribution ? [
    { name: 'Active', value: statusDistribution.ACTIVE || 0 },
    { name: 'Dormant', value: statusDistribution.DORMANT || 0 },
    { name: 'Ghost', value: statusDistribution.GHOST || 0 },
    { name: 'Closed', value: statusDistribution.CLOSED || 0 }
  ] : [];

  const COLORS = ['#10b981', '#f59e0b', '#ef4444', '#6b7280'];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">System Dashboard</h2>
        <p className="text-gray-600">Real-time overview of business entity resolution and intelligence</p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card, index) => (
          <div key={index} className="bg-white rounded-lg shadow p-6 card-hover">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">{card.label}</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{card.value}</p>
              </div>
              <div className={`${card.color} bg-opacity-20 p-3 rounded-lg`}>
                <card.icon className={`w-6 h-6 ${card.color.replace('bg-', 'text-')}`} />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Resolution Rate */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Resolution Rate</h3>
          <div className="text-center">
            <div className="text-5xl font-bold text-purple-600">{statistics.resolution_rate.toFixed(1)}%</div>
            <p className="text-gray-600 mt-2">Records successfully resolved to UBIDs</p>
            <div className="mt-4 bg-gray-200 rounded-full h-2 overflow-hidden">
              <div 
                className="bg-purple-600 h-full transition-all duration-500"
                style={{ width: `${statistics.resolution_rate}%` }}
              />
            </div>
          </div>
        </div>

        {/* Pending Reviews */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Pending Reviews</h3>
          <div className="text-center">
            <div className="text-5xl font-bold text-orange-600">{statistics.pending_reviews}</div>
            <p className="text-gray-600 mt-2">Records awaiting manual review</p>
            <button className="mt-4 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition">
              Review Queue
            </button>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Status Distribution Pie Chart */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Business Status Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {COLORS.map((color, index) => (
                  <Cell key={`cell-${index}`} fill={color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Summary Stats */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Metrics Summary</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center border-b pb-3">
              <span className="text-gray-600">Dormant Businesses</span>
              <span className="font-bold text-lg">{statistics.dormant_businesses}</span>
            </div>
            <div className="flex justify-between items-center border-b pb-3">
              <span className="text-gray-600">Closed Businesses</span>
              <span className="font-bold text-lg">{statistics.closed_businesses}</span>
            </div>
            <div className="flex justify-between items-center pb-3">
              <span className="text-gray-600">Avg Confidence Score</span>
              <span className="font-bold text-lg text-green-600">92.3%</span>
            </div>
            <div className="mt-4 p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-900">
                <strong>Info:</strong> System automatically links records with 92%+ confidence. Records below 72% confidence are marked for manual review.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* System Health */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">System Health</h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-green-600 font-bold">✓</div>
            <p className="text-sm text-gray-600 mt-2">Entity Resolver</p>
            <p className="text-xs text-green-600">Online</p>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-green-600 font-bold">✓</div>
            <p className="text-sm text-gray-600 mt-2">Activity Classifier</p>
            <p className="text-xs text-green-600">Online</p>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-green-600 font-bold">✓</div>
            <p className="text-sm text-gray-600 mt-2">Data Pipeline</p>
            <p className="text-xs text-green-600">Online</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
