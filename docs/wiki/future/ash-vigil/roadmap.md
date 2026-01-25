---
title: "Ash-Vigil - Development Roadmap (Wiki Mirror)"
description: "Development roadmap for the Ash-Vigil mental health risk detection service"
category: roadmap
tags:
  - ash-vigil
  - roadmap
  - planning
  - wiki-mirror
author: "PapaBearDoes"
version: "5.0"
last_updated: "2026-01-25"
---
# Ash-Vigil: Development Roadmap

============================================================================
**Ash**: Crisis Detection Ecosystem for The Alphabet Cartel
**The Alphabet Cartel** - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================

**Document Version**: v5.0.3
**Created**: 2026-01-24
**Status**: 📋 Planning
**Repository**: https://github.com/the-alphabet-cartel/ash-vigil
**Source Document**: `ash-vigil/docs/v5.0/roadmap.md`

> **Note**: This is a wiki mirror. The authoritative document is located at `ash-vigil/docs/v5.0/roadmap.md`.

---

## 🎯 Mission Statement

```
ASH-VIGIL MISSION:
    Watch    → Scan messages for subtle crisis signals that generic models miss
    Amplify  → Boost ensemble confidence when specialized risk patterns emerge
    Catch    → Detect planning signals, passive ideation, and minority stress indicators
    Protect  → Safeguard our LGBTQIA+ community through vigilant pattern detection
```

Ash-Vigil serves as the vigilant guardian that catches what others miss - the subtle signals of crisis that generic NLP models overlook.

---

## 📦 Component Overview

### What is Ash-Vigil?

Ash-Vigil is a specialized mental health risk detection service that provides a 5th model for the Ash-NLP ensemble. It runs on dedicated GPU hardware (Bacchus) and communicates with Ash-NLP via HTTP.

### Role in Ecosystem

| Capability | Description |
|------------|-------------|
| **Watch** | Identify suicide/crisis risk patterns in text |
| **Amplify** | Boost ensemble scores when risk is detected |
| **Flag** | Mark messages for CRT review when risk is high |
| **Fallback** | Graceful degradation when unavailable |

### Key Specifications

| Spec | Value |
|------|-------|
| **Host** | Bacchus (10.20.30.14) |
| **Port** | 30882 |
| **GPU** | NVIDIA RTX 5060 (8GB VRAM) |
| **Container** | Docker Desktop (WSL2) |
| **Model** | ourafla/mental-health-bert-finetuned (default) |
| **License** | Apache 2.0 (ecosystem standard) |

---

## 🖥️ Infrastructure

### Network Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Lofn (10.20.30.253)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   Ash-NLP (:30880)                    │  │
│  │  ┌──────┐ ┌─────────┐ ┌────────┐ ┌─────┐             │  │
│  │  │ BART │ │Sentiment│ │Emotions│ │Irony│             │  │
│  │  └──────┘ └─────────┘ └────────┘ └─────┘             │  │
│  │                    │                                  │  │
│  │           ┌────────▼────────┐                        │  │
│  │           │ Decision Engine │◄───── HTTP ────┐       │  │
│  │           └─────────────────┘                │       │  │
│  └──────────────────────────────────────────────│───────┘  │
└─────────────────────────────────────────────────│──────────┘
                                                  │
                                    Local Network (~2-10ms)
                                                  │
┌─────────────────────────────────────────────────│──────────┐
│                    Bacchus (10.20.30.14)        ▼          │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                  Ash-Vigil (:30882)                   │ │
│  │         Mental Health Risk Detection API              │ │
│  │                                                       │ │
│  │  Model: ourafla/mental-health-bert-finetuned         │ │
│  │  GPU: RTX 5060 (8GB VRAM)                            │ │
│  └───────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

---

## 📊 Phase Summary

| Phase | Name | Status | Estimated | Dependencies |
|-------|------|--------|-----------|--------------|
| 1 | Service Completion | 📋 Planning | 8-10 hours | Skeleton exists |
| 2 | Ash-Thrash Evaluation Infrastructure | 📋 Planning | 10-12 hours | Phase 1 |
| 3 | Ash-NLP Integration | 📋 Planning | 10-14 hours | Phase 1 |
| 4 | Full System Testing & Tuning | 📋 Planning | 8-10 hours | Phases 2 & 3 |
| 5 | Ecosystem Integration & Production | 📋 Planning | 6-8 hours | Phase 4 |

**Total Estimated**: 42-54 hours

---

## 📋 Phase 1: Service Completion

Complete the Ash-Vigil skeleton and make it production-ready on Bacchus.

**Key Deliverables**:
- Operational Ash-Vigil on Bacchus (port 30882)
- `/analyze`, `/health`, `/metrics`, `/evaluate` endpoints
- GHCR image publishing
- Real inference working on RTX 5060

---

## 📋 Phase 2: Ash-Thrash Evaluation Infrastructure

Build the model evaluation framework in Ash-Thrash that targets Ash-Vigil's `/evaluate` endpoint.

**Key Deliverables**:
- `ash-thrash/src/evaluators/` module
- Ability to evaluate any model via Ash-Vigil endpoint
- Baseline metrics for selected model
- Framework for future model comparisons

---

## 📋 Phase 3: Ash-NLP Integration

Integrate Ash-Vigil as a soft amplifier in the Ash-NLP Decision Engine.

**Key Deliverables**:
- Ash-NLP calling Ash-Vigil for every analysis
- Configurable amplification thresholds
- Response includes `vigil_status` field
- Circuit breaker preventing cascade failures

---

## 📋 Phase 4: Full System Testing & Tuning

Comprehensive Ash-Thrash testing of the integrated system and threshold tuning.

**Success Criteria**:
- Overall false negative rate <30% (from 63%)
- LGBTQIA+ accuracy >70% (from 20%)
- Gaming false positives <10% (from 60%)
- Total latency increase <200ms

---

## 📋 Phase 5: Ecosystem Integration & Production

Integrate with Ash Core monitoring and finalize documentation.

**Key Deliverables**:
- Ash-Vigil in Ash Core health monitoring
- All documentation complete
- Wiki mirror synchronized

---

## ✅ Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| False Negative Rate | <30% | Ash-Thrash full suite |
| LGBTQIA+ Detection | >70% | specialty_lgbtqia category |
| Planning Signal Detection | >75% | planning_signals phrases |
| Gaming False Positives | <10% | specialty_gaming category |
| Latency Impact | <200ms | End-to-end benchmark |
| Availability | >99% | Uptime with fallback |

---

## 📝 Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-01-25 | v5.0.3 | Reordered Phase 1 steps for sequential workflow (Fresh Pass now 1.2) | PapaBearDoes + Claude |
| 2026-01-25 | v5.0.2 | Restructured phases based on design decisions; Port confirmed as 30882; GPU confirmed as RTX 5060 | PapaBearDoes + Claude |
| 2026-01-24 | v5.0.1 | Initial roadmap created | PapaBearDoes + Claude |

---

**Built with care for chosen family** 🏳️‍🌈
