import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import AppRouter from './routes/AppRouter'; // Correct path
import { AuthProvider } from './context/AuthContext'; // Correct path
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <AppRouter />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;