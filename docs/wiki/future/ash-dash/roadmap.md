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
last_updated: "2026-01-12"
---
# Ash-Dash: v5.0 Development Roadmap

============================================================================
**Ash-Dash**: Crisis Response Dashboard
**The Alphabet Cartel** - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================

**Document Version**: v5.0.12
**Created**: 2026-01-06
**Last Updated**: 2026-01-12
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

> ⚠️ **Known Issue**: Ash-Vault connection requires verification - see [Known Issues](#-known-issues)

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

## 📋 Detailed Phase Breakdown

### Phase 1: Foundation & Infrastructure ✅ Complete
**Goal**: Establish project structure and core infrastructure

- [x] Project directory structure (Clean Architecture compliant)
- [x] Docker setup (Dockerfile, docker-compose.yml)
- [x] FastAPI application skeleton
- [x] Configuration management (JSON + environment variables)
- [x] LoggingConfigManager integration
- [x] Health check endpoints
- [x] Basic test framework setup

**Completed**: 2026-01-06
**Documentation**: [Phase 1 Completion Report](phase1/complete.md)

---

### Phase 2: Data Layer ✅ Complete
**Goal**: Implement persistent storage and data access patterns

- [x] PostgreSQL container setup
- [x] SQLAlchemy 2.0 models with Mapped[] annotations
- [x] Alembic migrations
- [x] Database schema (Users, Sessions, Notes, Archives, AuditLog)
- [x] Redis client for reading Ash-Bot data
- [x] Data sync service (Redis → PostgreSQL before TTL)
- [x] Repository pattern for data access
- [x] API endpoints for sessions and users

**Completed**: 2026-01-07
**Documentation**: [Phase 2 Completion Report](phase2/complete.md)

---

### Phase 3: Frontend Foundation ✅ Complete
**Goal**: Set up Vue.js application with core UI components

- [x] Vue.js 3 project initialization with Vite
- [x] TailwindCSS configuration
- [x] Layout components (Sidebar, Header, MainLayout)
- [x] Dark/light mode toggle with persistence
- [x] Responsive breakpoints
- [x] Vue Router setup
- [x] Pinia store for state management
- [x] API client service (Axios)

**Completed**: 2026-01-07
**Documentation**: [Phase 3 Completion Report](phase3/complete.md)

---

### Phase 4: Dashboard & Metrics ✅ Complete
**Goal**: Build the main dashboard with metrics and visualizations

- [x] Dashboard backend API endpoints
- [x] Metric cards (active sessions, critical/high, weekly totals)
- [x] Crisis trends chart (Chart.js stacked bar - 30 days)
- [x] CRT activity chart (Chart.js horizontal bar - 7 days)
- [x] Active sessions list with severity indicators
- [x] Configurable dual polling (10s/30s)
- [x] Dark/light mode chart theming

**Completed**: 2026-01-07
**Documentation**: [Phase 4 Completion Report](phase4/complete.md)

---

### Phase 5: Session Management ✅ Complete
**Goal**: Implement session history and detail views

- [x] Sessions list page with search and filters
- [x] Pagination with page size selector
- [x] Session detail page with user info, history, analysis panels
- [x] Session state management (active/closed/archived)
- [x] Audit logging for state transitions

**Completed**: 2026-01-07
**Documentation**: [Phase 5 Completion Report](phase5/complete.md)

---

### Phase 6: Notes System ✅ Complete
**Goal**: Implement WYSIWYG note-taking for CRT members

- [x] TipTap editor integration
- [x] Note CRUD operations
- [x] Auto-save functionality (2-second debounce)
- [x] Note locking after session close
- [x] Admin override for locked notes

**Completed**: 2026-01-08
**Documentation**: [Phase 6 Completion Report](phase6/complete.md)

---

### Phase 7: Documentation Wiki ✅ Complete
**Goal**: Build wiki system from Markdown files

- [x] Markdown file scanner for `docs/wiki/` directory
- [x] Frontmatter parser (title, category, tags)
- [x] Search functionality with weighted scoring
- [x] Markdown-to-HTML rendering with syntax highlighting
- [x] PDF export via WeasyPrint

**Completed**: 2026-01-09
**Documentation**: [Phase 7 Completion Report](phase7/complete.md)

---

### Phase 8: Archive Infrastructure ✅ Complete
**Goal**: Set up Syn VM with ZFS, MinIO, and backup strategy

**Syn** is a dedicated Debian Trixie VM named after the Norse goddess who guards doorways.

#### Part A: VM Foundation
- [x] Debian Trixie VM creation on Odin hypervisor
- [x] ZFS pool with native AES-256-GCM encryption
- [x] Encrypted dataset `syn/archives` with auto-mount
- [x] Docker installation
- [x] UFW firewall configuration

#### Part B: MinIO Deployment
- [x] MinIO container (ports 30884/30885)
- [x] Buckets: ash-archives, ash-documents, ash-exports

#### Part C: Ash-Dash Integration
- [x] MinIOManager class
- [x] Configuration in default.json
- [x] SecretsManager MinIO credential methods

#### Part D: Backup Infrastructure (via Ash-Vault)
- [x] Ash-Vault project created
- [x] ZFS snapshot automation
- [x] ZFS replication to Lofn
- [x] Backblaze B2 cloud sync

**Completed**: 2026-01-09
**Documentation**: [Phase 8 Planning](phase8/planning.md)

---

### Phase 9: Archive System Implementation ✅ Complete
**Goal**: Implement archive workflows in Ash-Dash

- [x] Archive master key setup with Docker secrets
- [x] AES-256-GCM encryption utilities (PBKDF2 key derivation)
- [x] ArchiveManager for archive orchestration
- [x] Database schema with queryable columns
- [x] Archive API endpoints (13 total)
- [x] "Save to Archive" button with retention tier selection
- [x] Archive metadata storage in PostgreSQL
- [x] Archive listing page with filters and pagination
- [x] Archive retrieval and decryption (viewer page)
- [x] Retention policy management (standard: 1yr, permanent: 7yr)
- [x] Automated cleanup script and admin API
- [x] Session protection (archived sessions cannot be reopened)

**Completed**: 2026-01-10
**Documentation**: [Phase 9 Completion Report](phase9/complete.md)

---

### Phase 10: Authentication & Authorization ✅ Complete
**Goal**: Enable Pocket-ID authentication and three-tier RBAC

**Critical Discovery**: TinyAuth only sets a simple hash cookie without user claims. Solution: Native Pocket-ID OIDC integration directly in Ash-Dash.

#### Pocket-ID Group → Role Mapping

| Group | Role |
|-------|------|
| `cartel_crt` | CRT Member |
| `cartel_crt_lead` | CRT Lead |
| `cartel_crt_admin` | CRT Admin |

#### Implementation
- [x] Native Pocket-ID OIDC integration
- [x] PKCE authorization flow with state/nonce protection
- [x] JWT ID token validation via JWKS
- [x] Redis-based server-side session management (DB 1)
- [x] Three-tier RBAC (Member/Lead/Admin)
- [x] User sync on login (create/update in PostgreSQL)
- [x] Note ownership enforcement
- [x] Audit log user tracking
- [x] Admin UI - CRT roster (Lead+)
- [x] Admin UI - Audit logs (Lead+)
- [x] Admin UI - System health (Admin only)
- [x] Browser vs API request handling
- [x] Automatic token refresh

**Completed**: 2026-01-10
**Documentation**: [Phase 10 Completion Report](phase10/complete.md)

---

### Phase 11: Polish & Documentation ✅ Complete
**Goal**: Finalize for production deployment

- [x] UI/UX refinement (collapsible sidebar, smooth transitions)
- [x] Accessibility improvements (ARIA labels, keyboard nav, WCAG 2.1 AA)
- [x] Performance optimization (Vite chunks, caching, minification)
- [x] Error handling (ErrorMessage component with retry)
- [x] Loading states (LoadingSpinner, SkeletonCard, SkeletonList, EmptyState)
- [x] User documentation (3 CRT guides)
- [x] Admin documentation (3 Admin guides)
- [x] Operations documentation (4 deployment/operations guides)
- [x] Test suite (101 tests across 7 files)
- [x] QA review (functionality, security, accessibility)
- [x] Dockerfile cleanup

**Completed**: 2026-01-10
**Documentation**: [Phase 11 Completion Report](phase11/completion_report.md)

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

### Ash-Vault Connection Verification Required

**Status**: 🟡 Needs Verification
**Priority**: Medium
**Affects**: Archive functionality (Phase 9)

The connection between Ash-Dash and Ash-Vault (MinIO on Syn) experienced some failures during development. While the archive system is implemented and tested, the live connection requires verification to ensure:

1. MinIO credentials are correctly configured in Docker secrets
2. Network connectivity between Lofn and Syn is stable
3. Archive upload/download operations complete successfully
4. Retention policy cleanup jobs run correctly

**Next Steps**:
- [ ] Verify MinIO health endpoint from Ash-Dash container
- [ ] Test archive creation workflow end-to-end
- [ ] Test archive retrieval and decryption
- [ ] Verify scheduled cleanup job execution

---

## 🔜 Future Enhancements

See [enhancements.md](enhancements.md) for detailed planning.

### Post-v5.0 Backlog

- Real-time WebSocket updates (replace polling)
- Advanced analytics and trend visualization
- Session export to PDF
- Bulk archive operations
- Mobile-responsive improvements
- Notification system for CRT
- Integration with external ticketing systems
- Performance monitoring dashboard

---

## 📝 Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
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
