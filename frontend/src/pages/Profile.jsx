import { useAuth } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';

const Profile = () => {
  const { user, profile, logout } = useAuth();
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      const data = await profile();
      setProfileData(data);
      setLoading(false);
    };
    fetchProfile();
  }, [profile]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-xl text-gray-500">Loading profile...</div>
      </div>
    );
  }

  const displayUser = profileData || user;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">Profile</h1>
              <p className="text-gray-500">Manage your account details</p>
            </div>
            <div className="space-x-2">
              <Link
                to="/dashboard"
                className="bg-indigo-500 text-white px-6 py-2 rounded-lg hover:bg-indigo-600 transition"
              >
                Dashboard
              </Link>
              <button
                onClick={logout}
                className="bg-red-500 text-white px-6 py-2 rounded-lg hover:bg-red-600 transition"
              >
                Logout
              </button>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Profile Card */}
            <div className="bg-gradient-to-r from-purple-500 to-pink-600 text-white p-8 rounded-xl">
              <div className="text-center mb-6">
                <div className="w-24 h-24 bg-white bg-opacity-20 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span className="text-3xl font-bold">
                    {displayUser?.first_name?.[0] || '?'}
                    {displayUser?.last_name?.[0] || ''}
                  </span>
                </div>
                <h2 className="text-2xl font-bold mb-1">
                  {displayUser?.first_name} {displayUser?.last_name}
                </h2>
                <p className="opacity-90">{displayUser?.email}</p>
              </div>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span>User ID:</span>
                  <span className="font-semibold">{displayUser?.id}</span>
                </div>
                <div className="flex justify-between">
                  <span>Account Status:</span>
                  <span className={`font-semibold ${displayUser?.is_active ? 'text-green-200' : 'text-red-200'}`}>
                    {displayUser?.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Member Since:</span>
                  <span>{new Date(displayUser?.date_joined).toLocaleDateString()}</span>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-gray-50 p-8 rounded-xl">
              <h3 className="text-xl font-bold mb-6 text-gray-800">Quick Actions</h3>
              <div className="space-y-3">
                <button
                  onClick={async () => {
                    setLoading(true);
                    const freshData = await profile();
                    setProfileData(freshData);
                    setLoading(false);
                  }}
                  disabled={loading}
                  className="w-full bg-indigo-500 text-white py-3 px-4 rounded-lg hover:bg-indigo-600 disabled:opacity-50 transition flex items-center justify-center space-x-2"
                >
                  <span>🔄</span>
                  <span>Refresh Profile</span>
                </button>
                <Link
                  to="/dashboard"
                  className="w-full block text-center bg-blue-500 text-white py-3 px-4 rounded-lg hover:bg-blue-600 transition"
                >
                  Go to Dashboard
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
