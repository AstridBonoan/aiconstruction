import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Card, CardHeader, CardBody } from '../components/Card';
import { Badge } from '../components/Badge';
import { CompletionChart } from '../components/charts/CompletionChart';
import { TaskStatusChart } from '../components/charts/TaskStatusChart';
import { CompletionGauge } from '../components/charts/CompletionGauge';

export function DashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .kpis()
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24">
        <div className="animate-pulse text-gray-500 dark:text-gray-400">Loading...</div>
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

  const { tenant, kpis, boards } = data || {};
  const ks = kpis || {};

  return (
    <div className="space-y-6 md:space-y-8">
      <div>
        <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
          Executive Portfolio Dashboard
        </h1>
        <p className="mt-1 text-gray-500 dark:text-gray-400">
          {tenant?.name} (Demo - Simulated Monday.com data)
        </p>
        {data?.source === 'fallback' && (
          <p className="mt-1 text-amber-600 dark:text-amber-400 text-sm">Running in offline fallback mode</p>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardBody>
            <p className="text-sm text-gray-500 dark:text-gray-400">Total Projects</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{ks.total_projects ?? 0}</p>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <p className="text-sm text-gray-500 dark:text-gray-400">Tasks Complete</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
              {ks.tasks_complete ?? 0} / {ks.total_tasks ?? 0}
            </p>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <p className="text-sm text-gray-500 dark:text-gray-400">Completion</p>
            <div className="flex items-center gap-4 mt-1">
              <div className="w-24 shrink-0">
                <CompletionGauge percent={ks.completion_percent} />
              </div>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{ks.completion_percent ?? 0}%</p>
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <p className="text-sm text-gray-500 dark:text-gray-400">Avg Risk Score</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{ks.avg_risk_score ?? 0}</p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              {ks.high_risk_items ?? 0} high / {ks.critical_risk_items ?? 0} critical
            </p>
          </CardBody>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader title="Risk by Project" subtitle="Horizontal bar chart" />
          <CardBody>
            <CompletionChart boards={boards} />
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Task Status Distribution" subtitle="Portfolio-wide breakdown" />
          <CardBody>
            <TaskStatusChart
              tasksComplete={ks.tasks_complete}
              tasksInProgress={ks.tasks_in_progress}
              tasksStuck={ks.tasks_stuck}
              totalTasks={ks.total_tasks}
            />
          </CardBody>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader title="Risk Overview" subtitle="Projects with elevated risk" />
          <CardBody>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              High risk: {ks.high_risk_items ?? 0} | Critical: {ks.critical_risk_items ?? 0}
            </p>
            <div className="space-y-3">
              {Array.isArray(boards) &&
                boards.map((b) => (
                  <div
                    key={b.board_id}
                    className="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700 last:border-0"
                  >
                    <span className="text-gray-900 dark:text-white font-medium">{b.board_name}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-gray-500 dark:text-gray-400">{b.high_risk_count} at risk</span>
                      <Badge variant={b.level}>{b.score}</Badge>
                    </div>
                  </div>
                ))}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Task Status" subtitle="Summary counts" />
          <CardBody>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-300">In progress</span>
                <span className="font-medium">{ks.tasks_in_progress ?? 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-300">Stuck</span>
                <span className="font-medium text-amber-600 dark:text-amber-400">{ks.tasks_stuck ?? 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-300">Done</span>
                <span className="font-medium text-green-600 dark:text-green-400">{ks.tasks_complete ?? 0}</span>
              </div>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
