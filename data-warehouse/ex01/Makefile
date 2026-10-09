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
	$(PYTHON) customers_table.py

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
	psql -U csalamit -d piscineds -h localhost -W -c "DROP TABLE IF EXISTS customers;"

re: fclean all

reset: dbclean re

.PHONY: all install run clean fclean dbclean re reset install-psql env