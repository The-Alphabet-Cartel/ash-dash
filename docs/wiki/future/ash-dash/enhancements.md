---
title: "Ash-Dash - Future Enhancements"
description: "Planned features and improvements for Ash-Dash"
category: future
tags:
  - roadmap
  - planning
  - ash-dash
author: "PapaBearDoes"
version: "5.0"
last_updated: "2026-01-11"
---
# Ash-Dash: Future Enhancements & Improvements

============================================================================
**Ash-Dash**: Crisis Detection Dashboard For The Alphabet Cartel Community  
**The Alphabet Cartel** - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================

**Document Version**: v5.0  
**Created**: 2026-01-11  
**Phase**: 1 (Future Planning)  
**Status**: 📋 Backlog  
**Last Updated**: 2026-01-11

---

## Table of Contents

1. [Overview](#overview)
2. [Active Enhancements](#active-enhancements)
3. [Back Burner](#back-burner)
4. [Considered But Deferred](#considered-but-deferred)
5. [Requests](#requests)
6. [Research](#research)
7. [How To Add Ideas](#how-to-add-ideas)

---

## 📋 Overview

This document tracks potential enhancements and feature ideas for Ash-Dash beyond the core v5.0 roadmap. Items are organized by priority and implementation complexity.

### Priority Legend

| Priority | Description |
|----------|-------------|
| 🔴 High | Significant user value, should be scheduled soon |
| 🟡 Medium | Good to have, schedule when capacity allows |
| 🟢 Low | Nice to have, opportunistic implementation |
| ⚪ Someday | Long-term vision, no immediate plans |

### Complexity Legend

| Complexity | Description |
|------------|-------------|
| 🟦 Low | < 4 hours, minimal dependencies |
| 🟨 Medium | 4-8 hours, some dependencies |
| 🟧 High | 8-16 hours, significant work |
| 🟥 Very High | 16+ hours, major feature |

---

## 🎯 Active Enhancements

Features we actively want to implement after the core roadmap is complete.

### 1. ~~Collapsible Sidebar~~ ✅ IMPLEMENTED

**Priority**: 🔴 High  
**Complexity**: 🟦 Low  
**Status**: ✅ Completed in Phase 11 (v5.0-11-11.1-1)  
**Implemented**: 2026-01-10

Allow users to collapse the left navigation sidebar into an icons-only mode, providing more horizontal space for main content.

**Implemented Features**:
- **Expanded Mode**: Full 256px sidebar with icons and labels
- **Collapsed Mode**: 64px sidebar with icons only
  - Hover tooltips show label text
  - Navigation works normally
- **Toggle Button**: Collapse/expand button at bottom of sidebar
- **Persistence**: User preference saved to localStorage (`ash-dash-sidebar`)
- **Smooth Transitions**: 200ms CSS transitions for width changes
- **Accessibility**: Full ARIA labels, keyboard navigation support
- **Theme Toggle**: Compact mode in collapsed state with tooltip
- **User Info**: Avatar-only display when collapsed with tooltip for details

**Files Modified**:
- `frontend/src/stores/ui.js` - New UI state store
- `frontend/src/components/layout/Sidebar.vue` - Collapse functionality
- `frontend/src/components/layout/MainLayout.vue` - Responsive margin
- `frontend/src/components/layout/Header.vue` - Mobile toggle + accessibility
- `frontend/src/components/layout/ThemeToggle.vue` - Compact mode support
- `frontend/tailwind.config.js` - Sidebar-collapsed spacing
- `frontend/src/assets/styles/main.css` - Transition utilities

---

### 2. ~~Session Claim Button~~ ✅ IMPLEMENTED

**Priority**: 🔴 High  
**Complexity**: 🟦 Low  
**Status**: ✅ Completed (v5.0-11-11.4-1)  
**Implemented**: 2026-01-11

Add a "Claim" button to the Session Detail page header, next to the "Close Session" button.

**Implemented Features**:
- **Unassigned Session**: Green "Claim" button with UserPlus icon
  - Clicking assigns the current authenticated user to the session
  - Button changes to "Release" after claiming
- **Claimed by You**: Amber "Release" button with UserMinus icon
  - Clicking unassigns you from the session
- **Claimed by Someone Else**: Blue "Assigned to [Name]" badge with User icon
  - Displays the assigned CRT member's name
- Loading states with disabled buttons during operations
- Store methods: `assignSession()` and `unassignSession()` added to sessions store

**Files Modified**:
- `frontend/src/stores/sessions.js` - Added assignSession/unassignSession methods
- `frontend/src/pages/SessionDetail.vue` - Added Claim/Release button UI

**Benefit**: Prevents duplicate work when multiple CRT members are online.

---

### 3. Note Templates

**Priority**: 🔴 High  
**Complexity**: 🟨 Medium  
**Depends On**: None  
**Estimated Time**: 3-5 hours

Quick-insert common response patterns into the notes editor.

**Features**:
- "Initial Contact" - Standard opening documentation
- "Resources Provided" - List of resources shared with user
- "Follow-up Scheduled" - Scheduling template with date/time placeholder
- "Escalation Needed" - Template for escalating to admin
- "Session Summary" - Closing summary template

**Implementation**:
- Dropdown in Toolbar: Add template selector to EditorToolbar
- Or Slash Commands: Type `/template` to see options (like Notion)
- Templates stored in PostgreSQL `note_templates` table or JSON config file for v1

**Benefit**: Faster documentation, consistent note quality across CRT members.

---

### 4. Saved Search Filters

**Priority**: 🟡 Medium  
**Complexity**: 🟦 Low  
**Depends On**: Phase 10 (to save per-user)  
**Estimated Time**: 2-3 hours

Save commonly-used filter combinations on the Sessions page.

**Features**:
- "My Active Sessions" - Status: Active, Assigned: Me
- "Unassigned Critical" - Status: Active, Severity: Critical, Assigned: None
- "This Week's Closed" - Status: Closed, Date: This Week
- Save button next to filters
- Dropdown to select saved filters

**Implementation**:
- Store in localStorage (immediate) or PostgreSQL (after Phase 10)

**Benefit**: Faster navigation to frequently-viewed session sets.

---

### 5. Shift Handoff View

**Priority**: 🔴 High  
**Complexity**: 🟨 Medium  
**Depends On**: Phase 10 (to track last login)  
**Estimated Time**: 5-7 hours

Summary view of what happened since the CRT member last logged in.

**Features**:
- "Since you were last here (8 hours ago):"
  - X new sessions opened
  - X sessions escalated to Critical/High
  - X sessions closed
  - X notes added to your assigned sessions
  - Notable events summary

**Implementation**:
- Track `last_seen_at` timestamp per user
- Query for changes since that timestamp
- Display as modal on login or dashboard card

**Benefit**: Quick situational awareness at shift start, no need to dig through history.

---

### 6. Session Priority Flag

**Priority**: 🟡 Medium  
**Complexity**: 🟦 Low  
**Depends On**: None  
**Estimated Time**: 2-3 hours

Manual "flag for attention" beyond automated severity scoring.

**Features**:
- Add `is_flagged` boolean and `flag_reason` text to Session model
- Flag/unflag button on Session Detail page
- Filter option on Sessions list: "Show Flagged Only"
- Visual indicator (flag icon, different border color)

**Implementation**:
- Alembic migration for new columns
- API endpoint for flag/unflag
- Frontend button and filter

**Benefit**: Human judgment layer on top of automated detection.

---

### 7. Session Transfer

**Priority**: 🔴 High  
**Complexity**: 🟨 Medium  
**Depends On**: Phase 10 (Authentication)  
**Estimated Time**: 4-5 hours

Formally hand off a claimed session to another specific CRT member.

**Features**:
- "Transfer" button on Session Detail (visible when you have it claimed)
- Modal with dropdown of active CRT members
- Optional handoff note field for context
- Audit log entry for the transfer
- Optionally auto-creates a note documenting the handoff

**Implementation**:
- API: `POST /sessions/{id}/transfer` with `target_user_id` and optional `note`
- Frontend modal component
- Store method for transfer action

**Benefit**: Clean shift transitions without losing session context.

---

### 8. Session Tags/Labels

**Priority**: 🟡 Medium  
**Complexity**: 🟨 Medium  
**Depends On**: None  
**Estimated Time**: 6-8 hours

Custom categorization beyond automated severity scoring.

**Features**:
- Crisis types: `housing`, `family`, `medical`, `financial`, `identity`
- Status modifiers: `needs-followup`, `external-referral`, `recurring`
- Tag management in Admin settings
- Tag chips displayed on Session Detail and Sessions list
- Filter sessions by tag on Sessions page
- Color-coded tags for quick visual identification

**Implementation**:
- New `session_tags` junction table (many-to-many)
- Admin tag management page
- Frontend tag components

**Benefit**: Pattern analysis over time, easier categorization for reporting.

---

### 9. Archive Search

**Priority**: 🟡 Medium  
**Complexity**: 🟨 Medium  
**Depends On**: Phase 9 (Archives)  
**Estimated Time**: 6-8 hours

Full-text search through archived session content.

**Features**:
- Search session summaries, note content (decrypted), Discord usernames, date ranges
- Respect archive access permissions
- Audit log all archive searches

**Implementation**:
- PostgreSQL Full-Text Search using `tsvector` on archived content
- Or maintain separate searchable index of non-sensitive metadata

**Benefit**: Find historical patterns and reference past similar situations.

---

### 10. User Risk Profile Summary

**Priority**: 🟡 Medium  
**Complexity**: 🟧 High  
**Depends On**: Sufficient historical data  
**Estimated Time**: 10-14 hours

Aggregate view of a Discord user's historical patterns across all sessions.

**Features**:
- **Session History**: Total sessions, frequency over time
- **Severity Patterns**: Average crisis score, trend direction
- **Common Themes**: Most frequent tags/categories (if tags implemented)
- **Response Patterns**: How user typically responds to outreach
- **Risk Indicators**: Escalation frequency, time between sessions

**Implementation**:
- New "User Profile" page accessible from Session Detail
- Aggregate queries across sessions and archives
- Visual timeline of user's history
- Summary card on Session Detail for quick context

**Benefit**: Better context for CRT when responding to "frequent fliers", identify patterns that might not be visible session-by-session.

---

### 11. Dashboard Widget Customization

**Priority**: 🟢 Low  
**Complexity**: 🟨 Medium  
**Depends On**: None  
**Estimated Time**: 6-8 hours

Allow users to personalize their dashboard layout.

**Features**:
- Drag-and-drop widget reordering
- Show/hide individual widgets
- Resize widgets (compact vs. expanded)
- Save layout preference per user
- "Reset to Default" option

**Implementation**:
- Store layout config in localStorage or user preferences table
- Use a grid library (e.g., `vue-grid-layout`)
- Default layout for new users

**Benefit**: Each CRT member can optimize their view for their workflow.

---

## ⏸️ Back Burner

Features we may want eventually, but are lower priority.

### Real-time Presence Indicators

**Priority**: ⚪ Someday  
**Complexity**: 🟨 Medium  
**Estimated Time**: 4-6 hours

Show when another CRT member is currently viewing the same session.

**Notes**:
- Prevents accidental duplicate responses
- Could use Redis pub/sub (already have Redis infrastructure)
- Display as avatar badges or "X is viewing" indicator
- Considered overkill for current team size, revisit as CRT grows

---

### Bulk Session Actions

**Priority**: ⚪ Someday  
**Complexity**: 🟨 Medium  
**Estimated Time**: 4-5 hours

Select multiple sessions from the list for batch operations.

**Notes**:
- Bulk close sessions, bulk assign to self, bulk tag (if tags implemented)
- Useful during shift handoff cleanup
- Team is currently small enough this isn't critical
- Revisit when session volume increases

---

### PWA / Offline Mode

**Priority**: ⚪ Someday  
**Complexity**: 🟧 High  
**Estimated Time**: 10-12 hours

Progressive Web App support for offline access.

**Notes**:
- View cached sessions when connectivity is spotty
- Queue actions for sync when back online
- Install as desktop/mobile app
- System is either working or needs attention - degraded states need discussion
- Offline actions could cause sync conflicts
- Needs further discussion to flesh out requirements

---

### @Mentions in Notes

**Priority**: ⚪ Someday  
**Complexity**: 🟨 Medium  
**Estimated Time**: 5-6 hours

Tag other CRT members in notes, creating a notification.

**Notes**:
- Would need notification system (Phase 7+)
- Could integrate with Discord notifications
- Useful for shift handoffs or escalations

---

### Personal Dashboard Stats

**Priority**: ⚪ Someday  
**Complexity**: 🟨 Medium  
**Estimated Time**: 5-6 hours

Individual performance metrics for CRT members.

**Notes**:
- Sessions handled this week/month, average response time, notes written, sessions closed
- Privacy considerations - who can see whose stats?
- Could be opt-in only
- Gamification concerns (don't want to incentivize rushing)

---

### Weekly Summary Reports

**Priority**: ⚪ Someday  
**Complexity**: 🟨 Medium  
**Estimated Time**: 6-8 hours

Auto-generated summary reports.

**Notes**:
- Total sessions by severity, CRT activity summary, notable trends, comparison to previous week
- Delivery: PDF export, email to admins, Discord channel post

---

### Export to CSV

**Priority**: ⚪ Someday  
**Complexity**: 🟦 Low  
**Estimated Time**: 3-4 hours

Export session data for external analysis.

**Notes**:
- Session list with metadata, notes export, audit log export, date range filtering
- Privacy review needed before implementation
- Consider what data is appropriate to export

---

## 💭 Considered But Deferred

Ideas discussed but not currently planned. May revisit based on team feedback.

| Idea | Reason for Deferral |
|------|---------------------|
| Keyboard Shortcuts | Nice-to-have, not essential for workflow |
| Desktop Notifications | Browser support varies, team prefers Discord |
| Internal CRT Chat | Team already uses Discord for communication |
| Note Attachments | Complexity vs. benefit; can link to external files |
| Mobile-Responsive Improvements | Primary use is desktop; tablet works adequately |
| Crisis Score Threshold Alerts | Already handled by Ash-Bot and Ash-NLP on Discord |
| Multi-language Support (i18n) | English-only community, not needed |

---

## 🗣️ Requests

Space for tracking community-requested features.

### Template for New Requests

```markdown
### CR-XXX: [Feature Name]
**Requested By**: [Discord username or "Multiple users"]
**Date**: YYYY-MM-DD
**Priority**: 🔴/🟡/🟢/⚪
**Complexity**: 🟦/🟨/🟧/🟥

**Description**: [What the community wants]

**Use Case**: [Why they want it]

**Notes**: [Implementation thoughts, concerns]
```

---

### CR-001: [Placeholder]

**Requested By**: -  
**Date**: -  
**Priority**: -  
**Complexity**: -

**Description**: *No community requests logged yet.*

---

## 🔬 Research

Ideas requiring research before planning.

### RE-001: Real-time Collaboration

**Status**: 🔬 Research Needed

**Question**: Should multiple CRT members be able to edit notes simultaneously?

**Approach**: Research operational transforms (OT) or CRDT libraries for Vue.js, evaluate complexity vs. benefit.

**Concerns**: Complexity, potential conflicts, current team size doesn't require this.

---

## 📝 How To Add Ideas

When adding new enhancement ideas:

1. **Discuss First**: Bring up in conversation before adding to document
2. **Categorize**: Place in appropriate section (Active, Back Burner, Deferred)
3. **Document**:
   - Brief description
   - Priority and complexity estimate
   - Dependencies (which phase must complete first)
   - Implementation notes
   - Benefit statement
4. **Update Date**: Update "Last Updated" at top of document

---

**Built with care for chosen family** 🏳️‍🌈
