# Ash-NLP v5.0 Complete Rewrite Roadmap

**Version**: v5.0  
**Repository**: https://github.com/the-alphabet-cartel/ash-nlp
**Community**: [The Alphabet Cartel](https://discord.gg/alphabetcartel) | [alphabetcartel.org](https://alphabetcartel.org)

---

## 📋 **TABLE OF CONTENTS**

1. [Executive Summary](#executive-summary)
2. [Architecture Decision](#architecture-decision)
3. [Model Selection](#model-selection)
4. [Project Phases](#project-phases)
5. [Phase Tracking](#phase-tracking)
6. [Dependencies & Prerequisites](#dependencies--prerequisites)
7. [Success Criteria](#success-criteria)
8. [Rollback Procedures](#rollback-procedures)

---

## 🎯 **EXECUTIVE SUMMARY**

### **Project Goal**
Complete rewrite of Ash-NLP from v3.1 to v5.0, implementing Local Multi-Model Ensemble architecture inspired by LLM Council principles while maintaining Clean Architecture Charter v5.0 compliance.

### **Key Changes**
- ✅ **Architecture**: Single model → Local Multi-Model Ensemble (Council-inspired)
- ✅ **Models**: Upgrade from generic zero-shot to specialized crisis detection models
- ✅ **Testing**: Implement comprehensive model evaluation framework
- ✅ **Context**: Add rolling window analysis for temporal pattern detection
- ✅ **Privacy**: Maintain 100% local processing (no external APIs)
- ✅ **Cost**: Maintain $0 ongoing costs (GPU-based, no API fees)

### **Non-Negotiables**
- ⚠️ **Latency**: Must remain < 500ms per message analysis
- ⚠️ **Privacy**: All data stays on local server (10.20.30.253)
- ⚠️ **Clean Architecture**: 100% v5.0 Charter compliance
- ⚠️ **Availability**: 24/7 uptime for crisis detection
- ⚠️ **VRAM**: Must fit within 12GB RTX 3060 constraints

---

## 📈 **PROGRESS TRACKING**

### **Current Status**: Phase 5 In Progress 🚧

### **Phase Completion**:
- [x] Phase 0: Foundation & Planning - 100% ✅
- [x] Phase 1: Testing Framework - 100% ✅
- [x] Phase 2: Model Migration - 100% ✅
- [x] Phase 3: API & Docker Deployment - 100% ✅
- [x] Phase 4: Ensemble Coordinator Enhancement - 100% ✅
- [x] Phase 5: Context History Analysis - 100% ✅

### **Overall Progress**: 100% (6/6 phases complete) 🎉

### **Phase Dependency Map**
```
Phase 0: Foundation & Planning ✅
    ↓
Phase 1: Testing Framework Setup ✅
    ↓
Phase 2: Model Migration & Integration ✅
    ↓
Phase 3: API & Docker Deployment ✅
    ↓
Phase 4: Ensemble Coordinator Enhancement ✅
    ↓
Phase 5: Context History Analysis ⏳
```

---

## 🏛️ **ARCHITECTURE DECISION**

### **Selected Approach: Local Multi-Model Ensemble (Option 3)**

**Rationale**:
```
┌─────────────────────────────────────────────────────────────────┐
│              Discord Message → CrisisAnalyzer                   │
├─────────────────────────────────────────────────────────────────┤
│  Local GPU Ensemble (4 models running in parallel)              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────┐  │
│  │ Model 1:     │ │ Model 2:     │ │ Model 3:     │ │Model 4:│  │
│  │ Crisis       │ │ Emotion      │ │ Sentiment    │ │Irony   │  │
│  │ Severity     │ │ Detection    │ │ Analysis     │ │Detect  │  │
│  │ (Zero-Shot)  │ │ (28 classes) │ │ (Pos/Neg/Neu)│ │(Sarc.) │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  Consensus Coordinator (Council-inspired logic) [Phase 4]       │
│  - Multiple consensus algorithms                                │
│  - Conflict detection & resolution                              │
│  - Human-readable explainability                                │
├─────────────────────────────────────────────────────────────────┤
│  Pattern Enhancement (existing functionality)                   │
│  - Temporal modifiers                                           │
│  - Contextual patterns                                          │
├─────────────────────────────────────────────────────────────────┤
│  Context History Analyzer (Phase 5 - rolling window)            │
│  - User message history (last 5-10 messages)                    │
│  - Escalation detection                                         │
│  - Temporal trends                                              │
├─────────────────────────────────────────────────────────────────┤
│  Crisis Score + Alert Decision                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Why This Approach**:
- ✅ **Latency**: 3-7 seconds (acceptable for crisis detection)
- ✅ **Privacy**: 100% local, no external APIs
- ✅ **Cost**: $0 ongoing (electricity only)
- ✅ **Accuracy**: Multi-model consensus reduces false positives/negatives
- ✅ **Council Benefits**: Cross-validation without external dependencies
- ✅ **VRAM Efficient**: ~1.5GB total (well within 12GB limit)

---

## 🎯 **MODEL SELECTION**

### **New Model Ensemble (v5.0)**

| Model | Purpose | Downloads | VRAM | Latency |
|-------|---------|-----------|------|---------|
| `facebook/bart-large-mnli` | Crisis Classifier | 132.9M | ~800MB | 1-2s |
| `SamLowe/roberta-base-go_emotions` | Emotion Detection | 92.8M | ~250MB | 0.5-1s |
| `cardiffnlp/twitter-roberta-base-sentiment-latest` | Sentiment Analysis | 295.9M | ~250MB | 0.3-0.5s |
| `cardiffnlp/twitter-roberta-base-irony` | Irony Detection | 71.1K | ~250MB | 0.3-0.5s |

**Total Ensemble Resources**:
- Total VRAM: ~1.55GB (12.9% of 12GB available)
- Total Parameters: ~782M
- Expected Latency: 3-7 seconds for full ensemble analysis

---

## 📝 **PHASE 0: FOUNDATION & PLANNING**

### **Status**: ✅ **COMPLETED** (2025-12-30)

### **Deliverables**:
- [x] Architecture decision documented (Local Multi-Model Ensemble)
- [x] Model selection finalized (4 models identified)
- [x] Roadmap created (this document)
- [x] Clean Architecture Charter v5.0 reviewed
- [x] Resource constraints validated (VRAM, latency, cost)

---

## 📝 **PHASE 1: TESTING FRAMEWORK SETUP**

### **Status**: ✅ **COMPLETED** (2025-12-30)

### **Deliverables**:
- [x] Testing directory structure created
- [x] Test datasets: crisis_examples.json, safe_examples.json, edge_cases.json, lgbtqia_specific.json, escalation_patterns.json
- [x] ModelEvaluator class implemented
- [x] Metrics calculators implemented
- [x] Report generation working
- [x] Baseline v3.1 performance documented

---

## 📝 **PHASE 2: MODEL MIGRATION & INTEGRATION**

### **Status**: ✅ **COMPLETED** (2025-12-31)

### **Deliverables**:
- [x] All 4 models downloaded and cached
- [x] ModelLoader implemented and tested
- [x] ModelWrapper interface implemented
- [x] All models validated independently
- [x] Total VRAM < 2GB verified
- [x] Total latency < 10 seconds verified

---

## 📝 **PHASE 3: API & DOCKER DEPLOYMENT**

### **Status**: ✅ **COMPLETED** (2026-01-01)

### **Deliverables**:
- [x] Ensemble Decision Engine implemented
- [x] FastAPI application with OpenAPI docs
- [x] Docker deployment with GPU support
- [x] Configuration management (JSON + environment)
- [x] Error handling with circuit breaker pattern
- [x] Logging and Discord alerting
- [x] Async parallel model inference

---

## 📝 **PHASE 4: ENSEMBLE COORDINATOR ENHANCEMENT**

### **Status**: ✅ **COMPLETED** (2026-01-01)

> **Documentation**: See `docs/v5.0/Phase4/` for detailed implementation docs

### **Deliverables**:

**Consensus Algorithms** (4 implemented):
- [x] Weighted Voting (default)
- [x] Majority Voting
- [x] Unanimous Consensus
- [x] Conflict-Aware Consensus

**Conflict Detection & Resolution**:
- [x] Score Disagreement detection (HIGH severity)
- [x] Irony-Sentiment Conflict detection (MEDIUM severity)
- [x] Emotion-Crisis Mismatch detection (MEDIUM severity)
- [x] Label Disagreement detection (MEDIUM severity)
- [x] Resolution strategies: conservative, optimistic, mean, review_flag
- [x] Discord alerts for model conflicts

**Result Aggregation**:
- [x] Comprehensive crisis assessment output
- [x] Model contribution summaries
- [x] Performance metrics tracking
- [x] Backward compatibility (legacy format)

**Explainability Layer**:
- [x] Three verbosity levels: minimal, standard, detailed
- [x] Human-readable decision summaries
- [x] Key factor identification
- [x] Recommended actions

**API Enhancements**:
- [x] Enhanced `/analyze` with Phase 4 options
- [x] `GET /config/consensus` endpoint
- [x] `PUT /config/consensus` endpoint
- [x] Phase 4 response schemas

**Testing**:
- [x] test_consensus.py (25+ tests)
- [x] test_conflict_detector.py (25+ tests)
- [x] test_conflict_resolver.py (25+ tests)
- [x] test_aggregator.py (30+ tests)
- [x] test_explainability.py (35+ tests)

### **Files Created**:
```
src/ensemble/consensus.py
src/ensemble/conflict_detector.py
src/ensemble/conflict_resolver.py
src/ensemble/aggregator.py
src/ensemble/explainability.py
src/config/consensus_config.json
tests/phase4/*.py (5 test files)
docs/v5.0/Phase4/phase_4_summary.md
docs/v5.0/Phase4/api_reference.md
```

---

## 📝 **PHASE 5: CONTEXT HISTORY ANALYSIS**

### **Status**: ⏳ **IN PROGRESS**

### **Duration**: 2-3 weeks
### **Priority**: MEDIUM

> **Documentation**: See `docs/v5.0/Phase5/phase_5_planning.md` for detailed implementation plan

### **Key Architectural Decision**:

**Ash-NLP remains STATELESS.** All message history persistence is managed by Ash-Bot.
Ash-NLP receives message history as part of the request payload and performs analysis.

### **Planned Objectives**:

**Context Analysis** (Ash-NLP receives history from Ash-Bot):
- [x] Escalation detection across message sequences
- [x] Temporal pattern detection (late night, rapid posting)
- [x] Trend analysis (worsening, stable, improving)
- [x] Pattern classification (rapid, gradual, sudden onset)
- [x] Intervention urgency scoring

**Configuration Management**:
- [x] `context_config.json` with environment variable overrides
- [x] `ContextConfigManager` with factory function
- [x] Configurable `max_history_size` (default: 20 messages)
- [x] Configurable `alert_cooldown_seconds` (default: 300)

**API Enhancement**:
- [x] Accept `message_history[]` in request payload
- [x] Return `context_analysis` in response
- [x] `GET/PUT /config/context` endpoints

**Engine Integration**:
- [x] Integrate ContextAnalyzer into EnsembleDecisionEngine
- [x] Add `phase5_enabled` configuration parameter
- [x] Update sync/async analyze methods
- [x] Add context analysis to CrisisAssessment dataclass

**Remaining Tasks**:
- [x] Discord escalation alerting integration
- [x] Unit tests for Phase 5 components
- [x] Integration tests for end-to-end flow

**NOT in Ash-NLP Scope** (handled elsewhere):
- Message persistence (Ash-Bot)
- Rolling window management (Ash-Bot)
- Performance benchmarking (Ash-Thrash)
- Monitoring dashboards (Ash-Dash)

### **File Structure**:
```
src/context/
├── __init__.py
├── context_analyzer.py   # Main orchestrator
├── escalation_detector.py # Escalation detection algorithms
├── temporal_detector.py  # Time-based pattern detection
└── trend_analyzer.py     # Trend direction and velocity

src/managers/
└── context_config_manager.py  # ContextConfigManager

src/config/context_config.json
tests/phase5/
```

---

## 🎯 **SUCCESS CRITERIA**

### **Phase Completion Criteria**:

| Phase | Status | Key Metrics |
|-------|--------|-------------|
| Phase 0: Foundation | ✅ Complete | Architecture documented |
| Phase 1: Testing | ✅ Complete | Baseline established |
| Phase 2: Models | ✅ Complete | VRAM < 2GB, Latency < 10s |
| Phase 3: API/Deploy | ✅ Complete | Docker deployed, GPU enabled |
| Phase 4: Ensemble | ✅ Complete | 4 algorithms, 140+ tests |
| Phase 5: Context | ⏳ Pending | TBD |

---

## 📊 **DEPENDENCIES & PREREQUISITES**

### **Technical Stack**:
- **Server**: Debian 12, AMD Ryzen 7 5800x, 64GB RAM
- **GPU**: NVIDIA RTX 3060 12GB VRAM
- **Docker**: Latest version with GPU support
- **Python**: 3.11+
- **CUDA**: 12.2+

### **Key Dependencies**:
```
transformers>=4.35.0
torch>=2.1.0
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0
```

---

## 💾 **VERSION CONTROL**

### **Document Version**: v5.0.9
### **Last Updated**: 2026-01-02
### **Last Updated By**: Project Team

### **Change Log**:
```
2026-01-02: PHASE 5 COMPLETE 🎉
- Created tests/integration/ directory structure
- test_engine_context_integration.py - 5 test classes, 20+ test methods
- test_api_context_flow.py - 8 test classes, 25+ test methods
- Full API → Engine → Context → Response flow tested
- All 6 phases now 100% complete!

2026-01-02: Phase 5 unit tests complete
- Created tests/phase5/ directory structure
- test_escalation_detector.py - 11 test classes, 35+ test methods
- test_temporal_detector.py - 10 test classes, 30+ test methods  
- test_trend_analyzer.py - 10 test classes, 30+ test methods
- test_context_analyzer.py - 10 test classes, 25+ test methods
- test_alerting_escalation.py - 7 test classes, 20+ test methods
- Progress: 95% (7/8 objectives complete)

2026-01-02: Phase 5 Discord alerting complete
- Added ESCALATION severity level to AlertSeverity enum
- Implemented send_escalation_alert() async method
- Implemented send_escalation_alert_sync() sync method
- Added escalation-specific cooldown (300s default)
- Urgency-based severity mapping (immediate=CRITICAL, high=ESCALATION)
- Updated factory function with escalation_cooldown_seconds parameter
- Progress: 85% (6/8 objectives complete)

2026-01-02: Phase 5 engine integration complete
- Integrated ContextAnalyzer into EnsembleDecisionEngine
- Updated API schemas with Phase 5 request/response types
- Enhanced /analyze endpoint with message_history support
- Added phase5_enabled configuration parameter
- Updated CrisisAssessment dataclass with context_analysis field
- Sync and async analyze methods now support context analysis
- Progress: 75% (6/8 objectives complete)

2026-01-01: Phase 5 core implementation
- Created src/context/ module with 4 core files
- Implemented ContextAnalyzer orchestrator
- Implemented EscalationDetector with pattern matching
- Implemented TemporalDetector (late night, rapid posting)
- Implemented TrendAnalyzer (direction, velocity)
- All factories follow Clean Architecture v5.1
- Progress: 60% (5/8 objectives complete)

2026-01-01: Phase 5 planning completed
- Planning document created (phase_5_planning.md)
- Architecture decision: Ash-NLP remains stateless
- Ash-Bot handles message persistence and rolling window
- Configuration schema designed (context_config.json)
- Confirmed max_history_size=20, alert_cooldown=300s
- Performance benchmarking deferred to Ash-Thrash

2026-01-01: Phase 4 completed
- Consensus algorithms implemented (4)
- Conflict detection/resolution complete
- Explainability layer added
- 140+ unit tests created
- API enhanced with Phase 4 endpoints
- Documentation updated

2026-01-01: Phase 3 completed
- API and Docker deployment operational
- GPU inference working
- Production ready

2025-12-31: Phase 2 completed
- All 4 models validated
- Model wrappers implemented

2025-12-30: Phase 1 completed
- Testing framework operational
- Baseline metrics established

2025-12-30: Initial roadmap created (Phase 0 complete)
- Architecture decision documented
- Model selection finalized
```

---

## 🏁 **NEXT STEPS**

**Phase 5 Implementation** (COMPLETE ✅):
1. ✅ Planning document created (`docs/v5.0/Phase5/phase_5_planning.md`)
2. ✅ Architecture decision: Ash-NLP remains stateless
3. ✅ Configuration schema designed (`context_config.json`)
4. ✅ Created `context_config.json` and `ContextConfigManager`
5. ✅ Implemented core context analysis components
6. ✅ Implemented escalation detection algorithms
7. ✅ Implemented temporal pattern detection
8. ✅ API enhancement with message history support
9. ✅ Engine integration (ContextAnalyzer in EnsembleDecisionEngine)
10. ✅ Discord escalation alerting
11. ✅ Unit tests for Phase 5 components
12. ✅ Integration tests for end-to-end flow

**Immediate Actions**: ALL COMPLETE ✅
- [x] Create Phase 5 planning document
- [x] Design context_config.json schema
- [x] Confirm architectural decisions (stateless NLP)
- [x] Create `src/config/context_config.json`
- [x] Create `src/managers/context_config_manager.py`
- [x] Update `.env.template` with Phase 5 variables
- [x] Create `src/context/` module structure
- [x] Implement `EscalationDetector` class
- [x] Implement `TemporalDetector` class
- [x] Implement `TrendAnalyzer` class
- [x] Implement `ContextAnalyzer` orchestrator
- [x] Update API schemas for context analysis
- [x] Update `/analyze` endpoint with message history support
- [x] Integrate ContextAnalyzer into EnsembleDecisionEngine
- [x] Implement Discord escalation alerting
- [x] Create unit tests for Phase 5 components
- [x] Create integration tests for end-to-end flow

---

**Built with care for chosen family** 🏳️‍🌈
