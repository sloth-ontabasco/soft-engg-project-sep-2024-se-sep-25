import { header } from './auth';

const BASE_URL = import.meta.env.VITE_SERVER_BASE_URL;

export async function getFeedbacks(projectId, milestoneId, teamId) {
    console.log("Fetching from URL: ", `${BASE_URL}/projects/${projectId}/milestones/${milestoneId}/teams/${teamId}/feedbacks`);
    const res = await fetch(`${BASE_URL}/projects/${projectId}/milestones/${milestoneId}/teams/${teamId}/feedbacks`, {
        method: "GET",
        headers: header(),
    });

    if (res.status === 200) {
        const data = await res.json();
        console.log(`Found ${data.feedbacks.length} feedbacks:`);
        return data.feedbacks;
    }

    throw new Error("Failed to fetch feedbacks");
}

export async function deleteFeedback(projectId, milestoneId, teamId, feedbackId) {
    const res = await fetch(`${BASE_URL}/projects/${projectId}/milestones/${milestoneId}/teams/${teamId}/feedbacks/${feedbackId}`, {
        method: "DELETE",
        headers: header(),
    });

    if (res.status !== 200) {
        throw new Error("Failed to delete feedback");
    }
}

export async function createFeedback(projectId, milestoneId, teamId, feedback) {
    const res = await fetch(`${BASE_URL}/projects/${projectId}/milestones/${milestoneId}/teams/${teamId}/feedbacks`, {
        method: "POST",
        headers: {
            ...header(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(feedback)
    });

    if (res.status === 201) {
        return await res.json();
    }

    throw new Error("Failed to create feedback");
}

export async function updateFeedback(projectId, milestoneId, teamId, feedbackId, feedback) {
    const res = await fetch(`${BASE_URL}/projects/${projectId}/milestones/${milestoneId}/teams/${teamId}/feedbacks/${feedbackId}`, {
        method: "PUT",
        headers: {
            ...header(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(feedback)
    });

    if (res.status === 200) {
        return await res.json();
    }

    throw new Error("Failed to update feedback");
}
