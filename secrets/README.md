# Ash-Dash Secrets

**Version**: v5.0-8-8.1-1
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
| `minio_access_key` | MinIO access key (username) | ✅ Required | Archive storage |
| `minio_secret_key` | MinIO secret key (password) | ✅ Required | Archive storage |
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

```bash
# Get credentials from Syn VM's MinIO setup
# These should match the credentials in /opt/minio/secrets/ on Syn

# MinIO access key (username)
echo "ashadmin" > secrets/minio_access_key
chmod 600 secrets/minio_access_key

# MinIO secret key (password) - copy from Syn VM
cat /opt/minio/secrets/minio_root_password > secrets/minio_secret_key
# Or if setting up new:
openssl rand -base64 32 > secrets/minio_secret_key
chmod 600 secrets/minio_secret_key
```

**Important**: The MinIO credentials must match what's configured on the Syn VM. If you're setting up fresh, ensure both systems use the same credentials.

### 4. Discord Alert Webhook (Optional)

For system alerts and notifications:

1. In Discord: Server Settings → Integrations → Webhooks → New Webhook
2. Copy the webhook URL
3. Create the secret:

```bash
echo "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN" > secrets/discord_alert_token
chmod 600 secrets/discord_alert_token
```

### 5. Redis Password (Optional)

If Redis requires authentication:

```bash
openssl rand -base64 32 > secrets/redis_token
chmod 600 secrets/redis_token
```

### 6. Verify Setup

```bash
# Check files exist and have correct permissions
ls -la secrets/

# Verify no trailing whitespace (should show $ at end of line)
cat -A secrets/postgres_token
cat -A secrets/minio_access_key
cat -A secrets/minio_secret_key
```

---

## How It Works

### Docker Secrets (Production)

Secrets are defined in `docker-compose.yml` and mounted at `/run/secrets/`:

```yaml
secrets:
  postgres_token:
    file: ./secrets/postgres_token
  minio_access_key:
    file: ./secrets/minio_access_key
  minio_secret_key:
    file: ./secrets/minio_secret_key
  discord_alert_token:
    file: ./secrets/discord_alert_token
  redis_token:
    file: ./secrets/redis_token

services:
  ash-dash:
    secrets:
      - postgres_token
      - minio_access_key
      - minio_secret_key
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
minio_key = secrets.get_minio_access_key()
minio_secret = secrets.get_minio_secret_key()

# Check if MinIO is configured
if secrets.has_minio_credentials():
    print("MinIO credentials available")
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

### DON'T ❌

- Commit secrets to Git
- Log or print secret values
- Share secrets in chat/email
- Include quotes or whitespace in files
- Use the same credentials across environments

---

## File Format

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

---

## Troubleshooting

### Secret Not Found

```
DEBUG: Secret 'minio_access_key' not found
```

Check:
1. File exists: `ls -la secrets/minio_access_key`
2. File has content: `cat secrets/minio_access_key`
3. Permissions correct: `chmod 600 secrets/minio_access_key`

### MinIO Connection Failed

```
ERROR: MinIO connection failed: Access denied
```

1. Verify credentials match Syn VM: `ssh syn cat /opt/minio/secrets/minio_root_user`
2. Check MinIO is running: `curl http://10.20.30.202:30884/minio/health/live`
3. Verify firewall allows connection from Lofn

### Permission Denied

```
WARNING: Failed to read secret: Permission denied
```

Fix:
```bash
chmod 600 secrets/*
```

---

## Support

- **Discord**: [discord.gg/alphabetcartel](https://discord.gg/alphabetcartel)
- **GitHub Issues**: [github.com/the-alphabet-cartel/ash-dash/issues](https://github.com/the-alphabet-cartel/ash-dash/issues)

---

**Built with care for chosen family** 🏳️‍🌈
