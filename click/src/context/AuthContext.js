// src/context/AuthContext.js
import React, { createContext, useState, useContext, useEffect } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useLazyQuery } from "@apollo/client";
import { GET_ME } from "../graphql/queries";

const AuthContext = createContext({});

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  const [getMe] = useLazyQuery(GET_ME, {
    onCompleted: (data) => {
      setUser(data.me);
      setLoading(false);
    },
    onError: (error) => {
      console.error("Error fetching user:", error);
      logout();
    },
  });

  // Check for stored token on app start
  useEffect(() => {
    checkAuthState();
  }, []);

  const checkAuthState = async () => {
    try {
      const storedToken = await AsyncStorage.getItem("authToken");
      if (storedToken) {
        setToken(storedToken);
        getMe();
      } else {
        setLoading(false);
      }
    } catch (error) {
      console.error("Error checking auth state:", error);
      setLoading(false);
    }
  };

  const login = async (authToken, userData) => {
    try {
      await AsyncStorage.setItem("authToken", authToken);
      setToken(authToken);
      setUser(userData);
    } catch (error) {
      console.error("Error storing auth token:", error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await AsyncStorage.removeItem("authToken");
      setToken(null);
      setUser(null);
    } catch (error) {
      console.error("Error removing auth token:", error);
    }
  };

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
