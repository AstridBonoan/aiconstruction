import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

export function CompletionGauge({ percent }) {
  const p = Math.min(100, Math.max(0, percent ?? 0));
  const data = [
    { value: p, color: p >= 75 ? '#22c55e' : p >= 50 ? '#eab308' : '#ef4444' },
    { value: 100 - p, color: 'rgba(156,163,175,0.3)' },
  ];

  return (
    <ResponsiveContainer width="100%" height={120}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={35}
          outerRadius={50}
          startAngle={90}
          endAngle={-270}
          dataKey="value"
          stroke="none"
        >
          {data.map((entry, i) => (
            <Cell key={i} fill={entry.color} />
          ))}
        </Pie>
      </PieChart>
    </ResponsiveContainer>
  );
}
