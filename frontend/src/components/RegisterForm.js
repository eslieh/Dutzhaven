// import React, { useState } from 'react';
// import { useNavigate, Link } from 'react-router-dom';
// import authService from '../services/authService'; // Import your auth service

// const RegisterForm = () => {
//   const [fullName, setFullName] = useState('');
//   const [username, setUsername] = useState('');
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   const [confirmPassword, setConfirmPassword] = useState('');
//   const [error, setError] = useState('');
//   const navigate = useNavigate();

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setError('');

//     if (password !== confirmPassword) {
//       setError('Passwords do not match.');
//       return;
//     }

//     try {
//       await authService.register(fullName, username, email, password); // Call the register function
//       navigate('/login'); // Redirect to login after successful registration
//     } catch (err) {
//       setError(err.message || 'Registration failed. Please try again.');
//     }
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       {error && <p style={{ color: 'red' }}>{error}</p>}
//       <label htmlFor="fullName">Full Name:</label>
//       <input
//         type="text"
//         id="fullName"
//         value={fullName}
//         onChange={(e) => setFullName(e.target.value)}
//         required
//       />
//       <label htmlFor="username">Username:</label>
//       <input
//         type="text"
//         id="username"
//         value={username}
//         onChange={(e) => setUsername(e.target.value)}
//         required
//       />
//       <label htmlFor="email">Email:</label>
//       <input
//         type="email"
//         id="email"
//         value={email}
//         onChange={(e) => setEmail(e.target.value)}
//         required
//       />
//       <label htmlFor="password">Password:</label>
//       <input
//         type="password"
//         id="password"
//         value={password}
//         onChange={(e) => setPassword(e.target.value)}
//         required
//       />
//       <label htmlFor="confirmPassword">Confirm Password:</label>
//       <input
//         type="password"
//         id="confirmPassword"
//         value={confirmPassword}
//         onChange={(e) => setConfirmPassword(e.target.value)}
//         required
//       />
//       <button type="submit">Sign Up</button>
//       <p className="register-link">
//         Already have an account? <Link to="/login">Login here</Link>
//       </p>
//     </form>
//   );
// };

// export default RegisterForm;