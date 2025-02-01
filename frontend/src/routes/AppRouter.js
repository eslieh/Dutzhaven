import React from 'react'; // No need for useEffect or useNavigate
import { Routes, Route } from 'react-router-dom'; // No need for useNavigate
import Home from '../pages/Home';
import Tasks from '../pages/Tasks';
import TaskDetails from '../pages/TaskDetails';
import Profile from '../pages/Profile';
import Login from '../pages/Login';
import Register from '../pages/Register';
import ProtectedRoute from './ProtectedRoute';
import NotFound from '../pages/NotFound';

const AppRouter = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/tasks" element={<Tasks />} />
      <Route path="/tasks/:taskId" element={<TaskDetails />} />
      <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default AppRouter;