const API_URL = '/api/tasks';

const getTasks = async () => {
  try {
    const response = await fetch(API_URL);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch tasks');
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
};

const getTask = async (taskId) => {
  try {
    const response = await fetch(`${API_URL}/${taskId}`);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch task details');
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
};

// ... other task-related services (create, update, delete)

const taskService = { // Changed here: Assign to a variable
  getTasks,
  getTask,
};

export default taskService; // Changed here: Export the variable