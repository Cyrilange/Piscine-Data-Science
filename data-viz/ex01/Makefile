VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

all: install

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r requirements.txt

run: $(VENV)
	$(PYTHON) chart.py

install-psql:
	mkdir -p $(HOME)/bin
	printf '#!/bin/sh\nexec docker exec -it piscineds_postgres psql "$$@"\n' > $(HOME)/bin/psql
	chmod +x $(HOME)/bin/psql


clean:
	rm -rf __pycache__

fclean: clean
	rm -rf $(VENV)

re: fclean all

.PHONY: all install run clean fclean re