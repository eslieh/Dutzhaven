import React, { useState, useEffect, useContext } from 'react';
import Navbar from '../components/Navbar';
import Message from '../components/Message';
import messageService from '../services/messageService';
import { AuthContext } from '../context/AuthContext';

const Messages = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true); // Add loading state
  const { user } = useContext(AuthContext);

  useEffect(() => {
    const fetchMessages = async () => {
      setLoading(true); // Set loading to true before fetching
      setError(null);   // Clear any previous errors
      try {
        const data = await messageService.getMessages();
        setMessages(data);
      } catch (err) {
        setError(err.message || 'Error fetching messages');
        console.error("Message fetch error:", err); // Log error for debugging
      } finally {
        setLoading(false); // Set loading to false after fetch (whether success or fail)
      }
    };

    if (user) {
      fetchMessages();
    } else {
      setLoading(false); // If no user, just set loading to false
    }
  }, [user]);

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!user) {
      return; // Don't send if user is not logged in
    }

    setError(null); // Clear any previous errors
    setLoading(true); // Set loading to true before sending

    try {
      await messageService.sendMessage(user.id, newMessage);
      setNewMessage(''); // Clear the input field

      // Optimistic update (add the message immediately to the UI)
      setMessages([...messages, { 
        message_text: newMessage, 
        sender_id: user.id, 
        timestamp: new Date().toISOString(), // Add a timestamp (or get it from the server response)
        sender: { username: user.username} // If you have user details
       }]);

      // You might want to fetch updated messages from the server after sending
      // const updatedMessages = await messageService.getMessages();
      // setMessages(updatedMessages);

    } catch (err) {
      setError(err.message || 'Error sending message');
      console.error("Message send error:", err); // Log the error
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading messages...</div>; // Display loading message
  }

  if (error) {
    return <div style={{ color: 'red' }}>{error}</div>;
  }

  return (
    <div>
      <Navbar />
      <h1>Messages</h1>
      <div className="message-list">
        {messages.map((message) => (
          <Message key={message._id || message.id} message={message} /> // Use _id or id
        ))}
      </div>
      <form onSubmit={handleSendMessage}>
        <textarea 
          value={newMessage} 
          onChange={(e) => setNewMessage(e.target.value)} 
          placeholder="Write a message..." 
          required // Make the textarea required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Sending...' : 'Send'} {/* Show sending message */}
        </button>
      </form>
    </div>
  );
};

export default Messages;