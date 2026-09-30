VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

all: install

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) automatic_table.py

clean:
	rm -rf __pycache__

fclean: clean
	rm -rf $(VENV)

dbclean:
	psql -U csalamit -d piscineds -h localhost -W -c "DROP TABLE IF EXISTS data_2022_dec, data_2022_nov, data_2022_oct, data_2023_jan;"

re: fclean all

reset: dbclean re

.PHONY: all install run clean fclean dbclean re reset