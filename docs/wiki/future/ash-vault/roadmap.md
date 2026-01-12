# Ash-Vault v5.0 Roadmap

**Version**: v5.0  
**Created**: 2026-01-09  
**Last Updated**: 2026-01-09 (All Phases Complete! 🎉)  
**Repository**: https://github.com/the-alphabet-cartel/ash-vault  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | [alphabetcartel.org](https://alphabetcartel.org)

---

## 🎯 Project Vision

**Ash-Vault** is the Crisis Archive & Backup Infrastructure for the Ash ecosystem. Running on the **Syn VM** (named after the Norse goddess who guards doors), it provides:

- **Encrypted Object Storage** via MinIO for crisis session archives
- **Defense-in-Depth Security** with application + filesystem encryption layers
- **1-2-3 Backup Strategy** ensuring data survives any disaster scenario
- **Python-Based Automation** for scheduled backups and health monitoring

---

## 📊 Phase Overview

| Phase | Name | Status | Completed |
|-------|------|--------|-----------|
| **1** | VM Foundation | ✅ Complete | 2026-01-09 |
| **2** | MinIO Deployment | ✅ Complete | 2026-01-09 |
| **3** | Backup Infrastructure | ✅ Complete | 2026-01-09 |
| **4** | Testing & Verification | ✅ Complete | 2026-01-09 |
| **5** | Documentation & Polish | ✅ Complete | 2026-01-09 |

**🎉 Ash-Vault v5.0 is COMPLETE!**

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           ASH-VAULT ARCHITECTURE                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                     ODIN HYPERVISOR (Windows 11)                     │    │
│   │   ┌─────────────────────────────────────────────────────────────┐   │    │
│   │   │                  SYN VM (Debian Trixie)                      │   │    │
│   │   │                  IP: 10.20.30.202                            │   │    │
│   │   │                  "The Guardian"                              │   │    │
│   │   │                                                              │   │    │
│   │   │   ┌──────────────────────────────────────────────────────┐  │   │    │
│   │   │   │  ZFS Pool: syn (aes-256-gcm encrypted)                │  │   │    │
│   │   │   │  Dataset: syn/archives → /mnt/archives                │  │   │    │
│   │   │   │                                                       │  │   │    │
│   │   │   │  /mnt/archives/minio-data/                            │  │   │    │
│   │   │   │  ├── ash-archives/    (encrypted sessions)            │  │   │    │
│   │   │   │  ├── ash-documents/   (document backups)              │  │   │    │
│   │   │   │  └── ash-exports/     (PDF exports, reports)          │  │   │    │
│   │   │   └──────────────────────────────────────────────────────┘  │   │    │
│   │   │                                                              │   │    │
│   │   │   ┌─────────────────────────────────────────────────────┐   │   │    │
│   │   │   │  Docker Containers                                   │   │   │    │
│   │   │   │  ┌─────────────────┐   ┌─────────────────────────┐  │   │   │    │
│   │   │   │  │ ash-vault-minio │   │ ash-vault-backup        │  │   │   │    │
│   │   │   │  │ :30884 API      │   │ (Python/FastAPI)        │  │   │   │    │
│   │   │   │  │ :30885 Console  │   │ :30886 Health           │  │   │   │    │
│   │   │   │  └─────────────────┘   └─────────────────────────┘  │   │   │    │
│   │   │   └─────────────────────────────────────────────────────┘   │   │    │
│   │   └─────────────────────────────────────────────────────────────┘   │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                      BACKUP DESTINATIONS                             │    │
│   │                                                                      │    │
│   │   TIER 3: On-Device     TIER 2: Same-Site      TIER 1: Off-Site     │    │
│   │   ┌───────────────┐     ┌───────────────┐     ┌───────────────┐     │    │
│   │   │ ZFS Snapshots │     │ Lofn ZFS      │     │ Backblaze B2  │     │    │
│   │   │ @daily (7)    │────►│ backup/       │────►│ ash-vault-    │     │    │
│   │   │ @weekly (4)   │     │ ash-vault     │     │ backup-       │     │    │
│   │   │ @monthly (12) │     │               │     │ alphabetcartel│     │    │
│   │   └───────────────┘     └───────────────┘     └───────────────┘     │    │
│   │   Daily 3 AM            Nightly 4 AM          Weekly Sun 5 AM       │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Phase Details

### Phase 1: VM Foundation ✅ COMPLETE

**Objective**: Create the Syn VM with encrypted ZFS storage

| Deliverable | Status |
|-------------|--------|
| Syn VM on Odin (Hyper-V Gen 2) | ✅ |
| Debian Trixie minimal install | ✅ |
| ZFS pool with native encryption | ✅ |
| Auto-mount on boot | ✅ |
| Docker + Docker Compose | ✅ |
| UFW firewall configured | ✅ |

**Documentation**: [Phase 1 Complete](phase1/complete.md) | [VM Setup Guide](phase1/syn-vm-setup.md)

---

### Phase 2: MinIO Deployment ✅ COMPLETE

**Objective**: Deploy MinIO object storage for archive data

| Deliverable | Status |
|-------------|--------|
| MinIO container (ports 30884/30885) | ✅ |
| Docker secrets for credentials | ✅ |
| Buckets: ash-archives, ash-documents, ash-exports | ✅ |
| Health endpoint integration | ✅ |

**Documentation**: [Phase 2 Complete](phase2/complete.md) | [Phase 2 Planning](phase2/planning.md)

---

### Phase 3: Backup Infrastructure ✅ COMPLETE

**Objective**: Implement 1-2-3 backup strategy

| Deliverable | Status |
|-------------|--------|
| SSH key setup (Syn → Lofn) | ✅ |
| Lofn ZFS target dataset | ✅ |
| ZFS snapshot automation (Tier 3) | ✅ |
| ZFS replication to Lofn (Tier 2) | ✅ |
| Backblaze B2 configuration (Tier 1) | ✅ |
| Python backup service container | ✅ |
| FastAPI health endpoints | ✅ |
| Discord alert integration | ✅ |

**Documentation**: [Phase 3 Complete](phase3/complete.md) | [Phase 3 Planning](phase3/planning.md)

---

### Phase 4: Testing & Verification ✅ COMPLETE

**Objective**: Validate all backup and recovery procedures

| Deliverable | Status |
|-------------|--------|
| Tier 3 test (ZFS snapshots) | ✅ |
| Tier 2 test (Lofn replication) | ✅ |
| Tier 1 test (B2 cloud sync) | ✅ |
| Recovery runbook | ✅ |
| Recovery drills | ⏸️ Deferred (until ecosystem live) |
| Performance benchmarks | ⏸️ Deferred (until live data) |

**Documentation**: [Phase 4 Complete](phase4/complete.md) | [Recovery Runbook](phase4/recovery_runbook.md)

---

### Phase 5: Documentation & Polish ✅ COMPLETE

**Objective**: Finalize documentation and operational procedures

| Deliverable | Status |
|-------------|--------|
| Recovery runbook | ✅ |
| Operations guide | ✅ |
| Troubleshooting guide | ✅ |
| README update | ✅ |
| Ash-Dash integration | ⏸️ Deferred (until Ash-Dash ready) |

**Documentation**: [Phase 5 Complete](phase5/complete.md) | [Operations Guide](../operations/operations_guide.md)

---

## 🔐 Security Model

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

---

## 📅 Timeline

| Phase | Status | Completed |
|-------|--------|-----------|
| Phase 1 | ✅ Complete | 2026-01-09 |
| Phase 2 | ✅ Complete | 2026-01-09 |
| Phase 3 | ✅ Complete | 2026-01-09 |
| Phase 4 | ✅ Complete | 2026-01-09 |
| Phase 5 | ✅ Complete | 2026-01-09 |

**Total Implementation Time**: 1 day! 🚀

---

## 📊 What's Running

### Deployment Location
```
/dockers/ash-vault/
├── docker-compose.yml    # Both services
├── .env                  # Configuration
├── secrets/              # Docker secrets
└── logs/                 # Service logs
```

### Services

| Container | Ports | Status |
|-----------|-------|--------|
| ash-vault-minio | 30884, 30885 | 🟢 Healthy |
| ash-vault-backup | 30886 | 🟢 Healthy |

### Scheduled Jobs

| Job | Schedule | Next Run |
|-----|----------|----------|
| Daily Snapshot | 3 AM | Tomorrow |
| Weekly Snapshot | Sunday 3 AM | Next Sunday |
| Monthly Snapshot | 1st 3 AM | Feb 1 |
| Lofn Replication | 4 AM | Tomorrow |
| B2 Cloud Sync | Sunday 5 AM | Next Sunday |

---

## 🔗 Related Documentation

| Document | Description |
|----------|-------------|
| [Operations Guide](../operations/operations_guide.md) | Day-to-day maintenance |
| [Troubleshooting](../operations/troubleshooting.md) | Common issues and fixes |
| [Recovery Runbook](phase4/recovery_runbook.md) | Disaster recovery procedures |
| [Clean Architecture Charter](../standards/clean_architecture_charter.md) | Code standards |

---

## 🔜 Future Work

| Item | Trigger |
|------|---------|
| Ash-Dash Integration | When Ash-Dash reaches archive phase |
| Recovery Drills | Quarterly, once ecosystem live |
| Performance Benchmarks | After 1 month of live data |

---

## 🔗 Ash Ecosystem

| Project | Purpose | Status |
|---------|---------|--------|
| [ash](https://github.com/the-alphabet-cartel/ash) | Parent repository | 🔄 Active |
| [ash-bot](https://github.com/the-alphabet-cartel/ash-bot) | Discord bot frontend | 🔄 Active |
| [ash-nlp](https://github.com/the-alphabet-cartel/ash-nlp) | NLP classification | 🔄 Active |
| [ash-dash](https://github.com/the-alphabet-cartel/ash-dash) | Crisis dashboard | 🔄 Active |
| [ash-thrash](https://github.com/the-alphabet-cartel/ash-thrash) | Testing suite | 🔲 Planned |
| **ash-vault** | Archive & backup | ✅ **Complete** |

---

**Built with care for chosen family** 🏳️‍🌈
