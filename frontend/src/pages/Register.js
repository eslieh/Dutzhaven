import React from 'react';
import { Link } from 'react-router-dom';
import RegisterForm from '../components/RegisterForm';

const Register = () => {
  return (
    <div className="register-page">
      <h1>Register</h1>
      <RegisterForm />
      <div className="back-to-home"> {/* Wrap Link in a div */}
        <Link to="/">
          <p>Home page</p>
        </Link>
      </div>
    </div>
  );
};

export default Register;