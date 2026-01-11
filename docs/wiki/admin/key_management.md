# Ash-Dash Key Management & Disaster Recovery

**Version**: v5.0-9-9.1-1  
**Created**: 2026-01-09  
**Status**: 📋 Reference Documentation  
**Repository**: https://github.com/the-alphabet-cartel/ash-dash  
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | [alphabetcartel.org](https://alphabetcartel.org)

---

## 🔐 Overview

Ash-Dash uses multiple layers of encryption to protect sensitive crisis session data. This document provides comprehensive procedures for key management, backup, and disaster recovery.

---

## 🔑 Encryption Keys Inventory

| Key | Type | Location | Purpose | Criticality |
|-----|------|----------|---------|-------------|
| **Archive Master Key** | AES-256 | Lofn: `secrets/archive_master_key` | Session content encryption | 🔴 CRITICAL |
| **ZFS Encryption Key** | AES-256-GCM | Syn: `/root/.zfs-key` | Disk-level encryption | 🔴 CRITICAL |
| **MinIO Credentials** | Password | Both servers | Storage access | 🟡 HIGH |
| **PostgreSQL Password** | Password | Lofn: `secrets/postgres_token` | Database access | 🟡 HIGH |

---

## 📦 Archive Master Key

### Purpose

The Archive Master Key encrypts session data **before** it leaves Ash-Dash. Even if MinIO storage or ZFS encryption are compromised, the session content remains protected.

### Key Characteristics

| Property | Value |
|----------|-------|
| Algorithm | AES-256-GCM |
| Key Size | 32 bytes (256 bits) |
| Format | Raw binary (not base64) |
| Derivation | PBKDF2(master_key, salt, 100,000 iterations) |
| Per-Archive | Unique derived key via random salt |

### Generation

```bash
# SSH to Lofn (10.20.30.253)
ssh lofn

# Navigate to Ash-Dash directory
cd /path/to/ash-dash

# Generate cryptographically secure 32-byte key
openssl rand 32 > secrets/archive_master_key

# Set strict permissions
chmod 600 secrets/archive_master_key

# Verify key is exactly 32 bytes
wc -c secrets/archive_master_key
# Expected: 32 secrets/archive_master_key

# View key in hex for verification
xxd secrets/archive_master_key
# Should show 2 lines of 16 bytes each (32 total)
```

### Backup Procedures

#### Backup Location 1: Encrypted USB Drive (Primary)

**Initial Setup (One-Time)**:
```bash
# Find USB device
lsblk

# Create LUKS encrypted partition
sudo cryptsetup luksFormat /dev/sdX1
# Enter and confirm passphrase (store separately!)

# Open encrypted partition
sudo cryptsetup luksOpen /dev/sdX1 ash-key-backup

# Format with ext4
sudo mkfs.ext4 /dev/mapper/ash-key-backup

# Create mount point
sudo mkdir -p /mnt/usb
```

**Backup Process**:
```bash
# Open and mount
sudo cryptsetup luksOpen /dev/sdX1 ash-key-backup
sudo mount /dev/mapper/ash-key-backup /mnt/usb

# Create backup directory structure
sudo mkdir -p /mnt/usb/ash-dash-keys/$(date +%Y-%m-%d)

# Copy key
sudo cp secrets/archive_master_key /mnt/usb/ash-dash-keys/$(date +%Y-%m-%d)/

# Create metadata file
cat << EOF | sudo tee /mnt/usb/ash-dash-keys/$(date +%Y-%m-%d)/README.txt
Ash-Dash Archive Master Key Backup
==================================
Date: $(date -Iseconds)
Source: Lofn (10.20.30.253)
Path: secrets/archive_master_key
Size: $(wc -c < secrets/archive_master_key) bytes
SHA256: $(sha256sum secrets/archive_master_key | cut -d' ' -f1)

Recovery Instructions:
1. Copy archive_master_key to secrets/archive_master_key
2. Set permissions: chmod 600 secrets/archive_master_key
3. Verify: wc -c secrets/archive_master_key (should be 32)
EOF

# Verify backup
sudo xxd /mnt/usb/ash-dash-keys/$(date +%Y-%m-%d)/archive_master_key | head -2

# Unmount and close
sudo umount /mnt/usb
sudo cryptsetup luksClose ash-key-backup
```

**Storage**: Fireproof safe, separate physical location from servers.

#### Backup Location 2: Password Manager (Secondary)

```bash
# Export as base64 for text-based storage
base64 secrets/archive_master_key
```

Store in password manager with:
- **Title**: `Ash-Dash Archive Master Key`
- **Username**: `archive_master_key`
- **Password**: `[base64 output]`
- **Notes**: 
  ```
  Type: AES-256 Encryption Key
  Format: Base64 encoded (decode before use)
  Recovery: echo "BASE64_HERE" | base64 -d > archive_master_key
  Verify: wc -c archive_master_key (must be 32 bytes)
  ```
- **Tags**: `ash`, `encryption`, `critical`

#### Backup Location 3: Paper Backup (Offline)

```bash
# Generate hex representation
xxd -p secrets/archive_master_key | tr -d '\n' && echo
```

**Output format**: 64 hexadecimal characters (e.g., `a1b2c3d4e5f6...`)

**Print and store with**:
```
ASH-DASH ARCHIVE MASTER KEY - PAPER BACKUP
===========================================
Date: [YYYY-MM-DD]
Key (Hex): [64 hex characters, split into groups of 8]
Checksum: [First 8 chars of SHA256 hash]

Recovery: echo "HEX_STRING" | xxd -r -p > archive_master_key
```

**Storage**: Fireproof safe, separate from USB backup.

### Recovery Procedures

#### From Encrypted USB

```bash
# Connect USB and find device
lsblk

# Open encrypted partition
sudo cryptsetup luksOpen /dev/sdX1 ash-key-backup
sudo mount /dev/mapper/ash-key-backup /mnt/usb

# Find latest backup
ls -la /mnt/usb/ash-dash-keys/

# Restore key
cp /mnt/usb/ash-dash-keys/YYYY-MM-DD/archive_master_key secrets/
chmod 600 secrets/archive_master_key

# Verify
wc -c secrets/archive_master_key  # Must be 32
sha256sum secrets/archive_master_key  # Compare with README.txt

# Cleanup
sudo umount /mnt/usb
sudo cryptsetup luksClose ash-key-backup
```

#### From Password Manager (Base64)

```bash
# Copy base64 string from password manager
echo "YOUR_BASE64_STRING_HERE" | base64 -d > secrets/archive_master_key
chmod 600 secrets/archive_master_key

# Verify
wc -c secrets/archive_master_key  # Must be 32
```

#### From Paper Backup (Hex)

```bash
# Enter the 64 hex characters (no spaces)
echo "YOUR_64_HEX_CHARS_HERE" | xxd -r -p > secrets/archive_master_key
chmod 600 secrets/archive_master_key

# Verify
wc -c secrets/archive_master_key  # Must be 32
```

---

## 🗄️ ZFS Encryption Key (Syn VM)

### Purpose

ZFS native encryption protects all data at rest on the Syn VM, including MinIO storage. This provides a second layer of protection for archived data.

### Key Location

```
Syn VM (10.20.30.202)
├── /root/.zfs-key                    # ZFS encryption passphrase
└── /mnt/archives/                    # Encrypted ZFS dataset
```

### Backup Procedures

The ZFS key should be backed up following similar procedures to the archive master key. See [Ash-Vault documentation](https://github.com/the-alphabet-cartel/ash-vault) for details.

### Key Relationship

```
To read an archived session, you need:
1. Archive Master Key (decrypts session JSON)
   AND
2. ZFS Key (if restoring from raw disk)
   AND
3. MinIO Credentials (to access storage)
```

---

## 🔄 Key Rotation

### When to Rotate Keys

| Scenario | Action |
|----------|--------|
| Scheduled rotation | Every 12 months recommended |
| Staff departure | Rotate if staff had key access |
| Suspected compromise | Rotate immediately |
| Security audit requirement | Follow audit timeline |

### Archive Master Key Rotation

⚠️ **WARNING**: Key rotation requires re-encrypting all existing archives. Plan for downtime.

**Process**:

1. **Generate New Key**
   ```bash
   openssl rand 32 > secrets/archive_master_key.new
   chmod 600 secrets/archive_master_key.new
   ```

2. **Backup New Key** (follow all backup procedures)

3. **Re-encrypt Archives** (requires custom script)
   ```python
   # Pseudocode - implement in Phase 9
   for archive in all_archives:
       # Decrypt with old key
       plaintext = decrypt(archive.data, old_key)
       # Encrypt with new key
       ciphertext = encrypt(plaintext, new_key)
       # Update archive
       archive.data = ciphertext
       archive.save()
   ```

4. **Swap Keys**
   ```bash
   mv secrets/archive_master_key secrets/archive_master_key.old
   mv secrets/archive_master_key.new secrets/archive_master_key
   ```

5. **Verify** all archives are readable

6. **Securely Delete Old Key**
   ```bash
   shred -vfz -n 5 secrets/archive_master_key.old
   ```

---

## 🚨 Disaster Scenarios

### Scenario 1: Lofn Server Total Loss

**Impact**: Archive master key lost along with server.

**Recovery**:
1. Restore key from backup (USB/password manager/paper)
2. Redeploy Ash-Dash to new server
3. Connect to Syn VM (archives preserved)
4. Verify archive decryption works

**Time to Recovery**: 2-4 hours (with prepared backups)

### Scenario 2: Syn VM Total Loss

**Impact**: MinIO storage lost, but data replicated to Lofn and Backblaze B2.

**Recovery**:
1. Rebuild Syn VM (see [VM-Syn documentation](../vm-syn/complete.md))
2. Restore ZFS pool from Lofn replication
3. Deploy MinIO container
4. Verify archive access

**Time to Recovery**: 4-8 hours

### Scenario 3: Both Servers Total Loss

**Impact**: Complete infrastructure loss.

**Recovery**:
1. Restore archive master key from off-site backup
2. Restore ZFS key from off-site backup
3. Rebuild Lofn server
4. Rebuild Syn VM
5. Restore archives from Backblaze B2
6. Verify full system functionality

**Time to Recovery**: 1-2 days

### Scenario 4: Archive Master Key Lost (No Backup)

**Impact**: 🔴 **CRITICAL** - All archived sessions permanently unreadable.

**Recovery**: **NOT POSSIBLE**

**Prevention**:
- Maintain 3+ backup copies
- Test recovery procedures quarterly
- Never store all backups in one location

---

## ✅ Recovery Testing Checklist

Perform quarterly:

- [ ] USB backup can be read and contains valid 32-byte key
- [ ] Password manager backup decodes to valid 32-byte key
- [ ] Paper backup can be manually entered and produces valid key
- [ ] Test archive can be decrypted with recovered key
- [ ] All backup locations are physically accessible
- [ ] Backup USB LUKS passphrase is known/accessible

---

## 📋 Key Management Audit Log

Maintain a log of all key management activities:

| Date | Action | Performed By | Notes |
|------|--------|--------------|-------|
| YYYY-MM-DD | Initial key generation | [Name] | Key created for Phase 9 |
| YYYY-MM-DD | USB backup created | [Name] | Stored in [Location] |
| YYYY-MM-DD | Password manager backup | [Name] | Entry created |
| YYYY-MM-DD | Recovery test | [Name] | All 3 backups verified |

---

## 🔗 Related Documentation

| Document | Description |
|----------|-------------|
| [secrets/README.md](../../../secrets/README.md) | Secret file setup instructions |
| [Phase 8 Complete](../phase8/complete.md) | Archive infrastructure overview |
| [Syn VM Setup](../vm-syn/complete.md) | ZFS and MinIO deployment |
| [Ash-Vault](https://github.com/the-alphabet-cartel/ash-vault) | Backup service documentation |

---

## ⚠️ Security Reminders

1. **Never** commit keys to Git
2. **Never** transmit keys over unencrypted channels
3. **Never** store all backups in one physical location
4. **Always** verify key integrity after restoration
5. **Always** test recovery procedures before they're needed
6. **Always** log all key management activities

---

**Built with care for chosen family** 🏳️‍🌈
