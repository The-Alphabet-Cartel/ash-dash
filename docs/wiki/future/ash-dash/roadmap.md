---
title: "Ash-Dash - v5.0 Development Roadmap"
description: "Roadmap for the v5.0 recode of Ash-Dash, the Crisis Response Dashboard"
category: roadmap
tags:
  - roadmap
  - planning
  - ash-dash
author: "PapaBearDoes"
version: "5.0"
last_updated: "2026-01-20"
---
# Ash-Dash: v5.0 Development Roadmap

============================================================================
**Ash-Dash**: Crisis Response Dashboard
**The Alphabet Cartel** - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================

**Document Version**: v5.0.13
**Created**: 2026-01-06
**Last Updated**: 2026-01-20
**Status**: ✅ Complete (All 11 Phases)
**Repository**: https://github.com/the-alphabet-cartel/ash-dash

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
11. [Known Issues](#-known-issues)
12. [Future Enhancements](#-future-enhancements)
13. [Change Log](#-change-log)

---

## 🎯 Mission Statement

```
MISSION - NEVER TO BE VIOLATED:
    Reveal   → Surface crisis alerts and user escalation patterns in real-time
    Enable   → Equip Crisis Response Teams with tools for swift intervention
    Clarify  → Translate detection data into actionable intelligence
    Protect  → Safeguard our LGBTQIA+ community through vigilant oversight
```

---

## 📋 Executive Summary

Ash-Dash is the Crisis Response Dashboard for The Alphabet Cartel's Discord crisis detection ecosystem. It provides CRT (Crisis Response Team) members and administrators with a web-based interface for monitoring, documentation, and archive management.

### Key Capabilities

- **Real-time Dashboard**: Live metrics, active sessions, crisis trends
- **Session Management**: Searchable history, detailed views, state tracking
- **WYSIWYG Note-Taking**: TipTap editor with auto-save for session documentation
- **Wiki Documentation**: Markdown-based training and reference materials with PDF export
- **Encrypted Archives**: AES-256-GCM encrypted session storage on MinIO
- **Three-Tier RBAC**: CRT Member, CRT Lead, CRT Admin roles via Pocket-ID

### Current Status

Ash-Dash v5.0 is **complete** and production ready. All 11 phases implemented with 101 tests passing, WCAG 2.1 AA accessibility compliance, and comprehensive documentation.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Ash-Dash Architecture                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    NGINX Reverse Proxy (crt.alphabetcartel.net:443)                         │
│           │                                                                 │
│           ▼                                                                 │
│    Pocket-ID (OIDC) ──> Ash-Dash (FastAPI + Vue.js) Port 30883              │
│                                    │                                        │
│         ┌──────────────────────────┼──────────────────────────┐             │
│         │                          │                          │             │
│         ▼                         ▼                          ▼             │
│    ┌─────────┐              ┌─────────────┐           ┌─────────────┐       │
│    │  Redis  │              │ PostgreSQL  │           │    MinIO    │       │
│    │(shared) │              │ (Ash-Dash)  │           │    (Syn)    │       │
│    └─────────┘              └─────────────┘           └─────────────┘       │
│         │                                                    │              │
│         │ (reads Ash-Bot data)                               │              │
│         ▼                                                   ▼              │
│    ┌─────────┐              ┌─────────────┐           ┌─────────────┐       │
│    │ Ash-Bot │<────────────>│   Ash-NLP   │           │  Backblaze  │       │
│    └─────────┘              └─────────────┘           │     B2      │       │
│                                                       └─────────────┘       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI (Python 3.11) | REST API, WebSocket support |
| **Frontend** | Vue.js 3 + Vite | Reactive UI components |
| **Styling** | TailwindCSS | Responsive design, dark/light mode |
| **Database** | PostgreSQL 16 | Persistent data storage |
| **ORM** | SQLAlchemy 2.0 | Database models with Mapped[] annotations |
| **Migrations** | Alembic | Database schema migrations |
| **Cache/Real-time** | Redis (shared with Ash-Bot) | Live session data |
| **Archive Storage** | MinIO on Syn VM (ZFS) | Encrypted long-term storage |
| **Cloud Backup** | Backblaze B2 | Off-site disaster recovery |
| **Authentication** | Pocket-ID (OIDC) | SSO with PKCE flow |
| **Charts** | Chart.js | Dashboard visualizations |
| **Markdown Editor** | TipTap | WYSIWYG note editing |
| **PDF Generation** | WeasyPrint | Documentation export |
| **Encryption** | cryptography (AES-256-GCM) | Archive encryption |
| **Containerization** | Docker | Deployment |

---

## 📅 Phase Overview

| Phase | Name | Focus | Status |
|-------|------|-------|--------|
| 1 | Foundation & Infrastructure | Docker, FastAPI, config | ✅ Complete |
| 2 | Data Layer | PostgreSQL, Redis, models | ✅ Complete |
| 3 | Frontend Foundation | Vue.js, layout, theming | ✅ Complete |
| 4 | Dashboard & Metrics | Charts, polling, metrics cards | ✅ Complete |
| 5 | Session Management | History, detail views, state | ✅ Complete |
| 6 | Notes System | TipTap editor, auto-save | ✅ Complete |
| 7 | Documentation Wiki | Markdown, PDF export, search | ✅ Complete |
| 8 | Archive Infrastructure | Syn VM, ZFS, MinIO | ✅ Complete |
| 9 | Archive System | Encryption, workflows, retention | ✅ Complete |
| 10 | Authentication & Authorization | OIDC, RBAC, admin UI | ✅ Complete |
| 11 | Polish & Documentation | QA, accessibility, docs | ✅ Complete |

---

## 🔐 Security Considerations

1. **Authentication**: Pocket-ID OIDC with PKCE flow
2. **Authorization**: Three-tier RBAC (Member/Lead/Admin)
3. **Session Management**: Redis-based server-side sessions
4. **Data Encryption**:
   - At-rest: ZFS native encryption on Syn VM
   - In-transit: HTTPS via NGINX
   - Application-level: AES-256-GCM for archived sessions (double encryption)
5. **Secrets Management**: Docker secrets for sensitive values
6. **Audit Logging**: All administrative actions logged with user tracking
7. **Note Ownership**: Users can only edit their own notes

---

## 🖥️ Infrastructure & Deployment

### Deployment Configuration

| Setting | Value |
|---------|-------|
| **Host** | Lofn (10.20.30.253) |
| **Container** | ash-dash |
| **Port** | 30883 |
| **Database** | PostgreSQL 16 |
| **Health Check** | HTTP /health |

### External Dependencies

| Service | Host | Port |
|---------|------|------|
| Redis (shared) | ash-redis | 6379 |
| MinIO API | Syn (10.20.30.202) | 30884 |
| MinIO Console | Syn (10.20.30.202) | 30885 |
| Pocket-ID | pocket-id | 443 |

### File Structure

```
ash-dash/
├── src/
│   ├── api/
│   │   └── main.py
│   ├── config/
│   │   └── default.json
│   ├── managers/
│   │   ├── config_manager.py
│   │   ├── secrets_manager.py
│   │   ├── auth/
│   │   └── archive/
│   ├── models/
│   │   └── database.py
│   ├── repositories/
│   └── services/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── stores/
│   │   └── services/
│   └── vite.config.js
├── docs/
│   └── wiki/
├── tests/
├── Dockerfile
└── docker-compose.yml
```

---

## 📊 Progress Summary

### Completed Phases: 11 of 11 🎉

| Phase | Status | Date | Key Deliverables |
|-------|--------|------|------------------|
| Phase 1 | ✅ Complete | 2026-01-06 | Docker, FastAPI, Config, Health API |
| Phase 2 | ✅ Complete | 2026-01-07 | PostgreSQL, Redis, Models, Repositories |
| Phase 3 | ✅ Complete | 2026-01-07 | Vue.js, Layout, Theming, Router |
| Phase 4 | ✅ Complete | 2026-01-07 | Dashboard, Charts, Metrics, Polling |
| Phase 5 | ✅ Complete | 2026-01-07 | Sessions List, Detail, History, Actions |
| Phase 6 | ✅ Complete | 2026-01-08 | TipTap Editor, Notes CRUD, Auto-save |
| Phase 7 | ✅ Complete | 2026-01-09 | Wiki System, PDF Export, Search |
| Phase 8 | ✅ Complete | 2026-01-09 | Syn VM, MinIO, MinIOManager, Ash-Vault |
| Phase 9 | ✅ Complete | 2026-01-10 | Archive System, Encryption, Retention |
| Phase 10 | ✅ Complete | 2026-01-10 | OIDC Auth, RBAC, Admin UI |
| Phase 11 | ✅ Complete | 2026-01-10 | UI Polish, Accessibility, Documentation, Tests |

**Total Tests**: 101 tests across 7 test files

---

## ✅ Success Criteria

All criteria met:

1. ✅ CRT members can log in via Pocket-ID and view the dashboard
2. ✅ Dashboard displays real-time metrics and active sessions
3. ✅ Session history is searchable and filterable
4. ✅ Session detail view shows all crisis data and user history
5. ✅ WYSIWYG notes editor allows documentation during sessions
6. ✅ Notes lock after session close (admin can unlock)
7. ✅ Documentation wiki renders from Markdown files
8. ✅ PDF export works for any document
9. ✅ Sessions can be archived to encrypted storage
10. ✅ Three-tier RBAC enforced (Member/Lead/Admin)
11. ✅ Admin UI shows CRT roster, audit logs, system health
12. ✅ Dark/light mode works throughout
13. ✅ Responsive design works on tablet and desktop
14. ✅ All code follows Clean Architecture Charter
15. ✅ UI is polished with accessibility (WCAG 2.1 AA)
16. ✅ Comprehensive documentation (user, admin, operations)
17. ✅ Test suite passes (101 tests)
18. ✅ QA review complete (security, functionality)

---

## ⚠️ Known Issues

### ~~Ash-Vault Connection Verification Required~~ ✅ VERIFIED

**Status**: ✅ Verified (2026-01-20)
**Priority**: ~~Medium~~ Closed
**Affects**: Archive functionality (Phase 9)

The connection between Ash-Dash and Ash-Vault (MinIO on Syn) has been fully verified and is operational.

**Verified** ✅:
- [x] MinIO health endpoint accessible from Ash-Dash container (91.44ms latency)
- [x] Network connectivity between Lofn and Syn is stable
- [x] MinIO client connects successfully
- [x] All three buckets accessible: `ash-archives`, `ash-documents`, `ash-exports`
- [x] ZFS backup infrastructure operational (fixed 2026-01-18)

**Archive functionality is fully operational.**

---

## 🔜 Future Enhancements

See [enhancements.md](enhancements.md) for detailed planning.

---

## 📝 Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-01-20 | v5.0.13 | **Ash-Vault Connection VERIFIED** - MinIO client, all 3 buckets accessible, archive functionality operational | PapaBearDoes |
| 2026-01-12 | v5.0.12 | Roadmap restructured to hybrid template format, added Known Issues section | PapaBearDoes |
| 2026-01-10 | v5.0.11 | Phase 11 complete - Polish, accessibility, documentation | PapaBearDoes |
| 2026-01-10 | v5.0.10 | Phase 10 complete - OIDC auth, RBAC, admin UI | PapaBearDoes |
| 2026-01-10 | v5.0.9 | Phase 9 complete - Archive system, encryption | PapaBearDoes |
| 2026-01-09 | v5.0.8 | Phase 8 complete - Syn VM, MinIO, Ash-Vault | PapaBearDoes |
| 2026-01-09 | v5.0.7 | Phase 7 complete - Wiki system, PDF export | PapaBearDoes |
| 2026-01-08 | v5.0.6 | Phase 6 complete - TipTap notes, auto-save | PapaBearDoes |
| 2026-01-07 | v5.0.5 | Phase 5 complete - Session management | PapaBearDoes |
| 2026-01-07 | v5.0.4 | Phase 4 complete - Dashboard, charts | PapaBearDoes |
| 2026-01-07 | v5.0.3 | Phase 3 complete - Vue.js frontend | PapaBearDoes |
| 2026-01-07 | v5.0.2 | Phase 2 complete - Data layer | PapaBearDoes |
| 2026-01-06 | v5.0.1 | Phase 1 complete - Foundation | PapaBearDoes |
| 2026-01-06 | v5.0.0 | Initial roadmap created | PapaBearDoes |

---

**Built with care for chosen family** 🏳️‍🌈
