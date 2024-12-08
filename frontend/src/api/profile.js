import axios from 'axios';

/**
 * Fetch upcoming milestones for a specific user.
 * @param {string} userId - The ID of the user.
 * @returns {Promise<Object[]>} List of milestones.
 */
export const getMilestonesByUser = async (userId) => {
  try {
    const response = await axios.get(`/api/projects/user/${userId}`);
    return response.data.data; // Adjusted based on backend response structure
  } catch (error) {
    console.error("Error fetching milestones:", error);
    throw error;
  }
};
