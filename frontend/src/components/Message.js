import React, { useContext } from 'react';
import moment from 'moment';
import { AuthContext } from '../context/AuthContext';

const Message = ({ message }) => {
  const { user } = useContext(AuthContext);

  if (!user) {
    return null; // Or a loading indicator if user data is still being fetched
  }

  const isCurrentUser = message.sender_id === user.id; // Directly access user.id
  const messageClass = isCurrentUser ? 'message-sent' : 'message-received';

  return (
    <div className={`message ${messageClass}`}>
      <p>{message.message_text}</p>
      <span className="message-timestamp">{moment(message.timestamp).format('lll')}</span>
    </div>
  );
};

export default Message;