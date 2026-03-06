# CI/CD Pipeline

## What is CI/CD?

- **CI (Continuous Integration)** - Automatically build and test code on every push
- **CD (Continuous Delivery)** - Automatically deploy to staging; manual approval for production
- **CD (Continuous Deployment)** - Automatically deploy all the way to production

## GitHub Actions

### Basic Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest

      - name: Run tests
        run: pytest --verbose

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff
      - run: ruff check .
```

### Build and Push Docker Image

```yaml
  build:
    needs: [test, lint]  # Run after test and lint pass
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: user/app:latest,user/app:${{ github.sha }}
```

### Deploy to Production

```yaml
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production  # Requires approval
    steps:
      - name: Deploy to server
        run: |
          ssh deploy@server "docker pull user/app:latest && docker compose up -d"
```

## Pipeline Stages

```
Code Push → Lint → Test → Build → Deploy (Staging) → Deploy (Production)
    │         │       │       │          │                    │
    └── Git   └── Static  └── Unit   └── Docker      └── Manual
        Hook      Analysis    Integration  Image         Approval
```

## Best Practices

| Practice | Why |
|----------|-----|
| Run tests in parallel | Faster feedback |
| Cache dependencies | Avoid re-downloading every run |
| Use specific versions | Reproducible builds |
| Separate environments | Staging mirrors production |
| Secret management | Never hardcode credentials |
| Branch protection | Require PR reviews + passing CI |

## Useful GitHub Actions

| Action | Purpose |
|--------|---------|
| `actions/cache@v4` | Cache pip/npm/yarn packages |
| `docker/build-push-action@v5` | Build & push Docker images |
| `actions/upload-artifact@v4` | Save build outputs |
| `peaceiris/actions-gh-pages@v4` | Deploy to GitHub Pages |
