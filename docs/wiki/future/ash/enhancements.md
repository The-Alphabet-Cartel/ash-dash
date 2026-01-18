---
title: "Ash Ecosystem - Future Enhancements"
description: "Consolidated enhancements and feature ideas across the Ash Crisis Detection Ecosystem"
category: future
tags:
  - roadmap
  - planning
  - ash
  - ecosystem
author: "PapaBearDoes"
version: "5.0"
last_updated: "2026-01-17"
---
# Ash Ecosystem: Future Enhancements & Improvements

============================================================================
**Ash**: Crisis Detection Ecosystem for The Alphabet Cartel
**The Alphabet Cartel** - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================

**Document Version**: v5.0.6
**Created**: 2026-01-12
**Phase**: Post-v5.0 Planning
**Status**: 📋 Backlog
**Last Updated**: 2026-01-17

---

## Table of Contents

1. [Overview](#-overview)
2. [Cross-Component Priorities](#-cross-component-priorities)
3. [Ash-Bot Enhancements](#-ash-bot-enhancements)
4. [Ash-NLP Enhancements](#-ash-nlp-enhancements)
5. [Ash-Dash Enhancements](#-ash-dash-enhancements)
6. [Ash-Vault Enhancements](#-ash-vault-enhancements)
7. [Ash-Thrash Enhancements](#-ash-thrash-enhancements)
8. [Ecosystem-Wide Research](#-ecosystem-wide-research)
9. [Community Requests](#-community-requests)
10. [SQLite to PostgreSQL Migration Guidelines](#-sqlite-to-postgresql-migration-guidelines)
11. [How To Add Ideas](#-how-to-add-ideas)

---

## 📋 Overview

This document provides a consolidated view of all planned enhancements across the Ash Crisis Detection Ecosystem. Each component maintains its own detailed `enhancements.md` file - this umbrella document summarizes priorities and highlights cross-component dependencies.

### Component Enhancement Documents

| Component | Enhancement Document |
|-----------|---------------------|
| **Ash-Bot** | [ash-bot/enhancements.md](../ash-bot/enhancements.md) |
| **Ash-NLP** | [ash-nlp/enhancements.md](../ash-nlp/enhancements.md) |
| **Ash-Dash** | [ash-dash/enhancements.md](../ash-dash/enhancements.md) |
| **Ash-Vault** | [ash-vault/enhancements.md](../ash-vault/enhancements.md) |
| **Ash-Thrash** | [ash-thrash/enhancements.md](../ash-thrash/enhancements.md) |

### Priority Legend

| Priority | Description |
|----------|-------------|
| 🔴 High | Significant user value, should be scheduled soon |
| 🟡 Medium | Good to have, schedule when capacity allows |
| 🟢 Low | Nice to have, opportunistic implementation |
| ⚪ Someday | Long-term vision, no immediate plans |

### Complexity Legend

| Complexity | Description |
|------------|-------------|
| 🟦 Low | < 4 hours, minimal dependencies |
| 🟨 Medium | 4-8 hours, some dependencies |
| 🟧 High | 8-16 hours, significant work |
| 🟥 Very High | 16+ hours, major feature |

---

## 🎯 Cross-Component Priorities

These enhancements require coordination across multiple Ash components and represent the highest-impact ecosystem improvements.

### 1. ~~LoggingConfigManager Colorization Enforcement~~ ✅ IMPLEMENTED

**Priority**: ✅ Implemented (Phase 6 - 2026-01-17)
**Components**: Ash (Core), Ash-Bot, Ash-NLP, Ash-Dash, Ash-Vault
**Complexity**: 🟨 Medium
**Status**: ✅ Complete

Updated LoggingConfigManager in all ecosystem components to comply with Clean Architecture Charter v5.2 Rule #9, providing standardized ANSI colorization across all components.

**Implemented Color Scheme** (Charter v5.2 Compliant):

| Log Level | Color | ANSI Code |
|-----------|-------|-----------|
| CRITICAL | Bright Red (Bold) | `\033[1;91m` |
| ERROR | Red | `\033[91m` |
| WARNING | Yellow | `\033[93m` |
| INFO | Cyan | `\033[96m` |
| DEBUG | Gray | `\033[90m` |
| SUCCESS | Green | `\033[92m` |

**Files Updated/Created**:
| Component | File | Action |
|-----------|------|--------|
| Ash (Core) | `src/managers/logging_manager.py` | Updated |
| Ash-Bot | `src/managers/logging_config_manager.py` | **Created** |
| Ash-NLP | `src/managers/logging_config_manager.py` | **Created** |
| Ash-Dash | `src/managers/logging_config_manager.py` | Updated |
| Ash-Vault | `src/managers/logging_config_manager.py` | Updated |

**Features Implemented**:
- Charter v5.2 compliant color scheme across all components
- Custom SUCCESS log level (25) with `logger.success()` method
- Emoji symbols for visual identification (🚨❌⚠️ℹ️🔍✅)
- TTY detection for automatic color support
- JSON format option preserved for production log aggregators

**Benefit**: Consistent visual debugging across all ecosystem components with immediate severity recognition through color coding.

**See**: [Phase 6 Planning](phase6/planning.md) | [Clean Architecture Charter v5.2 - Rule #9](../standards/clean_architecture_charter.md)

---

### 2. ~~Per-Module Discord Alert Webhooks~~ ✅ IMPLEMENTED

**Priority**: ✅ Implemented (Phase 4 - 2026-01-17)
**Components**: Ash (Core), Ash-Bot, Ash-NLP, Ash-Dash, Ash-Vault
**Complexity**: 🟦 Low
**Status**: ✅ Complete

Separate Discord webhook tokens per module allowing independent alert routing and management.

**Implemented Secret Names**:
| Module | Secret File | Purpose |
|--------|-------------|--------|
| Ash (Core) | `ash_discord_alert_token` | Ecosystem health alerts |
| Ash-Bot | `ash_bot_discord_alert_token` | Crisis detection alerts |
| Ash-NLP | `ash_nlp_discord_alert_token` | Model conflict alerts |
| Ash-Dash | `ash_dash_discord_alert_token` | Dashboard system alerts |
| Ash-Vault | `ash_vault_discord_alert_token` | Backup failure alerts |

**Files Updated** (per module):
- `src/managers/secrets_manager.py` - Updated `get_discord_alert_token()` with module-specific lookup + legacy fallback
- `docker-compose.yml` - Updated secrets section with new names
- `secrets/README.md` - Updated documentation

**Legacy Compatibility**: Each module's `get_discord_alert_token()` falls back to the deprecated `discord_alert_token` for migration support.

---

### 3. Ash-Dash ↔ Ash-Vault Integration Verification

**Priority**: 🔴 High (Immediate)
**Components**: Ash-Dash, Ash-Vault
**Complexity**: 🟨 Medium
**Status**: ⚠️ Known Issue - Requires Verification

The connection between Ash-Dash and Ash-Vault experienced failures during development. This must be verified before the archive functionality can be considered production-ready.

**Verification Tasks**:
- [ ] Verify MinIO health endpoint from Ash-Dash container
- [ ] Test archive upload workflow end-to-end
- [ ] Test archive retrieval and decryption
- [ ] Verify scheduled cleanup job execution

**See**: [Ash-Dash Known Issues](ash-dash/roadmap.md#-known-issues) | [Ash-Vault Known Issues](ash-vault/roadmap.md#-known-issues)

---

### 4. CRT Feedback Loop

**Priority**: 🔴 High
**Components**: Ash-Bot, Ash-NLP, Ash-Dash
**Complexity**: 🟥 Very High
**Estimated Time**: 30-40 hours total

Create a continuous improvement cycle where CRT severity overrides flow back to Ash-NLP for model optimization.

**Data Flow**:
```
CRT adjusts severity in Ash-Dash
         ↓
Ash-Bot receives override event
         ↓
Ash-Bot sends feedback to Ash-NLP
         ↓
Ash-NLP stores feedback for analysis
         ↓
Periodic weight/threshold optimization
```

**Implementation Phases**:
1. **Phase 1**: Severity Override UI (Ash-Dash) - See [Ash-Dash #2](ash-dash/enhancements.md)
2. **Phase 2**: Feedback API (Ash-NLP) - See [Ash-NLP #2](ash-nlp/enhancements.md)
3. **Phase 3**: Override Event Handling (Ash-Bot) - See [Ash-Bot #6](ash-bot/enhancements.md)
4. **Phase 4**: Automated Optimization (Ash-NLP) - See [Ash-NLP #3](ash-nlp/enhancements.md)

**Benefit**: Continuous accuracy improvement based on real-world CRT corrections.

---

### 5. Backup Health Visibility

**Priority**: 🔴 High
**Components**: Ash-Vault, Ash-Dash
**Complexity**: 🟨 Medium
**Estimated Time**: 6-8 hours

Surface Ash-Vault backup health status in Ash-Dash Admin interface, giving administrators visibility without SSH access.

**Features**:
- Last successful backup timestamps for each tier
- Storage usage trends and capacity warnings
- Failure alerts with error details
- Quick-view status indicators (green/yellow/red)

**See**: [Ash-Vault #2](ash-vault/enhancements.md)

---

### 6. End-to-End Testing Suite

**Priority**: 🟡 Medium
**Components**: Ash-Thrash, Ash-Bot, Ash-NLP, Ash-Dash
**Complexity**: 🟥 Very High
**Estimated Time**: 20-30 hours

Extend Ash-Thrash to test the complete crisis detection pipeline without requiring actual Discord interaction.

**Test Coverage**:
- Message → Ash-NLP analysis (current focus)
- Message → Ash-Bot processing → Alert generation
- Alert → Ash-Dash session creation → CRT visibility

**See**: [Ash-Thrash #2 & #3](ash-thrash/enhancements.md)

---

## 🤖 Ash-Bot Enhancements

**Full Details**: [ash-bot/enhancements.md](../ash-bot/enhancements.md)

### Active Enhancements

| # | Enhancement | Priority | Complexity | Estimated |
|---|-------------|----------|------------|-----------|
| 1 | Alert Escalation Chain | 🔴 High | 🟧 High | 8-12 hours |
| 2 | Alert Severity Override | 🟡 Medium | 🟦 Low | 2-3 hours |
| 3 | CRT Availability Status | 🟡 Medium | 🟨 Medium | 5-7 hours |
| 4 | Graceful Shutdown Enhancement | 🟡 Medium | 🟦 Low | 2-3 hours |
| 5 | Ash-Dash Integration | 🔴 High | 🟥 Very High | Part of Ash-Dash |
| 6 | Ash-NLP Feedback Loop | 🟡 Medium | 🟧 High | 8-10 hours |

### Key Highlights

**Alert Escalation Chain**: Critical safety net ensuring no crisis alert falls through the cracks. Implements timed escalation: 3 min → re-ping CRT, 5 min → auto-initiate + ping Admins, 10 min → log critical incident.

**CRT Availability Status**: Dynamic auto-initiate timing based on CRT availability. If no CRT available, auto-initiate faster.

### Research Items

- R-001: Sentiment Trend Analysis - Detecting users trending toward crisis
- R-002: Community Health Metrics - Aggregate anonymous metrics
- R-003: Peer Support Matching - Facilitating non-crisis peer connections
- R-004: Crisis Prevention Resources - Proactive resource sharing

---

## 🧠 Ash-NLP Enhancements

**Full Details**: [ash-nlp/enhancements.md](../ash-nlp/enhancements.md)

### Active Enhancements

| # | Enhancement | Priority | Complexity | Estimated |
|---|-------------|----------|------------|-----------|
| 1 | Conversation Context Window | 🔴 High | 🟧 High | 12-16 hours |
| 2 | Crisis Team Feedback Loop | 🔴 High | 🟥 Very High | 20-30 hours |
| 3 | Confidence Threshold Auto-Tuning | 🟡 Medium | 🟨 Medium | 6-8 hours |
| 4 | Custom Vocabulary Expansion | 🟡 Medium | 🟨 Medium | 6-10 hours |

### Key Highlights

**Conversation Context Window**: Analyze sequences of messages (5-10 over 30 minutes) to catch gradual crisis escalation that single-message analysis might miss. Builds on existing context-aware analysis.

**Custom Vocabulary Expansion**: Add community-specific terms, slang, and code words. Critical for LGBTQIA+ community language patterns that generic models may not recognize.

**Example Vocabulary**:
```json
{
  "crisis_indicators": [
    {"term": "rainbow bridge", "weight": 0.8, "context": "pet loss, may indicate grief"}
  ],
  "safe_modifiers": [
    {"term": "hyperbole warning", "weight": -0.3, "context": "user signaling exaggeration"}
  ]
}
```

### Research Items

- R-001: Smaller Distilled Models - Quantized models for lower latency
- R-002: Community-Specific Fine-Tuning - LGBTQIA+-specific language patterns

---

## 📊 Ash-Dash Enhancements

**Full Details**: [ash-dash/enhancements.md](../ash-dash/enhancements.md)

### Active Enhancements

| # | Enhancement | Priority | Complexity | Estimated |
|---|-------------|----------|------------|-----------|
| 1 | ~~Collapsible Sidebar~~ | ✅ | ✅ | ✅ Implemented |
| 2 | ~~Session Claim Button~~ | ✅ | ✅ | ✅ Implemented |
| 3 | Note Templates | 🔴 High | 🟨 Medium | 3-5 hours |
| 4 | Saved Search Filters | 🟡 Medium | 🟦 Low | 2-3 hours |
| 5 | Shift Handoff View | 🔴 High | 🟨 Medium | 5-7 hours |
| 6 | Session Priority Flag | 🟡 Medium | 🟦 Low | 2-3 hours |
| 7 | Session Transfer | 🔴 High | 🟨 Medium | 4-5 hours |
| 8 | Session Tags/Labels | 🟡 Medium | 🟨 Medium | 6-8 hours |
| 9 | Archive Search | 🟡 Medium | 🟨 Medium | 6-8 hours |
| 10 | User Risk Profile Summary | 🟡 Medium | 🟧 High | 10-14 hours |
| 11 | Dashboard Widget Customization | 🟢 Low | 🟨 Medium | 6-8 hours |

### Key Highlights

**Shift Handoff View**: Summary of what happened since CRT member last logged in. Critical for situational awareness at shift start: new sessions, escalations, closed sessions, notes added.

**Session Transfer**: Formal handoff of claimed sessions between CRT members with optional handoff notes and audit logging. Essential for clean shift transitions.

**User Risk Profile Summary**: Aggregate view of a Discord user's historical patterns - session frequency, severity trends, common themes, response patterns. Better context for responding to "frequent fliers".

### Research Items

- RE-001: Real-time Collaboration - Multiple CRT members editing notes simultaneously

---

## 🔒 Ash-Vault Enhancements

**Full Details**: [ash-vault/enhancements.md](../ash-vault/enhancements.md)

### Active Enhancements

| # | Enhancement | Priority | Complexity | Estimated |
|---|-------------|----------|------------|-----------|
| 1 | Ash-Dash Archive Integration | 🔴 High | 🟧 High | 12-16 hours |
| 2 | Backup Health Dashboard Widget | 🔴 High | 🟨 Medium | 6-8 hours |
| 3 | Automated Backup Verification | 🟡 Medium | 🟨 Medium | 6-8 hours |
| 4 | Retention Policy Enforcement | 🟡 Medium | 🟦 Low | 3-4 hours |

### Key Highlights

**Automated Backup Verification**: Periodic integrity checks by performing test restores and comparing checksums. Catches silent data corruption before actual disaster recovery is needed.

**Retention Policy Enforcement**: Automatic pruning of old snapshots and B2 objects (7 daily, 4 weekly, 12 monthly). Prevents storage exhaustion.

### Research Items

- R-001: Immutable Backups (WORM) - Write-once-read-many for ransomware protection

---

## 🧪 Ash-Thrash Enhancements

**Full Details**: [ash-thrash/enhancements.md](../ash-thrash/enhancements.md)

### Active Enhancements

| # | Enhancement | Priority | Complexity | Estimated |
|---|-------------|----------|------------|-----------|
| 1 | Multi-Consensus Algorithm Testing | 🟡 Medium | 🟨 Medium | 6-8 hours |
| 2 | Discord Message Simulation | 🟡 Medium | 🟧 High | 12-16 hours |
| 3 | Ash-Dash API Integration Testing | 🟢 Low | 🟨 Medium | 8-10 hours |

### Key Highlights

**Multi-Consensus Algorithm Testing**: Test each phrase against all four consensus algorithms (weighted_voting, majority_voting, unanimous, conflict_aware) to identify algorithm-specific strengths.

**Discord Message Simulation**: Simulate Discord messages through Ash-Bot's processing pipeline without actual Discord API interaction. Enables comprehensive end-to-end testing without risk of false alerts.

### Research Items

- R-001: Optimal Test Phrase Count Per Category - Statistical significance requirements

---

## 🔬 Ecosystem-Wide Research

These research items span multiple components or affect the ecosystem architecture.

### R-ECO-001: Unified Metrics & Observability

**Status**: 🔬 Research Needed
**Components**: All

**Question**: Should we implement a unified observability stack (Prometheus/Grafana) across all Ash components?

**Considerations**:
- Current state: Each component has `/health` and `/metrics` endpoints
- Ash-Dash Admin interface provides some visibility
- Full observability stack adds infrastructure complexity
- May be overkill for current team size

**Approach**: Evaluate after Ash-Dash Admin Metrics (#10) is implemented to determine if additional tooling is needed.

---

### R-ECO-002: Event-Driven Architecture

**Status**: 🔬 Research Needed
**Components**: All

**Question**: Should we move from request/response to event-driven communication between components?

**Considerations**:
- Current state: REST APIs between components work well
- Event bus (Redis Pub/Sub, RabbitMQ) could enable real-time updates
- Would benefit Shift Handoff View, real-time presence, notifications
- Adds architectural complexity

**Approach**: Start with Redis Pub/Sub for specific use cases (real-time updates in Ash-Dash) before full event-driven migration.

---

### R-ECO-003: Community Health Dashboard

**Status**: 🔬 Research Needed
**Components**: Ash-Bot, Ash-NLP, Ash-Dash

**Question**: Can we provide aggregate, anonymized community health metrics without individual tracking?

**Possible Metrics**:
- Overall sentiment trends (anonymized)
- Peak stress times
- Community mood indicators
- Alert volume trends

**Concerns**:
- Privacy must be paramount
- Potential for misuse or misinterpretation
- Actionability of aggregate data

---

## 🗣️ Community Requests

Space for tracking community-requested features across the ecosystem.

*No ecosystem-wide community requests logged yet.*

### Template for New Requests

```markdown
### CR-ECO-XXX: [Feature Name]
**Requested By**: [Discord username or "Multiple users"]
**Date**: YYYY-MM-DD
**Components**: [Which Ash components affected]
**Priority**: 🔴/🟡/🟢/⚪
**Complexity**: 🟦/🟨/🟧/🟥

**Description**: [What the community wants]

**Use Case**: [Why they want it]

**Notes**: [Implementation thoughts, concerns]
```

---

## 🔄 SQLite to PostgreSQL Migration Guidelines

**Status**: 📋 Reference Documentation
**Implemented In**: Phase 5 - Metrics & History (Ash Core)
**Last Updated**: 2026-01-18

These guidelines ensure that if Ash (Core) needs to migrate from SQLite to PostgreSQL in the future, the transition will be straightforward. **All code using the metrics database must be written with portability in mind.**

### Why SQLite Was Chosen

| Factor | Assessment |
|--------|------------|
| **Write Volume** | 1 snapshot/minute = 1,440/day (trivial for SQLite) |
| **Concurrency** | Single writer (health loop) - SQLite's weakness is irrelevant |
| **Query Complexity** | SQL aggregations work identically to PostgreSQL |
| **Data Criticality** | Historical metrics, not real-time crisis detection |
| **Independence** | No external dependencies, self-contained with Ash (Core) |
| **Backup** | Single file = trivial backup |

### ✅ DO's (Required Practices)

| Practice | Rationale |
|----------|------------|
| **Use standard SQL syntax** | SELECT, INSERT, UPDATE, DELETE, JOINs work identically |
| **Use `INTEGER PRIMARY KEY`** | Works in both SQLite (auto-increment) and PostgreSQL |
| **Store timestamps as ISO 8601 strings** | Universal format: `2026-01-17T14:30:00Z` |
| **Use parameterized queries** | `?` placeholders (SQLite) can be swapped to `$1` (PostgreSQL) |
| **Create a database abstraction layer** | Hide implementation details behind an interface |
| **Use standard aggregate functions** | COUNT, SUM, AVG, MIN, MAX are identical |
| **Store JSON as TEXT** | Both databases handle JSON-in-TEXT; PostgreSQL has native JSON but TEXT works |
| **Use explicit column types** | INTEGER, TEXT, REAL map cleanly to PostgreSQL equivalents |

### ❌ DON'Ts (Practices to Avoid)

| Practice | Problem |
|----------|----------|
| ❌ **SQLite-specific functions** | `datetime('now')` → use Python's datetime instead |
| ❌ **AUTOINCREMENT keyword** | Use `INTEGER PRIMARY KEY` (implicit auto-increment) |
| ❌ **Affinity type coercion** | Don't rely on SQLite's loose typing |
| ❌ **GLOB operator** | Use `LIKE` instead (standard SQL) |
| ❌ **PRAGMA statements in queries** | Configuration only, not in application logic |
| ❌ **Bare column defaults** | Use explicit `DEFAULT` keyword |
| ❌ **TRUE/FALSE literals** | Use `1`/`0` for booleans (portable) |
| ❌ **String concatenation with `\|\|` in WHERE** | Works but test PostgreSQL compatibility |
| ❌ **LIMIT without ORDER BY** | Results non-deterministic; always specify ORDER BY |

### Database Abstraction Pattern

```python
# src/managers/metrics/database.py

from abc import ABC, abstractmethod

class MetricsDatabaseInterface(ABC):
    """Abstract interface for metrics storage - enables future PostgreSQL migration."""
    
    @abstractmethod
    async def initialize(self) -> None: ...
    
    @abstractmethod
    async def store_snapshot(self, snapshot: HealthSnapshot) -> int: ...
    
    @abstractmethod
    async def record_incident(self, incident: Incident) -> int: ...
    
    @abstractmethod
    async def get_uptime(self, component: str, days: int) -> UptimeMetrics: ...
    
    @abstractmethod
    async def cleanup_old_data(self, retention_config: dict) -> int: ...
    
    @abstractmethod
    async def close(self) -> None: ...


class SQLiteMetricsDatabase(MetricsDatabaseInterface):
    """SQLite implementation of metrics storage."""
    # Current implementation


# Future: class PostgresMetricsDatabase(MetricsDatabaseInterface):
```

### Migration Checklist (For Future Use)

When migrating to PostgreSQL:

1. [ ] Create `PostgresMetricsDatabase` implementing `MetricsDatabaseInterface`
2. [ ] Update schema: `INTEGER PRIMARY KEY` → `SERIAL PRIMARY KEY`
3. [ ] Update schema: `TEXT` for timestamps → `TIMESTAMPTZ`
4. [ ] Update parameter placeholders: `?` → `$1, $2, ...`
5. [ ] Update factory function to return PostgreSQL implementation
6. [ ] Write one-time data migration script
7. [ ] Test all queries with PostgreSQL
8. [ ] Update docker-compose with PostgreSQL container
9. [ ] Add PostgreSQL secrets

### Type Mapping Reference

| SQLite | PostgreSQL | Notes |
|--------|------------|-------|
| `INTEGER PRIMARY KEY` | `SERIAL PRIMARY KEY` | Auto-increment |
| `INTEGER` | `INTEGER` or `BIGINT` | Identical |
| `TEXT` | `TEXT` or `VARCHAR(n)` | Identical |
| `REAL` | `REAL` or `DOUBLE PRECISION` | Identical |
| `TEXT` (datetime) | `TIMESTAMPTZ` | PostgreSQL has native timestamps |
| `TEXT` (JSON) | `JSONB` | PostgreSQL has native JSON |

### Reference Implementation

See `ash/src/managers/metrics/database.py` for the current SQLite implementation following these guidelines.

---

## 📝 How To Add Ideas

### For Component-Specific Enhancements

Add ideas directly to the component's `enhancements.md` file:
- [ash-bot/enhancements.md](../ash-bot/enhancements.md)
- [ash-nlp/enhancements.md](../ash-nlp/enhancements.md)
- [ash-dash/enhancements.md](../ash-dash/enhancements.md)
- [ash-vault/enhancements.md](../ash-vault/enhancements.md)
- [ash-thrash/enhancements.md](../ash-thrash/enhancements.md)

### For Cross-Component or Ecosystem Enhancements

1. **Discuss First**: Bring up in conversation before adding to document
2. **Identify Components**: Determine which Ash components are affected
3. **Categorize**: Place in appropriate section
4. **Document**:
   - Brief description
   - Affected components
   - Priority and complexity estimate
   - Dependencies
   - Implementation notes
   - Benefit statement
5. **Update Date**: Update "Last Updated" at top of document
6. **Cross-Reference**: Add references in affected component documents

### Section Guidelines

- **Cross-Component Priorities**: Multi-component features with dependencies
- **Component Sections**: Summaries with links to detailed docs
- **Ecosystem-Wide Research**: Ideas spanning multiple components
- **Community Requests**: Feature requests from The Alphabet Cartel community

---

## 📊 Enhancement Summary by Priority

### 🔴 High Priority (Schedule Soon)

| Enhancement | Component(s) | Complexity |
|-------------|--------------|------------|
| Ash-Dash ↔ Ash-Vault Verification | Ash-Dash, Ash-Vault | 🟨 Medium |
| Alert Escalation Chain | Ash-Bot | 🟧 High |
| Conversation Context Window | Ash-NLP | 🟧 High |
| CRT Feedback Loop | All | 🟥 Very High |
| Note Templates | Ash-Dash | 🟨 Medium |
| Shift Handoff View | Ash-Dash | 🟨 Medium |
| Session Transfer | Ash-Dash | 🟨 Medium |
| Backup Health Dashboard | Ash-Vault, Ash-Dash | 🟨 Medium |
| Ash-Dash Archive Integration | Ash-Vault | 🟧 High |

### 🟡 Medium Priority (When Capacity Allows)

| Enhancement | Component(s) | Complexity |
|-------------|--------------|------------|
| Alert Severity Override | Ash-Bot | 🟦 Low |
| CRT Availability Status | Ash-Bot | 🟨 Medium |
| Confidence Threshold Auto-Tuning | Ash-NLP | 🟨 Medium |
| Custom Vocabulary Expansion | Ash-NLP | 🟨 Medium |
| Saved Search Filters | Ash-Dash | 🟦 Low |
| Session Tags/Labels | Ash-Dash | 🟨 Medium |
| Archive Search | Ash-Dash | 🟨 Medium |
| User Risk Profile Summary | Ash-Dash | 🟧 High |
| Automated Backup Verification | Ash-Vault | 🟨 Medium |
| Multi-Consensus Algorithm Testing | Ash-Thrash | 🟨 Medium |
| Discord Message Simulation | Ash-Thrash | 🟧 High |

---

## 📝 Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-01-17 | v5.0.6 | Marked LoggingConfigManager Colorization Enforcement as IMPLEMENTED (Phase 6 complete) | PapaBearDoes |
| 2026-01-18 | v5.0.5 | Added SQLite to PostgreSQL Migration Guidelines section from Phase 5 planning | PapaBearDoes |
| 2026-01-17 | v5.0.4 | Marked Per-Module Discord Alert Webhooks as IMPLEMENTED (Phase 4 complete) | PapaBearDoes |
| 2026-01-17 | v5.0.3 | Added Per-Module Discord Alert Webhooks enhancement for independent alert routing | PapaBearDoes |
| 2026-01-15 | v5.0.2 | Added LoggingConfigManager Colorization Enforcement as first priority (Charter v5.2 Rule #9 compliance) | PapaBearDoes |
| 2026-01-12 | v5.0.1 | Created ecosystem umbrella enhancements document | PapaBearDoes |

---

**Built with care for chosen family** 🏳️‍🌈
