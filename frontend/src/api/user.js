import { header } from './auth';

const BASE_URL = import.meta.env.VITE_SERVER_BASE_URL;

/**
 * Fetch all users.
 */
export async function getUsers() {
    const res = await fetch(`${BASE_URL}/users`, {
        method: "GET",
        headers: header(),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to fetch users");
}

/**
 * Fetch a specific user by ID.
 * @param {string} userId - The ID of the user to fetch.
 */
export async function getUserById(userId) {
    const res = await fetch(`${BASE_URL}/users/${userId}`, {
        method: "GET",
        headers: header(),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error(`Failed to fetch user with ID: ${userId}`);
}

/**
 * Update user details.
 * @param {string} userId - The ID of the user to update.
 * @param {Object} userData - The data to update (e.g., username, github_id).
 */
export async function updateUser(userId, userData) {
    const res = await fetch(`${BASE_URL}/users/${userId}`, {
        method: "PUT",
        headers: {
            ...header(),
            "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error(`Failed to update user with ID: ${userId}`);
}

/**
 * Delete a user by ID.
 * @param {string} userId - The ID of the user to delete.
 */
export async function deleteUser(userId) {
    const res = await fetch(`${BASE_URL}/users/${userId}`, {
        method: "DELETE",
        headers: header(),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error(`Failed to delete user with ID: ${userId}`);
}