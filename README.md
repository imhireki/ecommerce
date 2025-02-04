## Setup development environment

### 1. Fill in a `.env` file using the `.env.example`

### 2. Build and start the containers
```bash
docker compose up -d --build  
```

### 3. Run database migrations
```bash
docker compose exec backend python3 manage.py makemigrations order product notification
docker compose exec backend python3 manage.py migrate  
```

### 4. Restart celery beat to apply its migrations
```bash
docker compose restart celery_beat
```

## Start/Stop services
```bash
docker compose up -d
docker compose down
```

## Run tests
```bash
docker compose exec backend pytest
```

## See logs
```bash
docker compose logs -f
docker compose logs celery_worker -f
```
