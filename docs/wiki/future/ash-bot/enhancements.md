---
title: "Ash-Bot - Future Enhancements"
description: "Planned features and improvements for Ash-Bot"
category: future
tags:
  - roadmap
  - planning
  - ash-bot
author: "PapaBearDoes"
version: "5.0"
last_updated: "2026-01-11"
---
# Ash-Bot: Future Enhancements & Improvements

============================================================================
**Ash-Bot**: Crisis Detection Discord Bot for The Alphabet Cartel  
**The Alphabet Cartel** - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================

**Document Version**: v5.0  
**Created**: 2026-01-11  
**Phase**: 1 (Future Planning)  
**Status**: 📋 Backlog  
**Last Updated**: 2026-01-11

---

## Table of Contents

1. [Overview](#overview)
2. [Active Enhancements](#active-enhancements)
3. [Back Burner](#back-burner)
4. [Considered But Deferred](#considered-but-deferred)
5. [Requests](#requests)
6. [Research](#research)
7. [How To Add Ideas](#how-to-add-ideas)

---

## 📋 Overview

This document tracks potential enhancements and feature ideas for Ash-Bot beyond the core v5.0 roadmap. Items are organized by priority and implementation complexity.

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

## 🎯 Active Enhancements

Features discussed and approved for future implementation.

### 1. Alert Escalation Chain

**Priority**: 🔴 High  
**Complexity**: 🟧 High  
**Depends On**: None  
**Estimated Time**: 8-12 hours

Implement escalation chain for unacknowledged alerts.

**Features**:
- Alert posted → Wait 3 min
- No response → Ping CRT role again
- Still no response (5 min) → Auto-initiate + ping Admins
- Still no response (10 min) → Log critical incident

**Implementation**:
- Configuration via environment variables:
  ```bash
  BOT_ESCALATION_ENABLED=true
  BOT_ESCALATION_STEP1_MINUTES=3
  BOT_ESCALATION_STEP2_MINUTES=5
  BOT_ESCALATION_STEP3_MINUTES=10
  BOT_ESCALATION_ADMIN_ROLE=Admin
  ```

**Benefit**: Critical safety net ensuring no crisis alert ever falls through the cracks. Even with an attentive CRT, life happens—phones die, meetings run long, people sleep.

---

### 2. Alert Severity Override

**Priority**: 🟡 Medium  
**Complexity**: 🟦 Low  
**Depends On**: None  
**Estimated Time**: 2-3 hours

Allow CRT to manually adjust alert severity after review.

**Features**:
- "Adjust Severity" dropdown in alert embed
- Logging of adjustments with reason
- Metrics tracking for overrides
- Feedback loop for future NLP tuning

**Implementation**:
- Add interaction handler for severity dropdown
- Store adjustments in Redis with reason
- Update session severity in real-time

**Benefit**: Enables CRT to correct false positives/negatives, improving response accuracy and feeding data back to NLP for model improvement.

---

### 3. CRT Availability Status

**Priority**: 🟡 Medium  
**Complexity**: 🟨 Medium  
**Depends On**: None  
**Estimated Time**: 5-7 hours

Allow CRT members to set availability status.

**Features**:
- `/ash available` - Mark self as available
- `/ash away [reason]` - Mark self as away
- Show available CRT count in alerts
- Adjust auto-initiate timing based on CRT availability

**Implementation**:
- Store availability in Redis with TTL
- Display count in alert embeds
- Dynamic auto-initiate delay based on availability

**Benefit**: If no CRT available, auto-initiate faster. If many available, allow more time for manual response.

---

### 4. Graceful Shutdown Enhancement

**Priority**: 🟡 Medium  
**Complexity**: 🟦 Low  
**Depends On**: None  
**Estimated Time**: 2-3 hours

Ensure clean shutdown preserves all pending state.

**Features**:
- Persist pending alerts to Redis before shutdown
- Restore pending alerts on startup
- Resume timers with adjusted remaining time

**Implementation**:
- Signal handler for SIGTERM/SIGINT
- Redis persistence of pending alert state
- Startup recovery routine

**Benefit**: Auto-initiate timers are never lost on restart, ensuring continuity of crisis response.

---

### 5. Ash-Dash Integration

**Priority**: 🔴 High  
**Complexity**: 🟥 Very High  
**Depends On**: Ash-Dash v5.0  
**Estimated Time**: Part of Ash-Dash project

Full web dashboard integration for Ash-Bot.

**Features**:
- WebSocket endpoint for real-time updates
- REST API for dashboard queries
- Authentication token support

**Implementation**:
- Handled primarily by Ash-Dash project
- Ash-Bot provides API endpoints and WebSocket feeds

**Benefit**: Real-time alert feed, user history lookup, session management, analytics, and CRT tools all in one place.

---

### 6. Ash-NLP Feedback Loop

**Priority**: 🟡 Medium  
**Complexity**: 🟧 High  
**Depends On**: Alert Severity Override (#2)  
**Estimated Time**: 8-10 hours (both sides)

Send CRT severity overrides back to NLP for model improvement.

**Features**:
- Automatic feedback when CRT adjusts severity
- Ash-NLP logs feedback for future training data
- Periodic model retraining improves accuracy

**Implementation**:
- API endpoint on Ash-NLP for feedback ingestion
- Ash-Bot sends override data after CRT adjustment
- Storage format for training data extraction

**Benefit**: Continuous improvement of NLP accuracy based on real-world CRT corrections.

---

## ⏸️ Back Burner

Features we may want eventually, but are lower priority.

### Repeat Crisis Detection

**Priority**: ⚪ Someday  
**Complexity**: 🟨 Medium  
**Estimated Time**: 4-6 hours

Track when users have multiple crisis alerts in a short period and escalate accordingly.

**Notes**:
- 2nd alert in 7 days → Note in embed: "⚠️ 2nd alert this week"
- 3rd+ alert in 7 days → Elevated priority, different embed color
- Current community size allows CRT to manually track repeat users
- Revisit when community grows significantly or when onboarding new CRT members

---

### Prometheus Metrics Enhancement

**Priority**: ⚪ Someday  
**Complexity**: 🟨 Medium  
**Estimated Time**: 4-6 hours

Expand Prometheus metrics for better observability.

**Notes**:
- New metrics: session duration, NLP latency, alert severity totals, opt-out counts, followup rates
- Current `/metrics` endpoint is sufficient for now
- Would be nice for advanced monitoring infrastructure

---

### Grafana Dashboard Template

**Priority**: ⚪ Someday  
**Complexity**: 🟦 Low  
**Estimated Time**: 3-4 hours

Create pre-built Grafana dashboard JSON for Ash-Bot metrics.

**Notes**:
- Depends on Prometheus Metrics Enhancement
- Panels for alert volume, response times, NLP latency, session counts, error rates
- Deliverable: `docs/monitoring/grafana-dashboard.json`

---

## 💭 Considered But Deferred

Ideas discussed but not currently planned. May revisit based on team feedback.

| Idea | Reason for Deferral |
|------|---------------------|
| Health Check Dashboard Endpoint | Redundant with Ash-Dash; JSON `/health` remains for programmatic checks |
| Discord Audit Log Integration | Ash-Dash + Redis history cover investigation needs; overhead outweighs gain |
| Shared User Profile Service | Solving a problem that doesn't exist; opt-outs already centralized in Ash-Bot |
| SMS Gateway Integration | Cost, privacy concerns, complexity; Discord mobile notifications suffice |
| Multi-Language Support | English-only server with no plans to change; would require NLP model changes |
| Email Notifications | Adds complexity, requires email collection; Discord notifications sufficient |
| Public Bot Distribution | Purpose-built for TAC; would require significant generalization and support |
| Voice Channel Monitoring | Privacy concerns, technical complexity, limited crisis detection value |
| Quiet Hours Configuration | Auto-initiate handles unresponsive periods; CRT can manage own notifications |
| NLP Response Caching | Adds complexity and edge cases; NLP API is fast enough |
| Structured Logging Enhancement | Current logging sufficient; complexity without immediate benefit |
| Circuit Breaker Tuning | Current hardcoded values work well; no clear use case for configurability |

---

## 🗣️ Requests

Space for tracking community-requested features.

### Template for New Requests

```markdown
### CR-XXX: [Feature Name]
**Requested By**: [Discord username or "Multiple users"]
**Date**: YYYY-MM-DD
**Priority**: 🔴/🟡/🟢/⚪
**Complexity**: 🟦/🟨/🟧/🟥

**Description**: [What the community wants]

**Use Case**: [Why they want it]

**Notes**: [Implementation thoughts, concerns]
```

---

### CR-001: [Placeholder]

**Requested By**: -  
**Date**: -  
**Priority**: -  
**Complexity**: -

**Description**: *No community requests logged yet.*

---

## 🔬 Research

Ideas requiring research before planning.

### R-001: Sentiment Trend Analysis

**Status**: 🔬 Research Needed

**Question**: Can we detect users trending toward crisis before they reach alert threshold?

**Approach**: Track per-user sentiment over time, identify downward trends, proactive gentle check-in (not crisis response).

**Concerns**: Privacy, false positives, user consent.

---

### R-002: Community Health Metrics

**Status**: 🔬 Research Needed

**Question**: Can we provide aggregate community health metrics without individual tracking?

**Possible Metrics**: Overall sentiment trends (anonymized), peak stress times, community mood indicators.

**Concerns**: Privacy, potential misuse, actionability.

---

### R-003: Peer Support Matching

**Status**: 🔬 Research Needed

**Question**: Can we facilitate peer support connections for non-crisis situations?

**Concept**: User opts into peer support, bot connects users with similar experiences, moderated introduction.

**Concerns**: Safety, liability, complexity.

---

### R-004: Crisis Prevention Resources

**Status**: 🔬 Research Needed

**Question**: Can Ash proactively share mental health resources based on detected themes?

**Concept**: Detect themes (anxiety, depression, relationship issues), share relevant resources (not triggered by crisis), educational not clinical.

**Concerns**: Coming across as preachy, accuracy of theme detection.

---

## 📝 How To Add Ideas

When adding new enhancement ideas:

1. **Discuss First**: Bring up in conversation before adding to document
2. **Categorize**: Place in appropriate section (Active, Back Burner, Deferred)
3. **Document**:
   - Brief description
   - Priority and complexity estimate
   - Dependencies (which phase must complete first)
   - Implementation notes
   - Benefit statement
4. **Update Date**: Update "Last Updated" at top of document

---

**Built with care for chosen family** 🏳️‍🌈
