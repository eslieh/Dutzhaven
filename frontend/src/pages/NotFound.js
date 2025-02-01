import React from 'react';
import Navbar from '../components/Navbar'; // Import Navbar if you want it on the 404 page

const NotFound = () => {
  return (
    <div>
        <Navbar /> {/* Include the navbar */}
      <h1>404: Page Not Found</h1>
      <p>The page you are looking for does not exist.</p>
    </div>
  );
};

export default NotFound;