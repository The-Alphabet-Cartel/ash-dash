---
title: "Ash Ecosystem - v5.0 Development Roadmap"
description: "Umbrella roadmap for the Ash Crisis Detection Ecosystem v5.0 recode"
category: roadmap
tags:
  - roadmap
  - planning
  - ash
  - ecosystem
author: "PapaBearDoes"
version: "5.0"
last_updated: "2026-01-17"
---
# Ash Ecosystem: v5.0 Development Roadmap

============================================================================
**Ash**: Crisis Detection Ecosystem for The Alphabet Cartel
**The Alphabet Cartel** - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================

**Document Version**: v5.0.7
**Created**: 2026-01-11
**Last Updated**: 2026-01-17
**Status**: 🟢 Production Ready (Ash-Thrash In Development)
**Repository**: https://github.com/the-alphabet-cartel/ash

---

## Table of Contents

1. [Mission Statement](#-mission-statement)
2. [Executive Summary](#-executive-summary)
3. [Ecosystem Architecture](#-ecosystem-architecture)
4. [Component Overview](#-component-overview)
5. [Infrastructure Overview](#-infrastructure-overview)
6. [Component Status Summary](#-component-status-summary)
7. [Known Issues](#-known-issues)
8. [Success Criteria](#-success-criteria)
9. [Next Steps](#-next-steps)
10. [Component Roadmaps](#-component-roadmaps)
11. [Change Log](#-change-log)

---

## 🎯 Mission Statement

```
ASH ECOSYSTEM MISSION - NEVER TO BE VIOLATED:
    Listen   → Maintain vigilant presence across all community spaces
    Detect   → Identify mental health crisis patterns through comprehensive analysis
    Connect  → Bridge community members to timely support and intervention
    Protect  → Safeguard our LGBTQIA+ chosen family through early crisis response
```

The Ash Ecosystem is a comprehensive crisis detection and response system built to protect The Alphabet Cartel's LGBTQIA+ Discord community. Every architectural decision, every line of code, and every feature serves one purpose: **keeping our chosen family safe**.

---

## 📋 Executive Summary

### What is Ash?

Ash is a Discord-based crisis detection ecosystem that monitors community conversations, identifies mental health crisis indicators, and connects community members with timely support. Named after the World Tree in Norse mythology that connects all realms, Ash connects our community members to the help they need.

### v5.0 Recode

The v5.0 recode represents a complete rewrite of the Ash ecosystem with:

- **Clean Architecture**: Standardized patterns across all components (Charter v5.3)
- **Multi-Model NLP**: Local 4-model ensemble with council-inspired consensus
- **Production Infrastructure**: Health monitoring, circuit breakers, graceful degradation
- **Encrypted Archives**: Defense-in-depth encryption with 1-2-3 backup strategy
- **Modern Dashboard**: Vue.js + FastAPI with three-tier RBAC
- **Comprehensive Testing**: 525+ test scenarios (in development)

### Current Status

| Component | Status | Description |
|-----------|--------|-------------|
| **Ash-Bot** | 🟢 Production Ready | Discord bot with Phase 9 enhancements in progress |
| **Ash-NLP** | 🟢 Complete | All 6 phases complete, 4-model ensemble operational |
| **Ash-Dash** | 🟢 Complete | All 11 phases complete, WCAG 2.1 AA accessible |
| **Ash-Vault** | 🟢 Complete | All 5 phases complete, 1-2-3 backup operational |
| **Ash-Thrash** | 📋 Planning | Ready to begin Phase 1 development |
| **Ash (Core)** | 🟢 Phase 2 Complete | Ecosystem Health API - Dashboard integrated |

**The ecosystem is live and protecting our community.**

---

## 🏗️ Ecosystem Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                              ASH ECOSYSTEM ARCHITECTURE                              │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│    ┌──────────────────────────────────────────────────────────────────────────────┐  │
│    │                   ASH (CORE) - Ecosystem Health API (:30887)                 │  │
│    │         https://ash.alphabetcartel.net/health/ecosystem                      │  │
│    │    Aggregates health from all components + validates inter-connectivity      │  │
│    └──────────────────────────────────────────────────────────────────────────────┘  │
│                 │              │                │                │                   │
│                 ▼             ▼                ▼                ▼                  │
│    ┌──────────────────────────────────────────────────────────────────────────────┐  │
│    │                        DISCORD GATEWAY                                       │  │
│    └──────────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                               │
│                                      ▼                                               │
│    ┌──────────────────────────────────────────────────────────────────────────────┐  │
│    │                           ASH-BOT (:30881)                                   │  │
│    │                      Crisis Detection Discord Bot                            │  │
│    │                                                                              │  │
│    │  • Message Monitoring        • Alert Routing          • Ash AI Sessions      │  │
│    │  • User History Tracking     • CRT Slash Commands     • Auto-Initiation      │  │
│    └──────────────────────────────────────────────────────────────────────────────┘  │
│                    │                             │                    │              │
│                    ▼                             │                   ▼              │
│    ┌──────────────────────────┐                  │     ┌──────────────────────┐      │
│    │     ASH-NLP (:30880)     │                  │     │     CLAUDE API       │      │
│    │  Crisis Detection NLP    │                  │     │  (Ash Personality)   │      │
│    │                          │                  │     └──────────────────────┘      │
│    │  ┌────────┐ ┌────────┐   │                  │                                   │
│    │  │ Crisis │ │Emotion │   │                  │                                   │
│    │  │Classify│ │Detect  │   │                  │                                   │
│    │  └────────┘ └────────┘   │                  │                                   │
│    │  ┌────────┐ ┌────────┐   │                  │                                   │
│    │  │Sentimnt│ │ Irony  │   │                  │                                   │
│    │  │Analysis│ │ Detect │   │                  │                                   │
│    │  └────────┘ └────────┘   │                  │                                   │
│    │                          │                  │                                   │
│    │  • Consensus Algorithms  │                  │                                   │
│    │  • Context Analysis      │                  │                                   │
│    │  • Explainability        │                  │                                   │
│    └──────────────────────────┘                  │                                   │
│                                                  │                                   │
│                                                  ▼                                   │
│    ┌──────────────────────────────────────────────────────────────────────────────┐  │
│    │                             SHARED REDIS                                     │  │
│    │                       User History • Session Data                            │  │
│    └──────────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                               │
│         ┌────────────────────────────┴────────────────────────────┐                  │
│         ▼                                                         ▼                 │
│    ┌───────────────────────────┐                   ┌──────────────────────────┐      │
│    │    ASH-DASH (:30883)      │                   │    ASH-VAULT (Syn VM)    │      │
│    │ Crisis Response Dashboard │                   │  Archive & Backup Infra  │      │
│    │                           │                   │                          │      │
│    │  • Real-time Metrics      │                   │  ┌──────────────────┐    │      │
│    │  • Session Management     │                   │  │ MinIO (:30884)   │    │      │
│    │  • WYSIWYG Notes          │                   │  │ Object Storage   │    │      │
│    │  • Wiki Documentation     │<─────────────────>│  └──────────────────┘    │      │
│    │  • Archive Management     │                   │                          │      │
│    │  • Three-tier RBAC        │                   │  • ZFS Encryption        │      │
│    │                           │                   │  • 1-2-3 Backups         │      │
│    │  ┌──────────────────┐     │                   │  • B2 Cloud Sync         │      │
│    │  │ PostgreSQL       │     │                   │                          │      │
│    │  │ (Dash Database)  │     │                   └──────────────────────────┘      │
│    │  └──────────────────┘     │                                                     │
│    └───────────────────────────┘                                                     │
│                                                                                      │
│    ┌──────────────────────────────────────────────────────────────────────────────┐  │
│    │                        ASH-THRASH (:30888)                                   │  │
│    │                      Crisis Detection Testing Suite                          │  │
│    │                                                                              │  │
│    │  • 525+ Test Scenarios   • Regression Detection   • Performance Benchmarks   │  │
│    │  • Accuracy Validation   • Baseline Tracking      • Discord Alerts           │  │
│    │                                                                              │  │
│    │                           STATUS: 📋 In Development                          │  │
│    └──────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Component Overview

### Ash-Bot - Crisis Detection Discord Bot
**Repository**: [github.com/the-alphabet-cartel/ash-bot](https://github.com/the-alphabet-cartel/ash-bot)

The Discord frontend that monitors community channels, forwards messages to Ash-NLP for analysis, and alerts the Crisis Response Team when crises are detected.

| Capability | Description |
|------------|-------------|
| **Monitor** | Listen to configured channels, forward to NLP |
| **Alert** | Route crisis alerts by severity to CRT channels |
| **Track** | Maintain user history for escalation detection |
| **Support** | AI-powered "Talk to Ash" via Claude API |

---

### Ash-NLP - Crisis Detection NLP Server
**Repository**: [github.com/the-alphabet-cartel/ash-nlp](https://github.com/the-alphabet-cartel/ash-nlp)

The AI backend that classifies messages using a local 4-model ensemble with council-inspired consensus algorithms.

| Capability | Description |
|------------|-------------|
| **Analyze** | Process messages through multi-model ensemble |
| **Detect** | Identify crisis signals with weighted consensus |
| **Explain** | Provide human-readable decision explanations |
| **Context** | Rolling window analysis for escalation patterns |

---

### Ash-Dash - Crisis Response Dashboard
**Repository**: [github.com/the-alphabet-cartel/ash-dash](https://github.com/the-alphabet-cartel/ash-dash)

The web dashboard for CRT members to monitor crises, document sessions, and manage archives.

| Capability | Description |
|------------|-------------|
| **Reveal** | Real-time metrics and active session display |
| **Enable** | Tools for swift CRT intervention |
| **Document** | WYSIWYG notes and wiki documentation |
| **Archive** | Encrypted long-term session storage |

---

### Ash-Vault - Archive & Backup Infrastructure
**Repository**: [github.com/the-alphabet-cartel/ash-vault](https://github.com/the-alphabet-cartel/ash-vault)

The backup infrastructure running on the Syn VM, providing encrypted storage and disaster recovery.

| Capability | Description |
|------------|-------------|
| **Secure** | Defense-in-depth encryption (app + ZFS) |
| **Archive** | MinIO object storage for session data |
| **Replicate** | 1-2-3 backup strategy (device, site, cloud) |
| **Recover** | Documented runbooks for disaster recovery |

---

### Ash (Core) - Ecosystem Health API
**Repository**: [github.com/the-alphabet-cartel/ash](https://github.com/the-alphabet-cartel/ash)

The centralized ecosystem health monitoring service providing a single endpoint for all component status and inter-component connectivity.

| Capability | Description |
|------------|-------------|
| **Aggregate** | Unified health status from all ecosystem components |
| **Validate** | Inter-component connectivity verification |
| **Report** | Single endpoint for monitoring tools and dashboard |
| **Alert** | Ecosystem-wide status and degradation detection |

---

### Ash-Thrash - Crisis Detection Testing Suite
**Repository**: [github.com/the-alphabet-cartel/ash-thrash](https://github.com/the-alphabet-cartel/ash-thrash)

The comprehensive testing suite for validating Ash-NLP accuracy and preventing regressions.

| Capability | Description |
|------------|-------------|
| **Validate** | 525+ test scenarios across severity levels |
| **Challenge** | Edge cases, sarcasm, gaming context tests |
| **Guard** | Baseline comparison for regression detection |
| **Report** | JSON, HTML, and Discord webhook reports |

---

## 🖥️ Infrastructure Overview

### Server Inventory

| Server | IP | Role | Key Services |
|--------|-----|------|--------------|
| **Lofn** | 10.20.30.253 | Primary Ash Host | Ash-Bot, Ash-NLP, Ash-Dash, PostgreSQL, Redis |
| **Syn** | 10.20.30.202 | Archive Vault | MinIO, ZFS encrypted storage, Ash-Vault |
| **Odin** | 10.20.30.240 | Hypervisor | Hosts Syn VM (Hyper-V) |
| **Bacchus** | 10.20.30.14 | AI Rig | Development/testing |
| **Backblaze B2** | Cloud | Off-site Backup | Disaster recovery tier |

### Port Allocation (308xx Range)

| Port | Service | Host | Description |
|------|---------|------|-------------|
| 30880 | Ash-NLP | Lofn | NLP API endpoint |
| 30881 | Ash-Bot | Lofn | Bot health endpoint |
| 30883 | Ash-Dash | Lofn | Dashboard web UI |
| 30884 | MinIO API | Syn | Object storage API |
| 30885 | MinIO Console | Syn | Object storage UI |
| 30886 | Ash-Vault Health | Syn | Backup service health |
| 30887 | Ash (Core) | Lofn | Ecosystem Health API |
| 30888 | Ash-Thrash | Lofn | Testing suite API |

### Hardware Specifications

**Lofn (Primary Host)**:
- CPU: AMD Ryzen 7 5800x (8 cores)
- GPU: NVIDIA RTX 3060 (12GB VRAM)
- RAM: 64Gb
- Storage: NAS mount
- OS: Debian 12

**Bacchus (AI Rig)**:
- CPU: AMD Ryzen 7 7700X (8 cores)
- GPU: NVIDIA RTX 5060 (8GB VRAM)
- RAM: 128Gb
- Storage:
  - NVME OS Drive (C:) - 1Tb
  - Docker/AI Drive (F:) - 1Tb
  - Storage Drive (D:) - 7Tb
- OS: Windows 11 Pro

**Odin (Hypervisor)**:
- CPU: AMD Ryzen 7 2700 (8 cores)
- GPU: NVIDIA RTX 3060 (6GB VRAM)
- RAM: 80Gb
- Storage:
  - NVME OS Drive (C:) - 1Tb
  - VM Drive (D:) - 2.7Tb
- OS: Windows 11 Pro

**Syn (Archive VM)**:
- Hypervisor: Hyper-V on Odin
- CPU: 4 Virtual
- RAM: 4Gb
- Storage:
  - Virtual OS Drive - 256Gb
  - Virtual ZFS Archive Drive - 256Gb
- OS: Debian Trixie
- Storage: ZFS with native AES-256-GCM encryption
- Purpose: Dedicated archive guardian

---

## 📊 Component Status Summary

### Production Components

| Component | Version | Phases | Tests | Status |
|-----------|---------|--------|-------|--------|
| **Ash-Bot** | v5.0.13 | 9 (8.5 complete) | 500+ | 🟢 Production (Phase 9 in progress) |
| **Ash-NLP** | v5.0.10 | 6/6 complete | 140+ | 🟢 Complete |
| **Ash-Dash** | v5.0.12 | 11/11 complete | 101 | 🟢 Complete |
| **Ash-Vault** | v5.0.2 | 5/5 complete | N/A | 🟢 Complete |
| **Ash (Core)** | v5.0.1 | 3/5 complete | 0 | 🟢 Phase 3 Complete |
| **Ash-Thrash** | v5.0.1 | 0/5 complete | 0 | 📋 Planning |

### Key Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Ash-NLP Latency | < 500ms | 3-7s (ensemble) |
| Ash-NLP VRAM | < 12GB | ~1.55GB |
| Ash-Bot Tests | Comprehensive | 500+ |
| Ash-Dash Accessibility | WCAG 2.1 AA | ✅ Compliant |
| Backup Strategy | 1-2-3 | ✅ Implemented |

---

## ⚠️ Known Issues

### Ash-Vault ZFS Backup Failures

**Status**: 🔴 Active Issue
**Priority**: High
**Components**: Ash-Vault
**Discovered**: 2026-01-16 (via Ash Ecosystem Health API testing)

The Ash-Vault backup service health endpoint responds normally, but the underlying ZFS backup jobs are failing:

**Failures Observed**:
- ❌ ZFS Daily Snapshot: "Failed to create daily snapshot" (Dataset: syn/archives)
- ❌ ZFS Replication to Lofn: "No local snapshots available for replication" (Target: 10.20.30.253:backup/ash-vault)

**Root Cause**: The replication failure is a cascading effect - since daily snapshots aren't being created, there are no snapshots available to replicate.

**Investigation Needed**:
- [ ] Check ZFS pool status on Syn VM (`zpool status`)
- [ ] Verify syn/archives dataset exists and is healthy
- [ ] Check Ash-Vault service logs for snapshot creation errors
- [ ] Verify ZFS permissions for the ash-vault service user
- [ ] Test manual snapshot creation

**Impact**: 1-2-3 backup strategy is currently non-functional. No new snapshots or off-site replications are occurring.

---

### Ash-Dash ↔ Ash-Vault Connection

**Status**: 🟡 Partially Verified
**Priority**: Medium
**Components**: Ash-Dash, Ash-Vault

The network connectivity between Ash-Dash and Ash-Vault (MinIO) has been verified working via the Ash Ecosystem Health API. However, the underlying backup infrastructure has issues (see above).

**Verified** ✅:
- [x] MinIO health endpoint accessible from Ash-Dash container (15.27ms latency)
- [x] Network path between Lofn and Syn is operational

**Still Needs Verification**:
- [ ] Archive upload workflow completes successfully
- [ ] Archive retrieval and decryption works end-to-end
- [ ] Retention policy cleanup jobs execute correctly

**Impact**: Archive functionality in Ash-Dash may work for uploads/downloads, but long-term backup integrity is compromised by ZFS failures.

---

## ✅ Success Criteria

### Ecosystem-Level Criteria

| Criterion | Status | Notes |
|-----------|--------|-------|
| All components follow Clean Architecture Charter v5.0+ | ✅ | Charter at v5.3 |
| Discord crisis detection operational | ✅ | Ash-Bot + Ash-NLP live |
| CRT dashboard accessible | ✅ | Ash-Dash complete |
| Encrypted archive storage | 🟡 | MinIO accessible, ZFS backups failing |
| 1-2-3 backup strategy | 🔴 | ZFS snapshot/replication failures |
| Comprehensive testing suite | 🔲 | Ash-Thrash in development |
| Production health monitoring | ✅ | Ash (Core) Phase 3 complete |

### Per-Component Criteria

See individual roadmaps for detailed success criteria:
- [Ash-Bot Success Criteria](ash-bot/roadmap.md#-success-criteria)
- [Ash-NLP Success Criteria](ash-nlp/roadmap.md#-success-criteria)
- [Ash-Dash Success Criteria](ash-dash/roadmap.md#-success-criteria)
- [Ash-Vault Success Criteria](ash-vault/roadmap.md#-success-criteria)
- [Ash-Thrash Success Criteria](ash-thrash/roadmap.md#-success-criteria)

---

## 🔜 Next Steps

### Immediate Priority

1. **Ash-Vault ZFS Backup Investigation** 🔴
   - Diagnose and fix ZFS snapshot creation failures
   - Restore 1-2-3 backup functionality
   - Priority: Critical for data protection

2. **Ash Ecosystem Health API (Phase 3)** ✅ Complete
   - CRT-accessible System Health page at `/system-health` - Complete
   - Simplified operational/down view for all CRT members - Complete
   - Pivoted from public status page to internal CRT access
   - See: [Phase 3 Completion](phase3/planning.md)

3. **Begin Ash-Thrash Development**
   - Start Phase 1: Foundation
   - Estimated effort: 32-46 hours total
   - Target: 525+ test scenarios

### Upcoming Work

| Priority | Task | Component |
|----------|------|-----------|
| ✅ Done | CRT-Accessible System Health | Ash (Core) / Ash-Dash |
| 🔴 High | ZFS backup investigation | Ash-Vault |
| ✅ Done | Ecosystem Health API Phase 2 | Ash (Core) |
| 🟡 Medium | Phase 4: Discord Webhook Alerting | Ash (Core) |
| 🔴 High | Ash-Thrash Phase 1 | Ash-Thrash |
| 🟡 Medium | Phase 9.2: Session Handoff | Ash-Bot |
| 🟡 Medium | Phase 9.3: Follow-up Check-ins | Ash-Bot |
| 🟢 Low | Performance benchmarking | Ash-Vault |

---

## 📑 Component Roadmaps

Detailed roadmaps for each component:

| Component | Roadmap Location |
|-----------|------------------|
| **Ash (Core)** | [This Document + phase1-5/planning.md](phase1-5/planning.md) |
| **Ash-Bot** | [ash-bot/roadmap.md](ash-bot/roadmap.md) |
| **Ash-NLP** | [ash-nlp/roadmap.md](ash-nlp/roadmap.md) |
| **Ash-Dash** | [ash-dash/roadmap.md](ash-dash/roadmap.md) |
| **Ash-Vault** | [ash-vault/roadmap.md](ash-vault/roadmap.md) |
| **Ash-Thrash** | [ash-thrash/roadmap.md](ash-thrash/roadmap.md) |

Enhancement tracking for each component:

| Component | Enhancements Location |
|-----------|----------------------|
| **Ash (Core)** | [enhancements.md](enhancements.md) |
| **Ash-Bot** | [ash-bot/enhancements.md](ash-bot/enhancements.md) |
| **Ash-NLP** | [ash-nlp/enhancements.md](ash-nlp/enhancements.md) |
| **Ash-Dash** | [ash-dash/enhancements.md](ash-dash/enhancements.md) |
| **Ash-Vault** | [ash-vault/enhancements.md](ash-vault/enhancements.md) |
| **Ash-Thrash** | [ash-thrash/enhancements.md](ash-thrash/enhancements.md) |

---

## 📝 Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-01-17 | v5.0.7 | Phase 3 complete - CRT-accessible System Health, pivoted from public status page | Claude + PapaBearDoes |
| 2026-01-17 | v5.0.6 | Phase 2 complete - Backend proxy pattern implemented, ServiceCard display fixes | Claude + PapaBearDoes |
| 2026-01-15 | v5.0.5 | Phase 2 implementation - Ash-Dash System Health page refactored | Claude + PapaBearDoes |
| 2026-01-16 | v5.0.4 | Phase 1 complete, updated known issues with ZFS backup failures discovered during testing | Claude + PapaBearDoes |
| 2026-01-14 | v5.0.2 | Added Ash (Core) Ecosystem Health API, Phase 1 planning, updated port allocation (30887 for Ash, 30888 for Ash-Thrash) | Claude + PapaBearDoes |
| 2026-01-12 | v5.0.1 | Created ecosystem roadmap from hybrid template | Claude + PapaBearDoes |
| 2026-01-11 | v5.0.0 | Initial ecosystem roadmap (template only) | Claude + PapaBearDoes |

---

## 🏆 Acknowledgments

The Ash Ecosystem is built by and for **The Alphabet Cartel** community. Every feature, every safeguard, and every line of code exists because our LGBTQIA+ chosen family deserves protection.

Special thanks to:
- The Crisis Response Team volunteers who put in countless hours
- Community members who trusted us with their safety
- Everyone who contributed feedback, testing, and support

---

**Built with care for chosen family** 🏳️‍🌈
