// import React, { useState, useEffect } from 'react';
// import { useParams } from 'react-router-dom'; // For getting URL params
// import Navbar from '../components/Navbar';
// import taskService from '../services/taskService';

// const TaskDetails = () => {
//   const { taskId } = useParams(); // Get the task ID from the URL
//   const [task, setTask] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     const fetchTask = async () => {
//       try {
//         const data = await taskService.getTask(taskId);
//         setTask(data);
//       } catch (err) {
//         setError(err.message || 'Error fetching task details');
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchTask();
//   }, [taskId]); // Add taskId to dependency array


//   if (loading) {
//     return <div>Loading task details...</div>;
//   }

//   if (error) {
//     return <div>Error: {error}</div>;
//   }

//   if (!task) {
//       return <div>Task not found.</div>
//   }

//   return (
//     <div>
//       <Navbar />
//       <h1>{task.title}</h1>
//       <p>{task.description}</p>
//       {/* ... other task details ... */}
//     </div>
//   );
// };

// export default TaskDetails;