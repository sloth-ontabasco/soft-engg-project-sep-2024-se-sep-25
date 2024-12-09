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

/**
 * Create a new team for a specific project.
 * @param {string} projectId - The ID of the project.
 * @param {Object} teamData - Team data containing `team_name` and `members`.
 * @returns {Promise<Object>} A promise that resolves to the created team object.
 */
export async function createTeam(projectId, teamData) {
  const res = await fetch(`${BASE_URL}/${projectId}/teams`, {
    method: "POST",
        headers: {
            ...header(),
            "Content-Type": "application/json",
        },
    body: JSON.stringify(teamData),
  });

  if (res.status === 201) {
    return res.json();
  }

  const errorData = await res.json();
  throw new Error(errorData.message || 'Failed to create team');
}

/**
 * Update a team's details.
 * @param {string} projectId - The ID of the project.
 * @param {string} teamId - The ID of the team to update.
 * @param {Object} teamData - Updated team data containing `team_name` and `members`.
 * @returns {Promise<Object>} A promise that resolves to the updated team object.
 */
export async function updateTeam(projectId, teamId, teamData) {
  const res = await fetch(`${BASE_URL}/${projectId}/teams/${teamId}`, {
    method: "PUT",
        headers: {
            ...header(),
            "Content-Type": "application/json",
        },
    body: JSON.stringify(teamData),
  });

  if (res.status === 200) {
    return res.json();
  }

  const errorData = await res.json();
  throw new Error(errorData.message || 'Failed to update team');
}

/**
 * Delete a team.
 * @param {string} projectId - The ID of the project.
 * @param {string} teamId - The ID of the team to delete.
 * @returns {Promise<void>} A promise that resolves when the team is deleted.
 */
export async function deleteTeam(projectId, teamId) {
  const res = await fetch(`${BASE_URL}/${projectId}/teams/${teamId}`, {
    method: 'DELETE',
    headers: header(),
  });

  if (res.status === 200) {
    return res.json();
  }

  const errorData = await res.json();
  throw new Error(errorData.message || 'Failed to delete team');
}
