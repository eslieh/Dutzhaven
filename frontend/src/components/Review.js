import React from 'react';
import StarRatings from 'react-star-ratings'; // Install: npm install react-star-ratings

const Review = ({ review }) => {
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
      <p>Reviewed by: {review.reviewer.username} </p> {/* Assuming you have reviewer data */}
    </div>
  );
};

export default Review;