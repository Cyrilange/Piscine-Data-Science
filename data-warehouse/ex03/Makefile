VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

POSTGRES_USER := csalamit
POSTGRES_PASSWORD := mysecretpassword
POSTGRES_DB := piscineds

ENV_FILE = .env

all: install

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r requirements.txt

run: install env
	$(PYTHON) fusion.py

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

clean:
	rm -rf __pycache__

fclean: clean
	rm -rf $(VENV)

dbclean:
	psql -U csalamit -d piscineds -h localhost -c "DROP TABLE IF EXISTS customers; DROP TABLE IF EXISTS data_2023_feb;"

dbrestart: dbclean
	cd ../ex01 && make && make run && \
	cd ../ex02 && make && make run && \
	cd ../ex03 && make && make run

re: fclean all

.PHONY: all install run clean fclean dbclean dbrestart re install-psql env