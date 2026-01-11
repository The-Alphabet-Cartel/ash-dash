---
title: Frequently Asked Questions
description: Common questions about Ash-Dash and CRT operations
category: Reference
tags:
  - faq
  - questions
  - help
  - support
author: Documentation Team
last_updated: "2026-01-10"
version: "2.0"
---

# Frequently Asked Questions

Common questions about Ash-Dash and Crisis Response Team operations at [The Alphabet Cartel](https://discord.gg/alphabetcartel).

## General Questions

### What is Ash?

Ash is our crisis detection ecosystem that helps identify community members who may be struggling. It consists of:

- **Ash-Bot** — Monitors Discord messages
- **Ash-NLP** — Analyzes messages using AI
- **Ash-Dash** — Dashboard for CRT (this app!)
- **Ash-Thrash** — Testing suite

### Who can use Ash-Dash?

Ash-Dash is available to:

| Role | Access Level |
|------|--------------|
| Admin | Full system access |
| CRT Lead | Sessions, archives, reports |
| CRT Member | Dashboard, sessions, wiki |
| Viewer | Read-only dashboard |

### How do I get access?

Access is managed through PocketID groups. Contact CRT Leadership to be added to the appropriate group.

### Is my data private?

Yes. Session data is only accessible to authorized CRT members. Archives are encrypted with AES-256 encryption. We follow strict privacy protocols and never share information without consent.

## Logging In

### How do I log in?

Ash-Dash uses **PocketID** for authentication:

1. Visit the Ash-Dash URL
2. Click "Sign in with PocketID"
3. Enter your PocketID credentials
4. You'll be redirected back to the dashboard

### I can't log in / "Unauthorized" error

This usually means you're not in a CRT PocketID group. Contact CRT Leadership to verify your access.

### How do I reset my password?

Password resets are handled through PocketID, not Ash-Dash. Visit the PocketID portal or contact an admin.

### How long does my login session last?

Sessions last 24 hours. After that, you'll be prompted to log in again.

## Using the Dashboard

### How do I know when there's a new crisis?

Active sessions appear on the Dashboard page. You'll see:

- A count of active sessions (metric cards)
- Sessions listed by severity in the Active Sessions panel
- The "Live" indicator confirms real-time polling is active

### What do the severity colors mean?

| Color | Level | Meaning |
|-------|-------|---------|
| 🟣 Purple | Critical | Immediate danger — respond NOW |
| 🔴 Red | High | Significant distress — respond within 1 hour |
| 🟡 Yellow | Medium | Elevated concern — respond within 4 hours |
| 🟢 Green | Low | Minor concern — monitor |
| ⚪ Gray | Safe | No crisis indicators |

### How often does data refresh?

- **Active Sessions**: Every 10 seconds
- **Metrics and Charts**: Every 30 seconds

You can also click the Refresh button for immediate updates.

### Can I collapse the sidebar?

Yes! Click the collapse button at the bottom of the sidebar. Your preference is saved automatically.

## Session Management

### How do I write session notes?

1. Open a session from the Sessions page
2. Scroll to the Notes panel
3. Click "Add Note"
4. Use the rich text editor to write your observations
5. Click Save (or it auto-saves)

See the [Notes Best Practices](../crt/notes-best-practices.md) guide for tips.

### Can I edit my notes?

Yes, you can edit your own notes while the session is active. Once a session is archived, notes become read-only.

### What happens when I close a session?

Closed sessions remain in the database and can be viewed in the Sessions list. They can be reopened if needed (admin only) or archived for long-term storage.

### What is archiving?

Archiving moves a closed session to encrypted long-term storage (MinIO). Archived sessions:

- Are encrypted with AES-256
- Cannot be modified or reopened
- Have retention periods (1-7 years)
- Are only accessible by CRT Leads and Admins

## Archives

### Who can view archives?

Only CRT Leads and Admins can access the Archives section.

### Can archived sessions be edited?

No. Archived sessions are permanently sealed to maintain data integrity.

### How long are archives kept?

| Retention Tier | Duration |
|----------------|----------|
| Standard | 1 year |
| Extended | 3 years |
| Permanent | 7 years |

### Can I extend an archive's retention?

Yes (CRT Lead/Admin only). Retention can be extended but never shortened.

## CRT Operations

### What should I do if I don't know how to respond?

It's okay to ask for help! You can:

- Reach out to another CRT member
- Post in the CRT channel
- Contact CRT Leadership
- Use the buddy system for difficult cases

### When should I escalate?

Escalate when:

- There's immediate danger
- The situation is complex
- You feel overwhelmed
- It involves minors
- You're unsure what to do

### How do I take a break?

1. Let CRT Leadership know you need time off
2. No explanation needed — we trust you
3. The team will cover
4. Come back when you're ready

### What if I make a mistake?

We're all human. If you make a mistake:

- Don't panic
- Reach out to your mentor or leadership
- Document what happened
- Learn from it
- Move forward with compassion for yourself

## Technical Issues

### The dashboard isn't loading

Try these steps:

1. Refresh the page (Ctrl+F5 for hard refresh)
2. Clear your browser cache
3. Try a different browser
4. Check your internet connection
5. Contact the Tech team if issues persist

### I can't access a session

This might happen if:

- The session was archived (check Archives if you have access)
- Your permissions changed
- There's a technical issue

Contact the Admin team for help.

### My notes didn't save

Notes auto-save after you stop typing. If they didn't save:

- Check your internet connection
- Look for error messages (red banner)
- Try saving manually with the Save button
- Contact the Admin team if the issue continues

### The "Live" indicator is red

This means real-time polling has stopped. Try:

1. Refreshing the page
2. Checking your internet connection
3. The system may be undergoing maintenance

## Getting Help

### Where can I ask questions?

- **CRT Channel** — For operational questions
- **Wiki** — Search the documentation
- **Admin Team** — For technical issues
- **CRT Leadership** — For complex situations

### How do I suggest improvements?

We love feedback! You can:

- Post in the CRT feedback channel
- Talk to your mentor
- Contact CRT Leadership
- Submit ideas to the Tech team

### How do I report a bug?

1. Note what you were doing when it happened
2. Screenshot any error messages
3. Post in the tech support channel or contact Admin team

---

*Have a question not listed here? Reach out in the CRT channel!*

*Last updated: 2026-01-10*

**Built with care for chosen family** 🏳️‍🌈
