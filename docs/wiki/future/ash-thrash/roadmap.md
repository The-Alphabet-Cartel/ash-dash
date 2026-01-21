---
title: "Ash-Thrash - v5.0 Development Roadmap"
description: "Roadmap for the v5.0 development of Ash-Thrash, the Crisis Detection Testing Suite"
category: roadmap
tags:
  - roadmap
  - planning
  - ash-thrash
author: "PapaBearDoes"
version: "5.0"
last_updated: "2026-01-12"
---
# Ash-Thrash: v5.0 Development Roadmap

============================================================================
**Ash-Thrash**: Crisis Detection Testing Suite
**The Alphabet Cartel** - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================

**Document Version**: v5.0.1
**Created**: 2026-01-11
**Last Updated**: 2026-01-12
**Status**: 📋 Planning (Ready to Begin)
**Repository**: https://github.com/the-alphabet-cartel/ash-thrash

---

## Table of Contents

1. [Mission Statement](#-mission-statement)
2. [Executive Summary](#-executive-summary)
3. [Architecture Overview](#-architecture-overview)
4. [Technology Stack](#-technology-stack)
5. [Phase Overview](#-phase-overview)
6. [Detailed Phase Breakdown](#-detailed-phase-breakdown)
7. [Test Scenario Distribution](#-test-scenario-distribution)
8. [Security Considerations](#-security-considerations)
9. [Infrastructure & Deployment](#-infrastructure--deployment)
10. [Progress Summary](#-progress-summary)
11. [Success Criteria](#-success-criteria)
12. [Future Enhancements](#-future-enhancements)
13. [Change Log](#-change-log)

---

## 🎯 Mission Statement

```
MISSION - NEVER TO BE VIOLATED:
    Validate   → Verify crisis detection accuracy through live Ash-NLP integration testing
    Challenge  → Stress test the system with edge cases and adversarial scenarios
    Guard      → Prevent regressions that could compromise detection reliability
    Protect    → Safeguard our LGBTQIA+ community through rigorous quality assurance
```

---

## 📋 Executive Summary

Ash-Thrash is the comprehensive testing suite for the Ash Crisis Detection Ecosystem. It validates the accuracy and reliability of Ash-NLP's crisis classification through extensive test scenarios, regression detection, and performance benchmarking.

### Key Capabilities

- **525+ Test Scenarios**: Comprehensive coverage across all crisis severity levels
- **Real API Testing**: Live integration with Ash-NLP (no mocks per Rule #8)
- **Flexible Tolerance System**: Accounts for human communication variability
- **Regression Detection**: Baseline comparison to catch accuracy degradation
- **Performance Benchmarking**: Latency and throughput validation
- **Detailed Reporting**: JSON, HTML, and Discord webhook notifications

### Project Goals

| Goal | Description | Success Criteria |
|------|-------------|------------------|
| **Accuracy Validation** | Verify crisis classification correctness | ≥95% accuracy on high/critical, ≥85% on medium/low |
| **False Positive Prevention** | Ensure non-crisis content doesn't trigger alerts | ≥95% accuracy on "none" priority messages |
| **Performance Validation** | Confirm acceptable response times | p95 latency < 500ms |
| **Regression Detection** | Catch degradations before production | Baseline comparison with deviation alerts |

### Current Status

Ash-Thrash v5.0 is in **planning stage** with roadmap complete. Ready to begin Phase 1 development.

---

## 🏗️ Architecture Overview

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        Ash-Thrash Architecture                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│    ┌─────────────────────────────────────────────────────────────────┐     │
│    │                    Ash-Thrash Container                         │     │
│    │                                                                 │     │
│    │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐   │     │
│    │  │ PhraseLoader     │  │ TestRunner       │  │ Report       │   │     │
│    │  │ Manager          │  │ Manager          │  │ Manager      │   │     │
│    │  │                  │  │                  │  │              │   │     │
│    │  │ • Load JSON      │  │ • Orchestrate    │  │ • JSON       │   │     │
│    │  │ • Validate       │  │ • Track progress │  │ • HTML       │   │     │
│    │  │ • Categorize     │  │ • Collect results│  │ • Discord    │   │     │
│    │  └──────────────────┘  └──────────────────┘  └──────────────┘   │     │
│    │           │                    │                    │           │     │
│    │           ▼                   ▼                    ▼           │     │
│    │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐   │     │
│    │  │ NLPClient        │  │ ResultAnalyzer   │  │ Baseline     │   │     │
│    │  │ Manager          │  │ Manager          │  │ Tracker      │   │     │
│    │  │                  │  │                  │  │              │   │     │
│    │  │ • HTTP client    │  │ • Calculate      │  │ • Store      │   │     │
│    │  │ • Retry logic    │  │   accuracy       │  │ • Compare    │   │     │
│    │  │ • Timeout        │  │ • Categorize     │  │ • Alert      │   │     │
│    │  └──────────────────┘  └──────────────────┘  └──────────────┘   │     │
│    │           │                                                     │     │
│    └───────────┼─────────────────────────────────────────────────────┘     │
│                │                                                           │
│                ▼                                                           │
│    ┌───────────────────────┐                                               │
│    │       Ash-NLP         │                                               │
│    │    (Port 30880)       │                                               │
│    │                       │                                               │
│    │  Live API Testing     │                                               │
│    │  (No Mocks - Rule #8) │                                               │
│    └───────────────────────┘                                               │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Runtime** | Python 3.11 | Primary language |
| **Testing** | pytest | Test framework |
| **HTTP Client** | httpx | Async HTTP for Ash-NLP API |
| **Validation** | Pydantic v2.x | Data validation |
| **Terminal Output** | Rich | Colorized progress display |
| **Configuration** | JSON + Environment | Clean Architecture compliant |
| **Containerization** | Docker | Deployment |

### Target Server

| Specification | Value |
|---------------|-------|
| **OS** | Debian 12 |
| **CPU** | AMD Ryzen 7 5800x |
| **GPU** | NVIDIA RTX 3060 (12GB VRAM) |
| **RAM** | 64GB |
| **Server** | Lofn (10.20.30.253) |

---

## 📅 Phase Overview

| Phase | Name | Focus | Status |
|-------|------|-------|--------|
| 1 | Foundation | Core infrastructure, managers, logging | 🔲 Not Started |
| 2 | Test Execution Engine | Runner, validators, result collection | 🔲 Not Started |
| 3 | Analysis & Reporting | Metrics, reports, baseline tracking | 🔲 Not Started |
| 4 | Test Data Population | 525+ test scenarios across categories | 🔲 Not Started |
| 5 | Performance & Stress Testing | Load testing, latency analysis | 🔲 Not Started |

### Phase Dependencies

```
Phase 1 (Foundation)
    ↓
Phase 2 (Test Execution)
    ↓
Phase 3 (Analysis & Reporting)
    ↓
Phase 4 (Test Data) ←── Can start parallel with Phase 2
    ↓
Phase 5 (Performance)
```

### Estimated Effort

| Phase | Estimated Hours |
|-------|-----------------|
| Phase 1 | 8-12 hours |
| Phase 2 | 6-8 hours |
| Phase 3 | 6-8 hours |
| Phase 4 | 8-12 hours |
| Phase 5 | 4-6 hours |
| **Total** | **32-46 hours** |

---

## 📋 Detailed Phase Breakdown

### Phase 1: Foundation 🔲 Not Started
**Goal**: Establish core infrastructure and managers

- [ ] Project directory structure (Clean Architecture compliant)
- [ ] Docker setup (Dockerfile, docker-compose.yml)
- [ ] ConfigManager rewrite with full validation
- [ ] LoggingConfigManager with colorized output
- [ ] SecretsManager rewrite for Docker secrets
- [ ] NLPClientManager with HTTP client, retry logic, timeout handling
- [ ] PhraseLoaderManager with JSON schema validation
- [ ] Health check endpoint

**Estimated**: 8-12 hours

---

### Phase 2: Test Execution Engine 🔲 Not Started
**Goal**: Build test orchestration and validation

- [ ] TestRunnerManager for orchestration
- [ ] ClassificationValidator (expected vs actual comparison)
- [ ] ResponseValidator (API response structure)
- [ ] In-memory result collection
- [ ] Progress tracking with Rich terminal output
- [ ] Tolerance system for edge cases

**Estimated**: 6-8 hours

---

### Phase 3: Analysis & Reporting 🔲 Not Started
**Goal**: Implement metrics calculation and reporting

- [ ] ResultAnalyzerManager for metrics calculation
- [ ] Accuracy by category, subcategory, and overall
- [ ] False positive/negative rate tracking
- [ ] ReportManager for JSON output
- [ ] ReportManager for HTML output
- [ ] Discord webhook notifications
- [ ] Baseline storage and comparison logic
- [ ] Regression alerting

**Estimated**: 6-8 hours

---

### Phase 4: Test Data Population 🔲 Not Started
**Goal**: Create comprehensive test scenario library

- [ ] Migrate existing ~200 phrases from old structure
- [ ] High/Critical priority scenarios (125 total)
- [ ] Medium priority scenarios (100 total)
- [ ] Low priority scenarios (100 total)
- [ ] None priority scenarios (100 total)
- [ ] Edge case scenarios (75 total)
- [ ] Specialty scenarios (100 total)
- [ ] Validate phrase distribution and coverage

**Estimated**: 8-12 hours

---

### Phase 5: Performance & Stress Testing 🔲 Not Started
**Goal**: Validate system performance under load

- [ ] Concurrent request testing
- [ ] Latency tracking (p50, p95, p99)
- [ ] Load curve generation
- [ ] Server stability validation
- [ ] Resource utilization monitoring
- [ ] Performance baseline establishment

**Estimated**: 4-6 hours

---

## 📊 Test Scenario Distribution

### Target: 525+ Test Scenarios

#### Definite Classifications (Clear-cut cases)

| Category | Count | Target Accuracy | Description |
|----------|-------|-----------------|-------------|
| **Critical/High Priority** | 125 | 95%+ | Method-specific suicide, immediate intent, active planning |
| **Medium Priority** | 100 | 85%+ | Severe distress, ideation without plan, emotional crisis |
| **Low Priority** | 100 | 85%+ | Mild distress, daily struggles, manageable concerns |
| **None Priority** | 100 | 95%+ | Positive content, neutral statements, false positive prevention |

#### Edge Cases (Ambiguous scenarios)

| Category | Count | Description |
|----------|-------|-------------|
| **Maybe High↔Medium** | 25 | Ambiguous severity - could reasonably be either |
| **Maybe Medium↔Low** | 25 | Moderate distress with unclear severity |
| **Maybe Low↔None** | 25 | Borderline content that might be normal venting |

#### Specialty Test Categories

| Category | Count | Description |
|----------|-------|-------------|
| **Irony/Sarcasm** | 25 | Dark humor, sarcasm that might trigger false positives |
| **Gaming Context** | 15 | "I died again", "kill me now" in gaming context |
| **Song Lyrics/Quotes** | 15 | Quoted content that sounds concerning out of context |
| **LGBTQIA+ Specific** | 20 | Identity-related distress, coming out struggles, discrimination |
| **Cultural/Slang** | 15 | Internet slang, cultural expressions |
| **Multi-language Hints** | 10 | Code-switching, expressions from other languages |

### Subcategory Examples

**High Priority Subcategories**:
- `method_specific` - Explicit suicide methods mentioned
- `suicidal_planning` - Active planning statements
- `suicidal_intent_immediate` - Immediate intent expressions
- `death_ideation` - Death-focused thoughts
- `burden_thoughts` - Feeling like a burden to others
- `self_harm_intent` - Self-harm with intent

**Medium Priority Subcategories**:
- `depression_severe` - Acknowledged severe depression
- `emotional_overwhelm` - Feeling overwhelmed
- `hopelessness` - Pervasive hopelessness
- `self_harm_thoughts` - Ideation without immediate intent
- `dissociation` - Dissociative episodes

---

## 🔐 Security Considerations

1. **Test Data Sensitivity**: Test phrases contain simulated crisis content - handle appropriately
2. **API Access**: NLP client credentials via Docker secrets
3. **Network Isolation**: Only communicates with Ash-NLP on internal network
4. **Report Storage**: Results stored locally, not transmitted externally
5. **Discord Webhooks**: Webhook URL stored as secret

---

## 🖥️ Infrastructure & Deployment

### Deployment Configuration

| Setting | Value |
|---------|-------|
| **Host** | Lofn (10.20.30.253) |
| **Container** | ash-thrash |
| **Port** | 30888 (API/Health) |
| **Health Check** | HTTP /health |

### Dependencies

| Service | Host | Port | Required |
|---------|------|------|----------|
| Ash-NLP | Lofn | 30880 | ✅ Yes |
| Discord Webhook | External | 443 | 🟡 Optional |

### File Structure

```
ash-thrash/
├── src/
│   ├── config/
│   │   ├── default.json
│   │   ├── testing.json
│   │   └── phrases/
│   │       ├── high_priority.json
│   │       ├── medium_priority.json
│   │       ├── low_priority.json
│   │       ├── none_priority.json
│   │       ├── edge_cases/
│   │       |   ├── maybe_high_medium.json
│   │       |   ├── maybe_low_none.json
│   │       |   └── maybe_medium_low.json
│   │       └── specialty/
│   │           ├── cultural_slang.json
│   │           ├── gaming_context.json
│   │           ├── irony_sarcasm.json
│   │           ├── language_hints.json
│   │           ├── lgbtqia_specific.json
│   │           └── songs_quotes.json
│   ├── managers/
│   │   ├── config_manager.py
│   │   ├── secrets_manager.py
│   │   ├── logging_config_manager.py
│   │   ├── nlp_client_manager.py
│   │   ├── phrase_loader_manager.py
│   │   ├── test_runner_manager.py
│   │   ├── result_analyzer_manager.py
│   │   └── report_manager.py
│   └── validators/
│       ├── classification_validator.py
│       └── response_validator.py
├── tests/
├── reports/
├── logs/
├── docs/
├── main.py
├── Dockerfile
└── docker-compose.yml
```

---

## 📊 Progress Summary

### Completed Phases: 0 of 5

| Phase | Status | Date | Key Deliverables |
|-------|--------|------|------------------|
| Phase 1 | 🔲 Not Started | - | Foundation, managers |
| Phase 2 | 🔲 Not Started | - | Test execution engine |
| Phase 3 | 🔲 Not Started | - | Analysis & reporting |
| Phase 4 | 🔲 Not Started | - | 525+ test scenarios |
| Phase 5 | 🔲 Not Started | - | Performance testing |

**Overall Progress**: 0% (Planning Complete)

---

## ✅ Success Criteria

The project is complete when:

1. [ ] 525+ test scenarios created and validated
2. [ ] High/Critical accuracy ≥ 95%
3. [ ] Medium/Low accuracy ≥ 85%
4. [ ] None (false positive prevention) accuracy ≥ 95%
5. [ ] p95 latency < 500ms
6. [ ] Baseline comparison operational
7. [ ] Regression alerting functional
8. [ ] JSON and HTML reports generated
9. [ ] Discord webhook notifications working
10. [ ] All code follows Clean Architecture Charter
11. [ ] Documentation complete
12. [ ] Docker deployment operational

---

## 🔜 Future Enhancements

See [enhancements.md](enhancements.md) for detailed planning.

### Post-v5.0 Backlog

| Enhancement | Priority | Description |
|-------------|----------|-------------|
| Multi-Consensus Testing | 🟡 Medium | Test each phrase against all consensus algorithms |
| Discord Message Simulation | 🟡 Medium | End-to-end Ash-Bot integration testing |
| Ash-Dash API Integration | 🟢 Low | Dashboard data flow validation |
| Automated CI/CD Integration | 🟡 Medium | Run tests on every commit |
| Historical Trend Analysis | 🟢 Low | Track accuracy over time |

### Research Items

| Item | Status |
|------|--------|
| Optimal test phrase count per category | 🔬 Research needed |
| Adversarial testing techniques | 🔬 Research needed |

---

## 📝 Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-01-12 | v5.0.1 | Roadmap restructured to hybrid template format | PapaBearDoes |
| 2026-01-11 | v5.0.0 | Initial v5.0 roadmap created | PapaBearDoes |

---

**Built with care for chosen family** 🏳️‍🌈
