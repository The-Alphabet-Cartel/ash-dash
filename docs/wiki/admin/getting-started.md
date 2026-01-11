---
title: Getting Started with Ash-Dash (Admin)
description: Introduction to the Ash-Dash crisis detection dashboard for administrators
category: Administration
tags:
  - getting-started
  - admin
  - setup
  - overview
author: Admin Team
last_updated: "2026-01-10"
version: "2.0"
---

# Getting Started with Ash-Dash

Welcome to Ash-Dash, the crisis detection dashboard for [The Alphabet Cartel](https://discord.gg/alphabetcartel) community. This guide provides an administrative overview.

## What is Ash-Dash?

Ash-Dash is part of the Ash ecosystem—a suite of tools designed to detect and respond to mental health crises within our Discord community.

### The Ash Ecosystem

| Component | Purpose |
|-----------|---------|
| **Ash-Bot** | Monitors Discord messages |
| **Ash-NLP** | Analyzes messages for crisis indicators |
| **Ash-Dash** | Dashboard for CRT members (this app) |
| **Ash-Thrash** | Testing suite |

### Key Features

- **Real-time monitoring** — Crisis alerts with severity levels
- **Session management** — Track interventions from detection to resolution
- **Notes system** — Rich text documentation with WYSIWYG editor
- **User history** — Pattern recognition across sessions
- **Archive storage** — Encrypted long-term storage
- **Wiki documentation** — Training materials and guides
- **Audit logging** — Complete activity tracking

## Authentication

Ash-Dash uses **PocketID** for authentication (OIDC/OAuth2).

### How It Works

1. User visits Ash-Dash
2. Redirected to PocketID login
3. After authentication, PocketID returns user info and group memberships
4. Ash-Dash grants access based on PocketID group membership

### PocketID Groups

| PocketID Group | Ash-Dash Role |
|----------------|---------------|
| `ash-dash-admins` | Admin |
| `ash-dash-crt-leads` | CRT Lead |
| `ash-dash-crt` | CRT Member |
| `ash-dash-viewers` | Viewer |

## Dashboard Overview

### Navigation (Sidebar)

The collapsible sidebar provides access to:

| Section | Description | Access |
|---------|-------------|--------|
| **Dashboard** | Metrics, charts, active sessions | All |
| **Sessions** | Session list with search/filter | All |
| **Archives** | Encrypted long-term storage | CRT Lead, Admin |
| **Wiki** | Documentation and training | All |
| **Admin** | System management | Admin only |

**Tip:** Click the collapse button (bottom of sidebar) to minimize and maximize workspace.

### Dashboard Page

- **Metric Cards** — Active sessions, critical/high count, weekly total, CRT online
- **Crisis Trends Chart** — 30-day session volume
- **CRT Activity Chart** — 7-day team response patterns
- **Active Sessions Panel** — Live list sorted by severity

### Sessions Page

- **Search** — By user ID, username, or session ID
- **Filters** — Severity, status, date range
- **Pagination** — Configurable page size
- **Session Detail** — Full context, notes, user history

### Archives Page

- **Archive List** — Encrypted sessions with retention info
- **Filters** — Date range, retention tier
- **View Archive** — Decrypted read-only view

## Access Levels

| Feature | Admin | CRT Lead | CRT Member | Viewer |
|---------|:-----:|:--------:|:----------:|:------:|
| View Dashboard | ✅ | ✅ | ✅ | ✅ |
| View Sessions | ✅ | ✅ | ✅ | ✅ |
| Add Notes | ✅ | ✅ | ✅ | ❌ |
| Close Sessions | ✅ | ✅ | ✅ | ❌ |
| Archive Sessions | ✅ | ✅ | ❌ | ❌ |
| View Archives | ✅ | ✅ | ❌ | ❌ |
| View Audit Logs | ✅ | ✅ | ❌ | ❌ |
| View System Health | ✅ | ❌ | ❌ | ❌ |
| Manage Users | ✅ | ❌ | ❌ | ❌ |

## Admin Section

Accessible only to administrators:

### Users

- View all users with Ash-Dash access
- See last activity and session counts
- User details and audit history

### Audit Logs

- Complete activity log
- Filter by event type, user, date
- Authentication, session, and admin events

### System Health

- Service status (API, Database, Redis, MinIO)
- Health check indicators
- Latency metrics

## Real-Time Updates

Ash-Dash uses polling for real-time data:

| Data | Poll Interval |
|------|--------------|
| Active Sessions | 10 seconds |
| Metrics/Charts | 30 seconds |

The "Live" indicator shows polling is active.

## Related Documentation

### For Administrators

- [User Management Guide](./user-management.md) — Managing users and roles
- [System Monitoring Guide](./system-monitoring.md) — Health and audit logs
- [Archive Management Guide](./archive-management.md) — Encryption and retention
- [Key Management Guide](./key_management.md) — Encryption key procedures

### For Operations

- [Deployment Guide](../operations/deployment.md) — Production setup
- [Configuration Reference](../operations/configuration.md) — Environment variables
- [Runbook](../operations/runbook.md) — Operating procedures
- [Troubleshooting](../operations/troubleshooting.md) — Common issues

## Getting Help

- **Technical Issues** — Contact Tech team in Discord
- **Configuration** — See Operations documentation
- **CRT Questions** — Contact CRT Leadership

---

*Last updated: 2026-01-10*

**Built with care for chosen family** 🏳️‍🌈
