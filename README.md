# Cloud-Native Multi-Region Disaster Recovery Platform

A portfolio project that starts as a small FastAPI service and will be progressively extended into a production-style AWS disaster recovery platform.

## Current stage

This first version provides:

- FastAPI REST API
- Health endpoint for cloud health checks
- Region/version identification
- User CRUD basics
- SQLAlchemy database layer
- Local SQLite database
- Automated API tests
- Docker containerization
- Environment-based configuration

## Planned architecture

```text
                    USERS
                      |
                      v
                  Route 53
                 /         \
                v           v
        PRIMARY REGION    DR REGION
          AWS Region A      AWS Region B
              |                 |
              v                 v
          Load Balancer     Load Balancer
              |                 |
              v                 v
             EKS               EKS
              |                 |
              v                 v
         Application       Application
              |                 |
              +-------> Database / Backup
              |
              v
             S3
```

## Run locally

### 1. Create a virtual environment

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r app/requirements.txt
```

### 3. Start the API

```bash
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/status
- http://127.0.0.1:8000/docs

The `/docs` page provides an interactive Swagger UI.

## Test the API

Create a user:

```bash
curl -X POST http://127.0.0.1:8000/users ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Jagrat\",\"email\":\"jagrat@example.com\"}"
```

On Linux/macOS:

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Jagrat","email":"jagrat@example.com"}'
```

List users:

```bash
curl http://127.0.0.1:8000/users
```

## Run tests

From the project root:

```bash
pytest -q
```

## Run with Docker

Build:

```bash
docker build -t cloud-dr-api .
```

Run:

```bash
docker run --rm -p 8000:8000 \
  -e AWS_REGION=local-docker \
  cloud-dr-api
```

Then open:

http://127.0.0.1:8000/status

## Region simulation

The application deliberately reads its region from an environment variable.

Primary:

```bash
AWS_REGION=ap-south-1
```

DR:

```bash
AWS_REGION=ap-south-2
```

This lets us later deploy the same container image in two AWS regions and verify which environment is serving traffic.

## Security notes

- Never commit `.env` files or AWS credentials.
- Database credentials will be moved to AWS Secrets Manager when we introduce RDS.
- The database will eventually be placed in private subnets.
- IAM roles will use least-privilege permissions.

## Roadmap

1. Local FastAPI application
2. Docker
3. AWS networking
4. Amazon RDS
5. Amazon EKS
6. Terraform infrastructure
7. Secondary AWS region
8. Backup/replication strategy
9. Route 53 health checks and failover
10. CloudWatch monitoring and alerts
11. GitHub Actions CI/CD
12. Disaster simulation
13. RTO/RPO measurement
14. Production-quality documentation

## Important

This is a learning/portfolio project. The DR claims and RTO/RPO values should only be reported after they are actually tested.
