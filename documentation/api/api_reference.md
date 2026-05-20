# KaliGhost API Reference

This document provides a comprehensive reference for the KaliGhost RESTful API and WebSocket interfaces, enabling developers to integrate with and extend the KaliGhost platform.

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [RESTful API Endpoints](#restful-api-endpoints)
   - [Agent Management](#agent-management)
   - [Tool Operations](#tool-operations)
   - [Reporting](#reporting)
   - [Configuration](#configuration)
4. [WebSocket API](#websocket-api)
5. [Data Models](#data-models)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)

## Overview

The KaliGhost API provides programmatic access to the platform's core functionalities, including AI agent control, security tool orchestration, and automated reporting. The API follows RESTful principles and uses JSON for request/response payloads.

Base URL: `http://localhost:8080/api/v1`

## Authentication

Most API endpoints require authentication. KaliGhost supports multiple authentication methods:

### API Key Authentication

Include your API key in the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

### OAuth 2.0

For browser-based applications, OAuth 2.0 with Authorization Code flow is supported:

```
Authorization: Bearer ACCESS_TOKEN
```

### Session Authentication

Web application sessions use cookie-based authentication after successful login.

## RESTful API Endpoints

### Agent Management

#### Get Agent Status

```
GET /agent/status
```

Returns the current status of the YrYs AI agent.

**Response:**
```json
{
  "status": "running",
  "uptime": "2h30m",
  "autonomy_level": 100,
  "active_sessions": 5,
  "model_info": {
    "primary": "claude-3-sonnet",
    "fallback": "llama3:70b"
  }
}
```

#### Process Natural Language Request

```
POST /agent/process
```

Submit a natural language request for the agent to process.

**Request Body:**
```json
{
  "text": "Scan the network 192.168.1.0/24",
  "context": {
    "project_id": "proj-123",
    "client_name": "Acme Corp"
  },
  "preferences": {
    "verbose": true,
    "format": "json"
  }
}
```

**Response:**
```json
{
  "task_id": "task-12345",
  "estimated_time": "5m",
  "tools_required": ["nmap", "masscan"],
  "confidence": 0.95
}
```

#### Get Task Status

```
GET /agent/task/{task_id}
```

Retrieve the status and results of a previously submitted task.

**Response:**
```json
{
  "status": "completed",
  "progress": 100,
  "result": {
    "hosts_found": 25,
    "open_ports": [
      {"host": "192.168.1.100", "port": 80, "service": "http"},
      {"host": "192.168.1.100", "port": 443, "service": "https"}
    ]
  },
  "findings": [
    {
      "id": "finding-001",
      "title": "Open HTTP Server Detected",
      "severity": "medium",
      "description": "Web server accessible on standard port"
    }
  ]
}
```

#### Update Agent Configuration

```
PUT /agent/config
```

Update agent configuration parameters.

**Request Body:**
```json
{
  "autonomy_level": 80,
  "max_parallel_tools": 4,
  "timeout_per_tool": 300
}
```

**Response:**
```json
{
  "success": true,
  "message": "Configuration updated successfully"
}
```

### Tool Operations

#### List Available Tools

```
GET /tools
```

List all security tools available in the KaliGhost environment.

**Response:**
```json
{
  "available_tools": [
    {
      "name": "nmap",
      "version": "7.93",
      "category": "scanner",
      "status": "installed",
      "description": "Network discovery and security auditing tool"
    },
    {
      "name": "sqlmap",
      "version": "1.7",
      "category": "exploitation",
      "status": "installed",
      "description": "Automatic SQL injection and database takeover tool"
    }
  ]
}
```

#### Execute Tool

```
POST /tools/{tool_name}/execute
```

Execute a security tool with specified parameters.

**Request Body:**
```json
{
  "arguments": ["-sV", "192.168.1.100"],
  "timeout": 300,
  "async": true,
  "context": {
    "project_id": "proj-123"
  }
}
```

**Response:**
```json
{
  "execution_id": "exec-67890",
  "status": "started",
  "estimated_completion": "45s"
}
```

#### Get Execution Status

```
GET /tools/executions/{execution_id}
```

Retrieve the status and output of a tool execution.

**Response:**
```json
{
  "status": "completed",
  "output": "# Nmap 7.93 scan initiated...",
  "return_code": 0,
  "duration": "45s",
  "parsed_results": {
    "hosts_scanned": 1,
    "open_ports": [
      {"port": 22, "protocol": "tcp", "service": "ssh"},
      {"port": 80, "protocol": "tcp", "service": "http"}
    ]
  }
}
```

### Reporting

#### Generate Report

```
POST /reports/generate
```

Generate a security assessment report in specified format.

**Request Body:**
```json
{
  "template": "executive_summary",
  "data": {
    "findings": [...],
    "scan_results": {...}
  },
  "format": "pdf",
  "delivery": {
    "email": "analyst@company.com",
    "webhook": "https://company.com/reports"
  }
}
```

**Response:**
```json
{
  "report_id": "rep-54321",
  "estimated_completion": "30s",
  "download_url": "/api/v1/reports/rep-54321/download"
}
```

#### Download Report

```
GET /reports/{report_id}/download?format=pdf
```

Download a generated report in specified format.

**Response:**
Binary content with appropriate Content-Type header.

#### List Reports

```
GET /reports
```

Get a list of available reports.

**Query Parameters:**
- `limit`: Number of reports to return (default: 10)
- `offset`: Offset for pagination (default: 0)
- `format`: Filter by format (pdf, html, json)

**Response:**
```json
{
  "reports": [
    {
      "id": "rep-54321",
      "title": "Network Security Assessment - Acme Corp",
      "created_at": "2026-05-15T14:30:00Z",
      "formats_available": ["pdf", "html", "json"],
      "size_bytes": 1024000
    }
  ],
  "total_count": 1
}
```

### Configuration

#### Get Current Configuration

```
GET /config
```

Retrieve the current agent configuration.

**Response:**
```json
{
  "agent": {
    "name": "YrYs",
    "mode": "AUTO",
    "autonomy_level": 100,
    "language": "es"
  },
  "aws": {
    "region": "us-east-1",
    "bedrock": {
      "enabled": true
    }
  },
  "tools": {
    "nmap": true,
    "sqlmap": true
  }
}
```

#### Update Configuration

```
PUT /config
```

Update specific configuration parameters.

**Request Body:**
```json
{
  "agent": {
    "autonomy_level": 80
  },
  "tools": {
    "burpsuite": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "updated_sections": ["agent", "tools"]
}
```

## WebSocket API

The WebSocket API provides real-time updates and bidirectional communication with the KaliGhost platform.

### Connection Endpoint

```
ws://localhost:8080/api/v1/ws
```

### Client Initialization

To establish a WebSocket connection:

```javascript
const ws = new WebSocket('ws://localhost:8080/api/v1/ws');

ws.onopen = function(event) {
    // Subscribe to channels of interest
    ws.send(JSON.stringify({
        "action": "subscribe",
        "channels": ["agent_status", "task_progress"]
    }));
};

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    // Handle incoming messages
};
```

### Available Channels

- **agent_status**: Agent state changes (idle, busy, error)
- **task_progress**: Progress updates for running tasks
- **finding_detected**: New security findings discovered
- **tool_executing**: Tool start/stop notifications
- **report_ready**: Generated report availability

### Message Format

All messages follow a consistent format:

```json
{
  "type": "event_type",
  "timestamp": "2026-05-15T14:30:00.123Z",
  "data": {...}
}
```

Example messages:

```json
{
  "type": "task_progress",
  "timestamp": "2026-05-15T14:30:15.456Z",
  "data": {
    "task_id": "task-12345",
    "progress": 65,
    "current_step": "Executing nmap scan"
  }
}
```

```json
{
  "type": "finding_detected",
  "timestamp": "2026-05-15T14:32:10.789Z",
  "data": {
    "finding": {
      "id": "finding-002",
      "title": "SSH Service Detected",
      "severity": "low",
      "host": "192.168.1.100",
      "port": 22
    }
  }
}
```

## Data Models

### SecurityFinding

```json
{
  "id": "string (UUID)",
  "title": "string (max 256 chars)",
  "description": "string",
  "severity": "enum[critical, high, medium, low, informational]",
  "cvss_score": "number (0-10)",
  "affected_assets": ["string"],
  "remediation": "string",
  "references": ["URI strings"],
  "detected_at": "ISO 8601 date-time",
  "tool_used": "string",
  "confidence": "number (0-1)"
}
```

### AssessmentTask

```json
{
  "id": "string (UUID)",
  "name": "string",
  "description": "string",
  "scope": {
    "targets": ["string"],
    "exclusions": ["string"]
  },
  "strategy": {
    "phases": ["reconnaissance", "scanning", ...],
    "tools": ["string"]
  },
  "schedule": {
    "start_time": "ISO 8601 date-time",
    "repeat": "string pattern"
  }
}
```

### ToolExecution

```json
{
  "id": "string (UUID)",
  "tool_name": "string",
  "arguments": ["string"],
  "status": "enum[pending, running, completed, failed]",
  "start_time": "ISO 8601 date-time",
  "end_time": "ISO 8601 date-time",
  "output": "string",
  "return_code": "integer",
  "duration_seconds": "number"
}
```

## Error Handling

All API responses follow standard HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error
- 503: Service Unavailable

Error responses include a JSON body with details:

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "The provided input is invalid",
    "details": {
      "field": "text",
      "reason": "Field is required"
    }
  }
}
```

## Rate Limiting

API requests are subject to rate limiting to ensure fair usage:

- **Anonymous users**: 100 requests/hour
- **Authenticated users**: 1,000 requests/hour
- **Premium subscribers**: 10,000 requests/hour

Rate limit headers are included in all responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 995
X-RateLimit-Reset: 1678886400
```

When a rate limit is exceeded, the API returns a 429 status code with a JSON error response.

---
© 2026 KaliGhost Project. All rights reserved.