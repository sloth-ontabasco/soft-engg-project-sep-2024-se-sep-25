import { header } from './auth';

const BASE_URL = import.meta.env.VITE_SERVER_BASE_URL;

export async function getAnnouncements(projectId) {
    console.log("Fetching from URL: ", `${BASE_URL}/projects/${projectId}/announcements`);
    const res = await fetch(`${BASE_URL}/projects/${projectId}/announcements`, {
        method: "GET",
        headers: header(),
    });

    if (res.status === 200) {
        const data = await res.json();
        console.log(`Found ${data.announcements.length} announcements:`);
        return data.announcements;
    }

    throw new Error("Failed to fetch projects");
}

export async function deleteAnnouncement(projectId, announcementId) {
    const res = await fetch(`${BASE_URL}/projects/${projectId}/announcements/${announcementId}`, {
        method: "DELETE",
        headers: header(),
    });

    if (res.status !== 200) {
        throw new Error("Failed to delete announcement");
    }
}

export async function createAnnouncement(projectId, announcement) {
    const res = await fetch(`${BASE_URL}/projects/${projectId}/announcements`, {
        method: "POST",
        headers: {
            ...header(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(announcement)
    });

    if (res.status === 201) {
        return await res.json();
    }

    throw new Error("Failed to create announcement");
}

export async function updateAnnouncement(projectId, announcementId, announcement) {
    const res = await fetch(`${BASE_URL}/projects/${projectId}/announcements/${announcementId}`, {
        method: "PUT",
        headers: {
            ...header(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(announcement)
    });

    if (res.status === 200) {
        return await res.json();
    }

    throw new Error("Failed to update announcement");
}