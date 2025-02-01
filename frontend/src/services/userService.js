// const API_URL = '/api/users';

// const getProfile = async () => {
//   try {
//     const token = localStorage.getItem('token');
//     const response = await fetch(`${API_URL}/profile`, {
//       headers: {
//         Authorization: `Bearer ${token}`,
//       },
//     });
//     if (!response.ok) {
//       const errorData = await response.json();
//       throw new Error(errorData.message || 'Failed to fetch profile');
//     }
//     return await response.json();
//   } catch (error) {
//     throw error;
//   }
// };

// const updateProfile = async (updatedUser) => {
//   try {
//     const token = localStorage.getItem('token');
//     const response = await fetch(`${API_URL}/profile`, {
//       method: 'PUT',
//       headers: {
//         'Content-Type': 'application/json',
//         Authorization: `Bearer ${token}`,
//       },
//       body: JSON.stringify(updatedUser),
//     });

//     if (!response.ok) {
//       const errorData = await response.json();
//       throw new Error(errorData.message || 'Failed to update profile');
//     }

//     return await response.json();
//   } catch (error) {
//     throw error;
//   }
// };

// const userService = { // Assign to a variable
//   getProfile,
//   updateProfile,
// };

// export default userService; // Export the variable