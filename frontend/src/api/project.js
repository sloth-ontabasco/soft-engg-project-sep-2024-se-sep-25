import { header } from './auth';

const BASE_URL = import.meta.env.VITE_SERVER_BASE_URL;

export async function getProjects() {
    const res = await fetch(`${BASE_URL}/project`, {
        method: "GET",
        headers: header(),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to fetch projects");
}

export async function getProjectById(projectId) {
    const res = await fetch(`${BASE_URL}/project/${projectId}`, {
        method: "GET",
        headers: header(),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to fetch project");
}

export async function createProject(projectData) {
    const res = await fetch(`${BASE_URL}/project`, {
        method: "POST",
        headers: {
            ...header(),
            "Content-Type": "application/json",
        },
        body: JSON.stringify(projectData),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to create project");
}

export async function updateProject(projectId, projectData) {
    const res = await fetch(`${BASE_URL}/project/${projectId}`, {
        method: "PUT",
        headers: {
            ...header(),
            "Content-Type": "application/json",
        },
        body: JSON.stringify(projectData),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to update project");
}

export async function deleteProject(projectId) {
    const res = await fetch(`${BASE_URL}/project/${projectId}`, {
        method: "DELETE",
        headers: header(),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to delete project");
}

export async function getProjectsByUser(userId) {
    const res = await fetch(`${BASE_URL}/project/user/${userId}`, {
        method: 'GET',
        headers: header(),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to fetch projects for user");
}

export async function getProjectsByStudent(studentId) {
    const res = await fetch(`${BASE_URL}/projects/student/${studentId}`, {
        method: "GET",
        headers: header(),
    });

    if (res.status === 200) {
        return res.json();
    }

    throw new Error("Failed to fetch projects for student");
}