import React from 'react';
import { Link } from 'react-router-dom';
import RegisterForm from '../components/RegisterForm';

const Register = () => {
  return (
    <div className="register-page">
      <h1>Register</h1>
      <RegisterForm />
      <Link to="/" className="back-to-home">
        <p>Back Home</p>
      </Link>
    </div>
  );
};

export default Register;