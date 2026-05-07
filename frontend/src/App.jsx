import React, { useState } from 'react';
import { Activity, Ghost, Database, FileSearch, BarChart3 } from 'lucide-react';
import Dashboard from './components/Dashboard';
import GhostBusinesses from './components/GhostBusinesses';
import EntityResolver from './components/EntityResolver';
import QueryInterface from './components/QueryInterface';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const navigation = [
    { id: 'dashboard', name: 'Dashboard', icon: BarChart3, component: Dashboard },
    { id: 'ghost', name: 'Ghost Businesses', icon: Ghost, component: GhostBusinesses },
    { id: 'resolver', name: 'Entity Resolver', icon: Database, component: EntityResolver },
    { id: 'query', name: 'Query Interface', icon: FileSearch, component: QueryInterface },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="gradient-bg text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Activity className="w-10 h-10" />
              <div>
                <h1 className="text-3xl font-bold">UBID-OS</h1>
                <p className="text-sm opacity-90">Business Operating System for Karnataka</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm opacity-90">PAN IIT Bangalore Hackathon 2026</p>
              <p className="text-xs opacity-75">Karnataka Commerce & Industry</p>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {navigation.map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`
                  flex items-center space-x-2 py-4 px-3 border-b-2 font-medium text-sm
                  transition-colors
                  ${activeTab === item.id
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <item.icon className="w-5 h-5" />
                <span>{item.name}</span>
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {navigation.map((item) => (
          <div key={item.id} className={activeTab === item.id ? 'block' : 'hidden'}>
            <item.component />
          </div>
        ))}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            UBID-OS: From Identity to Intelligence • Every Karnataka business. One identity. A living digital heartbeat.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
