import React, { createContext, useContext, useState, useEffect } from 'react';
import authService from '../services/authService';
import userService from '../services/userService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(authService.isAuthenticated());
    const [user, setUser] = useState(null);

    useEffect(() => {
        setIsAuthenticated(authService.isAuthenticated());

        const fetchUser = async () => {
            try {
                const userData = await userService.getProfile();
                setUser(userData);
            } catch (error) {
                console.error("Error fetching user data:", error);
                setUser(null);
            }
        };

        if (isAuthenticated) {
            fetchUser();
        } else {
            setUser(null)
        }
    }, [isAuthenticated]);

    const login = async (username, password) => {
        try {
            const data = await authService.login(username, password);
            setIsAuthenticated(true);
            return data;
        } catch (error) {
            throw error;
        }
    };

    const logout = () => {
        authService.logout();
        setIsAuthenticated(false);
        setUser(null); // Clear user data on logout
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);