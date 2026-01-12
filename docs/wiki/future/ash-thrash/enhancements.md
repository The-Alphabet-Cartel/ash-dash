---
title: "Ash-Thrash - Future Enhancements"
description: "Planned features and improvements for Ash-Thrash"
category: future
tags:
  - roadmap
  - planning
  - ash-thrash
author: "PapaBearDoes"
version: "5.0"
last_updated: "2026-01-11"
---
# Ash-Thrash: Future Enhancements

============================================================================
**Ash-Thrash**: Ash Ecosystem Testing Suite For The Alphabet Cartel Community
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

This document tracks potential enhancements and feature ideas for Ash-Thrash beyond the core v5.0 roadmap. Items are organized by priority and implementation complexity.

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

### 1. Multi-Consensus Algorithm Comparative Testing

**Priority**: 🟡 Medium  
**Complexity**: 🟨 Medium  
**Depends On**: Core NLP Testing Suite (Phase 1)  
**Estimated Time**: 6-8 hours

Test each phrase against all available Ash-NLP consensus algorithms to compare accuracy and identify algorithm-specific strengths/weaknesses.

**Features**:
- Test each phrase against all four consensus algorithms:
  - `weighted_voting` (current default)
  - `majority_voting`
  - `unanimous`
  - `conflict_aware`
- Generate comparative accuracy reports per algorithm
- Identify which algorithm performs best for each crisis category
- Track algorithm-specific false positive/negative rates
- Recommend optimal algorithm settings based on test results

**Implementation**:
- Add `consensus_algorithm` parameter to test runner
- Create parallel test execution mode (one run per algorithm)
- Develop comparative report generator
- Add algorithm performance metrics to baseline tracking

**Benefit**: Enables data-driven optimization of Ash-NLP's consensus configuration. May reveal that different algorithms perform better for different crisis severity levels, informing potential adaptive consensus strategies.

---

### 2. Discord Message Simulation (Ash-Bot Integration Testing)

**Priority**: 🟡 Medium  
**Complexity**: 🟧 High  
**Depends On**: Core NLP Testing Suite (Phase 1), Ash-Bot architecture understanding  
**Estimated Time**: 12-16 hours

Simulate Discord messages through Ash-Bot's internal message processing pipeline to test end-to-end crisis detection flow without requiring actual Discord API interaction.

**Features**:
- Bypass Discord API while using Ash-Bot's actual message handler code paths
- Test message → Ash-NLP → alert generation flow
- Validate Crisis Response Team notification triggers
- Test user history tracking and escalation pattern detection
- Verify embed formatting and alert content accuracy

**Implementation**:
- Study Ash-Bot's message handler architecture
- Create mock Discord message objects that satisfy Ash-Bot's expectations
- Develop test harness that injects messages into Ash-Bot's processing pipeline
- Capture and validate alert payloads before Discord delivery
- Add latency measurement for full pipeline timing

**Benefit**: Enables comprehensive end-to-end testing of the entire crisis detection pipeline without needing Discord test channels or risking false alerts to Crisis Response Team during testing.

**Notes**:
- Requires deep understanding of Ash-Bot's internal architecture
- May need coordination with Ash-Bot development to ensure testability
- Consider adding test hooks to Ash-Bot specifically for this purpose

---

### 3. Ash-Dash API Integration Testing

**Priority**: 🟢 Low  
**Complexity**: 🟨 Medium  
**Depends On**: Discord Message Simulation, Ash-Dash API stability  
**Estimated Time**: 8-10 hours

Validate that crisis alerts properly flow through to Ash-Dash and appear correctly in the dashboard interface.

**Features**:
- Test alert ingestion via Ash-Dash API
- Validate session creation and tracking
- Verify CRT (Crisis Response Team) notification workflows
- Test historical data queries and reporting endpoints
- Validate user history aggregation

**Implementation**:
- Create Ash-Dash API client manager for Ash-Thrash
- Develop test scenarios for dashboard data flow
- Add dashboard state validation after test alerts
- Implement cleanup routines for test data

**Benefit**: Ensures the full ecosystem works together, from message detection through dashboard visibility for Crisis Response Teams.

---

## ⏸️ Back Burner

Features we may want eventually, but are lower priority.

### 1. Automated Regression Detection

Automatically compare test results against historical baselines and flag regressions via Discord webhook.

**Notes**:
- Requires baseline storage infrastructure
- Would benefit from CI/CD integration
- Could alert on >2% accuracy drops

### 2. Performance Profiling Suite

Detailed performance analysis beyond basic latency tracking.

**Notes**:
- GPU memory utilization during inference
- Model-specific latency breakdown
- Throughput degradation curves under load
- Memory leak detection for long-running tests

### 3. Test Data Generation Tools

AI-assisted generation of new test phrases to expand coverage.

**Notes**:
- Use Claude API to generate variations of existing phrases
- Human review required before adding to test suite
- Could help identify coverage gaps

---

## 💭 Considered But Deferred

Ideas discussed but not currently planned. May revisit based on team feedback.

| Idea | Reason for Deferral |
|------|---------------------|
| Mock Ash-NLP Server | Violates Clean Architecture Rule #8 (real-world testing) |
| Browser-based Test UI | Complexity not justified for manual runs |
| Multi-language Testing | English-only community focus for now |
| Real Discord Channel Testing | Risk of false CRT alerts, complex setup |
| Automated Daily Test Runs | Manual execution preferred initially |

---

## 🗣️ Requests

Space for tracking community-requested features.

*No community requests yet.*

---

## 🔬 Research

Ideas requiring research before planning.

### R-001: Optimal Test Phrase Count Per Category

**Status**: 🔬 Research Needed

**Question**: What is the minimum number of test phrases per category needed to achieve statistically significant accuracy measurements?

**Approach**: 
- Research ML testing best practices
- Analyze variance in current test results
- Determine confidence interval requirements

**Concerns**: 
- Too few phrases may miss edge cases
- Too many phrases increases test runtime significantly

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
