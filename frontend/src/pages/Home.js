import React from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

const Home = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/register');
  };

  return (
    <div className="home-container">
      <Navbar />  {/* Navbar will not be rendered here due to conditional rendering in App.js */}
      <div className="home-content">
        <h1>Welcome to DutzHaven</h1>
        <p>Get things done and earn rewards.</p>
        <div className="cta-buttons">
          <button className="get-started" onClick={handleGetStarted}>
            Get Started
          </button>
          <button className="learn-more">Learn More</button>
        </div>
      </div>

      <div className="featured-tasks">
        <h2>Featured Tasks</h2>
        {/* Add task cards or list here */}
      </div>

      <div className="testimonials">
        <h2>Testimonials</h2>
        {/* Add testimonials here */}
      </div>

      <footer>
        <p>&copy; {new Date().getFullYear()} DutzHaven</p>
      </footer>
    </div>
  );
};

export default Home;