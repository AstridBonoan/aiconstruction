const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1';

async function fetchJson(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export const api = {
  health: () => fetchJson('/health'),
  kpis: () => fetchJson('/dashboard/kpis'),
  projects: () => fetchJson('/projects'),
  projectItems: (id) => fetchJson(`/projects/${id}/items`),
  riskScores: (scope = 'all') => fetchJson(`/risk/scores?scope=${scope}`),
  dependencyGraph: () => fetchJson('/dependencies/graph'),
  criticalPath: () => fetchJson('/dependencies/critical-path'),
};
