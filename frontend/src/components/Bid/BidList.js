import React, { useEffect, useState } from 'react';
import { getBid } from '../../utils/api';

function BidList() {
  const [bids, setBids] = useState([]);
  
  useEffect(() => {
    // Fetching all bids - assuming you have an endpoint for this or you can fetch multiple bids
    const fetchBids = async () => {
      try {
        const response = await getBid(); // Modify if you need an API to fetch multiple bids
        setBids(response.data); 
      } catch (error) {
        console.error("Error fetching bids", error);
      }
    };
    fetchBids();
  }, []);

  return (
    <div className="bid-list">
      <h2>Bids</h2>
      <ul>
        {bids.map((bid) => (
          <li key={bid.id}>
            <p>Task ID: {bid.task_id}</p>
            <p>Freelancer ID: {bid.freelancer_id}</p>
            <p>Proposal: {bid.proposal_text}</p>
            <p>Price: ${bid.price}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default BidList;
