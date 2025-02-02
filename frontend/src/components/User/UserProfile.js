import React, { useEffect, useState } from 'react';
import { getUser } from '../../utils/api';

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    getUser(userId).then((response) => setUser(response.data));
  }, [userId]);

  if (!user) return <p>Loading...</p>;

  return (
    <div className="user-profile">
      <h3>{user.username}</h3>
      <p>Email: {user.email}</p>
    </div>
  );
}

export default UserProfile;
