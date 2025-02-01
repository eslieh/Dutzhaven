// import React, { useState, useEffect } from 'react';
// import Navbar from '../components/Navbar';
// import { useAuth } from '../context/AuthContext';
// import userService from '../services/userService'; // Import user service

// const Profile = () => {
//     const { isAuthenticated } = useAuth();
//     const [user, setUser] = useState(null);
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);
//     const [editing, setEditing] = useState(false); // Track editing state
//     const [updatedUser, setUpdatedUser] = useState({}); // Store updated user data

//     useEffect(() => {
//         const fetchProfile = async () => {
//             try {
//                 const userData = await userService.getProfile();
//                 setUser(userData);
//                 setUpdatedUser(userData); // Initialize updatedUser with current data
//             } catch (err) {
//                 setError(err.message || 'Error fetching profile');
//             } finally {
//                 setLoading(false);
//             }
//         };

//         if (isAuthenticated) { // Only fetch if authenticated
//             fetchProfile();
//         }
//     }, [isAuthenticated]);

//     const handleEdit = () => {
//         setEditing(true);
//     };

//     const handleInputChange = (e) => {
//         setUpdatedUser({ ...updatedUser, [e.target.name]: e.target.value });
//     };

//     const handleSave = async () => {
//         try {
//             await userService.updateProfile(updatedUser);
//             setUser(updatedUser); // Update the displayed profile
//             setEditing(false);
//         } catch (err) {
//             setError(err.message || 'Error updating profile');
//         }
//     };

//     if (!isAuthenticated) {
//         return <div>Please login to view your profile.</div>; // Or redirect
//     }

//     if (loading) {
//         return <div>Loading profile...</div>;
//     }

//     if (error) {
//         return <div>Error: {error}</div>;
//     }

//     if (!user) {
//         return <div>User profile not found.</div>; // Handle if user data is null
//     }

//     return (
//         <div>
//             <Navbar />
//             <h1>Profile</h1>

//             {editing ? (
//                 <form>
//                     <input type="text" name="bio" value={updatedUser.bio || ''} onChange={handleInputChange} placeholder="Bio" />
//                     <input type="text" name="contact_info" value={updatedUser.contact_info || ''} onChange={handleInputChange} placeholder="Contact Info" />
//                     {/* ... other editable fields ... */}
//                     <button type="button" onClick={handleSave}>Save</button>
//                     <button type="button" onClick={() => setEditing(false)}>Cancel</button>
//                 </form>
//             ) : (
//                 <div>
//                     <p><strong>Username:</strong> {user.username}</p>
//                     <p><strong>Email:</strong> {user.email}</p>
//                     <p><strong>Bio:</strong> {user.bio}</p>
//                     <p><strong>Contact Info:</strong> {user.contact_info}</p>
//                     {/* ... other profile information ... */}
//                     <button onClick={handleEdit}>Edit Profile</button>
//                 </div>
//             )}
//         </div>
//     );
// };

// export default Profile;