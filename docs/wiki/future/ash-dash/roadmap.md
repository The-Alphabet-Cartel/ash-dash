---
title: "Ash - v5.0 Development Roadmap"
description: "Roadmap for the v5.0 recode of the Ash Ecosystem"
category: roadmap
tags:
  - roadmap
  - planning
  - ash
author: "PapaBearDoes"
version: "5.0"
last_updated: "2026-01-11"
---
# Ash-Dash v5.0 Development Roadmap

============================================================================
**Ash-Dash**: Dashboard For The Ash Crisis Detection Ecosystem
**The Alphabet Cartel** - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================

**Document Version**: v5.0
**Created**: 2026-01-06  
**Last Updated**: 2026-01-10  
**Phase**: 1 (Roadmap)
**Status**: 📋 Planning
**Last Updated**: 2026-01-11

---

## 🎯 Project Vision

Ash-Dash is the Crisis Response Dashboard for The Alphabet Cartel's Discord crisis detection ecosystem. It provides CRT (Crisis Response Team) members and administrators with:

- **Real-time visibility** into active crisis sessions
- **Historical data** for user patterns and trends
- **WYSIWYG note-taking** for session documentation
- **Wiki-style documentation** for training and reference
- **Administrative tools** for user management and system health monitoring
- **Secure archival** for long-term session storage

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Ash-Dash Architecture                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    NGINX Reverse Proxy (crt.alphabetcartel.net:443)                         │
│           │                                                                 │
│           ▼                                                                 │
│    TinyAuth + Pocket-ID ──▶ Ash-Dash (FastAPI + Vue.js) Port 30883          │
│                                    │                                        │
│         ┌──────────────────────────┼──────────────────────────┐             │
│         │                          │                          │             │
│         ▼                          ▼                          ▼            │
│    ┌─────────┐              ┌─────────────┐           ┌─────────────┐       │
│    │  Redis  │              │ PostgreSQL  │           │    MinIO    │       │
│    │(shared) │              │ (Ash-Dash)  │           │    (Syn)    │       │
│    └─────────┘              └─────────────┘           └─────────────┘       │
│         │                                                    │              │
│         │ (reads from Ash-Bot data)                          │              │
│         ▼                                                    ▼             │
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
| **Cache/Real-time** | Redis (shared with Ash-Bot) | Live session data |
| **Archive Storage** | MinIO on Syn VM (ZFS) | Encrypted long-term storage |
| **Cloud Backup** | Backblaze B2 | Off-site disaster recovery |
| **Authentication** | Pocket-ID + TinyAuth | SSO via cookies |
| **Charts** | Chart.js | Dashboard visualizations |
| **Markdown Editor** | TipTap | WYSIWYG note editing |
| **PDF Generation** | WeasyPrint | Documentation export |
| **Encryption** | cryptography (AES-256-GCM) | Archive encryption |
| **Containerization** | Docker + Docker Compose | Deployment |

---

## 📅 Phase Overview

| Phase | Name | Focus | Status |
|-------|------|-------|--------|
| 1 | Foundation & Infrastructure | Project setup, Docker, FastAPI skeleton | ✅ Complete |
| 2 | Data Layer | PostgreSQL, Redis integration, models | ✅ Complete |
| 3 | Frontend Foundation | Vue.js setup, layout, theming | ✅ Complete |
| 4 | Dashboard & Metrics | Metrics display, charts, polling | ✅ Complete |
| 5 | Session Management | Session history, detail views | ✅ Complete |
| 6 | Notes System | WYSIWYG editor, note CRUD | ✅ Complete |
| 7 | Documentation Wiki | Markdown rendering, PDF export | ✅ Complete |
| 8 | Archive Infrastructure | Syn VM, ZFS, MinIO, Backup Strategy | ✅ Complete |
| 9 | Archive System Implementation | Encryption, archive workflows | ✅ Complete |
| 10 | Authentication & Authorization | Pocket-ID auth, RBAC, admin UI | ✅ Complete |
| 11 | Polish & Documentation | QA, optimization, docs | ✅ Complete |

---

## 📋 Detailed Phase Breakdown

### Phase 1: Foundation & Infrastructure ✅ COMPLETE
**Goal**: Establish project structure and core infrastructure

- [x] Project directory structure (Clean Architecture compliant)
- [x] Docker setup (Dockerfile, docker-compose.yml)
- [x] FastAPI application skeleton
- [x] Configuration management (JSON + environment variables)
- [x] LoggingConfigManager integration
- [x] Health check endpoints
- [x] Pocket-ID/TinyAuth cookie parsing for authentication
- [x] Basic test framework setup

**Completion Date**: 2026-01-06  
**Documentation**: [Phase 1 Completion Report](phase1/complete.md)

---

### Phase 2: Data Layer ✅ COMPLETE
**Goal**: Implement persistent storage and data access patterns

- [x] PostgreSQL container setup
- [x] SQLAlchemy 2.0 models and Alembic migrations
- [x] Database schema design (Users, Sessions, Notes, Archives, AuditLog)
- [x] Redis client for reading Ash-Bot data
- [x] Data sync service (Redis → PostgreSQL before TTL)
- [x] Repository pattern for data access
- [x] API endpoints for sessions and users

**Completion Date**: 2026-01-07  
**Documentation**: [Phase 2 Completion Report](phase2/complete.md)

---

### Phase 3: Frontend Foundation ✅ COMPLETE
**Goal**: Set up Vue.js application with core UI components

- [x] Vue.js 3 project initialization with Vite
- [x] TailwindCSS configuration
- [x] Layout components (Sidebar, Header, MainLayout)
- [x] Dark/light mode toggle with persistence
- [x] Responsive breakpoints
- [x] Vue Router setup for page navigation
- [x] Pinia store for state management
- [x] API client service (Axios)

**Completion Date**: 2026-01-07  
**Documentation**: [Phase 3 Completion Report](phase3/complete.md)

---

### Phase 4: Dashboard & Metrics ✅ COMPLETE
**Goal**: Build the main dashboard with metrics and visualizations

- [x] Dashboard backend API endpoints
- [x] Metric cards (active sessions, critical/high, weekly totals)
- [x] Crisis trends chart (Chart.js stacked bar - 30 days)
- [x] CRT activity chart (Chart.js horizontal bar - 7 days)
- [x] Active sessions list with severity indicators
- [x] Configurable dual polling mechanism (10s/30s)
- [x] Dark/light mode chart theming

**Completion Date**: 2026-01-07  
**Documentation**: [Phase 4 Completion Report](phase4/complete.md)

---

### Phase 5: Session Management ✅ COMPLETE
**Goal**: Implement session history and detail views

- [x] Sessions list page with search and filters
- [x] Pagination with page size selector
- [x] Session detail page with user info, history, analysis panels
- [x] Session state management (active/closed/archived)
- [x] Audit logging for state transitions

**Completion Date**: 2026-01-07  
**Documentation**: [Phase 5 Completion Report](phase5/complete.md)

---

### Phase 6: Notes System ✅ COMPLETE
**Goal**: Implement WYSIWYG note-taking for CRT members

- [x] TipTap editor integration
- [x] Note CRUD operations
- [x] Auto-save functionality (2-second debounce)
- [x] Note locking after session close
- [x] Admin override for locked notes

**Completion Date**: 2026-01-08  
**Documentation**: [Phase 6 Completion Report](phase6/complete.md)

---

### Phase 7: Documentation Wiki ✅ COMPLETE
**Goal**: Build wiki system from Markdown files

- [x] Markdown file scanner for `docs/wiki/` directory
- [x] Frontmatter parser (title, category, tags)
- [x] Search functionality with weighted scoring
- [x] Markdown-to-HTML rendering with syntax highlighting
- [x] PDF export via WeasyPrint

**Completion Date**: 2026-01-09  
**Documentation**: [Phase 7 Completion Report](phase7/complete.md)

---

### Phase 8: Archive Infrastructure ✅ COMPLETE
**Goal**: Set up Syn VM with ZFS, MinIO, and 1-2-3 backup strategy

**Syn** is a dedicated Debian Trixie VM named after the Norse goddess who guards doorways - the guardian of our archives.

**Part A: VM Foundation** ✅ COMPLETE
- [x] Debian Trixie VM creation on Odin hypervisor
- [x] ZFS pool creation with native AES-256-GCM encryption
- [x] Encrypted dataset `syn/archives` with auto-mount
- [x] Docker installation
- [x] UFW firewall configuration

**Part B: MinIO Deployment** ✅ COMPLETE
- [x] MinIO container on ports 30884/30885
- [x] Bucket creation (ash-archives, ash-documents, ash-exports)

**Part C: Ash-Dash Integration** ✅ COMPLETE
- [x] MinIOManager class (`src/managers/archive/minio_manager.py`)
- [x] Configuration section in `default.json`
- [x] SecretsManager MinIO credential methods
- [x] Environment variables in `.env.template`
- [x] minio package in `requirements.txt`

**Part D: Backup Infrastructure** ✅ COMPLETE (via Ash-Vault)
- [x] Ash-Vault project created as separate repository
- [x] ZFS snapshot automation (daily/weekly/monthly)
- [x] ZFS replication to Lofn
- [x] Backblaze B2 cloud sync

**Completion Date**: 2026-01-09  
**Documentation**: [Phase 8 Planning](phase8/planning.md)  
**Related**: [Ash-Vault Repository](https://github.com/the-alphabet-cartel/ash-vault)

---

### Phase 9: Archive System Implementation ✅ COMPLETE
**Goal**: Implement archive workflows in Ash-Dash

- [x] Archive master key setup with Docker secrets
- [x] AES-256-GCM encryption utilities (PBKDF2 key derivation)
- [x] ArchiveManager for archive orchestration
- [x] Database schema with dedicated queryable columns
- [x] Archive API endpoints (13 total)
- [x] "Save to Archive" button with retention tier selection
- [x] Archive metadata storage in PostgreSQL
- [x] Archive listing page with filters and pagination
- [x] Archive retrieval and decryption (viewer page)
- [x] Retention policy management (standard: 1yr, permanent: 7yr)
- [x] Automated cleanup script and admin API
- [x] Session protection (archived sessions cannot be reopened)

**Completion Date**: 2026-01-10  
**Documentation**: [Phase 9 Completion Report](phase9/complete.md)

---

### Phase 10: Authentication & Authorization ✅ COMPLETE
**Goal**: Enable Pocket-ID authentication and three-tier RBAC

**Critical Discovery**: TinyAuth only sets a simple hash cookie without user claims. Solution: Native PocketID OIDC integration directly in Ash-Dash.

**Pocket-ID Group → Role Mapping**:
| Group | Role |
|-------|------|
| `cartel_crt` | CRT Member |
| `cartel_crt_lead` | CRT Lead |
| `cartel_crt_admin` | CRT Admin |

- [x] Native PocketID OIDC integration (replacing TinyAuth)
- [x] PKCE authorization flow with state/nonce protection
- [x] JWT ID token validation via JWKS
- [x] Redis-based server-side session management (DB 1)
- [x] Three-tier RBAC (Member/Lead/Admin)
- [x] User sync on login (create/update in PostgreSQL)
- [x] Note ownership enforcement (edit own notes only)
- [x] Audit log user tracking
- [x] Admin UI - CRT roster (Lead+)
- [x] Admin UI - Audit logs (Lead+)
- [x] Admin UI - System health (Admin only)
- [x] Browser vs API request handling (redirect vs JSON 401)
- [x] Automatic token refresh

**Completion Date**: 2026-01-10  
**Documentation**: [Phase 10 Completion Report](phase10/complete.md)

---

### Phase 11: Polish & Documentation ✅ COMPLETE
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
- [x] Dockerfile cleanup (removed testing dependencies)

**Completion Date**: 2026-01-10  
**Documentation**: [Phase 11 Completion Report](phase11/completion_report.md)

---

## 🔐 Security Considerations

1. **Authentication**: All routes protected via Pocket-ID/TinyAuth
2. **Authorization**: Role-based access (CRT Member vs Admin)
3. **Data Encryption**: 
   - At-rest: ZFS native encryption on Syn VM
   - In-transit: HTTPS via NGINX
   - Application-level: AES-256-GCM for archived sessions (double encryption)
4. **Secrets Management**: Docker secrets for sensitive values
5. **Audit Logging**: All administrative actions logged

---

## 🖥️ Infrastructure Overview

| Server | Role | Key Services |
|--------|------|--------------|
| **Lofn** (10.20.30.253) | Primary Ash host | Ash-Bot, Ash-NLP, Ash-Dash, PostgreSQL, Redis |
| **Syn** (10.20.30.202) | Archive vault | MinIO, ZFS encrypted storage, Ash-Vault |
| **Odin** | Hypervisor | Hosts Syn VM |
| **Backblaze B2** | Cloud backup | Off-site disaster recovery |

### Port Allocation (308xx Range)

| Port | Service | Host |
|------|---------|------|
| 30880 | Ash-NLP | Lofn |
| 30881 | Ash-Bot | Lofn |
| 30883 | Ash-Dash | Lofn |
| 30884 | MinIO API | Syn |
| 30885 | MinIO Console | Syn |
| 30886 | Ash-Vault Health | Syn |

---

## 📊 Progress Summary

### Completed Phases: 11 of 11 ✅ PROJECT COMPLETE

| Phase | Status | Date | Key Deliverables |
|-------|--------|------|------------------|
| Phase 1 | ✅ | 2026-01-06 | Docker, FastAPI, Config, Health API |
| Phase 2 | ✅ | 2026-01-07 | PostgreSQL, Redis, Models, Repositories |
| Phase 3 | ✅ | 2026-01-07 | Vue.js, Layout, Theming, Router |
| Phase 4 | ✅ | 2026-01-07 | Dashboard, Charts, Metrics, Polling |
| Phase 5 | ✅ | 2026-01-07 | Sessions List, Detail, History, Actions |
| Phase 6 | ✅ | 2026-01-08 | TipTap Editor, Notes CRUD, Auto-save |
| Phase 7 | ✅ | 2026-01-09 | Wiki System, PDF Export, Search |
| Phase 8 | ✅ | 2026-01-09 | Syn VM, MinIO, MinIOManager, Ash-Vault |
| Phase 9 | ✅ | 2026-01-10 | Archive System, Encryption, Retention |
| Phase 10 | ✅ | 2026-01-10 | OIDC Auth, RBAC, Admin UI |
| Phase 11 | ✅ | 2026-01-10 | UI Polish, Accessibility, Documentation, Tests |

### Remaining Phases: 0 of 11 🎉

**All phases complete! Ash-Dash v5.0 is production ready.**

---

## ✅ Success Criteria

The project is complete when:

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

**Built with care for chosen family** 🏳️‍🌈
