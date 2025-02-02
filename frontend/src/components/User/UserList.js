import React, { useEffect, useState } from 'react';
import { getUser } from '../../utils/api';

function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    // Fetching all users - assuming you have an endpoint for this or you can fetch multiple users
    const fetchUsers = async () => {
      try {
        const response = await getUser(); // Modify if you need an API to fetch multiple users
        setUsers(response.data);
      } catch (error) {
        console.error("Error fetching users", error);
      }
    };
    fetchUsers();
  }, []);

  return (
    <div className="user-list">
      <h2>Users</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            <p>Username: {user.username}</p>
            <p>Email: {user.email}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;
