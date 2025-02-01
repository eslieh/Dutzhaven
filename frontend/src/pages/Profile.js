import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { useAuth } from '../context/AuthContext';
import userService from '../services/userService';

const Profile = () => {
    const { isAuthenticated } = useAuth();
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [editing, setEditing] = useState(false);
    const [updatedUser, setUpdatedUser] = useState({});

    useEffect(() => {
        const fetchProfile = async () => {
            setLoading(true);
            setError(null);
            try {
                const userData = await userService.getProfile();
                setUser(userData);
                setUpdatedUser(userData ? { ...userData } : {}); // Handle null userData
            } catch (err) {
                setError(err.message || 'Error fetching profile');
                console.error("Profile fetch error:", err);
            } finally {
                setLoading(false);
            }
        };

        if (isAuthenticated) {
            fetchProfile();
        } else {
            setLoading(false);
        }
    }, [isAuthenticated]);

    const handleEdit = () => {
        setEditing(true);
    };

    const handleInputChange = (e) => {
        setUpdatedUser({ ...updatedUser, [e.target.name]: e.target.value });
    };

    const handleSave = async () => {
        setLoading(true); // Set loading to true during update
        setError(null);

        try {
            const updatedUserData = await userService.updateProfile(updatedUser); // Get updated user data from the server
            setUser(updatedUserData); // Update the displayed profile with the server data
            setUpdatedUser(updatedUserData); // Update the updated user data
            setEditing(false);
        } catch (err) {
            setError(err.message || 'Error updating profile');
            console.error("Profile update error:", err);
        } finally {
            setLoading(false);
        }
    };


    if (!isAuthenticated) {
        return <div>Please login to view your profile.</div>;
    }

    if (loading) {
        return <div>Loading profile...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!user) {
        return <div>User profile not found.</div>;
    }

    return (
        <div>
            <Navbar />
            <h1>Profile</h1>

            {editing ? (
                <form>
                    <input type="text" name="bio" value={updatedUser.bio || ''} onChange={handleInputChange} placeholder="Bio" />
                    <input type="text" name="contact_info" value={updatedUser.contact_info || ''} onChange={handleInputChange} placeholder="Contact Info" />
                    {/* ... other editable fields ... */}
                    <button type="button" onClick={handleSave} disabled={loading}> {/* Disable button while saving */}
                        {loading ? "Saving..." : "Save"} {/* Show loading indicator */}
                    </button>
                    <button type="button" onClick={() => setEditing(false)} disabled={loading}> {/* Disable button while saving */}
                        Cancel
                    </button>
                    {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error message */}

                </form>
            ) : (
                <div>
                    <p><strong>Username:</strong> {user.username}</p>
                    <p><strong>Email:</strong> {user.email}</p>
                    <p><strong>Bio:</strong> {user.bio}</p>
                    <p><strong>Contact Info:</strong> {user.contact_info}</p>
                    {/* ... other profile information ... */}
                    <button onClick={handleEdit}>Edit Profile</button>
                </div>
            )}
        </div>
    );
};

export default Profile;