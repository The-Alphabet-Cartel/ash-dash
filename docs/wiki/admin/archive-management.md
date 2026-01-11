---
title: Archive Management Guide
description: How to manage encrypted session archives in Ash-Dash
category: Administration
tags:
  - admin
  - archives
  - encryption
  - retention
author: Admin Team
last_updated: "2026-01-10"
version: "1.0"
---

# Archive Management Guide

This guide covers managing encrypted session archives in Ash-Dash for [The Alphabet Cartel](https://discord.gg/alphabetcartel) administrators.

## Understanding Archives

### What is Archiving?

Archiving moves closed sessions to encrypted long-term storage:

- **Source:** PostgreSQL database (closed sessions)
- **Destination:** MinIO object storage (encrypted)
- **Purpose:** Preserve sensitive data securely while freeing database space

### Archive Properties

| Property | Value |
|----------|-------|
| **Encryption** | AES-256-GCM (application level) |
| **Storage Encryption** | ZFS native encryption (storage level) |
| **Format** | Encrypted JSON blob |
| **Immutability** | Archived sessions cannot be modified |

### Why Double Encryption?

1. **Application-level (AES-256-GCM):** Protects data even if storage is compromised
2. **Storage-level (ZFS):** Protects against physical theft of drives

## Retention Tiers

Sessions are archived with retention policies:

| Tier | Retention | Use Case |
|------|-----------|----------|
| **Standard** | 1 year | Routine sessions |
| **Extended** | 3 years | Significant interventions |
| **Permanent** | 7 years | Critical cases, legal holds |

### Selecting Retention Tier

When archiving, consider:

- **Severity level** of the session
- **Outcome** of the intervention
- **Recurring patterns** for the user
- **Legal/compliance** requirements

## Archiving Sessions

### Prerequisites

Only these roles can archive:
- Admin
- CRT Lead

### Archive Workflow

1. Navigate to **Sessions**
2. Find the closed session to archive
3. Click **Archive** button
4. Select retention tier
5. Confirm the archive operation

### What Gets Archived

The archive includes:
- Session metadata (ID, dates, severity)
- Discord user information
- All flagged messages
- NLP analysis data
- Complete notes history
- User history snapshot

### Post-Archive State

After archiving:
- Session moves to Archives section
- Original database records are removed
- Session becomes read-only
- Cannot be reopened or modified

## Viewing Archives

Navigate to **Archives** to see archived sessions.

### Archive List

| Column | Description |
|--------|-------------|
| **Session ID** | Original session identifier |
| **User** | Discord user (from archive data) |
| **Severity** | Crisis level when closed |
| **Archived Date** | When it was archived |
| **Retention** | Standard/Extended/Permanent |
| **Expires** | When it will be purged |

### Filtering Archives

| Filter | Options |
|--------|---------|
| **Date Range** | Archive date range |
| **Retention Tier** | Standard, Extended, Permanent |
| **Search** | Session ID, user ID |

### Viewing Archive Contents

1. Click an archived session
2. System retrieves and decrypts the archive
3. View complete session history (read-only)

**Note:** Decryption requires the archive master key to be available.

## Archive Storage

### MinIO Configuration

Archives are stored in MinIO:

| Setting | Value |
|---------|-------|
| **Bucket** | `ash-archives` |
| **Path Pattern** | `{year}/{month}/{session_id}.enc` |
| **Object Lock** | Enabled (immutable) |

### Storage Location

Archives are stored on the Vault VM (planned):
- IP: To be assigned
- Storage: ZFS encrypted pool
- Replication: To Lofn server

### Backup Strategy (1-2-3)

| Backup | Location | Method |
|--------|----------|--------|
| **1 Cloud** | Backblaze B2 | Encrypted sync |
| **2 Same-site** | Lofn server | ZFS replication |
| **3 On-device** | Vault VM | ZFS snapshots |

## Retention Management

### Automatic Expiration

Archives are automatically purged when retention expires:

1. Nightly job checks archive expiration dates
2. Expired archives are scheduled for deletion
3. Deletion is logged in audit trail
4. Storage space is reclaimed

### Extending Retention

To extend retention on an archive:

1. Navigate to **Archives**
2. Find the session
3. Click **Extend Retention**
4. Select new tier (must be longer than current)
5. Confirm the change

**Note:** Retention can only be extended, never shortened.

### Legal Holds

For legal compliance:

1. Mark session as "Legal Hold"
2. Prevents automatic expiration
3. Requires admin to explicitly release hold
4. Fully audited

## Key Management

### Archive Master Key

The archive encryption key is stored in Docker secrets:

```
secrets/archive_master_key
```

### Key Requirements

- 256-bit (32 bytes) minimum
- Generated with cryptographically secure random
- Stored separately from encrypted data
- Backed up securely offline

### Key Rotation (Future)

Key rotation procedure (when implemented):

1. Generate new key
2. Re-encrypt existing archives
3. Update secret
4. Verify decryption works
5. Securely destroy old key

**Warning:** Loss of the master key means permanent loss of all archives!

## Disaster Recovery

### Backup Verification

Monthly verification:

1. Select random archived session
2. Retrieve from backup (not primary)
3. Verify decryption succeeds
4. Verify content integrity

### Recovery Procedure

If primary MinIO fails:

1. Deploy replacement MinIO instance
2. Restore from most recent backup
3. Update connection configuration
4. Verify archive accessibility
5. Resume normal operations

### Key Recovery

If master key is lost:

- Archives become permanently inaccessible
- No recovery possible without key
- **Prevent this:** Multiple secure key backups

## Audit Trail

All archive operations are logged:

| Event | Details Logged |
|-------|----------------|
| **Archive Created** | Who, when, session ID, retention |
| **Archive Viewed** | Who, when, session ID |
| **Retention Extended** | Who, when, old tier, new tier |
| **Archive Expired** | Session ID, original archive date |
| **Archive Deleted** | Session ID, deletion method |

## Best Practices

### Before Archiving

✅ Ensure session is properly closed
✅ Verify notes are complete
✅ Select appropriate retention tier
✅ Confirm user history is captured

### Storage Hygiene

✅ Monitor storage usage monthly
✅ Verify backups are completing
✅ Test restore procedure quarterly
✅ Review retention policy annually

### Security

✅ Limit archive access to necessary roles
✅ Audit archive access regularly
✅ Keep master key backup current
✅ Monitor for unusual access patterns

## Troubleshooting

### "Decryption Failed"

**Causes:**
- Wrong master key
- Corrupted archive file
- Key file permissions

**Solutions:**
1. Verify master key secret is correct
2. Check MinIO object integrity
3. Restore from backup if corrupted

### "Archive Not Found"

**Causes:**
- Session was never archived
- Archive was expired and purged
- MinIO connectivity issue

**Solutions:**
1. Check session status in database
2. Check audit logs for expiration
3. Verify MinIO connection

### "Storage Full"

**Causes:**
- Too many archives
- Retention too long
- Backup bloat

**Solutions:**
1. Review retention policies
2. Purge expired archives manually
3. Expand storage allocation

---

*Last updated: 2026-01-10*

*For encryption key management, see the [Key Management Guide](./key_management.md).*

**Built with care for chosen family** 🏳️‍🌈
