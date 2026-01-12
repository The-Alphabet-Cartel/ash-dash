---
title: "Ash-Vault - v5.0 Development Roadmap"
description: "Roadmap for the v5.0 development of Ash-Vault, the Crisis Archive & Backup Infrastructure"
category: roadmap
tags:
  - roadmap
  - planning
  - ash-vault
author: "PapaBearDoes"
version: "5.0"
last_updated: "2026-01-12"
---
# Ash-Vault: v5.0 Development Roadmap

============================================================================
**Ash-Vault**: Crisis Archive & Backup Infrastructure
**The Alphabet Cartel** - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================

**Document Version**: v5.0.2
**Created**: 2026-01-09
**Last Updated**: 2026-01-12
**Status**: ✅ Complete (All 5 Phases)
**Repository**: https://github.com/the-alphabet-cartel/ash-vault

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
    Secure     → Encrypt sensitive session data with defense-in-depth layering
    Archive    → Preserve crisis records in resilient object storage
    Replicate  → Maintain backups across device, site, and cloud tiers
    Protect    → Safeguard our LGBTQIA+ community through vigilant data guardianship
```

---

## 📋 Executive Summary

Ash-Vault is the Crisis Archive & Backup Infrastructure for the Ash ecosystem. Running on the **Syn VM** (named after the Norse goddess who guards doors), it provides encrypted object storage and implements the 1-2-3 backup strategy to ensure crisis session data survives any disaster scenario.

### Key Capabilities

- **Encrypted Object Storage**: MinIO with ZFS native encryption underneath
- **Defense-in-Depth**: Application-level AES-256-GCM + filesystem encryption
- **1-2-3 Backup Strategy**: 3 copies on 2 media types with 1 offsite
- **Automated Backups**: Python-based service for scheduled snapshots and replication
- **Health Monitoring**: FastAPI endpoints for backup status and alerting

### Architecture Decision

Ash-Vault was created as a dedicated service to separate archive/backup concerns from the main Ash-Dash application:

| Aspect | Without Ash-Vault | With Ash-Vault |
|--------|-------------------|----------------|
| Storage | Local filesystem | MinIO object storage |
| Encryption | Single layer | Defense-in-depth (2 layers) |
| Backups | Manual | Automated 1-2-3 strategy |
| Recovery | Ad-hoc | Documented runbook |
| Monitoring | None | Health endpoints + Discord alerts |

### Current Status

Ash-Vault v5.0 is **complete** and running on the Syn VM. All 5 phases implemented in a single day. Backup jobs are scheduled and operational.

> ⚠️ **Known Issue**: Ash-Dash connection requires verification - see [Known Issues](#-known-issues)

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           ASH-VAULT ARCHITECTURE                             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                     ODIN HYPERVISOR (Windows 11)                    │    │
│   │   ┌─────────────────────────────────────────────────────────────┐   │    │
│   │   │                  SYN VM (Debian Trixie)                     │   │    │
│   │   │                  IP: 10.20.30.202                           │   │    │
│   │   │                  "The Guardian"                             │   │    │
│   │   │                                                             │   │    │
│   │   │   ┌──────────────────────────────────────────────────────┐  │   │    │
│   │   │   │  ZFS Pool: syn (aes-256-gcm encrypted)               │  │   │    │
│   │   │   │  Dataset: syn/archives → /mnt/archives               │  │   │    │
│   │   │   │                                                      │  │   │    │
│   │   │   │  /mnt/archives/minio-data/                           │  │   │    │
│   │   │   │  ├── ash-archives/    (encrypted sessions)           │  │   │    │
│   │   │   │  ├── ash-documents/   (document backups)             │  │   │    │
│   │   │   │  └── ash-exports/     (PDF exports, reports)         │  │   │    │
│   │   │   └──────────────────────────────────────────────────────┘  │   │    │
│   │   │                                                             │   │    │
│   │   │   ┌─────────────────────────────────────────────────────┐   │   │    │
│   │   │   │  Docker Containers                                  │   │   │    │
│   │   │   │  ┌─────────────────┐   ┌─────────────────────────┐  │   │   │    │
│   │   │   │  │ ash-vault-minio │   │ ash-vault-backup        │  │   │   │    │
│   │   │   │  │ :30884 API      │   │ (Python/FastAPI)        │  │   │   │    │
│   │   │   │  │ :30885 Console  │   │ :30886 Health           │  │   │   │    │
│   │   │   │  └─────────────────┘   └─────────────────────────┘  │   │   │    │
│   │   │   └─────────────────────────────────────────────────────┘   │   │    │
│   │   └─────────────────────────────────────────────────────────────┘   │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                      BACKUP DESTINATIONS                            │    │
│   │                                                                     │    │
│   │   TIER 3: On-Device     TIER 2: Same-Site      TIER 1: Off-Site     │    │
│   │   ┌───────────────┐     ┌───────────────┐     ┌───────────────┐     │    │
│   │   │ ZFS Snapshots │     │ Lofn ZFS      │     │ Backblaze B2  │     │    │
│   │   │ @daily (7)    │────>│ backup/       │────>│ ash-vault-    │     │    │
│   │   │ @weekly (4)   │     │ ash-vault     │     │ backup-       │     │    │
│   │   │ @monthly (12) │     │               │     │ alphabetcartel│     │    │
│   │   └───────────────┘     └───────────────┘     └───────────────┘     │    │
│   │   Daily 3 AM            Nightly 4 AM          Weekly Sun 5 AM       │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 1-2-3 Backup Strategy

| Tier | Location | Schedule | Retention | Purpose |
|------|----------|----------|-----------|---------|
| **3** | Syn (On-Device) | Daily 3 AM | 7 daily, 4 weekly, 12 monthly | Quick recovery |
| **2** | Lofn (Same-Site) | Nightly 4 AM | Mirrors Tier 3 | Hardware failure |
| **1** | Backblaze B2 (Off-Site) | Weekly Sun 5 AM | 90 days | Disaster recovery |

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **VM Host** | Hyper-V on Odin | VM hypervisor |
| **VM OS** | Debian Trixie | Stable Linux base |
| **Filesystem** | ZFS | Native encryption, snapshots |
| **Object Storage** | MinIO | S3-compatible API |
| **Backup Service** | Python 3.11 + FastAPI | Automation and health |
| **Cloud Backup** | Backblaze B2 + rclone | Off-site replication |
| **Containerization** | Docker | Service deployment |
| **Encryption** | AES-256-GCM | ZFS native + application layer |

---

## 📅 Phase Overview

| Phase | Name | Focus | Status |
|-------|------|-------|--------|
| 1 | VM Foundation | Syn VM, ZFS, Docker | ✅ Complete |
| 2 | MinIO Deployment | Object storage, buckets | ✅ Complete |
| 3 | Backup Infrastructure | 1-2-3 strategy, automation | ✅ Complete |
| 4 | Testing & Verification | Backup/restore validation | ✅ Complete |
| 5 | Documentation & Polish | Runbooks, operations guide | ✅ Complete |

---

## 📋 Detailed Phase Breakdown

### Phase 1: VM Foundation ✅ Complete
**Goal**: Create the Syn VM with encrypted ZFS storage

- [x] Syn VM on Odin (Hyper-V Gen 2)
- [x] Debian Trixie minimal install
- [x] ZFS pool with native AES-256-GCM encryption
- [x] Auto-mount on boot
- [x] Docker + Docker Compose
- [x] UFW firewall configured

**Completed**: 2026-01-09
**Documentation**: [Phase 1 Complete](phase1/complete.md) | [VM Setup Guide](phase1/syn-vm-setup.md)

---

### Phase 2: MinIO Deployment ✅ Complete
**Goal**: Deploy MinIO object storage for archive data

- [x] MinIO container (ports 30884/30885)
- [x] Docker secrets for credentials
- [x] Buckets: ash-archives, ash-documents, ash-exports
- [x] Health endpoint integration

**Completed**: 2026-01-09
**Documentation**: [Phase 2 Complete](phase2/complete.md) | [Phase 2 Planning](phase2/planning.md)

---

### Phase 3: Backup Infrastructure ✅ Complete
**Goal**: Implement 1-2-3 backup strategy

- [x] SSH key setup (Syn → Lofn)
- [x] Lofn ZFS target dataset
- [x] ZFS snapshot automation (Tier 3)
- [x] ZFS replication to Lofn (Tier 2)
- [x] Backblaze B2 configuration (Tier 1)
- [x] Python backup service container
- [x] FastAPI health endpoints
- [x] Discord alert integration

**Completed**: 2026-01-09
**Documentation**: [Phase 3 Complete](phase3/complete.md) | [Phase 3 Planning](phase3/planning.md)

---

### Phase 4: Testing & Verification ✅ Complete
**Goal**: Validate all backup and recovery procedures

- [x] Tier 3 test (ZFS snapshots)
- [x] Tier 2 test (Lofn replication)
- [x] Tier 1 test (B2 cloud sync)
- [x] Recovery runbook
- [x] Recovery drills - Deferred until ecosystem live
- [x] Performance benchmarks - Deferred until live data

**Completed**: 2026-01-09
**Documentation**: [Phase 4 Complete](phase4/complete.md) | [Recovery Runbook](phase4/recovery_runbook.md)

---

### Phase 5: Documentation & Polish ✅ Complete
**Goal**: Finalize documentation and operational procedures

- [x] Recovery runbook
- [x] Operations guide
- [x] Troubleshooting guide
- [x] README update
- [x] Ash-Dash integration - Deferred until verification

**Completed**: 2026-01-09
**Documentation**: [Phase 5 Complete](phase5/complete.md) | [Operations Guide](../operations/operations_guide.md)

---

## 🔐 Security Considerations

### Encryption Layers

| Layer | Method | Purpose |
|-------|--------|---------|
| **Application** | AES-256-GCM | Ash-Dash encrypts data before storage |
| **Filesystem** | ZFS native encryption | Defense-in-depth for data at rest |
| **Transport** | HTTPS/TLS | Data in transit (MinIO API) |

### Access Control

| Service | Access Restriction |
|---------|-------------------|
| SSH (22) | Local network only (10.20.30.0/24) |
| MinIO API (30884) | Lofn only (10.20.30.253) |
| MinIO Console (30885) | Local network only |
| Backup Service (30886) | Local network only |

### Secrets Management

- MinIO credentials stored in Docker secrets
- SSH keys for Lofn replication (no password)
- B2 application keys in environment variables
- ZFS encryption key stored securely on Syn

---

## 🖥️ Infrastructure & Deployment

### Syn VM Configuration

| Setting | Value |
|---------|-------|
| **Hypervisor** | Odin (Hyper-V) |
| **OS** | Debian Trixie |
| **IP** | 10.20.30.202 |
| **ZFS Pool** | syn |
| **ZFS Dataset** | syn/archives → /mnt/archives |

### Docker Services

| Container | Ports | Purpose |
|-----------|-------|---------|
| ash-vault-minio | 30884, 30885 | Object storage |
| ash-vault-backup | 30886 | Backup automation |

### Scheduled Jobs

| Job | Schedule | Action |
|-----|----------|--------|
| Daily Snapshot | 3 AM | ZFS snapshot @daily |
| Weekly Snapshot | Sunday 3 AM | ZFS snapshot @weekly |
| Monthly Snapshot | 1st 3 AM | ZFS snapshot @monthly |
| Lofn Replication | 4 AM | ZFS send to Lofn |
| B2 Cloud Sync | Sunday 5 AM | rclone sync to B2 |

### File Structure

```
/dockers/ash-vault/
├── docker-compose.yml
├── .env
├── secrets/
│   ├── minio_root_user
│   └── minio_root_password
├── src/
│   ├── backup_service.py
│   ├── managers/
│   └── config/
└── logs/
```

---

## 📊 Progress Summary

### Completed Phases: 5 of 5 🎉

| Phase | Status | Date | Key Deliverables |
|-------|--------|------|------------------|
| Phase 1 | ✅ Complete | 2026-01-09 | Syn VM, ZFS, Docker |
| Phase 2 | ✅ Complete | 2026-01-09 | MinIO, buckets, health |
| Phase 3 | ✅ Complete | 2026-01-09 | 1-2-3 backup strategy |
| Phase 4 | ✅ Complete | 2026-01-09 | Testing, runbook |
| Phase 5 | ✅ Complete | 2026-01-09 | Documentation |

**Total Implementation Time**: 1 day! 🚀

---

## ✅ Success Criteria

All criteria met:

1. ✅ Syn VM operational with encrypted ZFS
2. ✅ MinIO deployed with three buckets
3. ✅ ZFS snapshots automated (daily/weekly/monthly)
4. ✅ Replication to Lofn configured
5. ✅ Backblaze B2 cloud sync operational
6. ✅ Health endpoints responding
7. ✅ Discord alerts configured
8. ✅ Recovery runbook documented
9. ✅ Operations guide complete
10. ✅ All backup tiers tested

---

## ⚠️ Known Issues

### Ash-Dash Connection Verification Required

**Status**: 🟡 Needs Verification
**Priority**: Medium
**Affects**: Archive operations from Ash-Dash

The connection between Ash-Dash (on Lofn) and Ash-Vault (MinIO on Syn) experienced some failures during development. While both services are operational independently, the integration requires verification to ensure:

1. MinIO credentials are correctly configured in Ash-Dash Docker secrets
2. Network connectivity between Lofn (10.20.30.253) and Syn (10.20.30.202) is stable
3. Archive upload from Ash-Dash completes successfully
4. Archive retrieval and decryption works end-to-end

**Next Steps**:
- [ ] Verify MinIO health endpoint from Ash-Dash container
- [ ] Test archive creation workflow from Ash-Dash UI
- [ ] Test archive retrieval and decryption
- [ ] Monitor for connection timeouts or failures

---

## 🔜 Future Enhancements

See [enhancements.md](enhancements.md) for detailed planning.

### Deferred Items

| Item | Trigger |
|------|---------|
| Ash-Dash Integration Verification | Immediate priority |
| Recovery Drills | Quarterly, once ecosystem live |
| Performance Benchmarks | After 1 month of live data |

### Post-v5.0 Backlog

- Automated recovery testing
- Backup integrity verification (checksums)
- Retention policy automation
- Storage usage alerting
- Compression optimization
- Multi-region cloud backup

---

## 📝 Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-01-12 | v5.0.2 | Roadmap restructured to hybrid template format, added Known Issues section | Claude + PapaBearDoes |
| 2026-01-09 | v5.0.1 | All 5 phases complete | Claude + PapaBearDoes |
| 2026-01-09 | v5.0.0 | Initial roadmap and implementation | Claude + PapaBearDoes |

---

## 🔗 Ash Ecosystem

| Project | Purpose | Status |
|---------|---------|--------|
| [ash](https://github.com/the-alphabet-cartel/ash) | Parent repository | ✅ Active |
| [ash-bot](https://github.com/the-alphabet-cartel/ash-bot) | Discord bot frontend | ✅ Complete |
| [ash-nlp](https://github.com/the-alphabet-cartel/ash-nlp) | NLP classification | ✅ Complete |
| [ash-dash](https://github.com/the-alphabet-cartel/ash-dash) | Crisis dashboard | ✅ Complete |
| [ash-thrash](https://github.com/the-alphabet-cartel/ash-thrash) | Testing suite | 🟡 In Development |
| **ash-vault** | Archive & backup | ✅ Complete |

---

**Built with care for chosen family** 🏳️‍🌈
