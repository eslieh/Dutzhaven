import React, { useEffect, useState } from 'react';
import { getTask } from '../../utils/api';

function TaskList() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    // Fetching all tasks - assuming you have an endpoint for this or you can fetch multiple tasks
    const fetchTasks = async () => {
      try {
        const response = await getTask(); // Modify if you need an API to fetch multiple tasks
        setTasks(response.data);
      } catch (error) {
        console.error("Error fetching tasks", error);
      }
    };
    fetchTasks();
  }, []);

  return (
    <div className="task-list">
      <h2>Tasks</h2>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <p>Title: {task.title}</p>
            <p>Description: {task.description}</p>
            <p>Status: {task.status}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TaskList;
