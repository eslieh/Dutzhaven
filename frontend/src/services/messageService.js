// const API_URL = '/api/messages';

// const getMessages = async () => {
//     try {
//         const token = localStorage.getItem('token');
//         const response = await fetch(API_URL, {
//             headers: {
//                 Authorization: `Bearer ${token}`,
//             },
//         });
//         if (!response.ok) {
//             const errorData = await response.json();
//             throw new Error(errorData.message || 'Failed to fetch messages');
//         }
//         return await response.json();
//     } catch (error) {
//         throw error;
//     }
// };

// const sendMessage = async (receiverId, messageText) => {
//     try {
//         const token = localStorage.getItem('token');
//         const response = await fetch(`${API_URL}/send/${receiverId}`, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 Authorization: `Bearer ${token}`,
//             },
//             body: JSON.stringify({ message_text }),
//         });

//         if (!response.ok) {
//             const errorData = await response.json();
//             throw new Error(errorData.message || 'Failed to send message');
//         }

//         return await response.json();
//     } catch (error) {
//         throw error;
//     }
// };

// const messageService = { // Assign the object to a variable
//     getMessages,
//     sendMessage,
// };

// export default messageService; // Export the variable