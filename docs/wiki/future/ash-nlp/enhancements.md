---
title: "Ash-NLP - Future Enhancements"
description: "Planned features and improvements for Ash-NLP"
category: future
tags:
  - roadmap
  - planning
  - ash-nlp
author: "PapaBearDoes"
version: "5.0"
last_updated: "2026-01-11"
---
# Ash-NLP: Future Enhancements & Improvements

============================================================================
**Ash-NLP**: Natural Language Processing Backend Server for Crisis Detection
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

This document tracks potential enhancements and feature ideas for Ash-NLP beyond the core v5.0 roadmap. Items are organized by priority and implementation complexity.

Ash-NLP v5.0 is production-ready with a multi-model ensemble architecture combining BART Zero-Shot Classification, Cardiff Sentiment Analysis, Cardiff Irony Detection, and RoBERTa Emotions Classification. These enhancements represent the next evolution of our crisis detection capabilities.

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

### 1. Conversation Context Window

**Priority**: 🔴 High  
**Complexity**: 🟧 High  
**Depends On**: Ash-NLP v5.0 Core Complete
**Estimated Time**: 12-16 hours

Extend our current single-message analysis to support analyzing a sequence of messages from the same user over a configurable time window (e.g., last 5-10 messages over 30 minutes). This builds upon our existing context-aware analysis and escalation pattern detection.

**Features**:
- Configurable message count window (default: 10 messages)
- Configurable time window (default: 30 minutes)
- Gradual mood deterioration detection across messages
- Escalating distress pattern recognition over time
- Improved context for sarcasm/irony disambiguation
- Maintains stateless architecture (Ash-Bot provides message history per request)

**Implementation**:
- New API endpoint: `POST /api/v1/analyze/conversation`
- Accept array of timestamped messages with user identifier
- Apply individual message analysis to each message
- Aggregate results with temporal weighting (recent messages weighted higher)
- Calculate conversation-level risk trajectory (improving, stable, declining)
- Return both individual and aggregate analysis results

**Benefit**: Catches gradual crisis escalation that single-message analysis might miss. A user saying "I'm fine" after several increasingly distressed messages should still trigger concern.

---

### 2. Crisis Team Feedback Loop

**Priority**: 🔴 High  
**Complexity**: 🟥 Very High  
**Depends On**: Ash-Dash Admin Interface, Ash-NLP v5.0 Core Complete
**Estimated Time**: 20-30 hours

Allow the Crisis Response Team (CRT) to mark analysis results as false positives or false negatives through Ash-Dash. This feedback creates a continuous improvement cycle for the NLP system.

**Features**:
- Feedback submission API endpoint
- Structured feedback categories (false positive, false negative, severity adjustment)
- Feedback storage with message context (anonymized)
- Automated reporting on model accuracy trends
- Pattern identification for systematic model weaknesses
- Curated dataset generation for future fine-tuning

**Implementation**:
- New API endpoint: `POST /api/v1/feedback`
- Feedback storage in dedicated JSON files or lightweight database
- Aggregation service for generating accuracy reports
- Export functionality for fine-tuning datasets

**Learning Approach - Hybrid Model**:

We will implement a two-tier learning system that balances immediate improvements with long-term model enhancement while respecting server resource constraints.

#### Tier 1: Live Weight & Threshold Optimization

**Resource Impact**: Minimal - configuration updates only

- Automatically adjust ensemble model weights based on feedback patterns
- If a specific model consistently generates false positives for certain message types, reduce its weight in the weighted decision engine
- Tune confidence thresholds per severity level based on real-world outcomes
- Changes applied via configuration updates without model retraining
- Can be automated with scheduled analysis jobs (weekly/monthly)

*Example*: If Cardiff Sentiment produces false positives on messages containing dark humor 40% of the time, its weight could be reduced from 25% to 20% for messages flagged with high irony scores.

#### Tier 2: Offline Periodic Fine-Tuning

**Resource Impact**: Heavy during training (hours), zero impact during normal operation

- Collect anonymized feedback data over extended periods (quarterly)
- When sufficient samples accumulated (500+ per category), flag for fine-tuning consideration
- Perform fine-tuning jobs on Bacchus (Windows AI server) to keep Lofn's GPU available for production
- Test fine-tuned models extensively via Ash-Thrash before deployment
- Deploy new model weights to production after validation

*Training Infrastructure*:
- Primary: Bacchus (Ryzen 7 7700x, 64GB RAM, RTX 3050)
- Backup: Lofn during maintenance windows (Ryzen 7 5800x, 64GB RAM, RTX 3060 12GB)

#### Implementation Phases

1. **Phase 1**: Feedback collection and storage infrastructure
2. **Phase 2**: Reporting and pattern identification
3. **Phase 3**: Automated weight/threshold optimization (Tier 1)
4. **Phase 4**: Fine-tuning pipeline and validation framework (Tier 2)

**Benefit**: Creates a virtuous cycle where real-world usage continuously improves detection accuracy. The hybrid approach provides quick wins through weight optimization while building toward deeper model improvements over time.

---

### 3. Confidence Threshold Auto-Tuning

**Priority**: 🟡 Medium  
**Complexity**: 🟨 Medium  
**Depends On**: Crisis Team Feedback Loop (Phase 1)
**Estimated Time**: 6-8 hours

Implement an automated system that analyzes historical performance data and suggests or applies optimal confidence thresholds for each model and severity level.

**Features**:
- Analysis of feedback data to identify optimal thresholds
- Per-model threshold recommendations
- Per-severity-level threshold tuning
- Simulation mode to preview threshold changes before applying
- Rollback capability if new thresholds underperform

**Implementation**:
- New service: `ThresholdOptimizer` in ensemble coordination layer
- Analysis endpoint: `GET /api/v1/admin/threshold-analysis`
- Apply endpoint: `POST /api/v1/admin/threshold-apply`
- Configuration versioning for rollback support
- Integration with feedback loop data store

**Benefit**: Removes guesswork from threshold configuration. As our community evolves and communication patterns change, thresholds automatically adapt.

---

### 4. Custom Vocabulary Expansion

**Priority**: 🟡 Medium  
**Complexity**: 🟨 Medium  
**Depends On**: Ash-NLP v5.0 Core Complete
**Estimated Time**: 6-10 hours

Allow adding community-specific terms, slang, phrases, and code words to improve detection accuracy. Our LGBTQIA+ community has unique language patterns that generic models may not recognize.

**Features**:
- Admin-managed vocabulary lists via API
- Term categories: crisis indicators, safe indicators, contextual modifiers
- Weight assignment per term (how strongly it influences scoring)
- Pre-processing layer that identifies custom terms before model analysis
- Support for phrases, not just single words
- Version-controlled vocabulary with rollback

**Implementation**:
- New configuration: `config/vocabulary/custom_terms.json`
- Vocabulary manager in managers layer
- Pre-processor integration in analysis pipeline
- API endpoints for CRUD operations on vocabulary
- Ash-Dash integration for CRT vocabulary management

**Example Vocabulary Structure**:
```json
{
  "crisis_indicators": [
    {"term": "rainbow bridge", "weight": 0.8, "context": "pet loss, may indicate grief"},
    {"term": "chosen family", "weight": 0.2, "context": "positive community term"}
  ],
  "safe_modifiers": [
    {"term": "hyperbole warning", "weight": -0.3, "context": "user signaling exaggeration"}
  ]
}
```

**Benefit**: Improves accuracy for community-specific language that generic NLP models weren't trained on. Empowers the CRT to continuously refine detection based on observed patterns.

---

## ⏸️ Back Burner

Features we may want eventually, but are lower priority.

### 1. Multi-Language Detection & Routing

Detect non-English messages and handle them appropriately. Currently, [The Alphabet Cartel](https://discord.gg/alphabetcartel) is an English-only community, making this a long-term consideration.

**Notes**:
- Implement language detection as first step in analysis pipeline
- Return reduced confidence scores for non-English messages
- Flag for human review when language detected as non-English
- Future: Route to language-appropriate models if community expands
- Consider: Community translation volunteers for crisis situations

---

### 2. Model Performance Dashboard (Ash-Dash Integration)

Expose NLP performance metrics through Ash-Dash for Admins and CRT Leads rather than external tools like Prometheus/Grafana.

**Notes**:
- New API endpoints for metrics retrieval
- Per-model inference latency tracking
- Confidence score distributions over time
- Alert rate trends (hourly, daily, weekly)
- Model agreement/disagreement rates
- Integration with Ash-Dash admin views
- Historical performance comparison

---

## 💭 Considered But Deferred

Ideas discussed but not currently planned. May revisit based on team feedback.

| Idea | Reason for Deferral |
|------|---------------------|
| Real-time streaming analysis | Current batch approach works well; streaming adds complexity without proportional benefit |
| Sentiment trending per-channel | Better suited for Ash-Dash analytics layer; NLP should focus on message analysis |
| User risk profiles | Privacy concerns require careful ethical consideration; needs community input before proceeding |
| Voice message analysis | Significant privacy concerns; community would likely view as autonomy violation; hard no |
| Batch historical analysis | Planned for Ash-Bot specifically; keeping NLP focused on single responsibility |

---

## 🗣️ Requests

Space for tracking community-requested features.

*No community requests logged yet.*

### Template: CR-XXX: Feature Name
**Requested By**: Discord username or "Multiple Users"
**Date**: YYYY-MM-DD
**Priority**: 🔴/🟡/🟢/⚪
**Complexity**: 🟦/🟨/🟧/🟥

**Description**: Brief description of the requested feature.

**Use Case**: How would this feature be used?

**Notes**: Additional context or considerations.

---

## 🔬 Research

Ideas requiring research before planning.

### R-001: Smaller Distilled Models

**Status**: 🔬 Research Needed

**Question**: Can we use quantized or distilled versions of our current models to reduce inference latency while maintaining acceptable accuracy?

**Approach**:
- Benchmark current model inference times under load
- Identify quantization options for each model (INT8, FP16)
- Test distilled alternatives from HuggingFace
- Compare accuracy vs. latency tradeoffs
- Determine minimum acceptable accuracy threshold

**Concerns**:
- Accuracy degradation may be unacceptable for crisis detection
- Different models may respond differently to quantization
- Need comprehensive testing via Ash-Thrash before any deployment

---

### R-002: Community-Specific Fine-Tuning

**Status**: 🔬 Research Needed

**Question**: Would fine-tuning our base models on LGBTQIA+-specific language patterns and crisis indicators meaningfully improve detection accuracy?

**Approach**:
- Accumulate anonymized training data from feedback loop (requires 500+ samples minimum)
- Research fine-tuning approaches for each model architecture
- Evaluate training infrastructure requirements (Bacchus vs. cloud)
- Establish validation methodology with Ash-Thrash
- Consider ethical implications of community-specific training data

**Concerns**:
- Data privacy and anonymization requirements
- Risk of overfitting to specific community patterns
- Maintenance burden of custom-tuned models
- Need sufficient diverse training samples before attempting

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

### Section Guidelines

- **Active Enhancements**: Features we intend to build in the near term
- **Back Burner**: Good ideas that aren't prioritized yet
- **Considered But Deferred**: Ideas we've discussed and consciously decided not to pursue (with reasons)
- **Requests**: Community-requested features awaiting evaluation
- **Research**: Ideas that need investigation before we can plan them

---

**Built with care for chosen family** 🏳️‍🌈
