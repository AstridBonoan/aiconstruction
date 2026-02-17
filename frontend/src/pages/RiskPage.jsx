import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Card, CardHeader, CardBody } from '../components/Card';
import { Badge } from '../components/Badge';

export function RiskPage() {
  const [scores, setScores] = useState([]);
  const [scope, setScope] = useState('items');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    api
      .riskScores(scope)
      .then((res) => setScores(res.scores || []))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [scope]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24">
        <div className="animate-pulse text-gray-500 dark:text-gray-400">Loading risk scores...</div>
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

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">Risk Scores</h1>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setScope('items')}
            className={`px-4 py-2 rounded-lg text-sm font-medium ${
              scope === 'items'
                ? 'bg-gray-900 dark:bg-white text-white dark:text-gray-900'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            By Task
          </button>
          <button
            type="button"
            onClick={() => setScope('boards')}
            className={`px-4 py-2 rounded-lg text-sm font-medium ${
              scope === 'boards'
                ? 'bg-gray-900 dark:bg-white text-white dark:text-gray-900'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            By Project
          </button>
        </div>
      </div>

      <Card>
        <CardHeader
          title={scope === 'items' ? 'Task-Level Risk' : 'Project-Level Risk'}
          subtitle="Rule-based scoring from status, schedule, and dependencies"
        />
        <CardBody>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <th className="pb-3 text-sm font-medium text-gray-500 dark:text-gray-400">Name</th>
                  {scope === 'items' && (
                    <th className="pb-3 text-sm font-medium text-gray-500 dark:text-gray-400">Project</th>
                  )}
                  <th className="pb-3 text-sm font-medium text-gray-500 dark:text-gray-400">Score</th>
                  <th className="pb-3 text-sm font-medium text-gray-500 dark:text-gray-400">Level</th>
                </tr>
              </thead>
              <tbody>
                {scores.map((s) => (
                  <tr key={s.item_id || s.board_id} className="border-b border-gray-100 dark:border-gray-800">
                    <td className="py-3 text-gray-900 dark:text-white">{s.item_name || s.board_name}</td>
                    {scope === 'items' && s.board_name && (
                      <td className="py-3 text-gray-500 dark:text-gray-400">{s.board_name}</td>
                    )}
                    <td className="py-3">
                      <span className="font-medium">{s.score}</span>
                    </td>
                    <td className="py-3">
                      <Badge variant={s.level}>{s.level}</Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardBody>
      </Card>
    </div>
  );
}
