import axios from 'axios';
import { header } from './auth';

const BASE_URL = import.meta.env.VITE_SERVER_BASE_URL;

export async function getSubmission(teamId, milestoneId) {
    try {
        const response = await axios.get(`${BASE_URL}/submission`, {
            params: {
                team_id: teamId,
                milestone_id: milestoneId
            },
            headers: header()
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        throw error;
    }
}

export async function createSubmission(formData) {
    try {
        const response = await axios.post(`${BASE_URL}/submission`, formData, {
            headers: {
                ...header(),
                'Content-Type': 'multipart/form-data'
            }
        });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export async function updateSubmission(teamId, milestoneId, formData) {
    try {
        const response = await axios.put(`${BASE_URL}/submission`, formData, {
            params: {
                team_id: teamId,
                milestone_id: milestoneId
            },
            headers: {
                ...header(),
                'Content-Type': 'multipart/form-data'
            }
        });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export async function getSubmissionFile(teamId, milestoneId) {
    try {
        console.log("Downloading file from: ", `${BASE_URL}/file`);
        const response = await axios.get(`${BASE_URL}/file`, {
            params: {
                team_id: teamId,
                milestone_id: milestoneId
            },
            headers: header(),
            responseType: 'blob'
        });
        console.log("Response received: ", response);
        return response;
    } catch (error) {
        console.error("Error in getSubmissionFile: ", error);
        throw error;
    }
}

export async function fetchGenAIReport(submissionId) {
    try {
        const response = await axios.get(`${BASE_URL}/genai/summary/${submissionId}`, {
            headers: header(),
            responseType: 'blob'
        });
        return response;
    } catch (error) {
        throw error;
    }
}
