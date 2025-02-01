// const API_URL = '/api/reviews';

// const getReviews = async (taskId, userId) => {
//     try {
//         let url = API_URL;
//         if (taskId) {
//             url += `/task/${taskId}`;
//         } else if (userId) {
//             url += `/user/${userId}`;
//         }

//         const response = await fetch(url);
//         if (!response.ok) {
//             const errorData = await response.json();
//             throw new Error(errorData.message || 'Failed to fetch reviews');
//         }

//         return await response.json();
//     } catch (error) {
//         throw error;
//     }
// };

// const createReview = async (taskId, rating, reviewText) => {
//     try {
//         const token = localStorage.getItem('token');
//         const response = await fetch(`${API_URL}/create/${taskId}`, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 Authorization: `Bearer ${token}`,
//             },
//             body: JSON.stringify({ rating, reviewText }),
//         });

//         if (!response.ok) {
//             const errorData = await response.json();
//             throw new Error(errorData.message || 'Failed to create review');
//         }

//         return await response.json();

//     } catch (error) {
//         throw error;
//     }
// };

// const reviewService = {  // Assign to a variable
//     getReviews,
//     createReview,
// };

// export default reviewService; // Export the variable