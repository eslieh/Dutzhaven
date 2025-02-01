// // Navbar.js
// import React from 'react';
// import { Link, useNavigate, useLocation } from 'react-router-dom'; // Import useLocation
// import { useAuth } from '../context/AuthContext';

// const Navbar = () => {
//     const { isAuthenticated, logout } = useAuth();
//     const navigate = useNavigate();
//     const location = useLocation(); // Get current location

//     const handleLogout = () => {
//         logout();
//         navigate('/');
//     };

//     // Conditionally render links based on authentication and route
//     const renderAuthLinks = () => {
//       if (location.pathname === '/') { // Check if it's the home page
//         return null; // Don't render any auth links on home
//       } else if (isAuthenticated) {
//         return (
//           <>
//             <Link to="/profile">Profile</Link>
//             <button onClick={handleLogout}>Logout</button>
//           </>
//         );
//       } else {
//         return (
//           <>
//             <Link to="/login">Login</Link>
//             <Link to="/register">Register</Link>
//           </>
//         );
//       }
//     };

//     return (
//         <nav>
//             <Link to="/" className="logo">TaskHaven</Link>
//             <div>
//               {renderAuthLinks()} {/* Call the function to render links */}
//             </div>
//         </nav>
//     );
// };

// export default Navbar;