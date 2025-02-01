import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
    const { isAuthenticated, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    const renderAuthLinks = () => {
        if (location.pathname === '/') {
            return null;
        } else if (isAuthenticated) {
            return (
                <>
                    <Link to="/profile">Profile</Link>{' '} {/* Added space */}
                    <button onClick={handleLogout}>Logout</button>
                </>
            );
        } else {
            return (
                <>
                    <Link to="/login">Login</Link>{' '} {/* Added space */}
                    <Link to="/register">Register</Link>
                </>
            );
        }
    };

    return (
        <nav>
            <Link to="/" className="logo">DutzHaven</Link>
            <div>
                {renderAuthLinks()}
            </div>
        </nav>
    );
};

export default Navbar;