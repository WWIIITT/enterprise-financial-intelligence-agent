# Local Runbook

## Start Infrastructure

```powershell
docker compose -f infra\docker-compose.yml up -d
```

## Start Backend

```powershell
.\.venv\Scripts\Activate.ps1
cd backend
..\.venv\Scripts\python -m uvicorn app.main:app
```

## Start Frontend Dashboard

```powershell
cd frontend
npm install
npm run dev
```

## Start Knowledge Site Locally

```powershell
cd site
npm install
npm run docs:dev
```

## Run Tests

```powershell
.\.venv\Scripts\python -m pytest
cd frontend
npm run build
cd ..\site
npm run docs:build
```
