import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AuthForm from './components/Auth/AuthForm';
import UserProfile from './components/User/UserProfile';
import TaskForm from './components/Task/TaskForm';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/auth/register" element={ <AuthForm action="register" />} />
          <Route path="/auth/login" element={<AuthForm action="login" />} />
          <Route path="/user/:id" element={(props) => <UserProfile userId={props.match.params.id} />} />
          <Route path="/task/create" element={<TaskForm/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
