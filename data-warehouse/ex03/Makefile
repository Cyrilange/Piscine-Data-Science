VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

all: install

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) fusion.py

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

.PHONY: all install run clean fclean dbclean dbrestart re