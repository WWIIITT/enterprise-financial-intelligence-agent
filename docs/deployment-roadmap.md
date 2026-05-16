# Deployment Roadmap

## Stage 1: Local Demo

Goal: demonstrate end-to-end capability on a developer machine.

Services:

- FastAPI backend
- React frontend
- PostgreSQL
- Qdrant
- Redis

Validation:

- `GET /health`
- policy ingestion
- SEC ingestion
- macro analysis
- SQL analytics
- security check
- evaluation suite
- observability summary

## Stage 2: Single VM / Docker Compose

Goal: run a small internal demo in a controlled environment.

Add:

- Dockerized backend and frontend
- Persistent volumes for PostgreSQL and Qdrant
- Reverse proxy with TLS
- Environment variable management
- Scheduled backups

Operational checks:

- Container health checks
- PostgreSQL connectivity
- Qdrant collection availability
- SEC and FRED API connectivity
- Evaluation pass rate

Rollback:

- Keep previous container image
- Keep database backups
- Revert environment variables
- Restore Qdrant volume from snapshot if needed

## Stage 3: Managed Cloud Pilot

Goal: support a small team with stronger reliability controls.

Add:

- Managed PostgreSQL
- Managed Redis or queue service
- Hosted Qdrant or managed vector database
- Centralized logs
- Secret manager
- Basic auth or SSO
- Scheduled ingestion jobs

Monitoring:

- Request volume
- Route distribution
- Latency p50 and p95
- Error rate
- Evaluation pass rate
- Security block and mask counts
- Storage growth

## Stage 4: Production Hardening

Goal: prepare for broader enterprise use.

Add:

- RBAC and data classification
- Formal Alembic migrations
- Human approval workflow
- Model risk review process
- Retention policies
- Disaster recovery plan
- Provider fallback
- Load testing

Release controls:

- CI tests
- Evaluation gate
- Security smoke suite
- Rollback checklist
- Change approval for model or prompt changes

## Stage 5: Optional Kubernetes

Use Kubernetes only if operational complexity is justified by scale.

Good triggers:

- Multiple backend replicas are needed
- Batch ingestion workers need independent scaling
- Separate environments require consistent deployment templates
- Central platform team already operates Kubernetes

Avoid Kubernetes for the first portfolio or small pilot deployment if Docker Compose is sufficient.
