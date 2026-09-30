VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

all: install

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) remove_duplicates.py

clean:
	rm -rf __pycache__

fclean: clean
	rm -rf $(VENV)
  
re: fclean all

.PHONY: all install run clean fclean re