import { header } from './auth';

const BASE_URL = import.meta.env.VITE_SERVER_BASE_URL;

/**
 * Fetch all milestones for a specific project.
 * @param {string} projectId - The ID of the project.
 * @returns {Promise<Object[]>} A promise that resolves to an array of milestones.
 */
export async function getProjectMilestones(projectId) {
    const res = await fetch(`${BASE_URL}/api/project/milestones/${projectId}`, {
        method: "GET",
        headers: header(),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to fetch project milestones");
}

/**
 * Fetch a specific milestone by its ID.
 * @param {string} milestoneId - The ID of the milestone.
 * @returns {Promise<Object>} A promise that resolves to the milestone object.
 */
export async function getMilestone(milestoneId) {
    const res = await fetch(`${BASE_URL}/api/milestones/${milestoneId}`, {
        method: "GET",
        headers: header(),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to fetch milestone");
}

/**
 * Create a new milestone for a project.
 * @param {string} projectId - The ID of the project.
 * @param {Object} milestoneData - The data for the new milestone (title, description, due_date).
 * @returns {Promise<Object>} A promise that resolves to the newly created milestone object.
 */
export async function createMilestone(projectId, milestoneData) {
    const res = await fetch(`${BASE_URL}/api/project/milestones/${projectId}`, {
        method: "POST",
        headers: {
            ...header(),
            "Content-Type": "application/json",
        },
        body: JSON.stringify(milestoneData),
    });

    if (res.status === 201 || res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to create milestone");
}

/**
 * Update an existing milestone.
 * @param {string} projectId - The ID of the project.
 * @param {string} milestoneId - The ID of the milestone to update.
 * @param {Object} milestoneData - The updated milestone data.
 * @returns {Promise<Object>} A promise that resolves to the updated milestone object.
 */
export async function updateMilestone(projectId, milestoneId, milestoneData) {
    const res = await fetch(`${BASE_URL}/api/milestones/${projectId}/${milestoneId}`, {
        method: "PUT",
        headers: {
            ...header(),
            "Content-Type": "application/json",
        },
        body: JSON.stringify(milestoneData),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to update milestone");
}

/**
 * Delete a milestone.
 * @param {string} projectId - The ID of the project.
 * @param {string} milestoneId - The ID of the milestone to delete.
 * @returns {Promise<void>} A promise that resolves when the milestone is deleted.
 */
export async function deleteMilestone(projectId, milestoneId) {
    const res = await fetch(`${BASE_URL}/api/milestones/${projectId}/${milestoneId}`, {
        method: "DELETE",
        headers: header(),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to delete milestone");
}

/**
 * Fetch milestones submitted by a specific user (optional based on requirements).
 * @param {string} userId - The ID of the user.
 * @returns {Promise<Object[]>} A promise that resolves to an array of milestones.
 */
export async function getMilestonesByUser(userId) {
    const res = await fetch(`${BASE_URL}/api/milestones/user/${userId}`, {
        method: "GET",
        headers: header(),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to fetch milestones for user");
}
