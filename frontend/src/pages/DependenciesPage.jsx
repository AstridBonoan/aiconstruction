import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Card, CardHeader, CardBody } from '../components/Card';
import { Badge } from '../components/Badge';
import { DependencyGraphVisual } from '../components/DependencyGraphVisual';

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

  return (
    <div className="space-y-6">
      <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">Dependency Graph</h1>
      <p className="text-gray-500 dark:text-gray-400">
        Task dependencies from Monday.com boards. Arrows indicate blocking relationships (A blocks B).
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader
            title="Task Dependency Graph"
            subtitle={`${nodes.length} tasks, ${edges.length} dependencies`}
          />
          <CardBody className="p-0">
            <DependencyGraphVisual nodes={nodes} edges={edges} />
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Tasks by Project" subtitle="Quick reference" />
          <CardBody>
            <div className="space-y-4">
              {[...new Set(nodes.map((n) => n.board_name))].filter(Boolean).map((board) => {
                const boardNodes = nodes.filter((n) => n.board_name === board);
                return (
                  <div key={board}>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300">{board}</p>
                    <ul className="mt-2 space-y-1 text-sm text-gray-600 dark:text-gray-400">
                      {boardNodes.map((n) => (
                        <li key={n.id} className="flex justify-between items-center gap-2">
                          <span className="truncate">{n.label}</span>
                          <Badge variant={n.risk_level} className="shrink-0">
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
