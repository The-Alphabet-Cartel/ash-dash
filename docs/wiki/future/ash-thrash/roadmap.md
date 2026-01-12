# Ash-Thrash v5.0 Roadmap

============================================================================
**Ash-Thrash**: Discord Crisis Detection Testing Suite
**The Alphabet Cartel** - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================

**Document Version**: v5.0  
**Created**: 2026-01-11  
**Last Updated**: 2026-01-11  
**Status**: 🚧 In Development  
**Repository**: https://github.com/the-alphabet-cartel/ash-thrash

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Mission Statement](#mission-statement)
3. [Project Goals](#project-goals)
4. [Architecture Overview](#architecture-overview)
5. [Phase Overview](#phase-overview)
6. [Test Scenario Distribution](#test-scenario-distribution)
7. [Technology Stack](#technology-stack)
8. [Success Metrics](#success-metrics)
9. [Dependencies](#dependencies)
10. [Future Enhancements](#future-enhancements)

---

## Executive Summary

Ash-Thrash v5.0 is a complete recode of the Ash Ecosystem's testing suite, designed to comprehensively validate the crisis detection capabilities of Ash-NLP and eventually the entire Ash ecosystem. This version focuses on:

- **525+ test scenarios** across multiple crisis severity categories
- **Individual API testing** for detailed analysis and stress testing
- **Flexible tolerance system** for human communication variability
- **Comprehensive reporting** with baseline tracking for regression detection
- **Clean Architecture compliance** following the Ash ecosystem standards

---

## Mission Statement

```
MISSION - NEVER TO BE VIOLATED:
    Validate   → Verify crisis detection accuracy through live Ash-NLP integration testing
    Challenge  → Stress test the system with edge cases and adversarial scenarios
    Guard      → Prevent regressions that could compromise detection reliability
    Protect    → Safeguard our LGBTQIA+ community through rigorous quality assurance
```

---

## Project Goals

### Primary Goals

| Goal | Description | Success Criteria |
|------|-------------|------------------|
| **Accuracy Validation** | Verify Ash-NLP correctly classifies crisis messages | ≥95% accuracy on high/critical, ≥85% on medium/low |
| **False Positive Prevention** | Ensure non-crisis content doesn't trigger alerts | ≥95% accuracy on "none" priority messages |
| **Performance Validation** | Confirm Ash-NLP handles load appropriately | Response times within acceptable thresholds |
| **Regression Detection** | Catch accuracy degradations before production | Baseline comparison with deviation alerts |

### Secondary Goals

| Goal | Description |
|------|-------------|
| **Edge Case Coverage** | Test ambiguous scenarios, sarcasm, gaming context, cultural expressions |
| **LGBTQIA+ Specific Testing** | Validate detection of identity-related distress patterns |
| **Documentation** | Comprehensive test coverage reporting for team visibility |

---

## Architecture Overview

### Directory Structure

```
ash-thrash/
├── src/
│   ├── config/
│   │   ├── default.json
│   │   ├── testing.json
│   │   ├── production.json
│   │   └── phrases/
│   │       ├── high_priority.json
│   │       ├── medium_priority.json
│   │       ├── low_priority.json
│   │       ├── none_priority.json
│   │       ├── edge_cases/
│   │       │   ├── maybe_high_medium.json
│   │       │   ├── maybe_medium_low.json
│   │       │   └── maybe_low_none.json
│   │       └── specialty/
│   │           ├── irony_sarcasm.json
│   │           ├── gaming_context.json
│   │           ├── song_lyrics_quotes.json
│   │           ├── lgbtqia_specific.json
│   │           └── cultural_slang.json
│   │
│   ├── managers/
│   │   ├── config_manager.py
│   │   ├── secrets_manager.py
│   │   ├── logging_config_manager.py
│   │   ├── nlp_client_manager.py
│   │   ├── phrase_loader_manager.py
│   │   ├── test_runner_manager.py
│   │   ├── result_analyzer_manager.py
│   │   └── report_manager.py
│   │
│   └── validators/
│       ├── classification_validator.py
│       └── response_validator.py
│
├── tests/
├── reports/
├── logs/
├── docs/
├── main.py
├── Dockerfile
└── docker-compose.yml
```

### Manager Responsibilities

| Manager | Responsibility |
|---------|----------------|
| `ConfigManager` | JSON configuration loading, environment variable overrides, validation |
| `SecretsManager` | Docker secrets handling for sensitive tokens |
| `LoggingConfigManager` | Colorized, structured logging output (Rule #11) |
| `NLPClientManager` | HTTP client for Ash-NLP API with retry logic |
| `PhraseLoaderManager` | Load and validate test phrases from JSON files |
| `TestRunnerManager` | Orchestrate test execution, progress tracking |
| `ResultAnalyzerManager` | Calculate accuracy metrics, category breakdowns |
| `ReportManager` | Generate JSON/HTML reports, Discord webhook notifications |

---

## Phase Overview

### Phase Summary

| Phase | Name | Description | Estimated Effort |
|-------|------|-------------|------------------|
| **Phase 1** | Foundation | Core infrastructure, managers, logging | 8-12 hours |
| **Phase 2** | Test Execution Engine | Runner, validators, result collection | 6-8 hours |
| **Phase 3** | Analysis & Reporting | Metrics, reports, baseline tracking | 6-8 hours |
| **Phase 4** | Test Data Population | 525+ test scenarios across categories | 8-12 hours |
| **Phase 5** | Performance & Stress Testing | Load testing, latency analysis | 4-6 hours |

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

### Detailed Phase Breakdown

#### Phase 1: Foundation
- ConfigManager completion with full validation
- LoggingConfigManager with colorized output
- SecretsManager for Docker secrets
- NLPClientManager with HTTP client, retry logic, timeout handling
- PhraseLoaderManager with JSON schema validation

#### Phase 2: Test Execution Engine
- TestRunnerManager for orchestration
- ClassificationValidator for expected vs actual comparison
- ResponseValidator for API response structure
- In-memory result collection
- Progress tracking and status reporting

#### Phase 3: Analysis & Reporting
- ResultAnalyzerManager for metrics calculation
- Accuracy by category, subcategory, and overall
- False positive/negative rate tracking
- ReportManager for JSON, HTML, Discord webhook output
- Baseline storage and comparison logic

#### Phase 4: Test Data Population
- Migrate existing ~200 phrases from old structure
- Expand to 525+ scenarios
- Add new subcategories for specialty testing
- Validate phrase distribution and coverage

#### Phase 5: Performance & Stress Testing
- Concurrent request testing
- Latency tracking (p50, p95, p99)
- Load curve generation
- Server stability validation
- Resource utilization monitoring

---

## Test Scenario Distribution

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

### Subcategory Organization

Each priority category maintains granular subcategories for detailed weakness identification:

**High Priority Subcategories** (examples):
- `method_specific` - Explicit suicide methods mentioned
- `suicidal_planning` - Active planning statements
- `suicidal_intent_immediate` - Immediate intent expressions
- `death_ideation` - Death-focused thoughts
- `burden_thoughts` - Feeling like a burden to others
- `self_harm_intent` - Self-harm with intent

**Medium Priority Subcategories** (examples):
- `depression_severe` - Acknowledged severe depression
- `emotional_overwhelm` - Feeling overwhelmed
- `hopelessness` - Pervasive hopelessness
- `self_harm_thoughts` - Ideation without immediate intent
- `dissociation` - Dissociative episodes

---

## Technology Stack

### Core Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Primary language | 3.11+ |
| **pytest** | Testing framework | Latest |
| **httpx** | Async HTTP client | Latest |
| **Pydantic** | Data validation | v2.x |
| **Rich** | Terminal output formatting | Latest |

### Infrastructure

| Component | Purpose |
|-----------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Service orchestration |
| **Docker Secrets** | Sensitive credential management |

### Target Server

| Specification | Value |
|---------------|-------|
| **OS** | Debian 12 |
| **CPU** | AMD Ryzen 7 5800x |
| **GPU** | NVIDIA RTX 3060 (12GB VRAM) |
| **RAM** | 64GB |
| **Server IP** | 10.20.30.253 |

---

## Success Metrics

### Accuracy Targets

| Category | Minimum | Target | Stretch |
|----------|---------|--------|---------|
| High/Critical | 90% | 95% | 98% |
| Medium | 80% | 85% | 90% |
| Low | 80% | 85% | 90% |
| None (False Positive Prevention) | 90% | 95% | 98% |

### Performance Targets

| Metric | Acceptable | Target | Optimal |
|--------|------------|--------|---------|
| Single Request Latency (p50) | <500ms | <300ms | <200ms |
| Single Request Latency (p95) | <1000ms | <500ms | <300ms |
| Sustained Throughput | 5 req/s | 10 req/s | 20 req/s |

### Quality Targets

| Metric | Target |
|--------|--------|
| Test Coverage (Ash-Thrash code) | ≥80% |
| Documentation Completeness | 100% |
| Clean Architecture Compliance | 100% |

---

## Dependencies

### External Dependencies

| Dependency | Required For | Status |
|------------|--------------|--------|
| Ash-NLP Server | All testing | ✅ Available at 10.20.30.253:30880 |
| Docker | Containerization | ✅ Available on Lofn |
| Network Access | API communication | ✅ Internal network |

### Internal Dependencies

| Dependency | Required For | Notes |
|------------|--------------|-------|
| Clean Architecture Charter | Code standards | Must follow v5.1+ |
| Ash-NLP API Schema | Request/Response format | See `docs/api/` |

---

## Future Enhancements

The following enhancements are planned for post-v5.0 releases. See `docs/wiki/future/ash-thrash/enhancements.md` for full details.

### Planned Enhancements

| Enhancement | Priority | Description |
|-------------|----------|-------------|
| Multi-Consensus Algorithm Testing | 🟡 Medium | Test each phrase against all consensus algorithms |
| Discord Message Simulation | 🟡 Medium | End-to-end Ash-Bot integration testing |
| Ash-Dash API Integration | 🟢 Low | Dashboard data flow validation |

### Research Items

| Item | Status |
|------|--------|
| Optimal test phrase count per category | 🔬 Research needed |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v5.0 | 2026-01-11 | PapaBearDoes + Claude | Initial v5.0 roadmap |

---

**Built with care for chosen family** 🏳️‍🌈
