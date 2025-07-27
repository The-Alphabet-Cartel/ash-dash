# 🔌 Ash Analytics Dashboard API Reference

Complete API documentation for ash-dash v2.1

---

## 📋 API Overview

The Ash Analytics Dashboard provides a comprehensive REST API for accessing real-time crisis detection metrics, service health information, testing results, and team management data. All endpoints return JSON responses and support standard HTTP status codes.

### **Base URL**
- **Production**: `https://10.20.30.16:8883/api`
- **Development**: `http://localhost:8883/api`

### **Authentication**
Most endpoints require authentication using JWT Bearer tokens:
```http
Authorization: Bearer your-jwt-token-here
```

### **Response Format**
All API responses follow a consistent format:
```json
{
  "success": true,
  "data": { /* response data */ },
  "timestamp": "2025-07-27T12:00:00.000Z",
  "cached": false
}
```

Error responses:
```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE",
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

---

## 🏥 Health and Status Endpoints

### **GET /health**
Check dashboard health status.

**Authentication**: None required

**Response**:
```json
{
  "status": "healthy",
  "uptime": 3600,
  "version": "2.1.0",
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

**Status Codes**:
- `200` - Dashboard is healthy
- `503` - Dashboard is experiencing issues

---

### **GET /status**
Get comprehensive system status including all integrated services.

**Authentication**: Observer role or higher

**Response**:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "services": [
      {
        "name": "ash-bot",
        "status": "healthy",
        "responseTime": 45,
        "lastCheck": "2025-07-27T12:00:00.000Z",
        "error": null
      },
      {
        "name": "nlp-server",
        "status": "healthy",
        "responseTime": 120,
        "lastCheck": "2025-07-27T12:00:00.000Z",
        "error": null
      },
      {
        "name": "testing-suite",
        "status": "healthy",
        "responseTime": 200,
        "lastCheck": "2025-07-27T12:00:00.000Z",
        "error": null
      }
    ],
    "healthyCount": 3,
    "totalCount": 3,
    "uptime": 3600
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

**Service Status Values**:
- `healthy` - Service is responding normally
- `degraded` - Service is slow but functional
- `unhealthy` - Service is not responding
- `unknown` - Service status cannot be determined

---

## 📊 Metrics Endpoints

### **GET /metrics**
Get comprehensive crisis detection and system metrics.

**Authentication**: Observer role or higher

**Query Parameters**:
- `timeRange` (optional): Time range for metrics
  - Values: `1h`, `24h`, `7d`, `30d`
  - Default: `24h`

**Example Request**:
```http
GET /api/metrics?timeRange=24h
Authorization: Bearer your-jwt-token
```

**Response**:
```json
{
  "success": true,
  "data": {
    "crisisDetection": {
      "high": 5,
      "medium": 12,
      "low": 18,
      "total": 35,
      "totalMessages": 1250,
      "accuracyRate": 0.94
    },
    "learningSystem": {
      "falsePositiveCorrections": 8,
      "falseNegativeCorrections": 3,
      "adaptationRate": 0.12,
      "totalAdjustments": 45,
      "effectivenessScore": 0.89
    },
    "testing": {
      "passRate": 0.96,
      "goalAchievement": 0.94,
      "lastRun": "2025-07-27T11:30:00.000Z",
      "failedTests": 12,
      "totalTests": 350
    },
    "performance": {
      "avgResponseTime": 180,
      "uptime": 0.999,
      "memoryUsage": 0.65,
      "cpuUsage": 0.23
    }
  },
  "timeRange": "24h",
  "timestamp": "2025-07-27T12:00:00.000Z",
  "cached": true
}
```

---

### **GET /metrics/crisis-trends**
Get detailed crisis detection trends over time.

**Authentication**: Observer role or higher

**Query Parameters**:
- `timeRange` (optional): `1h`, `24h`, `7d`, `30d` (default: `24h`)
- `granularity` (optional): `minute`, `hour`, `day` (default: auto-selected)

**Response**:
```json
{
  "success": true,
  "data": {
    "timeRange": "24h",
    "granularity": "hour",
    "data": [
      {
        "timestamp": "2025-07-27T00:00:00.000Z",
        "high": 0,
        "medium": 2,
        "low": 3,
        "total": 5,
        "messagesAnalyzed": 45
      },
      {
        "timestamp": "2025-07-27T01:00:00.000Z",
        "high": 1,
        "medium": 1,
        "low": 2,
        "total": 4,
        "messagesAnalyzed": 38
      }
    ],
    "summary": {
      "totalDetections": 156,
      "averagePerHour": 6.5,
      "peakHour": "2025-07-27T20:00:00.000Z",
      "quietHour": "2025-07-27T04:00:00.000Z"
    }
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

---

### **GET /metrics/learning-stats**
Get detailed learning system analytics.

**Authentication**: Moderator role or higher

**Response**:
```json
{
  "success": true,
  "data": {
    "overview": {
      "totalCorrections": 127,
      "accuracyImprovement": 0.15,
      "communityAdaptations": 34,
      "patternRecognition": 89
    },
    "corrections": {
      "falsePositives": {
        "total": 89,
        "thisWeek": 12,
        "categories": {
          "gaming": 23,
          "movies": 18,
          "jokes": 15,
          "other": 33
        }
      },
      "falseNegatives": {
        "total": 38,
        "thisWeek": 4,
        "categories": {
          "subtle": 15,
          "coded": 8,
          "context": 12,
          "other": 3
        }
      }
    },
    "effectiveness": {
      "beforeLearning": 0.82,
      "afterLearning": 0.94,
      "improvement": 0.12,
      "learningRate": 0.08,
      "stability": 0.96
    },
    "trends": [
      {
        "week": "2025-W30",
        "accuracy": 0.94,
        "corrections": 8,
        "newPatterns": 3
      }
    ]
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

---

## 🧪 Testing Endpoints

### **GET /testing/status**
Get current testing suite status and progress.

**Authentication**: Observer role or higher

**Response**:
```json
{
  "success": true,
  "data": {
    "currentTest": {
      "running": true,
      "type": "comprehensive",
      "startTime": "2025-07-27T11:45:00.000Z",
      "progress": 0.67,
      "estimatedCompletion": "2025-07-27T12:15:00.000Z"
    },
    "lastCompleted": {
      "type": "comprehensive",
      "completedAt": "2025-07-27T10:30:00.000Z",
      "duration": 1800,
      "passRate": 0.96,
      "status": "success"
    },
    "schedule": {
      "nextRun": "2025-07-27T18:00:00.000Z",
      "frequency": "every-6-hours",
      "enabled": true
    }
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

---

### **GET /testing/results**
Get detailed testing results and analysis.

**Authentication**: Observer role or higher

**Query Parameters**:
- `type` (optional): `comprehensive`, `quick`, `custom`
- `limit` (optional): Number of results to return (default: 10, max: 100)
- `timeRange` (optional): `24h`, `7d`, `30d`

**Response**:
```json
{
  "success": true,
  "data": {
    "latest": {
      "id": "test_20250727_103000",
      "type": "comprehensive",
      "startTime": "2025-07-27T10:30:00.000Z",
      "endTime": "2025-07-27T11:00:00.000Z",
      "duration": 1800,
      "results": {
        "totalTests": 350,
        "passed": 336,
        "failed": 14,
        "passRate": 0.96,
        "goals": {
          "achieved": 6,
          "total": 7,
          "achievementRate": 0.86
        }
      },
      "categories": [
        {
          "name": "high_priority_safety",
          "tests": 50,
          "passed": 50,
          "passRate": 1.0,
          "goalMet": true
        },
        {
          "name": "depression_detection",
          "tests": 75,
          "passed": 72,
          "passRate": 0.96,
          "goalMet": true
        }
      ],
      "failures": [
        {
          "phrase": "Test phrase example",
          "expected": "medium_crisis",
          "actual": "low_crisis",
          "category": "subtle_indicators",
          "confidence": 0.65
        }
      ]
    },
    "history": [
      {
        "id": "test_20250727_040000",
        "completedAt": "2025-07-27T04:30:00.000Z",
        "passRate": 0.94,
        "goalAchievement": 0.83
      }
    ],
    "trends": {
      "passRateTrend": 0.02,
      "averagePassRate": 0.95,
      "consistencyScore": 0.92
    }
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

---

### **POST /testing/trigger**
Manually trigger a test run.

**Authentication**: Moderator role or higher

**Request Body**:
```json
{
  "type": "comprehensive",
  "priority": "normal",
  "notify": true,
  "options": {
    "categories": ["high_priority_safety", "depression_detection"],
    "timeout": 3600
  }
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "testId": "test_20250727_120000",
    "type": "comprehensive",
    "status": "queued",
    "estimatedDuration": 1800,
    "estimatedCompletion": "2025-07-27T12:30:00.000Z",
    "queuePosition": 1
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

---

## 👥 Team Management Endpoints

### **GET /team/members**
Get active team members and their roles.

**Authentication**: Moderator role or higher

**Response**:
```json
{
  "success": true,
  "data": {
    "activeMembers": [
      {
        "id": "user_123",
        "username": "crisis_responder_1",
        "role": "moderator",
        "lastActive": "2025-07-27T11:45:00.000Z",
        "sessionDuration": 3600,
        "permissions": ["view_metrics", "trigger_tests", "export_data"]
      }
    ],
    "totalMembers": 12,
    "activeCount": 3,
    "roles": {
      "admin": 2,
      "moderator": 4,
      "observer": 6
    }
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

---

### **GET /team/activity**
Get team activity and audit log.

**Authentication**: Admin role required

**Query Parameters**:
- `limit` (optional): Number of entries (default: 50, max: 200)
- `timeRange` (optional): `1h`, `24h`, `7d`, `30d`
- `userId` (optional): Filter by specific user
- `action` (optional): Filter by action type

**Response**:
```json
{
  "success": true,
  "data": {
    "activities": [
      {
        "id": "activity_789",
        "timestamp": "2025-07-27T11:30:00.000Z",
        "userId": "user_123",
        "username": "crisis_responder_1",
        "action": "export_data",
        "details": {
          "format": "csv",
          "timeRange": "24h",
          "dataType": "crisis_metrics"
        },
        "ipAddress": "10.20.30.45",
        "userAgent": "Mozilla/5.0..."
      }
    ],
    "summary": {
      "totalActivities": 156,
      "uniqueUsers": 8,
      "mostActiveUser": "crisis_responder_1",
      "commonActions": ["view_dashboard", "export_data", "trigger_test"]
    }
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

---

## 📤 Data Export Endpoints

### **POST /export**
Export dashboard data in various formats.

**Authentication**: Observer role or higher (CSV), Moderator role or higher (detailed exports)

**Request Body**:
```json
{
  "format": "csv",
  "timeRange": "7d",
  "dataTypes": ["crisis_metrics", "learning_stats"],
  "options": {
    "includeMetadata": true,
    "compression": false,
    "delimiter": ","
  }
}
```

**Response** (Success):
```json
{
  "success": true,
  "data": {
    "exportId": "export_20250727_120000",
    "filename": "ash-dashboard-export-20250727.csv",
    "downloadUrl": "/api/export/download/export_20250727_120000",
    "expiresAt": "2025-07-28T12:00:00.000Z",
    "fileSize": 1048576,
    "recordCount": 1500
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

**Supported Formats**:
- `csv` - Comma-separated values
- `json` - JSON format
- `xlsx` - Excel format (moderator+ only)

**Available Data Types**:
- `crisis_metrics` - Crisis detection data
- `learning_stats` - Learning system statistics
- `testing_results` - Testing suite results
- `service_health` - Service health history
- `team_activity` - Team activity logs (admin only)

---

### **GET /export/download/:exportId**
Download a previously generated export file.

**Authentication**: Same role that created the export

**Response**: File download with appropriate Content-Type and Content-Disposition headers.

---

## 🔄 Real-time Updates (WebSocket)

### **Connection**
Connect to WebSocket endpoint for real-time updates:
```javascript
const socket = new WebSocket('wss://10.20.30.16:8883/ws');
```

### **Authentication**
Send authentication token after connection:
```javascript
socket.send(JSON.stringify({
  type: 'authenticate',
  token: 'your-jwt-token'
}));
```

### **Subscription**
Subscribe to specific data channels:
```javascript
socket.send(JSON.stringify({
  type: 'subscribe',
  channels: ['crisis_updates', 'health_status', 'testing_results']
}));
```

### **Available Channels**
- `crisis_updates` - Real-time crisis detection events
- `health_status` - Service health changes
- `testing_results` - Testing completion notifications
- `learning_updates` - Learning system changes
- `team_activity` - Team member activity (admin only)

### **Message Format**
```json
{
  "type": "crisis_update",
  "channel": "crisis_updates",
  "data": {
    "level": "medium",
    "timestamp": "2025-07-27T12:00:00.000Z",
    "confidence": 0.78,
    "category": "depression_indicators"
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

---

## 🔧 Service Integration Endpoints

### **GET /services/bot**
Get Ash Bot specific metrics and status.

**Authentication**: Observer role or higher

**Response**:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "responseTime": 45,
    "uptime": 7200,
    "version": "2.0.1",
    "metrics": {
      "messagesProcessed": 1250,
      "crisisDetections": 35,
      "keywordMatches": 89,
      "learningCorrections": 12
    },
    "configuration": {
      "sensitivityLevel": 0.7,
      "enabledFeatures": ["learning", "keyword_management", "crisis_detection"],
      "lastUpdate": "2025-07-27T10:00:00.000Z"
    }
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

---

### **GET /services/nlp**
Get NLP Server specific metrics and status.

**Authentication**: Observer role or higher

**Response**:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "responseTime": 120,
    "hardware": {
      "gpu": "RTX 3050",
      "gpuUtilization": 0.45,
      "memory": "64GB",
      "memoryUsage": 0.38,
      "cpu": "Ryzen 7 7700X",
      "cpuUsage": 0.23
    },
    "models": {
      "depression": {
        "loaded": true,
        "accuracy": 0.94,
        "version": "1.2.3",
        "lastUpdate": "2025-07-20T00:00:00.000Z"
      },
      "sentiment": {
        "loaded": true,
        "accuracy": 0.89,
        "version": "2.1.0",
        "lastUpdate": "2025-07-15T00:00:00.000Z"
      }
    },
    "performance": {
      "avgInferenceTime": 0.15,
      "requestsPerSecond": 12.5,
      "batchSize": 8,
      "queueLength": 2
    }
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

---

### **GET /services/testing**
Get Testing Suite specific status and metrics.

**Authentication**: Observer role or higher

**Response**:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "responseTime": 200,
    "currentTest": null,
    "statistics": {
      "testsRunToday": 4,
      "averagePassRate": 0.95,
      "totalPhrases": 350,
      "categoriesActive": 7,
      "lastFullTest": "2025-07-27T10:30:00.000Z"
    },
    "configuration": {
      "scheduleEnabled": true,
      "frequency": "every-6-hours",
      "timeout": 3600,
      "retryAttempts": 3,
      "notifications": true
    }
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

---

## ⚠️ Error Codes and Troubleshooting

### **HTTP Status Codes**
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (authentication required)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `429` - Too Many Requests (rate limited)
- `500` - Internal Server Error
- `503` - Service Unavailable

### **Error Response Format**
```json
{
  "success": false,
  "error": "Detailed error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "Specific field error",
    "suggestion": "How to fix the error"
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

### **Common Error Codes**

#### **Authentication Errors**
- `AUTH_TOKEN_MISSING` - Authorization header not provided
- `AUTH_TOKEN_INVALID` - JWT token is invalid or expired
- `AUTH_TOKEN_EXPIRED` - Token has expired, refresh required
- `AUTH_INSUFFICIENT_PERMISSIONS` - User role lacks required permissions

#### **Validation Errors**
- `VALIDATION_FAILED` - Request data validation failed
- `INVALID_TIME_RANGE` - Time range parameter is invalid
- `INVALID_FORMAT` - Export format not supported
- `MISSING_REQUIRED_FIELD` - Required field missing from request

#### **Service Errors**
- `SERVICE_UNAVAILABLE` - External service (Bot, NLP, Testing) is down
- `SERVICE_TIMEOUT` - Service request timed out
- `SERVICE_ERROR` - External service returned an error

#### **Rate Limiting**
- `RATE_LIMIT_EXCEEDED` - Too many requests, try again later
- `EXPORT_LIMIT_EXCEEDED` - Too many export requests

#### **Data Errors**
- `DATA_NOT_FOUND` - Requested data does not exist
- `DATA_EXPORT_FAILED` - Export generation failed
- `CACHE_ERROR` - Cache operation failed

### **Error Handling Examples**

#### **Authentication Error**
```json
{
  "success": false,
  "error": "Authentication required",
  "code": "AUTH_TOKEN_MISSING",
  "details": {
    "suggestion": "Include 'Authorization: Bearer <token>' header"
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

#### **Validation Error**
```json
{
  "success": false,
  "error": "Validation failed",
  "code": "VALIDATION_FAILED",
  "details": {
    "timeRange": "Must be one of: 1h, 24h, 7d, 30d",
    "format": "Must be one of: csv, json, xlsx"
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

#### **Service Unavailable**
```json
{
  "success": false,
  "error": "NLP Server is currently unavailable",
  "code": "SERVICE_UNAVAILABLE",
  "details": {
    "service": "nlp-server",
    "lastSeen": "2025-07-27T11:45:00.000Z",
    "suggestion": "Try again in a few minutes or contact support"
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

---

## 🔧 Rate Limiting

### **Rate Limit Headers**
All responses include rate limiting headers:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1627389600
X-RateLimit-Window: 900
```

### **Rate Limits by Endpoint Category**

#### **General API Endpoints**
- **Limit**: 200 requests per 15 minutes
- **Applies to**: Most GET endpoints, health checks

#### **Export Endpoints**
- **Limit**: 10 exports per 15 minutes
- **Applies to**: `/export` POST requests
- **Note**: Large exports count as multiple requests

#### **Testing Endpoints**
- **Limit**: 5 test triggers per hour
- **Applies to**: `/testing/trigger` POST requests
- **Note**: Admin users have higher limits

#### **Authentication Endpoints**
- **Limit**: 5 attempts per 15 minutes
- **Applies to**: Login, token refresh
- **Note**: Failed attempts count toward limit

### **Rate Limit Bypass**
Certain scenarios bypass rate limits:
- Health check endpoints (`/health`)
- WebSocket connections (different limits apply)
- Trusted IP addresses (configurable)
- Emergency override tokens (admin only)

---

## 🔐 Authentication and Authorization

### **JWT Token Structure**
```json
{
  "userId": "user_123",
  "username": "crisis_responder_1",
  "role": "moderator",
  "permissions": [
    "view_metrics",
    "export_data",
    "trigger_tests"
  ],
  "iat": 1627389600,
  "exp": 1627476000
}
```

### **Role-Based Permissions**

#### **Observer Role**
- View dashboard and metrics
- Export basic data (CSV format)
- Access real-time updates
- View service health status

**API Access**:
- `GET /health` ✅
- `GET /status` ✅
- `GET /metrics` ✅
- `GET /testing/status` ✅
- `GET /testing/results` ✅
- `POST /export` ✅ (CSV only)

#### **Moderator Role**
- All Observer permissions
- Trigger manual tests
- Access detailed analytics
- Export advanced data formats
- View team activity (limited)

**Additional API Access**:
- `POST /testing/trigger` ✅
- `GET /metrics/learning-stats` ✅
- `POST /export` ✅ (all formats)
- `GET /team/members` ✅

#### **Admin Role**
- All Moderator permissions
- Manage team members
- Access audit logs
- System configuration
- Emergency overrides

**Additional API Access**:
- `GET /team/activity` ✅
- `POST /team/notifications` ✅
- `GET /admin/logs` ✅
- `POST /admin/config` ✅

### **Permission Checks**
Each endpoint validates permissions:
```javascript
// Example permission validation
if (!user.permissions.includes('trigger_tests') && user.role !== 'admin') {
  return res.status(403).json({
    success: false,
    error: "Insufficient permissions",
    code: "AUTH_INSUFFICIENT_PERMISSIONS",
    required: "trigger_tests",
    current: user.permissions
  });
}
```

---

## 📡 WebSocket API Reference

### **Connection Lifecycle**

#### **1. Connect**
```javascript
const ws = new WebSocket('wss://10.20.30.16:8883/ws');

ws.onopen = function() {
  console.log('WebSocket connected');
  // Send authentication
  ws.send(JSON.stringify({
    type: 'authenticate',
    token: localStorage.getItem('jwt_token')
  }));
};
```

#### **2. Authenticate**
```javascript
// Send authentication message
{
  "type": "authenticate",
  "token": "your.jwt.token"
}

// Response
{
  "type": "auth_response",
  "success": true,
  "userId": "user_123",
  "role": "moderator"
}
```

#### **3. Subscribe to Channels**
```javascript
// Subscribe to specific channels
{
  "type": "subscribe",
  "channels": ["crisis_updates", "health_status"]
}

// Response
{
  "type": "subscription_response",
  "success": true,
  "channels": ["crisis_updates", "health_status"]
}
```

### **Message Types**

#### **Crisis Updates**
```javascript
{
  "type": "crisis_update",
  "channel": "crisis_updates",
  "data": {
    "id": "crisis_789",
    "level": "high",
    "confidence": 0.92,
    "timestamp": "2025-07-27T12:00:00.000Z",
    "category": "immediate_danger",
    "source": "ash-bot",
    "userId": "discord_user_456" // Only for admin users
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

#### **Health Status Updates**
```javascript
{
  "type": "health_update",
  "channel": "health_status",
  "data": {
    "service": "nlp-server",
    "status": "degraded",
    "previousStatus": "healthy",
    "responseTime": 450,
    "error": "High GPU utilization",
    "timestamp": "2025-07-27T12:00:00.000Z"
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

#### **Testing Results**
```javascript
{
  "type": "test_update",
  "channel": "testing_results",
  "data": {
    "testId": "test_20250727_120000",
    "status": "completed",
    "passRate": 0.94,
    "duration": 1800,
    "failedTests": 21,
    "goalAchievement": 0.89,
    "timestamp": "2025-07-27T12:00:00.000Z"
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

#### **Learning System Updates**
```javascript
{
  "type": "learning_update",
  "channel": "learning_updates",
  "data": {
    "type": "false_positive_correction",
    "category": "gaming_references",
    "pattern": "respawn",
    "adjustment": -0.15,
    "userId": "user_123",
    "timestamp": "2025-07-27T12:00:00.000Z"
  },
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

### **Client Heartbeat**
```javascript
// Send every 30 seconds to maintain connection
{
  "type": "ping"
}

// Server response
{
  "type": "pong",
  "timestamp": "2025-07-27T12:00:00.000Z"
}
```

### **Error Handling**
```javascript
{
  "type": "error",
  "error": "Invalid channel subscription",
  "code": "INVALID_CHANNEL",
  "details": {
    "channel": "admin_only_channel",
    "requiredRole": "admin",
    "currentRole": "moderator"
  }
}
```

---

## 🧪 Testing the API

### **Using cURL**

#### **Basic Health Check**
```bash
curl -X GET "https://10.20.30.16:8883/api/health" \
  -H "Accept: application/json" \
  -k  # Ignore SSL certificate warnings
```

#### **Authenticated Request**
```bash
curl -X GET "https://10.20.30.16:8883/api/metrics?timeRange=24h" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json" \
  -k
```

#### **POST Request (Export Data)**
```bash
curl -X POST "https://10.20.30.16:8883/api/export" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "format": "csv",
    "timeRange": "7d",
    "dataTypes": ["crisis_metrics"]
  }' \
  -k
```

### **Using JavaScript (Fetch API)**

#### **GET Request with Error Handling**
```javascript
async function getMetrics(timeRange = '24h') {
  try {
    const response = await fetch(`/api/metrics?timeRange=${timeRange}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Request failed');
    }

    const data = await response.json();
    return data.data;
  } catch (error) {
    console.error('Failed to fetch metrics:', error);
    throw error;
  }
}
```

#### **POST Request with File Download**
```javascript
async function exportData(options) {
  try {
    const response = await fetch('/api/export', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(options)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error);
    }

    const result = await response.json();
    
    // Download the file
    const downloadResponse = await fetch(result.data.downloadUrl, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
      }
    });

    const blob = await downloadResponse.blob();
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = result.data.filename;
    a.click();
    
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Export failed:', error);
    throw error;
  }
}
```

### **Using Python (Requests)**

#### **API Client Class**
```python
import requests
import json
from typing import Optional, Dict, Any

class AshDashboardAPI:
    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.verify = False  # For self-signed certificates
        
        if token:
            self.session.headers.update({
                'Authorization': f'Bearer {token}'
            })

    def get_health(self) -> Dict[str, Any]:
        """Get dashboard health status."""
        response = self.session.get(f'{self.base_url}/api/health')
        response.raise_for_status()
        return response.json()

    def get_metrics(self, time_range: str = '24h') -> Dict[str, Any]:
        """Get comprehensive metrics."""
        response = self.session.get(
            f'{self.base_url}/api/metrics',
            params={'timeRange': time_range}
        )
        response.raise_for_status()
        return response.json()['data']

    def export_data(self, format_type: str = 'csv', 
                   time_range: str = '24h',
                   data_types: list = None) -> str:
        """Export data and return download URL."""
        if data_types is None:
            data_types = ['crisis_metrics']
            
        payload = {
            'format': format_type,
            'timeRange': time_range,
            'dataTypes': data_types
        }
        
        response = self.session.post(
            f'{self.base_url}/api/export',
            json=payload
        )
        response.raise_for_status()
        
        return response.json()['data']['downloadUrl']

# Usage example
api = AshDashboardAPI('https://10.20.30.16:8883', 'your-jwt-token')

# Get health status
health = api.get_health()
print(f"Dashboard status: {health['status']}")

# Get metrics
metrics = api.get_metrics('7d')
print(f"Crisis detections: {metrics['crisisDetection']['total']}")
```

---

## 📚 SDK and Integration Examples

### **JavaScript SDK**

#### **Dashboard Client**
```javascript
class AshDashboardClient {
  constructor(baseUrl, options = {}) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.token = options.token;
    this.timeout = options.timeout || 30000;
    this.ws = null;
    this.eventListeners = new Map();
  }

  async authenticate(token) {
    this.token = token;
    // Verify token is valid
    try {
      await this.getHealth();
      return true;
    } catch (error) {
      this.token = null;
      throw new Error('Authentication failed');
    }
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}/api${endpoint}`;
    const config = {
      timeout: this.timeout,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    };

    if (this.token) {
      config.headers.Authorization = `Bearer ${this.token}`;
    }

    const response = await fetch(url, config);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Request failed');
    }

    return response.json();
  }

  // API Methods
  async getHealth() {
    const response = await fetch(`${this.baseUrl}/api/health`);
    return response.json();
  }

  async getStatus() {
    return this.request('/status');
  }

  async getMetrics(timeRange = '24h') {
    return this.request(`/metrics?timeRange=${timeRange}`);
  }

  async getTesting() {
    return this.request('/testing/status');
  }

  async exportData(options) {
    return this.request('/export', {
      method: 'POST',
      body: JSON.stringify(options)
    });
  }

  // WebSocket Methods
  connectWebSocket() {
    const wsUrl = this.baseUrl.replace(/^http/, 'ws') + '/ws';
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      if (this.token) {
        this.ws.send(JSON.stringify({
          type: 'authenticate',
          token: this.token
        }));
      }
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleWebSocketMessage(message);
    };

    this.ws.onclose = () => {
      // Attempt reconnection
      setTimeout(() => this.connectWebSocket(), 5000);
    };
  }

  subscribe(channels) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'subscribe',
        channels: Array.isArray(channels) ? channels : [channels]
      }));
    }
  }

  on(event, callback) {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, []);
    }
    this.eventListeners.get(event).push(callback);
  }

  handleWebSocketMessage(message) {
    const listeners = this.eventListeners.get(message.type);
    if (listeners) {
      listeners.forEach(callback => callback(message.data));
    }
  }
}

// Usage Example
const dashboard = new AshDashboardClient('https://10.20.30.16:8883');

// Authenticate
await dashboard.authenticate('your-jwt-token');

// Get metrics
const metrics = await dashboard.getMetrics('24h');
console.log('Crisis detections:', metrics.data.crisisDetection);

// Connect WebSocket for real-time updates
dashboard.connectWebSocket();
dashboard.subscribe(['crisis_updates', 'health_status']);

dashboard.on('crisis_update', (data) => {
  console.log('New crisis detected:', data);
});

dashboard.on('health_update', (data) => {
  console.log('Service health changed:', data);
});
```

---

## 🚀 Best Practices

### **API Usage Guidelines**

#### **Authentication**
- Always include authentication headers for protected endpoints
- Refresh tokens before they expire
- Handle authentication errors gracefully
- Store tokens securely (avoid localStorage for sensitive data)

#### **Error Handling**
- Always check response status codes
- Parse error responses for detailed information
- Implement retry logic for temporary failures
- Log errors for debugging but don't expose sensitive information

#### **Performance**
- Use appropriate time ranges to avoid large data transfers
- Cache responses when appropriate
- Use WebSockets for real-time data instead of polling
- Implement request throttling to respect rate limits

#### **Data Export**
- Request only necessary data types
- Use appropriate formats (CSV for spreadsheets, JSON for processing)
- Handle large exports asynchronously
- Clean up downloaded files to save storage

### **Integration Patterns**

#### **Polling vs WebSockets**
```javascript
// ❌ Don't poll for real-time data
setInterval(async () => {
  const metrics = await dashboard.getMetrics();
  updateDashboard(metrics.data);
}, 5000); // Inefficient and hits rate limits

// ✅ Use WebSockets for real-time updates
dashboard.connectWebSocket();
dashboard.on('crisis_update', updateCrisisDisplay);
dashboard.on('health_update', updateServiceStatus);
```

#### **Graceful Degradation**
```javascript
async function getMetricsWithFallback(timeRange) {
  try {
    // Try to get real-time data
    return await dashboard.getMetrics(timeRange);
  } catch (error) {
    if (error.code === 'SERVICE_UNAVAILABLE') {
      // Fall back to cached data
      return getCachedMetrics(timeRange);
    }
    throw error;
  }
}
```

#### **Batch Operations**
```javascript
// ❌ Don't make multiple individual requests
for (const service of services) {
  await dashboard.getServiceHealth(service);
}

// ✅ Use combined endpoints
const status = await dashboard.getStatus(); // Gets all services
```

---

## 📖 Additional Resources

### **API Postman Collection**
A Postman collection is available with pre-configured requests:
- Import URL: `https://10.20.30.16:8883/api/postman-collection.json`
- Includes environment variables for easy testing
- Pre-request scripts for authentication

### **OpenAPI Specification**
- **Specification**: Available at `/api/openapi.json`
- **Interactive Docs**: Available at `/api/docs`
- **Swagger UI**: Browse and test API endpoints

### **Code Examples Repository**
Complete integration examples available in the project repository:
- `examples/javascript/` - Frontend integration examples
- `examples/python/` - Python SDK and scripts
- `examples/curl/` - cURL command examples
- `examples/postman/` - Postman collection and environments

### **Support and Community**
- **GitHub Issues**: Report bugs and request features
- **Discord #tech-support**: Real-time community support
- **Documentation**: Comprehensive guides in `/docs` directory
- **API Updates**: Follow repository releases for API changes

---

*This API documentation is part of the ash-dash v2.1 documentation suite. For user guides, see [Team Guide](team_guide.md). For technical implementation, see [Implementation Guide](implementation.md).*
  "