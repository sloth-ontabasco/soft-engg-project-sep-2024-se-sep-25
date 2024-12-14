import { header } from './auth';

const BASE_URL = import.meta.env.VITE_SERVER_BASE_URL;

export async function getGithubRepos(teamId) {
  const res = await fetch(`${BASE_URL}/github/integration/${teamId}`, {
    method: "GET",
    headers: header(),
  });
  if (res.status === 200) {
    const data = await res.json();
    return data;
  }

  throw new Error("Failed to fetch github details for the team with id: " + teamId);
}

export async function getGithubCommits(teamId, repo_name) {
    const res = await fetch(`${BASE_URL}/github/commits/${teamId}?repo_name=${repo_name}`, {
      method: "GET",
      headers: header(),
    });
    if (res.status === 200) {
      const data = await res.json();
      return data;
    }
  
    throw new Error("Failed to fetch github commits for the team with id: " + teamId + " and repo_name: " + repo_name);
  }