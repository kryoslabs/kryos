# Kryos API Documentation

## Overview

The Kryos API provides enterprise-grade cryptocurrency analytics and predictions through a RESTful interface. The API is designed to be self-hosted within your infrastructure.

## Authentication

All API requests require authentication using JWT tokens:

```bash
curl -H "Authorization: Bearer your-jwt-token" http://localhost:8000/api/v1/analysis
```

To obtain a token:
```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"api_key": "your-api-key"}'
```

## API Endpoints

### Market Analysis

```bash
GET /api/v1/analysis/{asset_pair}
```

Parameters:
- `asset_pair`: Trading pair (e.g., "BTC/USD")
- `timeframe`: Interval (e.g., "1h", "4h", "1d")
- `indicators`: List of required indicators

Example Response:
```json
{
  "asset": "BTC/USD",
  "timestamp": "2025-01-15T14:30:00Z",
  "analysis": {
    "regime": "bullish",
    "risk_score": 75.5,
    "sentiment": "positive",
    "technical": {
      "trend": "upward",
      "momentum": "strong",
      "volatility": "medium"
    }
  },
  "predictions": {
    "price_target": 85000.00,
    "confidence": 0.85,
    "timeframe": "24h"
  }
}
```

### Sentiment Analysis

```bash
GET /api/v1/sentiment/{asset}
```

Parameters:
- `asset`: Asset symbol (e.g., "BTC")
- `sources`: Data sources to include
- `timeframe`: Analysis period

Example Response:
```json
{
  "asset": "BTC",
  "timestamp": "2025-01-15T14:30:00Z",
  "sentiment": {
    "overall_score": 0.75,
    "sources": {
      "news": 0.82,
      "social": 0.68,
      "on_chain": 0.77
    },
    "trends": {
      "24h_change": 0.05,
      "7d_change": 0.12
    }
  }
}
```

## Rate Limits

Default rate limits (configurable):
- 100 requests per second
- 1M requests per day
- Burst capacity: 200 requests

## Error Handling

Standard error responses:
```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded",
    "details": {
      "limit": 100,
      "reset_at": "2025-01-15T14:31:00Z"
    }
  }
}
```

## Websocket API

For real-time data:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.send(JSON.stringify({
  "action": "subscribe",
  "channels": ["BTC/USD@analysis", "ETH/USD@sentiment"]
}));
```

## Client Libraries

Reference implementations:
- Python: See `clients/python/`
- JavaScript: See `clients/js/`
- Java: See `clients/java/`

## Support

For technical support and implementation assistance, please refer to the project's GitHub repository and documentation. 