all:
	docker compose up -d

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

clean:
	docker compose down

fclean:
	docker compose down -v

re: fclean all

.PHONY: all up down logs ps clean fclean re