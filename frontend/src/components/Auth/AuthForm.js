import React, { useState } from 'react';
import { registerUser, loginUser } from '../../utils/api';

function AuthForm({ action }) {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    full_name: '',
    user_type: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (action === 'register') {
      registerUser(formData).then((response) => alert(response.data.message));
    } else {
      loginUser(formData).then((response) => alert(`Logged in! Token: ${response.data.user_id}`));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <h2>{action === 'register' ? 'Register' : 'Login'}</h2>
      {action === 'register' && (
        <input
          type="text"
          name="full_name"
          value={formData.full_name}
          onChange={handleChange}
          placeholder="Full Name"
        />
      )}
      <input
        type="text"
        name="username"
        value={formData.username}
        onChange={handleChange}
        placeholder="Username"
      />
      <input
        type="email"
        name="email"
        value={formData.email}
        onChange={handleChange}
        placeholder="Email"
      />
      <input
        type="password"
        name="password"
        value={formData.password}
        onChange={handleChange}
        placeholder="Password"
      />
      {action === 'register' && (
        <input
          type="text"
          name="user_type"
          value={formData.user_type}
          onChange={handleChange}
          placeholder="User Type"
        />
      )}
      <button type="submit">{action === 'register' ? 'Register' : 'Login'}</button>
    </form>
  );
}

export default AuthForm;
