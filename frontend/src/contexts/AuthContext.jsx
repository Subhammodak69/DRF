import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/auth/';

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [tokens, setTokens] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch complete user data from backend
  const fetchUserData = useCallback(async (accessToken) => {
    try {
      const response = await axios.get('/user/', {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch user data:', error);
      return null;
    }
  }, []);

  // Initialize authentication state
  useEffect(() => {
    const initAuth = async () => {
      const access = localStorage.getItem('access');
      const refresh = localStorage.getItem('refresh');
      
      if (access && refresh) {
        try {
          // Set auth header first
          axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
          
          // Fetch fresh user data from backend
          const userData = await fetchUserData(access);
          
          if (userData) {
            setTokens({ access, refresh });
            setUser(userData);
          } else {
            // Invalid token, clear everything
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            delete axios.defaults.headers.common['Authorization'];
          }
        } catch (error) {
          // Clear invalid session
          localStorage.removeItem('access');
          localStorage.removeItem('refresh');
          delete axios.defaults.headers.common['Authorization'];
        }
      }
      setLoading(false);
    };

    initAuth();
  }, [fetchUserData]);

  const login = async (credentials) => {
    try {
      const response = await axios.post('/login/', credentials);
      const loginData = response.data;

      const { access, refresh } = loginData;

      // Store tokens
      localStorage.setItem('access', access);
      localStorage.setItem('refresh', refresh);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;

      // Fetch complete user data
      const userData = await fetchUserData(access);

      if (userData) {
        setTokens({ access, refresh });
        setUser(userData);
        return { success: true };
      } else {
        throw new Error('Failed to fetch user data');
      }
    } catch (error) {
      console.error('Login error:', error);
      // Always read the normalised { error: '...' } key from backend
      const message =
        error.response?.data?.error ||
        'Login failed. Please try again.';
      return { success: false, error: message };
    }
  };


  const register = async (userData) => {
    try {
      await axios.post('/register/', userData);
      return {
        success: true,
        message: 'Account created successfully. Please sign in.',
      };
    } catch (error) {
      const message =
        error.response?.data?.error ||
        'Registration failed. Please try again.';
      return { success: false, error: message };
    }
  };

  const logout = async () => {
    try {
      const refresh = localStorage.getItem('refresh');
      if (refresh) {
        await axios.post('/logout/', { refresh });
      }
    } catch (error) {
      // Ignore logout API errors — always clear local state
      console.warn('Logout API error (ignored):', error?.response?.data?.error);
    } finally {
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      setTokens(null);
      setUser(null);
      delete axios.defaults.headers.common['Authorization'];
    }
  };

  const profile = useCallback(async () => {
    try {
      // Use the already set axios Authorization header from context
      const response = await axios.get('/profile/');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch profile:', error);
      
      // If it's a 401 (Unauthorized), trigger logout
      if (error.response?.status === 401) {
        await logout();
      }
      
      return null;
    }
  }, [logout]);

  const value = {
    user,
    tokens,
    login,
    register,
    logout,
    profile,
    loading,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
