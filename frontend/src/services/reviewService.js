const API_URL = '/api/reviews';

const getReviews = async (taskId, userId) => {
    try {
        let url = API_URL;
        if (taskId) {
            url += `/task/${taskId}`;
        } else if (userId) {
            url += `/user/${userId}`;
        }

        const response = await fetch(url);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to fetch reviews');
        }

        return await response.json();
    } catch (error) {
        console.error("Error fetching reviews:", error); // Log the error
        throw error; // Re-throw for component handling
    }
};

const createReview = async (taskId, rating, reviewText) => {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_URL}/create/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ rating, review_text: reviewText }), // Corrected key name
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to create review');
        }

        return await response.json();

    } catch (error) {
        console.error("Error creating review:", error); // Log the error
        throw error; // Re-throw for component handling
    }
};

const reviewService = {
    getReviews,
    createReview,
};

export default reviewService;