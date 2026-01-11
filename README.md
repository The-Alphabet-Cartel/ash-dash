# Ash-Dash v5.0

**Crisis Detection Dashboard for [The Alphabet Cartel](https://discord.gg/alphabetcartel) LGBTQIA+ Discord Community**

[![Version](https://img.shields.io/badge/version-5.0.0-purple.svg)](https://github.com/the-alphabet-cartel/ash-dash)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Discord](https://img.shields.io/discord/1234567890?color=7289da&label=Discord&logo=discord&logoColor=white)](https://discord.gg/alphabetcartel)
[![Built with Vue](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vue.js)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)

---

## 🎯 Mission

> **Reveal** → Surface crisis alerts and user escalation patterns in real-time  
> **Enable** → Equip Crisis Response Teams with tools for swift intervention  
> **Clarify** → Translate detection data into actionable intelligence  
> **Protect** → Safeguard our LGBTQIA+ community through vigilant oversight

Ash-Dash is the administrative dashboard for the **Ash Crisis Detection Ecosystem**, providing Crisis Response Team (CRT) members with real-time monitoring, session management, and comprehensive crisis response workflows.

---

## ✨ Features

### 📊 Real-Time Dashboard
- Live session monitoring with auto-refresh
- Crisis severity indicators and trends
- CRT activity tracking
- Quick access to active and recent sessions

### 📋 Session Management
- Detailed session views with full context
- Claim/release sessions to prevent duplicate work
- Session transfer between CRT members
- Close sessions with resolution tracking
- Reopen closed sessions (Lead+ permission)

### 📝 Notes System
- Rich text editor (TipTap WYSIWYG)
- Per-session note threads
- Note locking for completed sessions
- Edit history and attribution

### 🗄️ Archive System
- Automated session archiving
- Double-encrypted storage (AES-256-GCM + ZFS)
- MinIO S3-compatible object storage
- Tiered retention policies
- Archive restoration capabilities

### 🔐 Authentication & Authorization
- PocketID OIDC integration with PKCE
- Role-based access control (Member/Lead/Admin)
- Server-side session management
- Automatic token refresh with race condition protection

### 📚 Documentation Wiki
- Built-in documentation system
- Role-filtered content access
- Full-text search
- PDF export capability

### 🎨 User Experience
- Dark/light theme support
- Collapsible sidebar navigation
- Mobile-responsive design
- Accessibility (WCAG 2.1 AA compliant)

---

## 🏗️ Architecture

Ash-Dash is part of the **Ash Crisis Detection Ecosystem**:

```
┌─────────────────────────────────────────────────────────────┐
│                     Ash Ecosystem                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐    ┌─────────────┐    ┌──────────────┐    │
│   │   Ash-Bot   │───>│   Ash-NLP   │    │  Ash-Dash    │    │
│   │  (Discord)  │<───│   (ML/AI)   │    │ (Dashboard)  │    │
│   └──────┬──────┘    └─────────────┘    └──────┬───────┘    │
│          │                                     │            │
│          │           ┌─────────────┐           │            │
│          └──────────>│    Redis    │<──────────┘            │
│                      │  (Shared)   │                        │
│                      └─────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Component | Purpose | Repository |
|-----------|---------|------------|
| **Ash-Bot** | Discord bot for crisis detection and alerts | [ash-bot](https://github.com/the-alphabet-cartel/ash-bot) |
| **Ash-NLP** | Natural language processing backend | [ash-nlp](https://github.com/the-alphabet-cartel/ash-nlp) |
| **Ash-Dash** | Administrative dashboard (this repo) | [ash-dash](https://github.com/the-alphabet-cartel/ash-dash) |
| **Ash-Thrash** | Integration testing suite | [ash-thrash](https://github.com/the-alphabet-cartel/ash-thrash) |
| **Ash-Vault** | Secure archive storage for sensitive data | [ash-vault](https://github.com/the-alphabet-cartel/ash-vault) |

---

## 🛠️ Tech Stack

### Backend
- **Python 3.11** - Runtime
- **FastAPI** - Async web framework
- **SQLAlchemy 2.0** - ORM with async support
- **PostgreSQL 16** - Primary database
- **Redis** - Session store and shared state
- **MinIO** - S3-compatible archive storage
- **WeasyPrint** - PDF generation

### Frontend
- **Vue.js 3** - Reactive UI framework
- **Vite** - Build tooling
- **TailwindCSS** - Utility-first styling
- **Pinia** - State management
- **TipTap** - Rich text editor
- **Lucide** - Icon library
- **Chart.js** - Data visualization

### Infrastructure
- **Docker** - Containerization
- **PocketID** - OIDC authentication provider

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- PocketID instance (or compatible OIDC provider)
- Redis instance (shared with Ash-Bot)
- MinIO instance (for archives)

### 1. Clone the Repository

```bash
git clone https://github.com/the-alphabet-cartel/ash-dash.git
cd ash-dash
```

### 2. Configure Environment

```bash
cp .env.template .env
# Edit .env with your configuration
```

Required environment variables:
```bash
# Database
DASH_DB_HOST=ash-dash-db
DASH_DB_NAME=ash_dash
DASH_DB_USER=ash_dash

# Redis (shared with Ash-Bot)
DASH_REDIS_HOST=ash-redis
DASH_REDIS_PORT=6379

# OIDC Authentication
DASH_OIDC_ISSUER=https://id.yourdomain.com
DASH_OIDC_CLIENT_ID=your-client-id
DASH_OIDC_REDIRECT_URI=https://dashboard.yourdomain.com/auth/callback

# MinIO Archives
DASH_MINIO_ENDPOINT=minio.yourdomain.com:9000
DASH_MINIO_BUCKET=ash-archives
```

### 3. Configure Secrets

Create Docker secrets for sensitive values:
```bash
mkdir -p secrets
echo "your-db-password" > secrets/dash_db_password
echo "your-oidc-client-secret" > secrets/dash_oidc_client_secret
echo "your-minio-access-key" > secrets/dash_minio_access_key
echo "your-minio-secret-key" > secrets/dash_minio_secret_key
echo "your-archive-encryption-key" > secrets/dash_archive_key
```

### 4. Start the Application

```bash
docker compose up -d
```

The dashboard will be available at `http://localhost:30883` (or your configured port).

### 5. Run Database Migrations

```bash
docker compose exec ash-dash alembic upgrade head
```

---

## ⚙️ Configuration

### Role Mapping

Ash-Dash maps PocketID groups to CRT roles:

| PocketID Group | Dashboard Role | Permissions |
|----------------|----------------|-------------|
| `cartel_crt_admin` | Admin | Full access, delete operations, system config |
| `cartel_crt_lead` | Lead | Reopen sessions, unlock notes, archive management |
| `cartel_crt` | Member | View sessions, add notes, claim sessions |

### Environment Variables

See [.env.template](.env.template) for all available configuration options.

### OIDC Setup

Configure your PocketID (or OIDC provider) client:
- **Callback URL**: `https://yourdomain.com/auth/callback`
- **Logout URL**: `https://yourdomain.com/auth/login`
- **PKCE**: Enabled
- **Public Client**: Disabled (use client secret)

---

## 📖 Documentation

Ash-Dash includes a built-in documentation wiki accessible from the dashboard navigation.

### Documentation Categories

| Category | Access | Description |
|----------|--------|-------------|
| CRT Operations | All CRT | Crisis response procedures and protocols |
| Training | All CRT | Onboarding and training materials |
| Reference | All CRT | Technical reference and API docs |
| Administration | Admin | System administration guides |
| Operations | Admin | Deployment and operational procedures |
| Future Enhancements | All CRT | Planned features and roadmaps |

### Adding Documentation

1. Create a Markdown file in `docs/wiki/<category>/`
2. Add YAML frontmatter with title, description, and tags
3. Restart the container or wait for wiki cache refresh

---

## 🧪 Development

### Local Development Setup

```bash
# Backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm run test
```

### Code Standards

This project follows our internal Clean Architecture Charter:
- Factory function pattern for all managers
- Dependency injection
- Comprehensive error handling
- Structured logging

---

## 📁 Project Structure

```
ash-dash/
├── src/                    # Backend source code
│   ├── api/               # FastAPI routes and middleware
│   ├── managers/          # Business logic managers
│   ├── models/            # SQLAlchemy models
│   ├── services/          # Background services
│   └── utils/             # Utility functions
├── frontend/              # Vue.js frontend
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Page components
│   │   ├── stores/       # Pinia state stores
│   │   └── services/     # API client
│   └── dist/             # Built frontend (Docker)
├── docs/                  # Documentation
│   └── wiki/             # Built-in wiki content
├── migrations/            # Alembic migrations
├── tests/                 # Test suite
└── secrets/              # Docker secrets (gitignored)
```

---

## 🏳️‍🌈 Community

**The Alphabet Cartel** is an LGBTQIA+ Discord community centered around gaming, political discourse, activism, and societal advocacy.

- 🌐 **Website**: [alphabetcartel.org](https://alphabetcartel.org)
- 💬 **Discord**: [discord.gg/alphabetcartel](https://discord.gg/alphabetcartel)
- 🐙 **GitHub**: [github.com/the-alphabet-cartel](https://github.com/the-alphabet-cartel)

---

## 🤝 Contributing

We welcome contributions from the community! Please read our contributing guidelines before submitting pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- The Alphabet Cartel community for inspiration, support, and being chosen family
- All CRT volunteers who dedicate their time to keeping our community safe
- The open-source projects that make this possible

---

## 📊 Version History

| Version | Date | Highlights |
|---------|------|------------|
| v5.0.0 | 2026-01 | Complete recode: Vue 3 frontend, FastAPI backend, OIDC auth, archive system |

---

**Built with care for chosen family** 🏳️‍🌈
