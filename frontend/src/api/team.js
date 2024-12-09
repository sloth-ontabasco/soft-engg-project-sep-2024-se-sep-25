import { header } from './auth';

const BASE_URL = import.meta.env.VITE_SERVER_BASE_URL;

/**
 * Fetch all teams for a specific project.
 * @param {string} projectId - The ID of the project.
 * @returns {Promise<Object[]>} A promise that resolves to an array of teams or a single team object.
 */
export async function getProjectTeams(projectId) {
  const res = await fetch(`${BASE_URL}/${projectId}/teams`, {
    method: "GET",
    headers: header(),
  });

  if (res.status === 200) {
    const data = await res.json();
    console.log(data);
    return data.teams || { team: data.team };
  }

  throw new Error("Failed to fetch project teams");
}