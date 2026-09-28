all: up

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

ps:
	docker compose ps

clean:
	docker compose down

fclean:
	docker compose down -v

.PHONY: all up down restart logs ps clean fclean