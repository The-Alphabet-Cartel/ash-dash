---
title: Session Management Guide
description: How to view, manage, and close crisis sessions in Ash-Dash
category: CRT Operations
tags:
  - sessions
  - management
  - workflow
  - procedures
author: CRT Team
last_updated: "2026-01-10"
version: "1.0"
---

# Session Management Guide

This guide covers everything you need to know about managing crisis sessions in Ash-Dash for [The Alphabet Cartel](https://discord.gg/alphabetcartel) community.

## What is a Session?

A **session** represents a detected crisis event for a Discord user. Sessions are created automatically when Ash-Bot and Ash-NLP detect concerning messages and contain:

- The Discord user's information
- Flagged messages that triggered the alert
- NLP analysis scores and risk factors
- CRT notes and actions taken
- Timeline of the intervention

## Viewing Sessions

### Active Sessions (Dashboard)

The Dashboard shows sessions needing attention. Sessions are color-coded by severity:

| Severity | Color | Response Time |
|----------|-------|---------------|
| Critical | 🟣 Purple | Immediate |
| High | 🔴 Red | Within 1 hour |
| Medium | 🟡 Yellow | Within 4 hours |
| Low | 🟢 Green | Monitor |
| Safe | ⚪ Gray | No action needed |

### Session History (Sessions Page)

Navigate to **Sessions** to see all sessions with powerful filtering:

#### Search

Type in the search box to find sessions by:
- Discord User ID
- Discord Username
- Session ID

#### Filters

| Filter | Options |
|--------|---------|
| **Severity** | Critical, High, Medium, Low, Safe |
| **Status** | Active, Closed, Archived |
| **Date Range** | From/To date pickers |

#### Pagination

- Default: 20 sessions per page
- Use page controls at the bottom
- Adjust page size (10, 20, 50, 100)

## Session Detail View

Click any session to see the full details:

### Header Section

- Discord user info (name, ID, avatar)
- Current severity level
- Session status (Active/Closed)
- Session timeline

### Ash Analysis Panel

Shows NLP analysis results:

- **Crisis Score** — Overall risk assessment (0-100)
- **Risk Factors** — Specific concerns detected
- **Confidence Level** — How certain the NLP is

### Flagged Messages

The messages that triggered the alert, with:
- Timestamp
- Channel name
- Message content
- Individual analysis scores

### User History

Previous sessions for this user, showing:
- Past session dates
- Previous severity levels
- Pattern indicators

**Important:** User history helps identify recurring patterns. A user with multiple sessions may need different support strategies.

### Session Notes

CRT notes documenting the intervention (see [Notes Best Practices](./notes-best-practices.md)).

## Session Workflow

### 1. Claim a Session

When you start working on a session:

1. Click the session to view details
2. The session is now "assigned" to you (future feature)
3. Begin your assessment

### 2. Assess the Situation

Review in order:

1. **Flagged messages** — What triggered the alert?
2. **Crisis score** — How severe is the NLP assessment?
3. **Risk factors** — What specific concerns?
4. **User history** — Any patterns or previous sessions?

### 3. Take Action

Based on your assessment:

- **Reach out** to the user via Discord DM
- **Monitor** the situation in real-time
- **Escalate** if needed (contact CRT lead)
- **Involve emergency services** for immediate danger

### 4. Document Everything

Add notes as you go (see [Notes Best Practices](./notes-best-practices.md)):

- Initial assessment
- Actions taken
- User responses
- Resources shared
- Follow-up plans

### 5. Close the Session

When the crisis is resolved:

1. Click **Close Session**
2. Add a closing summary (optional but recommended)
3. The session moves to "Closed" status

### 6. Archive (Optional)

For significant cases that should be preserved:

1. CRT Lead/Admin clicks **Archive Session**
2. Session is encrypted and moved to long-term storage
3. Archived sessions cannot be reopened

## Understanding Severity Levels

### How Severity is Determined

Ash-NLP analyzes messages for:

- **Keywords** — Crisis-related terms
- **Sentiment** — Emotional tone
- **Context** — Surrounding messages
- **Patterns** — Historical behavior

### Manual Override

CRT members can adjust severity if the NLP assessment seems incorrect:

1. Your notes should document why you disagree
2. Contact CRT lead for significant discrepancies
3. This helps improve the NLP over time

## Tips for Effective Session Management

### Do's

✅ Review user history before reaching out
✅ Document your actions in real-time
✅ Use the session notes as a collaborative space
✅ Close sessions promptly when resolved
✅ Escalate when unsure

### Don'ts

❌ Leave sessions unattended for long periods
❌ Close sessions without documentation
❌ Make assumptions without reading context
❌ Share session details outside CRT
❌ Forget self-care during difficult sessions

## Frequently Asked Questions

**Q: What if I disagree with the severity level?**
A: Document your assessment in the notes and contact your CRT lead. Your feedback helps improve the system.

**Q: Can I reopen a closed session?**
A: Only admins can reopen sessions. Contact CRT leadership if needed.

**Q: What if a user has multiple active sessions?**
A: This shouldn't happen—new alerts for the same user update the existing session. Report this to admins if you see it.

**Q: How long are sessions kept?**
A: Active and closed sessions are kept indefinitely. Archived sessions follow retention policies (1-7 years).

---

*Last updated: 2026-01-10*

*For questions, reach out in the CRT Discord channel.*

**Built with care for chosen family** 🏳️‍🌈
