const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1';
import { demoKpis, demoRiskScores, demoGraph } from './demoFallback';

async function fetchJson(path, fallback = null) {
  try {
    const res = await fetch(`${API_BASE}${path}`);
    if (res.ok) return res.json();
    if (fallback) return fallback;
    throw new Error(`API error: ${res.status}`);
  } catch (e) {
    if (fallback) return fallback;
    throw e;
  }
}

export const api = {
  health: () => fetchJson('/health'),
  kpis: () => fetchJson('/dashboard/kpis', demoKpis),
  projects: () => fetchJson('/projects', { tenant: demoKpis.tenant, projects: [], source: 'fallback' }),
  projectItems: (id) => fetchJson(`/projects/${id}/items`, { items: [], board_id: id }),
  riskScores: (scope = 'all') => fetchJson(`/risk/scores?scope=${scope}`, { scores: demoRiskScores, scope }),
  dependencyGraph: () => fetchJson('/dependencies/graph', demoGraph),
  criticalPath: () => fetchJson('/dependencies/critical-path', { critical_path: [] }),
};
