// import React, { useState, useEffect, useContext } from 'react'; // Import useContext
// import Navbar from '../components/Navbar';
// import Message from '../components/Message';
// import messageService from '../services/messageService';
// import { AuthContext } from '../context/AuthContext'; // Import AuthContext

// const Messages = () => {
//   const [messages, setMessages] = useState([]);
//   const [newMessage, setNewMessage] = useState('');
//   const [error, setError] = useState(null);
//   const { user } = useContext(AuthContext); // Access user from context

//   useEffect(() => {
//     const fetchMessages = async () => {
//       try {
//         const data = await messageService.getMessages();
//         setMessages(data);
//       } catch (err) {
//         setError(err.message || 'Error fetching messages');
//       }
//     };

//     if (user) { // Only fetch messages if the user is logged in
//         fetchMessages();
//     }
//   }, [user]); // Add user to the dependency array

//   const handleSendMessage = async (e) => {
//     e.preventDefault();
//     if (!user) {
//         return; // Don't send if user is not logged in
//     }
//     try {
//       await messageService.sendMessage(user.id, newMessage); // Use user.id as receiver ID
//       setNewMessage('');
//       const updatedMessages = await messageService.getMessages();
//       setMessages(updatedMessages);
//     } catch (err) {
//       setError(err.message || 'Error sending message');
//     }
//   };

//   return (
//     <div>
//       <Navbar />
//       <h1>Messages</h1>
//       {error && <p style={{ color: 'red' }}>{error}</p>}
//       <div className="message-list">
//         {messages.map((message) => (
//           <Message key={message.id} message={message} />
//         ))}
//       </div>
//       <form onSubmit={handleSendMessage}>
//         <textarea value={newMessage} onChange={(e) => setNewMessage(e.target.value)} placeholder="Write a message..."></textarea>
//         <button type="submit">Send</button>
//       </form>
//     </div>
//   );
// };

// export default Messages;