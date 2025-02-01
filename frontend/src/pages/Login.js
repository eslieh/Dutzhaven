import React from 'react';
import { Link } from 'react-router-dom';
import LoginForm from '../components/LoginForm';

const Login = () => {
  return (
    <div className="login-page">
      <h1>Login</h1>
      <LoginForm />
      <div className="back-to-home"> {/* Wrap the Link in a div for better styling control */}
        <Link to="/">
          <p>Home Page</p>
        </Link>
      </div>
    </div>
  );
};

export default Login;