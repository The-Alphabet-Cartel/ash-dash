---
title: "Ash-Bot - v5.0 Development Roadmap"
description: "Roadmap for the v5.0 recode of Ash-Bot, the Crisis Detection Discord Bot"
category: roadmap
tags:
  - roadmap
  - planning
  - ash-bot
author: "PapaBearDoes"
version: "5.0"
last_updated: "2026-01-20"
---
# Ash-Bot: v5.0 Development Roadmap

============================================================================
**Ash-Bot**: Crisis Detection Discord Bot
**The Alphabet Cartel** - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================

**Document Version**: v5.0.14
**Created**: 2026-01-03
**Last Updated**: 2026-01-20
**Status**: ✅ Complete (All 9 Phases)
**Repository**: https://github.com/the-alphabet-cartel/ash-bot

---

## Table of Contents

1. [Mission Statement](#-mission-statement)
2. [Executive Summary](#-executive-summary)
3. [Architecture Overview](#-architecture-overview)
4. [Technology Stack](#-technology-stack)
5. [Phase Overview](#-phase-overview)
6. [Detailed Phase Breakdown](#-detailed-phase-breakdown)
7. [Security Considerations](#-security-considerations)
8. [Infrastructure & Deployment](#-infrastructure--deployment)
9. [Progress Summary](#-progress-summary)
10. [Success Criteria](#-success-criteria)
11. [Future Enhancements](#-future-enhancements)
12. [Change Log](#-change-log)

---

## 🎯 Mission Statement

```
MISSION - NEVER TO BE VIOLATED:
    Monitor  → Send messages to Ash-NLP for crisis classification
    Alert    → Notify Crisis Response Team via embeds when crisis detected
    Track    → Maintain user history for escalation pattern detection
    Protect  → Safeguard our LGBTQIA+ community through early intervention
```

---

## 📋 Executive Summary

Ash-Bot is the Discord frontend for the Ash Crisis Detection Ecosystem. It serves as the primary interface between The Alphabet Cartel's Discord community and the crisis detection infrastructure.

### Key Capabilities

- **Real-time Monitoring**: Listens to configured channels and forwards messages to Ash-NLP for analysis
- **Intelligent Alerting**: Routes crisis alerts to appropriate CRT channels based on severity
- **User History**: Maintains rolling message history in Redis for escalation pattern detection
- **AI Support**: Provides "Talk to Ash" functionality via Claude API for immediate conversational support
- **CRT Tools**: Slash commands for Crisis Response Team workflow management

### Current Status

Ash-Bot v5.0 is **complete** and running in production. All 9 phases complete with 600+ tests passing, including CRT workflow enhancements (slash commands, session handoff, follow-up check-ins).

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Ash-Bot Architecture                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    Discord Gateway                                                          │
│         │                                                                   │
│         ▼                                                                   │
│    ┌──────────────────────────────────────────────────────────────────┐     │
│    │                      Ash-Bot (discord.py)                        │     │
│    │                                                                  │     │
│    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐    │     │
│    │  │ Discord      │  │ Alert        │  │ Ash Personality      │    │     │
│    │  │ Manager      │  │ Dispatcher   │  │ (Claude API)         │    │     │
│    │  └──────────────┘  └──────────────┘  └──────────────────────┘    │     │
│    │         │                 │                    │                 │     │
│    │         ▼                 ▼                    ▼                │     │
│    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐    │     │
│    │  │ NLP Client   │  │ Embed        │  │ Session              │    │     │
│    │  │ Manager      │  │ Builder      │  │ Manager              │    │     │
│    │  └──────────────┘  └──────────────┘  └──────────────────────┘    │     │
│    │         │                                                        │     │
│    └─────────┼────────────────────────────────────────────────────────┘     │
│              │                                                              │
│              ▼                                                              │
│    ┌───────────────────┐    ┌──────────────────┐                            │
│    │     Ash-NLP       │    │      Redis       │                            │
│    │   (Port 30880)    │    │  (User History)  │                            │
│    └───────────────────┘    └──────────────────┘                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Severity Behavior Matrix

| Severity | Store | Alert | Channel | CRT Ping | Ash Behavior |
|----------|-------|-------|---------|----------|--------------|
| SAFE/NONE | ❌ | ❌ | - | ❌ | None |
| LOW | ✅ | ❌ | - | ❌ | None |
| MEDIUM | ✅ | ✅ | #monitor-queue | ❌ | Monitor silently |
| HIGH | ✅ | ✅ | #crisis-response | ✅ | Talk to Ash button |
| CRITICAL | ✅ | ✅ | #critical-response | ✅ | Talk to Ash button |

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Runtime** | Python 3.11 | Primary language |
| **Discord Library** | discord.py 2.x | Discord API interaction |
| **HTTP Client** | httpx | Async HTTP for Ash-NLP API |
| **Cache/Storage** | Redis | User history, session data |
| **AI Integration** | Anthropic Claude API | Ash personality conversations |
| **Configuration** | JSON + Environment | Clean Architecture compliant |
| **Health Monitoring** | asyncio HTTP server | /health, /metrics endpoints |
| **Containerization** | Docker | Deployment |

### Target Performance

| Metric | Target |
|--------|--------|
| Message-to-response latency | < 750ms |
| Ash-NLP API timeout | 5s (with retry) |
| Redis operations | < 50ms |
| Concurrent Ash sessions | 10+ |
| Claude API response | 1-3s |

---

## 📅 Phase Overview

| Phase | Name | Focus | Status |
|-------|------|-------|--------|
| 0 | Foundation Cleanup | Docker, configs, headers | ✅ Complete |
| 1 | Discord Connectivity | Bot connection, NLP integration | ✅ Complete |
| 2 | Redis Integration | User history, TTL management | ✅ Complete |
| 3 | Alert System | Embeds, buttons, severity routing | ✅ Complete |
| 4 | Ash Personality | Claude API, DM sessions | ✅ Complete |
| 5 | Production Hardening | Health, metrics, circuit breakers | ✅ Complete |
| 6 | Final Testing | End-to-end validation | ✅ Complete |
| 7 | Core Safety | Auto-initiate, opt-out, sensitivity | ✅ Complete |
| 8 | Metrics & Reporting | Response tracking, weekly reports | ✅ Complete |
| 9 | CRT Workflow | Slash commands, handoff, check-ins | ✅ Complete |

---

## 🔐 Security Considerations

1. **Authentication**: Discord bot token via Docker secrets
2. **Authorization**: Role-based slash command permissions (CRT Member vs Admin)
3. **Data Protection**: User history TTL in Redis (configurable retention)
4. **API Security**: Claude API key via Docker secrets
5. **Rate Limiting**: Cooldown manager prevents alert flooding
6. **Audit Trail**: All CRT actions logged with timestamps

---

## 🖥️ Infrastructure & Deployment

### Deployment Configuration

| Setting | Value |
|---------|-------|
| **Host** | Lofn (10.20.30.253) |
| **Container** | ash-bot |
| **Internal Port** | 8080 (health) |
| **External Port** | 30881 |
| **Health Check** | HTTP /health |

### Key Endpoints

| Service | URL |
|---------|-----|
| Ash-NLP API | `http://ash-nlp:30880` |
| Redis | `ash-redis:6379` |
| Claude API | `https://api.anthropic.com` |
| Health | `http://localhost:8080/health` |
| Metrics | `http://localhost:8080/metrics` |

### File Structure

```
ash-bot/
├── src/
│   ├── managers/
│   │   ├── config_manager.py
│   │   ├── secrets_manager.py
│   │   ├── discord/
│   │   ├── alerting/
│   │   ├── storage/
│   │   ├── nlp/
│   │   ├── ash/
│   │   ├── utils/
│   │   ├── metrics/
│   │   └── health/
│   ├── models/
│   ├── prompts/
│   └── views/
├── config/
│   └── default.json
├── tests/
├── docs/
├── main.py
├── Dockerfile
└── docker-compose.yml
```

---

## 📊 Progress Summary

### Completed Phases: 9 of 9 🎉

| Phase | Status | Date | Key Deliverables |
|-------|--------|------|------------------|
| Phase 0 | ✅ Complete | 2026-01-03 | Docker, configs, headers |
| Phase 1 | ✅ Complete | 2026-01-03 | Discord, NLP, 77 tests |
| Phase 2 | ✅ Complete | 2026-01-04 | Redis, history, 90+ tests |
| Phase 3 | ✅ Complete | 2026-01-04 | Alerts, embeds, 89 tests |
| Phase 4 | ✅ Complete | 2026-01-04 | Ash AI, Claude, 69+ tests |
| Phase 5 | ✅ Complete | 2026-01-04 | Health, metrics, circuit breakers |
| Phase 6 | ✅ Complete | 2026-01-04 | E2E testing, docs |
| Phase 7 | ✅ Complete | 2026-01-05 | Auto-initiate, opt-out, 65+ tests |
| Phase 8 | ✅ Complete | 2026-01-05 | Metrics, reports, 127 tests |
| Phase 9 | ✅ Complete | 2026-01-05 | Slash commands, handoff, follow-ups, 107 tests |

**Total Tests**: 600+ (unit and integration tests across all phases)

---

## ✅ Success Criteria

Core functionality complete:

1. ✅ Bot connects to Discord and monitors configured channels
2. ✅ Messages forwarded to Ash-NLP for classification
3. ✅ Alerts routed to correct CRT channels by severity
4. ✅ Rich embeds with Acknowledge and Talk to Ash buttons
5. ✅ User history maintained in Redis with TTL
6. ✅ Ash personality provides AI support via Claude
7. ✅ Auto-initiate when CRT doesn't respond
8. ✅ User opt-out functionality
9. ✅ Health and metrics endpoints operational
10. ✅ Circuit breakers protect external services
11. ✅ Weekly CRT reports generated
12. ✅ Data retention policies enforced
13. ✅ CRT slash commands operational
14. ✅ Session handoff between CRT members
15. ✅ Follow-up check-in system

---

## 🔜 Future Enhancements

See [enhancements.md](enhancements.md) for detailed planning.


---

## 📝 Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-01-20 | v5.0.14 | **Phase 9 COMPLETE** - Updated roadmap to reflect all 9 phases complete; 600+ total tests | PapaBearDoes |
| 2026-01-12 | v5.0.13 | Roadmap restructured to hybrid template format | PapaBearDoes |
| 2026-01-05 | v5.0.12 | Phase 9.1 complete - CRT slash commands | PapaBearDoes |
| 2026-01-05 | v5.0.11 | Phase 8 complete - PUID/PGID container support | PapaBearDoes |
| 2026-01-05 | v5.0.10 | Phase 8 complete - Response metrics, weekly reports, data retention | PapaBearDoes |
| 2026-01-05 | v5.0.9 | Phase 7 complete - Auto-initiate, user opt-out, channel sensitivity | PapaBearDoes |
| 2026-01-04 | v5.0.8 | Phase 5 complete - Health, metrics, error recovery, documentation | PapaBearDoes |
| 2026-01-04 | v5.0.7 | Phase 4 complete - Ash AI, Claude integration, 200+ total tests | PapaBearDoes |
| 2026-01-04 | v5.0.6 | Phase 3 complete - Alert system, embeds, buttons, 130+ tests | PapaBearDoes |
| 2026-01-04 | v5.0.5 | Phase 2 complete - Redis storage, history, 68 tests passing | PapaBearDoes |
| 2026-01-03 | v5.0.4 | Phase 1 complete - Discord, NLP, 77 tests passing | PapaBearDoes |
| 2026-01-03 | v5.0.3 | Phase 0 complete - headers, configs, Docker verified | PapaBearDoes |
| 2026-01-03 | v5.0.2 | Added Docker dev environment to Phase 0 | PapaBearDoes |
| 2026-01-03 | v5.0.1 | Initial roadmap created | PapaBearDoes |

---

**Built with care for chosen family** 🏳️‍🌈
