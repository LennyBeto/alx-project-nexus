// src/hooks/useAuth.js
import { useState } from 'react';
import { useMutation, useLazyQuery } from '@apollo/client';
import { LOGIN_USER, REGISTER_USER, GET_ME } from '../graphql/queries';
import { useAuth as useAuthContext } from '../context/AuthContext';
import AsyncStorage from '@react-native-async-storage/async-storage';

/**
 * Custom hook for authentication operations
 * Handles login, registration, and user profile operations
 */
export const useAuthMutations = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { login: contextLogin, logout: contextLogout } = useAuthContext();

  // GraphQL mutations
  const [loginMutation] = useMutation(LOGIN_USER, {
    onError: (error) => {
      console.error('Login mutation error:', error);
      setError(error.message);
    }
  });

  const [registerMutation] = useMutation(REGISTER_USER, {
    onError: (error) => {
      console.error('Register mutation error:', error);
      setError(error.message);
    }
  });

  // Query for fetching user profile
  const [getMe, { data: userData, loading: profileLoading }] = useLazyQuery(GET_ME, {
    onError: (error) => {
      console.error('Get user profile error:', error);
      setError(error.message);
    }
  });

  /**
   * Login user with username and password
   * @param {string} username - User's username
   * @param {string} password - User's password
   * @returns {Object} - Result object with success status and user data
   */
  const login = async (username, password) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await loginMutation({
        variables: { username, password },
      });

      const { success, message, token, user } = result.data.loginUser;

      if (success && token && user) {
        // Store token and update context
        await contextLogin(token, user);
        
        return { 
          success: true, 
          user,
          message: message || 'Login successful'
        };
      } else {
        throw new Error(message || 'Login failed');
      }
    } catch (error) {
      console.error('Login failed:', error);
      const errorMessage = error.graphQLErrors?.[0]?.message || error.message || 'Login failed';
      setError(errorMessage);
      
      return { 
        success: false, 
        error: errorMessage 
      };
    } finally {
      setLoading(false);
    }
  };

  /**
   * Register new user
   * @param {Object} userData - User registration data
   * @param {string} userData.username - Desired username
   * @param {string} userData.email - User's email
   * @param {string} userData.password - User's password
   * @param {string} userData.firstName - User's first name (optional)
   * @param {string} userData.lastName - User's last name (optional)
   * @returns {Object} - Result object with success status and user data
   */
  const register = async (userData) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await registerMutation({
        variables: {
          username: userData.username,
          email: userData.email,
          password: userData.password,
          firstName: userData.firstName || '',
          lastName: userData.lastName || '',
        },
      });

      const { success, message, token, user } = result.data.registerUser;

      if (success && token && user) {
        // Store token and update context
        await contextLogin(token, user);
        
        return { 
          success: true, 
          user,
          message: message || 'Registration successful'
        };
      } else {
        throw new Error(message || 'Registration failed');
      }
    } catch (error) {
      console.error('Registration failed:', error);
      const errorMessage = error.graphQLErrors?.[0]?.message || error.message || 'Registration failed';
      setError(errorMessage);
      
      return { 
        success: false, 
        error: errorMessage 
      };
    } finally {
      setLoading(false);
    }
  };

  /**
   * Logout current user
   * @returns {Promise} - Logout operation promise
   */
  const logout = async () => {
    setLoading(true);
    setError(null);
    
    try {
      await contextLogout();
      return { success: true };
    } catch (error) {
      console.error('Logout error:', error);
      setError(error.message);
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  };

  /**
   * Fetch current user profile
   * @returns {Promise} - User profile data
   */
  const fetchUserProfile = async () => {
    try {
      const result = await getMe();
      return result.data?.me || null;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      setError(error.message);
      return null;
    }
  };

  /**
   * Clear authentication error
   */
  const clearError = () => {
    setError(null);
  };

  return {
    // Operations
    login,
    register,
    logout,
    fetchUserProfile,
    clearError,
    
    // State
    loading,
    error,
    profileLoading,
    userData: userData?.me,
  };
};

/**
 * Hook for accessing authentication context
 * Provides current user state and authentication status
 */
export const useAuthState = () => {
  const { user, token, loading, isAuthenticated } = useAuthContext();
  
  return {
    user,
    token,
    loading,
    isAuthenticated,
    isLoggedIn: isAuthenticated,
  };
};

/**
 * Hook for form validation
 * Provides validation functions for auth forms
 */
export const useAuthValidation = () => {
  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePassword = (password) => {
    // At least 8 characters, 1 letter and 1 number
    return password.length >= 8 && /[A-Za-z]/.test(password) && /\d/.test(password);
  };

  const validateUsername = (username) => {
    // 3-30 characters, alphanumeric and underscores only
    return /^[a-zA-Z0-9_]{3,30}$/.test(username);
  };

  const validateRegistrationForm = (formData) => {
    const errors = {};

    if (!formData.username) {
      errors.username = 'Username is required';
    } else if (!validateUsername(formData.username)) {
      errors.username = 'Username must be 3-30 characters and contain only letters, numbers, and underscores';
    }

    if (!formData.email) {
      errors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      errors.email = 'Please enter a valid email address';
    }

    if (!formData.password) {
      errors.password = 'Password is required';
    } else if (!validatePassword(formData.password)) {
      errors.password = 'Password must be at least 8 characters with letters and numbers';
    }

    if (formData.confirmPassword && formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  };

  const validateLoginForm = (formData) => {
    const errors = {};

    if (!formData.username) {
      errors.username = 'Username is required';
    }

    if (!formData.password) {
      errors.password = 'Password is required';
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  };

  return {
    validateEmail,
    validatePassword,
    validateUsername,
    validateRegistrationForm,
    validateLoginForm,
  };
};

/**
 * Hook for managing authentication token
 * Handles token storage and retrieval
 */
export const useAuthToken = () => {
  const [tokenLoading, setTokenLoading] = useState(false);

  const storeToken = async (token) => {
    setTokenLoading(true);
    try {
      await AsyncStorage.setItem('authToken', token);
    } catch (error) {
      console.error('Error storing auth token:', error);
      throw error;
    } finally {
      setTokenLoading(false);
    }
  };

  const getToken = async () => {
    setTokenLoading(true);
    try {
      const token = await AsyncStorage.getItem('authToken');
      return token;
    } catch (error) {
      console.error('Error getting auth token:', error);
      return null;
    } finally {
      setTokenLoading(false);
    }
  };

  const removeToken = async () => {
    setTokenLoading(true);
    try {
      await AsyncStorage.removeItem('authToken');
    } catch (error) {
      console.error('Error removing auth token:', error);
      throw error;
    } finally {
      setTokenLoading(false);
    }
  };

  return {
    storeToken,
    getToken,
    removeToken,
    tokenLoading,
  };
};

// Default export for convenience
export default useAuthMutations;
