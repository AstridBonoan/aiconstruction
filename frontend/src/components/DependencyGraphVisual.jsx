import { useMemo } from 'react';

const NODE_WIDTH = 160;
const NODE_HEIGHT = 56;
const HORZ_GAP = 40;
const VERT_GAP = 60;

function layoutNodes(nodes, edges) {
  const nodeIds = new Set(nodes.map((n) => n.id));
  const incoming = {};
  const outgoing = {};
  nodeIds.forEach((id) => {
    incoming[id] = new Set();
    outgoing[id] = new Set();
  });
  edges.forEach((e) => {
    if (nodeIds.has(e.from) && nodeIds.has(e.to)) {
      outgoing[e.from].add(e.to);
      incoming[e.to].add(e.from);
    }
  });

  const layers = [];
  const assigned = new Set();
  let remaining = new Set(nodeIds);

  while (remaining.size > 0) {
    const layer = [];
    for (const id of remaining) {
      const deps = incoming[id];
      const allDepsAssigned = [...deps].every((d) => assigned.has(d));
      if (allDepsAssigned) layer.push(id);
    }
    if (layer.length === 0) {
      for (const id of remaining) layer.push(id);
    }
    layer.forEach((id) => {
      assigned.add(id);
      remaining.delete(id);
    });
    layers.push(layer);
  }

  const pos = {};
  let maxCol = 0;
  layers.forEach((layer, row) => {
    layer.forEach((id, col) => {
      pos[id] = { row, col, x: 0, y: 0 };
      maxCol = Math.max(maxCol, col);
    });
  });

  const colsPerLayer = layers.map((l) => l.length);
  const maxCols = Math.max(...colsPerLayer, 1);

  layers.forEach((layer, row) => {
    const count = layer.length;
    const totalWidth = count * NODE_WIDTH + (count - 1) * HORZ_GAP;
    const startX = (maxCols * (NODE_WIDTH + HORZ_GAP) - totalWidth) / 2 + NODE_WIDTH / 2 + HORZ_GAP / 2;
    layer.forEach((id, col) => {
      pos[id].x = startX + col * (NODE_WIDTH + HORZ_GAP);
      pos[id].y = 40 + row * (NODE_HEIGHT + VERT_GAP);
    });
  });

  const width = maxCols * (NODE_WIDTH + HORZ_GAP) + 80;
  const height = layers.length * (NODE_HEIGHT + VERT_GAP) + 60;

  return { pos, width, height };
}

function getEdgePath(from, to, pos) {
  const p1 = pos[from];
  const p2 = pos[to];
  if (!p1 || !p2) return '';
  const x1 = p1.x;
  const y1 = p1.y + NODE_HEIGHT / 2;
  const x2 = p2.x;
  const y2 = p2.y - NODE_HEIGHT / 2;
  const midY = (y1 + y2) / 2;
  return `M ${x1} ${y1} C ${x1} ${midY}, ${x2} ${midY}, ${x2} ${y2}`;
}

export function DependencyGraphVisual({ nodes, edges }) {
  const { pos, width, height } = useMemo(() => layoutNodes(nodes || [], edges || []), [nodes, edges]);
  const nodeMap = useMemo(() => Object.fromEntries((nodes || []).map((n) => [n.id, n])), [nodes]);

  if (!nodes?.length) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400 text-sm">
        No dependencies to display
      </div>
    );
  }

  return (
    <div className="overflow-auto rounded-lg bg-gray-50 dark:bg-gray-900/50 p-4 min-h-[400px]">
      <svg
        width={width}
        height={height}
        className="dependency-graph"
        style={{ minWidth: '100%' }}
      >
        <defs>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="9"
            refY="3.5"
            orient="auto"
          >
            <polygon points="0 0, 10 3.5, 0 7" fill="#6b7280" />
          </marker>
        </defs>
        {edges.map((e) => {
          const path = getEdgePath(e.from, e.to, pos);
          if (!path) return null;
          return (
            <path
              key={`${e.from}-${e.to}`}
              d={path}
              fill="none"
              stroke="#6b7280"
              strokeWidth="2"
              markerEnd="url(#arrowhead)"
              className="dark:stroke-gray-500"
            />
          );
        })}
        {nodes.map((n) => {
          const p = pos[n.id];
          if (!p) return null;
          const x = p.x - NODE_WIDTH / 2;
          const y = p.y - NODE_HEIGHT / 2;
          const isHighRisk = n.risk_level === 'high' || n.risk_level === 'critical';
          const label = n.label?.length > 22 ? n.label.slice(0, 20) + '...' : n.label;
          return (
            <g key={n.id} transform={`translate(${x}, ${y})`}>
              <rect
                width={NODE_WIDTH}
                height={NODE_HEIGHT}
                rx="8"
                fill={isHighRisk ? '#fef2f2' : '#ffffff'}
                stroke={isHighRisk ? '#f87171' : '#e5e7eb'}
                className="dark:fill-gray-800 dark:stroke-gray-600"
              />
              <text x={NODE_WIDTH / 2} y="22" textAnchor="middle" className="fill-gray-900 dark:fill-white" fontSize="11" fontWeight="600">
                {label}
              </text>
              <text x={NODE_WIDTH / 2} y="38" textAnchor="middle" className="fill-gray-500 dark:fill-gray-400" fontSize="9">
                {n.board_name?.slice(0, 18)}{n.board_name?.length > 18 ? '...' : ''}
              </text>
              <text x={NODE_WIDTH / 2} y="48" textAnchor="middle" fontSize="10">
                <tspan className={isHighRisk ? 'fill-red-600' : 'fill-gray-600 dark:fill-gray-300'}>
                  {n.risk_level} ({n.risk_score ?? 0})
                </tspan>
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
