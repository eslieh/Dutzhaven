import React from 'react';
import { Link } from 'react-router-dom'; // Import Link

const NotFound = () => {
  return (
    <div className="not-found-page"> {/* Add a class for styling */}
      <h1>404: Page Not Found</h1>
      <p>The page you are looking for does not exist.</p>
      <Link to="/"> {/* Add a "Go Home" link */}
        <p>Home</p>
      </Link>
    </div>
  );
};

export default NotFound;