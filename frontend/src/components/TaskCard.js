import React from 'react';
import { Link } from 'react-router-dom';

const TaskCard = ({ task }) => {

  if (!task) { // Check if task data is available
    return <p>Loading task...</p>; // Or a better loading indicator
  }

  return (
    <div className="task-card">
      <h3>{task.title}</h3>
      <p>{task.description}</p>
      <Link to={`/tasks/${task._id || task.id}`}>View Details</Link> {/* Use task._id if available, fallback to task.id */}
    </div>
  );
};

export default TaskCard;