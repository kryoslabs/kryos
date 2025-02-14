# Getting Started with Kryos

This guide will help you set up and run Kryos on your infrastructure.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 15+
- Redis 7+
- Apache Kafka 3.5+

## Installation Methods

### 1. Docker Installation (Recommended)

The fastest way to get started with Kryos is using Docker:

```bash
# Clone the repository
git clone https://github.com/yourusername/kryos.git
cd kryos

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Download pre-trained models
mkdir -p models
curl -o models/market_analysis.pt https://github.com/yourusername/kryos/releases/download/v0.1.0/market_analysis.pt
curl -o models/sentiment_analysis.pt https://github.com/yourusername/kryos/releases/download/v0.1.0/sentiment_analysis.pt

# Start all services
docker-compose up -d

# Initialize the database
docker-compose exec api poetry run python -m kryos db upgrade

# Create initial admin user
docker-compose exec api poetry run python -m kryos users create-admin

# Check services status
docker-compose ps
```

### 2. Manual Installation

For development or custom deployments:

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Download pre-trained models
mkdir -p models
curl -o models/market_analysis.pt https://github.com/yourusername/kryos/releases/download/v0.1.0/market_analysis.pt
curl -o models/sentiment_analysis.pt https://github.com/yourusername/kryos/releases/download/v0.1.0/sentiment_analysis.pt

# Initialize database
poetry run python -m kryos db upgrade

# Create initial admin user
poetry run python -m kryos users create-admin

# Start the application
poetry run python -m kryos
```

## Configuration

### Essential Environment Variables

```bash
# API Keys (Required)
BINANCE_API_KEY=your-binance-api-key
BINANCE_SECRET_KEY=your-binance-secret-key
COINMARKETCAP_API_KEY=your-coinmarketcap-api-key
COINGECKO_API_KEY=your-coingecko-api-key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/kryos

# Redis Cache
REDIS_URL=redis://localhost:6379/0

# Kafka
KAFKA_BROKERS=localhost:9092

# Security
SECRET_KEY=your-secret-key  # Generate using: openssl rand -hex 32
JWT_SECRET_KEY=your-jwt-key # Generate using: openssl rand -hex 32
```

### Security Configuration

1. Generate secure keys:
```bash
openssl rand -hex 32 # For SECRET_KEY
openssl rand -hex 32 # For JWT_SECRET_KEY
```

2. Update your `.env` file with these values.

## Verification

1. Check the health endpoint:
```bash
curl http://localhost:8000/health
```

2. Create an API key:
```bash
# Using the admin interface
curl -X POST http://localhost:8000/api/v1/admin/apikeys \
  -H "Authorization: Bearer your-admin-token" \
  -H "Content-Type: application/json" \
  -d '{"name": "test-key", "expires_at": "2024-12-31T23:59:59Z"}'
```

3. Test the API:
```bash
# Get an access token
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"api_key": "your-api-key"}'

# Test market analysis
curl http://localhost:8000/api/v1/analysis/BTC-USD \
  -H "Authorization: Bearer your-access-token"
```

4. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Next Steps

- Review the [API Documentation](api/README.md)
- Learn about [Deployment Options](deployment/README.md)
- Understand the [Model Architecture](models/README.md)

## Troubleshooting

Common issues and solutions:

1. **Connection Errors**
   - Verify all services are running: `docker-compose ps`
   - Check service logs: `docker-compose logs -f [service_name]`
   - Ensure correct ports are exposed
   - Check firewall settings

2. **Authentication Issues**
   - Verify admin user creation was successful
   - Check API key generation and permissions
   - Validate JWT token configuration
   - Verify environment variables are properly set

3. **Performance Issues**
   - Monitor resource usage: `docker stats`
   - Check Redis cache configuration
   - Verify database connection pool settings
   - Monitor Kafka consumer lag

4. **Model Loading Issues**
   - Verify model files are downloaded correctly
   - Check model file permissions
   - Ensure GPU drivers are installed (if using GPU)
   - Monitor GPU memory usage

## Support

For technical support and implementation assistance, please refer to the project's documentation and GitHub repository. 
