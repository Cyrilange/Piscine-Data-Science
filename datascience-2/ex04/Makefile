VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

all: install

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r requirements.txt

run: $(VENV)
	$(PYTHON) Tree.py ../Train_knight.csv ../Test_knight.csv


clean:
	rm -rf __pycache__

fclean: clean
	rm -rf $(VENV)
	rm -rf *csv
	rm -rf *png
	rm -rf Tree.txt

re: fclean all

.PHONY: all install run clean fclean re