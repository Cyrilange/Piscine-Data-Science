COMPOSE = docker compose

POSTGRES_USER := csalamit
POSTGRES_PASSWORD := mysecretpassword
POSTGRES_DB := piscineds

ENV_FILE := .env

.PHONY: all up down restart logs ps clean fclean reset install-psql env

all: up

up: env
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

logs:
	$(COMPOSE) logs -f postgres

ps:
	$(COMPOSE) ps

clean:
	$(COMPOSE) down

fclean:
	$(COMPOSE) down -v

install-psql:
	mkdir -p $(HOME)/bin
	printf '#!/bin/sh\nexec docker exec -it piscineds_postgres psql "$$@"\n' > $(HOME)/bin/psql
	chmod +x $(HOME)/bin/psql

env:
	@echo "Creating $(ENV_FILE)..."
	@printf 'POSTGRES_USER=%s\n' "$(POSTGRES_USER)" > $(ENV_FILE)
	@printf 'POSTGRES_PASSWORD=%s\n' "$(POSTGRES_PASSWORD)" >> $(ENV_FILE)
	@printf 'POSTGRES_DB=%s\n' "$(POSTGRES_DB)" >> $(ENV_FILE)
	@echo "$(ENV_FILE) created."

reset: fclean up
