import axios from 'axios';

const API_URL = 'http://localhost:5000'; // Change this based on your Flask server URL

// Auth
export const registerUser = (data) => axios.post(`${API_URL}/auth/register`, data);
export const loginUser = (data) => axios.post(`${API_URL}/auth/login`, data);

// User
export const getUser = (userId) => axios.get(`${API_URL}/users/${userId}`);
export const createUser = (data) => axios.post(`${API_URL}/users`, data);

// Task
export const getTask = (taskId) => axios.get(`${API_URL}/tasks/${taskId}`);
export const createTask = (data) => axios.post(`${API_URL}/tasks`, data);

// Bid
export const getBid = (bidId) => axios.get(`${API_URL}/bids/${bidId}`);
export const createBid = (data) => axios.post(`${API_URL}/bids`, data);
