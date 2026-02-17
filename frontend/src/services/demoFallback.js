/** Static demo data when API is unavailable. */
export const demoKpis = {
  tenant: { name: 'Acme Construction (Demo)', integration_status: 'demo' },
  source: 'fallback',
  kpis: {
    total_projects: 3,
    total_tasks: 12,
    tasks_complete: 4,
    tasks_in_progress: 6,
    tasks_stuck: 2,
    completion_percent: 33.3,
    avg_risk_score: 42.5,
    high_risk_items: 3,
    critical_risk_items: 1,
  },
  boards: [
    { board_id: '1', board_name: 'Riverside Tower - Phase 1', score: 38.2, level: 'medium', high_risk_count: 1 },
    { board_id: '2', board_name: 'Westside Industrial Complex', score: 28.5, level: 'low', high_risk_count: 0 },
    { board_id: '3', board_name: 'Downtown Medical Center Expansion', score: 58.1, level: 'high', high_risk_count: 2 },
  ],
};

export const demoRiskScores = [
  { item_id: '1', item_name: 'Curtain Wall Installation', board_name: 'Riverside Tower', score: 72, level: 'high' },
  { item_id: '2', item_name: 'New HVAC Ductwork', board_name: 'Downtown Medical', score: 68, level: 'high' },
  { item_id: '3', item_name: 'Structural Steel - Level 1-5', board_name: 'Riverside Tower', score: 45, level: 'medium' },
  { item_id: '4', item_name: 'MEP Rough-in - Floors 1-3', board_name: 'Riverside Tower', score: 38, level: 'medium' },
  { item_id: '5', item_name: 'Warehouse Shell - Steel Frame', board_name: 'Westside Industrial', score: 32, level: 'medium' },
];

export const demoGraph = {
  nodes: [
    { id: 'item_1', label: 'Foundation - Excavation', board_name: 'Riverside Tower', risk_score: 0, risk_level: 'low' },
    { id: 'item_2', label: 'Foundation - Concrete Pour', board_name: 'Riverside Tower', risk_score: 0, risk_level: 'low' },
    { id: 'item_3', label: 'Structural Steel L1-5', board_name: 'Riverside Tower', risk_score: 45, risk_level: 'medium' },
    { id: 'item_4', label: 'MEP Rough-in Floors 1-3', board_name: 'Riverside Tower', risk_score: 38, risk_level: 'medium' },
    { id: 'item_5', label: 'Curtain Wall Install', board_name: 'Riverside Tower', risk_score: 72, risk_level: 'high' },
    { id: 'item_6', label: 'Elevator Shaft', board_name: 'Riverside Tower', risk_score: 42, risk_level: 'medium' },
    { id: 'item_7', label: 'Site Preparation', board_name: 'Westside Industrial', risk_score: 0, risk_level: 'low' },
    { id: 'item_8', label: 'Warehouse Steel Frame', board_name: 'Westside Industrial', risk_score: 32, risk_level: 'medium' },
  ],
  edges: [
    { from: 'item_2', to: 'item_3' },
    { from: 'item_3', to: 'item_4' },
    { from: 'item_3', to: 'item_5' },
    { from: 'item_3', to: 'item_6' },
    { from: 'item_7', to: 'item_8' },
  ],
};
