import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const COLORS = { low: '#22c55e', medium: '#eab308', high: '#f97316', critical: '#ef4444' };

export function RiskDistributionChart({ scores }) {
  const levelCounts = (scores || []).reduce((acc, s) => {
    const l = s.level || 'low';
    acc[l] = (acc[l] || 0) + 1;
    return acc;
  }, {});

  const data = ['low', 'medium', 'high', 'critical'].map((level) => ({
    level: level.charAt(0).toUpperCase() + level.slice(1),
    count: levelCounts[level] ?? 0,
    fill: COLORS[level],
  }));

  if (data.every((d) => d.count === 0)) return null;

  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={data} margin={{ top: 10, right: 10, left: 10, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
        <XAxis dataKey="level" stroke="#9ca3af" fontSize={12} />
        <YAxis stroke="#9ca3af" fontSize={12} />
        <Tooltip formatter={(v) => [v, 'Items']} />
        <Bar dataKey="count" radius={[4, 4, 0, 0]}>
          {data.map((entry, i) => (
            <Cell key={i} fill={entry.fill} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
