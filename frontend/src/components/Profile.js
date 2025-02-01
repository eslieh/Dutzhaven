import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import userService from '../services/userService';

const Profile = () => {
  const { user, logout } = useAuth();
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true); // Set loading to true before fetching
      setError(null); // Clear any previous errors

      try {
        const data = await userService.getProfile();
        setProfileData(data);
      } catch (err) {
        setError(err.message || 'Error fetching profile.');
        console.error("Profile fetch error:", err); // Log error for debugging
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      fetchProfile();
    } else {
      setLoading(false);
      // Optional: Redirect to login if user is not authenticated
      // navigate('/login');
    }
  }, [user, navigate]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) {
    return <div>Loading profile...</div>; // Or a more visually appealing loading indicator
  }

  if (error) {
    return <div style={{ color: 'red' }}>{error}</div>;
  }

  if (!profileData) {
    return <div>No profile data available.</div>; // Or a message like "Profile data not found"
  }

  return (
    <div>
      <h1>Profile</h1>
      <p><strong>Full Name:</strong> {profileData.fullName}</p>
      <p><strong>Username:</strong> {profileData.username}</p>
      <p><strong>Email:</strong> {profileData.email}</p>
      {/* ... other profile details */}
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Profile;