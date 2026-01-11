---
title: Glossary
description: Definitions of terms used throughout Ash-Dash and CRT documentation
category: Reference
tags:
  - glossary
  - definitions
  - reference
  - terminology
author: Documentation Team
last_updated: "2026-01-10"
version: "2.0"
---

# Glossary

A comprehensive glossary of terms used in Ash-Dash and CRT operations within [The Alphabet Cartel](https://discord.gg/alphabetcartel) community.

## A

### Active Session
A crisis session that is currently open and requiring CRT attention. Active sessions appear on the dashboard and in the sessions list with an "Active" status badge.

### Archive
An encrypted copy of a closed session stored in long-term storage (MinIO). Archives are sealed and cannot be modified, ensuring data integrity for historical records.

### Archive Master Key
The AES-256 encryption key used to encrypt session data before archiving. Loss of this key means permanent loss of all archived data.

### Ash
The complete crisis detection ecosystem used by The Alphabet Cartel. Includes Ash-Bot, Ash-NLP, Ash-Dash, and Ash-Thrash.

### Ash-Bot
The Discord bot component of Ash that monitors community messages and sends them to Ash-NLP for analysis.

### Ash-Dash
The web dashboard (this application!) used by CRT members to monitor and respond to crisis alerts.

### Ash-NLP
The natural language processing server that analyzes messages for crisis indicators using machine learning models.

### Ash-Thrash
The testing suite for the Ash ecosystem.

### Audit Log
A record of all actions taken in Ash-Dash, including logins, session access, note creation, and administrative changes. Used for security and accountability.

## C

### Confidence Score
A percentage (0-100%) indicating how confident Ash-NLP is in its crisis classification. Higher confidence means more certainty in the assessment.

### Crisis Level
See: Severity Level.

### Crisis Score
A numerical score (0.0-1.0) representing the overall crisis severity based on Ash-NLP analysis.

### CRT (Crisis Response Team)
Volunteer team members trained to respond to community members in crisis.

## D

### Dashboard
The main page of Ash-Dash showing active sessions, metrics, and community health indicators.

### Double Encryption
The strategy of encrypting data twice: once at the application level (AES-256-GCM before storage) and once at the storage level (ZFS native encryption). Provides defense in depth.

## E

### Escalation
The process of involving additional CRT members or leadership when a situation requires more support or expertise.

## F

### Frontmatter
YAML metadata at the top of documentation files that includes title, description, tags, and other properties.

## I

### Intervention
The actions taken by CRT members to support a community member in crisis.

## M

### Metrics
Statistical data about CRT operations, including response times, session counts, and activity levels.

### MinIO
S3-compatible object storage service used to store encrypted session archives. Runs on the Syn VM.

## N

### NLP (Natural Language Processing)
The AI technology used by Ash-NLP to analyze text and detect crisis indicators.

## O

### OIDC (OpenID Connect)
The authentication protocol used by PocketID to provide secure single sign-on for Ash-Dash.

## P

### Pattern Detection
Ash's ability to identify escalating behavior patterns across multiple messages from the same user.

### PocketID
The identity provider (OIDC/OAuth2) used for Ash-Dash authentication. Manages user accounts and group memberships.

### Polling
The technique Ash-Dash uses to check for new data at regular intervals (10 seconds for sessions, 30 seconds for metrics).

## R

### Redis
In-memory data store used for real-time session data sharing between Ash-Bot and Ash-Dash.

### Retention Tier
The duration an archived session will be kept before automatic deletion:
- **Standard**: 1 year
- **Extended**: 3 years
- **Permanent**: 7 years

## S

### Session
A crisis incident from detection through resolution. Each session has a unique ID, severity level, notes, and status.

### Session Notes
Documentation written by CRT members about their observations, actions, and follow-up plans for a session.

### Severity Level
The classification of how serious a crisis situation is:
- 🟣 **Critical**: Immediate danger
- 🔴 **High**: Significant distress
- 🟡 **Medium**: Elevated concern
- 🟢 **Low**: Minor concern
- ⚪ **Safe**: No crisis indicators

### Status
The current state of a session:
- **Active**: Open and requiring attention
- **Closed**: Resolved and documented
- **Archived**: Encrypted in long-term storage

## T

### The Alphabet Cartel
The LGBTQIA+ Discord community served by the Ash ecosystem. Visit us at [discord.gg/alphabetcartel](https://discord.gg/alphabetcartel) or [alphabetcartel.org](https://alphabetcartel.org).

### TipTap
The rich text editor library used for session notes in Ash-Dash. Provides formatting options like bold, italic, lists, and links.

### Trigger
A word, phrase, or pattern that causes Ash-NLP to flag a message for review.

## U

### User History
The record of a Discord user's past sessions and interactions with CRT, used to identify patterns and provide context.

## W

### Wiki
The documentation system within Ash-Dash containing guides, training materials, and reference information. Rendered from Markdown files.

## Z

### ZFS
The file system used on the Syn VM for archive storage. Provides native encryption, snapshots, and replication capabilities.

---

*Last updated: 2026-01-10*

*Have a term to add? Contact the Documentation Team.*

**Built with care for chosen family** 🏳️‍🌈
