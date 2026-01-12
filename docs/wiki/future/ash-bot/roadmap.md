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
last_updated: "2026-01-12"
---
# Ash-Bot: v5.0 Development Roadmap

============================================================================
**Ash-Bot**: Crisis Detection Discord Bot
**The Alphabet Cartel** - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================

**Document Version**: v5.0.13
**Created**: 2026-01-03
**Last Updated**: 2026-01-12
**Status**: 🟢 Production Ready (Phase 9 Enhancements In Progress)
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

Ash-Bot v5.0 is **production ready** and running. Core functionality (Phases 0-8) is complete with 500+ tests passing. Phase 9 CRT workflow enhancements are in progress.

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
| 9 | CRT Workflow | Slash commands, handoff, check-ins | 🟡 In Progress |

---

## 📋 Detailed Phase Breakdown

### Phase 0: Foundation Cleanup ✅ Complete
**Goal**: Establish working Docker dev environment and update existing files

- [x] Docker environment setup and verification
- [x] Clean Architecture header updates
- [x] Configuration management (JSON + env)
- [x] LoggingConfigManager integration
- [x] Base test framework

**Completed**: 2026-01-03
**Documentation**: [Phase 0 Completion Report](phase0/complete.md)

---

### Phase 1: Discord Connectivity ✅ Complete
**Goal**: Basic bot connectivity, channel monitoring, NLP integration

- [x] DiscordManager with event handling
- [x] ChannelConfigManager for monitored channels
- [x] NLPClientManager with retry logic
- [x] NLP request/response models
- [x] 77 unit tests passing

**Completed**: 2026-01-03
**Documentation**: [Phase 1 Completion Report](phase1/complete.md)

---

### Phase 2: Redis Integration ✅ Complete
**Goal**: Persistent storage, user history tracking, TTL management

- [x] RedisManager with connection pooling
- [x] UserHistoryManager for message tracking
- [x] History models with Pydantic
- [x] Graceful degradation when Redis unavailable
- [x] 90+ unit tests passing

**Completed**: 2026-01-04
**Documentation**: [Phase 2 Completion Report](phase2/complete.md)

---

### Phase 3: Alert System ✅ Complete
**Goal**: Full alerting pipeline with embeds, buttons, severity routing

- [x] AlertDispatcher for routing logic
- [x] EmbedBuilder for rich Discord embeds
- [x] CooldownManager to prevent alert spam
- [x] AlertButtons view (Acknowledge, Talk to Ash)
- [x] 89 unit tests passing

**Completed**: 2026-01-04
**Documentation**: [Phase 3 Completion Report](phase3/complete.md)

---

### Phase 4: Ash Personality ✅ Complete
**Goal**: AI-powered conversational support via Claude API

- [x] ClaudeClientManager with API integration
- [x] AshSessionManager for DM session lifecycle
- [x] AshPersonalityManager for system prompts
- [x] Safety guardrails with resource injection
- [x] Session timeout (5 min idle, 10 min max)
- [x] 69+ unit tests passing

**Completed**: 2026-01-04
**Documentation**: [Phase 4 Completion Report](phase4/complete.md)

---

### Phase 5: Production Hardening ✅ Complete
**Goal**: Production-grade infrastructure, monitoring, error recovery

- [x] CircuitBreaker utility class
- [x] retry_with_backoff decorator
- [x] MetricsManager (Prometheus format)
- [x] HealthManager with component registration
- [x] HealthServer (6 endpoints)
- [x] Operational documentation (runbook, troubleshooting, deployment)
- [x] 40+ unit tests passing

**Completed**: 2026-01-04
**Documentation**: [Phase 5 Completion Report](phase5/completion_report.md)

---

### Phase 6: Final Testing & Documentation ✅ Complete
**Goal**: End-to-end testing, final documentation, deployment verification

- [x] Integration test suite
- [x] End-to-end flow validation
- [x] Documentation review
- [x] 50+ tests passing

**Completed**: 2026-01-04
**Documentation**: [Phase 6 Completion Report](phase6/complete.md)

---

### Phase 7: Core Safety & User Preferences ✅ Complete
**Goal**: Auto-initiation, user opt-out, channel sensitivity

- [x] Auto-initiate Ash when CRT doesn't respond (3 min)
- [x] User opt-out via reaction
- [x] Per-channel sensitivity adjustments
- [x] 65+ new tests passing

**Completed**: 2026-01-05
**Documentation**: [Phase 7 Completion Report](phase7/complete.md)

---

### Phase 8: Metrics & Reporting ✅ Complete
**Goal**: Response time tracking, weekly reports, data retention

- [x] Alert response time metrics
- [x] Automated weekly CRT reports
- [x] Data retention and cleanup policies
- [x] PUID/PGID container support
- [x] 127 new tests passing

**Completed**: 2026-01-05
**Documentation**: [Phase 8 Completion Report](phase8/complete.md)

---

### Phase 9: CRT Workflow Enhancements 🟡 In Progress
**Goal**: Slash commands, session handoff, follow-up check-ins

#### Step 9.1: CRT Slash Commands ✅ Complete
- [x] `/ash status` - System status overview
- [x] `/ash stats` - CRT statistics
- [x] `/ash history` - User history lookup
- [x] `/ash config` - Configuration view
- [x] `/ash notes` - Session notes
- [x] `/ash optout` - Manage user opt-outs
- [x] Permission system (CRT/Admin roles)
- [x] 27+ unit tests

**Completed**: 2026-01-05
**Documentation**: [Phase 9.1 Completion Report](phase9/phase9_1_complete.md)

#### Step 9.2: Session Handoff & Notes 🔲 Ready
- [ ] CRT-to-CRT session handoff
- [ ] Handoff notification system
- [ ] Session notes persistence
- [ ] Handoff audit logging

#### Step 9.3: Follow-Up Check-Ins 🔲 Ready
- [ ] Scheduled follow-up reminders
- [ ] Check-in message templates
- [ ] Follow-up tracking and completion

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

### Completed Phases: 8.5 of 9

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
| Phase 9 | 🟡 In Progress | - | Slash commands (9.1 ✅), handoff, check-ins |

**Total Tests**: 500+ (unit and integration tests across all phases)

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
14. 🔲 Session handoff between CRT members
15. 🔲 Follow-up check-in system

---

## 🔜 Future Enhancements

See [enhancements.md](enhancements.md) for detailed planning.

### Post-v5.0 Backlog

- Web dashboard for CRT analytics
- Historical trend visualization
- Custom alert thresholds per channel
- Multi-guild support
- Webhook integration for external systems
- ML model fine-tuning based on feedback
- Mobile push notifications for CRT
- Scheduled wellness check-ins
- Streaming Ash responses
- Session persistence in Redis
- Session history export for CRT

---

## 📝 Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-01-12 | v5.0.13 | Roadmap restructured to hybrid template format | Claude + PapaBearDoes |
| 2026-01-05 | v5.0.12 | Phase 9.1 complete - CRT slash commands | Claude + PapaBearDoes |
| 2026-01-05 | v5.0.11 | Phase 8 complete - PUID/PGID container support | Claude + PapaBearDoes |
| 2026-01-05 | v5.0.10 | Phase 8 complete - Response metrics, weekly reports, data retention | Claude + PapaBearDoes |
| 2026-01-05 | v5.0.9 | Phase 7 complete - Auto-initiate, user opt-out, channel sensitivity | Claude + PapaBearDoes |
| 2026-01-04 | v5.0.8 | Phase 5 complete - Health, metrics, error recovery, documentation | Claude + PapaBearDoes |
| 2026-01-04 | v5.0.7 | Phase 4 complete - Ash AI, Claude integration, 200+ total tests | Claude + PapaBearDoes |
| 2026-01-04 | v5.0.6 | Phase 3 complete - Alert system, embeds, buttons, 130+ tests | Claude + PapaBearDoes |
| 2026-01-04 | v5.0.5 | Phase 2 complete - Redis storage, history, 68 tests passing | Claude + PapaBearDoes |
| 2026-01-03 | v5.0.4 | Phase 1 complete - Discord, NLP, 77 tests passing | Claude + PapaBearDoes |
| 2026-01-03 | v5.0.3 | Phase 0 complete - headers, configs, Docker verified | Claude + PapaBearDoes |
| 2026-01-03 | v5.0.2 | Added Docker dev environment to Phase 0 | Claude + PapaBearDoes |
| 2026-01-03 | v5.0.1 | Initial roadmap created | Claude + PapaBearDoes |

---

**Built with care for chosen family** 🏳️‍🌈
