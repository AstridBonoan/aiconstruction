import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Card, CardHeader, CardBody } from '../components/Card';
import { Badge } from '../components/Badge';

export function DependenciesPage() {
  const [graph, setGraph] = useState({ nodes: [], edges: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .dependencyGraph()
      .then(setGraph)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24">
        <div className="animate-pulse text-gray-500 dark:text-gray-400">Loading dependency graph...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20 p-4 text-red-700 dark:text-red-400">
        Error: {error}
      </div>
    );
  }

  const { nodes, edges } = graph;
  const nodeMap = Object.fromEntries(nodes.map((n) => [n.id, n]));

  return (
    <div className="space-y-6">
      <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">Dependency Graph</h1>
      <p className="text-gray-500 dark:text-gray-400">
        Task dependencies from Monday.com boards. Arrows indicate blocking relationships.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader
            title="Graph"
            subtitle={`${nodes.length} tasks, ${edges.length} dependencies`}
          />
          <CardBody>
            <div className="overflow-x-auto min-h-[300px] p-4 bg-gray-50 dark:bg-gray-900/50 rounded-lg">
              <div className="flex flex-wrap gap-4">
                {nodes.map((n) => (
                  <div
                    key={n.id}
                    className={`px-4 py-2 rounded-lg border text-sm ${
                      n.risk_level === 'critical' || n.risk_level === 'high'
                        ? 'border-red-300 dark:border-red-700 bg-red-50 dark:bg-red-900/20'
                        : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800'
                    }`}
                  >
                    <div className="font-medium text-gray-900 dark:text-white">{n.label}</div>
                    <div className="flex gap-2 mt-1">
                      <Badge variant={n.risk_level}>{n.risk_level}</Badge>
                      <span className="text-xs text-gray-500 dark:text-gray-400">{n.board_name}</span>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-6 text-sm text-gray-500 dark:text-gray-400">
                Edges: {edges.map((e) => `${nodeMap[e.from]?.label || e.from} -> ${nodeMap[e.to]?.label || e.to}`).join('; ')}
              </div>
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Tasks" subtitle="By project" />
          <CardBody>
            <div className="space-y-4">
              {[...new Set(nodes.map((n) => n.board_name))].map((board) => {
                const boardNodes = nodes.filter((n) => n.board_name === board);
                return (
                  <div key={board}>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">{board}</p>
                    <ul className="mt-2 space-y-1 text-sm text-gray-600 dark:text-gray-400">
                      {boardNodes.map((n) => (
                        <li key={n.id} className="flex justify-between">
                          <span className="truncate">{n.label}</span>
                          <Badge variant={n.risk_level} className="ml-2 shrink-0">
                            {n.risk_score}
                          </Badge>
                        </li>
                      ))}
                    </ul>
                  </div>
                );
              })}
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
