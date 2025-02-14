# Deployment Guide

## Infrastructure Requirements

### Minimum Requirements
- 8 CPU cores
- 32GB RAM
- 100GB SSD
- NVIDIA GPU (Optional)

### Recommended Setup
- 32 CPU cores
- 128GB RAM
- 500GB NVMe SSD
- NVIDIA A100 GPU

## Deployment Options

### 1. Docker Deployment

```bash
# Production deployment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# With GPU support
docker-compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
```

### 2. Kubernetes Deployment

```bash
# Deploy using Helm
helm install kryos ./charts/kryos \
  --namespace kryos \
  --create-namespace \
  --values values.yaml
```

Example `values.yaml`:
```yaml
replicas:
  api: 3
  worker: 5
  inference: 2

resources:
  api:
    limits:
      cpu: 4
      memory: 8Gi
  inference:
    limits:
      cpu: 8
      memory: 16Gi
      nvidia.com/gpu: 1

persistence:
  size: 100Gi
  storageClass: standard

monitoring:
  enabled: true
  prometheus:
    retention: 30d
```

## Security Configuration

### SSL/TLS Setup

1. Generate certificates:
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/kryos.key \
  -out /etc/ssl/certs/kryos.crt
```

2. Configure NGINX:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/ssl/certs/kryos.crt;
    ssl_certificate_key /etc/ssl/private/kryos.key;
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

### Firewall Configuration

```bash
# Allow API access
ufw allow 443/tcp

# Allow monitoring
ufw allow from 10.0.0.0/8 to any port 9090
```

## Monitoring Setup

### Prometheus Configuration

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'kryos'
    static_configs:
      - targets: ['localhost:8000']
```

### Grafana Dashboards

Pre-configured dashboards available at:
- `dashboards/api-metrics.json`
- `dashboards/model-performance.json`
- `dashboards/system-metrics.json`

## Backup Strategy

### Database Backups

```bash
# Automated backup script
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump -U kryos -d kryos > backup_${TIMESTAMP}.sql
```

### Model Checkpoints

Models are automatically backed up:
- Daily incremental backups
- Weekly full backups
- 30-day retention

## Scaling Guidelines

### Horizontal Scaling

```bash
# Scale API servers
kubectl scale deployment kryos-api --replicas=5

# Scale workers
kubectl scale deployment kryos-worker --replicas=10
```

### Vertical Scaling

Recommended resource allocation:
- API Servers: 4 CPU, 8GB RAM per instance
- Workers: 8 CPU, 16GB RAM per instance
- Inference Servers: 8 CPU, 16GB RAM, 1 GPU per instance

## Troubleshooting

Common issues and solutions:

1. **High Latency**
   - Check resource utilization
   - Verify network connectivity
   - Monitor database performance

2. **Memory Issues**
   - Adjust JVM heap size
   - Configure Redis memory limits
   - Review memory leak monitoring

3. **GPU Problems**
   - Update NVIDIA drivers
   - Check CUDA compatibility
   - Monitor GPU memory usage 