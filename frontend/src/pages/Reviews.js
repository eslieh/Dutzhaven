import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import Review from '../components/Review';
import reviewService from '../services/reviewService';

const Reviews = ({ taskId, userId }) => {
    const [reviews, setReviews] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true); // Add loading state

    useEffect(() => {
        const fetchReviews = async () => {
            setLoading(true); // Set loading to true before fetching
            setError(null); // Clear any previous errors

            try {
                const data = await reviewService.getReviews(taskId, userId);
                setReviews(data);
            } catch (err) {
                setError(err.message || 'Error fetching reviews');
                console.error("Review fetch error:", err);  // Log error for debugging
            } finally {
                setLoading(false); // Set loading to false after fetch
            }
        };

        fetchReviews(); // Call fetchReviews only once

    }, [taskId, userId]); // Add both taskId and userId to dependency array

    if (loading) {
        return <div>Loading reviews...</div>; // Or a better loading indicator
    }

    if (error) {
        return <div style={{ color: 'red' }}>{error}</div>;
    }

    return (
        <div>
            <Navbar />
            <h1>Reviews</h1>
            <div className="review-list">
                {reviews.map((review) => (
                    <Review key={review._id || review.id} review={review} /> // Use _id or id for the key
                ))}
            </div>
        </div>
    );
};

export default Reviews;