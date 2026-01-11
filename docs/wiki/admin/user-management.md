---
title: User Management Guide
description: How to manage CRT users and roles in Ash-Dash
category: Administration
tags:
  - admin
  - users
  - roles
  - management
author: Admin Team
last_updated: "2026-01-10"
version: "1.0"
---

# User Management Guide

This guide covers managing users in Ash-Dash for [The Alphabet Cartel](https://discord.gg/alphabetcartel) administrators.

## Overview

Ash-Dash uses **PocketID** for authentication. Users are managed through a combination of:

- **PocketID** — Identity and authentication
- **PocketID Groups** — Role assignments
- **Ash-Dash** — User activity and audit logs

## Access Roles

### Role Hierarchy

| Role | Access Level | Typical Users |
|------|--------------|---------------|
| **Admin** | Full system access | Server admins, Tech leads |
| **CRT Lead** | Session management + reports | CRT leadership |
| **CRT Member** | Dashboard + sessions | Crisis responders |
| **Viewer** | Read-only dashboard | Training observers |

### Role Permissions

| Feature | Admin | CRT Lead | CRT Member | Viewer |
|---------|:-----:|:--------:|:----------:|:------:|
| View Dashboard | ✅ | ✅ | ✅ | ✅ |
| View Sessions | ✅ | ✅ | ✅ | ✅ |
| Add Notes | ✅ | ✅ | ✅ | ❌ |
| Close Sessions | ✅ | ✅ | ✅ | ❌ |
| Archive Sessions | ✅ | ✅ | ❌ | ❌ |
| View Archives | ✅ | ✅ | ❌ | ❌ |
| View Audit Logs | ✅ | ✅ | ❌ | ❌ |
| Manage Users | ✅ | ❌ | ❌ | ❌ |
| System Settings | ✅ | ❌ | ❌ | ❌ |

## Adding New Users

### Step 1: PocketID Account

Ensure the user has a PocketID account:

1. Direct them to the PocketID registration page
2. They complete registration with email verification
3. Account is created but has no Ash-Dash access yet

### Step 2: Assign to CRT Group

In PocketID Admin:

1. Navigate to **Groups**
2. Find the appropriate group:
   - `ash-dash-admins` — For administrators
   - `ash-dash-crt-leads` — For CRT leadership
   - `ash-dash-crt` — For CRT members
   - `ash-dash-viewers` — For read-only access
3. Click **Add Member**
4. Search for the user's email or username
5. Click **Add** to confirm

### Step 3: Verify Access

Have the new user:

1. Log into Ash-Dash
2. Confirm they see appropriate menu items
3. Check they can access expected features

## Removing User Access

### Immediate Removal

To revoke access immediately:

1. Go to PocketID Admin → **Groups**
2. Find the user in the appropriate group
3. Click **Remove** next to their name
4. User loses access on next login (or session refresh)

### Graceful Offboarding

For planned departures:

1. Notify the user of the timeline
2. Ensure any open sessions are handed off
3. Review audit logs for any cleanup needed
4. Remove from PocketID group
5. Document the offboarding

## Viewing Users in Ash-Dash

Navigate to **Admin → Users** to see:

### User List

| Column | Description |
|--------|-------------|
| **User** | Name and avatar from PocketID |
| **Role** | Current access level |
| **Last Active** | Most recent dashboard activity |
| **Sessions Handled** | Total sessions they've worked |
| **Status** | Active/Inactive |

### User Detail

Click a user to see:

- Account information
- Activity history
- Sessions they've handled
- Notes they've written
- Audit log entries

## Troubleshooting Access Issues

### "Unauthorized" Error

**Cause:** User not in any Ash-Dash PocketID group

**Solution:** Add them to appropriate group in PocketID

### User Can't See Admin Menu

**Cause:** User in `ash-dash-crt` but not `ash-dash-admins`

**Solution:** Verify role requirements; add to admin group if appropriate

### User Shows as "Inactive"

**Cause:** No activity in past 30 days

**Solution:** Not necessarily a problem; user may not have had sessions

### Login Works But Dashboard Empty

**Cause:** Usually a browser cache issue

**Solution:** Have user clear cache and cookies, then retry

## Audit Considerations

All user management actions are logged:

- Group membership changes (in PocketID)
- Login events
- Session access
- Note creation
- Administrative actions

Review audit logs periodically for:

- Unusual access patterns
- Failed login attempts
- Unexpected role changes

## Best Practices

### Principle of Least Privilege

- Only grant the access level needed
- Start with CRT Member, elevate if needed
- Review permissions quarterly

### Regular Access Reviews

- Monthly: Check for inactive users
- Quarterly: Verify role assignments are current
- Annually: Full access audit

### Documentation

- Document why each user has their role
- Note who approved elevated access
- Keep offboarding records

## Emergency Procedures

### Compromised Account

If you suspect an account is compromised:

1. **Immediately** remove from all Ash-Dash groups in PocketID
2. Reset their PocketID password
3. Review audit logs for suspicious activity
4. Investigate scope of potential breach
5. Re-enable access only after security review

### Mass Access Revocation

In case of security incident:

1. Contact PocketID admin to lock groups
2. Disable OAuth integration temporarily
3. Investigate and remediate
4. Re-enable with fresh tokens

---

*Last updated: 2026-01-10*

*For PocketID administration, see the PocketID Admin Guide.*

**Built with care for chosen family** 🏳️‍🌈
