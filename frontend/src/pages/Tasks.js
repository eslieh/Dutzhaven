import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import taskService from '../services/taskService';
import TaskCard from '../components/TaskCard';

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true); // Set loading to true *before* fetching
      setError(null);   // Clear previous errors

      try {
        const data = await taskService.getTasks();
        setTasks(data);
      } catch (err) {
        setError(err.message || 'Error fetching tasks');
        console.error("Task fetch error:", err); // Log error for debugging
      } finally {
        setLoading(false); // Set loading to false in finally block
      }
    };

    fetchTasks();
  }, []);

  if (loading) {
    return <div>Loading tasks...</div>; // Or a better loading indicator
  }

  if (error) {
    return <div style={{ color: 'red' }}>{error}</div>;
  }

  return (
    <div>
      <Navbar />
      <h1>Tasks</h1>
      <div className="task-list">
        {tasks.map((task) => (
          <TaskCard key={task._id || task.id} task={task} /> // Use _id or id for key
        ))}
      </div>
    </div>
  );
};

export default Tasks;