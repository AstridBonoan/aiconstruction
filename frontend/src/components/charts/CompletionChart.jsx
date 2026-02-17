import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const COLORS = { low: '#22c55e', medium: '#eab308', high: '#f97316', critical: '#ef4444' };

export function CompletionChart({ boards }) {
  const data = (boards || []).map((b) => ({
    name: b.board_name?.length > 20 ? b.board_name.slice(0, 18) + '...' : b.board_name || 'Unknown',
    score: b.score ?? 0,
    level: b.level || 'low',
  }));

  if (data.length === 0) return null;

  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={data} layout="vertical" margin={{ top: 5, right: 20, left: 80, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
        <XAxis type="number" domain={[0, 100]} stroke="#9ca3af" fontSize={12} />
        <YAxis type="category" dataKey="name" stroke="#9ca3af" fontSize={11} width={75} />
        <Tooltip
          contentStyle={{
            backgroundColor: 'var(--tw-bg-opacity, rgb(255 255 255))',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
          }}
          formatter={(v) => [`${v}`, 'Risk Score']}
        />
        <Bar dataKey="score" radius={[0, 4, 4, 0]} maxBarSize={28}>
          {data.map((entry, i) => (
            <Cell key={i} fill={COLORS[entry.level] || COLORS.low} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
