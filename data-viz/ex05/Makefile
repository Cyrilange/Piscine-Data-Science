POSTGRES_USER := csalamit
POSTGRES_PASSWORD := mysecretpassword
POSTGRES_DB := piscineds

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
ENV_FILE = .env

all: install

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r requirements.txt

run: $(VENV) env
	$(PYTHON) Clustering.py

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

re: fclean all

.PHONY: all install run install-psql env clean fclean re