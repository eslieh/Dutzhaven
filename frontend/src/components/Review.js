import React from 'react';
import StarRatings from 'react-star-ratings';

const Review = ({ review }) => {

  if (!review || !review.reviewer) { // Check if review or reviewer data is available
    return <p>Loading review...</p>; // Or a better loading indicator
  }

  return (
    <div className="review">
      <StarRatings
        rating={review.rating}
        starRatedColor="gold"
        numberOfStars={5}
        starDimension="20px"
        starSpacing="2px"
      />
      <p>{review.review_text}</p>
      <p>Reviewed by: {review.reviewer.username} </p> 
    </div>
  );
};

export default Review;