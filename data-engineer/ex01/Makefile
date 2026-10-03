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


# docker exec -e PGPASSWORD=mysecretpassword -it piscineds_postgres \
# psql -h localhost -U csalamit -d piscineds -c "\conninfo"



# PostgreSQL : 16.15
# Database and name   : piscineds
# User       : csalamit
# Password   : mysecretpassword
# Host       : localhost
# Port       : 5432

# | Champ                | Valeur               |
# | -------------------- | -------------------- |
# | Host name/address    | `piscineds_postgres` |
# | Port                 | `5432`               |
# | Maintenance database | `piscineds`          |
# | Username             | `csalamit`           |
# | Password             | `mysecretpassword`   |
