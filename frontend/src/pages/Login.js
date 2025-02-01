import React from 'react';
import { Link } from 'react-router-dom'; // Import Link
import LoginForm from '../components/LoginForm';

const Login = () => {
  return (
    <div className="login-page"> {/* Add a class for styling the page */}
      <h1>Login</h1>
      <LoginForm />
      <Link to="/" className="back-to-home"> {/* Add class to Link */}
        <p>Back Home</p>
      </Link>
    </div>
  );
};

export default Login;