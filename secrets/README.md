# Ash-Dash Secrets

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

| File | Description | Required |
|------|-------------|----------|
| `postgres_password` | PostgreSQL database password | **Required** |
| `discord_alert_token` | Discord webhook for system alerts | Optional |
| `redis_token` | Redis password (if authentication enabled) | Optional |
| `claude_api_token` | Claude API key (for future AI features) | Optional |
| `webhook_token` | Webhook signing secret | Optional |

---

## Setup Instructions

### 1. Create the secrets directory

```bash
mkdir -p secrets
```

### 2. Add PostgreSQL Password (Required)

```bash
# Create the secret file (no file extension)
echo "your_secure_database_password" > secrets/postgres_password

# Set secure permissions
chmod 600 secrets/postgres_password
```

**Important**: Change this from the default `changeme_in_production` before deploying!

### 3. Add Discord Alert Webhook (Optional)

For system alerts (service failures, startup notifications):

1. In Discord: Server Settings → Integrations → Webhooks → New Webhook
2. Copy the webhook URL
3. Create the secret:

```bash
# Create the webhook secret
echo "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN" > secrets/discord_alert_token

# Set secure permissions
chmod 600 secrets/discord_alert_token
```

### 4. Add Redis Password (Optional)

If your Redis instance requires authentication:

```bash
# Create the secret file
echo "your_redis_password" > secrets/redis_token

# Set secure permissions
chmod 600 secrets/redis_token
```

### 5. Verify Setup

```bash
# Check files exist and have content
ls -la secrets/

# Verify permissions (should be 600 or rw-------)
stat secrets/postgres_password
```

---

## How It Works

### Docker Secrets (Production)

When running with Docker Compose, secrets are:
1. Defined in `docker-compose.yml`
2. Mounted to `/run/secrets/<name>` inside the container
3. Read by `SecretsManager` at startup

```yaml
# docker-compose.yml
secrets:
  postgres_password:
    file: ./secrets/postgres_password

services:
  ash-dash:
    secrets:
      - postgres_password
```

Inside the container, the secret is available at:
```
/run/secrets/postgres_password
```

### PostgreSQL Container

The PostgreSQL container reads the password via `POSTGRES_PASSWORD_FILE`:

```yaml
services:
  ash-dash-db:
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
    secrets:
      - postgres_password
```

### Local Development

For local development without Docker:
1. `SecretsManager` checks `/run/secrets/` first
2. Falls back to `./secrets/` directory
3. Finally checks environment variables

```python
from src.managers import get_secret

password = get_secret("postgres_password")
```

---

## Security Best Practices

### DO ✅

- Use `chmod 600` for secret files
- Keep secrets out of Git (check `.gitignore`)
- Rotate passwords periodically
- Use Docker Secrets in production
- Use strong, unique passwords

### DON'T ❌

- Commit secrets to Git
- Log or print secret values
- Share secrets in chat/email
- Use the same password for dev and prod
- Use the default `changeme_in_production` password

---

## File Format

Secret files should contain **only** the secret value:

**Correct** ✅
```
mysecurepassword123
```

**Wrong** ❌
```
POSTGRES_PASSWORD=mysecurepassword123
```

**Wrong** ❌
```
"mysecurepassword123"
```

---

## Troubleshooting

### Secret Not Found

```
DEBUG: Secret 'postgres_password' not found
```

Check:
1. File exists: `ls -la secrets/postgres_password`
2. File has content: `cat secrets/postgres_password`
3. No extra whitespace: `cat -A secrets/postgres_password`

### Permission Denied

```
WARNING: Failed to read secret: Permission denied
```

Fix permissions:
```bash
chmod 600 secrets/postgres_password
```

### Database Connection Failed

If PostgreSQL won't start or accept connections:

1. Check the password file exists and has content
2. Verify the `POSTGRES_PASSWORD_FILE` environment variable is set
3. Check PostgreSQL logs: `docker-compose logs ash-dash-db`

### Docker Secrets Not Mounting

Verify in docker-compose.yml:
```yaml
secrets:
  postgres_password:
    file: ./secrets/postgres_password

services:
  ash-dash:
    secrets:
      - postgres_password
```

Check inside container:
```bash
docker exec ash-dash ls -la /run/secrets/
docker exec ash-dash cat /run/secrets/postgres_password
```

---

## Adding New Secrets

1. Create the secret file in `secrets/`
2. Add to `docker-compose.yml`:
   ```yaml
   secrets:
     new_secret:
       file: ./secrets/new_secret
   
   services:
     ash-dash:
       secrets:
         - new_secret
   ```
3. Add to `KNOWN_SECRETS` in `src/managers/secrets_manager.py`
4. Access in code:
   ```python
   from src.managers import get_secret
   value = get_secret("new_secret")
   ```

---

## Support

- **Discord**: [discord.gg/alphabetcartel](https://discord.gg/alphabetcartel)
- **Website**: [alphabetcartel.org](https://alphabetcartel.org)
- **GitHub Issues**: [github.com/the-alphabet-cartel/ash-dash/issues](https://github.com/the-alphabet-cartel/ash-dash/issues)

---

**Built with care for chosen family** 🏳️‍🌈
