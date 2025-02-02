const API_URL = '/http://127.0.0.1:5000/auth';

const register = async (fullName, username, email, password) => {
  try {
    const user_type = "client";
    const full_name = fullName;
    const response = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ full_name,username, email, password, user_type }),
    });

    if (!response.ok) {
      const errorData = await response.json(); // Parse error details
      throw new Error(errorData.message || 'Registration failed'); // Throw error
    }

    return await response.json(); // Return data on success
  } catch (error) {
    console.error("Registration error:", error); // Log for debugging
    throw error; // Re-throw for the component to handle
  }
};

const login = async (username, password) => {
  try {
    const response = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Login failed');
    }

    const data = await response.json();

    if (data.access_token) {
      localStorage.setItem('token', data.access_token);
    }

    return data;
  } catch (error) {
    console.error("Login error:", error); // Log for debugging
    throw error; // Re-throw for the component to handle
  }
};

const logout = () => {
  localStorage.removeItem('token');
};

const isAuthenticated = () => {
  const token = localStorage.getItem('token');
  return !!token;
};

const authService = {
  register,
  login,
  logout,
  isAuthenticated,
};

export default authService;