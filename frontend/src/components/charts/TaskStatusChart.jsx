import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const COLORS = {
  done: '#22c55e',
  in_progress: '#3b82f6',
  stuck: '#ef4444',
  new: '#9ca3af',
};

export function TaskStatusChart({ tasksComplete, tasksInProgress, tasksStuck, totalTasks }) {
  const done = tasksComplete ?? 0;
  const inProgress = tasksInProgress ?? 0;
  const stuck = tasksStuck ?? 0;
  const newCount = Math.max(0, (totalTasks ?? 0) - done - inProgress - stuck);

  const data = [
    { name: 'Done', value: done, color: COLORS.done },
    { name: 'In Progress', value: inProgress, color: COLORS.in_progress },
    { name: 'Stuck', value: stuck, color: COLORS.stuck },
    { name: 'New', value: newCount, color: COLORS.new },
  ].filter((d) => d.value > 0);

  if (data.length === 0) return null;

  return (
    <ResponsiveContainer width="100%" height={220}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={50}
          outerRadius={75}
          paddingAngle={2}
          dataKey="value"
          label={({ name, value }) => `${name}: ${value}`}
        >
          {data.map((entry, i) => (
            <Cell key={i} fill={entry.color} stroke="transparent" />
          ))}
        </Pie>
        <Tooltip formatter={(v) => [v, 'Tasks']} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}
