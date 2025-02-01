import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import taskService from '../services/taskService';

const TaskDetails = () => {
  const { taskId } = useParams();
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTask = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await taskService.getTask(taskId);
        setTask(data);
      } catch (err) {
        setError(err.message || 'Error fetching task details');
        console.error("Task details fetch error:", err); // Log error for debugging
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [taskId]);

  if (loading) {
    return <div>Loading task details...</div>; // Or a better loading indicator
  }

  if (error) {
    return <div style={{ color: 'red' }}>{error}</div>;
  }

  if (!task) {
    return <div>Task not found.</div>;
  }

  return (
    <div>
      <Navbar />
      <h1>{task.title}</h1>
      <p>{task.description}</p>
      {/* ... other task details ... */}
      {/* Example: Displaying other details */}
      {task.due_date && <p>Due Date: {task.due_date}</p>} {/* Conditional rendering */}
      {task.status && <p>Status: {task.status}</p>}         {/* Conditional rendering */}
      {/* ... more details as needed */}
    </div>
  );
};

export default TaskDetails;