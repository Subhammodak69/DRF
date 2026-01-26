import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const { user } = useAuth(); 
  const [loading, setLoading] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
          </div>

          {loading ? (
            <div className="text-center py-8">
              <p className="text-gray-500">Loading your dashboard...</p>
            </div>
          ) : (
            <>
              <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-8 rounded-xl mb-8">
                <h2 className="text-3xl font-bold mb-2">
                  Hello, {user?.first_name || 'User'}!
                </h2>
                <p className="opacity-90">
                  Welcome back to your dashboard. Here's what's happening with your account.
                </p>
              </div>

              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

