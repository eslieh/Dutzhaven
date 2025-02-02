import React, { useState } from 'react';
import { createBid } from '../../utils/api';

function BidForm() {
  const [bidData, setBidData] = useState({
    task_id: '',
    freelancer_id: '',
    proposal_text: '',
    price: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setBidData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    createBid(bidData).then((response) => alert(response.data.message));
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <h2>Create Bid</h2>
      <input
        type="number"
        name="task_id"
        value={bidData.task_id}
        onChange={handleChange}
        placeholder="Task ID"
      />
      <input
        type="number"
        name="freelancer_id"
        value={bidData.freelancer_id}
        onChange={handleChange}
        placeholder="Freelancer ID"
      />
      <textarea
        name="proposal_text"
        value={bidData.proposal_text}
        onChange={handleChange}
        placeholder="Proposal Text"
      />
      <input
        type="number"
        name="price"
        value={bidData.price}
        onChange={handleChange}
        placeholder="Price"
      />
      <button type="submit">Create Bid</button>
    </form>
  );
}

export default BidForm;
