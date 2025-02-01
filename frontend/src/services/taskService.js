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
    console.error("Error fetching tasks:", error); // Log the error
    throw error; // Re-throw for component handling
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
    console.error("Error fetching task details:", error); // Log the error
    throw error; // Re-throw for component handling
  }
};

// ... other task-related services (create, update, delete)

const taskService = {
  getTasks,
  getTask,
  // ... other functions
};

export default taskService;