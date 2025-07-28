# 🔌 Ash Dashboard API Documentation v2.1

**Complete REST API Reference**  
**Repository:** https://github.com/the-alphabet-cartel/ash-dash  
**Base URL:** https://10.20.30.253:8883/api  
**OpenAPI Spec:** https://10.20.30.253:8883/docs

## 📋 API Overview

The Ash Dashboard API provides comprehensive endpoints for crisis monitoring, team management, analytics, and system integration. All endpoints require authentication unless explicitly noted.

### 🏗️ Base Configuration

**API Base URL:** `https://10.20.30.253:8883/api`  
**API Version:** `v2.1`  
**Content Type:** `application/json`  
**Authentication:** Bearer Token (Discord OAuth2)

### 🔐 Authentication

All API requests require authentication using Discord OAuth2 Bearer tokens.

**Authentication Flow:**
```bash
# 1. Redirect user to Discord OAuth
GET https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&redirect_uri=REDIRECT_URI&response_type=code&scope=identify

# 2. Exchange code for token
POST https://10.20.30.253:8883/api/auth/discord/callback
Content-Type: application/json
{
  "code": "DISCORD_AUTH_CODE"
}

# Response
{
  "access_token": "JWT_TOKEN",
  "refresh_token": "REFRESH_TOKEN",
  "expires_in": 3600,
  "user": {
    "id": "user_id",
    "username": "username",
    "discriminator": "1234",
    "avatar": "avatar_hash",
    "roles": ["crisis_responder", "team_lead"]
  }
}

# 3. Use token in subsequent requests
Authorization: Bearer JWT_TOKEN
```

## 🚨 Crisis Management Endpoints

### Get Active Crises

```http
GET /api/crises/active
Authorization: Bearer {token}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "active_crises": [
      {
        "id": "crisis_12345",
        "severity": "HIGH",
        "user_id": "anonymized_user_678",
        "detected_at": "2025-01-28T14:32:18Z",
        "confidence": 94.2,
        "status": "ACTIVE",
        "assigned_responder": null,
        "trigger_message": "I can't take this anymore...",
        "analysis": {
          "keywords_detected": ["suicidal_ideation", "hopelessness"],
          "pattern_analysis": "escalating_distress",
          "risk_factors": ["isolation", "recent_loss"],
          "protective_factors": ["community_engagement"]
        },
        "history": {
          "previous_interventions": 2,
          "last_contact": "2025-01-25T10:15:30Z",
          "response_rate": "positive"
        },
        "recommended_actions": [
          "immediate_private_contact",
          "safety_assessment",
          "resource_provision"
        ]
      }
    ],
    "total_count": 1,
    "by_severity": {
      "HIGH": 1,
      "MEDIUM": 3,
      "LOW": 7
    }
  }
}
```

### Assign Crisis to Responder

```http
POST /api/crises/{crisis_id}/assign
Authorization: Bearer {token}
Content-Type: application/json

{
  "responder_id": "user_12345",
  "notes": "Taking this case - available for immediate response"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "crisis_id": "crisis_12345",
    "assigned_to": "user_12345",
    "assigned_at": "2025-01-28T14:35:42Z",
    "assignment_notes": "Taking this case - available for immediate response"
  }
}
```

### Update Crisis Status

```http
PUT /api/crises/{crisis_id}/status
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "IN_PROGRESS",
  "contact_method": "discord_dm",
  "initial_response": "User responsive and willing to engage",
  "safety_level": "MODERATE_RISK",
  "intervention_notes": "Provided immediate support and scheduled follow-up",
  "resources_provided": [
    "crisis_hotline_988",
    "local_therapy_resources",
    "community_support_channels"
  ],
  "follow_up_scheduled": "2025-01-29T10:00:00Z"
}
```

### Complete Crisis Intervention

```http
POST /api/crises/{crisis_id}/complete
Authorization: Bearer {token}
Content-Type: application/json

{
  "resolution_type": "SUCCESSFUL_INTERVENTION",
  "outcome_summary": "User connected with professional support, safety plan created",
  "resources_utilized": [
    "local_therapist_referral",
    "peer_support_group",
    "safety_planning_session"
  ],
  "follow_up_required": true,
  "follow_up_schedule": "weekly_check_ins",
  "responder_notes": "User expressed gratitude and seems stabilized with support plan"
}
```

## 👥 Team Management Endpoints

### Get Team Status

```http
GET /api/team/status
Authorization: Bearer {token}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "online_responders": [
      {
        "user_id": "responder_123",
        "username": "CrisisResponder1",
        "role": "SENIOR_RESPONDER",
        "status": "AVAILABLE",
        "current_cases": 2,
        "max_capacity": 5,
        "specializations": ["lgbtq_youth", "substance_abuse"],
        "last_activity": "2025-01-28T14:30:00Z"
      }
    ],
    "shift_schedule": {
      "current_shift": {
        "start": "2025-01-28T08:00:00Z",
        "end": "2025-01-28T16:00:00Z",
        "lead": "responder_123",
        "coverage": "FULL"
      },
      "next_shift": {
        "start": "2025-01-28T16:00:00Z",
        "end": "2025-01-29T00:00:00Z",
        "lead": "responder_456",
        "coverage": "PARTIAL"
      }
    },
    "team_metrics": {
      "total_responders": 12,
      "available_now": 4,
      "on_break": 1,
      "off_duty": 7,
      "average_response_time": "4.2_minutes",
      "current_workload": "MODERATE"
    }
  }
}
```

### Update Responder Availability

```http
PUT /api/team/responder/{user_id}/availability
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "AVAILABLE",
  "max_concurrent_cases": 3,
  "specializations": ["depression", "anxiety", "lgbtq_issues"],
  "shift_notes": "Available for high-priority cases",
  "contact_preferences": {
    "discord_dm": true,
    "dashboard_notifications": true,
    "mobile_alerts": false
  }
}
```

### Get Team Performance Analytics

```http
GET /api/team/analytics
Authorization: Bearer {token}
Query Parameters:
  - start_date (ISO 8601)
  - end_date (ISO 8601)
  - responder_id (optional)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "date_range": {
      "start": "2025-01-21T00:00:00Z",
      "end": "2025-01-28T23:59:59Z"
    },
    "team_metrics": {
      "total_interventions": 47,
      "successful_resolutions": 42,
      "average_response_time": "3.8_minutes",
      "average_resolution_time": "45_minutes",
      "escalation_rate": "10.6%"
    },
    "individual_performance": [
      {
        "responder_id": "responder_123",
        "cases_handled": 12,
        "success_rate": "91.7%",
        "average_response_time": "3.2_minutes",
        "user_satisfaction": 4.8,
        "specialization_effectiveness": {
          "lgbtq_youth": "95%",
          "substance_abuse": "87%"
        }
      }
    ],
    "trends": {
      "response_time_trend": "IMPROVING",
      "case_volume_trend": "STABLE",
      "team_capacity_trend": "ADEQUATE"
    }
  }
}
```

## 📊 Analytics & Reporting Endpoints

### Get Community Health Metrics

```http
GET /api/analytics/community-health
Authorization: Bearer {token}
Query Parameters:
  - period (day|week|month|quarter|year)
  - granularity (hour|day|week)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "period": "month",
    "community_wellness_index": 7.3,
    "trend_direction": "STABLE",
    "metrics": {
      "crisis_detection_rate": {
        "current": 2.1,
        "previous": 2.3,
        "unit": "per_1000_messages",
        "change": "-8.7%"
      },
      "intervention_success_rate": {
        "current": 89.2,
        "previous": 87.5,
        "unit": "percentage",
        "change": "+1.9%"
      },
      "community_engagement": {
        "active_users": 1247,
        "support_channel_usage": 156,
        "peer_support_interactions": 89
      },
      "risk_indicators": {
        "high_risk_periods": ["Sunday_evening", "Monday_morning"],
        "seasonal_factors": ["winter_months", "holiday_periods"],
        "emerging_trends": ["academic_stress", "relationship_concerns"]
      }
    },
    "predictions": {
      "next_week_risk_level": "MODERATE",
      "intervention_capacity_needed": "standard",
      "recommended_team_size": 8
    }
  }
}
```

### Get Crisis Detection Analytics

```http
GET /api/analytics/detection
Authorization: Bearer {token}
Query Parameters:
  - start_date (ISO 8601)
  - end_date (ISO 8601)
  - model_version (optional)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "detection_performance": {
      "total_analyses": 15234,
      "crises_detected": 47,
      "false_positives": 3,
      "missed_detections": 1,
      "accuracy": 97.2,
      "precision": 94.0,
      "recall": 97.9,
      "f1_score": 95.9
    },
    "model_performance": {
      "current_model": "ash-nlp-v2.1.3",
      "confidence_distribution": {
        "90-100%": 23,
        "80-89%": 15,
        "70-79%": 9,
        "60-69%": 0
      },
      "processing_times": {
        "average": "234ms",
        "p95": "450ms",
        "p99": "678ms"
      }
    },
    "pattern_analysis": {
      "most_common_indicators": [
        "hopelessness_language",
        "isolation_expressions",
        "life_transition_stress"
      ],
      "emerging_patterns": [
        "academic_pressure_keywords",
        "financial_stress_indicators"
      ],
      "temporal_patterns": {
        "peak_hours": ["22:00-02:00", "14:00-16:00"],
        "peak_days": ["Sunday", "Monday"],
        "seasonal_trends": "winter_increase"
      }
    }
  }
}
```

### Export Analytics Report

```http
POST /api/analytics/export
Authorization: Bearer {token}
Content-Type: application/json

{
  "report_type": "comprehensive",
  "date_range": {
    "start": "2025-01-01T00:00:00Z",
    "end": "2025-01-31T23:59:59Z"
  },
  "sections": [
    "crisis_overview",
    "team_performance",
    "community_health",
    "model_effectiveness"
  ],
  "format": "pdf",
  "include_anonymized_cases": true,
  "recipient_email": "team-lead@alphabetcartel.org"
}
```

## 🔗 Service Integration Endpoints

### Get Service Health Status

```http
GET /api/services/health
Authorization: Bearer {token}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "services": {
      "ash-bot": {
        "status": "HEALTHY",
        "endpoint": "http://10.20.30.253:8882",
        "last_check": "2025-01-28T14:45:12Z",
        "response_time": "45ms",
        "version": "v2.1.2",
        "uptime": "99.8%"
      },
      "ash-nlp": {
        "status": "HEALTHY",
        "endpoint": "http://10.20.30.253:8881",
        "last_check": "2025-01-28T14:45:10Z",
        "response_time": "123ms",
        "version": "v2.1.1",
        "queue_size": 0,
        "processing_rate": "15.2_per_second"
      },
      "ash-thrash": {
        "status": "HEALTHY",
        "endpoint": "http://10.20.30.253:8884",
        "last_check": "2025-01-28T14:45:08Z",
        "response_time": "67ms",
        "version": "v2.1.0",
        "last_test_run": "2025-01-28T12:00:00Z",
        "test_success_rate": "98.7%"
      }
    },
    "overall_status": "HEALTHY",
    "system_load": {
      "cpu_usage": "23%",
      "memory_usage": "67%",
      "disk_usage": "45%",
      "network_throughput": "normal"
    }
  }
}
```

### Trigger Integration Test

```http
POST /api/services/test-integration
Authorization: Bearer {token}
Content-Type: application/json

{
  "service": "ash-nlp",
  "test_type": "connectivity",
  "test_message": "This is a test message for crisis detection validation"
}
```

## 🛡️ Security & Audit Endpoints

### Get Audit Log

```http
GET /api/audit/log
Authorization: Bearer {token}
Query Parameters:
  - start_date (ISO 8601)
  - end_date (ISO 8601)
  - user_id (optional)
  - action_type (optional)
  - page (default: 1)
  - limit (default: 50, max: 200)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "audit_entries": [
      {
        "id": "audit_789",
        "timestamp": "2025-01-28T14:32:18Z",
        "user_id": "responder_123",
        "action": "CRISIS_ASSIGNMENT",
        "resource": "crisis_12345",
        "details": {
          "crisis_severity": "HIGH",
          "assignment_method": "manual",
          "response_time": "3.2_minutes"
        },
        "ip_address": "10.20.30.45",
        "user_agent": "Dashboard/2.1.0 (Chrome/120.0.0.0)"
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 5,
      "total_entries": 247,
      "has_next": true,
      "has_previous": false
    }
  }
}
```

### Get User Permissions

```http
GET /api/auth/permissions
Authorization: Bearer {token}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": "responder_123",
    "roles": ["CRISIS_RESPONDER", "TEAM_MEMBER"],
    "permissions": [
      "crises.view",
      "crises.assign",
      "crises.update",
      "team.view_status",
      "analytics.view_basic",
      "resources.access"
    ],
    "restrictions": [
      "admin.user_management",
      "admin.system_config",
      "analytics.export_full"
    ],
    "session_info": {
      "login_time": "2025-01-28T08:15:30Z",
      "expires_at": "2025-01-28T16:15:30Z",
      "last_activity": "2025-01-28T14:45:12Z"
    }
  }
}
```

## 📱 Real-time WebSocket Events

### WebSocket Connection

```javascript
// Connect to WebSocket
const ws = new WebSocket('wss://10.20.30.253:8883/ws');

// Authentication
ws.onopen = function() {
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'YOUR_JWT_TOKEN'
  }));
};

// Subscribe to events
ws.send(JSON.stringify({
  type: 'subscribe',
  channels: ['crises', 'team_status', 'system_alerts']
}));
```

### Event Types

**Crisis Alert:**
```json
{
  "type": "crisis_alert",
  "data": {
    "crisis_id": "crisis_12345",
    "severity": "HIGH",
    "user_id": "anonymized_user_678",
    "confidence": 94.2,
    "requires_immediate_attention": true,
    "estimated_response_time": "5_minutes"
  },
  "timestamp": "2025-01-28T14:32:18Z"
}
```

**Team Status Update:**
```json
{
  "type": "team_status_update",
  "data": {
    "responder_id": "responder_123",
    "status_change": {
      "from": "AVAILABLE",
      "to": "RESPONDING"
    },
    "current_case_load": 3,
    "availability_notes": "Responding to high-priority case"
  },
  "timestamp": "2025-01-28T14:35:42Z"
}
```

**System Alert:**
```json
{
  "type": "system_alert",
  "data": {
    "alert_level": "WARNING",
    "service": "ash-nlp",
    "message": "Response time exceeding threshold",
    "details": {
      "current_response_time": "500ms",
      "threshold": "300ms",
      "queue_size": 15
    },
    "action_required": false
  },
  "timestamp": "2025-01-28T14:40:15Z"
}
```

## 🔧 Configuration & Admin Endpoints

### Get System Configuration

```http
GET /api/admin/config
Authorization: Bearer {token}
Requires: admin.system_config permission
```

### Update Crisis Detection Thresholds

```http
PUT /api/admin/detection-thresholds
Authorization: Bearer {token}
Content-Type: application/json

{
  "high_crisis_threshold": 0.85,
  "medium_crisis_threshold": 0.65,
  "low_crisis_threshold": 0.45,
  "auto_assignment_enabled": true,
  "escalation_timeout": 900,
  "max_responder_load": 5
}
```

## 📝 Error Handling

### Standard Error Response

```json
{
  "success": false,
  "error": {
    "code": "INVALID_CRISIS_ID",
    "message": "The specified crisis ID does not exist or is not accessible",
    "details": {
      "crisis_id": "invalid_id_123",
      "user_permissions": ["crises.view", "crises.assign"]
    },
    "request_id": "req_789456",
    "timestamp": "2025-01-28T14:45:30Z"
  }
}
```

### HTTP Status Codes

- **200 OK** - Successful request
- **201 Created** - Resource created successfully
- **400 Bad Request** - Invalid request parameters
- **401 Unauthorized** - Authentication required or invalid
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **409 Conflict** - Resource conflict (e.g., crisis already assigned)
- **429 Too Many Requests** - Rate limit exceeded
- **500 Internal Server Error** - Server error
- **503 Service Unavailable** - Service temporarily unavailable

### Rate Limiting

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1643723400
X-RateLimit-Window: 3600
```

**Rate Limits by Endpoint Category:**
- **Crisis Management:** 500 requests/hour
- **Analytics:** 200 requests/hour
- **Team Management:** 300 requests/hour
- **Real-time Updates:** No limit (WebSocket)
- **Admin Operations:** 100 requests/hour

## 🧪 Testing & Development

### API Testing Examples

**Using cURL:**
```bash
# Health check
curl -H "Authorization: Bearer $TOKEN" \
     https://10.20.30.253:8883/api/health

# Get active crises
curl -H "Authorization: Bearer $TOKEN" \
     https://10.20.30.253:8883/api/crises/active

# Assign crisis
curl -X POST \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"responder_id":"user_123","notes":"Taking this case"}' \
     https://10.20.30.253:8883/api/crises/crisis_12345/assign
```

**Using JavaScript (Fetch):**
```javascript
// Get team status
const response = await fetch('https://10.20.30.253:8883/api/team/status', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});

const teamStatus = await response.json();
console.log(teamStatus);
```

### API Client Libraries

**JavaScript/Node.js:**
```javascript
const AshDashboardAPI = require('@alphabet-cartel/ash-dashboard-client');

const client = new AshDashboardAPI({
  baseURL: 'https://10.20.30.253:8883/api',
  token: 'your_jwt_token'
});

// Get active crises
const crises = await client.crises.getActive();

// Assign crisis
await client.crises.assign('crisis_12345', {
  responder_id: 'user_123',
  notes: 'Taking this case'
});
```

**Python:**
```python
from ash_dashboard_client import AshDashboardClient

client = AshDashboardClient(
    base_url='https://10.20.30.253:8883/api',
    token='your_jwt_token'
)

# Get active crises
crises = client.crises.get_active()

# Assign crisis
client.crises.assign('crisis_12345', {
    'responder_id': 'user_123',
    'notes': 'Taking this case'
})
```

## 📚 Additional Resources

### OpenAPI Specification
- **Interactive Docs:** https://10.20.30.253:8883/docs
- **OpenAPI JSON:** https://10.20.30.253:8883/openapi.json
- **Redoc Interface:** https://10.20.30.253:8883/redoc

### SDK & Libraries
- **JavaScript SDK:** `npm install @alphabet-cartel/ash-dashboard-client`
- **Python SDK:** `pip install ash-dashboard-client`
- **C# SDK:** Available via NuGet (alpha)

### Development Resources
- **Postman Collection:** Available in repository `/docs/api/postman/`
- **API Testing Suite:** Automated tests in `/tests/api/`
- **Mock Server:** Development mock server for testing

### Support Channels
- **API Issues:** https://github.com/the-alphabet-cartel/ash-dash/issues
- **Discord Support:** https://discord.gg/alphabetcartel (#tech-support)
- **Documentation Updates:** PRs welcome for improvements

---

**This comprehensive API documentation ensures effective integration and usage of the Ash Dashboard system for crisis detection and community support operations.**