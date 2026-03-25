import { useAuth } from '../contexts/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import { useEffect, useState, useCallback } from 'react';

const Profile = () => {
  const { user, profile, logout } = useAuth();
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchProfile = useCallback(async () => {
    setLoading(true);
    const data = await profile();
    setProfileData(data);
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="bg-mesh flex items-center justify-center">
        <div className="text-center animate-fade-in">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-primary-500 font-medium">Loading profile...</p>
        </div>
      </div>
    );
  }

  const displayUser = profileData || user;
  const initials = (displayUser?.first_name?.[0] || '?') + (displayUser?.last_name?.[0] || '');

  const infoItems = [
    { label: 'Email', value: displayUser?.email, icon: '✉️' },
    { label: 'User ID', value: `#${displayUser?.id}`, icon: '🔑' },
    { label: 'Status', value: displayUser?.is_active ? 'Active' : 'Inactive', icon: '🟢',
      badge: true, badgeColor: displayUser?.is_active ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-500' },
    { label: 'Member Since', value: displayUser?.date_joined ? new Date(displayUser.date_joined).toLocaleDateString('en-US', { year:'numeric', month:'long', day:'numeric'}) : '—', icon: '📅' },
  ];

  return (
    <div className="bg-mesh pb-12">
      <div className="max-w-4xl mx-auto px-6 pt-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8 animate-fade-in">
          <div>
            <h1 className="text-3xl font-bold text-slate-800">Profile</h1>
            <p className="text-slate-500">Manage your account details</p>
          </div>
          <div className="flex items-center space-x-3">
            <Link to="/dashboard" className="px-5 py-2.5 rounded-xl bg-white border border-slate-200 text-slate-700 font-medium text-sm hover:border-primary-300 hover:text-primary-600 transition-all duration-300 hover:shadow-md">
              Dashboard
            </Link>
            <button onClick={handleLogout} className="px-5 py-2.5 rounded-xl bg-red-50 border border-red-100 text-red-500 font-medium text-sm hover:bg-red-100 hover:border-red-200 transition-all duration-300">
              Sign Out
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-5 gap-6">
          {/* Left: Profile Card */}
          <div className="md:col-span-2 animate-slide-up">
            <div className="glass-card p-8 text-center overflow-hidden relative">
              <div className="orb w-[150px] h-[150px] bg-gradient-to-br from-primary-200/30 to-purple-200/20 -top-16 -right-16 animate-float" />
              <div className="relative z-10">
                <div className="w-24 h-24 mx-auto rounded-2xl bg-gradient-to-br from-primary-500 to-purple-600 flex items-center justify-center text-white text-3xl font-bold shadow-glow mb-4">
                  {initials.toUpperCase()}
                </div>
                <h2 className="text-xl font-bold text-slate-800 mb-1">
                  {displayUser?.first_name} {displayUser?.last_name}
                </h2>
                <p className="text-sm text-slate-400 mb-5">{displayUser?.email}</p>
                <button
                  onClick={fetchProfile}
                  className="btn-gradient w-full !py-2.5 text-sm"
                >
                  🔄 Refresh Profile
                </button>
              </div>
            </div>
          </div>

          {/* Right: Info */}
          <div className="md:col-span-3 animate-slide-up-delay">
            <div className="glass-card p-8">
              <h3 className="text-lg font-bold text-slate-800 mb-5 flex items-center space-x-2">
                <svg className="w-5 h-5 text-primary-500" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
                </svg>
                <span>Account Details</span>
              </h3>
              <div className="space-y-3">
                {infoItems.map((item, i) => (
                  <div key={i} className="flex items-center justify-between p-4 bg-slate-50/60 rounded-xl hover:bg-slate-50 transition-colors">
                    <div className="flex items-center space-x-3">
                      <span className="text-lg">{item.icon}</span>
                      <span className="text-sm text-slate-500 font-medium">{item.label}</span>
                    </div>
                    {item.badge ? (
                      <span className={`text-xs font-semibold px-3 py-1 rounded-full ${item.badgeColor}`}>{item.value}</span>
                    ) : (
                      <span className="text-sm font-semibold text-slate-800">{item.value}</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
