// import React, { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { useAuth } from '../context/AuthContext'; // Import your auth context
// import userService from '../services/userService';  // Import your user service

// const Profile = () => {
//   const { user, logout } = useAuth(); // Get user data and logout function
//   const [profileData, setProfileData] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);
//   const navigate = useNavigate();

//   useEffect(() => {
//     const fetchProfile = async () => {
//       try {
//         const data = await userService.getProfile(user._id); // Fetch profile data
//         setProfileData(data);
//       } catch (err) {
//         setError(err.message || 'Error fetching profile.');
//       } finally {
//         setLoading(false);
//       }
//     };

//     if (user) { // Only fetch if user data is available
//       fetchProfile();
//     } else {
//       setLoading(false); // If no user, just set loading to false
//     }
//   }, [user]); // Run when user data changes

//   const handleLogout = () => {
//     logout();
//     navigate('/login'); // Redirect to login after logout
//   };

//   if (loading) {
//     return <div>Loading profile...</div>;
//   }

//   if (error) {
//     return <div style={{ color: 'red' }}>{error}</div>;
//   }

//   if (!profileData) { // Handle the case where profileData is still null
//     return <div>No profile data available.</div>;
//   }

//   return (
//     <div>
//       <h1>Profile</h1>
//       {/* Display profile information */}
//       <p><strong>Full Name:</strong> {profileData.fullName}</p>
//       <p><strong>Username:</strong> {profileData.username}</p>
//       <p><strong>Email:</strong> {profileData.email}</p>
//       {/* ... other profile details */}
//       <button onClick={handleLogout}>Logout</button>
//     </div>
//   );
// };

// export default Profile;