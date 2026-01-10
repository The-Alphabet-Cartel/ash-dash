# Ash-Dash Secrets

**Version**: v5.0-9-9.2-2
**Repository**: https://github.com/the-alphabet-cartel/ash-dash
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | [alphabetcartel.org](https://alphabetcartel.org)

---

## Overview

This directory contains sensitive credentials used by Ash-Dash. These files are:
- **NOT** committed to Git (via `.gitignore`)
- Mounted into Docker containers via Docker Secrets
- Read by the `SecretsManager` at runtime

---

## Secret Files

| File | Description | Required | Usage |
|------|-------------|----------|-------|
| `postgres_token` | PostgreSQL password | ✅ Required | Database connections |
| `minio_root_user` | MinIO root username | ✅ Required | Archive storage |
| `minio_root_password` | MinIO root password | ✅ Required | Archive storage |
| `archive_master_key` | AES-256 encryption key | ✅ Required | Session archive encryption |
| `discord_alert_token` | Discord webhook URL | Optional | System alerts |
| `redis_token` | Redis password | Optional | Session data cache |

---

## Setup Instructions

### 1. Create the secrets directory

```bash
mkdir -p secrets
chmod 700 secrets
```

### 2. PostgreSQL Password (Required)

```bash
# Generate a secure password
openssl rand -base64 32 > secrets/postgres_token

# Set secure permissions
chmod 600 secrets/postgres_token
```

### 3. MinIO Credentials (Required for Archive Storage)

MinIO runs on the Syn VM (10.20.30.202) and provides S3-compatible storage.

**Naming Convention**: We use `minio_root_user` and `minio_root_password` to match the naming on Syn VM.

```bash
# Copy credentials from Syn VM (recommended)
ssh syn 'cat /opt/minio/secrets/minio_root_user' > secrets/minio_root_user
ssh syn 'cat /opt/minio/secrets/minio_root_password' > secrets/minio_root_password
chmod 600 secrets/minio_root_user secrets/minio_root_password

# Or manually create if setting up fresh (must match Syn VM!)
echo "ashadmin" > secrets/minio_root_user
openssl rand -base64 32 > secrets/minio_root_password
chmod 600 secrets/minio_root_user secrets/minio_root_password
```

**Important**: The MinIO credentials must match what's configured on the Syn VM (`/opt/minio/secrets/`). If setting up fresh, ensure both systems use the same credentials.

### 4. Archive Master Key (Required for Session Archives)

⚠️ **CRITICAL**: This key encrypts all archived session data. If lost, archived sessions become **permanently unrecoverable**.

```bash
# Generate a cryptographically secure 32-byte (256-bit) key
openssl rand 32 > secrets/archive_master_key

# Set strict permissions
chmod 600 secrets/archive_master_key

# Verify the key is exactly 32 bytes
wc -c secrets/archive_master_key
# Expected output: 32 secrets/archive_master_key
```

**Key Characteristics**:
- Raw binary format (not base64 encoded)
- Exactly 32 bytes (256 bits) for AES-256
- Used with PBKDF2 to derive unique per-archive keys

⚠️ **BACKUP IMMEDIATELY** - See [Key Backup Procedures](#archive-master-key-backup) below.

### 5. Discord Alert Webhook (Optional)

For system alerts and notifications:

1. In Discord: Server Settings → Integrations → Webhooks → New Webhook
2. Copy the webhook URL
3. Create the secret:

```bash
echo "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN" > secrets/discord_alert_token
chmod 600 secrets/discord_alert_token
```

### 6. Redis Password (Optional)

If Redis requires authentication:

```bash
openssl rand -base64 32 > secrets/redis_token
chmod 600 secrets/redis_token
```

### 7. Verify Setup

```bash
# Check files exist and have correct permissions
ls -la secrets/

# Verify no trailing whitespace on text secrets
cat -A secrets/postgres_token
cat -A secrets/minio_root_user
cat -A secrets/minio_root_password

# Verify archive_master_key is exactly 32 bytes (binary)
wc -c secrets/archive_master_key
# Must output: 32 secrets/archive_master_key

# Verify archive_master_key is valid binary
xxd secrets/archive_master_key | head -2
# Should show 32 bytes of hex data
```

---

## Archive Master Key Backup

### Why This Key is Critical

The `archive_master_key` is used to encrypt session archives with AES-256-GCM before they're stored in MinIO. This provides **application-level encryption** on top of ZFS storage encryption.

**Encryption Layers**:
```
Session Data (JSON)
    ↓
AES-256-GCM Encryption (archive_master_key + unique salt)
    ↓
MinIO Storage (Syn VM)
    ↓
ZFS Native Encryption (Syn's ZFS key)
```

If the `archive_master_key` is lost:
- ❌ All existing archived sessions become permanently unreadable
- ❌ The ZFS key alone cannot decrypt session content
- ❌ No recovery is possible without the original key

### Backup Procedures

#### Backup Location 1: Encrypted USB Drive (Primary)

```bash
# On Lofn (10.20.30.253)

# Insert USB drive, find device
lsblk

# Create encrypted partition (one-time setup)
sudo cryptsetup luksFormat /dev/sdX1
sudo cryptsetup luksOpen /dev/sdX1 ash-key-backup
sudo mkfs.ext4 /dev/mapper/ash-key-backup
sudo mount /dev/mapper/ash-key-backup /mnt/usb

# Copy key with metadata
sudo mkdir -p /mnt/usb/ash-dash-keys
sudo cp secrets/archive_master_key /mnt/usb/ash-dash-keys/
echo "$(date -Iseconds) - Lofn - Ash-Dash Archive Master Key" | \
  sudo tee /mnt/usb/ash-dash-keys/README.txt

# Verify
sudo xxd /mnt/usb/ash-dash-keys/archive_master_key | head -2

# Unmount and secure
sudo umount /mnt/usb
sudo cryptsetup luksClose ash-key-backup

# Store USB in fireproof safe, separate from servers
```

#### Backup Location 2: Password Manager (Secondary)

```bash
# Export key as base64 for password manager storage
base64 secrets/archive_master_key

# Store the base64 output in your password manager with:
# - Title: "Ash-Dash Archive Master Key"
# - Notes: "Base64 encoded. Decode with: echo 'BASE64_HERE' | base64 -d > archive_master_key"
# - Tags: "ash", "encryption", "critical"
```

#### Backup Location 3: Printed Paper Key (Offline)

```bash
# Generate hex representation for paper backup
xxd -p secrets/archive_master_key | tr -d '\n'

# Output will be 64 hex characters, e.g.:
# a1b2c3d4e5f6...

# Print and store in fireproof safe
# To restore: echo "HEX_STRING" | xxd -r -p > archive_master_key
```

### Key Restoration

If the key is lost from `secrets/archive_master_key`:

**From Encrypted USB**:
```bash
sudo cryptsetup luksOpen /dev/sdX1 ash-key-backup
sudo mount /dev/mapper/ash-key-backup /mnt/usb
cp /mnt/usb/ash-dash-keys/archive_master_key secrets/
chmod 600 secrets/archive_master_key
sudo umount /mnt/usb
sudo cryptsetup luksClose ash-key-backup
```

**From Password Manager (Base64)**:
```bash
echo "YOUR_BASE64_STRING_HERE" | base64 -d > secrets/archive_master_key
chmod 600 secrets/archive_master_key

# Verify 32 bytes
wc -c secrets/archive_master_key
```

**From Paper Backup (Hex)**:
```bash
echo "YOUR_64_HEX_CHARS_HERE" | xxd -r -p > secrets/archive_master_key
chmod 600 secrets/archive_master_key

# Verify 32 bytes
wc -c secrets/archive_master_key
```

### Key Rotation (Advanced)

Key rotation requires re-encrypting all archives:

1. Generate new key
2. Decrypt all archives with old key
3. Re-encrypt all archives with new key
4. Update backups with new key
5. Securely destroy old key

⚠️ **This is a complex operation** - plan for downtime and test thoroughly.

---

## How It Works

### Docker Secrets (Production)

Secrets are defined in `docker-compose.yml` and mounted at `/run/secrets/`:

```yaml
secrets:
  postgres_token:
    file: ./secrets/postgres_token
  minio_root_user:
    file: ./secrets/minio_root_user
  minio_root_password:
    file: ./secrets/minio_root_password
  archive_master_key:
    file: ./secrets/archive_master_key
  discord_alert_token:
    file: ./secrets/discord_alert_token
  redis_token:
    file: ./secrets/redis_token

services:
  ash-dash:
    secrets:
      - postgres_token
      - minio_root_user
      - minio_root_password
      - archive_master_key
      - discord_alert_token
      - redis_token
```

### Local Development

`SecretsManager` checks locations in order:
1. Docker Secrets (`/run/secrets/`)
2. Local secrets directory (`./secrets/`)
3. Environment variables (`DASH_SECRET_*`)

```python
from src.managers import create_secrets_manager

secrets = create_secrets_manager()

# Database
postgres_pass = secrets.get_postgres_token()

# MinIO Archive Storage
minio_user = secrets.get_minio_root_user()
minio_pass = secrets.get_minio_root_password()

# Archive Encryption (returns raw bytes)
archive_key = secrets.get_archive_master_key()

# Check if archive encryption is configured
if secrets.has_archive_master_key():
    print("Archive encryption available")
```

---

## MinIO Integration

Ash-Dash connects to MinIO on Syn VM for archive storage:

| Setting | Value |
|---------|-------|
| Endpoint | 10.20.30.202 |
| API Port | 30884 |
| Console Port | 30885 |
| Buckets | ash-archives, ash-documents, ash-exports |

### Testing MinIO Connection

```python
from src.managers.archive import create_minio_manager
from src.managers import create_config_manager, create_secrets_manager
from src.managers import create_logging_config_manager

# Initialize managers
config = create_config_manager()
secrets = create_secrets_manager()
logging = create_logging_config_manager(config)

# Create and test MinIO connection
minio = await create_minio_manager(config, secrets, logging)
health = await minio.health_check()
print(health)
```

---

## Security Best Practices

### DO ✅

- Use `chmod 600` for all secret files
- Keep secrets out of Git (verify `.gitignore`)
- Rotate credentials periodically
- Use Docker Secrets in production
- Use separate credentials for dev/prod
- **Backup archive_master_key in 3+ locations**
- **Test key restoration before production use**

### DON'T ❌

- Commit secrets to Git
- Log or print secret values
- Share secrets in chat/email
- Include quotes or whitespace in text files
- Use the same credentials across environments
- **Store archive_master_key only on the server**
- **Assume ZFS encryption replaces application encryption**

---

## File Format

### Text Secrets (passwords, tokens)

Secret files should contain **only** the secret value:

**Correct** ✅
```
mysecretpassword123
```

**Wrong** ❌
```
PASSWORD=mysecretpassword123
```

**Wrong** ❌
```
"mysecretpassword123"
```

### Binary Secrets (encryption keys)

The `archive_master_key` is **raw binary**, not text:

**Correct** ✅
```bash
openssl rand 32 > secrets/archive_master_key
# File contains 32 raw bytes
```

**Wrong** ❌
```bash
openssl rand -base64 32 > secrets/archive_master_key
# File contains 44+ base64 characters, not 32 bytes
```

---

## Troubleshooting

### Secret Not Found

```
DEBUG: Secret 'minio_access_key' not found
```

Check:
1. File exists: `ls -la secrets/minio_root_user`
2. File has content: `cat secrets/minio_root_user`
3. Permissions correct: `chmod 600 secrets/minio_root_user`

### MinIO Connection Failed

```
ERROR: MinIO connection failed: Access denied
```

1. Verify credentials match Syn VM: `ssh syn cat /opt/minio/secrets/minio_root_user`
2. Check MinIO is running: `curl http://10.20.30.202:30884/minio/health/live`
3. Verify firewall allows connection from Lofn

### Archive Master Key Invalid

```
ERROR: Archive master key must be at least 32 bytes
```

1. Check key size: `wc -c secrets/archive_master_key`
2. If not 32 bytes, regenerate: `openssl rand 32 > secrets/archive_master_key`
3. If using base64 encoded key, decode it first

### Permission Denied

```
WARNING: Failed to read secret: Permission denied
```

Fix:
```bash
chmod 600 secrets/*
```

---

## Encryption Key Summary

| Key | Location | Purpose | Recovery Impact |
|-----|----------|---------|-----------------|
| ZFS Key | Syn VM `/root/.zfs-key` | Disk encryption | Loss = raw disk unreadable |
| Archive Master Key | Lofn `secrets/archive_master_key` | Session content encryption | Loss = archived sessions unreadable |
| MinIO Credentials | Both servers | Storage access | Loss = regenerate & reconfigure |

**Both ZFS Key AND Archive Master Key are needed to read archived sessions.**

---

## Support

- **Discord**: [discord.gg/alphabetcartel](https://discord.gg/alphabetcartel)
- **GitHub Issues**: [github.com/the-alphabet-cartel/ash-dash/issues](https://github.com/the-alphabet-cartel/ash-dash/issues)

---

**Built with care for chosen family** 🏳️‍🌈
