---
title: "Ash-Vault - Future Enhancements"
description: "Planned features and improvements for Ash-Vault"
category: future
tags:
  - roadmap
  - planning
  - ash-vault
author: "PapaBearDoes"
version: "5.0"
last_updated: "2026-01-11"
---
# Ash-Vault: Future Enhancements & Improvements

============================================================================
**Ash-Vault**: Crisis Archive & Backup Infrastructure for the Ash Ecosystem
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

This document tracks potential enhancements and feature ideas for Ash-Vault beyond the core v5.0 roadmap. Items are organized by priority and implementation complexity.

Ash-Vault v5.0 is complete with:
- Encrypted ZFS storage on the Syn VM
- MinIO object storage (ash-archives, ash-documents, ash-exports buckets)
- 1-2-3 backup strategy (ZFS snapshots → Lofn replication → Backblaze B2)
- FastAPI health endpoints and Discord alerting

The enhancements below build on this foundation.

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

### 1. Ash-Dash Archive Integration

**Priority**: 🔴 High
**Complexity**: 🟧 High
**Depends On**: Ash-Dash reaching archive phase
**Estimated Time**: 12-16 hours

Build the integration layer that allows Ash-Dash to store and retrieve crisis session archives from Ash-Vault. The infrastructure is ready (MinIO, buckets, health endpoints), but the actual API endpoints for dashboard integration need to be built.

**Features**:
- Crisis session archive storage endpoint
- Document upload/download endpoints
- Export retrieval for PDF reports
- Session metadata indexing
- Secure token-based authentication between services

**Implementation**:
- Create `/api/archives/` route group in Ash-Vault
- Implement MinIO client wrapper for CRUD operations
- Add authentication middleware for Ash-Dash service tokens
- Build session metadata storage (JSON sidecar files or separate index)
- Create Ash-Dash client library for vault operations

**Benefit**: Enables the core use case - actually archiving crisis session data for long-term secure storage and compliance.

---

### 2. Backup Health Dashboard Widget

**Priority**: 🔴 High
**Complexity**: 🟨 Medium
**Depends On**: Ash-Dash Admin interface
**Estimated Time**: 6-8 hours

Create an Admin-only widget in Ash-Dash that displays real-time backup health status, giving administrators visibility into the backup infrastructure without needing SSH access to Syn.

**Features**:
- Last successful backup timestamps for each tier (snapshots, Lofn, B2)
- Storage usage trends and capacity warnings
- Failure alerts with error details
- Next scheduled job timestamps
- Quick-view status indicators (green/yellow/red)

**Implementation**:
- Extend Ash-Vault health API to include detailed backup status
- Create new `/api/health/detailed` endpoint with job history
- Build Ash-Dash widget component consuming the API
- Add Admin-only route protection in Ash-Dash
- Store job history in local SQLite or JSON for trend data

**Benefit**: Proactive monitoring for administrators, reduces time to detect and respond to backup failures.

---

### 3. Automated Backup Verification

**Priority**: 🟡 Medium
**Complexity**: 🟨 Medium
**Depends On**: Core backup jobs stable
**Estimated Time**: 6-8 hours

Implement periodic integrity verification by performing test restores to a temporary location and comparing checksums. This catches silent data corruption before it becomes a disaster during an actual recovery scenario.

**Features**:
- Weekly verification job (configurable schedule)
- Random sample selection from each backup tier
- Checksum comparison against source data
- Verification report with pass/fail status
- Discord alerts on verification failures

**Implementation**:
- Add new job in `src/jobs/verify.py`
- Create temporary restore location on Syn (`/tmp/verify`)
- Implement ZFS snapshot mount and checksum logic
- Add B2 download and verify capability
- Extend alerting for verification results
- Add verification schedule to configuration

**Benefit**: Confidence that backups are actually restorable, not just successfully written.

---

### 4. Retention Policy Enforcement

**Priority**: 🟡 Medium
**Complexity**: 🟦 Low
**Depends On**: None
**Estimated Time**: 3-4 hours

Implement automatic pruning of old snapshots and B2 objects according to the retention policy already defined in configuration (7 daily, 4 weekly, 12 monthly).

**Features**:
- Automatic ZFS snapshot cleanup based on retention counts
- B2 object lifecycle management
- Dry-run mode for testing before enabling
- Retention report showing what would be/was deleted
- Protection against deleting the only remaining backup

**Implementation**:
- Add `prune_snapshots()` function to `src/jobs/snapshot.py`
- Parse snapshot names to identify age/type (daily/weekly/monthly)
- Implement safe deletion with minimum retention checks
- Add B2 lifecycle rules via API or rclone
- Schedule pruning to run after backup jobs complete

**Benefit**: Prevents storage exhaustion, maintains clean backup history without manual intervention.

---

## ⏸️ Back Burner

Features we may want eventually, but are lower priority.

### 1. MinIO Object Versioning

Enable S3 versioning on MinIO buckets for protection against accidental overwrites or deletions. Would allow recovery of previous object versions without relying on ZFS snapshots.

**Notes**:
- Simple configuration change in MinIO
- Increases storage usage (keeps all versions)
- Need to define version retention policy
- May be redundant given ZFS snapshot coverage

---

### 2. Ash-Dash Admin Metrics

Extend the Backup Health Dashboard Widget with detailed metrics: job durations, transfer sizes, success/failure rates over time, and trend analysis. Visible to Admins only.

**Notes**:
- Builds on the Health Dashboard Widget (#2)
- Requires job history storage (SQLite recommended)
- Charts/graphs for visual trend analysis
- Could help identify performance degradation early

---

### 3. Archive REST API

Create a simplified REST API that allows other Ash ecosystem services (Ash-Bot, Ash-NLP) to archive data directly without going through Ash-Dash. Useful for automated archival workflows.

**Notes**:
- Separate from the Ash-Dash integration endpoints
- Would need its own authentication scheme
- Consider rate limiting and quota management
- May duplicate functionality if Ash-Dash becomes the central hub

---

## 💭 Considered But Deferred

Ideas discussed but not currently planned. May revisit based on team feedback.

| Idea | Reason for Deferral |
|------|---------------------|
| Multi-Channel Alerting (Email) | Discord is our sole communication platform; adding email adds complexity without value |
| Geo-Redundant Cloud Storage | B2 already provides durability; multi-region adds cost and complexity we don't need yet |
| Prometheus/Grafana Integration | We don't use this stack; Ash-Dash Admin Metrics covers the use case |

---

## 🗣️ Requests

Space for tracking community-requested features.

*No community requests yet. Features will be added here as they're requested through Discord or GitHub issues.*

---

## 🔬 Research

Ideas requiring research before planning.

### R-001: Immutable Backups (WORM)

**Status**: 🔬 Research Needed

**Question**: How can we implement write-once-read-many (WORM) storage for ransomware protection?

**Approach**:
- Research B2 Object Lock capabilities and pricing
- Investigate ZFS snapshot hold mechanisms
- Evaluate MinIO object locking features
- Consider air-gapped backup options

**Concerns**:
- Cost implications of immutable storage tiers
- Complexity of recovery from immutable backups
- Balance between protection and operational flexibility
- Retention periods for immutable copies

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
