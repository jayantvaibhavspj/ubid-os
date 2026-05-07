import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-red-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-lg p-8 max-w-md">
            <h1 className="text-2xl font-bold text-red-600 mb-4">⚠️ Application Error</h1>
            <p className="text-gray-700 mb-4">An error occurred while rendering the application.</p>
            <p className="text-sm text-red-600 mb-4 bg-red-50 p-3 rounded font-mono overflow-auto">
              {this.state.error?.message || 'Unknown error'}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="w-full bg-red-600 text-white py-2 rounded hover:bg-red-700 font-semibold"
            >
              Reload Page
            </button>
            <p className="text-xs text-gray-500 mt-4">
              Check browser console (F12) for more details
            </p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
