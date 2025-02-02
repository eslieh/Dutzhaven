import React, { useState } from 'react';
import { createTask } from '../../utils/api';

function TaskForm() {
  const [taskData, setTaskData] = useState({
    title: '',
    description: '',
    client_id: '',
    category: '',
    budget: '',
    deadline: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTaskData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    createTask(taskData).then((response) => alert(response.data.message));
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <h2>Create Task</h2>
      <input type="text" name="title" value={taskData.title} onChange={handleChange} placeholder="Task Title" />
      <textarea
        name="description"
        value={taskData.description}
        onChange={handleChange}
        placeholder="Task Description"
      />
      <input type="number" name="client_id" value={taskData.client_id} onChange={handleChange} placeholder="Client ID" />
      <input type="text" name="category" value={taskData.category} onChange={handleChange} placeholder="Category" />
      <input type="number" name="budget" value={taskData.budget} onChange={handleChange} placeholder="Budget" />
      <input type="date" name="deadline" value={taskData.deadline} onChange={handleChange} placeholder="Deadline" />
      <button type="submit">Create Task</button>
    </form>
  );
}

export default TaskForm;
