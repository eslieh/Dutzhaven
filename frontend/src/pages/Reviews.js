// import React, { useState, useEffect } from 'react';
// import Navbar from '../components/Navbar';
// import Review from '../components/Review';
// import reviewService from '../services/reviewService';

// const Reviews = ({ taskId, userId }) => { // Receive taskId or userId as props
//     const [reviews, setReviews] = useState([]);
//     const [error, setError] = useState(null);

//     useEffect(() => {
//         const fetchReviews = async () => {
//             try {
//                 const data = await reviewService.getReviews(taskId, userId); // Pass both if needed
//                 setReviews(data);
//             } catch (err) {
//                 setError(err.message || 'Error fetching reviews');
//             }
//         };
//         fetchReviews();
//     }, [taskId, userId]);

//     return (
//         <div>
//             <Navbar />
//             <h1>Reviews</h1>
//             {error && <p style={{ color: 'red' }}>{error}</p>}
//             <div className="review-list">
//                 {reviews.map((review) => (
//                     <Review key={review.id} review={review} />
//                 ))}
//             </div>
//         </div>
//     );
// };

// export default Reviews;