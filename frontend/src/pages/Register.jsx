import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (field) => (e) => {
    setFormData({ ...formData, [field]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (formData.password !== formData.password_confirm) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    const result = await register(formData);
    if (result.success) {
      alert(result.message);
      navigate('/login');
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  const fields = [
    {
      row: true,
      items: [
        { key: 'first_name', label: 'First Name', type: 'text', placeholder: 'John', icon: (
          <svg className="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
          </svg>
        )},
        { key: 'last_name', label: 'Last Name', type: 'text', placeholder: 'Doe', icon: (
          <svg className="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
          </svg>
        )},
      ]
    },
    { key: 'username', label: 'Username', type: 'text', placeholder: 'johndoe', icon: (
      <svg className="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    )},
    { key: 'email', label: 'Email Address', type: 'email', placeholder: 'name@company.com', icon: (
      <svg className="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
      </svg>
    )},
    {
      row: true,
      items: [
        { key: 'password', label: 'Password', type: 'password', placeholder: '••••••••', icon: (
          <svg className="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
          </svg>
        )},
        { key: 'password_confirm', label: 'Confirm', type: 'password', placeholder: '••••••••', icon: (
          <svg className="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
          </svg>
        )},
      ]
    },
  ];

  const renderInput = (field) => (
    <div key={field.key}>
      <label className="block text-sm font-semibold text-slate-700 mb-2">{field.label}</label>
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
          {field.icon}
        </div>
        <input
          type={field.type}
          value={formData[field.key]}
          onChange={handleChange(field.key)}
          className="input-modern !pl-11"
          placeholder={field.placeholder}
          required
        />
      </div>
    </div>
  );

  return (
    <div className="bg-auth flex items-center justify-center px-4 py-12 relative overflow-hidden">
      {/* Floating Orbs */}
      <div className="orb orb-1 animate-float" />
      <div className="orb orb-2 animate-float-delayed" />

      <div className="w-full max-w-lg relative z-10">
        {/* Header */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="w-16 h-16 mx-auto mb-5 rounded-2xl bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center shadow-lg">
            <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={1.8} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M19 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zM4 19.235v-.11a6.375 6.375 0 0112.75 0v.109A12.318 12.318 0 0110.374 21c-2.331 0-4.512-.645-6.374-1.766z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gradient mb-2">Create Account</h1>
          <p className="text-slate-500">Join us and get started in seconds</p>
        </div>

        {/* Card */}
        <div className="glass-card p-8 animate-fade-in-delay">
          <form onSubmit={handleSubmit} className="space-y-4">
            {fields.map((field, i) => (
              field.row ? (
                <div key={i} className="grid grid-cols-2 gap-4">
                  {field.items.map(renderInput)}
                </div>
              ) : renderInput(field)
            ))}

            {/* Password strength hint */}
            {formData.password && (
              <div className="flex items-center space-x-2 animate-scale-in">
                <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      formData.password.length >= 8
                        ? 'w-full bg-gradient-to-r from-emerald-400 to-emerald-500'
                        : formData.password.length >= 6
                        ? 'w-2/3 bg-gradient-to-r from-amber-400 to-amber-500'
                        : 'w-1/3 bg-gradient-to-r from-red-400 to-red-500'
                    }`}
                  />
                </div>
                <span className={`text-xs font-medium ${
                  formData.password.length >= 8 ? 'text-emerald-500' :
                  formData.password.length >= 6 ? 'text-amber-500' : 'text-red-400'
                }`}>
                  {formData.password.length >= 8 ? 'Strong' :
                   formData.password.length >= 6 ? 'Medium' : 'Weak'}
                </span>
              </div>
            )}

            {/* Error */}
            {error && (
              <div className="flex items-center space-x-2 p-3 bg-red-50 border border-red-100 rounded-xl animate-scale-in">
                <svg className="w-5 h-5 text-red-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                </svg>
                <span className="text-sm text-red-600">{error}</span>
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="btn-gradient w-full !py-3 text-base mt-2"
              style={{ background: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)' }}
            >
              {loading ? (
                <span className="flex items-center justify-center space-x-2">
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Creating Account...</span>
                </span>
              ) : (
                'Create Account'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="mt-8 mb-6 flex items-center">
            <div className="flex-1 h-px bg-gradient-to-r from-transparent via-slate-200 to-transparent" />
            <span className="px-4 text-xs text-slate-400 font-medium uppercase tracking-wider">Already a member?</span>
            <div className="flex-1 h-px bg-gradient-to-r from-transparent via-slate-200 to-transparent" />
          </div>

          {/* Login Link */}
          <Link
            to="/login"
            className="block text-center w-full py-3 rounded-xl border-2 border-primary-200 text-primary-600 font-semibold hover:bg-primary-50 hover:border-primary-300 transition-all duration-300 hover:shadow-md"
          >
            Sign In Instead
          </Link>
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-slate-400 mt-6 animate-fade-in-delay-2">
          By signing up, you agree to our Terms of Service
        </p>
      </div>
    </div>
  );
};

export default Register;
