import axios from 'axios';

export const getProjectsByUser = async (userId) => {
  try {
    const token = localStorage.getItem('token'); // Assuming JWT is stored in localStorage
    const response = await axios.get('/api/milestones', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params: {
        github_id: userId, // Ensure the backend is configured to accept this
      },
    });
    return response.data.data; // Assuming the API response format { data: milestones }
  } catch (error) {
    console.error('Error fetching milestones:', error);
    throw error;
  }
};
