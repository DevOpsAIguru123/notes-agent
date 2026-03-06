# Docker Guide

## Core Concepts

- **Image** - A read-only template with application code and dependencies
- **Container** - A running instance of an image
- **Volume** - Persistent storage that survives container restarts
- **Network** - Communication channel between containers

## Essential Commands

```bash
# Images
docker build -t myapp:latest .
docker images
docker pull nginx:alpine
docker rmi image_name

# Containers
docker run -d -p 8080:80 --name web nginx
docker ps                    # Running containers
docker ps -a                 # All containers
docker logs -f web           # Follow logs
docker exec -it web sh       # Shell into container
docker stop web && docker rm web

# Cleanup
docker system prune -a       # Remove unused everything
```

## Dockerfile Best Practices

```dockerfile
# Use specific base image tags
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency files first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Use non-root user
RUN adduser --disabled-password appuser
USER appuser

# Expose port and set entrypoint
EXPOSE 8000
CMD ["python", "app.py"]
```

!!! tip "Layer Caching"
    Order Dockerfile instructions from least to most frequently changed. Dependencies change less often than source code, so install them first.

## Docker Compose

```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./src:/app/src

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

```bash
docker compose up -d          # Start all services
docker compose logs -f web    # Follow web logs
docker compose down -v        # Stop and remove volumes
```

## Multi-Stage Builds

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

This produces a much smaller final image since build tools aren't included.

## MCP Server in Docker

The Model Context Protocol (MCP) lets AI assistants connect to external tools and data sources. Running MCP servers in Docker keeps them isolated and portable.

### Basic MCP Server Dockerfile

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

### Docker Compose with MCP Server

```yaml
services:
  mcp-server:
    build: ./mcp-server
    ports:
      - "3000:3000"
    environment:
      - MCP_TRANSPORT=sse
      - API_KEY=${API_KEY}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### Streamable HTTP Transport (Recommended)

```yaml
services:
  mcp-server:
    build: .
    ports:
      - "3000:3000"
    environment:
      - MCP_TRANSPORT=streamable-http
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 10s
      retries: 3
```

### SSE Transport

```yaml
services:
  mcp-server:
    build: .
    ports:
      - "8080:8080"
    environment:
      - MCP_TRANSPORT=sse
      - SSE_ENDPOINT=/sse
      - MESSAGE_ENDPOINT=/messages
```

### Connecting to MCP Server

Point your MCP client config at the containerized server:

```json
{
  "mcpServers": {
    "my-server": {
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

For SSE transport, use the `/sse` endpoint instead.

!!! tip "Networking"
    When running multiple MCP servers in Docker Compose, use Docker's internal networking so containers communicate by service name (e.g., `http://mcp-server:3000`) rather than `localhost`.

### Security Considerations

- Never bake API keys into images — use environment variables or Docker secrets
- Run as non-root user inside the container
- Use read-only volumes where possible (`./data:/app/data:ro`)
- Limit container capabilities with `--cap-drop ALL`
