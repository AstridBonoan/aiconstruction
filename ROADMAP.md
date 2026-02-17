# Construction AI Suite - Product Roadmap

## Branching Strategy

- `main`: Production-ready code
- One branch per feature: `feature/<name>`
- PR required for merge
- CI must pass before merge
- Commit and push after each feature

---

## Feature Branches (in order)

### Phase 1 - 24-Hour Demo Build (Presentation Safe)

| Branch | Status |
|--------|--------|
| feature/platform-skeleton | Done |
| feature/multi-docker-infrastructure | Done |
| feature/github-actions-ci | Done |
| feature/data-schema-design | Done |
| feature/demo-data-layer | Done |
| feature/risk-scoring-v1 | Done |
| feature/dependency-graph-engine | Done |
| feature/executive-portfolio-dashboard | Done |
| feature/dark-light-theme-toggle | Done |
| feature/mobile-first-responsive-design | Done |

**Phase 1 Outcome**: App runs with docker-compose, displays seeded construction data, risk scores, dependency graph, executive KPI dashboard, dark/light themes, fully responsive. Uses mock data; architecture supports real data.

---

### Phase 2 - Real Monday Integration

| Branch | Status |
|--------|--------|
| feature/monday-oauth-integration | Done |
| feature/jwt-verification-middleware | Done |
| feature/token-encryption-layer | Done |
| feature/board-sync-engine | Pending |
| feature/webhook-engine | Pending |

**Phase 2 Outcome**: Replace mock data with real GraphQL calls. Secure token storage. Uninstall handling. Auto-sync board updates.

---

### Phase 3 - Data Collection for Real AI

| Branch | Status |
|--------|--------|
| feature/historical-snapshot-system | Pending |
| feature/workforce-reliability-engine | Pending |
| feature/subcontractor-performance-engine | Pending |
| feature/equipment-maintenance-engine | Pending |
| feature/material-forecasting-engine | Pending |

**Phase 3 Outcome**: Begin collecting real production data. No ML training yet.

---

### Phase 4 - Machine Learning

| Branch | Status |
|--------|--------|
| feature/feature-engineering-pipeline | Pending |
| feature/ml-training-pipeline | Pending |
| feature/model-inference-service | Pending |
| feature/multi-factor-risk-synthesis | Pending |

**Phase 4 Outcome**: Train models only after sufficient real-world data. Deploy inference endpoints.

---

### Phase 5 - Enterprise Intelligence

| Branch | Status |
|--------|--------|
| feature/what-if-scenario-engine | Pending |
| feature/predictive-resource-allocation | Pending |
| feature/executive-portfolio-dashboard (enhancements) | Pending |
| feature/compliance-intelligence-engine | Pending |
| feature/iot-site-intelligence | Pending |

---

### Infrastructure and Quality Branches

| Branch | Status |
|--------|--------|
| feature/multi-tenant-architecture | Pending |
| feature/authentication-foundation | Pending |
| feature/api-versioning | Pending |
| feature/rate-limiting-layer | Pending |
| feature/logging-and-monitoring | Pending |
| feature/error-handling-standardization | Pending |
| feature/design-system-components | Pending |

---

## AI Model Data Collection Guidelines

- Real ML training begins only after 3-6 months production data
- Requires thousands of completed tasks
- Proper labeling of delay outcomes
- Historical snapshots stored
- Before that: use rule-based scoring, statistical heuristics, deterministic risk models

---

## Current Phase

**Phase 1: COMPLETE**  
**Next: Phase 2 - Real Monday Integration**
