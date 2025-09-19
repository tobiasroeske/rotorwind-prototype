COMPOSE=docker compose -f docker/docker-compose.yaml --env-file .env

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down -v

logs:
	$(COMPOSE) logs -f

topics:
	bash scripts/create-topics.sh
